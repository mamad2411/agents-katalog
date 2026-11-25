---
name: architecture-awareness
description: Detects project type, analyzes existing patterns, generates architecture specifications, and maintains architectural consistency across sessions. The key innovation that turns CLAUDE.md-style contracts into automatic, evolving project specifications.
invoke_when: Use when a project has no .shipworthy/architecture.md, running /scaffold, adding new technology to the project, or making a significant architectural decision during brainstorming.
---

# Architecture Awareness

## Purpose

This skill solves the critical problem of **architectural amnesia** — when AI coding assistants forget project constraints between sessions. It generates and maintains an architecture specification that acts as a persistent, enforceable contract.

## When This Skill Activates

1. **No architecture spec exists** — first interaction with a new project
2. **User runs `/scaffold`** — explicit regeneration request
3. **New technology detected** — package.json/requirements.txt changes
4. **Architectural decision made** — during brainstorming, a decision warrants documentation

## User Tier Detection

The session-start hook detects a project's maturity tier based on these signals. Architecture awareness should adapt its behavior to the detected tier.

### Tier Signals

| Signal | How to Detect | What It Means |
|--------|--------------|---------------|
| Has code | `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `setup.py`, `pyproject.toml` exist | Project has been initialized with a language/framework |
| Has tests | `tests/`, `__tests__/`, `test/`, `spec/` directories exist, or files matching `*.test.*`, `*.spec.*`, `test_*.py`, `*_test.go` | Project has some test coverage |
| Has CI | `.github/workflows/`, `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile`, `.travis.yml`, `.buildkite/` exist | Project has automated quality checks |
| Has architecture | `.shipworthy/architecture.md` exists | Project has documented constraints |

### Tier Definitions

- **Builder** (no code OR no tests): Focus on getting working code first. Architecture spec should be lightweight — just Project Identity and 3-5 Mandatory Rules. Do not overwhelm with sections the project is not ready for yet.
- **Maker** (code + tests, no CI/architecture): Standard architecture spec with all sections. Recommend CI setup as part of architecture generation.
- **Engineer** (code + tests + CI/architecture): Full architecture spec with strict rules. Include Quality Gate Levels and Performance Budgets sections.

### Adapting Spec Generation to Tier

- **Builder**: Generate a minimal spec (Project Identity, Mandatory Rules, Directory Structure, Testing Strategy). Skip Quality Gate Levels and Performance Budgets unless the user asks.
- **Maker**: Generate a standard spec (all sections). Keep Common Mistakes to 5 items. Suggest but do not require CI configuration.
- **Engineer**: Generate a comprehensive spec (all sections fully populated). Include 8-10 Common Mistakes. Require CI configuration documentation.

## Coexistence with CLAUDE.md

Many projects already have a `CLAUDE.md` file that defines project-specific rules and conventions for AI assistants. When both `CLAUDE.md` and `architecture.md` exist (or when generating a new `architecture.md`), follow these rules:

### Detection
Check for `CLAUDE.md` (or `.claude/CLAUDE.md`) in the project root when generating or updating architecture.md.

### Incorporation Rules
1. **Read CLAUDE.md first**: Before generating architecture.md, read any existing CLAUDE.md and extract its rules.
2. **Do not conflict**: If CLAUDE.md says "use snake_case for files" and architecture.md would default to kebab-case, architecture.md MUST adopt snake_case. CLAUDE.md rules about the specific project take priority over template defaults.
3. **Do not duplicate**: If a rule exists in CLAUDE.md, reference it rather than copying it verbatim. Example: "See CLAUDE.md for commit message format" rather than restating the same rule.
4. **Complement, do not compete**: architecture.md should add engineering structure (Quality Gates, Performance Budgets, Testing Strategy) that CLAUDE.md typically does not cover. CLAUDE.md typically covers conventions and preferences.
5. **Document the relationship**: Include a note in architecture.md:
   ```
   ## Relationship to CLAUDE.md
   This project has a CLAUDE.md file. Rules in CLAUDE.md take priority for project-specific
   conventions. This architecture spec adds engineering structure (quality gates, testing
   strategy, performance budgets) that complements CLAUDE.md.
   ```

### Conflict Resolution
If there is a genuine conflict between CLAUDE.md and what architecture.md would recommend:
1. Flag the conflict to the user
2. Ask which rule should win
3. Document the resolution in architecture.md

## Context Budget

For large projects, the session-start hook has a 4000-character context budget. Architecture specs that exceed this limit will be summarized to just the Mandatory Rules section.

### Summary Section Requirement
Every architecture.md SHOULD have a Summary section at the top (under 500 characters) for quick context injection when the full spec exceeds the budget.

```markdown
# Architecture Specification: [Project Name]

