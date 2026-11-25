---
name: agent-md-creator
description: "Create high-quality CLAUDE.md files and accompanying docs/ knowledge stores for projects. Use this skill whenever the user wants to create, write, generate, set up, or improve a CLAUDE.md file, AGENTS.md file, or project-level agent instructions. Also trigger when the user mentions 'project setup for Claude Code', 'agent onboarding', 'context engineering', 'harness setup', or asks how to configure Claude Code for a new or existing project. Trigger even if the user says 'set up my project for AI coding' or 'configure my repo for agents' without explicitly mentioning CLAUDE.md."
---

# CLAUDE.md Creator

Create lean CLAUDE.md files that act as a table of contents — not an encyclopedia — with a supporting `docs/` knowledge store for progressive disclosure.

The central insight: Claude Code wraps CLAUDE.md with a system reminder saying "this context may or may not be relevant." Irrelevant content causes the entire file to be de-prioritized. Keep it short, universally applicable, and pointed at deeper docs.

## Step 1: Gather Project Context

Before writing anything, understand the project. Ask the user or explore the codebase:

1. **What is this project?** — One-liner purpose, who it's for
2. **Tech stack** — Language, framework, database, key libraries
3. **Project structure** — Key directories and what they contain
4. **Essential commands** — Build, test, lint, deploy
5. **Critical rules** — Things that must never be violated (3-5 max)
6. **Workflow preferences** — Git conventions, commit format, PR process
7. **Gotchas** — Project-specific quirks or non-obvious patterns
8. **Existing docs** — READMEs, architecture docs, ADRs already in the repo?

If the user has an existing CLAUDE.md, read it and identify what to keep, what to move to docs/, and what to delete.

## Step 2: Choose the Setup

Pick based on project complexity:

**Small projects** (single app, small team):
```
CLAUDE.md                    # 40-80 lines
docs/
├── architecture.md          # If non-trivial
└── conventions.md           # If team has specific patterns
```

**Medium projects** (multiple modules, growing team):
```
CLAUDE.md                    # 60-100 lines, with docs index
docs/
├── architecture.md          # Service boundaries, data flow
├── conventions.md           # Naming, patterns, error handling
├── testing.md               # Test patterns, fixtures, strategies
└── deployment.md            # CI/CD, environments
```

**Large / monorepos:**
```
CLAUDE.md                    # 80-120 lines, with docs index
docs/
├── architecture.md          # Top-level domain map
├── conventions.md           # Universal patterns
├── testing.md               # Test strategies
├── database.md              # Schema, migrations
├── api-patterns.md          # API design, auth, errors
├── deployment.md            # CI/CD pipeline
└── decisions/               # Architecture Decision Records
packages/frontend/CLAUDE.md  # Module-scoped (auto-loaded)
packages/api/CLAUDE.md       # Module-scoped
```

**Placement rules:**
- Goes in CLAUDE.md if it applies to 100% of sessions (stack, commands, critical rules, docs index)
- Goes in docs/ if it's task-specific (architecture details, testing patterns, DB schema)
- Goes in hooks if it must happen deterministically (formatting, linting, pre-commit)
- Goes in subdirectory CLAUDE.md if it's module-scoped in a monorepo
- Code style belongs in linters, not CLAUDE.md — LLMs are in-context learners and follow existing patterns

## Step 3: Write the CLAUDE.md

Use this template. Adapt and delete sections that don't apply.

```markdown
# Project: [Name]

[One sentence: what this is, who it's for, core technology.]

## Stack
[Language] + [Framework] + [Database] + [Key libraries]

## Structure
- `src/` — [what's in here]
- `tests/` — [test organization]
- `docs/` — Agent docs (read relevant doc before starting work)

## Commands
- `[build]` — Build the project
- `[test]` — Run all tests
- `[lint]` — Lint check
- `[deploy]` — Deploy to [environment]

## Workflow
1. Read the relevant doc from `docs/` before starting work
2. Explore codebase before implementing changes
3. Make small, testable changes
4. Run tests after each change
5. [Git convention: commit format, branch naming]

## Docs
Read the relevant doc before working on that area:
- `docs/architecture.md` — [one-line description]
- `docs/conventions.md` — [one-line description]
- `docs/testing.md` — [one-line description]

## Critical Rules
- NEVER [inviolable rule 1, with reason]
- ALWAYS [inviolable rule 2, with reason]
- Do NOT [inviolable rule 3, with reason]
```

**Writing principles:**
- Target under 100 lines. Under 200 max (Anthropic's recommendation). Shorter is better.
- Be specific and verifiable: "Run `npm test` before committing" not "Test your changes."
- Include the reason for non-obvious rules — Claude makes better decisions when it understands why.
- Reserve CAPS/emphasis for 3-5 truly inviolable rules. When everything is critical, nothing is.
- Use `@imports` to reference existing docs: `See @README.md for overview` — don't duplicate.
- Use `file:line` pointers instead of inlining code snippets, which go stale.

**Don't include:**
- Code style rules (use linters + hooks)
- Personality instructions ("be a senior engineer")
- Rules Claude already follows naturally
- Task-specific instructions (put in docs/)

## Step 4: Write the docs/ Files

For each doc file referenced in the CLAUDE.md index:
- Start with a one-paragraph summary so Claude can quickly assess relevance
- Keep each file under 200 lines; split or add a table of contents if longer
- Use `file:line` pointers to source code, not inlined snippets
- Describe patterns and reasoning, not just prohibitions
- Make each file self-contained — it should be useful without reading the others

See `references/doc-templates.md` for example templates for architecture.md, testing.md, conventions.md, and other common doc files.

## Step 5: Verify and Deliver

Before delivering, check:
1. CLAUDE.md is under 120 lines. If over, move content to docs/.
2. Every line in CLAUDE.md is relevant to 100% of sessions.
3. Commands listed actually work (run them if you have codebase access).
4. No inlined code snippets — only file references.
5. Every docs/ file referenced in the index actually exists.

Deliver the CLAUDE.md, all docs/ files, and subdirectory CLAUDE.md files if applicable. If the user had an existing CLAUDE.md, show a before/after highlighting what moved to docs/ and what was removed.

Advise the user on maintenance: build the file organically (when Claude makes wrong assumptions, add the correction), prune monthly (delete rules Claude already follows naturally), and convert advisory instructions into hooks/linters whenever possible. When something fails, ask "what capability is missing?" and encode the fix into the repo.

## Reference

- `references/doc-templates.md` — Example templates for common docs/ files (architecture, testing, conventions, database, deployment, API patterns)
