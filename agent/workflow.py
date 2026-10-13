"""Fetch -> Draft -> Reviewer -> Human approval, as a LangGraph graph.

Build order:
1. Get draft() working for one ticker.
2. Add review(): compare each claim with the fetched data, return flags.
3. Add the loop: if flags, redraft; else go to human approval.
4. Add a --no-review flag for the baseline run.
"""
import argparse


def fetch(ticker: str) -> dict:
    # TODO: call tools.data.get_company_data(ticker)
    raise NotImplementedError


def draft(data: dict) -> dict:
    # TODO: prompt the LLM to fill agent.schema.Brief using ONLY the data given
    raise NotImplementedError


def review(brief: dict, data: dict) -> list[str]:
    # TODO: return a list of unsupported or wrong claims (empty list = pass)
    raise NotImplementedError


def human_approval(brief: dict) -> bool:
    print(brief)
    return input("Approve? (y/n) ").strip().lower() == "y"


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", required=True)
    p.add_argument("--no-review", action="store_true", help="baseline run")
    args = p.parse_args()
    # TODO: wire the steps together with LangGraph
