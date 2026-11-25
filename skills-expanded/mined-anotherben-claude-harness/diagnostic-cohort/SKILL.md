---
name: diagnostic-cohort
description: Bounded consensus workflow for diagnostic skills, root-cause handoffs, fix evals, and pasteable /goal prompts. Use when Ben asks for a cohort, committee, looping agreement, multi-agent diagnostic review, but-why style assumption challenge, or when diagnose, patch-or-fix, blast-radius, or another diagnostic gate needs agreement on the issue, root cause, resolution, evals, and next goal before implementation.
---

# Diagnostic Cohort

Diagnostic Cohort is the reusable agreement layer for diagnostic work. It keeps
one lead agent in charge, assigns one job per reviewer, loops only when new
evidence changes the contract, and stops with a validated consensus artifact.

This skill does not implement fixes. It turns diagnostic evidence into an
agreement contract that downstream build, proof, or PR-closeout work can execute.

## Core Rule

Do not encode "loop until everyone agrees" as an unbounded loop. Consensus work
must have:

- one lead owner
- at most three active reviewers by default
- one job per reviewer
- a max round count, normally 2 and never more than 3 without explicit approval
- a material revision between rounds
- a hard stop when the same blocker repeats

Use `/Users/ben/.codex/skills/nested-agent-control/SKILL.md` when spawning
subagents so thread capacity, one-agent-one-job ownership, and closeout receipts
stay disciplined.

## Workflow

1. Resolve the target.
   Name the diagnosis packet, skill, PR, issue, workflow, branch/SHA, or artifact
   being reviewed. If the target is a diagnosis packet, validate it first with
   its own validator.

2. Define the agreement objective.
   Consensus must cover the issue, root cause, resolution boundary, fix evals,
   and pasteable `/goal` prompt. If any of those are not in scope, record them
   as explicit non-goals.

3. Prepare the evidence bundle.
   Pass reviewers compact source, packet, diff, command, runtime, schema, or
   artifact evidence. Do not ask reviewers to rediscover the whole repo unless
   their one job requires it.

4. Assign reviewer roles.
   Use the smallest set that can catch the likely failure class:

   - `issue-root-cause-reviewer`: verifies the symptom, causal chain, and owner.
   - `adversarial-but-why-reviewer`: challenges assumptions, contradictions,
     shallow causality, and missing alternatives.
   - `proof-eval-reviewer`: checks fix evals, freshness, and proof commands.
   - `blast-radius-reviewer`: checks sibling paths, callers, consumers, and
     missed surfaces when the change radius is material.
   - `patch-or-fix-reviewer`: classifies whether the proposed resolution removes
     the root cause or only masks the symptom.

5. Integrate, then decide.
   Agreement means required reviewers approve the same issue, root cause,
   owning-boundary resolution, required evals, and `/goal` handoff. If reviewers
   disagree, run one focused evidence round only after the lead updates the
   evidence or contract. If the same blocker remains, stop as blocked.

6. Write the contract.
   Use `references/consensus-contract.sample.json` as the artifact shape and save
   the filled contract beside the diagnostic artifact when writes are allowed.
   For repo-blocked work, write to an approved scratch path or return the JSON
   inline.

7. Validate the contract.

```bash
python3 /Users/ben/.codex/skills/diagnostic-cohort/scripts/validate_consensus_contract.py <contract.json>
```

Do not claim consensus if the validator fails.

## Contract Requirements

The contract must use:

```json
{ "schema_version": "diagnostic_cohort.consensus_contract.v1" }
```

Required content:

- `target`: what was reviewed, with path/URL, repo root, branch, and SHA when known
- `objective`: success criteria and non-goals
- `root_cause_confirmation`: status, agreed chain refs, rejected hypotheses, and
  remaining uncertainty
- `fix_evals`: commands or proof actions that must fail before the fix or prove
  the old failure cannot recur after the fix
- `orchestration`: mode, lead owner, active limit, and pasteable `/goal` prompt
- `reviewers`: one row per required reviewer with status, evidence refs, and
  blocking findings
- `loop_control`: current round, max rounds, stop gate, and material-revision rule
- `consensus`: decision, agreed issue, root cause, resolution, blockers, and
  revisions required
- `validator`: validation command and whether it is required

## Decision Rules

- `approved`: every required reviewer is approved, root cause is confirmed, all
  fix evals are named, the `/goal` prompt references those evals, and no
  unresolved blocker remains.
- `blocked`: evidence is missing, reviewers disagree on a material claim, the
  same blocker repeats after a focused round, a required reviewer cannot run, or
  the validator fails.
- `pending`: reviewers have not finished or the contract has not been validated.
- `needs_revision`: reviewers agree the current contract is not ready but the
  next evidence or wording change is clear.

Do not turn blocked consensus into a softer recommendation. A blocked cohort is a
handoff to gather evidence, narrow scope, or split the lane.

## But-Why Handling

The archived `but-why` behavior belongs inside the
`adversarial-but-why-reviewer` role. That reviewer asks why/how/how-do-you-know
questions against the evidence, but must return concrete contradictions,
unproven assumptions, rejected hypotheses, and next evidence needs. Do not
restore a second standalone orchestration skill unless it has unique validators
or templates that this consensus contract cannot cover.

## Output

Return:

```markdown
**Diagnostic cohort verdict:** approved | blocked | pending | needs_revision
**Target:** <path, PR, issue, packet, or workflow>
**Consensus:** <issue -> root cause -> resolution>
**Fix evals:** <eval IDs and commands/proof>
**Goal prompt:** <pasteable /goal prompt or blocker>
**Validator:** <command and PASS/FAIL/NOT RUN>
**Next action:** <one concrete action>
```
