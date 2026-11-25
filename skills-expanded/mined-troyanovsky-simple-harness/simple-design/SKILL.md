---
name: simple-design
description: >
  Write a technical design document (docs/<feature-name>/design.md) describing how to build a
  feature — architecture, data flow, interfaces, key decisions, testing strategy — from a spec,
  user message, or codebase context. Use when the user wants to design a feature, plan an
  implementation approach, document architecture decisions, or turn a spec.md into its design.
  Triggers: "write a design doc", "design this feature", "plan the implementation", "how should
  we build this", "technical approach", "architecture for".
disable-model-invocation: true
---

# Simple Design — Write a Technical Design Document

You are writing a technical design document. Your job is to produce a `design.md` file inside `docs/<feature-name>/`
that gives an AI coding agent (or a human developer) a clear, actionable plan for **how** to implement
a feature — the architecture, data flow, interfaces, key decisions, and testing strategy.

This skill works standalone from a user's message or any input file that describes what needs to be built.
It also pairs well with **simple-spec** — consuming `docs/<feature-name>/spec.md` as input gives the
best results, but it's not required.

## Folder convention

All feature artifacts live in `docs/<feature-name>/`:

```
docs/
  index.json              ← feature manifest
  visual.md               ← from simple-visual (app-level, optional)
  <feature-name>/
    spec.md               ← from simple-spec
    design.md             ← THIS SKILL'S OUTPUT
    design/               ← optional: detail files when design.md is split
      <area>.md
    issues.json           ← from simple-tasks
    progress-log.md       ← from simple-implement
```

The `<feature-name>` token is a short kebab-case identifier that ties all artifacts together by directory.

## Workflow

### 1. Gather context

Start by collecting as much information as you can **before** asking the user anything.

**From the input:**
- If the user points to a feature folder (e.g., `docs/<feature-name>/`), read `spec.md` in that folder.
  This is your primary source of truth for *what* to build and *why*.
- If no feature folder is specified, check `docs/index.json` for features with status `"planning"` or
  `"spec_ready"` and look for a `spec.md` in their directory.
- If there's no spec file, treat the user's message or input file as the feature description and extract
  the goals, scope, and requirements from it.

**From the codebase:**
- This is where the design skill does its heaviest lifting. You need to understand the existing system
  deeply enough to propose changes that fit naturally.
- **Durable docs first (if present):** read `docs/architecture.md` for the high-level system shape
  and `docs/adr/` for past decisions and their rationale. These tell you *why* the system is the way
  it is and stop you from re-litigating settled decisions — reconcile any high-level claim against
  the code, which remains the source of truth for detail.
- Search for and read:
  - **Architecture:** Directory structure, module boundaries, how the app is organized.
  - **Data layer:** Database schemas/models, ORMs, migrations, data access patterns.
  - **API layer:** Route definitions, controllers, middleware, request/response shapes.
  - **Business logic:** Services, domain models, shared utilities relevant to the feature area.
  - **UI layer** (if applicable): Component structure, state management, routing.
  - **Tests:** Existing test patterns, test utilities, what's covered and what's not.
  - **Config & infra:** Environment variables, feature flags, deployment setup, CI/CD.
- Look for patterns the codebase already uses — the design should follow existing conventions unless
  there's a strong reason to deviate (and if so, document that as a key decision).

The goal is to understand the system well enough that your design reads like it was written by someone
who works on this codebase daily.

### 2. Ask follow-up questions (only if needed)

After gathering context, assess what's still ambiguous. Common gaps at the design stage:

- **Technical constraints:** "I see you're on Postgres 14 — are you open to using native JSON columns,
  or do you prefer a normalized schema?"
- **Integration boundaries:** "The spec mentions a webhook — should this integrate with the existing
  event system in `lib/events/`, or is this a separate concern?"
- **Performance expectations:** "The current query for listing workspaces does a full table scan.
  Should the design include indexing, or is the dataset small enough that it doesn't matter?"
- **Migration/rollout concerns:** "There are ~50k rows in the users table. Should we plan for a
  zero-downtime migration, or is a maintenance window acceptable?"

