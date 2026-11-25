---
name: harness-improve
description: Turn an observed harness deficiency or improvement idea into a landed, properly-gated change to the neuro-matrix protocol. Use when the user reports a harness gap or defect, proposes a protocol improvement, or asks to harvest improvements from a session or audit. Verifies the gap against current main first, then routes each change class to its correct gate.
---

# Harness-improve: changing the protocol without meta-neuroslop

BLUF: improvements to the harness are the highest-slop-risk artifact in this repo — plausible protocol text detached from incidents is neuroslop about neuroslop. Entry requires a live anchor; every change class has its own gate; a null measurement result is information, not failure.

## Stage 0 — anchor or stop

Admissible anchors, in order of strength:
1. A reproduced incident — tool output from this or a documented session.
2. A structured harness-gap report (`.github/ISSUE_TEMPLATE/harness-gap.yml`).
3. A measurement — an eval run, an A/B result, a counted pattern across sessions.
4. An explicit owner decision.

«Would be nice» without an anchor → record as a ROADMAP row candidate or drop. Do not proceed to implementation on an unanchored idea: critique of the harness demands the same evidence bar as critique of code.

## Stage 1 — verify against current main

- Pull main; confirm the gap still exists by reading the current files, not the report. Reports go stale: the 2026-06-11 issue revision found a «missing» acceptance kit that had been merged before the issue was written.
- Check `ROADMAP.md` and open issues for an existing row or tracker. A recorded decision (ADR, ROADMAP status, protocol doc) must be quoted before re-opening, and re-opening requires new evidence — not repeated association.

## Stage 2 — classify the change and pick its gate

| Class | Typical diff | Gate before merge |
|---|---|---|
| Mechanical | `hooks/`, `scripts/` | `bash -n` + `python3 -m json.tool` on JSON + the matching `scripts/selftest_*.sh` (extend it with the new behavior — a test of a hand-copied reimplementation is decorative coverage) |
| Behavioral text | `invariants.txt`, `agents/`, `references/`, `CLAUDE.md` | single-line invariant format (`selftest_random_invariant.sh`); role-subset inheritance ONLY via the eval-gated N8 path (ROADMAP) |
| Calibration | `eval/criteria.md`, judge prompts, role subsets, agent system prompts | eval run (label `run-eval`); reconcile every consumer of changed counts/contracts (`ci_eval.py`, docs — the 16-vs-17 drift class); expect judge noise — report null results as-is |

All classes pass the critic gate at push (`auto-critic.sh`); protocol paths additionally pass the human-token gate (PR #59). One concern per branch and PR.

## Stage 3 — implement the minimal diff

- Evolve existing mechanisms; a new subsystem needs an ADR first.
- ROADMAP bookkeeping follows the file's own convention: new row before work starts, or move to Shipped with the landing PR.
- The change description states its own Counter — the condition under which the new rule does not apply.

## Stage 4 — measure and keep the deletion path open

- A calibration claim gets a before/after eval reference; publish the numbers including null (precedent: a candidate sentence measured null at judge-noise α 0.34–0.46 — that outcome was reported, not hidden).
- Every added rule carries a deletion path: rules that stop earning their keep are removed, not accumulated. The harness is not append-only.

## Output contract

1. Anchor. 2. Verified gap vs main. 3. Class + gate. 4. Diff. 5. Verification/measurement outputs. 6. ROADMAP/issue bookkeeping. BLUF at every step.

Counter: when the owner explicitly orders an unanchored exploratory change («try it, we'll see»), the anchor requirement converts into a measurement obligation after landing — exploration is allowed; unmeasured persistence is not.

---
Provenance: codifies the pipeline executed manually in the 2026-06-11/12 issue revision (#55/#56, PR #57–#60): verify-against-main caught an already-done item; per-class gates landed across #44, #51–#53, #59.
