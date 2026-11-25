---
name: feature-dev
description: Develop a feature from documentation (PRD, ARD, design doc, implementation plan) with automatic role detection based on project tech stack
context: fork
argument-hint: [PRD path or feature description]
---

# Feature Development

End-to-end feature implementation from documentation to working code. Automatically detects and applies the appropriate engineering role based on the project's tech stack.

## 1. Receive and Parse Documentation

Gather all input documentation provided by the user:

- **Accepted formats**: PRD, ARD (Architecture Decision Record), design doc, implementation plan, ticket/issue, or any structured feature specification
- Read every provided document thoroughly
- Extract and organize:
  - **Goal**: what the feature does (1–2 sentences)
  - **Requirements**: functional and non-functional
  - **Acceptance criteria**: how to verify the feature works
  - **Implementation plan**: ordered steps, architecture decisions, data models, API contracts
  - **Constraints**: performance, security, compatibility, dependencies
  - **Out of scope**: what this feature explicitly does NOT cover

**Check for an existing implementation plan.** Search the documentation, linked files, and project directory for an implementation plan (file named `*plan*`, `*implementation*`, or a plan section inside the PRD/ARD). If one exists — it is the authority. Proceed to Step 2 with the existing plan loaded.

If the documentation is ambiguous or incomplete, ask the user before proceeding.

## 2. Detect Tech Stack and Apply Role

Determine the project's tech stack and apply the appropriate engineering role:

1. **Read project's `AGENTS.md`** — look for tech stack declaration (language, framework, runtime)
2. **Scan project files** — check `package.json`, `pom.xml`, `*.csproj`, `requirements.txt`, `go.mod`, `Cargo.toml`, or equivalent to confirm
3. **Role matching** — select the relevant Windsurf role guidance based on the detected stack and file ownership:
   - If multiple specializations match (e.g., fullstack) — apply all relevant roles
   - If no specialization role exists — fall back to base engineering principles
4. **Announce** the detected stack and applied role(s) to the user for confirmation

**Examples:**
- Next.js + TypeScript → `frontend-engineer` role applies
- Spring Boot → `java-engineer` role applies
- Python + FastAPI → `python-engineer` role applies
- Terraform / Docker / K8s → `devops-engineer` role applies
- Cloud architecture / landing zones / networking / multi-cloud → `cloud-architect` role applies
- GitHub Actions / CI/CD pipelines / deployment strategy → `devops-architect` role applies
- React Native / Flutter / iOS / Android → `mobile-engineer` role applies
- ETL / Spark / dbt / Airflow / data pipelines → `data-engineer` role applies
- SQL / database schema / migrations / query optimization → `db-engineer` role applies
- ARCHITECTURE.md / system design / component boundaries → `system-architect` role applies
- LLM / RAG / agents / memory / multi-agent / AI pipelines → `ml-engineer` role applies + consult `context-engineering` skill for context pipeline design

## 3. Analyze Codebase Context

Before writing any code, understand the existing codebase:

1. **Project structure** — directory layout, module boundaries, entry points
2. **Existing patterns** — naming conventions, error handling, logging, testing approach
3. **Dependencies** — installed packages, available libraries, version constraints
4. **Related code** — files and modules the new feature will interact with, extend, or modify
5. **Test infrastructure** — test framework, test file locations, existing test patterns

Map how the new feature fits into the existing architecture. Identify:
- Files to **create** (new modules, components, tests)
- Files to **modify** (integration points, routes, configs)
- Files to **not touch** (unrelated code — minimize blast radius)

## 4. Resolve Implementation Plan

<plan_policy>
An implementation plan is MANDATORY. Never start coding without an approved plan.

**If a plan already exists** (from documentation, PRD, ARD, or `plan` skill output):
- Use it as-is. Do NOT rewrite, reorder, or simplify it
- Follow it STRICTLY — step by step, in the exact order specified
- Present the loaded plan to the user for confirmation before proceeding

