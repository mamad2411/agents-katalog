---
description: Titan AI — context, approved APIs, no hallucinated app data
alwaysApply: true
---

# Titan AI

Titan AI must understand context, pages, workflows, and user history — then act only through approved APIs.

## Requirements

| Area | Rule |
|---|---|
| Context | Allowlisted `pageContext`: path, title, domain, entityType/id, workflow. Prefer shared `api/_lib/aiContext.js` |
| Pages | System prompt includes a compact page/domain catalog — do not invent screens |
| Workflows | Confirm intents + `ALLOWED_AI_INTENTS` only; Driver/DoorDash state only when wired via snapshots/APIs |
| History | Chat is session-scoped unless a persisted store exists — do not imply long-term memory |
| Actions | Mutations only via `executeAiOfficeAction` / allowlisted intents; confirm before write; JWT + ownership + sanitize |
| Explanations | Short answer + optional bullets + one TitanOS next step |
| Recommendations | Prefer snapshot-grounded next steps; reuse insight helpers where possible |
| No hallucination | Business facts from **server-owned** snapshots only. Never trust client `businessSummary` / `businessData` |
| Provenance | Distinguish **YOUR DATA** (snapshot) vs **GENERAL KNOWLEDGE** vs **UNKNOWN** in prompt and UI (`source`, `dataBasis`) |

## Honesty

- If snapshot is capped (“sample of last N”), say so  
- Do not claim side effects the API does not perform (e.g. `send_invoice` = status sent, not email)  
- Marketplace modes (Law Mastermind): disclaimer required; verify entitlement when possible  

## Definition of done

Incomplete if Titan AI invents customers/jobs/money, mutates outside allowlisted intents, or fails to label user data vs general knowledge.
