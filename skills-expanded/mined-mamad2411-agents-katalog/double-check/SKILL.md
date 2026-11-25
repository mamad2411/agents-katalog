---
name: double-check
description: >
  Automatic final verification pass on completed deliverables. Runs automatically
  at the end of every fable-mode run (fable-mode, fable-fable, fable-opus,
  fable-sonnet, fable-haiku) — those skills invoke it before delivery. Also
  triggers when the user says "double check this", "double-check", or wants the
  finished work re-checked without doing it themselves. Uses a panel of
  model-tier checker agents (Haiku for mechanical checks, Sonnet for
  logic/requirements, Opus to adjudicate disagreements) to verify the finished
  output — not to redo the task. Any FAIL gets fixed and re-checked before
  delivery. Do NOT trigger on work still in progress, and never trigger on its
  own output (no recursion).
---

# Double Check

Automatic verification pass on a *finished* deliverable. The user should never have to
re-check work themselves — this skill is that re-check.

## What it is and is not

- It verifies **outputs**, it does not re-run the task. A full second run produces a
  second divergent version and a comparison problem; attacking the finished artifact
  catches the same errors at a fraction of the cost.
- It runs **after** the work is complete and **before** it is delivered.
- It never runs on its own output. One double-check per deliverable. Fixes triggered by
  a FAIL get their specific failed check re-run — not a whole new panel. No recursion.

## When it runs

1. **Automatically** at the end of any fable-mode run (fable-mode, fable-fable,
   fable-opus, fable-sonnet, fable-haiku). Those skills call this one as their final
   delivery gate. Exception: if a fable run already executed a cold verification of the
   final deliverable, do not duplicate it — run only the seam check (section "Check the
   synthesis seam") and skip the rest. Do not infer this from the narrative: the
   orchestrator closes its report with a `FINAL-COLD-CHECK:` line. `yes` → seam check
   only. `intermediates-only`, `no`, or no line at all → run the full panel. Absence of
   the line is never evidence that the check happened.
2. **On request**: "double check this", "verify this", "make sure this is right".

## Skip conditions

Trivial, reversible, low-stakes output where being wrong costs nothing and is
immediately visible. Say in one line that double-check was skipped and why.
Never skip when the deliverable tells the user to delete data, change a system or
security setting, spend money, or act on a warning.

## Procedure

### 1. Extract claims and requirements

From the finished deliverable, build two numbered lists:

- **Claims** (C1, C2, ...): every falsifiable assertion in the deliverable. Facts,
  numbers, file paths, computations, statements that something works. Each must be
  stated so a specific observation could refute it. If a claim can't be, either sharpen
  it or drop it from "established" status in the deliverable.
- **Requirements** (R1, R2, ...): everything the user's original request demanded.
  Each phrased as a yes/no: "deliverable contains X", "file Y exists and opens",
  "all rows from source present".

For each item, name the exact check: the command, file, source, or comparison that
settles it. An item with no nameable check is marked UNVERIFIABLE by you, up front,
and labeled as such in the deliverable.

### 2. Detect the runtime, pick the mode

**Agent runtime (Claude Code, Cowork — Agent tool available): run the checker panel.**

Spawn fresh checker agents. They receive claims, requirements, checks, constraints
(READ-ONLY — checkers never modify anything), and the output format. They never
receive your reasoning, your confidence, or hints about which items you suspect —
a verifier that reads your reasoning inherits your blind spots and returns agreement,
not verification.

Tier routing:
- **Haiku checkers (parallel, one per bundle of mechanical checks):** numbers re-added,
  files opened and read back, links/paths exist, commands re-run, counts reconciled.
- **One Sonnet checker:** requirements coverage (every R satisfied by the artifact
  itself, not by the work log), internal consistency, logic of any argument the
  deliverable makes.
- **Opus (only if needed):** when two checkers disagree on the same item, or a
  REFUTED verdict is itself disputed after the fix. Adjudicates; does not re-check
  everything.

Every checker brief must state: *"Refute freely. Finding a wrong claim is a success,
not a failure. Do not report CONFIRMED unless you personally observed the output that
proves it. If you cannot check something, say UNVERIFIABLE — do not guess."*

**Chat runtime (no Agent tool): degraded single-pass mode.**

Say plainly that the full checker panel isn't available on this surface. Then run the
checks yourself, cold: work only from the claims/requirements lists and the artifact —
deliberately not from memory of how you produced it. Re-derive each number, re-read
each file or source, re-test each requirement against the artifact. Same ternary
verdicts, same output format. Weaker than fresh agents — label it as a self-check in
the summary.

### 3. Verdicts — ternary, forced

Every claim and requirement returns exactly one of:

- **PASS / CONFIRMED** — with the exact command or observation and the exact output
  line proving it. "Looks good" is banned; it is not a verdict.
- **FAIL / REFUTED** — with what is actually true instead.
- **UNVERIFIABLE** — with why the check could not run. First-class outcome, not a
  failure. A panel that never returns UNVERIFIABLE is guessing to look thorough.

### 4. Check the synthesis seam

The error that survives everything above: work checked at intermediate stages, then
the final write-up introduces new claims nobody checked. Always extract claims from the
**document about to be handed over**, not from intermediate outputs. Two seam-specific
hunts:

- **Escalated hedges:** anywhere a caveat in the underlying work became a firm
  conclusion in the deliverable. If the work said "signal" and the deliverable says
  "exposure", check it.
- **Proxy metrics read as the real thing:** a timestamp is not a version; a file size
  is not disk usage; a search returning nothing is not evidence of absence. Verify the
  actual quantity.

### 5. Fix, then re-check

Any FAIL: fix the deliverable, then re-run **that specific check** (fresh checker in
agent runtime; cold re-derivation in chat). If the fix invalidates upstream content,
fix and re-check that too. Deliver only when every item is PASS or explicitly
UNVERIFIABLE. Never deliver with an unresolved FAIL footnoted.

### 6. Report

Deliver with a short verification summary:

```
Double-check: N claims + M requirements.
PASS: n. FIXED after FAIL: n (list what was wrong, one line each). UNVERIFIABLE: n (named).
Checkers: [e.g. 2× Haiku, 1× Sonnet | self-check, no agents on this surface]
```

Name what got refuted and fixed — that is the evidence the check was real. A summary
that confirms everything is either a clean run or a rubber stamp, and the user can't
tell which unless specifics are named. If everything passed cleanly, say that plainly;
do not manufacture a finding.

## Operational rules

- Verify-before-flag applies: a checker's FAIL must cite the observed evidence, not
  the absence of confirmation. Absence of evidence is not a finding.
- Checkers are READ-ONLY. Only the main session fixes things.
- Budget: default panel is small (2–4 Haiku bundles + 1 Sonnet). Escalate to Opus only
  on disagreement. Match tier to the check, not to the importance of the deliverable —
  mechanical checks stay cheap.
- If the runtime has a `cold-verify` skill available, its brief template and rules are
  the canonical form of the checker brief — reuse them rather than improvising.
