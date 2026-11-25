---
name: follow-principles
description: Identify and apply the principles of the given context in the work
argument-hint: "[scope]"
allowed-tools:
  - read
  - grep
  - find_file_by_name
  - exec
  - skill
  - ask_user_question
  - todo_write
related:
  - report
  - suggest-next-action
  - scan-codebase
  - search
  - deep-analyze
  - ask-me
  - check-reference
  - deep-review-codebase
  - refactor

---

## Goal

Identify the real principles, conventions, and requirements of the context, then explicitly apply them to the current task

## Scope

Use when checking or following the principles of a specific project, framework, team, or skill — without inventing or adding anything beyond what exists — including checking files that match a principle conveyed through their file name (`### 7`, merged from `/follow-principles-engineering`)

## Execute

### 1. Identify Context

> Goal: determine which context's principles are needed

1. Take the context from the user, the task, or the current workspace
2. Classify it: `project`, `framework`, `language`, `team`, `skill`, `domain`
3. If the context is unclear → ask the user first via `/ask-me`
4. Record the context name and scope

### 2. Discover Principle Sources

> Goal: find where the principles live

1. Use `/scan-codebase` and `/search-files-patterns` to find standard files:
   - `PRINCIPLES.md`, `ARCHITECTURE.md`, `DESIGN.md`
   - `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`
   - `global_rules.md`, `AGENTS.md`
   - the principles/conventions sections of `README.md`
   - `docs/principles/`, `.github/`, `.devin/`
2. Search the `SKILL.md` of related skills, especially the `Rules` and `Expected Outcome` sections
3. Run `/deep-analyze` or `/check-reference` to verify the sources are complete
4. Check `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml` to see the ecosystem
5. Record every source found, with paths

### 3. Extract Principles

> Goal: distill the usable principles

1. Read all principle source files
2. Group the principles:
   - `design` — architecture, patterns, coupling/cohesion
   - `coding` — style, conventions, safety
   - `process` — workflow, review, commit, release
   - `communication` — naming, docs, reports
3. Identify principles that conflict with each other
4. Summarize them as actionable bullet points

### 4. Prioritize For Current Task

> Goal: pick the principles relevant to the task

1. Compare the principles against the task's goal and scope
2. Order by impact: `must`, `should`, `may`
3. If there's a conflict → state the priority and the reason
4. Ask the user if the priority is unclear

### 5. Apply Principles

> Goal: use the principles in the work

1. Cite the principle before deciding, e.g. "per principle X, do Y"
2. Adjust code, structure, or content accordingly
3. Use the principles when reviewing or validating the result
4. If a principle can't be followed 100% → state the reason and trade-off

### 6. Report

> Goal: summarize the principles used

1. Use `/report` showing: Principle, Source, Priority, Applied
2. Summarize the key principles that shaped the work
3. Run `/suggest-next-action`

### 7. Check File Against Filename Principle (Conditional — merged from `/follow-principles-engineering`)

> Goal: check that a file matches the software engineering principle indicated by its file name

1. Derive the principle from the file name: `single-responsibility.ts` → SRP, `open-closed.ts` → OCP, `dry-utils.ts` → DRY, `simple-component.ts` → KISS, `clean-architecture.ts` → Clean Architecture (principle names use kebab-case); doesn't match any principle → stop and report
2. Read the target file; check structure, logic, and naming against the principle; gather objective evidence with `/deep-review-codebase` (function/SRP metrics, naming)
3. List violations ordered by severity: Critical (completely breaks the principle) / High (significant but still works) / Medium (should fix) / Low (minor)
4. Report a table: No., Principle, Match Status, Violations (severity), Recommendations — recommend better patterns/examples present in the codebase; fixes needed → route to `/refactor`

## Rules

### 1. Evidence Based

- Never invent principles without a source
- State the source of every principle used
- If there's no clear principle → report instead of interpreting on your own

### 2. Context Specific

- Principles must fit the stated context — don't use another context's principles without reason
- If several contexts apply → state their order and interaction

### 3. Minimal And Traceable

- Use only the principles that affect the current task
- Record each decision that cites a principle
- Don't use principles as excuses to over-engineer

### 4. Safety

- If a principle conflicts with safety or correctness → ask the user or stop
- Don't cling to a principle at the cost of the work's correctness

### 5. Software Engineering Principles Catalog

- SOLID: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- DRY (Don't Repeat Yourself), KISS (Keep It Simple), YAGNI (You Aren't Gonna Need It)
- Separation of Concerns — split concerns by responsibilities, in both logic and naming
- Clean Architecture — clear layer separation, correct dependencies
- Functional Programming — pure functions, immutability
- TDD — test before implement
- Check criteria per principle: SRP = 1 unit = 1 responsibility, DRY = no duplicated code/logic, KISS = simple, not over-engineered, Clean Arch = clear layers, SoC = cleanly separated concerns

## Expected Outcome

- The list of principles found, with sources
- The principles applied to the current task
- A report of the actions taken and the next action
- No interpretation or invention of principles beyond the sources
- Files checked per `### 7` have a match/violations/severity summary with a recommendation
