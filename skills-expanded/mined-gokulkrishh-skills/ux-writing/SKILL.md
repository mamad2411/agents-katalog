---
name: ux-writing
description: Write, review, and improve UX copy -- error messages, button labels, empty states, tooltips, onboarding flows, and all interface microcopy. Use when writing or fixing user-facing text in a product. Outputs production-ready copy with rationale.
license: MIT
args:
  - name: target
    description: The feature, component, or screen needing copy (optional)
    required: false
user-invokable: true
---

# UX Writing

Write, review, and improve user-facing interface text so products are easier to understand and use.

## Instructions

**STEP 1 — GATHER CONTEXT**

Before writing, establish: **product/feature**, **audience** (technical? general? first-time?), **platform** (web/mobile/CLI/email), **user's emotional state** (mid-task? recovering from error? onboarding?), and **constraints** (character limits, brand voice, localization). If not provided and not inferable, ask.

Pick a tone: **professional-friendly** (clear, warm — SaaS default), **casual-conversational** (relaxed, personality-forward — consumer apps), or **technical-precise** (minimal, exact — dev tools/CLIs). Let the user override.

**STEP 2 — DIAGNOSE (when improving existing copy)**

Check for: jargon users won't know, ambiguity, passive voice, wordiness, missing next step, blame language ("You entered invalid..." vs "That doesn't look right..."), tone mismatch, and inconsistency (same concept called different things).

**STEP 3 — WRITE OR REWRITE**

For each piece of copy, output in this format:

```
| Location | Original (skip if new) | Improved | Rationale (one line) |
| -------- | ---------------------- | -------- | -------------------- |
```

When writing a multi-step flow, show the full sequence to verify narrative coherence.

### Principles by Category

**Errors**: Plain language + how to fix it + example if format matters. Never blame the user.

**Form labels**: Specific labels (not generic placeholders). Show format expectations. Explain why you're asking when non-obvious.

**Buttons/CTAs**: Verb + noun ("Create account", "Delete project"). Avoid "OK", "Submit", "Click here". For destructive actions, name the object.

**Empty states**: Explain why empty + clear next action. Inviting, not a dead end.

**Success**: Confirm what happened + what happens next. Match emotional weight.

**Loading**: Set time expectations. Explain what's happening. Offer cancel for long waits.

**Confirmations**: Name the action and object. Descriptive button labels ("Delete project" / "Keep project", not "Yes" / "No"). Only for irreversible actions.

**Onboarding**: One concept per step. Value before effort. Let users skip.

**Permission requests**: Explain the benefit. Ask in context, not on first load.

**Transactional emails**: Lead with the action. One CTA. Include fallback instructions.

**Accessibility text**: Describe function not appearance ("Search" not "Magnifying glass icon"). Concise aria-labels.

**Pricing prompts**: Lead with value not cost. Be specific about what they get. Respect current plan choice.

### Example

Before:

```
Error: Invalid input
[OK]
```

After:

```
That email address doesn't look right — check for typos and try again.
[Update email]
```

Rationale: Names the field, suggests a fix, uses a specific button label instead of "OK".

**STEP 4 — CONSISTENCY CHECK**

When reviewing multiple pieces: flag terms used inconsistently (delete vs remove, workspace vs project), inconsistent button patterns, and tone shifts between states. Recommend a single term to standardize on.

**STEP 5 — VERIFY**

Before delivering, confirm:

- Understandable without context?
- User knows what to do next?
- Every word earning its place?
- Terminology matches rest of product?
- Tone fits user's emotional state?
- Works within constraints?

## Rules

- Be specific, concise, active, helpful, consistent, and honest
- Never blame users for errors
- Never use unexplained jargon
- Never use humor in error states
- Never vary terminology for variety's sake — pick one term and stick with it
- Output format must use the table template for each piece of copy
- When reviewing multiple pieces, always include a consistency check
- If context is missing and cannot be inferred, ask before writing
