---
name: skills-update
description: Update installed Codex skills from known GitHub sources and set up optional daily automatic skill updates. Use when the user wants to check for newer versions of installed skills, update custom or curated skills, configure skill source metadata, or enable or disable recurring skill update automation.
---

# Skills Update

## Purpose

Keep installed Codex skills current without manually reinstalling them. Use the bundled updater script for deterministic checks and updates, then summarize exactly what changed and which skills could not be updated safely.

## First Run

Before the first update, check whether the user has already answered the automation prompt:

```bash
python scripts/update_skills.py --first-run-status
```

If `first_run_required` is `true`, ask exactly:

> Do you want to turn on automatic updates? This will set up an automation that runs every day. You can turn it off at any time in `Automations`.

If the user says yes, create a daily automation named `Update Codex skills` with a prompt equivalent to:

```text
Use $skills-update to check installed Codex skills for updates and apply safe updates. Report updated, current, untracked, and failed skills.
```

Prefer a local daily cron automation at 9:00 AM in the user's locale when the automation tool is available. Then run:

```bash
python scripts/update_skills.py --mark-first-run enabled
```

If the user declines, run:

```bash
python scripts/update_skills.py --mark-first-run declined
```

## Update Workflow

1. Inspect update sources with a dry run:

```bash
python scripts/update_skills.py
```

2. Explain any `untracked` skills. A plain copied custom skill has no reliable upstream unless it has metadata, a config entry, or is installed as a git checkout.

3. Apply updates when the user asked to update or when running from the daily automation:

```bash
python scripts/update_skills.py --apply
```

4. Report the result by category: `updated`, `current`, `update_available`, `untracked`, `source_missing`, and `error`.

5. Tell the user to restart Codex when skills were updated so the refreshed skill metadata is picked up.

## Source Resolution

The updater checks sources in this order:

1. `--source` entries passed to the script.
2. Per-skill metadata at `<skill>/.skills-update.json`.
3. Global config at `$CODEX_HOME/skills/.skills-update/sources.json`.
4. A git remote when the installed skill folder is a git checkout.
5. Inferred OpenAI curated or experimental source paths in `openai/skills`.

Use explicit metadata for custom skills that were installed by copying files:

```json
{
  "repo": "owner/repo",
  "path": "skills/my-skill",
  "ref": "main"
}
```

Use global config when several custom skills are tracked from one place:

```json
{
  "skills": {
    "my-skill": {
      "repo": "owner/repo",
      "path": "skills/my-skill",
      "ref": "main"
    }
  }
}
```

## Safety Rules

- Skip system skills under `.system` unless the user explicitly asks to include them.
- Never guess a custom skill's upstream repository from its name alone.
- Always create a timestamped backup before replacing an installed skill.
- Replace whole skill folders only after validating the remote source contains `SKILL.md`.
- Treat dry-run output as advisory; only `--apply` changes installed skills.
- If an update fails, report the failure and leave the original skill restored when possible.

## Script Reference

Common commands:

```bash
python scripts/update_skills.py
python scripts/update_skills.py --apply
python scripts/update_skills.py --json
python scripts/update_skills.py --only frontend-skill --apply
python scripts/update_skills.py --source "my-skill=owner/repo:skills/my-skill@main" --apply
```

Use `--include-system` only when the user intentionally wants to check bundled system skills.