Only ask questions where the answer changes the design meaningfully. If the codebase gives you enough
signal to make a reasonable choice, make it and document it as a key decision with your rationale.

Present your questions to the user — keep it to one round of 1-4 focused questions.
Use whatever mechanism is available (a structured question tool, a chat message, etc.).

### 3. Write the design

Read the template at `references/design_template.md` in this skill's directory. Use only applicable
sections; remove unused headings and placeholders.

**Key principles:**

- **Ground everything in the actual codebase.** Reference real file paths, real function names, real
  table names. "We'll add a new service" is vague. "We'll add `src/services/workspace-sharing.ts`
  following the pattern established by `src/services/workspace.ts`" is actionable.

- **Keep current state selective.** List only relevant code touchpoints and why each matters; do not
  reproduce the codebase survey.

- **Make changes actionable.** Name material new or modified files, contracts, schemas, and endpoints
  so implementation can begin without guessing.

- **Specify changed boundaries, not implementations.** Include only material type/interface definitions,
  function signatures, schema diffs, endpoint shapes, and file-level structure. Do *not* include full
  function bodies or large code blocks — leave the implementation to the coding agent. If you find
  yourself writing more than ~10 lines of logic inside a code block, you've crossed into implementation
  territory; pull back and describe the behavior in prose or pseudocode instead.

- **Record only consequential decisions.** Include cross-cutting, hard-to-reverse, or convention-breaking
  choices and real alternatives. Zero decisions is valid. These decisions are the source
  **simple-distill** uses for durable ADRs after the feature ships.

- **Use data flow when it clarifies boundaries.** Describe one concrete proposed flow; include the
  current flow only when the contrast matters.

- **Make verification specific.** Map changed behavior or spec IDs to test level, location, and existing
  utilities without restating the behavior.

- **Preserve compatibility unless the spec permits breaking changes.** Describe migration or rollout
  only when needed.

- **Avoid repeating the spec.** When one exists, reference its goals, scope, acceptance criteria,
  and success measures. Summarize only constraints needed to explain the design.

- **Use one change map.** Do not repeat the same file or component changes in separate planned-change
  and affected-component sections.

**Concision**

Research broadly; write only material facts. Keep each fact in one place and link instead of
repeating content across sections, parent/child documents, or upstream artifacts.

Prefer one file. Split only for independently implementable areas; move detail out of the parent
rather than summarizing it twice. Keep the complete design, including children, under ~4,000 words.
If that is insufficient, split the feature scope.

Before saving, remove content that does not clarify the approach, a changed contract, a material
decision or risk, or verification.

### 4. Save the output

- Use the same feature name from the spec (or derive a short kebab-case name if working standalone).
- Save to `docs/<feature-name>/design.md` relative to the project root (create the directory if needed).
- If you split the design, save the child files under `docs/<feature-name>/design/` and make sure
  `design.md` indexes them. Otherwise a single `design.md` is the complete output.
- Update `docs/index.json` to set the feature status to `"design_ready"` (or create the entry if
  working standalone).
- Tell the user the file path and give a brief summary of the technical approach.

### 5. Suggest next step

Let the user know the design is ready. The typical next step is to run **simple-tasks** to break the
design into an ordered task list (`docs/<feature-name>/issues.json`), then use **simple-implement**
or **simple-run** to execute. If there are open questions or risks flagged in the document, highlight
them so the user can address them before moving to task breakdown.

## Important notes

- This skill produces a **technical design**, not a product spec — focus on *how*, not *what* or
  *why* (the spec covers those). If you find yourself writing user stories or acceptance
  criteria, you've crossed into spec territory; pull back.
- If the spec has open questions that affect the design, call them out explicitly rather than
  guessing — e.g. "this design assumes X; if Y holds instead, section Z would need to change."
- If no spec exists and the input is vague, consider suggesting a spec be written first (via
  **simple-spec** or manually) — designing against ambiguous goals leads to rework. This is a
  suggestion, not a blocker; proceed with what you have if the user wants to.
