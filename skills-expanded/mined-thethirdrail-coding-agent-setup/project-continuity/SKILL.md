---
name: project-continuity
description: |
  Handle onboarding, daily startup, handoff, and explicit teaching/documentation support.
  Use when joining or returning to a project, creating handoff notes, running a morning routine, or when the user explicitly asks to learn or be taught.
---
# Project Continuity

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| New codebase onboarding | `onboard.md` | Read when joining, inheriting, or learning an unfamiliar repository. |
| End-of-session handoff | `handoff.md` | Read when preparing transition notes or stopping work. |
| Daily startup | `morning.md` | Read when returning to a project or starting a work day. |
| Teaching mode | `tutor.md` | Read only when the user explicitly asks for learning, explanation, or teaching. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `onboard`, `handoff`, `morning`, `tutor`.

Related routers: `archive-manager`, `research-docs`.
