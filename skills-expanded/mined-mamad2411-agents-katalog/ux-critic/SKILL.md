---
name: ux-critic
description: Critically evaluate user flows, intent clarity, friction, labels, forms, feedback, recovery, and decision complexity. Use when reviewing B2B SaaS, admin, developer-tool, productivity, CRM/ERP, or internal-tool workflows to reduce unnecessary steps, clarify actions, expose hidden anxiety, and improve task completion.
---

# UX Critic

## When to Use This Skill

Use this skill when the user asks to critique a workflow, onboarding sequence, form, settings flow, destructive action, approval process, search experience, or multi-step task.

Focus on whether users can confidently reach an intended outcome. Do not convert the request into a visual-style review unless visual presentation directly creates flow friction. Generate implementation code only when explicitly requested.

## Inputs

Establish:

- primary user and role
- desired outcome and success condition
- entry point and expected next step
- frequency, urgency, and reversibility of the task
- required data, permissions, dependencies, and business rules
- current flow steps, labels, validations, and system responses

State assumptions when analytics, research, or product rules are unavailable.

## What to Inspect

- **User goal clarity:** Determine whether the page and first action match the user's likely intent.
- **Flow length:** Count meaningful decisions and interactions, not only screens or clicks.
- **Action wording:** Check that buttons and links use specific verbs and communicate outcomes.
- **Form friction:** Review required fields, defaults, sequencing, validation timing, input formats, and repeated entry.
- **Error recovery:** Confirm errors explain what happened, preserve user input, and provide a recovery path.
- **Confirmation patterns:** Match confirmation strength to risk, reversibility, and consequence.
- **Information requests:** Challenge every requested field for necessity, timing, and whether the system can infer it.
- **User anxiety:** Identify uncertainty about cost, permanence, progress, permissions, privacy, side effects, or completion.
- **Feedback:** Check progress, success, pending, autosave, background processing, and partial completion signals.

## Decision Rules

1. Define one primary user goal before evaluating the flow.
2. Remove a step only when doing so does not hide a meaningful choice, safety check, or required context.
3. Ask for information at the latest responsible moment; do not front-load optional details.
4. Prefer smart defaults for predictable choices, while keeping consequential choices explicit.
5. Use action labels that state the result, such as `Send invite` or `Archive project`, instead of generic labels such as `Submit`.
6. Add confirmation for destructive, costly, external, or difficult-to-reverse actions. Avoid confirmation for harmless reversible actions.
7. Preserve entered data after validation or network failures.
8. Separate system limitations from user mistakes in error messages.
9. Make asynchronous work visible with status, expected duration when known, and a clear next action.
10. Treat uncertainty as friction even when the number of clicks is low.
11. Mark findings as `Blocking`, `High`, `Medium`, or `Low`, based on task failure risk and frequency.
12. Distinguish evidence, inference, and questions requiring user research or analytics.

## Output Format

Use these headings in this order:

### User Goal

Describe the primary user, trigger, desired outcome, and success condition.

### Friction Points

List friction in flow order. For each item include severity, step, cause, and consequence.

### Confusing Labels

Show the current label, why it is unclear, and the intended meaning.

### Missing Feedback

Identify absent progress, validation, success, pending, recovery, or state-change feedback.

### Suggested UX Changes

Provide prioritized changes. Explain which step or decision changes and why.

### Better Microcopy

Provide a compact table with `Location`, `Current`, `Suggested`, and `Reason`. Do not invent legal, pricing, or policy claims.

## Anti-Patterns to Avoid

- Optimizing only for fewer clicks.
- Assuming novice behavior for expert operational tools.
- Replacing explicit choices with hidden automation for consequential actions.
- Using generic button labels such as `OK`, `Yes`, or `Submit` when the outcome can be named.
- Clearing forms after an error.
- Using confirmation dialogs to compensate for unclear actions.
- Asking for data the system already has or does not yet need.
- Treating every inferred concern as validated research.
- Suggesting deceptive urgency, forced continuity, or other dark patterns.
