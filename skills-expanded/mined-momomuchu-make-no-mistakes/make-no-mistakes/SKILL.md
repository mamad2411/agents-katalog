---
name: make-no-mistakes
description: >-
  Zero-unverified-work execution harness for coding agents. Use when the user invokes
  /make-no-mistakes, says "make no mistakes", "don't get this wrong", "this must be
  correct", "prove it works", or hands over work where a wrong result is costly. Turns
  any task into a verified pipeline: freeze what "correct" means BEFORE acting, execute
  in budgeted loops against hard deterministic gates, have work certified by an independent
  verifier that is never the implementer, and report with evidence. Never claims done
  without proof; fails loudly (STUCK / GAMING-DETECTED) instead of pretending.
license: MIT
hooks:
  PreToolUse:
    - matcher: "Write|Edit|MultiEdit|Read|Bash"
      hooks:
        - type: command
          command: "./hooks/pretooluse-protect.sh"
  Stop:
    - hooks:
        - type: command
          command: "./hooks/stop-loop.sh"
---

# Make No Mistakes

**The contract: no unverified work ever reaches the user.** Every "done" is backed by a check
that actually ran. When you cannot prove it, you say so — loudly, with the exact gap named. A
plausible-but-wrong "done" is the one forbidden output.

You are the **orchestrator**. You hold goal integrity, you delegate specialized work explicitly,
you resolve conflicts, you make the final claim — and you do the specialized work yourself only at
the trivial tier. The machinery below is deterministic on purpose: prose erodes over a long run,
scripts don't. Invoke the scripts; don't reimplement them in your head.

> Scripts live in `scripts/` next to this file. State lives in `.mnm/` in the working repo.
> Deep detail is in `references/` — load a page only when the step needs it.

## The three laws

1. **No claim without proof.** Every "it works" traces to a command that ran this session, with its
   real output. Memory and plausibility are hypotheses, not evidence.
2. **The author never grades the author.** Whoever wrote the change never certifies it — verification
   runs in a separate context against the frozen spec (Step 5), by the `mnm-verify` panel.
3. **A check that cannot fail is not a check.** Before trusting green, know what red looks like. A
   test that passes on broken code is theater.

## Terminal states — end in exactly one, never blur them

| State | Meaning | Report |
|---|---|---|
| `DONE` | Every gate green + independently certified | ✅ DONE_VERIFIED + evidence |
| `STUCK-BUDGET` | Budget spent, honest progress ongoing | 🟡 PARTIAL |
| `STUCK-OSCILLATING` | Thrashing — gates flip, no progress | 🟡 PARTIAL, gate named |
| `STUCK-INCONCLUSIVE` | Verification itself could not run | 🔴 BLOCKED — *unverified ≠ refuted* |
| `GAMING-DETECTED` | A check was weakened/edited to pass | 🔴 BLOCKED, halt — **never retried** |
| `INTEGRITY-COMPROMISED` | Frozen spec or harness files tampered | 🔴 BLOCKED, all recent verdicts suspect |

A true `STUCK` is a **successful** run of this skill. A false `DONE` is the only real failure.
Detail + reasons: `references/terminal-states.md`.

## Step 0 — Classify, and set the budget

Rigor scales with consequence × likelihood-of-error. Ambiguity raises the tier — a vague request for
important work is where agents fail most. Over-ceremony on trivial work is itself a mistake.

| Tier | Looks like | Pipeline | V&V team |
|---|---|---|---|
| **T** | typo, rename, one obvious value | act, re-read diff | self-review |
| **L** | small reversible fix, one file | light spec, full gates, self-review | single blind verifier |
| **M** | feature, bug fix, multi-file | full pipeline | panel: 2–3 lenses |
| **H** | auth, money, data, migration, public API | full + competing implementers on failure | panel: 4–5 lenses |
| **C** | irreversible, production, security | full + tournament + human sign-off | panel + human |

