# Agentic Equity Research Assistant: Prototype and Evaluation

An AI agent that drafts one-page research briefs on listed companies, with a
**Reviewer step** that checks every number against the source data and a
**human approval step** before a brief is final. The project measures how much
the Reviewer step improves accuracy.

## Headline result
> _To fill in:_ Across 15 companies, the Reviewer step raised factual accuracy from __% to __% and cut made-up figures by __%.

## How it works
Ticker -> Fetch data (yfinance, SEC EDGAR) -> Draft brief (LLM + Pydantic) -> Reviewer (supported?) -> Human approval -> Final brief

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
```bash
pip install -r requirements.txt
cp .env.example .env   # add your API key
python -m agent.workflow --ticker JPM
```

## Repo layout
- `agent/` workflow and brief schema
- `tools/` data fetchers and MCP server
- `eval/` ground truth and scored results
- `briefs/` sample outputs
- `reports/` findings memo

## Limitations
_To fill in: data gaps, small test set, one model, not for investment decisions._

## Findings memo
See [reports/findings_memo.md](reports/findings_memo.md).
