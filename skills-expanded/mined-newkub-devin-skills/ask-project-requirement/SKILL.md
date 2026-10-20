---
name: ask-project-requirement
description: Gather requirements via /ask-me with multi-select/multi-step questions and summarize them
argument-hint: "[topic]"
related:
  - ask-me
  - update-docs
  - alternative
  - ship
  - plan
  - follow-goal

---

## Goal

Ask for the requirements needed before starting a project, using multi-select and multi-step flows through `ask_user_question` or `/ask-me`, then summarize them into a requirements statement

## Scope

Use when starting a new project, or when the context is unclear, before making a plan

## Execute

### 1. Inspect Existing Context

> Goal: Know the context before asking

1. Read `AGENTS.md` if present
2. Read `rules/**/*.yml` if present
3. Read `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, or other key manifests
4. If there is no `AGENTS.md` → run `/update-agents-md` first

### 2. Multi-Step Requirement Interview

> Goal: Gather requirements step by step with multi-select

1. Design steps covering the topics below, with 1-4 questions per step
2. For questions that allow multiple answers, set `multi_select: true` and make the options comprehensive

#### Step 1: Interfaces And Users

- Ask about the interfaces involved, multi_select: web, desktop, CLI/TUI, mobile, SDK, library, API, PWA, others
- Ask about user personas, multi_select: end users, developers, business, partners, enterprise, internal ops, others
- Ask about mode: real-time, batch, async, offline, others

#### Step 2: Tech And Product Context

- Ask about ecosystem/runtime, multi_select: bun, node, deno, rust, go, python, kotlin, swift, others
- Ask about the product/domain context as text or single choice
- Ask about functional/non-functional requirements, multi_select: performance, security, compliance, reliability, observability, i18n, accessibility, others

#### Step 3: Scale And Constraints

- Ask about scale/traffic as text or single choice
- Ask about constraints, multi_select: security, privacy, compliance, data residency, integration, deployment, compatibility, budget, timeline
- Ask about definition of done, multi_select: tests, docs, observability, rollback, migration, others

#### Step 4: Libraries And Tools

- Ask whether `/alternative` should be used
- If a needed library is missing, ask which one should be recommended, multi_select from the candidates
- Ask about the required build/ship tools, multi_select

### 3. Synthesize Requirements

> Goal: Summarize the requirements into a statement

1. Collect the answers from every step into bullets or `requirement-summary.md`
2. If a library choice is needed → run `/alternative`
3. To continue with a plan → run `/plan`
4. To set a goal → run `/follow-goal`
5. Run `/update-agents-md` to update `AGENTS.md` with the requirements

### 4. Confirm

> Goal: Confirm before use

1. Run `/ask-me` so the user confirms the summary is correct
2. If not correct → re-ask only the unclear parts using multi-step
3. Save `requirement-summary.md` in the project root

## Rules

### 1. No Web UI

- Don't open a Web UI
- Don't run the `bun --filter` CLI
- Use `ask_user_question` or `/ask-me` only

### 2. Multi-Step And Multi-Select

- Ask in stages, with 1-4 questions per step
- Questions that allow multiple answers must set `multi_select: true`
- Ask only questions that do not have answers yet
- If unsure → run `/ask-me` again

## Expected Outcome

- Every requirement is explicit: answered, assumed (stated), or deferred with reason
- The user confirmed the gathered requirement list before any work starts
- A follow-up `/create-plan-in-dot-devin` or implement pass can run without re-asking
