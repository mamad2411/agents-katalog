---
name: tailwindcss-skills-upgrade
description: Maintains this tailwindcss-skills repository when Tailwind CSS releases, docs, APIs, utilities, plugins, or migration guidance change. Use this skill when the user asks to upgrade, update, refresh, audit, or sync the Tailwind CSS skills, references, examples, README files, plugin metadata, or agent instructions for a new Tailwind CSS version or changed official Tailwind documentation.
---

# Tailwind CSS Skills Upgrade

## Overview

Use this skill to update the local `tailwindcss-skills` repository after Tailwind CSS changes. The goal is to keep the published skills factual, PixiJS-style, CSS-first, and free of development-only artifacts.

Before editing for any non-trivial upgrade, read [references/upgrade-checklist.md](references/upgrade-checklist.md).

## Quick Start

1. Identify the requested Tailwind version or release window. If the user did not name one, verify the latest official version before editing.
2. Use official sources only: Tailwind docs, Tailwind blog, Tailwind Labs GitHub source, and npm package metadata.
3. Build an impact map before edits: affected skills, references, examples, README files, plugin metadata, and agent instructions.
4. Edit only the affected surfaces. Preserve the existing PixiJS-style skill format: quick start, related skills, core patterns, common mistakes with severity labels, and official references.
5. Run validation and repository hygiene checks before reporting completion.

## Source Of Truth

Prefer sources in this order:

- `https://tailwindcss.com/docs`
- `https://tailwindcss.com/blog`
- `https://github.com/tailwindlabs/tailwindcss.com`
- `npm view tailwindcss version` and related first-party package metadata
- Local `upstream/tailwindcss.com`, only as ignored scratch reference when it exists

Do not rely on memory for release facts, browser requirements, Node requirements, plugin support, new utilities, renamed docs pages, or migration guidance. Tailwind version facts are time-sensitive.

## Upgrade Workflow

### 1. Classify Risk

- Patch release: check factual corrections, link validity, examples, and changed docs copy.
- Minor release: check new utilities, directives, functions, variants, plugins, browser/Node requirements, docs navigation, and release notes.
- Major release: re-audit every shared rule, migration skill, compatibility skill, examples, and README claim.

Escalate risk when the change touches CSS-first configuration, package split, source detection, variants, theme namespaces, compatibility requirements, or migration behavior.

### 2. Map Affected Files

Use the release notes and docs diff to decide which files need edits. Common hotspots:

- `skills/tailwindcss-installation/SKILL.md`
- `skills/tailwindcss-functions-directives/SKILL.md`
- `skills/tailwindcss-theme/SKILL.md`
- `skills/tailwindcss-colors/SKILL.md`
- `skills/tailwindcss-source-detection/SKILL.md`
- `skills/tailwindcss-compatibility/SKILL.md`
- `skills/tailwindcss-upgrade-v4/SKILL.md`
- `skills/tailwindcss/references/index.md`
- `README.md` and `README.zh-CN.md`
- `.github/`, `.claude-plugin/`, and `.cursor-plugin/` metadata
- `examples/vanilla/` when generated CSS or setup commands change

If a new concept deserves a new skill, add `skills/<skill-name>/SKILL.md`, then update both README skill tables, the README structure section, and `skills/tailwindcss/references/index.md`.

### 3. Edit Rules

- Keep published files independent of local checkouts. Never require `upstream/` or absolute local paths.
- Keep `upstream/` ignored and treat it as scratch-only evidence.
- Prefer Tailwind CSS v4+ CSS-first patterns unless the task explicitly targets v3 or a migration path.
- Do not introduce `tailwind.config.js`, `content`, `purge`, or `@tailwind base/components/utilities` as defaults.
- Include exact version attribution when a claim depends on a release note.
- Keep examples executable and small.
- Move dense utility tables into `references/` instead of bloating `SKILL.md`.

### 4. Verification

Run the local hygiene check:

```bash
python3 .codex/skills/tailwindcss-skills-upgrade/scripts/check_tailwindcss_skills_repo.py .
```

Validate skill folders with the Agent Skills validator when available:

```bash
validator="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"
for skill in skills/*; do
  [ -d "$skill" ] && python3 "$validator" "$skill"
done
```

Also verify:

- `rg -n "TODO|\\[TODO|upstream/tailwindcss\\.com|upstream/pixijs-skills|/Users/" README.md README.zh-CN.md AGENTS.md .github .claude-plugin .cursor-plugin skills examples`
- All official links or docs slugs touched by the change.
- The vanilla example still compiles with the current first-party Tailwind CLI when package guidance changes.
- README skill tables still match the directories under `skills/`.

## Reporting

In the final answer, state:

- The Tailwind version or docs date used as source of truth.
- The files changed.
- The official sources checked.
- The verification commands run and their results.
- Any remaining unverified Tailwind facts, blocked runtime checks, or intentionally deferred updates.
