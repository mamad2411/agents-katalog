---
name: research-docs
description: |
  Perform validated research, choose lookup tools, and generate accurate project documentation.
  Use when researching current technical facts, comparing approaches, choosing search/fetch tools, or creating/updating docs from source behavior.
---
# Research Docs

This is a router skill. Classify the request, choose one lane, then read only the lane reference needed for the current task. Compose lanes only when the user request genuinely crosses responsibilities.

## Intent Routing

| Intent | Load | Use When |
|---|---|---|
| Validated technical research | `research.md` | Read when current docs, repos, or best practices are required. |
| Antigravity research capability | `research-capability.md` | Read when using the Antigravity research protocol. |
| Documentation generation | `documentation-generator.md` | Read when creating README, API docs, ADRs, or runbooks. |
| Tool selection | `tool-selection-router.md` | Read when selecting search/fetch/scrape/documentation tools. |

## Loading Protocol

1. Match the user request to the narrowest intent above.
2. Read `references/<lane>.md` for that intent before executing specialized steps.
3. Load scripts or assets from this skill only after the selected reference calls for them.
4. Keep outputs concise and state which lane was used when that matters for handoff or auditability.

## Consolidated Names

Former installable skills now routed here: `research`, `research-capability`, `documentation-generator`, `tool-selection-router`.

Related routers: `archive-manager`, `architect`.
