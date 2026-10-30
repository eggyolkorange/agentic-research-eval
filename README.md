# Agentic Equity Research Assistant: Prototype and Evaluation

**Data snapshot:** 20 Oct 2026 (yfinance) | **Model:** Google Gemini 3.8 Flash, free tier (set in `.env` as `GEMINI_MODEL`)

**Status:** agent built and tested on one company (JPM); full evaluation across 10 companies in progress.

An AI agent that drafts one-page research briefs on listed companies, with a
**Reviewer step** that checks every number against the source data and a
**human approval step** before a brief is final. The project measures how much
the Reviewer step improves accuracy.

## Headline result
> _To fill in:_ Across 10 companies, the Reviewer step raised factual accuracy from __% to __% and cut made-up figures by __%.

## How it works
Ticker -> Fetch data (`eval/snapshot.json`) -> Draft brief (LLM + Pydantic) -> Reviewer (supported?) -> Human approval -> Final brief

1. **Fetch** reads the company's frozen data from `eval/snapshot.json`.
2. **Draft** asks Gemini to fill a fixed brief (revenue, net income, 1-year price change, summary, key risk) using only that data, citing the data field behind each number. The reply is forced into JSON and validated with Pydantic (`agent/schema.py`).
3. **Reviewer** gives a second Gemini call the draft and the data, and asks it to list every claim that is wrong or unsupported (number, units, period, company).
4. **Redraft loop:** if there are flags, the draft goes back with the flags, at most 2 times. Every flag is logged to `eval/flags.csv`.
5. **Human approval:** the final brief is printed and saved only if you approve it.

The `--no-review` switch stops after step 2, giving the baseline for comparison.

Example check: when the JPM brief's net income was changed from $57,048m to $75,048m, the Reviewer flagged it with the correct figure from the data.

## Results
| Setup | Accuracy | Made-up claims | Tool errors | Avg cost per brief |
|---|---|---|---|---|
| Baseline (no Reviewer) | | | | |
| With Reviewer + human approval | | | | |

### Errors by type
| Error type | Baseline | With Reviewer |
|---|---|---|
| Wrong period | | |
| Wrong units | | |
| Calculation | | |
| Wrong company | | |
| Made up | | |
| Tool failure | | |

## Run it
Requires Python 3.11+ and a free Gemini API key from [Google AI Studio](https://aistudio.google.com).

```bash
git clone https://github.com/eggyolkorange/agentic-research-eval.git
cd agentic-research-eval
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env           # Windows (Mac/Linux: cp .env.example .env)
# open .env and add your GOOGLE_API_KEY and GEMINI_MODEL
python -m agent.workflow --ticker JPM               # with Reviewer + approval -> briefs/JPM_reviewed.json
python -m agent.workflow --ticker JPM --no-review   # baseline -> briefs/JPM_baseline.json
```

On the free tier each Gemini call can take several minutes and may return "high demand" (503) errors; the workflow retries these automatically.

The data snapshot (`eval/snapshot.json`) is already included, so results can be reproduced.
Only run `python -m tools.snapshot` if you deliberately want fresh data: it overwrites the snapshot and the ground truth.

## Repo layout
- `agent/workflow.py` fetch, draft, review loop, human approval, `--no-review` baseline
- `agent/schema.py` brief and reviewer-flag schemas
- `tools/data.py` fetches company data from yfinance
- `tools/snapshot.py` takes the one-off frozen data snapshot and builds the ground truth
- `tools/mcp_server.py` serves company data as an MCP tool (stretch)
- `eval/snapshot.json` frozen data the agent reads
- `eval/ground_truth.csv` correct answers, spot-checked against annual reports
- `eval/results.csv` scored results
- `eval/flags.csv` every Reviewer flag (ticker, attempt, claim, reason), created on first run
- `briefs/` generated briefs (`<TICKER>_baseline.json`, `<TICKER>_reviewed.json`)
- `reports/` findings memo

## Limitations
- Small test set: 10 US-listed companies, 3 facts each
- One model (Gemini 3.8 Flash, free tier), used both to draft and to review, so the Reviewer may share the drafter's blind spots
- Companies have different fiscal year ends (e.g. Apple Sep, Microsoft Jun, Nvidia Jan), so "latest year" is not the same period for every company
- Price changes are the 12 months up to the snapshot date (20 Oct 2026)
- This is strictly a research prototype, not investment advice

## Findings memo
See [reports/findings_memo.md](reports/findings_memo.md).
