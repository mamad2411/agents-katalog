---
name: fabrico-creating-instructions
description: "Creates Claude Code memory files (CLAUDE.md) for Claude Code. Covers the root project memory (CLAUDE.md) and nested, directory-scoped memory files, plus @import references. Provides templates and a decision framework for memory vs. skill placement. Use when creating, reviewing, or updating CLAUDE.md memory files."
---

# Creating Instructions

Creates well-structured memory files for Claude Code. Covers the root project "constitution" (`CLAUDE.md`) and granular, directory-scoped conventions (nested `CLAUDE.md` files), with clear guidance on what belongs in memory versus skills.

## Core Design Principles

<principles>

<instruction-types>
Two ways to encode project memory exist:

**Root project memory** (`CLAUDE.md` at the repository root): A single file per repository — the "constitution." Defines architecture, directory structure, languages, frameworks, library versions, and fundamental project constraints. Loaded automatically by Claude Code for ALL interactions in the project. No frontmatter required (it is plain Markdown). This is the first file any developer or AI agent should read to understand the project. A personal, untracked `CLAUDE.local.md` can hold developer-specific overrides.

**Nested / scoped memory** (`CLAUDE.md` files in subdirectories): Multiple files per repository. Plain Markdown, no frontmatter and no `applyTo` glob — scope is determined by file location. A `CLAUDE.md` inside `src/api/` applies to that subtree. Claude Code loads a nested `CLAUDE.md` when it works on files within that directory. These encode directory-specific or domain-specific coding conventions. You can also pull shared content into any `CLAUDE.md` with an `@import` reference (e.g. `@./docs/conventions.md`) instead of duplicating it.

| Aspect | Root project memory | Nested / scoped memory |
|---|---|---|
| File | `CLAUDE.md` (repo root) | `CLAUDE.md` (in a subdirectory) |
| Count per repo | Exactly one root file | Multiple, one per relevant subtree |
| Frontmatter | None (plain Markdown) | None (plain Markdown) |
| Applied when | Every Claude Code interaction in the project | Claude works on files within that directory subtree |
| Scoping mechanism | Whole project | File location (the directory it lives in and below) |
| Purpose | Project constitution — architecture, stack, fundamental rules | Scoped conventions — directory- or domain-specific rules |

There is no `applyTo` glob in Claude Code. Scope is by file location: a `CLAUDE.md` in a subdirectory applies to that subtree. For content that should be shared across several memory files, factor it into a separate Markdown file and pull it in with `@import` rather than copying it.
</instruction-types>

<instructions-vs-skills>
Memory files define **RULES** — declarative constraints that Claude Code must follow whenever they apply. They are project-specific, loaded automatically, and encode decisions for THIS repository.

Skills define **HOW** — procedural workflows loaded on-demand to perform specific tasks. Skills are generic, reusable across projects, and encode expert knowledge.

| If the content is... | It belongs in... | Example |
|---|---|---|
| A project-specific rule or constraint | Memory (`CLAUDE.md`) | "Use `date-fns` instead of `moment.js` — moment.js is deprecated" |
| A step-by-step workflow for performing a task | Skill | "How to perform code review with severity categorization" |
| A coding convention for a specific directory/subtree | Memory (nested `CLAUDE.md`) | "React components use functional style with hooks" |
| A reusable process template across projects | Skill | "How to create a new API endpoint with validation" |
| An architectural decision for this repository | Memory (root `CLAUDE.md`) | "This is a monorepo with apps/ and packages/ structure" |
| Domain knowledge needed to execute a task | Skill | "E2E testing patterns with Playwright Page Objects" |
| Technology stack and version requirements | Memory (root `CLAUDE.md`) | "TypeScript 5.4, React 19, Next.js 15" |
| A coding standard that linters don't enforce | Memory (nested `CLAUDE.md`) | "Business logic must not import from UI layer" |

**Mental model**: Memory files are "the law" (always in force). Skills are "expert handbooks" (consulted for specific tasks).
</instructions-vs-skills>

