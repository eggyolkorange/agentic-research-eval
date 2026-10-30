## Testing the Gemini connection

python -c
```
from dotenv import load_dotenv      # tool that reads the .env file
load_dotenv()                       # load GOOGLE_API_KEY and GEMINI_MODEL into the environment

import os                           # lets Python read environment variables
from google import genai            # Google's Gemini library

c = genai.Client(api_key=os.environ['GOOGLE_API_KEY'])   # connect to Gemini with your key

response = c.models.generate_content(
    model=os.environ['GEMINI_MODEL'],   # the model name you saved in .env
    contents='Say hi in 3 words',       # the message sent to the model
)
print(response.text)                    # show the model's reply
```

python -c allows us to run the code IN THE TERMINAL with the quotes

---

## Learning points

Run one company:
```
python -m agent.workflow --ticker JPM               # Reviewer + approval
python -m agent.workflow --ticker JPM --no-review   # baseline
```

### Gemini free tier
- Model names change: `gemini-2.5-flash` has been retired (404), so always list the models first instead of guessing.
- Under load, calls can take 3 to 5 minutes and return `503 UNAVAILABLE` ("high demand"). This is temporary, not a bug in the code: retry with a growing wait (5s, 10s, 20s...). `_llm()` in `agent/workflow.py` does this.
- Plan Phase 3 around this: 10 companies × 2 setups, plus review rounds, can take hours. Run it off-peak.

### Getting reliable output from the LLM
- Pass a Pydantic model as `response_schema` with `response_mime_type="application/json"`. Gemini then has to reply in that shape, and `model_validate_json` checks it. That avoids having to parse messy text.
- `temperature=0` makes runs more repeatable, which matters when comparing two setups.
- Fixed fields (`revenue`, `net_income`, `price_change_1y`, each with `value`, `period` and `source`) make every number easy to score against `ground_truth.csv`.
- Ask for units explicitly ("USD millions"). The raw data is in USD, so wrong units is a likely error type.

### The Reviewer
- The Reviewer is just a second LLM call with the draft AND the source data, asked to list what doesn't match. An empty list means pass.
- Test it with a planted error: changing JPM net income 57,048 → 75,048 was caught, with the right number quoted back.
- On a correct brief it returned no flags, so there were no false alarms in that test.
- Limitation: the same model drafts and reviews, so it may share the drafter's blind spots. Worth saying in the memo.
- The redraft loop is capped at 2 retries so a stubborn flag can't loop forever. Flags are logged to `eval/flags.csv` for scoring.

### Results so far
- JPM baseline (no Reviewer) was already 3/3 correct. With clean, small data, the baseline may score high, so the Reviewer's value may show up more in made-up claims and units/period errors than in headline accuracy.

### Git
- `.env` holds the API key: never commit it (`.gitignore` blocks it).
- Rewriting a commit that's already pushed (e.g. to change its message) needs `git push --force-with-lease`. That's fine on a solo repo, risky on a shared one. Fixing a message before pushing (`git commit --amend`) avoids the problem.