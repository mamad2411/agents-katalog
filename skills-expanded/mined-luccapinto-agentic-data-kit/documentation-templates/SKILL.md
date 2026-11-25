---
name: documentation-templates
description: Use when the user asks to document, write docs for, or generate a runbook, data dictionary, metric definition, ADR, or Power BI dashboard catalog for a data project. Provides the team's canonical documentation templates as separate files.
allowed-tools: Read, Glob, Grep, Write
---

# Skill: documentation-templates

The team's canonical documentation formats. The value here is **consistency** — one agreed
structure per doc type — not novel knowledge. Pick the template that matches the request and
open only that file (each lives in `templates/`).

| The user wants to document… | Open |
|---|---|
| A pipeline/job (for 3 AM failures) | `templates/pipeline-runbook.md` |
| A table/model (data dictionary) | `templates/data-dictionary.md` |
| A metric for analysts | `templates/metric-definition.md` |
| An architecture decision | `templates/adr.md` |
| A Power BI dashboard (auto-generated from PBIP) | `templates/powerbi-dashboard.md` |

## Principles
- **Audience first:** an engineer fixing a bug reads differently than a business user.
- **Keep docs close to the code/schema** (YAML, `schema.yml`, repo) — wikis rot fastest.
- Explain the *why* and the edge cases; don't restate what the code already says.