<conciseness>
Memory files compete for the context window with conversation history, skills, and the actual task.

- Keep memory short and self-contained — each rule should be a single, simple statement.
- Include the reasoning behind rules (e.g., "Use `date-fns` instead of `moment.js` — moment.js is deprecated and increases bundle size").
- Show preferred and avoided patterns with concrete code examples — Claude responds more effectively to examples than abstract rules.
- Focus on non-obvious rules — skip conventions that standard linters/formatters already enforce.
- Whitespace between rules is ignored — format for legibility.
- Prefer `@import` over duplication when several memory files need the same content.
</conciseness>

</principles>

## Creation Process

Use the checklist below and track progress with the **TodoWrite** tool:

```
Creation progress:
- [ ] Step 1: Determine the memory type
- [ ] Step 2: Define the memory scope
- [ ] Step 3: Gather content for the memory file
- [ ] Step 4: Write the memory file
- [ ] Step 5: Validate the memory file
```

**Step 1: Determine the memory type**

Determine from context or ask the user. Use the **AskUserQuestion** tool to clarify the user's intent if it's ambiguous:
- Is this a NEW project needing its first root `CLAUDE.md`? → Create root project memory.
- Are there an existing root `CLAUDE.md` and directory-specific rules are needed? → Create a nested `CLAUDE.md` in the relevant subdirectory.
- Unsure? → Check if a root `CLAUDE.md` exists. If not, recommend creating it first. The constitution comes before specific laws.

**Step 2: Define the memory scope**

