---
name: ux-copy
description: >
  Write UX copy for screens, flows, components, and micro-interactions.
  TRIGGER when: user says "UX copy", "microcopy", "write copy for", "button text",
  "error message", "empty state", "onboarding copy", or needs interface text.
argument-hint: "[screen, component, or flow to write copy for]"
user-invocable: true
---

# UX Copy

Write clear, concise, and human interface text. Every word in a UI earns its place — guide users, reduce friction, and reflect the product's voice.

## UX Writing Principles

1. **Clear over clever**: Users scan, not read. Say exactly what happens.
2. **Concise**: Every word must earn its place. Cut filler ruthlessly.
3. **Actionable**: Tell users what to do, not just what happened.
4. **Human**: Write like a helpful colleague, not a robot or a lawyer.
5. **Consistent**: Same action = same label everywhere.
6. **Accessible**: Write for a global audience — avoid idioms, jargon, and cultural assumptions.

## Copy by Component Type

### Headings & Titles

- Use sentence case ("Create new project" not "Create New Project").
- Be specific: "Choose a payment method" not "Payment".
- Match the user's mental model of the task.

| Instead of | Write |
|---|---|
| Settings | Account settings |
| Error | Something went wrong |
| Success | Payment confirmed |
| Dashboard | Your projects |

### Buttons & CTAs

- Start with a verb: "Save changes", "Create account", "Send invite".
- Be specific about the outcome: "Delete project" not just "Delete".
- Primary CTA: 2-4 words max.
- Match the button to the heading/context:
  - Heading: "Delete this project?" -> Buttons: "Delete project" / "Keep project"
  - NOT: "Yes" / "No"

| Context | Weak | Strong |
|---|---|---|
| Sign-up form | Submit | Create account |
| File upload | OK | Upload file |
| Destructive action | Yes | Delete permanently |
| Save form | Done | Save changes |
| Newsletter | Submit | Subscribe |

### Error Messages

Structure: **What happened** + **Why** (if not obvious) + **What to do next**.

```
{What happened}. {What to do}.
```

| Instead of | Write |
|---|---|
| Invalid input | Enter an email address like name@example.com |
| Error 403 | You don't have access to this page. Ask your admin for permission. |
| Something went wrong | We couldn't save your changes. Check your connection and try again. |
| Required field | Enter your name to continue |
| Password error | Password must be at least 8 characters with one number |

Rules:
- Never blame the user ("You entered an invalid email" -> "Enter a valid email address")
- Be specific about what's wrong and how to fix it
- Use inline validation where possible — don't wait for form submission
- Avoid error codes unless users need them for support

### Empty States

Structure: **What this space is for** + **How to fill it** (with a CTA).

```
## {Feature name}

{Explain what goes here in 1 sentence}.
{How to get started — with a clear CTA}.

[CTA Button]
```

Examples:
- "No projects yet. Create your first project to get started." [Create project]
- "Your inbox is empty. Messages from your team will appear here."
- "No results found for '{query}'. Try different keywords or check your filters."

### Loading & Progress States

- Keep it short: "Loading projects..." not "Please wait while we load your projects"
- For long operations, set expectations: "This usually takes 1-2 minutes"
- Use skeleton states over spinners where possible (show structure, not blankness)

| Duration | Pattern |
|---|---|
| < 1s | No indicator needed |
| 1-3s | Skeleton / spinner |
| 3-10s | Spinner + "Loading..." |
| 10s+ | Progress bar + time estimate |

### Confirmation & Success

- Be specific about what succeeded: "Project created" not "Success!"
- Include next steps if relevant: "Invite sent. They'll receive it within a few minutes."
- Keep celebrations proportional — don't confetti for saving a form.

### Tooltips & Help Text

- Tooltips: 1-2 sentences max. Answer "what does this do?"
- Help text below inputs: explain format or constraints *before* the user makes an error.
- Progressive disclosure: show basic labels, reveal detail on hover/focus.

| Field | Help text |
|---|---|
| Username | Letters, numbers, and hyphens. 3-20 characters. |
| API key | Find this in Settings > API. Starts with "sk_". |
| Date range | Select up to 90 days. Longer ranges are available in exports. |

### Onboarding & First-Run

- Welcome without wasting time: 1 sentence max before the first action.
- Use the user's name if available.
- Show progress: "Step 2 of 4"
- Let users skip: "Skip for now" (not "Maybe later" which is vague).
- End with value: show them what they just set up, not just "You're all done!"

## Voice & Tone Matrix

Adapt tone to context while keeping voice consistent:

| Context | Tone | Example |
|---|---|---|
| Onboarding | Warm, encouraging | "Welcome! Let's set up your workspace." |
| Success | Confident, brief | "Changes saved." |
| Error | Calm, helpful | "That email is already in use. Try another or sign in." |
| Destructive action | Serious, clear | "This will permanently delete all project data. This can't be undone." |
| Empty state | Friendly, guiding | "No reports yet. Create one to start tracking your metrics." |
| Loading/waiting | Reassuring | "Importing your data. This usually takes about a minute." |

## Delivery Format

When writing copy, output a structured spec:

```
## UX Copy — {screen/flow name}

### Screen: {name}

| Element | Copy | Notes |
|---|---|---|
| Page title | {text} | Sentence case |
| Subtitle | {text} | Optional — only if title needs context |
| Primary CTA | {text} | Verb-first, 2-4 words |
| Secondary CTA | {text} | |
| Field: Email | Label: "Email address" / Placeholder: "name@company.com" / Error: "Enter a valid email address" | |
| Field: Password | Label: "Password" / Help: "At least 8 characters" / Error: "Password is too short" | |
| Empty state | {text + CTA} | |
| Success toast | {text} | Auto-dismiss after 5s |
| Error banner | {text} | Persistent until resolved |

### Content Guidelines for This Screen
- Max heading length: {N} characters
- Max body text: {N} lines
- Truncation behavior: {ellipsis at N chars / expand on click}
```

## Quality Checklist

Before delivering copy:

- [ ] Is every label/button specific enough to stand alone without surrounding context?
- [ ] Is the copy free of jargon, acronyms, and technical terms?
- [ ] Are error messages actionable (not just "invalid")?
- [ ] Does the copy work for the shortest and longest possible content?
- [ ] Is sentence case used consistently (not Title Case)?
- [ ] Are destructive actions clearly described with consequences?
- [ ] Would this make sense translated to another language?
- [ ] Are instructions positive ("Enter your name") not negative ("Don't leave this blank")?

## Edge Cases

- If input data is incomplete, state assumptions explicitly and flag gaps
- For time-sensitive situations, prioritize speed over comprehensiveness
- If multiple stakeholders have conflicting needs, document the tradeoffs
- For first-time use, start with a simplified version and iterate
- Adapt the depth and detail to the audience's expertise level
