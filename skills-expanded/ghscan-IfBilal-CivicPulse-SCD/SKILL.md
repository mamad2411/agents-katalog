---
name: civicpulse-guardrails
description: >
  Use before reporting ANY task complete on the CivicPulse repo — a code change, a
  commit, a PR, a "this phase is done" claim, or a merge. Also use before touching
  anything under backend/app/providers/triage/, backend/app/domain/transitions.py,
  04-CONTRACTS.md, k8s/, or .github/workflows/. This is a checklist skill, not a
  code-writing skill: it does not implement anything, it verifies and blocks.
---

# CivicPulse guardrail check

You are not done. Run this checklist against the actual diff before saying otherwise.
Do not summarize this checklist to the user as passed — run each check for real against
the files that changed, and report the result of each one that applies.

## Step 1 — What changed

`git diff --stat` (or equivalent) against the base branch. Classify every changed file
into exactly one bucket:

- `routes/` · `services/` · `repositories/` · `providers/` · `domain/` · `schemas/`
- `frontend/`
- `k8s/` · `compose*.yaml` · `Dockerfile`
- `.github/workflows/`
- `docs/` · `*.md`
- other

Run only the sections below that match a bucket you touched. Do not skip a section
because you're confident nothing bad happened — confirm it.

## Step 2 — Layer boundary check (if `backend/app/` touched)

```bash
grep -rn "select(\|\.execute(\|text(" backend/app/routes/         # must be empty
grep -rn "^from app.db\|^import app.db" backend/app/routes/       # must be empty
grep -rn "^from app.repositories" backend/app/routes/             # must be empty
grep -rn "if.*status ==.*Status\." backend/app/ --include=*.py | grep -v transitions.py
                                                                    # must be empty
```
If any of these return a hit, the change is wrong regardless of whether tests pass.
Fix it — move the logic to the correct layer — before continuing.

## Step 3 — Triage fallback integrity (if `providers/triage/` or `services/*triage*` touched)

Answer explicitly, don't assume:
- Can any code path in this diff raise an exception that is not caught before it would
  reach the route handler for `POST /api/complaints`?
- Does every failure mode (timeout, 429, 5xx, malformed JSON, bad enum, provider down)
  still terminate in a persisted row with `triaged_by="rules:fallback"` and a `201`?
- Is a validation failure (malformed JSON / bad enum) retried? It must not be —
  straight to fallback, zero retries.
- Is a timeout/429/5xx retried more than once, or retried past the 12s total budget?
  It must not be.
- Run: `pytest backend/tests/integration/test_triage_fallback.py -q` — must be green.
  If this file doesn't exist yet or the test isn't present, that is a blocker, not a
  note — stop and say so.

## Step 4 — Contract surface check (if `04-CONTRACTS.md`, `schemas/`, or `routes/` touched)

```bash
git diff 04-CONTRACTS.md                       # any diff here needs explicit user sign-off
                                                # before proceeding — do not silently edit it
pytest -m contract -q                          # must be green, unmodified test files
```
If a contract test had to be edited to pass, the code is wrong — revert the test edit
and fix the implementation, unless the user has explicitly approved a contract change
via the `chore/contract-*` process.

## Step 5 — Secrets and PII scan (always, every diff)

```bash
git diff | grep -iE "gsk_[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{35}|api[_-]?key\s*=\s*['\"][^'\"]{10,}"
git diff -- '*.yaml' '*.yml' | grep -i "stringData\|LLM_API_KEY" | grep -v "PLACEHOLDER"
git diff | grep -iE "reporter_contact|complaint.*text" -- backend/app/obs/ backend/app/routes/metrics.py
```
Any hit is a stop-and-flag, not a warning. If a real credential appears anywhere in
the diff, treat it as compromised — say so explicitly and recommend rotation; do not
just delete it and move on quietly.

## Step 6 — Cardinality and observability check (if `obs/`, `middleware/`, or routes touched)

- Any new metric label built from a raw request path, UUID, IP, or free-text field?
  Must use `path_template`, never the literal value.
- Any new log field or ring entry containing complaint text, a prompt, or a key?
  Must not.

## Step 7 — Infra deduction sweep (if `k8s/`, `compose*.yaml`, `Dockerfile`, or `.github/workflows/` touched)

```bash
grep -rn ":latest" k8s/ compose*.yaml .github/workflows/ 2>/dev/null   # must be empty
grep -rln "kind: Deployment" k8s/ | xargs grep -l "postgres" 2>/dev/null  # must be empty
grep -rn "NodePort\|LoadBalancer" k8s/base/*.yaml 2>/dev/null | grep -i "postgres\|redis"
                                                                        # must be empty
grep -rn "localhost" backend/app/ frontend/src/ compose.yaml 2>/dev/null
                                                                        # must be empty
```
Check every publish/deploy job in touched workflow files has a `needs:` clause and no
registry credentials on a job triggered by `pull_request`.

## Step 8 — Test honesty check (if any new test file or test function)

For each new test: confirm it fails against the pre-change code (revert locally or
reason explicitly about why the old code would fail this assertion). State this
explicitly in your report — "confirmed red without the fix" — don't just assert it ran
green after the fix and call that sufficient.

## Step 9 — Skill invocation audit (always, independent of bucket)

Two named skills plus one review discipline are mandatory, not optional, per
`CLAUDE.md §6`. Before reporting completion, confirm — don't assume:

- **`caveman`** ran at the start of this phase and produced a stripped task list (verbs
  only, ≤90-min items, ≥5 items). If this is mid-phase and it already ran earlier in the
  session, that's fine — but if it never ran this phase, that's a blocker: go run it,
  don't retroactively write a task list and call it equivalent.
- **`ponytail`** ran at every point in this diff where a design decision had ≥2
  defensible answers. Scan the diff for exactly that pattern (a choice between two
  approaches, a config knob, a "we could also have done X instead") — if you find one
  with no corresponding decision-record stub, that's a blocker.
- **the pre-PR hardening review** ran on the full diff before this PR, with ≥3 findings
  at `file:line` each resolved into a commit or an explicit `WONTFIX`. A diff you believe
  is clean still needs this pass — "I didn't find anything" is only credible after the
  pass ran, not instead of it. This is a review discipline, not a named skill — the skill
  that used to share its nickname here, `grill-me` (real behavior: an interactive
  interview with the user about a plan/decision), is optional on this project; don't
  invoke it expecting an automated diff scan.
- **`docs/AI-USAGE.md`** has an entry for each invocation above, written at the time,
  including an explicit "I changed" line (even if it's "accepted as-is").

If `caveman`, `ponytail`, or the pre-PR review didn't fire where required, stop and run
it now before reporting the task done — don't note it as a gap and proceed anyway.

## Step 10 — Report

State, per bucket touched, which checks ran and their result — pass/fail, not vibes.
If anything failed and you fixed it, say what you fixed. If anything failed and you did
NOT fix it (needs a human decision — e.g., an intentional contract change), say so
explicitly and do not report the overall task as done.
