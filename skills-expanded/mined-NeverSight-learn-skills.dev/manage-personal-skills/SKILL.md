---
name: manage-personal-skills
description: Maintain and publish AtticusZeller's personal agent skills repository. Use when adding, updating, validating, publishing, pulling, or reinstalling personal skills from AtticusZeller/skills; when updating the global external skills manifest; or when preparing a fresh machine to consume these skills with npx skills add.
---

# Manage Personal Skills

## Overview

Use this skill to keep the `AtticusZeller/skills` repository installable, safe, and easy to reuse from fresh machines. The repository contains original personal skills plus a manifest of external global skills; it must not vendor third-party skill source or secrets.

## Repository Shape

Expected layout:

```text
AGENTS.md
README.md
skills/<skill-name>/SKILL.md
manifests/global-skills.json
scripts/install-global-skills.sh
scripts/validate-skills.sh
```

## Workflow

1. Read root `AGENTS.md` before changing the repository.
2. For a new personal skill, create `skills/<skill-name>/SKILL.md` with valid `name` and `description` frontmatter.
3. Put detailed reusable guidance in `references/` and deterministic helpers in `scripts/` inside the skill directory.
4. For third-party skills, update `manifests/global-skills.json`; do not copy their source into this repository.
5. Run validation before committing:

```bash
bash scripts/validate-skills.sh
npx skills add . --list --full-depth
```

6. Publish with `git` and `gh` only after confirming no secrets are staged.

## Safety Rules

- Never commit tokens, PATs, private subscriptions, SSH keys, node credentials, API keys, or machine-private config.
- Never vendor third-party skills; reference them in the manifest.
- Keep root `README.md` human-facing and root `AGENTS.md` agent-facing.
- Keep individual skill folders lean; do not add skill-local README files.
- Keep `npx skills add AtticusZeller/skills --list --full-depth` working.

## Common Commands

List remote skills:

```bash
npx skills add AtticusZeller/skills --list --full-depth
```

Install one personal skill:

```bash
npx skills add AtticusZeller/skills --skill bootstrap-dev-machine -g -y --full-depth
```

Install external global skills from this repo:

```bash
bash scripts/install-global-skills.sh
```

Publish:

```bash
git status --short
git add .
git commit -m "Update personal skills"
git push
```

## Completion Criteria

The repository is healthy when local and remote `npx skills add ... --list --full-depth` both discover the personal skills, validation passes, and the manifest install script can dry-run all external global skills.
