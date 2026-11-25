---
name: openspeq-review
description: Review a repository change against openspeq mission, staged specs, and verification evidence.
---

# openspeq-review

Use this skill for audits, PR reviews, or pre-merge checks.

## Goal

Judge whether a change matches the mission, respects existing specs, and has real verification behind it.

## Inputs

- target repository root
- changed files or PR diff
- relevant plan folder if one exists

## Steps

1. Read `specs/mission.md` and any relevant permanent specs.
2. Compare the code changes against staged deltas or plan documents.
3. Check whether tests and validation commands cover the claimed behavior.
4. Look for missing `/adr` records where a change introduces durable architecture constraints, not just plan-local decision prose.
5. Report findings in BLUF style:
   - verdict
   - critical gaps
   - suggested fixes
   - optional ADR/spec follow-ups

## Review questions

- Did the implementation match the staged plan?
- Were tests added or updated where behavior changed?
- Is any new complexity justified?
- Should any plan-level decision become permanent?
- Can another agent understand the resulting repo state without hidden context?

## Constraints

- Be evidence-driven.
- Prefer precise file references and command results.
- Criticize complexity theater when you see it.

## Outputs

- review summary
- concrete findings
- follow-up actions if needed
