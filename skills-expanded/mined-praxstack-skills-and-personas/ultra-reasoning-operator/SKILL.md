---
name: ultra-reasoning-operator
description: >
  Scope-calibrated ultra-rigor workflow for hard reasoning, high-risk code changes,
  architecture decisions, debugging with multiple plausible root causes, security-sensitive
  work, and user requests like "ultra reasoning", "think harder", "verify everything",
  "adversarial review", "war room", "deep check", "paranoid verifier", or "no hallucinations".
  Use to force evidence-first planning, assumption tracking, hypothesis falsification,
  adversarial self-review, verification gates, and clear uncertainty without overloading
  trivial tasks.
triggers:
  - "ultra reasoning"
  - "think harder"
  - "verify everything"
  - "war room"
  - "no hallucinations"
---

# Ultra Reasoning Operator

## Overview

Turn vague requests for "more reasoning" into a concrete, evidence-backed operating loop. Use this
as a rigor overlay on top of domain skills; do not treat it as a replacement for task-specific
knowledge.

## Core Rule

Calibrate rigor to risk.

| Task class | Use this level |
|---|---|
| Trivial edit or known-answer question | Answer directly; verify only the touched artifact if applicable. |
| Normal implementation or bug fix | Plan, make the smallest safe change, run focused verification, report evidence. |
| Ambiguous, high-risk, architectural, security, data, infra, or repeated-failure task | Run the full operator loop plus verification and adversarial references. |

Do not apply maximum ceremony to simple work. Over-orchestration is a rigor failure.

## Operator Loop

1. Restate the target outcome in one sentence.
2. Separate facts, assumptions, inferences, and unknowns.
3. Decide whether missing information is blocking. Ask only when a wrong assumption would change the product direction, cross a safety boundary, or make the result non-reversible.
4. Gather evidence from the closest source first: repo files, tests, logs, official docs, upstream source, then broader web sources when current external behavior matters.
5. Generate competing hypotheses or approaches when the answer is not obvious.
6. Define falsifiers: what evidence would disprove each hypothesis or make an approach unacceptable?
7. Plan with explicit acceptance criteria and the commands or inspections that will prove them.
8. Act in small reversible steps. Preserve existing user work and avoid speculative refactors.
9. Verify against the acceptance criteria. Replace confidence with evidence.
10. Run adversarial review when risk is material, then fix supported findings before finalizing.

## Reference Loading

**MANDATORY - READ** `references/verification-gates.md` when the task includes code changes beyond a one-line edit, bug fixing, refactoring, data migration, performance claims, security claims, or any final statement that something is fixed, working, safe, or verified.

**MANDATORY - READ** `references/adversarial-review.md` before committing to an architecture, choosing between non-obvious approaches, overriding a test or reviewer signal, finalizing a high-risk change, or when the reasoning feels too easy.

Do not load either reference for pure Q&A, copy edits, trivial formatting, or tasks where the user explicitly requested brevity.

## Composition Rules

- If the user explicitly activates APEX, autonomous mode, or another binding contract, follow that activation protocol. This skill can inform rigor but must not silently activate or override that contract.
- Use domain skills for domain mechanics first. Use this skill to enforce reasoning discipline, evidence mapping, and review depth.
- Use `devils-advocate` before a high-impact choice when available.
- Use `reasoning-verifier` after complex reasoning when available.
- Use a council or external model only when one model's blind spot could plausibly cost serious rework, safety, security, money, or user trust.

## Anti-Patterns

- Do not say "verified everything"; name the exact checks.
- Do not trust the first plausible explanation; try to falsify it.
- Do not browse by default when repo evidence or tests answer the question.
- Do not skip browsing when the answer depends on current external facts.
- Do not claim commands, tests, benchmarks, docs, or web research were run unless they were actually run.
- Do not lower acceptance criteria because the task is taking longer than expected.
- Do not bury uncertainty. Mark it as unresolved and explain the next verification step.
- Do not expose private chain-of-thought. Report assumptions, evidence, decisions, and trade-offs.
- Do not expand scope to "improve" adjacent code unless it is required for the requested outcome.

## Output Contract

For substantial tasks, structure the response around:

- Assumptions and unknowns
- Plan and acceptance criteria
- Decision or implementation summary
- Verification evidence
- Remaining risks or unverified items

For code reviews, lead with findings ordered by severity, with file and line references when available.
For tiny tasks, keep the response short and include only the verification that matters.
