# MCP Tool Description Economy

**Confidence:** Medium (validated by independent full-sweep trim application)  
**Source:** Holden audit 2026-06-11, helix.mcp reference pattern

## Pattern

MCP tool `[Description]` attributes are **always-loaded context** — every agent pays this cost upfront even if it only uses 1–3 tools. Parameter descriptions are only loaded when the agent is *considering* a tool.

### What belongs in tool descriptions
- **Purpose verb** — lead with what the tool does ("List...", "Get...", "Check...")
- **Brief routing signal** — 1 phrase max ("Niche — only works for X", "Does NOT return Y — use Z")
- **Tool cross-references** — when two tools are commonly confused ("For batch checks, use X instead")
- **Target: 10–16 words / 1–2 sentences**

### What does NOT belong in tool descriptions
- **Parameter names or behaviors** — "staleOnly filters to stale subscriptions" → move to the `staleOnly` param `[Description]`
- **Return-value schemas** — "Shows forward flow, backflow statuses, active PRs, and build staleness" → agent discovers this from output
- **Implementation details** — "resolving aka.ms redirect URLs and checking Last-Modified header" → irrelevant for tool selection
- **Domain knowledge** — "for stale backflow PR remediation" → belongs in knowledge tool or SKILL.md
- **Default value explanations** — "Defaults to a 3-day window and skips expensive build-time metrics" → param description

### Growth vector to watch
Feature PRs that add parameters (filters, output modes) naturally expand tool descriptions. The anti-pattern is: "I added `compact` param, so I explain what compact does in the description." Instead: put the explanation on the param's `[Description]` and leave the tool description alone.

## Checklist for PR review
- [ ] Tool description ≤16 words?
- [ ] Leads with a verb?
- [ ] No parameter names mentioned in description?
- [ ] No return-value shape described?
- [ ] No implementation details?
- [ ] Cross-refs only for commonly confused tool pairs?

## Reference
- helix.mcp trimmed 17 descriptions from ~60 → ~20 words average, removing ~550 words of always-loaded context
- maestro.mcp March P0 cleanup was effective but growth crept back in PRs #22–#24
