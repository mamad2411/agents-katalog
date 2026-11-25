---
name: devin-scripts-toolkit
description: PowerShell scripts for check, review, setup, build, and deploy, reusable across skills and projects
argument-hint: "[scope]"
related:
  - devin-templates-toolkit
  - review-devin-global-harness
  - follow-create-web
  - setup-cicd
  - ship
---

## Goal

Collect reusable PowerShell scripts across the devin skills ecosystem and projects

## Scope

- Skill validation scripts (e.g. `/review-devin-global-harness`, `/review-devin-global-harness`)
- Project health check scripts
- Build/test/run scripts
- Setup/deployment helper scripts (e.g. `/setup-cicd`)
- Use together with `/follow-create-web` to set up a project

## Execute

### 1. Validate Skills

> Goal: check the skills repo

1. Run `scripts/devin-skills-audit.ps1`
2. Run `scripts/check-skills-mentions.ps1 -FilterSkill <skill>`
3. Run `scripts/check-skills-references.ps1`

### 2. Validate Project

> Goal: check the project tech stack, config, and quality

1. Run `scripts/check-techstack.ps1 -ProjectDir <path>`
2. Run `scripts/check-config-files.ps1 -ProjectDir <path>`
3. Run `scripts/check-broken-references.ps1 -ProjectDir <path>`
4. Run `scripts/check-naming-conventions.ps1 -ProjectDir <path>`
5. Run `scripts/check-quality.ps1 -ProjectDir <path>`

### 3. Fix Skill Names

> Goal: fix skill names to match their directories

1. Run `scripts/fix-skill-names.ps1 -WhatIf`
2. If correct, run `scripts/fix-skill-names.ps1`

## Scripts

| Script | Purpose |
|--------|-----------|
| `devin-skills-audit.ps1` | Combined check of frontmatter, references, mentions, line-count |
| `check-skills-frontmatter.ps1` | Check frontmatter |
| `check-skills-references.ps1` | Check related references |
| `check-skills-mentions.ps1` | Check related mentions in content |
| `check-skills-line-count.ps1` | Check SKILL.md <= 250 lines |
| `check-techstack.ps1` | Check package.json/Cargo.toml |
| `check-config-files.ps1` | Check config files |
| `check-broken-references.ps1` | Check broken skill references |
| `check-naming-conventions.ps1` | Check naming |
| `check-quality.ps1` | Run lint, typecheck, build |
| `fix-skill-names.ps1` | Fix names to match directories |
| `list-skills.ps1` | List skills |

## Rules

- Run these scripts before `/ship`
- Use `/devin-templates-toolkit` for templates
- Do not hardcode paths in scripts
- Use `Write-Host` with green for OK, yellow for warning, red for error

## Expected Outcome

- Fast checks for skills and projects
- Less manual review
- Reusable scripts across the ecosystem

