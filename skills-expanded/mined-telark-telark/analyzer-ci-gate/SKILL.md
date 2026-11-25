---
name: analyzer-ci-gate
description: Use before reporting any change to the Python analyzer service (services/analyzer) as done. Reproduces its CI job locally, covering the syntax check, the two-process pytest run and the combined coverage floor.
---

# Analyzer CI gate

Goal: `services/analyzer` passes the `analyzer` job in `.github/workflows/ci.yaml`. That job is the source of truth for the Python version, the test file lists and the coverage floor; copy from it when it differs from the commands below.

## Commands

```sh
cd services/analyzer
VENV="${TMPDIR:-/tmp}/analyzer-venv"   # outside the service: compileall walks every subdirectory
python3 -m venv "$VENV"
"$VENV/bin/pip" install --require-hashes -r requirements-test.txt

"$VENV/bin/python" -m compileall -q .
"$VENV/bin/python" -m pytest --cov=. --cov-report= tests/test_*_cov.py -q
"$VENV/bin/python" -m pytest --cov=. --cov-append --cov-report= <real-dependency suites listed in ci.yaml> -q
"$VENV/bin/python" -m coverage report --fail-under=<floor from ci.yaml>
```

## What to check

- The stub-based suites (`tests/test_*_cov.py`) run in their own process, apart from the suites that use real dependencies; `--cov-append` then combines both into one coverage gate. The split is historical: no suite replaces `sys.modules` entries, and one pytest process gives the same result.
- New `test_*_cov.py` files are picked up by the glob. A new real-dependency suite only runs in CI once it's added to the explicit list in `ci.yaml`.
- Raise the coverage floor as coverage improves; never lower it.
- Review the change against the analyzer constraints in `AGENTS.md` (open-weight models only, no API keys, answers in seconds on small CPU nodes); tests don't check those.
