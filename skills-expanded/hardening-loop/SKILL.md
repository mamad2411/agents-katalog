---
name: hardening-loop
description: The repo's active development workflow — drive ONE core flow at a time to "I'd bet my real numbers on it" via the evidence-not-assertion loop. Use whenever doing feature/bug/hardening work toward launch, picking up the next task, capturing a bug, or asking "what should I work on / what's the process here". Live board is docs/launch/BOARD.md.
---

# The Hardening Loop

Active development on Open Net Worth runs as a **hardening loop**, not a feature firehose. The goal is a narrow core the owner trusts with real money, reached by converging ONE flow at a time. This skill is the executable workflow; the live state is **`docs/launch/BOARD.md`**; the rationale is `docs/superpowers/specs/2026-06-28-hardening-loop-design.md`.

## The one rule (non-negotiable)
**Status is earned by evidence, never asserted.** `🧪 built ≠ done`. A task is ✅ **trusted** only with (1) a named passing test AND (2) the owner's sign-off on the real numbers. Agents may take work to `built`; **only the owner flips to `trusted`**. Never mark a flow done because code compiles or a doc says so — that is the exact failure this loop exists to kill.

## The sequence
One flow to rock-solid before the next: **① Foundation (ledger + net worth) → ② Budgeting → ③ Investments.** Everything else is Deferred — it may say "coming soon" but must never lie with a broken screen. Do not start flow N+1 while flow N is unlocked.

## Capture a bug (5 seconds, anytime)
`make bug MSG="net worth wrong with a USD account — looks like FX"` → appends a 🆕 line to the board Inbox. No triage at capture time. (Or hand-edit the `## 📥 Inbox` section.)

## Run one turn of the loop
1. **Triage** 🆕 Inbox items into the current flow: give each an ID (`F<n>`/`B<n>`/`I<n>`), a one-line scope + severity; set 📋 todo. Park deferred-area bugs under `🅿️`.
2. **Pick** the top 📋 todo of the *current* flow (respect the sequence). Keep ≤2–3 in 🔄 doing at once — convergence over throughput.
3. **Isolate**: spawn the implementer in a **git worktree** on `lane/<id>-<slug>` (`junior-engineer` for a small contained change; `senior-engineer` if it spans layers / needs design judgment). Set the row to 🔄 doing with the lane noted.
4. **Build with a test**: the implementer makes the SMALLEST correct change **and writes the regression/acceptance test that proves it**, then runs `make check` (hang-safe: import-smoke + `pytest -m "not integration"` + lint + build). UI work is **design-first** (a `ui-designer` spec first) and clears the UI Quality Gate.
5. **Verify gate (BLOCKING)** — dispatch independent reviewers, never skip: `code-reviewer` (logic/layering/DoD) + `qa-engineer` (behavioral, against the RUNNING app). UI also gets `ui-designer` conformance + `make qa-e2e` for the touched acceptance IDs + `make ui-gate`. On any fail, back to step 4.
6. **→ 🧪 built**: update the board row with the evidence (test name, lane, what was verified, screenshots for UI). **Do not merge to main.** Surface it for the owner.
7. **Owner sign-off → ✅ trusted**: the owner checks the real numbers in the running app and approves. Merge the lane. Flip to ✅ with `trusted <date> @<commit>`. Only now does it count.

## Lock a flow (convergence + anti-regression)
When every task in a flow is ✅ and its acceptance suite is green and the owner signed off:
- Add the flow's acceptance suite to `make check` so later work that breaks it **fails CI**.
- Record `🔒 <flow> — LOCKED <date> @<commit>` in the board's Locked section.
- Only then start the next flow.

## Guardrails
- Honor `.Codex/AUTONOMOUS_GUARDRAILS.md` (git-safety; never repo-wide `reset --hard`/`checkout .`/`clean`; never touch `backend/data/**`).
- All money math in `services/`; never trust stored `base_amount` — recompute via `txn_base_amount()`.
- The board IS the truth: keep it current in the SAME change that does the work — a status flip and its evidence land together.
