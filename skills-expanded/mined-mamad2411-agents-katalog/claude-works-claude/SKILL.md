# CLAUDE.md

Claude Works is an MCP server (FastMCP, stdio) exposing a job-application
pipeline as typed tools. The honesty policy lives in the modules, not in
prompts: hard caps in scoring, gate findings in the resume tools, fill-and-park
plans in submission. Do not move policy into docstrings or prompt text.

Companion docs, read before the matching work: **PLAYBOOK.md** (every per-ATS
form-driving lesson; read it before executing a submission plan with
Playwright), **OPERATING.md** (the loop's operating model: queue-first gate,
hard walls, de-dup semantics, cadence). To onboard a new candidate end to end,
run the bundled **/setup** command.

## Standing rule: append lessons in the same session

When you discover a better way to fill or submit a form (a new ATS, a
selector, a validator trick, a submit-blocker), append it to PLAYBOOK.md AND,
in terse generic form, to `submission.py`'s `ATS_GOTCHAS` (tests green, no
PII, no em dashes) before the session ends. When a skip reveals a pattern, add
it to `curation.py`'s filters. This is how the system remembers; do not wait
to be asked.

## Commands

```bash
pip install -e ".[dev]"          # dev install
ruff check . && mypy && pytest   # the exact checks CI runs (no network needed)
python -m claude_works           # run the server over stdio
```

Demo mode (all 14 tools work offline, from this clone):

```bash
JOBSEARCH_DATA_DIR="$PWD/examples" \
JOBSEARCH_RESUMES_DIR="$PWD/examples/resumes" \
python -m claude_works
```

## Setting it up for a user

Prefer the bundled `/setup` command: it interviews the user for example jobs +
their resume and derives everything below from those examples. The manual
outline:

1. `pip install claude-works` (PyPI) or `pip install -e .` from a clone.
2. Create a data directory for their search (ledger, queue, and policy live
   there; empty is fine, readers degrade gracefully).
3. Copy `examples/policy.sample.json` to `<data dir>/policy.json` and edit it
   WITH them: their excluded companies, skill gaps, level terms, scoring
   vocabulary, curation lanes. The defaults are one specific candidate's
   policy; never let a new user run on them.
4. Register the server (identity is env-only; nothing personal is in code):

   ```bash
   claude mcp add claude-works \
     -e JOBSEARCH_DATA_DIR="/path/to/their/data" \
     -e JOBSEARCH_APPLY_NAME="Their Name" \
     -e JOBSEARCH_APPLY_EMAIL="them@example.com" \
     -e JOBSEARCH_APPLY_LINKEDIN="linkedin.com/in/them" \
     -e JOBSEARCH_APPLY_GITHUB="github.com/them" \
     -- claude-works
   ```

5. For the resume tools: copy `examples/resumes/_genlib.py` into their
   `JOBSEARCH_RESUMES_DIR` and replace every fragment with claims that are
   true of THEM. Never invent fragments; the anti-fabrication gate exists to
   catch exactly that.
6. Smoke-test: `score_job` on an over-level title (expect a hard cap),
   `curate_queue`, `submit_application` (expect a plan, not a submission).

Discovery that works out of the box: the default `boards` source (public
Ashby/Greenhouse/Lever posting APIs over the user's `seed_boards`), the
JobDataLake MCP for the wide net, and the offline `demo` source. Only the
`newsource`/`board_harvest` sources wrap private scripts that do not ship.

## Architecture

`models.py` holds the five dataclasses (`SearchAngle -> Job -> Score -> Resume
-> Application`); everything crossing a tool boundary is one of them via
`to_dict`. `server.py` is the only module that imports `mcp`; the rest is
stdlib-only and must stay that way. `config.py` resolves paths, rails, and the
per-candidate `policy.json` AT IMPORT, so config changes need a server
relaunch (tests use `Rails.from_env(policy=...)` or subprocesses). Per-ATS
form tactics accrete in `submission.py`'s `ATS_GOTCHAS`; append new gotchas
there, never rewrite history.

## Gotchas

- `examples/` fixtures are live data in demo mode: demo runs append to
  `examples/applications.json` and write HTML/PDF into `examples/resumes/`.
  Restore the fixtures (`git checkout examples/`) before committing.
- `examples/policy.sample.json` is deliberately NOT named `policy.json`;
  demo mode would auto-load it and change demo behavior (and break tests).
- De-dup semantics differ by layer on purpose: tracker/discovery de-dup by
  ROLE (`role_key`); curation parks whole already-applied COMPANIES.
- Ledger writes must stay flock-locked and atomic (`tracker.py`); parallel
  loop instances share the file.
- Release = `gh release create vX.Y.Z` after bumping the version in
  `pyproject.toml`; publish.yml handles PyPI via trusted publishing (OIDC,
  environment `pypi`, no token).
- No em dashes anywhere in this repo, code or prose.
