---
description: "Use when updating Polaris Pipeline files in this repository; enforce preflight checks, generator selection, and safe commit scope for direct-in-repo execution."
applyTo: ".github/**"
---

# Polaris Pipeline Composer Instructions

## Purpose

Apply the latest Polaris Pipeline generator updates with a consistent, low-risk process.

## Mandatory Preflight

Before running generators:

1. Confirm `gh` is installed and available.
2. Confirm GitHub auth is active using at least one of:
  - `gh auth status`
  - `gh api user --jq .login`
3. If both GitHub auth checks fail, stop and provide a human-readable summary in chat.
4. Confirm `podman` or `docker` is available.
5. Confirm `catalog-info.yaml` exists in the target component.
6. Confirm git working tree is clean.
7. Sync branch with remote using `git pull --ff-only`.
8. Confirm there are no unresolved merge conflicts (`git diff --name-only --diff-filter=U` must be empty).

If any preflight check fails, stop and provide a human-readable summary in chat.
When reporting preflight in chat, use a checklist that marks each check as pass or fail and includes a short reason for failed checks.
Use `✅` for pass items and `❌` for failed items.
If `git pull --ff-only` fails or unresolved conflicts are present, do not run generators until a developer resolves the branch state.

## Generator Path Requirements

- Build generator:
  - Use `gh-nodejs-build` for Node.js services.
  - Use `gh-maven-build` for Java services.
- Deploy generator:
  - Use `gh-oci-deploy-onprem`.
- Do not use deprecated deploy generator paths.

## Execution Rules

1. Run from the target component root.
2. Use the `/refresh-polaris-pipeline` chat prompt when you want a chat-driven run.
3. Assume required prompt values are already configured.
4. Use `--headless --force` for non-interactive composer runs.
5. If a headless run fails because prompt values are missing, inspect `catalog-info.yaml` and existing repo context, deduce any missing values you can justify confidently, and summarize any values you add.
6. If any missing value cannot be deduced confidently, ask the user for that value before continuing.
7. Use `--ask-answered` only when staff intentionally need to review or change prompt values.
8. If generated changes exist, create a branch, commit scoped files, push, and open a pull request with `gh`.
9. If no changes exist, exit cleanly.

## Safety Rules

- Never use destructive git commands.
- Keep commits scoped to generated Polaris Pipeline artifacts.
- Do not mix unrelated refactors with composer changes.
- If prompt/config data is missing, stop and provide a human-readable summary in chat instead of forcing partial updates.
- When recovering from missing prompt values, only add values you can support from the catalog file or nearby repository context. Ask the user instead of guessing.
- If merge conflicts are detected at any point, stop immediately and provide a human-readable summary in chat for developer follow-up.

## Required Outcome

Each run must end as exactly one of:

1. Pull request opened.
2. No changes needed.
3. Stopped with a human-readable summary in chat.