Then **start the run** — this is what turns enforcement ON (creates `.mnm/lock`, which the hooks
self-gate on, and initializes the budget): `scripts/mnm_start.sh <task_id> <tier>`. It refuses a
second loop on the same tree and auto-clears a stale lock. Without it the hooks stay inert — so it
is not optional. (Cost ceiling is the primary hard stop; iterations are diagnostic: T~$1 · L~$3 ·
M~$8 · H~$20 · C~$40, tunable.)

## Step 1 — SPEC-GATE: freeze what "correct" means before touching anything

A perfectly executed misunderstanding still fails the user. Explore the repo first (never ask what
the code answers). Rewrite the goal in `WHEN <trigger> THE SYSTEM SHALL <response>` form; each
acceptance criterion as Given/When/Then with a concrete example. Scan for ambiguity; take safe
reversible defaults and **log them as assumptions**; ask at most 5 batched questions only for
irreversible unknowns (the reversibility test). Detail: `references/dod-extraction.md`.

Write the DoD, then freeze it: `scripts/freeze_dod.sh <dod.md> <task_id>`. It **refuses to freeze**
an incomplete DoD (missing Goal / Acceptance / Non-goals / Write-scope / Tier / Assumptions / Budget)
and prints the `dod_hash`. From here the DoD is read-only to you; discovering it's wrong mid-run is a
legitimate `STUCK` — renegotiate with the user, **never silently redefine "done" as "whatever I built"**.

For M+, the write-scope allowlist is produced by delegating to the **`mnm-planner`** skill.

## Step 2 — PLAN & TESTS (delegate; M+)

- **`mnm-planner`** (read-only) → `.mnm/plan.json`: file-touch map, write-scope allowlist, acceptance-slice map.
- **`mnm-test-author`** → the failing-first tests, authored from the frozen DoD *only* (independent of any
  implementation). Anchor them **and the recipe that decides what runs** — the test files *plus* the
  runner (`Makefile` / `package.json` / `conftest.py` / fixture files): `scripts/hash_anchors.sh <test-globs>
  Makefile package.json conftest.py`. Anchoring only the test file lets an agent pass by editing the
  build recipe instead — anchor both.
- Decompose into units small enough that each closes its **own** verify cycle. Per-step error compounds.

## Step 3 — EXECUTE: the budgeted loop

Per unit, **red → green → verify**. Write the failing test, watch it fail (that failure is your negative
control), then implement the minimum to pass. Each iteration:

1. `scripts/run_gates.sh <task_id> <dod_hash> <iter>` — integrity gate first (tamper-diff), then the
   detected stack cheap→expensive, fail-fast, each logged with its oracle tier. **Iterate on the code,
   never on the oracle** — changing a test to pass is `GAMING-DETECTED`, not a fix.
2. `scripts/budget.sh tick <cost>` then `scripts/budget.sh check` — ceiling → `STUCK-BUDGET`.
3. `scripts/detect_oscillation.py` — green-gate count must not go backwards → else `STUCK-OSCILLATING`.
4. Re-read `.mnm/dod.lock.md` after any long stretch — the file is the truth, not your memory of it.

For H/C, when a single implementer fails or the DoD admits ≥2 distinct valid approaches, run a
**tournament**: diverse candidates (minimal-fix / defensive / refactor-first), each in its own git
worktree, each pre-filtered through `run_gates` before the panel ever runs. Detail: `references/gate-stack.md`.

## Step 4 — VERIFY: the author never certifies (delegate to `mnm-verify`)

