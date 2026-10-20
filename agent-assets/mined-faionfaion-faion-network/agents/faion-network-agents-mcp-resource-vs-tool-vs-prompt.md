# Mcp Resource Vs Tool Vs Prompt

## Summary

**One-sentence:** Classifies every MCP capability as Tool/Resource/Prompt via the three-question test and emits a primitive-classification spec.

**One-paragraph:** The #1 MCP design bug is exposing a Resource as a Tool (LLM calls it unnecessarily and burns tokens) or a Tool as a Prompt (user can't side-effect properly). This methodology runs every capability through the three-question test (Does it side-effect? Is the user calling it directly? Does the model need to reason about its result?) and emits a classification table.

**Ефективно для:** solopreneur building an MCP server who wants the LLM to actually pick the right capability.

## Applies If (ALL must hold)

- Building or refactoring an MCP server.
- Server exposes ≥1 capability that's currently a Tool (the default).
- Selection-accuracy or token cost matters.
- User-facing slash commands exist (or could).
- Read-only content (docs, configs) is part of the surface.

## Skip If (ANY kills it)

- Server has exactly 1 obvious tool — no classification needed.
- Pure write surface — only Tools make sense.
- Pure data dump — only Resources.
- MCP server is throwaway scaffold.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| `capability-inventory.yaml` | capabilities (name, intent, side_effect, user_facing, llm_reasons_on_result) | author |
| `Existing MCP server (or scaffold)` | code | repo |
| `Slash-command surface design` | if any | docs |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|---|---|
| [[mcp-transport-stdio-vs-http]] | Different transports gate which primitives are practical. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | Rules r1-r11 for the three-question test and each primitive, plus the three tree-branch rules (r-advanced, r-default-high, r-default-low) fixing Prompt+Tool, Tool, and Resource/Prompt outcomes. | ~2000 |
| `content/02-output-contract.xml` | essential | primitive-classification spec schema + examples. | ~800 |
| `content/03-failure-modes.xml` | essential | Resource as Tool, Tool as Prompt, Prompt with side-effect. | ~700 |
| `content/04-procedure.xml` | recommended | 5-step classification procedure. | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree | ~700 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Profile parsing | haiku | Mechanical. |
| Decision drafting | sonnet | Tradeoffs require sound reasoning. |
| Code/config emission | sonnet | Mechanical but must compile. |
| Failure-mode cross-check | opus | Catches subtle gaps. |

## Templates

| File | Purpose |
|---|---|
| `templates/capability-inventory.yaml` | Input. |
| `templates/classification-spec.md.j2` | Output. |
| `templates/classification-spec.md` | Output. Generated from `templates/classification-spec.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/server.py` | Working MCP server scaffold with all 3 primitives. |
| `templates/_smoke-test.yaml` | Minimum. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-mcp-resource-vs-tool-vs-prompt.py` | Validates output against the JSON schema. | Pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[mcp-gateway-composition]]
- [[mcp-transport-stdio-vs-http]]

## Decision tree

Lives at `content/06-decision-tree.xml`. Branches on side_effect (true → Tool), then on user_facing+!side_effect (true → Prompt; false → Resource). Each leaf cites a rule id in 01-core-rules.xml so the agent always cites which rule drove the choice — and can be replayed for audit.