For **root project memory**, the scope is always the entire project. Research by:
- Reading `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent to identify languages, frameworks, and versions.
- Analyzing the directory structure to understand architecture (monorepo, feature-based, layered, etc.).
- Reading existing config files (`.eslintrc`, `tsconfig.json`, `.prettierrc`, etc.) to understand tooling.
- Checking for existing README or architectural documentation.

For **nested / scoped memory**, determine:
- Which directory subtree the rules apply to (this is where you place the `CLAUDE.md`).
- What specific conventions exist for that subtree.
- Whether an existing memory file already covers this scope (avoid placing overlapping rules in parent and child memory files).

Scoping reference (file location, not globs):

| Place `CLAUDE.md` at... | Applies to |
|---|---|
| Repository root | The whole project (every interaction) |
| `src/` | All files under `src/` |
| `src/components/` | All files under the components directory |
| `src/api/` | All API-related files in that subtree |
| `tests/` | The test subtree (collocated conventions, fixtures, etc.) |

For TypeScript-vs-test or other file-type distinctions that don't map cleanly to a directory, encode the rule as a clearly-worded statement in the nearest enclosing `CLAUDE.md` (e.g. "Test files (`*.test.ts`) use ..."). There is no glob-based targeting — use prose plus location.

**Step 3: Gather content for the memory file**

For **root project memory** (the constitution), research and document:
1. **Architecture** — Overall architecture pattern (monorepo, microservices, modular monolith, etc.), directory structure, and responsibility of each top-level directory.
2. **Technology Stack** — ALL languages, frameworks, and key libraries with specific versions. Critical — Claude Code needs exact versions to generate compatible code.
3. **Coding Conventions** — Conventions NOT enforced by linters/formatters. Architectural rules (e.g., "business logic must not import from UI layer"), project-specific naming conventions, and agreed-upon patterns.
4. **Error Handling** — The project's error handling strategy.
5. **Testing Strategy** — Testing approach (unit, integration, E2E), frameworks, and key patterns.
6. **Development Workflow** — How developers interact with the project. Document task runners (Make, Taskfile, npm scripts, Turbo), containerization (Docker Compose commands), and common developer commands (build, test, lint, migrate, seed). Claude Code should use the same scripts and tools a regular developer would — never raw commands when a script exists.

For **nested / scoped memory**, research and document:
- Specific conventions for the target directory subtree.
- Preferred patterns with code examples.
- Anti-patterns to avoid with code examples.
- Reasoning behind non-obvious rules.

Use the `./assets/claude-md.template.md` and `./assets/nested-claude-md.template.md` templates as starting points.

**Step 4: Write the memory file**

For **root project memory**:
- Create the file at `CLAUDE.md` in the repository root.
- No frontmatter — it is plain Markdown.
- Use clear Markdown headers to organize sections.
- Use the `./assets/claude-md.template.md` template.
- Factor out content shared with other memory files into a separate Markdown file and reference it with `@import` (e.g. `@./docs/conventions.md`).

For **nested / scoped memory**:
- Create the file as `CLAUDE.md` inside the target subdirectory (e.g. `src/api/CLAUDE.md`, `src/components/CLAUDE.md`).
- No frontmatter and no `applyTo` — placement determines scope.
- Keep it focused on conventions unique to that subtree; do not repeat root-level rules.
- Use the `./assets/nested-claude-md.template.md` template.

Memory mechanics reference:

| Mechanism | Description |
|---|---|
| Root `CLAUDE.md` | Loaded for every interaction in the project. Plain Markdown, no frontmatter. |
| Nested `CLAUDE.md` | Loaded when Claude works within that directory subtree. Scope = file location. |
| `@import` | Pull shared Markdown into any memory file (e.g. `@./docs/conventions.md`) to avoid duplication. |
| `CLAUDE.local.md` | Personal, untracked overrides for an individual developer (gitignored). |

**Step 5: Validate the memory file**

```
Validation:
- [ ] File is in the correct location (root `CLAUDE.md`, or `CLAUDE.md` inside the intended subdirectory)
- [ ] No frontmatter (memory files are plain Markdown — no YAML, no applyTo)
- [ ] Scope is correct — the file lives in the directory whose subtree the rules govern
- [ ] Rules are short and self-contained — each rule is a single statement
- [ ] Non-obvious rules include reasoning ("because...")
- [ ] Preferred/avoided patterns include concrete code examples
- [ ] Shared content is pulled in via @import rather than duplicated across memory files
- [ ] No duplication of rules already enforced by linters/formatters
- [ ] No procedural workflow content (that belongs in skills)
- [ ] No agent personality or behavior definitions (that belongs in a subagent, `.claude/agents/*.md`)
- [ ] No slash-command / workflow triggers (that belongs in a command, `.claude/commands/*.md`)
- [ ] Root file covers: architecture, stack with versions, key conventions
- [ ] Nested files live in the right subtree and do not repeat root-level rules
```

## Quick Reference

### Memory File Types

| Type | Location | Purpose | Loading |
|---|---|---|---|
| Root project memory | `CLAUDE.md` (repo root) | Project constitution | Always loaded for the project |
| Nested / scoped memory | `CLAUDE.md` (in a subdirectory) | Scoped conventions | Loaded when working in that subtree |
| Imported memory | Any Markdown referenced via `@import` | Shared content reused across memory files | Pulled in wherever it is imported |
| Personal memory | `CLAUDE.local.md` (repo root, gitignored) | Developer-specific overrides | Loaded locally for that developer only |
| User (global) memory | `~/.claude/CLAUDE.md` | Cross-project personal defaults | Loaded for all projects on that machine |

### Priority Order

Higher takes precedence on conflict:

1. Nested / more-specific `CLAUDE.md` (closest to the files being worked on) — highest
2. Root project `CLAUDE.md`
3. User (global) `~/.claude/CLAUDE.md` — lowest

Personal `CLAUDE.local.md` overrides apply on top of the project's tracked memory for the individual developer.

## Connected Skills

- `fabrico-creating-agents` - to ensure subagent files (`.claude/agents/*.md`) don't embed coding standards that belong in memory
- `fabrico-creating-skills` - to understand the boundary between procedural knowledge (skills) and declarative rules (memory)
- `fabrico-creating-prompts` - to ensure slash commands (`.claude/commands/*.md`) reference memory rather than duplicating conventions
- `fabrico-technical-context-discovering` - the complementary skill that discovers and reads existing memory files
- `fabrico-codebase-analysing` - to analyze existing memory files and identify patterns to follow
