---
name: pbs-codebase-familiarization
description: "Use when starting work on an existing codebase for the first time, or returning after a long absence, before any feature planning"
---

# Codebase Familiarization

## Overview

Progressive scan of an existing codebase in 3 levels: surface, environment, impact zone. Understand enough to work safely without understanding everything.

**Core principle:** Scan progressively, not exhaustively. Start at the surface and deepen only where your feature needs it. Never try to "understand the whole project."

**Announce at start:** "I'm using the pbs-codebase-familiarization skill to understand this codebase before planning any changes."

## When to Use

- First time working on an existing codebase
- Starting a new feature in a project you haven't touched recently
- Onboarding to a project before making any changes

## When to Skip Levels

- Already know the codebase → skip Level 1-2, go to Level 3
- Nothing changed since last time → quick refresh of Level 3 only
- Feature is trivial (< 4 hours) → skip the framework entirely

## The Process

### Level 1: Surface (15-30 min) — NO code reading

Understand what the project IS without reading any source code.

| # | Source | What to extract |
|---|--------|-----------------|
| 1 | README / CONTRIBUTING | What the project is, who maintains it |
| 2 | Directory structure | Architectural pattern (monorepo, modular, flat) — `tree -L 2` |
| 3 | Package files | Stack, key dependencies, available scripts |
| 4 | Config files | Linter, CI/CD, DB, environment setup |
| 5 | CLAUDE.md / AGENTS.md / .cursorrules | Project conventions, constraints, patterns |
| 6 | Internal docs / ADRs | Architecture decisions, diagrams |
| 7 | Recent issues / PRs | What's active, what's broken |

**Goal:** Can describe the project in 2-3 sentences. Know the stack and directory structure.

### Level 2: Environment (30-60 min) — still no business logic

Get the project running locally.

| # | Question | Where to look |
|---|----------|---------------|
| 1 | What do I need to install? | README, CONTRIBUTING, Dockerfile |
| 2 | Environment variables needed? | `.env.example`, docker-compose, docs |
| 3 | How to run locally? | README, Makefile, package.json scripts |
| 4 | Database needed? How to initialize? | docker-compose, migrations, seeds |
| 5 | External services required? | `.env.example`, docs |
| 6 | How to run tests? | README, CI config, package.json |
| 7 | Linter/formatter and how to run? | Config files, pre-commit hooks |
| 8 | CI/CD flow? | `.github/workflows/`, `.gitlab-ci.yml` |

**REQUIRED:** Use superpowers:verification-before-completion — verify the project RUNS locally and tests PASS before proceeding. If it doesn't run, that's a problem to solve before touching any code.

**Goal:** Project runs locally. Tests pass. Know the dev workflow (edit → test → lint → commit).

### Level 3: Impact Zone (1-3 hours) — NOW read code, surgically

Identify the files, modules, and flows relevant to YOUR feature.

**Search strategy — search by layers, never read entire files:**

1. **Search by keywords:** grep/ripgrep for terms related to your feature
2. **Read headers:** first 30-50 lines of each relevant file to understand purpose
3. **Read specific functions:** only the functions you actually need to understand
4. **NEVER read an entire 500+ line file** unless absolutely necessary

**Steps:**

1. **Search by keywords** related to the feature (routes, endpoints, models, services)
2. **Trace the flow** from entry point (route/endpoint/handler) through the chain of calls
3. **Map dependencies** — what depends on what you'll touch? What consumes it?
4. **Identify reference module** — find existing similar code to follow as pattern
5. **Map existing tests** in the impact zone — what's already tested?
6. **Check for conflicts** — any PRs or features in progress touching the same files?

**Goal:** List of relevant files, understood flow, identified patterns to follow.

### Step 4: Generate Context Map

Generate `.pbs-framework/features/[feature-name]/codebase-context-map.md`:

