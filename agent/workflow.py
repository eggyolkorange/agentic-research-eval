"""Fetch -> Draft -> Reviewer -> Human approval.

Plain Python functions (LangGraph is a stretch goal).
`--no-review` stops after the first draft and saves a baseline brief.
"""
import argparse
import csv
import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from agent.schema import Brief, Review

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
MAX_REDRAFTS = 2
FLAG_LOG = ROOT / "eval" / "flags.csv"

_client = None


def _llm(prompt: str, schema):
    """Call Gemini and return the reply parsed into `schema`."""
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    for attempt in range(5):
        try:
            resp = _client.models.generate_content(
                model=os.environ["GEMINI_MODEL"],
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0,
                ),
            )
            return schema.model_validate_json(resp.text)
        except errors.ServerError:  # 503 "high demand" is common on the free tier
            if attempt == 4:
                raise
            time.sleep(5 * 2**attempt)


def fetch(ticker: str) -> dict:
    snapshot = json.loads((ROOT / "eval" / "snapshot.json").read_text())
    if ticker not in snapshot:
        raise SystemExit(f"{ticker} is not in eval/snapshot.json")
    return snapshot[ticker]


def draft(data: dict, flags: list | None = None, previous: dict | None = None) -> dict:
    prompt = (
        "You are an equity research assistant. Fill in the research brief for this company "
        "using ONLY the data below. Do not use outside knowledge. Statement values are in USD; "
        "report revenue and net income in USD millions, and price change in percent. "
        "Cite the exact data field for each number.\n\n"
        f"DATA:\n{json.dumps(data, indent=1)}\n"
    )
    if flags:
        prompt += (
            f"\nYour previous draft:\n{json.dumps(previous, indent=1)}\n\n"
            "A reviewer flagged these problems. Fix them using the data:\n"
            + "\n".join(f"- {f['claim']}: {f['reason']}" for f in flags)
        )
    return _llm(prompt, Brief).model_dump()


def review(brief: dict, data: dict) -> list[dict]:
    prompt = (
        "You are a strict fact-checker. Compare the brief with the source data. "
        "List every claim that does not match the data or has no source in the data. "
        "Check each number, its units (USD millions vs USD), its period and its company. "
        "Do not flag claims that are correct. If everything matches, return an empty list.\n\n"
        f"DATA:\n{json.dumps(data, indent=1)}\n\nBRIEF:\n{json.dumps(brief, indent=1)}"
    )
    return [f.model_dump() for f in _llm(prompt, Review).flags]


def log_flags(ticker: str, attempt: int, flags: list[dict]) -> None:
    new = not FLAG_LOG.exists()
    with FLAG_LOG.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ticker", "attempt", "claim", "reason"])
        for fl in flags:
            w.writerow([ticker, attempt, fl["claim"], fl["reason"]])


def human_approval(brief: dict) -> bool:
    print(json.dumps(brief, indent=2))
    return input("Approve? (y/n) ").strip().lower() == "y"


def save(brief: dict, ticker: str, suffix: str) -> Path:
    path = ROOT / "briefs" / f"{ticker}_{suffix}.json"
    path.write_text(json.dumps(brief, indent=2))
    return path


def run(ticker: str, no_review: bool) -> None:
    start = time.time()
    data = fetch(ticker)
    brief = draft(data)

    if no_review:
        print(f"Saved {save(brief, ticker, 'baseline')} ({time.time() - start:.1f}s)")
        return

    for attempt in range(MAX_REDRAFTS + 1):
        flags = review(brief, data)
        if not flags:
            break
        log_flags(ticker, attempt, flags)
        print(f"Attempt {attempt}: {len(flags)} flag(s)")
        for fl in flags:
            print(f"  - {fl['claim']}: {fl['reason']}")
        if attempt < MAX_REDRAFTS:
            brief = draft(data, flags, brief)
    else:
        print("Warning: flags remain after the last redraft")

    if human_approval(brief):
        print(f"Saved {save(brief, ticker, 'reviewed')} ({time.time() - start:.1f}s)")
    else:
        print("Not approved; nothing saved.")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", required=True)
    p.add_argument("--no-review", action="store_true", help="baseline run")
    args = p.parse_args()
    run(args.ticker.upper(), args.no_review)
