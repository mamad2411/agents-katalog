---
name: repo-browser-debugging-session
description: Plans and documents safe browser-debugging sessions. Use when reproducing browser-visible bugs, collecting console/network/DOM/screenshot evidence, or preparing a reproducible browser-debug report.
---


# Repository Browser Debugging Session

Use this skill when a task requires seeing or reproducing behavior in a browser.

## When to Use

Use this skill for:

- browser-only bugs
- visual regressions or broken layouts
- broken forms or interactions
- console errors
- failed network requests
- route/navigation issues
- screenshots or trace evidence
- browser-specific reproduction steps

## Approach

1. Identify the environment and route.
2. Confirm whether authentication is needed.
3. Prefer local or staging URLs.
4. Define safe browser actions before interacting.
5. Collect only necessary evidence.
6. Redact private data.
7. Summarize evidence and confidence before editing code.

## Workflow

Use `workflows/browser-bug-reproduction-workflow.md` for reproducible debugging.

## Resources

Use `resources/browser-debugging-evidence-checklist.md` to structure findings.

## Scripts

This skill owns:

```text
scripts/browser-debug-report-template.py
```

Run scripts with `--help` before manual use.

