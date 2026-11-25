---
name: clay-gtm
description: "Use when the user wants Clay GTM work from an agent: company/people search, enrichment waterfalls, tables, or workflows. Not for product code or n8n (use an n8n workflow)."
user-invocable: true
---

# Clay GTM (on demand)

This file is the router. Do not fetch a GitHub plugin pack.

Original Clay procedures (same steps and output as the Clay plugin) already live on disk when this machine has used Clay before:

`${HOME}/.claude/plugins/cache/clay-plugins/clay/<version>/skills/<name>/SKILL.md`

Read **that** `SKILL.md` for the job and follow it. Do not rewrite Clay's workflow from memory. If that cache folder is missing, stop and say the original Clay pack is not on this machine — do not `/plugin marketplace add` another owner's repo.

Never store a Clay token, `mcp_token`, or JWT in a file. Sign-in is `clay login` (OS/CLI only) after a fresh go.

On Windows the official CLI is **macOS/Linux only**. `clay login` needs WSL or another Unix host. Do not paste a token into a file as a workaround.

## Once signed in — pick the cached skill

| Job | Read this cached skill |
|---|---|
| Find people/companies | `searches` |
| Workspace people/companies | `audiences` |
| Enrichment / tables | `tables-analyze`, `tables-cli`, `update` |
| Automations | `workflows`, `workflows-claygent`, `routines` |
| Sequences | `campaigns`, `campaigns-sequence-writing` |
| Credits / CLI | `credits-quotas-plans`, `cli`, `setup` |

Spend and CRM writes wait for the user's go.

GTM automation stays separate from product engineering.