```markdown
# Codebase Context Map

## Date: [date]
## Project: [project name]
## Feature: [short description of the feature to implement]

---

## 1. Project Overview
### What it is
[2-3 sentences describing the project]

### Stack
| Component | Technology | Version |
|-----------|-----------|---------|
| Language | | |
| Framework | | |
| Database | | |
| Testing | | |
| CI/CD | | |

### High-level structure
[Main directories with one-line explanation each]

---

## 2. Development Environment
### Prerequisites
- [tool 1] (version)

### Required environment variables
| Variable | Purpose | Example value |
|----------|---------|---------------|

### Steps to run
1. [step 1]
2. [step 2]

### Steps to test
- Unit tests: [command]
- Integration tests: [command]
- Linter: [command]

### External services needed
| Service | Purpose | How to run locally |
|---------|---------|-------------------|

---

## 3. Feature Impact Zone
### Feature description
[What needs to be implemented — in your own words]

### Relevant files identified
| File | Relevance | What it does |
|------|-----------|-------------|
| src/... | High — modify | [description] |
| src/... | Medium — read/understand | [description] |
| src/... | Reference — pattern to follow | [description] |

### Current related flow
[Description or ASCII diagram of the current flow the feature touches]
[entry point] → [service A] → [model B] → [output]

### Codebase patterns to follow
- Module pattern: [how similar modules are structured]
- Testing pattern: [how this type of functionality is tested]
- Naming conventions: [what you observed]
- Error handling: [observed pattern]

### Existing tests in the zone
| Test file | What it covers | Relevance |
|-----------|---------------|-----------|

### Reference module
[Name of the existing module most similar to what you need]
[Why it's a good reference]

---

## 4. Discovered Constraints and Conventions
- [convention 1 — observed in code]
- [convention 2 — documented in AGENTS.md/docs]
- [restriction 1 — something NOT to do]

---

## 5. Open Questions
[Things you couldn't resolve with the scan]
- [question 1]
- [question 2]

---

## 6. Implementation Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Touching X could break Y] | | |
```

## Readiness Signals

Familiarization is complete when:
- [ ] Can describe the project in 2-3 sentences
- [ ] Project runs locally and tests pass
- [ ] Have a list of files relevant to the feature
- [ ] Identified a reference module (pattern to follow)
- [ ] Know what tests exist in the impact zone
- [ ] Open questions are documented (not blocking)

<HARD-GATE>
The human MUST validate the context map is correct before any planning begins.
If the human identifies missing areas or incorrect assumptions, investigate further.
Do NOT start feature planning or implementation until the human approves.
</HARD-GATE>

## Common Mistakes

- **Reading entire 500+ line files** — search first, read headers, then read specific functions. Never the whole file.
- **Skipping Level 2 (environment)** — if you can't run the project and tests, you can't validate anything you build.
- **Empty "Reference module" in context map** — there's always a similar module. If you didn't find one, you didn't search enough.
- **Describing the project without running it** — a README can be outdated. Running the project is the real verification.

## Red Flags

- "Let me read the entire codebase" → NO. Scan progressively — surface, then environment, then impact zone only.
- "I understand the project" without running it → Level 2 is not complete. Run it first.
- Reading entire 500+ line files → Read only relevant functions. Search first, read second.
- Skipping Level 2 to jump to code → If the project doesn't run locally, you can't validate anything.
- Empty "Reference module" in the context map → There's always a similar module. Find it.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I can figure it out as I go" | That's how you break things you didn't know existed. |
| "The README has everything I need" | READMEs are often outdated. Verify by running the project. |
| "I don't need to run tests, I'll just read the code" | If you can't run tests, you can't validate your changes. |
| "This module is too complex to scan quickly" | You don't need to understand all of it — only the parts your feature touches. |
| "The feature is simple, I don't need a context map" | Simple features in complex codebases cause the most unexpected breakage. |

## Integration

**Entry point:** This is the first skill for existing codebase work — no prerequisites.

**Required skills:**
- **REQUIRED:** superpowers:verification-before-completion — Level 2: verify project runs and tests pass

**Calls next:**
- pbs-exploration-brainstorming (lightweight mode) — if the feature needs exploration
- pbs-feature-planning — if the feature is already clear and well-defined

**Language:** Write all `.pbs-framework/` documents in the language defined in AGENTS.md `framework_language` field.
