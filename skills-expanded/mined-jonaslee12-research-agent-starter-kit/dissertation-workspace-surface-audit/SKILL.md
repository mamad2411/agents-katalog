---
name: dissertation-workspace-surface-audit
description: Read-only audit of what the dissertation workspace can actually do now, including skills, project memory, Obsidian vault, knowledge base, LMS/browser access, Word/PDF rendering, local tools, connectors, and missing surfaces.
---

# Dissertation Workspace Surface Audit

Use this skill when the user asks what the current dissertation system can do, what is missing, why something feels unsmooth, or whether local tools/skills/knowledge stores are actually available.

## Purpose

Adapt ECC workspace-surface audit to this dissertation workspace. The main rule is: verify live surfaces instead of trusting memory or configuration text.

## Audit Surfaces

Check only what is relevant to the user's question.

### Project Surface

- `AGENTS.md`
- `PROJECT_AGENT_PREFERENCES.md`
- `.agents/skills/`
- `research-wiki/`
- `knowledge-base/`
- `proposal/`
- `ethics/`

### Knowledge Surface

- Obsidian vault path: `<OBSIDIAN_VAULT_PATH>`
- source registers
- LMS reading-list notes
- supervisor or public resource notes
- source-of-record rules

### Tool Surface

- Word/LibreOffice rendering chain
- Poppler/PDF tools
- browser/LMS access state
- installed plugins/connectors visible to the current Codex session
- local scripts or setup notes

### Automation Surface

- Codex automations, if present
- hooks, if present
- MCP configs, if present
- scheduled jobs or monitors, if present

## Workflow

1. Inventory what exists.
2. Mark each item:
   - `available now`
   - `configured but unverified`
   - `missing`
   - `not needed now`
3. Distinguish real capabilities from written intentions.
4. Recommend top 3-5 maintenance moves, ordered by dissertation value.

## Output Format

```text
Current surface:
- ...

Available now:
- ...

Configured but unverified:
- ...

Missing or weak:
- ...

Top next moves:
1. ...
```

## Guardrails

- Do not print secret values.
- Do not install tools or enable integrations during an audit.
- Do not treat a skill file as proof that a tool is live.
- Do not widen the task into a full system rewrite unless the user asks.