**If no plan exists:**
- Create one from scratch based on the parsed requirements and codebase analysis
</plan_policy>

When creating a plan, break the feature into ordered, atomic implementation steps:

1. Number each step sequentially
2. Each step = one logical unit of work (one file or one cohesive change across tightly coupled files)
3. Order by dependency — implement foundations before consumers
4. Interleave test steps with implementation (do not defer all tests to the end)

Present the plan to the user:

```
Feature: [name]
Stack: [detected] | Role: [applied]
Plan source: [loaded from <file> | created from scratch]
Steps:
  1. [description] → [file(s)]
  2. [description] → [file(s)]
  ...
  N. [description] → [file(s)]
```

Wait for user approval before proceeding. The user may reorder, add, remove, or modify steps.

## 5. Implement

Execute the approved plan STRICTLY step by step. Do not skip steps, reorder steps, or combine steps.

<plan_adherence>
**Hard rules:**
- Follow the plan in the EXACT order approved by the user
- Complete each step fully before moving to the next
- Do not add steps that are not in the plan
- Do not skip steps you consider unnecessary
- Do not silently modify the plan's intent

**If the plan needs correction** (a step is blocked, wrong, or a new step is needed):
1. STOP implementation immediately
2. Explain to the user what happened and why the plan needs to change
3. Propose the specific correction (add/remove/modify steps)
4. Wait for user approval
5. Update the plan document if one exists as a file
6. Resume implementation from the corrected point

Never silently deviate from the plan. Every deviation requires explicit user approval.
</plan_adherence>

**For each step:**
1. State what you are about to do (step number, file, change summary)
2. Write code following:
   - Project's existing patterns and conventions
   - Active role's guidelines (stack-specific best practices)
   - Documentation's architecture decisions and constraints
3. Verify the code compiles/parses without errors after each step
4. If a step introduces a new dependency — install it immediately

**Rules:**
- Minimal, focused changes — do not refactor unrelated code
- Follow existing code style (indentation, naming, imports)
- Add imports at the top of files
- Production-quality code — no TODOs, no placeholders, no stubs (unless the plan explicitly calls for them)
- If you encounter an unexpected issue — stop and consult the user

## 6. Write Tests

For each implemented component, write tests following the project's test infrastructure:

1. **Unit tests** — business logic, utilities, data transformations
2. **Integration tests** — API endpoints, database queries, service interactions
3. **Component tests** (frontend) — UI components with user interactions
4. Cover both **happy path** and **edge cases** (error handling, boundary values, empty states)
5. Run the tests and verify they pass

If the documentation specifies acceptance criteria, write tests that directly verify each criterion.

## 7. Verify

Run the full verification sequence:

1. **Build/compile** — project builds without errors or warnings
2. **Lint** — run the project's linter if configured
3. **Test** — run the full test suite (new + existing) to catch regressions
4. **Acceptance check** — review implementation against documentation's acceptance criteria

**Checklist:**
- [ ] All acceptance criteria from the documentation are met
- [ ] No new warnings or errors in build output
- [ ] All tests pass (new and existing)
- [ ] No unrelated files were modified
- [ ] Code follows project conventions and active role's guidelines

If any check fails — fix the issue and re-verify.

## 8. Summary

Present the completed work:

- **Feature**: what was implemented
- **Stack / Role**: detected tech stack and applied role(s)
- **Files changed**: list of created and modified files with brief descriptions
- **Tests**: number of tests added, pass status
- **Acceptance criteria**: status of each criterion (met / partially met / not met)
- **Notes**: deviations from original plan, trade-offs, follow-up items

## Integration

- **Precedes**: `run-tests` skill, `pre-commit` skill, `create-pr` skill
- **Planning**: `plan` skill (produces the implementation plan this workflow executes)
- **Skills**: `test-strategy` skill (test strategy), `code-review` skill (review standards), `context-engineering` skill (context pipelines, RAG, agent harness, production checklists — for AI/LLM features), `worktree-isolation` skill (branch isolation via git worktree)
