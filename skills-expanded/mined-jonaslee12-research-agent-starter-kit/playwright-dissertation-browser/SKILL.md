---
name: playwright-dissertation-browser
description: Use when a dissertation or maintenance task needs real-browser automation, browser screenshots, UI verification, Canvas/browser inspection, or web-flow debugging; routes to the global playwright skill and preserves read-only and privacy boundaries.
---

# Playwright Dissertation Browser

Use this project wrapper when browser automation is needed for dissertation or maintenance work.

## Purpose

Connect the global `playwright` skill to the research-agent system safely.

Use it for:

- browser screenshots or UI verification;
- local web app or template preview checks;
- Canvas/module inspection when the user is logged in and asks for read-only browsing;
- checking browser-visible output from generated pages or docs;
- debugging browser flows in a controlled way.

## Workflow

1. Confirm whether the task is read-only or editing.
2. If LMS, university systems, or private sites are involved:
   - do not download, submit, upload, or modify anything unless the user confirms;
   - record source status and access date when useful.
3. Use the global `playwright` skill for CLI workflow details.
4. Prefer screenshots/snapshots over guessing from memory.
5. For LMS/rubric/deadline/word-count claims, still use `university-guidance/RUBRIC_EVIDENCE_GATE.md`.
6. Save only necessary artifacts and avoid storing private screenshots in public/shareable layers.

## Boundaries

- Do not use Playwright to bypass login, permissions, paywalls, or access controls.
- Do not automate form submissions without explicit confirmation.
- Do not save private LMS pages into the GitHub template.
- Do not treat browser-visible summaries as official source text unless exact source text is captured and labelled.

## Output

Report:

```text
Browser check:
- Target:
- Mode: read-only / edit-confirmed
- Tool used:
- Evidence captured:
- Source boundary:
- Files saved:
```

