---
name: simple-spec
description: >
  Write a product/feature specification (docs/<feature-name>/spec.md) defining what to build and
  why — scope, user stories, acceptance criteria, edge cases — from a user message, input file, or
  codebase context. Use when the user wants to spec a feature, define requirements, write
  acceptance criteria, or scope work before implementation. Triggers: "write a spec", "create
  requirements", "define the feature", "scope this out", "what should we build", "spec this".
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
    spec/                 ← optional: detail files when spec.md is split
      <area>.md
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
- If durable app-level docs exist, read them first: `docs/capabilities.md` for what the product
  already does and `docs/visual.md` for UI conventions. These describe current product truth and
  keep the spec grounded without re-deriving it from scratch.
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

Read the template at `references/spec_template.md` in this skill's directory. Use only applicable
sections; remove unused headings and placeholders.

**Key principles:**

- **Be specific, not generic.** Every item should reference actual entities from the codebase or the user's
  description. "The system must handle errors" is useless. "The system must return a 409 Conflict when the
  user attempts to create a duplicate workspace name" is useful.

- **Acceptance criteria are the behavioral contract.** Write concise, testable criteria; use
  GIVEN/WHEN/THEN when it improves clarity. Do not restate them as functional requirements or
  edge cases. Include cross-cutting requirements and global edge cases only when they apply to
  multiple scenarios. Omit story priority and rationale unless material.

- **Scope is a decision, not a description.** The "In scope" and "Out of scope" sections are where you
  make explicit choices. If something is borderline, put it in "Out of scope" with a note about why.
  This prevents scope creep during implementation.

- **Current state is selective.** Use codebase research to validate existing product behavior, but
  document only the current behavior needed to understand the requested change.

- **Edge cases should be actionable.** Put each edge case and its expected behavior with the closest
  scenario unless it affects the whole feature.

- **Open questions are honest.** If something is genuinely unresolved, say so. Don't paper over
  uncertainty with vague language.

**Concision**

Research broadly; write only material facts. Keep each fact in one place and link instead of
repeating content across sections, parent/child documents, or upstream artifacts.

Prefer one file. Split only for independently implementable areas; move detail out of the parent
rather than summarizing it twice. Keep the complete spec, including children, under ~2,500 words.
If that is insufficient, split the feature scope.

Before saving, remove content that does not clarify scope, required behavior, a material constraint,
or verification.

### 4. Save the output

- Derive a short kebab-case feature name from the spec title (e.g., "workspace-sharing", "auth-jwt-migration").
- Create the directory `docs/<feature-name>/` if it doesn't exist.
- Save to `docs/<feature-name>/spec.md` relative to the project root.
- If you split the spec, save the child files under `docs/<feature-name>/spec/` and make sure
  `spec.md` indexes them. Otherwise a single `spec.md` is the complete output.
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

- This skill produces a **product spec**, not a technical design — focus on *what* and *why*, not
  *how*. If you find yourself writing about database schemas, API implementations, or code
  architecture, you've crossed into design territory; pull back.
