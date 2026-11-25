---
name: simple-design
description: >
  Write a well-defined technical design document (docs/<feature-name>/design.md) from a spec file, user
  message, or codebase context. Use this skill whenever the user wants to create a technical design, plan
  an implementation approach, document architecture decisions, or describe how a feature should be built.
  Trigger on phrases like "write a design doc", "design this feature", "plan the implementation",
  "how should we build this", "technical approach", "architecture for", or any request that involves
  turning a spec or feature idea into a structured, implementation-ready technical design. Also trigger
  when the user has a spec.md file in a feature folder and wants the corresponding design document, or
  when they ask for documentation an AI agent would need to implement a feature.
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

Read the template at `references/design_template.md` in this skill's directory. Use it as the structural
backbone for your output. Replace all bracketed placeholder text with real content.

**Key principles:**

- **Ground everything in the actual codebase.** Reference real file paths, real function names, real
  table names. "We'll add a new service" is vague. "We'll add `src/services/workspace-sharing.ts`
  following the pattern established by `src/services/workspace.ts`" is actionable.

- **Current state is your foundation.** The "Current technical state" section should read like a guided
  tour of the relevant parts of the codebase. An agent reading this should be able to navigate to
  every file that matters without searching.

- **Proposed state is your blueprint.** The "Proposed technical state" section is where you describe
  what changes. Be explicit about new files, modified files, new database columns, new API endpoints,
  new types/interfaces. The agent should be able to start coding from this section.

- **Key decisions need real alternatives.** For each decision, explain what you chose, why, and what
  you considered instead. This isn't bureaucracy — it prevents the implementing agent from second-guessing
  the approach and going down a different path. Good alternatives are ones that a reasonable developer
  would actually consider, not strawmen.

- **Data flow tells the story.** The current and proposed data flow sections are often the most valuable
  parts of the design. Walk through a concrete request end-to-end: "User clicks Share → frontend calls
  POST /api/workspaces/:id/share → controller validates → service creates sharing record → sends email
  notification → returns 201." This is what makes the design implementable.

- **Testing strategy should be specific.** Don't just say "unit test the service." Say which behaviors
  to test, what the tricky cases are, and what existing test utilities to use. The agent should be able
  to write tests from your descriptions.

- **Backward compatibility is non-negotiable unless stated otherwise.** If the spec doesn't mention
  breaking changes, assume they're not acceptable. Document how you preserve compatibility — migration
  scripts, feature flags, fallback behavior, dual-write periods.

### 4. Save the output

- Use the same feature name from the spec (or derive a short kebab-case name if working standalone).
- Save to `docs/<feature-name>/design.md` relative to the project root (create the directory if needed).
- Update `docs/index.json` to set the feature status to `"design_ready"` (or create the entry if
  working standalone).
- Tell the user the file path and give a brief summary of the technical approach.

### 5. Suggest next step

Let the user know the design is ready. The typical next step is to run **simple-tasks** to break the
design into an ordered task list (`docs/<feature-name>/issues.json`), then use **simple-implement**
or **simple-run** to execute. If there are open questions or risks flagged in the document, highlight
them so the user can address them before moving to task breakdown.

## Important notes

- This skill produces a **technical design**, not a product spec. Focus on *how*, not *what* or *why*
  (the spec covers those). If you catch yourself writing user stories or acceptance criteria, you've
  crossed into spec territory — pull back.
- The depth of the design should match the complexity of the change. A simple API endpoint addition
  doesn't need a 5-page design. A database migration affecting millions of rows does. Scale the
  document proportionally.
- If the spec has open questions that affect the design, call them out explicitly rather than guessing.
  It's better to say "this design assumes X; if Y is true instead, the approach in section Z would
  need to change" than to silently pick one interpretation.
- If no spec exists and the user's input is vague, consider suggesting that a specification be written
  first (via **simple-spec**, or manually). A good design needs clear requirements — trying to design
  against ambiguous goals leads to rework. That said, this is a suggestion, not a blocker — proceed
  with what you have if the user wants to move forward.
