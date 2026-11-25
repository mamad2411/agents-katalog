---
name: byte-review
description: Run a cross-functional Your ByteDance / Byte OS project review. Use when the user asks to review, audit, critique, check quality, simulate a ByteDance-inspired product meeting, assess readiness, or find issues before delivery or iteration.
---

# Byte Review

Review is the internal project-team quality gate. It may use assumptions, specs, code, screenshots, and tests, but it must not pretend to be real user feedback.

## Inputs

Read available artifacts:

```text
.byte-os/BYTE.md
.byte-os/PRODUCT_SPEC.md
.byte-os/UX_SPEC.md
.byte-os/TECH_SPEC.md
.byte-os/ROADMAP.md
.byte-os/OKRS.md
.byte-os/plans/*.plan.md
.byte-os/BUILD_LOG.md
```

Inspect the actual product or code when available.

## Review Roles

- Product Director: strategic fit and decision quality.
- Product Manager: requirement completeness and priority.
- UX Researcher: user journey and friction.
- Product Designer: interface structure and interaction quality.
- Tech Lead: architecture and maintainability.
- QA Engineer: bugs, edge cases, missing tests.
- Growth Analyst: activation, retention, monetization.
- Market Researcher: competitor gap, only if current research exists or browsing is performed.

Use the Your ByteDance style: be candid and clear, ground conclusions in facts, and call out weak context instead of smoothing it over.

Use actual subagents only when explicitly authorized. Otherwise synthesize roles inline.

## Review Dimensions

Check:

- Does the product solve the stated problem?
- Is the MVP complete and focused?
- Is the first user workflow obvious?
- Are key states handled?
- Are acceptance criteria satisfied?
- Are tests or verification sufficient for the risk?
- Are security, privacy, data, or compliance risks present?
- Does the product have a reason to exist versus substitutes?
- Is it ready for delivery, or does it need iteration?
- Did the work advance the stated Objective or Key Results?
- Which assumptions need an experiment or real user evidence?
- Did coding work follow `byte-code-rules`: simple implementation, surgical diff, no unrelated refactors, explicit assumptions, and recorded verification?

## Output

Write:

```text
.byte-os/reviews/review-N.md
```

Include:

```text
# Verdict
ship | iterate | block

# Findings
Severity, owner role, evidence, recommended fix

# Role Notes
Concise notes by role

# Required Changes
Must fix before delivery

# Suggested Changes
Can improve after delivery

# Verification Gaps
Tests, checks, or user evidence still missing

# Engineering Rule Findings
Overengineering, broad unrelated edits, hidden assumptions, unverified success criteria, or cleanup risks

# Decision
Next command
```

Update `STATUS.md`:

```text
Stage: reviewed
Review verdict: <ship|iterate|block>
Next recommended command: byte-iterate or byte-deliver
```

## Completion Criteria

Review is complete when there is a clear verdict, prioritized findings, and a next action.
