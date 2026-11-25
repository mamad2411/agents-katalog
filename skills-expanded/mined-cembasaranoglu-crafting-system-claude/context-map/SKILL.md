---
name: context-map
description: Maps instructions and knowledge into CLAUDE.md, skills, plugin files,
  subagents, MCP, hooks, prompt cache, or per-request context. Use when organizing
  Claude context.
---

# Context Map

Map context for: `$ARGUMENTS`

## Instructions

Classify each instruction or knowledge item by:

- volatility
- sensitivity
- length
- invocation frequency
- scope
- whether it is a fact, procedure, tool, external data source, or enforcement rule

Choose one location:

- `CLAUDE.md`
- skill
- plugin
- subagent
- MCP
- hook
- prompt cache
- per-request input
- external state file

## Output

```yaml
context_map:
 items:
 - item: ""
 type: "fact | procedure | tool | external_source | enforcement | example"
 recommended_location: "CLAUDE.md | skill | plugin | subagent | mcp | hook | prompt_cache | request_input | external_state"
 rationale: ""
 risk: "low | medium | high | critical"
 migrations: []
 duplication_to_remove: []
 cost_notes: []
```
