---
name: repo-browser-automation-safety
description: Applies safety controls to browser automation. Use when an agent may click, type, submit forms, navigate authenticated sessions, grant permissions, capture screenshots, read storage, or run browser-debugging commands.
---


# Browser Automation Safety

Use this skill before browser automation or DevTools actions that can expose data or mutate state.

## Risky Actions

- clicking destructive controls
- submitting forms
- changing settings
- triggering payments, emails, notifications, deploys, or webhooks
- reading cookies, local storage, session storage, IndexedDB, or auth headers
- opening production or admin pages
- enabling remote debugging ports
- granting browser permissions
- taking screenshots of private pages
- running automation on authenticated real accounts

## Required Behavior

1. Explain what the browser tool can access.
2. Prefer local, staging, or demo data.
3. Use isolated profiles when possible.
4. Ask before destructive or authenticated actions.
5. Redact sensitive evidence.
6. Avoid non-loopback remote debugging.
7. Close or disable debugging sessions when done.

## Workflow

Use `workflows/safe-browser-automation-workflow.md`.

## Scripts

This skill owns:

```text
scripts/guard-browser-debug-command.py
```

The root-level `hooks.json` calls this script.

