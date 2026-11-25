---
name: skill-enricher
description: Cross-reference an existing skill with its source repository to fill gaps — missing scripts, references, install steps, configuration, examples, or usage patterns. Use when a skill was created from documentation but needs to be enriched with real implementation details. Triggers on "update skill from repo", "enrich skill", "sync skill with source", "fill skill gaps", "improve skill from source".
alwaysAllow:
  - Read
  - Glob
  - Grep
  - Bash
  - Edit
  - Write
---

# Skill Enricher

Cross-reference an existing skill with its source repository to identify and fill gaps in scripts, references, install steps, configuration, and examples.

## Overview

Skills are often created from documentation or high-level understanding. The enricher reads the actual source repo to find concrete details the skill is missing — real CLI commands, configuration files, error handling patterns, edge cases, and working examples.

## When to Use

- After creating a skill with `/skill-creator` that needs real-world grounding
- When a skill's scripts reference commands that need verification against the source
- When a skill is missing install steps, configuration, or environment requirements
- When updating a skill to match a new version of its source project

## Workflow

### Step 1: Read the Skill

Read the target skill's complete contents:

```
Read SKILL.md
Read all files in scripts/
Read all files in references/
Read all files in assets/
```

Build a mental model of:
- What the skill claims to do
- What scripts it provides
- What references it includes
- What gaps or TODOs exist

### Step 2: Explore the Source Repository

Clone or navigate to the source repository. Explore systematically:

```
1. Read README.md, CONTRIBUTING.md, docs/
2. Read package.json / pyproject.toml / Cargo.toml / go.mod
3. Read configuration files (.env.example, config/, etc.)
4. Read the main entry points (src/index.ts, main.py, cmd/, etc.)
5. Read test files for usage patterns
6. Read CI/CD configs (.github/workflows/, Makefile, etc.)
```

### Step 3: Gap Analysis

Compare the skill against the source using the enrichment checklist (`references/enrichment-checklist.md`). For each category, note:

- **Present and correct** — skill already covers this
- **Present but incomplete** — skill mentions it but missing details
- **Missing entirely** — source has it, skill doesn't
- **Outdated** — skill has old information

### Step 4: Generate Diff Report

Before making changes, produce a structured gap report:

```markdown
## Enrichment Report: [skill-name]

### Source: [repo-url or path]

### Gaps Found

#### Scripts
- [ ] Missing: [script that should exist]
- [ ] Incomplete: [script exists but missing X]

#### References
- [ ] Missing: [reference doc that should exist]
- [ ] Outdated: [reference has old info]

#### SKILL.md
- [ ] Missing section: [section name]
- [ ] Incomplete: [section needs more detail]

#### Configuration
- [ ] Missing env vars: [VAR_NAME]
- [ ] Missing config files: [filename]

#### Install/Setup
- [ ] Missing dependency: [package]
- [ ] Missing step: [description]

#### Examples
- [ ] Missing usage example for: [feature]
- [ ] Example uses deprecated API: [detail]
```

### Step 5: Update the Skill

Apply the enrichments:

1. **Update SKILL.md** — Add missing sections, fix incomplete info, add real examples
2. **Add/update scripts** — Create missing scripts or fix existing ones with real commands
3. **Add/update references** — Add documentation from the source that agents need
4. **Add/update assets** — Templates, config examples, boilerplate from the source
5. **Verify** — Ensure all file references in SKILL.md point to real files

### Step 6: Validate

After enrichment, validate the skill:

- All scripts are executable and have correct shebangs
- All file references in SKILL.md resolve to real files
- SKILL.md frontmatter is valid (name, description present)
- No placeholder TODOs remain
- Examples use real commands from the source (not hypothetical)

## Key Enrichment Patterns

### Pattern: CLI Commands

Source repos often have CLI tools. Enrich the skill with:
- Exact command syntax (not paraphrased)
- All flags and options
- Exit codes and error messages
- Environment variables

### Pattern: Configuration

Source repos often have config files. Enrich with:
- Required config file paths
- All config keys with defaults
- Environment variable overrides
- Example configs (add to assets/)

### Pattern: Error Handling

Source repos show real error cases. Enrich with:
- Common error messages and their causes
- Troubleshooting steps
- Recovery procedures

### Pattern: Integration Points

Source repos show how tools connect. Enrich with:
- API endpoints and formats
- Event hooks and callbacks
- File format specifications
- Protocol details

## Anti-Patterns

- **Copy-pasting entire source files** — Extract relevant patterns, don't dump code
- **Guessing commands** — Every command must come from the actual source
- **Ignoring tests** — Test files show real usage patterns and edge cases
- **Skipping validation** — Always verify enrichments against the source
- **Over-enriching** — Add what agents need, not everything that exists

## References

- `references/enrichment-checklist.md` — Category-by-category checklist of what to look for
