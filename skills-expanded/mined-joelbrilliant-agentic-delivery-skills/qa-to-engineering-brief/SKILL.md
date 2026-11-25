---
name: qa-to-engineering-brief
description: Converts bug reports, screenshots, user panic, QA notes, and vague complaints into durable engineering briefs. Use when turning observed failures into reproducible issues with severity, expected behaviour, evidence, scope, owner, and acceptance tests.
---

# QA to Engineering Brief

## Overview

Use this skill when a bug report is too vague for a builder but too real to ignore.

The output is not a diagnosis essay. It is a brief a builder can execute and a reviewer can verify.

## When to Use

- User reports something broken.
- Screenshot shows confusing UI state.
- QA notes are scattered across chat.
- A bug seems intermittent.
- A failing workflow needs reproduction steps.
- You need to turn panic into an engineering slice.

## Brief Structure

```text
# [Short bug title]

## User-visible problem
[What the user experienced]

## Expected behaviour
[What should happen]

## Actual behaviour
[What happened]

## Evidence
[Screenshots, logs, run IDs, URLs, files, timestamps]

## Reproduction steps
1.
2.
3.

## Scope
In:
Out:

## Suspected area
[Files, services, components, data path]

## Severity
HIGH / MEDIUM / LOW with rationale

## Acceptance criteria
- [ ] Behaviour fixed
- [ ] Regression test added
- [ ] Runtime/browser/API proof captured

## Required verification
[Exact tests and smoke checks]

## Owner / role
[Builder or triage owner]
```

## Severity Guide

HIGH:

- data loss;
- security or permission breach;
- payment/money/account impact;
- production feature structurally inert;
- user cannot complete core workflow.

MEDIUM:

- important workflow degraded;
- no regression test catches plausible failure;
- misleading user-facing state;
- recoverable but costly failure.

LOW:

- minor UX issue with no workflow break;
- copy/visual defect;
- small edge case with clear workaround.

## Evidence Rules

- Screenshots need a timestamp or context.
- Logs need file/source and relevant lines.
- User quotes are evidence of perception, not root cause.
- Reproduction steps must be concrete enough for another agent.
- If you cannot reproduce, say what was tried and what remains unknown.

## Anti-patterns

- "It feels broken" with no expected behaviour.
- Starting with suspected code before user impact.
- Filing a giant omnibus bug.
- Severity based on emotion instead of regression impact.
- Acceptance criteria that say "fix it".
