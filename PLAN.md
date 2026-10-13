# Plan: Agentic Equity Research Assistant

**Goal:** show that a Reviewer step makes an AI research agent more accurate.
**Headline result to fill in:** the Reviewer step raised accuracy from __% to __%.
**Finish by:** Fri 23 Oct 2026 | **Apply to Dymon by:** 30 Oct (aim for 24 or 25 Oct)

Tick boxes as you go (`- [x]`) and commit once a day.

## Phase 1: Setup + data (Wed 14 to Thu 15 Oct)
- [ ] Create an empty GitHub repo and push this folder
- [ ] Create a Python environment and run `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env` and add your LLM API key
- [ ] Get `tools/data.py` working for 3 tickers
- [ ] Fill `eval/ground_truth.csv`: 5 true facts for each of the 15 companies
- **Done when:** data loads and the fact sheet is complete

## Phase 2: Build (Fri 16 to Sun 18 Oct)
- [ ] `agent/schema.py`: the brief's fields (Pydantic)
- [ ] `agent/workflow.py`: Fetch -> Draft -> Reviewer -> Human approval (LangGraph)
- [ ] Reviewer sends unsupported claims back for a redraft, and logs each flag
- [ ] Works end to end on 1 company
- [ ] Stretch: serve the data through `tools/mcp_server.py`
- **Done when:** one full brief is produced and saved in `briefs/`

## Phase 3: Test (Mon 19 to Wed 21 Oct)
- [ ] Run all 15 companies WITHOUT the Reviewer (baseline)
- [ ] Run all 15 companies WITH the Reviewer
- [ ] Score each brief against `eval/ground_truth.csv` and record it in `eval/results.csv`
- [ ] Tag every error by type (wrong period, wrong units, calculation, wrong company, made up, tool failure)
- **Done when:** the results table is filled in

## Phase 4: Write up (Thu 22 to Fri 23 Oct)
- [ ] Fill in the README (results table and workflow picture)
- [ ] Write `reports/findings_memo.md` (1 to 2 pages): what you tested, results, errors, risks, verdict
- [ ] Make the repo public and pin it on your GitHub profile
- [ ] Add the project and resume bullet to your AI & Data Science resume
- **Done when:** a recruiter can understand the project in 2 minutes

## If you fall behind
- LangGraph too slow to learn: use plain Python functions and mention LangGraph as next step
- MCP not working: skip it, keep a note in the README
- Behind on 20 Oct: cut to 10 companies and 3 facts each

## Daily log (one line a day, useful for feedback)
- 14 Oct:
