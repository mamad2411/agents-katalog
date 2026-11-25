---
name: openclaw-operator
description: Use this skill when working inside an OpenClaw installation, workspace, or source tree to set up or modify skills, cron jobs, channels, providers, files, or integrations. Inspect the current state first, use official OpenClaw docs and CLI commands when available, make the smallest safe change, and validate the result before finishing.
---

# OpenClaw Operator

Use this skill when the task is about **setting up, modifying, debugging, or validating an OpenClaw installation or repo**.

## What this skill is for

Use this skill when the user wants to:

- install or repair OpenClaw
- configure providers or models
- connect or troubleshoot channels and integrations
- create or update custom skills
- set up cron jobs or scheduled automations
- edit OpenClaw config or workspace files
- diagnose why an OpenClaw setup is not working

Do **not** use this skill for unrelated application code unless the task clearly touches OpenClaw.

## Default operating loop

Always follow this sequence:

1. **Inspect before editing.**
   - Identify whether you are in an OpenClaw source repo, an installed workspace, or both.
   - Locate the relevant files before changing anything.
   - Prefer reading existing config and project docs before proposing edits.

2. **Confirm the current state.**
   When the `openclaw` CLI is available, start with the smallest commands that reveal health and scope:
   - `openclaw status`
   - `openclaw gateway status`
   - `openclaw skills list --eligible`
   - `openclaw channels status --probe`
   - `openclaw doctor`
   - `openclaw docs <topic>`

3. **Make the smallest reversible change.**
   - Prefer targeted edits over broad rewrites.
   - Preserve the user’s structure, naming, and existing conventions.
   - Do not replace a whole config file when a narrow edit is enough.
   - Avoid changing multiple subsystems at once unless the task requires it.

4. **Prefer native OpenClaw mechanisms.**
   - Prefer first-class OpenClaw tools and documented config patterns over ad hoc scripts.
   - Prefer a proper skill folder over burying large instructions in random markdown files.
   - Prefer official CLI diagnostics over guessing.

5. **Validate before finishing.**
   After changes, run the most relevant validation steps and summarize the result.
   Common checks:
   - `openclaw status`
   - `openclaw gateway status`
   - `openclaw skills check`
   - `openclaw channels status --probe`
   - `openclaw doctor`

## Discovery checklist

Before making edits, determine all of the following when possible:

- current working directory and repo root
- whether `openclaw` CLI is installed and on `PATH`
- whether this is a source checkout, a local install, or both
- where the active workspace is located
- whether the relevant skill/config already exists
- whether the task affects runtime config, repo files, or user-level files

## Task playbooks

### 1) Creating or updating a custom OpenClaw skill

- Look for an existing skill folder first.
- If none exists, create a focused skill with a clear `name` and `description` in YAML frontmatter.
- Keep `SKILL.md` concise and action-oriented.
- Put long examples, checklists, or reference material in supporting files under `references/`.
- Make sure the skill describes **when** it should be used, not just what it contains.
- After creating or editing the skill, validate with:
  - `openclaw skills list`
  - `openclaw skills info <skill-name>`
  - `openclaw skills check`

### 2) Setting up cron or scheduled work

- First determine whether the task belongs in OpenClaw-native scheduling or an external system scheduler.
- Prefer the documented OpenClaw approach when the automation is part of the assistant’s runtime behavior.
- Keep schedules explicit, named, and easy to audit.
- Store any job definitions close to the workspace or config they depend on.
- Validate that the job is discoverable and that the referenced skill/script/config exists.

### 3) Configuring channels or integrations

- Start by inspecting health before reconnecting or rewriting auth.
- Prefer incremental fixes to the exact channel or integration being modified.
- Never print or hard-code secrets into committed files.
- If auth or connectivity is involved, re-run health/status commands after the change.
- If the issue is ambiguous, use `openclaw docs <topic>` and existing repo docs before inventing a fix.

### 4) Configuring providers or models

- Inspect the existing provider/model config before changing it.
- Keep names and config keys aligned with what is already present in the repo or workspace.
- Avoid unnecessary provider churn.
- Validate with `openclaw status` and `openclaw doctor` after edits.

### 5) Troubleshooting a broken setup

Use this order unless there is a better local project-specific runbook:

1. `openclaw status`
2. `openclaw status --all`
3. `openclaw gateway probe`
4. `openclaw gateway status`
5. `openclaw doctor`
6. `openclaw channels status --probe`
7. `openclaw logs --follow`

When troubleshooting:
- capture the smallest set of evidence needed
- identify the failing layer: config, gateway, channel, skill, provider, or OS/service
- explain the probable root cause before making a large change
- prefer repair over reinstall unless reinstall is clearly simpler and safer

## Safety rules

- Treat all third-party skills, scripts, shell one-liners, and copied snippets as untrusted until reviewed.
- Never ask the user to run opaque remote shell commands unless the task explicitly requires an official installer.
- Never expose tokens, API keys, cookies, QR codes, or credentials in output files.
- Do not silently disable safety controls to “make it work.”
- When changing config, preserve backups or show a diff when practical.

## Output expectations

When you finish a task, report back in this structure:

1. **What I found**
2. **What I changed**
3. **How I validated it**
4. **Any follow-up risks or next steps**

## Notes for coding agents

- Prefer repository-local guidance over generic habits.
- If `AGENTS.md` or `CLAUDE.md` says to use this skill, read this file before planning edits.
- If the CLI is unavailable, fall back to the repo’s docs, scripts, config files, and workspace layout.
- If OpenClaw commands differ from expectations, trust the installed version and local docs over memory.
- Keep momentum high: make best-effort progress without unnecessary back-and-forth.