## Summary
[Under 500 characters. Project type, language, framework, and the 3 most critical rules.
This section is used for context injection when the full spec is too large.]

## Project Identity
...
```

### How Summarization Works
1. The session-start hook checks if combined context exceeds 4000 characters
2. If it does, it extracts only the Mandatory Rules section
3. A note is added telling the assistant to read the full file for details
4. Skills that need full architecture context should read the file directly

### Best Practices for Budget-Friendly Specs
- Keep Mandatory Rules to 5-15 items, each on one line
- Use the Summary section for the essential identity and top 3 rules
- Move detailed examples and rationale into separate ADR files in `.shipworthy/decisions/`
- Prefer terse, actionable rules over verbose explanations

## Polyglot Projects

For projects with multiple languages (e.g., TypeScript frontend + Python backend, Go services + React UI), generate a composite architecture spec.

### Detection
A project is polyglot if it has multiple language indicators:
- `package.json` + `requirements.txt` (JS + Python)
- `package.json` + `go.mod` (JS + Go)
- `pom.xml` + `package.json` (Java + JS)
- Multiple `go.mod` files in subdirectories (Go monorepo)
- `Cargo.toml` + `package.json` (Rust + JS)

### Composite Spec Structure
For polyglot projects, the architecture spec should:

1. **Shared sections at the top**: Project Identity, Summary, and Mandatory Rules that apply to ALL languages.
2. **Language-specific sections**: Clearly scoped by directory path.

```markdown
## Mandatory Rules (All Languages)
1. All code must have tests
2. No secrets in source code
3. Use conventional commits

## TypeScript Rules (applies to: src/frontend/, src/shared/)
4. Strict mode enabled
5. No any types
6. Use React functional components

## Python Rules (applies to: src/backend/, scripts/)
7. Type hints required on all public functions
8. Use FastAPI for API endpoints
9. Format with black, lint with ruff

