---
name: intent-to-spec
description: Automatically generates a lightweight specification before code starts flowing. Captures what the user wants, what will be built, acceptance criteria, and constraints — in a single invisible pass. Skipped for Quick Fixes. Invisible for Builder tier, presented for Engineer tier.
invoke_when: Use when a user requests a new feature, new project, or significant new functionality. Fires BEFORE brainstorming. Skip for Quick Fix tasks (typo, config change, one-line fix, rename). Skip if a spec already exists in .shipworthy/specs/.
---

# Intent-to-Spec

## Purpose

Bridge the gap between "user says what they want" and "code starts flowing." Without a spec, AI-generated code drifts from intent. With a heavyweight spec process, non-technical users bounce. This skill generates a lightweight specification in a single pass — fast enough to be invisible, structured enough to anchor the work.

## When This Skill Fires

- **YES**: "Build me an invoice app", "Add Stripe payments", "Create a dashboard", "Implement user auth"
- **NO**: "Fix the typo", "Change the button color", "Add a health endpoint", "Rename this variable"
- **NO**: A spec already exists in `.shipworthy/specs/` for this feature

## Tier Behavior

### Builder Tier (Non-Technical Users)
- Generate the spec **silently** — do not show it to the user
- Save it to `.shipworthy/specs/` without discussion
- Use the spec internally to guide your work
- The user should never know a spec was written — they just see better results
- If something is genuinely ambiguous (e.g., "build me an app" with zero context), ask ONE clarifying question, not five

### Maker Tier
- Generate the spec and show a **brief summary** (3-4 bullets) before proceeding
- "Here's what I'll build: [bullets]. Sound right?"
- Save to `.shipworthy/specs/` after implicit or explicit approval
- Do not wait for formal sign-off — if the user doesn't object, proceed

### Engineer Tier
- Generate the full spec and **present it for review**
- Wait for explicit approval before proceeding to brainstorming/planning
- Save to `.shipworthy/specs/` after approval

## Spec Generation Process

This is a single-pass process. Do NOT turn it into a multi-step interrogation.

### Step 1: Capture Intent
Read the user's request and extract:
- **What they want** (in their own words — preserve their language)
- **Who it's for** (end users, internal team, themselves)
- **Why it matters** (what problem does this solve)

If the request is too vague to build anything (e.g., "make an app"), ask ONE clarifying question:
> "What's the main thing this app should do? I'll figure out the rest."

Do NOT ask about tech stack, architecture, or implementation details — that's your job to decide.

### Step 2: Define Deliverables
Based on the intent, determine:
- **Concrete outputs** — what files, endpoints, pages, components will exist when done
- **Core behaviors** — what the thing actually does (user stories or scenarios, not technical specs)
- **Out of scope** — what this does NOT include (prevents scope creep)

### Step 3: Acceptance Criteria
Write 3-7 acceptance criteria. These are how you (and the user) know the work is done:
- Written as "When [action], then [result]"
- Cover the happy path AND the most important edge case
- Include at least one error scenario

Example:
```
- When a user submits a valid invoice, it is saved and appears in the invoice list
- When a user submits an invoice with missing required fields, they see specific error messages
- When a user views the invoice list, invoices are sorted by date (newest first)
```

### Step 4: Constraints Check
Pull constraints from existing project context:
- **Architecture rules** — read `.shipworthy/architecture.md` Mandatory Rules if it exists
- **Existing patterns** — scan the codebase for established conventions (routing, state management, DB access)
- **Security requirements** — flag if the feature touches auth, payments, user data, or external APIs

### Step 5: Save the Spec

Save to `.shipworthy/specs/[feature-name].md` using this format:

```markdown
# [Feature Name]

## Intent
[User's request in their own words]

## Deliverables
- [Concrete output 1]
- [Concrete output 2]
- [Concrete output 3]

## Out of Scope
- [What this does NOT include]

## Acceptance Criteria
- When [action], then [result]
- When [action], then [result]
- When [action], then [result]

## Constraints
- [Architecture rules that apply]
- [Existing patterns to follow]
- [Security considerations]

## Generated
- Date: [today]
- Tier: [Builder/Maker/Engineer]
- Task Size: [Feature/Project]
```

### Step 6: Transition

After saving the spec:
- For **Feature-size** tasks: transition to `brainstorming` (Lite or Full mode based on tier)
- For **Project-size** tasks: transition to `brainstorming` (always Full mode)
- The spec becomes input context for brainstorming — reference it, don't repeat it

## Anti-Patterns

1. **Don't interrogate the user** — One clarifying question max. If you need to ask five questions, the feature is too vague and you should ask ONE broader question instead.
2. **Don't write a novel** — The spec should fit on one screen. If it doesn't, you're over-specifying.
3. **Don't spec Quick Fixes** — Adding a health endpoint does not need a spec. Use common sense.
4. **Don't spec what's already specced** — Check `.shipworthy/specs/` first. If a spec exists for this feature, update it instead of creating a new one.
5. **Don't block Builder-tier users** — They came to build, not to review documents. Generate the spec silently and use it internally.
6. **Don't include implementation details** — The spec says WHAT, not HOW. No file paths, no function names, no database schemas. That's for brainstorming and planning.
7. **Don't duplicate architecture.md** — Reference constraints, don't copy them into the spec.

## Why This Matters

Without a spec:
- AI starts coding based on assumptions → user says "that's not what I meant" → rework
- Features creep because there's no boundary → "while you're at it, add X" → scope explosion
- Acceptance criteria don't exist → "is this done?" becomes a guessing game
- Constraints get ignored → code violates architecture rules discovered only at review time

With a spec (even an invisible one):
- AI has a contract to build against → fewer "that's not what I meant" moments
- Scope is defined → additions are conscious choices, not drift
- Done means done → acceptance criteria are checkable
- Constraints are front-loaded → no surprises at review time
