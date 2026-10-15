---
name: simple-spec
description: >
  Write a well-defined product/feature specification document (docs/<feature-name>/spec.md) from a user's
  message, input file, or codebase context. Use this skill whenever the user wants to create a spec, define
  requirements, write acceptance criteria, scope a feature, or document what needs to be built before
  implementation begins. Trigger on phrases like "write a spec", "create requirements", "define the feature",
  "scope this out", "what should we build", "spec this", or any request that involves turning a vague idea
  into a structured, implementation-ready specification. Also trigger when the user provides a feature
  description and asks for documentation an AI agent would need before coding.
disable-model-invocation: true
---

# Simple Spec — Write a Specification Document

You are writing a product/feature specification. Your job is to produce a `spec.md` file inside `docs/<feature-name>/`
that gives an AI coding agent (or a human developer) everything they need to understand **what** to build
and **why**, without prescribing **how** to build it (that's the design document's job).

## Folder convention

All feature artifacts live in `docs/<feature-name>/`:

```
docs/
  index.json              ← feature manifest (created/updated by this skill)
  visual.md               ← from simple-visual (app-level, optional)
  <feature-name>/
    spec.md               ← THIS SKILL'S OUTPUT
    design.md             ← from simple-design
    issues.json           ← from simple-tasks
    progress-log.md       ← from simple-implement
```

The `<feature-name>` token is a short kebab-case identifier (e.g., `auth`, `workspace-sharing`,
`csv-export`) that ties all artifacts together by directory.

## Workflow

### 1. Gather context

Start by collecting as much information as you can **before** asking the user anything.

**From the user's input:**
- Read the user's message carefully. Extract the feature name, intent, and any constraints they've stated.
- If the user provided an input file (e.g., a brief, PRD, issue, or notes), read it fully.

**From the codebase:**
- Search for files, modules, and code related to the feature area. Look at directory structure,
  existing models, API routes, UI components, tests — whatever helps you understand the current state
  of the system the spec is targeting.
- Pay attention to naming conventions, architectural patterns, and existing abstractions. These inform
  scope, constraints, and edge cases.
- If there's existing documentation (README, CONTRIBUTING, docs/), skim it for relevant context.

The goal is to arrive at the follow-up question phase already knowing a lot, so you can ask sharp,
specific questions rather than generic ones.

### 2. Ask follow-up questions (only if needed)

After gathering context, assess what's still unclear or ambiguous. Common gaps:

- **Who is this for?** (user type, persona, internal vs. external)
- **What's the boundary?** (what's in scope vs. explicitly out of scope)
- **What does success look like?** (measurable outcomes, acceptance criteria)
- **Are there constraints?** (timeline, backward compatibility, dependencies, tech mandates)
- **Edge cases the code context surfaced** (e.g., "I see there's a legacy auth flow — should this work with both?")

Only ask questions where the answer materially affects the spec. If you can make a reasonable assumption
based on the codebase and state it explicitly, prefer that over asking. You can note assumptions in the
spec's "Open questions" section for the user to confirm.

Present your questions to the user — keep it to one round of 1-4 focused questions.
Use whatever mechanism is available (a structured question tool, a chat message, etc.).

### 3. Write the spec

Read the template at `references/spec_template.md` in this skill's directory. Use it as the structural
backbone for your output. The template has placeholder text in brackets — replace all of it with real content.

**Key principles:**

- **Be specific, not generic.** Every item should reference actual entities from the codebase or the user's
  description. "The system must handle errors" is useless. "The system must return a 409 Conflict when the
  user attempts to create a duplicate workspace name" is useful.

- **User stories drive the spec.** Each user story should have concrete acceptance criteria in
  GIVEN/WHEN/THEN format. These become the contract that implementation is measured against.

- **Scope is a decision, not a description.** The "In scope" and "Out of scope" sections are where you
  make explicit choices. If something is borderline, put it in "Out of scope" with a note about why.
  This prevents scope creep during implementation.

- **Current state matters.** The "Current product state" section grounds the spec in reality. Describe
  what users actually do today — the agent implementing this needs to understand the starting point
  to avoid breaking existing behavior.

- **Edge cases should be actionable.** Each edge case needs an expected behavior, not just a description
  of the situation. "What if the user submits an empty form?" is incomplete. "Empty form submission →
  show inline validation errors, do not submit" is complete.

- **Open questions are honest.** If something is genuinely unresolved, say so. Don't paper over
  uncertainty with vague language.

### 4. Save the output

- Derive a short kebab-case feature name from the spec title (e.g., "workspace-sharing", "auth-jwt-migration").
- Create the directory `docs/<feature-name>/` if it doesn't exist.
- Save to `docs/<feature-name>/spec.md` relative to the project root.
- Update (or create) `docs/index.json` at the project root:

```json
{
  "features": {
    "<feature-name>": {
      "status": "planning",
      "path": "docs/<feature-name>/"
    }
  }
}
```

- Tell the user the file path and give a brief summary of what's covered.

### 5. Suggest next step (optional)

If a **simple-design** skill is available in the environment, mention that the user can run it to
produce the corresponding technical design document (`docs/<feature-name>/design.md`). The typical
workflow is: **simple-spec** → **simple-design** → **simple-tasks** → **simple-implement** (or
**simple-run**). This is a suggestion, not a requirement — the spec stands on its own as a
complete deliverable.

## Important notes

- This skill produces a **product spec**, not a technical design. Focus on *what* and *why*, not *how*.
  If you catch yourself writing about database schemas, API implementations, or code architecture,
  you've crossed into design territory — pull back.
- Adapt the template to fit the feature. Not every section will be relevant for every spec. A small
  bug fix doesn't need 5 user stories. A large feature might need more than the template shows.
  Use judgment — the template is a guide, not a straitjacket.
- If the feature is very small (a config change, a one-line fix), say so and produce a proportionally
  brief spec. Don't inflate.
