# Plan: Agentic Equity Research Assistant

**Goal:** show that a Reviewer step makes an AI research agent more accurate.
**Headline result to fill in:** the Reviewer step raised accuracy from __% to __%.

**Core scope:** 10 companies, 3 facts each (revenue, net income, 1-year price change).
**Stretch:** 15 companies, 5 facts each, MCP server, LangGraph.

Tick boxes as you go (`- [x]`) and commit after every work session.

---

## Phase 1: Setup and data

**Goal:** reliable data for every company, plus the true answers to check the AI against.

1. Open a terminal in the project folder and turn on the environment
    - [ ] `.venv\Scripts\Activate.ps1` (you should see `(.venv)`)
2. Test the data script
    - [ ] Run `python -m tools.data`
    - [ ] Check it prints 3 lines (JPM, AAPL, KO) with a name, fiscal year end and price change
3. Add your API key
    - [ ] Open `.env` and paste your key after `ANTHROPIC_API_KEY=` (or `OPENAI_API_KEY=`)
    - [ ] Never commit `.env` (it is already blocked by `.gitignore`)
4. Choose your companies
    - [ ] Keep 10 tickers in `eval/ground_truth.csv` (e.g. JPM, BAC, GS, AAPL, MSFT, NVDA, KO, PG, WMT, MCD) and delete the other rows
5. Write down the true answers (ground truth)
    - [ ] For each company, fill in: fiscal year, revenue, net income, 1-year price change
    - [ ] Take them from the same source the agent uses (run `get_company_data` and copy the numbers), then spot-check 2 or 3 against the company's annual report
    - [ ] Note your source in `source_notes`
6. Save
    - [ ] Commit and push

**Done when:** the data script works and `ground_truth.csv` is filled for all 10 companies.

---

## Phase 2: Build the agent

**Goal:** one company goes all the way from ticker to approved brief.

Build it one step at a time in `agent/workflow.py`, testing each step before the next.

1. Define the brief
    - [ ] In `agent/schema.py`, add fields for revenue, net income and price change, each with a source
2. Fetch
    - [ ] `fetch()` calls `get_company_data(ticker)` and returns the data
3. Draft
    - [ ] `draft()` sends the data to the LLM and asks it to fill the brief using ONLY that data
    - [ ] Test on JPM and print the result
    - [ ] Save the output to `briefs/JPM_baseline.json`
4. Review
    - [ ] `review()` sends the draft AND the data to the LLM and asks: "List every claim that does not match the data or has no source"
    - [ ] It returns a list of flags (an empty list means pass)
    - [ ] Test it by editing a draft to include a wrong number, and check the Reviewer catches it
5. Loop
    - [ ] If there are flags, send the draft back to `draft()` with the flags, at most 2 times
    - [ ] Log every flag (ticker, claim, reason) to a file
6. Human approval
    - [ ] Print the final brief and ask "Approve? (y/n)"
    - [ ] Save approved briefs to `briefs/<TICKER>_reviewed.json`
7. Baseline switch
    - [ ] `--no-review` skips steps 4 to 6, so you can run the comparison
8. Save
    - [ ] Commit and push

**Done when:** `python -m agent.workflow --ticker JPM` produces a reviewed, approved brief, and `--no-review` produces a baseline one.

**Stretch (only if Phase 2 is done early):**
- [ ] Rewrite the steps as a LangGraph graph (same logic, named nodes)
- [ ] Run `tools/mcp_server.py` and fetch data through it

---

## Phase 3: Test

**Goal:** real numbers comparing the two setups.

1. Run the baseline
    - [ ] Run every company with `--no-review`
2. Run the full workflow
    - [ ] Run every company with the Reviewer and your approval
3. Score each brief against `eval/ground_truth.csv`
    - [ ] Add one row per company per setup to `eval/results.csv`
    - [ ] `facts_correct` out of `facts_checked` (3 per brief)
    - [ ] `made_up_claims`: numbers with no support in the data
    - [ ] `reviewer_flags` and `reviewer_false_alarms` (correct numbers it wrongly flagged)
    - [ ] `tool_errors`, `human_edits`, rough `cost_usd` and `seconds`
4. Tag every error by type in `error_types`
    - [ ] wrong period, wrong units, calculation, wrong company, made up, tool failure
5. Work out the totals
    - [ ] Accuracy % for each setup (total correct / total checked)
    - [ ] Count of each error type for each setup
6. Pick 2 examples for the write-up
    - [ ] One brief where the Reviewer caught a real error
    - [ ] One where it missed something or raised a false alarm
7. Save
    - [ ] Commit and push

**Done when:** `results.csv` is complete and you have your headline accuracy numbers.

---

## Phase 4: Write up

**Goal:** a recruiter understands the project in 2 minutes.

1. README
    - [ ] Fill in the headline result and both results tables
    - [ ] Add the limitations (small test set, one model, free data, not investment advice)
2. Findings memo (`reports/findings_memo.md`, 1 to 2 pages)
    - [ ] Bottom line: one sentence with your headline number
    - [ ] What was tested and how
    - [ ] Results table
    - [ ] Where it fails, with your 2 examples
    - [ ] Risks (made-up numbers, stale data, people over-trusting it) and the controls that help
    - [ ] Verdict: good for first drafts with a human check, not for unsupervised use
3. Publish
    - [ ] Commit and push
    - [ ] Check the repo is public, add the description and topics, and pin it on your profile
4. Resume
    - [ ] Add the project to your AI & Data Science resume with your real numbers and the GitHub link

**Done when:** the repo is public, pinned, and on your resume.

---

## If you fall behind

- **LangGraph is slow to learn:** keep plain Python functions; mention LangGraph as a next step
- **MCP does not work:** skip it and note it in the README
- **The LLM output is messy:** ask it to reply in JSON only, and validate it with the Pydantic schema
- **Still behind before Phase 3:** cut to 6 companies; keep both setups, since the comparison is the point

## Work log (one line per session, helps with feedback)

-
