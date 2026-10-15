---
name: computer-doctor
description: Audit a computer as a working environment across security, performance, startup behavior, installed software, storage, updates, and developer tools after asking the user to choose Audit mode or YOLO mode.
---

# Computer Doctor

Use this when the user wants a broad machine audit.

## First Step: Pick A Mode

At the start of the interaction, ask the user to choose one mode:

Ask exactly:
`Choose a mode: Audit mode (recommended) or YOLO mode.`

- `Audit mode` (recommended): inspect first, report findings, ask before changing anything
- `YOLO mode`: still try to be safe, but carry out actions without asking again after the initial mode choice

If the user already picked a mode earlier in the same task, do not ask again.

## What It Covers

This is the top-level command for checking the computer as a whole working environment:

- security posture
- startup and background activity
- performance bottlenecks
- storage pressure
- software quality
- developer tooling health
- update posture and outdated tools

## When To Use

- full machine check
- setup review
- general performance and security review
- broad audit before cleanup or optimization decisions

## Rules

- Detect the environment first: OS, shell, permissions, runtime boundaries, and available tools
- In Audit mode, default to read-first behavior and ask before changing things
- In YOLO mode, proceed without repeated approval, but still avoid reckless actions
- Prefer direct evidence over guesses
- Clearly separate confirmed issues from suspicion
- Prioritize the few highest-impact issues before listing cleanup-grade findings
- Avoid bloating the report with low-value observations when larger risks or bottlenecks dominate

## Workflow

1. Detect environment and limits.
2. Inspect the machine broadly using `references/audit-checklist.md`.
3. Apply `references/safety-boundaries.md`.
4. Read the relevant platform notes:
   - Windows: `references/windows.md`
   - macOS: `references/macos.md`
   - Linux: `references/linux.md`
5. Report findings using `references/report-template.md`.

## Output

Report:

1. executive summary
2. highest-impact findings
3. security findings
4. performance findings
5. startup and background findings
6. software and developer environment findings
7. prioritized action plan
8. limitations

## Companion Commands

Use the narrower commands when the user wants a focused pass:

- `$security-scan`
- `$devtools-audit`
- `$update-audit`

## Read Next

- `references/audit-checklist.md`
- `references/safety-boundaries.md`
- `references/report-template.md`
- `references/windows.md`
- `references/macos.md`
- `references/linux.md`
