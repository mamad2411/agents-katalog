---
name: build-next
description: >
  Two-mode skill for structured software project development using the harness engineering pattern.

  **Mode 1 — Project Architect** (`/architect` or starting a new project): Interview the user about
  their project, guide them through architecture and technology decisions (language, framework, storage,
  build tooling, CI/CD, testing), record Architecture Decision Records, then generate three files:
  CLAUDE.md (agent harness), docs/ARCHITECTURE.md, and a phased docs/PROJECT_STATUS.md with
  implementation phases, per-phase file lists, test requirements, and done criteria.

  **Mode 2 — Build Next** (`/build-next` or "implement the next phase"): Read docs/PROJECT_STATUS.md,
  find the first incomplete (⬜) phase, implement exactly that one phase, run tests, verify they pass,
  then update the status document. Enforce: one phase per session, tests must pass before marking
  complete, conventional commit message.

  Use this skill whenever: the user is starting a greenfield project and needs architecture guidance;
  the user says "/architect"; the user says "/build-next" or "implement the next phase" or "work on
  the next phase"; the user references PROJECT_STATUS.md and wants to make progress; the user wants
  to break a project into implementation phases.
---

# build-next

This skill runs in two modes. Detect which mode applies from context:

- **Mode 1 (Architect)**: No `docs/PROJECT_STATUS.md` exists yet, or the user is asking about starting a new project, or they used `/architect`.
- **Mode 2 (Build Next)**: `docs/PROJECT_STATUS.md` exists with at least one ⬜ phase, or the user said `/build-next` or "implement the next phase".

---

## Mode 1 — Project Architect

Your goal is to produce three documents that wire up a full harness for agentic development:
1. `CLAUDE.md` — the feedforward guide for coding agents
2. `docs/ARCHITECTURE.md` — high-level design and Architecture Decision Records
3. `docs/PROJECT_STATUS.md` — phased implementation plan

### Step 1: Architecture Interview

Ask about the project in a single, focused message. Cover:

- **What** the software does (one sentence)
- **Who** uses it (end-users, developers, internal tools)
- **Platform** (desktop, web, mobile, CLI, server)
- **Language/framework preferences** (or ask for recommendations)
- **Storage needs** (none, files, SQLite, cloud DB, etc.)
- **Deployment target** (local-only, self-hosted, cloud)
- **Team size and experience level**
- **Any non-negotiable constraints** (open source only, specific OS, existing stack)

Wait for answers before proceeding. If the user has already shared project details in the conversation, extract what you can and ask only about gaps.

### Step 2: Technology Recommendations

Present a proposed tech stack as a markdown table with columns: Package/Tool | Recommended Version | Reason. Pin specific versions — no `latest` tags. Briefly justify each choice.

For each major architecture decision, write a short ADR (Architecture Decision Record):
- **ADR-NNN**: [Title]
- **Decision**: What was chosen
- **Rationale**: Why this over the alternatives
- **Alternatives considered**: What was rejected and why

Ask the user to confirm or adjust before generating files.

### Step 3: Phase Planning

Break the implementation into 8–15 phases. Good phases are:
- Small enough to implement in a single session (~1–4 files)
- Independently testable
- Ordered so each phase builds on the previous
- Named by what they deliver, not how they're built

For each phase, capture:
- A one-line description
- Files to create (exact paths)
- Tests to write (what behavior each test verifies)
- A "when done" criterion (typecheck + test command that must pass)

Common phase patterns:
- Phase 0: Scaffold (config files, CI, shared types — no logic yet)
- Phase 1–N: Core features in dependency order (data layer before business logic, business logic before UI)
- Phase N-1: Integration wiring (connect all modules, entry point)
- Phase N: E2E tests

Ask the user to confirm the phase list before writing files.

### Step 4: Generate the Three Documents

Use the templates in `references/templates.md`. Substitute project-specific values throughout — do not leave any placeholder text.

**CLAUDE.md** must include:
- Project summary (2–3 sentences)
- Technology stack table (pinned versions with reasons)
- Architecture decisions (key constraints and why)
- Security rules relevant to the project type (at minimum: input validation, secrets handling)
- Coding conventions (naming, imports, error handling, types)
- Testing conventions (test framework, file naming, what to mock)
- Git conventions (commit format, branch naming)
- Harness engineering alignment section listing feedforward guides and feedback sensors specific to this project

**docs/ARCHITECTURE.md** must include:
- One-paragraph overview
- Architecture diagram (ASCII)
- Process/module model description
- Data model (key interfaces/types)
- All ADRs from Step 2

**docs/PROJECT_STATUS.md** must follow this exact format — see the format specification in `references/templates.md`.

After creating the files, tell the user: "Run `/build-next` whenever you're ready to start implementing. Each invocation will implement exactly one phase and update this file."

---

## Mode 2 — Build Next

### Step 1: Read and orient

Read `docs/PROJECT_STATUS.md`. Find the first phase with status `⬜ Not started`. If all phases are complete, congratulate the user and stop.

Read `CLAUDE.md` in full — it contains the coding conventions, security rules, and testing requirements you must follow exactly.

### Step 2: Understand the phase

Read the phase's file list, test requirements, and "when done" criteria carefully. If the phase references any already-completed phases (as dependencies), skim those files to understand the patterns and types in use before writing new code.

### Step 3: Implement

Write the files. Follow CLAUDE.md conventions precisely — naming, imports, error handling, TypeScript strict mode, security rules, whatever applies.

Co-locate test files next to source files (`foo.ts` → `foo.test.ts`). Tests should:
- Cover the behaviors listed in the phase spec
- Use the same test patterns as existing test files
- Mock at the right boundary (never mock what you're testing, mock its dependencies)

### Step 4: Verify

Run the "when done" commands from the phase spec (typically `npx vitest run` or equivalent + typecheck). If tests fail, fix them before proceeding. Do not mark a phase complete if tests are red.

**This is a hard rule: tests must be green before the phase is marked complete.**

### Step 5: Update PROJECT_STATUS.md

- Check off all tasks in the phase
- Change the phase header from `⬜` to `✅`
- Update the status overview table
- Add a changelog entry with today's date, phase number, and one-line summary

Then tell the user the phase is done, what was built, and remind them they can run `/build-next` again for the next phase.

### One phase per session

Only implement the next incomplete phase — never two at once, even if asked. The reason: each phase is a checkpoint. If tests fail or the design needs adjustment, stopping at phase boundaries makes it easy to course-correct without unwinding work. If the user explicitly overrides this, acknowledge the risk and proceed.

---

## The harness pattern (why this works)

This pattern treats software development as a **feedback control loop**:

- **Feedforward guides** (CLAUDE.md, typed schemas, strict lint) steer agents *before* they act
- **Feedback sensors** (tests, typecheck, linting) detect errors *after* they act and enable self-correction
- **Phase boundaries** are checkpoints where humans can review and adjust before more work is built on top

Phases are ordered so that foundational, well-tested code exists before code that depends on it. This means errors surface when the affected code is small and easy to change.

The PROJECT_STATUS.md is both a plan and a live contract — it tells future agents exactly what was built, what wasn't, and what the next move is.

---

## Reference files

- `references/templates.md` — exact templates for CLAUDE.md, ARCHITECTURE.md, and PROJECT_STATUS.md
