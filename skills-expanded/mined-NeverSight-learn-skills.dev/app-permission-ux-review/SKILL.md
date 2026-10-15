---
name: app-permission-ux-review
description: Design and audit permission request UX, consent moments, privacy rationale, denial recovery, settings paths, OS prompts, notification opt-ins, location/camera/microphone/photo/contact access, tracking prompts, and trust copy for mobile, desktop, web, and games. Use when products need sensitive access without hurting conversion, review approval, accessibility, or user trust.
---

# App Permission UX Review

Use this skill to convert a high-stakes product decision into a concrete, measurable, reviewable operating artifact.

## Workflow

1. List every requested permission, platform, user value moment, data sensitivity, fallback, and store/review implication.
2. Read `references/permission-ux-patterns.md`.
3. Map request timing, pre-prompt rationale, OS prompt, denial state, settings recovery, and data-use disclosure.
4. Separate necessary access, optional convenience, background access, tracking, and regulated/sensitive data.
5. Produce permission matrix, UX flow, copy, event schema, and rejection-risk review.

## Guardrails

- Do not ask before the user understands the value moment.
- Do not block the whole product when a graceful fallback can work.
- Do not obscure data use, background behavior, or persistent access.
- Verify current platform policy before shipping regulated, tracking, or background permissions.

## Output format

```text
Permission context:
Platform / permission / value moment:

Permission matrix:
| Permission | Why now | Prompt copy | Fallback | Settings recovery | Risk |
| --- | --- | --- | --- | --- | --- |

State flow:
- <state> -> <screen/prompt/recovery>

Events and review notes:
- <event/policy/support note>
```