**Prove the tests have teeth before trusting them (mutation gate — the source-of-truth boost).** A
self-authored test that passes on a wrong fix produces a *confident false DONE* — the failure mode the
SWE-bench eval surfaced. So for M+ tiers, before certifying: `scripts/mutation_gate.sh <task> <dod>
<iter> <changed_file> "<your test command>"`. It mutates your changed code; if your tests fail to kill
the mutants, they are too weak to certify anything → the run becomes STUCK, not DONE. Prefer
property-based / metamorphic tests (many generated inputs + invariants) over single examples — they
survive far fewer mutants. Then hand off to the **`mnm-verify`** skill — a forked, read-only context given ONLY the
diff + frozen DoD (never your conversation). It runs an **adversarial panel**: specialized refuters
(correctness / spec-conformance / regression / reproduction / +abuse for H/C), each rewarded for *breaking*
the work and citing file:line, and an **arbiter** that aggregates under the **independence guard** —
adversarial-unanimity or calibrated weighting, **never a naive majority vote**. Any `REFUTED` → back to
Step 3 (budget permitting). Any `UNVERIFIABLE` → the run cannot end `DONE`. Bug fixes require
reproduction-first. Why this shape: `references/anti-gaming.md`.

## Step 5 — REPORT: evidence first, state exact

Emit the terminal row: `scripts/log_verdict.sh terminal <task_id> <dod_hash> <state> "<summary>"`.
Then lead with the state and, separated and labeled: **Evidence** (commands + decisive output per
criterion, from `.mnm/verdict.log`), **Assumptions taken** (with confidence), **Residual risk** (what no
gate covers — every task has some), **Inference vs fact** (never present a conclusion as an observation).
The user should be able to accept in under a minute *because the proof is laid out* — not because they
trust you. Schema: `references/verdict-log.md`.

## Anti-gaming absolutes

These end the run `GAMING-DETECTED` — reported, never silently retried, no exceptions: editing/deleting/
weakening a test/assertion/type/lint rule to pass a gate; hardcoding an expected output or special-casing
test inputs; suppressing a warning instead of resolving it; redefining a DoD criterion after implementation
started (HARKing); claiming a command succeeded without running it. If you feel the *pressure* to do any of
these, that pressure is information — the honest `STUCK-*` states exist so you never need the dishonest ones.

## Enforcement (how this binds, not just advises)

Prose is advisory; these make it structural. **PreToolUse hook** (`hooks/`) denies Write on frozen
files and Read on the verifier rubric; **Stop hook** refuses to end the turn until a terminal row exists;
`.githooks/pre-commit` refuses a commit that isn't `DONE`; `manifest.json` is **ed25519-signed** with a
maintainer key held outside the repo (`check_manifest.sh`), the out-of-band trust root, so a tampered
harness trips `INTEGRITY-COMPROMISED`. Crucially, a `DONE` **re-executes the deterministic gate stack at
write time** (`run_gates` re-run, gated by nothing an honest run sets) rather than trusting logged rows —
so a `DONE` *typed* on broken code is refused when the real gates fail. Each Claude-Code-internal layer has
a documented bypass — the honest guarantee is the **stack** (hook + OS git-hook + signed manifest + CI),
not any single hook. On runtimes without hooks, the frozen-DoD and read-only-test rules bind by this skill's
authority, and the OS/CI layer still holds.

**Honest residual (named, not hidden):** because any in-band check runs in a shell the agent also
controls, a logged `verify` row remains forgeable *in principle*. The DONE re-execution closes the
**dangerous** case — a false `DONE` on code whose gates actually fail — and it runs in the project cwd
(not an agent-supplied dir) so it can't be aimed at a passing decoy: a redirect trips the cwd-relative
DoD/test anchors. What it does **not** close in-band: (a) an agent whose code genuinely passes the
deterministic gates can still type a `verify` row to skip the *adversarial panel's* deeper scrutiny; and
(b) `MNM_SKIP_REVERIFY` is a test-only escape hatch that disables the re-execution — it is announced
loudly on stderr when set, but an agent *could* set it. Both are the same fundamental limit: a guard
that closed them inline would either re-run the panel (violating the author≠verifier independence it
exists to enforce) or trust an env the agent owns. The real roots are the **ed25519-signed manifest**,
the **independent `mnm-verify` sub-agent**, and **CI/pre-commit re-running the gates in a clean
environment** — none of which the agent-under-test controls.