## Go Rules (applies to: services/)
10. Use standard library where possible
11. Error wrapping with fmt.Errorf
12. Table-driven tests
```

3. **Directory mapping**: Include a clear mapping of which rules apply where.
4. **Shared types/contracts**: Document how types are shared between languages (API schemas, protobuf, GraphQL, etc.).
5. **Build coordination**: Document how the different language components are built and tested together.

### Common Pitfalls in Polyglot Projects
- Applying JavaScript conventions to Python code (or vice versa)
- Missing integration tests between language boundaries
- Inconsistent error handling across language boundaries
- Different naming conventions in shared API contracts

## Phase 1: Project Detection

Analyze the project to understand its technology stack. Check for:

### Language & Framework Indicators
- `package.json` -> Node.js (check for Next.js, Express, React, Vue, etc.)
- `tsconfig.json` -> TypeScript (check strict mode, target, module system)
- `requirements.txt` / `pyproject.toml` / `setup.py` -> Python (check for FastAPI, Django, Flask)
- `go.mod` -> Go
- `Cargo.toml` -> Rust
- `pom.xml` / `build.gradle` -> Java/Kotlin

### Structure Indicators
- `src/app/` or `app/` -> Next.js App Router / framework convention
- `src/pages/` -> Next.js Pages Router or similar
- `src/components/` -> Component-based frontend
- `src/routes/` or `routes/` -> Express/backend routing
- `prisma/` or `drizzle.config.*` -> ORM usage
- `.github/workflows/` -> CI/CD with GitHub Actions
- `Dockerfile` / `docker-compose.yml` -> Containerized deployment
- `tests/` or `__tests__/` or `*.test.*` -> Testing patterns

### Existing Convention Indicators
- Read existing source files to detect naming patterns (camelCase, snake_case, PascalCase)
- Check import patterns (relative, absolute, aliases)
- Check error handling patterns
- Check existing test patterns (framework, location, naming)

## Phase 2: Template Selection

Select the most appropriate template from `templates/`:
- `nextjs.md` — Next.js applications (App Router or Pages Router)
- `express.md` — Express/Node.js API services
- `fastapi.md` — Python FastAPI services
- `go-service.md` — Go microservices
- `react-spa.md` — React single-page applications
- `generic-typescript.md` — TypeScript projects without specific framework
- `generic-python.md` — Python projects without specific framework
- `monorepo.md` — Multi-package repositories

If the project doesn't match any template, use the closest one and adapt.

For polyglot projects, combine relevant templates and use the composite spec structure described above.

## Phase 3: Specification Generation

### For Greenfield Projects (no existing code)
Fill the template with sensible defaults and best practices for the detected stack. **Prescribe what SHOULD BE.**

### For Brownfield Projects (existing code)
Analyze existing patterns and document them as-is. **Describe what IS.**

Critical rule: Do NOT impose alien patterns on existing codebases. If the project uses `snake_case` for files, the spec should say `snake_case`, not `kebab-case`. The spec should codify existing conventions, making them explicit and enforceable.

### Specification Structure

Generate `.shipworthy/architecture.md` with these sections:

```markdown
# Architecture Specification: [Project Name]

## Summary
[Under 500 characters. Project type, language, framework, and the 3 most critical rules.
Used for context injection when the full spec exceeds the budget.]

## Project Identity
- **Type**: [e.g., Next.js 14 App Router application]
- **Language**: [e.g., TypeScript 5.x strict mode]
- **Runtime**: [e.g., Node.js 20+]
- **Primary Framework**: [e.g., Next.js 14]
- **Package Manager**: [e.g., npm/pnpm/yarn/bun]

## Relationship to CLAUDE.md
[If CLAUDE.md exists: note the relationship. If not: omit this section.]

## Mandatory Rules
[Numbered list of 5-15 inviolable constraints specific to this project]
[These become the CLAUDE.md-style rules enforced at every session]

## Directory Structure
[Expected layout with purpose annotations]

## Naming Conventions
[File naming, variable naming, component naming, test naming]

## Type System
[Where types live, how shared between modules, strict mode rules]

## Testing Strategy
[Framework, file locations, naming patterns, coverage expectations]
[What MUST be tested vs what's optional]

## Error Handling
[Stack-specific error handling pattern]

## Security Baseline
[Stack-specific security requirements]

## Performance Budgets
[Default thresholds — bundle size, API response time, query limits]

## Quality Gate Levels
[Graduated thresholds configuration]
Level 1 (always): [checks]
Level 2 (10+ files): [checks]
Level 3 (50+ files): [checks]
Level 4 (100+ files): [checks]

## Common Mistakes
[5-10 documented pitfalls specific to this stack/project]
```

## Phase 4: User Approval

Present the generated specification to the user with:
1. Summary of what was detected
2. The full specification
3. Invitation to modify before saving

**Do NOT save architecture.md without user approval.** This is their project; the spec is a suggestion until they accept it.

## Phase 5: Evolution

When the architecture needs to change:
1. Identify what changed (new dependency, new pattern, architectural decision)
2. Propose specific updates to the relevant sections
3. Show the diff (old -> new)
4. Get user approval before updating

Track significant decisions as Architecture Decision Records in `.shipworthy/decisions/`:
```markdown
# ADR-NNN: [Decision Title]

## Status: [Accepted/Superseded/Deprecated]
## Date: [YYYY-MM-DD]

## Context
[What prompted this decision]

## Decision
[What was decided]

## Consequences
[What this means going forward]
```
