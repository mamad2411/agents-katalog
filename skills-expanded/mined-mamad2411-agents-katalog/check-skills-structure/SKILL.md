---
name: check-skills-structure
description: Check skill package structure (frontmatter, references, workflows, subagents, src, MCP) with one CLI
argument-hint: "[root] [--skill <name>] [--json] [--findings] [--detail]"
allowed-tools:
  - exec
  - grep
  - glob
  - find_file_by_name
  - read
related:
  - check-my-global-cli
  - update-devin-global-skills
  - review-devin-global-harness
  - deep-validate
  - report
  - use-scripts

---

## Goal

Inspect the structure of skill packages in `%APPDATA%\devin\skills\` — frontmatter fields, `references/`, `workflows/`, `subagents/`, `best-practices/`, `src/`, `scripts/`, MCP, website — with a single CLI command that outputs a bullet list + findings

## Scope

Use to inventory/audit skill structure across the whole repo or a single skill — read-only check, reproducible via `scripts/check-skills-structure.ts` (Bun, zero deps)

- Boundary: detailed convention linting (related contract, section order, naming) → `/review-devin-global-harness`; per-skill frontmatter validation → `/deep-validate`; this skill = a fast structural inventory table

## Execute

### 1. Run Check

> Goal: get a bullet-list structure of every skill

```bash
bun "check-skills-structure/scripts/check-skills-structure.ts"                    # whole repo (default root = %APPDATA%/devin/skills)
bun "check-skills-structure/scripts/check-skills-structure.ts" --skill refactor   # single skill
bun "check-skills-structure/scripts/check-skills-structure.ts" --findings          # warnings only
bun "check-skills-structure/scripts/check-skills-structure.ts" --json              # machine-readable
bun "check-skills-structure/scripts/check-skills-structure.ts" --detail            # show every entry name per skill
bun "check-skills-structure/scripts/check-skills-structure.ts" <custom-root>       # another repo
```

Besides the bullet counts, use `--skill <name>` or `--detail` to see the **actual names** per skill — `related`, `references`, `workflows`, `subagents`, `best-practices`, `scripts`, `frontmatter-missing`

### 2. Interpret Output

> Goal: read each field — 1 bullet per skill (`- <skill> — Field: value, ...`)

| Field | Meaning |
|--------|----------|
| `Skill` | the skill's directory name (bullet name) |
| `Frontmatter` | frontmatter keys present x/10 (`name`, `description`, `argument-hint`, `allowed-tools`, `related`, `model`, `triggers`, `permissions`, `subagent`, `agent`) |
| `Name` | `ok` = frontmatter name matches the dir, `!=` = mismatch, `missing` |
| `Related` | number of entries in `related:` |
| `References`/`Workflows`/`Subagents`/`BestPractices` | counts of `references/*.md`, `workflows/*/SKILL.md`, `subagents`, `best-practices/*.md` |
| `Source`/`Scripts` | whether a `src/` dir exists, number of files in `scripts/` |
| `MCP` | SKILL.md mentions MCP/`mcp_config`, or `src/` is an MCP package |
| `Website` | SKILL.md mentions website/viewer/vite, or `src/` is a web app |
| `Lines` | SKILL.md line count |

### 3. Triage Findings

> Goal: handle the warnings found

1. `[WARN]` per skill: `no SKILL.md`, `name!=dir`, `no description`, `desc >100 chars`, `no frontmatter`, `>250 lines`
2. severity: Critical = `no SKILL.md`/`no frontmatter`; High = `name!=dir`; Warning = `no description`/`desc >100 chars`/`>250 lines`
3. findings that need fixing → `/update-devin-global-skills`; deep lint → `/review-devin-global-harness`; per-skill validation → `/deep-validate`

## Rules

### 1. Read-Only

- The CLI touches no files — it only reads structure

### 2. Reproducible

- Results must come from the script, not the naked eye — rows/WARNs can always be cited in the report

### 3. Single Command

- One entry point only — options via flags, no subcommands

- Use /check-my-global-cli if needed
- Use /use-scripts if needed
- Use /report if needed

## Expected Outcome

- bullet-list structure of every skill (or one skill) via a single command
- findings with severity and the correct next-action skill
