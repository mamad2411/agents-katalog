---
name: enterprise-compound
description: Use when verified enterprise work or a resolved debugging session should be captured as searchable institutional knowledge with prevention guidance
---

# Enterprise Compound
## Global Precheck

Before reading further, writing artifacts, delegating, or changing files, run:

```bash
enterprise-precheck --skill enterprise-compound
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet files or evidence markers to bypass it.


Capture the lesson while it is still fresh.

## Required Workflow

1. Run the agent-bound compound gate in [agent-stage-gates.md](../enterprise/references/agent-stage-gates.md).
2. Search for an existing related solution note.
3. If none exists, create one under `docs/solutions/YYYY-MM-DD-<slug>.md`.
4. Use [solution-template.md](references/solution-template.md).
5. Include structured `enterprise_prevention_records` whenever the lane involved a failed review, unresolved conversation, Copilot finding, or review-thread closeout.
6. Validate the solution artifact with `tools/enterprise-skills/scripts/validate_structured_proof.py`.
7. Focus on retrieval and prevention, not storytelling.

## Review Feedback Harvester

When the lane includes PR review, Copilot review, Codex review, forge bugs, or verify defects, compound the learning before closing:

- Record each accepted P1/P2/P3 finding, root cause, missed prevention point, fix pattern, and regression proof.
- Route each accepted finding to exactly one prevention target: plan question, contract postcondition, build authority scan, review check, forge lens, verify command, CI/gate recommendation, repo trap, or skill eval.
- Classify whether the missed prevention point was intent continuity, touched-file
  SRP/refactor, DB/query ownership, runtime proof, or another class. Intent/SRP/
  DB ownership misses must update the corresponding ledger, packet, lens, gate,
  trap, or eval before closeout or be recorded as blocked.
- If a useful finding is advisory-only, record it as `advisory harvested` rather than silently dropping it.
- If the same finding class appears twice, update the repo trap matrix or recommend a deterministic gate.

## Required Content

- the problem or decision
- the root cause or rationale
- the actual change
- the blast radius or related checks
- the prevention pattern
- durable domain language, avoided synonyms, or ADR rationale when the lane
  resolved load-bearing terminology or decisions
- intent-continuity, touched-file SRP/refactor, and DB/query ownership prevention
  learning when those classes were relevant
- machine-readable prevention records when review failure learning applies
- tags that make the note searchable later

This stage is post-verification knowledge capture.

## Proof Boundary Rule

- Carry forward the upstream proof boundary exactly as verified.
- Do not upgrade a prior `function-level`, `slice-level`, or `domain-level` result into `full-system`.
- If the verified work still had unproven legs, keep the fail-closed posture explicit in the compound note.
- Do not use the solution note itself as evidence that unresolved enterprise scope is now closed.

## PR Review Failure Learning Rule

When compound follows a failed PR review, unresolved conversation, Copilot finding, merge-blocking review thread, or `enterprise-pr-review` run, the solution note must include a `Review Failure Prevention` section.

That section must name, for every real finding:

- reviewer finding and root cause
- which upstream stage should have caught it first: `plan`, `contract`, `build`, `review`, `forge`, `harness`, or `verify`
- the exact prevention upgrade: trap-matrix entry, repo gate, deterministic script, contract invariant/postcondition, plan rule, or skill eval
- whether the upgrade targets the Intent Continuity Ledger, Touched File SRP
  Assessment, DB/Query Ownership Packet, review/forge/verify lens, or harness gate
- whether the upgrade was implemented now or recorded as a dated follow-up blocker
- a matching structured `enterprise_prevention_records` entry with status `implemented`, `tracked-follow-up`, `gate-added`, `eval-added`, or `blocked-with-reason`

If no prevention upgrade is possible, mark the item `BLOCKED` and explain why. A compound note that only says "add more tests" or "be more careful" fails this stage.
