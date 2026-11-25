---
name: heavy-review
description: Adversarially review a heavy prompt in heavy/library/ before it is run. Hunts logical gaps, missing defaults, unattended-safety violations, resumability holes, output-spec errors, guardrail gaps, and cost-realism issues. Produces a severity-tagged report (BLOCKER / SHOULD / NICE) and a PASS / NEEDS-FIX verdict, then offers to apply fixes.
---

# Heavy-prompt reviewer

A smart, skeptical review of one heavy prompt before a real run wastes a long unattended window on a
flawed spec. **Read adversarially: assume the unattended agent will take the dumbest valid
interpretation of every instruction — find where that breaks.** Work in your project repo (current
working directory); the library lives under `heavy/`.

The argument `$ARGUMENTS` is the heavy-prompt number `NN`.

## Step 1 — Load
- Resolve `heavy/library/NN-*.md` (the prompt under review). If none, list `heavy/library/INDEX.md` and stop.
- Read `heavy/library/_TEMPLATE.md` and `heavy/README.md` for the rules the prompt must satisfy.

## Step 2 — Review against the rubric
Check every item. For each problem, record: **severity** (BLOCKER / SHOULD / NICE), the exact location,
why it breaks, and the concrete fix.

**A. Completeness & logic**
- Every phase has steps; every step has ONE clearly-defined output (a file + an anchored `SEC:id`).
- No missing step between inputs and an output that later steps assume exists.
- DONE criteria are concrete and checkable (not "do a good job"). They actually cover all OUTPUT SPEC files/sections.
- No internal contradictions (frontmatter vs body: `phases` list matches the phases written; `subagents`/`websearch_max` match what the body tells the agent to do).

**B. Unattended-safety (the big one)**
- The body NEVER instructs `AskUserQuestion` / waiting for the user. (Grep for it.)
- EVERY decision the agent must make has an encoded **default** + the "take default, log to `assumptions`" rule.
- All paths are explicit/relative-from-repo-root; no "the relevant file" hand-waving.
- No step depends on information only a human would have.

**C. Resumability**
- A RESUME step exists (read `STATUS.json`, skip `completed_steps`).
- Steps are idempotent; output is append-only within a run (re-running a partial step rewrites only its own anchored block).
- Nothing assumes the whole run happens in one window.

**D. Output spec**
- Sections use stable `<!-- SEC:id -->` anchors with dotted semantic ids and the shared vocabulary.
- `00-summary.md` opens with the ```yaml``` machine block (`run`, `status`, `top_findings`, `key_sections`).
- `MAP.md` regeneration is included (at least at synthesize; ideally each phase end).
- `heavy/output/INDEX.md` update is in the synthesize phase.

**E. Guardrails**
- `subagents: false` unless the user explicitly accepted the added complexity/billing; body doesn't spawn `Agent`/sub-workflows when false.
- `websearch_max` present and the body respects it.
- Security (secrets in env/`.env` only, no bypassing hooks), low-risk-edits-only if it touches live code (risky → backlog, not blind edits), verify-external-facts where it makes claims about APIs/pricing/tools.

**F. Cost realism**
- `est_cost` matches the scope; `websearch_max` isn't absurd; phases aren't so huge a single window can't make real progress (resumability mitigates, but flag if a phase is monolithic).

**G. Edge cases**
- What if a WebSearch returns junk / rate-limits? a step's input file is missing? the prompt finishes mid-window? double-launch? — the prompt should degrade gracefully, not hang.

## Step 3 — Verdict
Print:
- A findings table: `severity | location | problem | fix`.
- **Verdict: PASS** (no BLOCKERs and no SHOULDs) or **NEEDS-FIX** (lists what must change).
- A one-line readiness call: is this safe to launch unattended right now?

## Step 4 — Offer to fix
If there are BLOCKER/SHOULD findings, offer to apply the fixes directly to `heavy/library/NN-*.md`
with `Edit` (keep edits minimal and within the template). Re-state the verdict after fixing. Don't
launch the prompt — that's `/heavy NN`.
