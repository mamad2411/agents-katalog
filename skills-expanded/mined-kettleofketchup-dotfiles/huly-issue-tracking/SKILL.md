---
name: huly-issue-tracking
description: >-
  Track bugs and issues for a software project with the huly CLI. Use when logging a bug, filing an issue, or organizing work by area of the codebase. Records issues in a single Huly project and groups them with components.
metadata:
  managed_by: "huly-cli"
  huly_cli_version: "v0.4.0"
  content_hash: "sha256:7c75885c689298418582d2b996e422baedb1740a7a049a1d6e37218b8f105089"
---

# Tracking issues and bugs with huly

Use the `huly` CLI to record bugs and issues for this repository in Huly, and
group them by area of the codebase using **components**.

## One project per repository

Track everything for this repository in a single Huly project. Find it once:

```sh
huly project list
```

Pass the project to every command with `--project <identifier>`, or set
`defaults.project` in config once and omit the flag thereafter.

## Group the codebase with components

A **component** is a named area of the codebase (for example `cli`, `api`,
`docs`). Create one per area you want to track separately, then file issues
against it.

```sh
huly component list --project <id>
huly component create --project <id> --label "cli" --description "Command-line interface"
```

## File a bug or issue

Set `--component` so the issue is grouped, and a `--priority` of
`NoPriority`, `Urgent`, `High`, `Medium`, or `Low`.

```sh
huly issue create --project <id> \
  --title "Login fails on empty OTP" \
  --description "Steps to reproduce ..." \
  --component "cli" \
  --priority High
```

Inspect and progress issues:

```sh
huly issue list --project <id>
huly issue view <ISSUE-ID>
huly issue update <ISSUE-ID> --status "In Progress"
```

## Workflow

1. Confirm the project with `huly project list`.
2. Ensure a component exists for the area: `huly component list`, otherwise
   `huly component create`.
3. Create the issue with `huly issue create`, setting `--component` and a
   sensible `--priority`.
4. Track with `huly issue list` / `huly issue view` and change state with
   `huly issue update`.
