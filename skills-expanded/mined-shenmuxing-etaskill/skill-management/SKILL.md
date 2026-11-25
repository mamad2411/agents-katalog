---
name: skill-management
description: Manage, inventory, standardize, migrate, and test reusable Codex skills for the MetaSkill repository. Use when Codex needs to inspect local skills, convert a personal workflow into a public skill candidate, normalize skill folder shape, plan skill promotion, or decide whether a skill belongs in skill-management, publication-review, or skill-examples.
---

# Skill Management

## Overview

Use this skill to turn useful local skill workflows into public, reusable, and testable skill packages. For publish-before-review privacy and contract checks, use `publication-review/`.

## Workflow

1. Identify the task type.
   - Use `skill-management/` for inventory, audit, standards, tests, migration, and publishing workflows.
   - Use `publication-review/` for final public-safety, structure, and truthful-contract checks before publication.
   - Use `skill-examples/<skill-name>/` for mature reusable skills and public-safe examples.
2. Inspect the candidate skill or workflow.
   - Read `SKILL.md`, `agents/openai.yaml`, and directly referenced resources.
   - Search for private paths, user identifiers, unpublished content, account details, and local-only assumptions.
3. Normalize the public contract.
   - Keep only implemented behavior in the trigger description and body.
   - Mark unsupported behavior as manual, optional, or out of scope.
   - Replace private examples with generic fixtures.
4. Validate structure and metadata.
   - Ensure the folder name is lowercase hyphen-case.
   - Ensure frontmatter follows the system `skill-creator` validator; `name` and `description` are required.
   - Ensure optional resources are actually used.
   - Ensure reusable `skill-examples/` skills include `install.md` with copy,
     dependencies, install, update, verification, rollback, and notes sections.
   - Ensure required companion skills, CLIs, app connectors, and bundled scripts
     are explicit enough for a post-install agent check.
   - Ensure installed path examples resolve from `$CODEX_HOME/skills`, with
     `~/.codex/skills` as the fallback when `CODEX_HOME` is unset.
5. Record the result.
   - Update collection-level documentation when a new category or convention is introduced.
   - Avoid adding per-skill README files unless explicitly required by the repository owner.

## Standard Skill Shape

A public skill should normally look like:

```text
skill-name/
  SKILL.md
  install.md
  agents/openai.yaml
  references/
  scripts/
  assets/
```

Only keep optional directories that serve the skill. Delete scaffold placeholders.

## Validation Commands

When the system skill-creator utilities are available, validate a skill with:

```powershell
uv run --with pyyaml python .\skill-examples\skill-creator\scripts\quick_validate.py .\skill-management
```

If the repository sample is unavailable, use an installed `skill-creator` validator without committing machine-specific absolute paths.

For skill examples, also run the installation smoke checker in source mode:

```powershell
python .\scripts\validate_muxing_install.py --source-only --skill deepseek-agent
```

## Output Expectations

- For audits, report blocking publication issues first.
- For migrations, list changed files and any behavior intentionally omitted.
- For publication-readiness validation, delegate to `publication-review/` and distinguish structural validation from real-world forward testing.
- For public README updates, keep the repository purpose broad and avoid private context.
