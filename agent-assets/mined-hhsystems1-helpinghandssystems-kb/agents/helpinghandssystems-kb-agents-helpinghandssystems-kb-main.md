# OpenClaw Agent Operating Instructions (Repo-Level)

## Purpose
This repository is the company knowledge base for Helping Hands Systems. It is optimized for OpenClaw ingestion and for agents to retrieve accurate, current operational context.

## Startup Behavior (Always)
1. Read these files first:
   - `MEMORY.md`
   - `IDENTITY.md`
   - `SOUL.md`
   - `TOOLS.md`
   - `USER.md`
2. Then read the most relevant domain files based on the request:
   - Company: `company/*.md`
   - Divisions: `divisions/*.md`
   - SOPs: `sops/*.md`
   - Marketing: `marketing/*.md`
   - Automation: `automation/*.md`
   - Products: `products/*.md`
   - Vision: `vision/*.md`
   - Role prompts: `agents/*.md`

## Current State vs Vision (Do Not Mix)
- **Current Operations / Current State** sections describe what is live and true today.
- **Vision / Direction / Planned Architecture** sections describe future-state intent.
- If you cannot find a clear label, treat the content as **unverified** and ask Stephen for confirmation before acting on it.

## Knowledge Base Usage Rules
- Prefer answering with information directly supported by files in this repo.
- When uncertain, quote the exact file + section header you used (briefly) and ask a clarifying question.
- Avoid guessing about:
  - tools in use
  - integration status
  - customer volume / metrics
  - legal/finance specifics
  - geographic/service coverage

## Response Discipline (High-Signal)
- Summarize the relevant sources in 3-7 bullets before giving recommendations or decisions.
- Separate:
  - facts from repo (current state)
  - proposals (direction / plan)
  - assumptions (explicitly labeled)

## Updating the Knowledge Base
- Prefer small, surgical edits.
- Do not overwrite durable context in `MEMORY.md` casually:
  - update only when a durable truth changes (team, mission, stack direction)
  - leave tactical details in domain files instead
- When you add future-state content, label it clearly as **Vision**, **Direction**, or **Planned Architecture**.

## Prohibited / Legacy Tool Mentions
- Do not introduce references to legacy/deprecated tooling unless a file explicitly marks it as **Legacy/Deprecated**.
- If you encounter legacy tooling in the wild, document it in `automation/` under an explicitly **Legacy/Deprecated** heading.
