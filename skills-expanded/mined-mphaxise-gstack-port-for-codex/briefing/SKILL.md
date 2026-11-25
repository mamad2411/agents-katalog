---
name: briefing
description: GBrain-inspired daily briefing for Codex. Use when the user wants a daily brief, a morning context bundle, or a concise picture of what matters today.
---

# Briefing

Use this skill when the user wants a daily briefing, morning prep summary, or an integrated view of meetings, active threads, and near-term priorities.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain assumes a brain repo with searchable people, company, and timeline pages. In Codex, the closest equivalents are:

- Google Calendar context
- Gmail or other connector context
- repo-local notes or task files
- explicit source citations and coverage-gap notes

## Workflow

1. Load today's meetings and time blocks from available calendar context.
2. Load active threads, tasks, or notes from the best available source.
3. Surface:
   - meetings today and why they matter
   - open threads and deadlines
   - people or projects in play
   - recent changes relevant to today
4. Cite the source of each concrete claim when possible.
5. Flag missing context explicitly instead of inventing it.

## Current Upstream Coverage

Load brain context before meetings, email replies, and daily briefings; backlink newly surfaced people, organizations, decisions, and open threads; and cite the brain or external source behind each material claim.

## Guardrails

- Do not pretend unavailable connector or file data exists.
- Keep the briefing read-only unless the user explicitly asks to save it.
- Prefer a short, decision-useful briefing over exhaustive dumping.
