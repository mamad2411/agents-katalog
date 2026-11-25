---
name: fix-review-finding
description: The loop for resolving one finding from the docs/review/ register (MEM/INV1/SP1/SP4/DATA/FE). Use when fixing a catalogued review issue so the smallest correct change ships with a regression test, passes the gate, and the register is updated to ✅ Closed. Keeps fixes scoped and the triage doc honest.
---

# Fix a review finding

Resolve **one** finding from the `docs/review/` register (front door:
docs/review/TRIAGE.md). The goal is a small,
correct, tested change — and a register that stays truthful.

> Read [.Codex/AUTONOMOUS_GUARDRAILS.md](../../AUTONOMOUS_GUARDRAILS.md) first.
> Live data is external; never repo-wide `git reset`/`checkout .`/`stash`/`clean`,
> never branch-switch the main checkout, never touch `backend/data/**`.

## 1. Read the finding
Open its area file (e.g. `docs/review/sp1-spend-rules.md#sp1-3`). Note the
**Where** (exact `file:line`), the **Proposed fix**, and the **Decision** (scope).
If a finding needs a product decision still marked "triage", **stop and surface
it** — don't guess money/scope behavior.

## 2. Right-size + scope
- **S finding** (copy, CSS, one-liner, add-a-field, single behavior) → dispatch to
  **implementer** (smallest correct change, no refactor). Skip PM/architect.
- **M/L finding** (cross-layer, a product call, new surface) → **senior-engineer**,
  and if it changes the data model or the AI/tool surface, write/refresh the RFC
  first (`.Codex/rfcs/phase2/`).
- **Cluster findings that share files** (e.g. the disposal set: DisposalForm /
  ChangePreview / lots / positions) → do them in **one sequential pass**, not N
  racing edits, so the same files load once.

## 3. Implement the smallest correct change
Follow `AGENTS.md`: data via `backend/db/` stores; financial math only in
`services/`; balances/amounts computed, never trusted; no back-compat shims
(migrate the file); reuse the shared pattern (e.g. `.modal-overlay` + `btn-primary`,
not a new one). **Don't expand scope beyond the finding.**

## 4. Test (required — repo test policy)
Every fix ships a test that **fails before** the change: a regression test for a
bug, a unit test for a service method, a TestClient smoke for an endpoint, a CRUD
test for a store. For UI/behavior findings, **verify by running the app**
(qa-engineer) — reviewers read code; the review's UI misses (gallery layout,
missing confirm-card fields) slipped because nobody ran it.

## 5. Gate (must be green)
```
.venv/bin/python3 -m ruff check . && .venv/bin/python3 -m ruff format --check .
.venv/bin/python3 -m pytest -q -m "not integration"
.venv/bin/python3 -c "import signal,sys; signal.signal(signal.SIGALRM, lambda *a:(print('TIMEOUT'),sys.exit(99))); signal.alarm(25); import backend.main; print('IMPORT_OK')"
# if frontend touched:
cd frontend && npm run build
```
Green → commit (explicit paths only). Red → fix, or revert only your files and
report the blocker.

## 6. Close the loop (don't skip)
- Flip the finding's **Status to ✅ Closed (`<commit>`)** in **both** its area file
  **and** `docs/review/TRIAGE.md`.
- If you discovered a **new** issue, log it: area file + `README.md` index + a
  TRIAGE cluster/bucket.
- Conventional commit referencing the finding id, e.g.
  `fix(INV1-3): default disposal date to local time` ending with the project's
  `Co-Authored-By` line.

**Definition of done for a finding:** smallest correct change + a test that
failed before it + gate green + register updated. Doing less, correctly, wins.
