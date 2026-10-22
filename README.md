# Agentic Equity Research Assistant: Prototype and Evaluation

**Data snapshot:** 20 Oct 2026 (yfinance) | **Model:** Google Gemini, free tier (name set in `.env` as `GEMINI_MODEL`)

An AI agent that drafts one-page research briefs on listed companies, with a
**Reviewer step** that checks every number against the source data and a
**human approval step** before a brief is final. The project measures how much
the Reviewer step improves accuracy.

## Headline result
> _To fill in:_ Across 10 companies, the Reviewer step raised factual accuracy from __% to __% and cut made-up figures by __%.

## How it works
Ticker -> Fetch data (`eval/snapshot.json`) -> Draft brief (LLM + Pydantic) -> Reviewer (supported?) -> Human approval -> Final brief

Unsupported claims are sent back for a redraft and logged for evaluation.

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
python -m agent.workflow --ticker JPM
```

The data snapshot (`eval/snapshot.json`) is already included, so results can be reproduced.
Only run `python -m tools.snapshot` if you deliberately want fresh data: it overwrites the snapshot and the ground truth.

## Repo layout
- `agent/` workflow and brief schema
- `tools/data.py` fetches company data from yfinance
- `tools/snapshot.py` takes the one-off frozen data snapshot and builds the ground truth
- `tools/mcp_server.py` serves company data as an MCP tool (stretch)
- `eval/snapshot.json` frozen data the agent reads
- `eval/ground_truth.csv` correct answers, spot-checked against annual reports
- `eval/results.csv` scored results
- `briefs/` sample outputs
- `reports/` findings memo

## Limitations
- Small test set: 10 US-listed companies, 3 facts each
- One model (Gemini, free tier)
- Companies have different fiscal year ends (e.g. Apple Sep, Microsoft Jun, Nvidia Jan), so "latest year" is not the same period for every company
- Price changes are the 12 months up to the snapshot date (20 Oct 2026)
- This is strictly a research prototype, not investment advice

## Findings memo
See [reports/findings_memo.md](reports/findings_memo.md).
