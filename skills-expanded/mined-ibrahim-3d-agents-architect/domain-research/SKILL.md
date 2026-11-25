---
name: domain-research
description: Research a domain end-to-end before scaffolding an agentic system for it. Use when the user asks to "research [domain]", "learn about [field]", "what are the best practices for X", "survey the tools for Y", "what MCPs exist for Z", "before we build the agent, understand [topic]", or when kicking off a new /agents-architect:new for an unfamiliar domain. Covers methodology: taxonomy → tools → MCPs → idioms → anti-patterns → eval cases. Produces DOMAIN.md.
---

# Domain Research

Before you build an agentic system for a domain, you research the domain the way a senior practitioner would brief a new hire. Output: a single `DOMAIN.md` that later agents consume.

## Research layers

1. **Taxonomy**: core concepts, sub-fields, canonical workflows. (e.g., 3D modeling → modeling / UV / rigging / animation / shading / lighting / rendering / post.)
2. **Tools**: the 5-10 dominant programs, libraries, APIs. Note open-source vs. commercial, CLI vs. GUI, scriptable vs. not.
3. **MCPs / programmatic interfaces**: what's already exposed via MCP? What's scriptable via SDK? What requires GUI automation?
4. **Idioms & conventions**: how do practitioners name things, structure projects, version files, share work? (e.g., Blender → `bpy` API, collections, linked libraries.)
5. **Best practices**: top 10 rules practitioners would cite unprompted. Sourced from docs, style guides, community consensus.
6. **Anti-patterns**: top 10 ways novices and AI go wrong. Common failure modes.
7. **Eval seeds**: 10 concrete tasks that an agent in this domain should ace, and 10 harder ones it should survive.

## Research methodology

- **WebSearch** for current-year docs, "best practices <domain>", "[tool] Python API", "anti-patterns in <domain>".
- **WebFetch** the official docs, top 3 community style guides, one textbook if available.
- **MCP registry search** (`search_mcp_registry`) for each major tool.
- **arxiv / scholar** (if connected) for recent methodology papers.
- Cross-check sources: a practice is only "consensus" if it appears in 3+ independent sources.

## DOMAIN.md structure

```markdown
# Domain: <name>

## One-line definition

## Taxonomy
- Concept A — what it is, when it matters.
- ...

## Dominant tools
| Tool | License | Interface | Notes |
|---|---|---|---|

## Available MCPs
| MCP | Registry ID | Capabilities | Auth |
|---|---|---|---|

## Idioms
- Naming: ...
- Project layout: ...
- File versioning: ...

## Best practices (prioritized)
1. ...

## Anti-patterns
1. ...

## Eval seeds
### Core (must pass)
1. ...

### Stretch
1. ...

## Sources
- [Doc title](url)
- ...
```

## Scope discipline

- Time-box: 15-20 min of research per pass. Go deeper only when the user specifies a narrow sub-domain.
- Breadth before depth: taxonomy + tool list first. Drill into the top 2-3 tools only.
- Cite sources. Every best-practice bullet has a source link.

## Output

Produce `DOMAIN.md` in the architect session's working directory. Return a 10-line summary to the orchestrator: scope, top 3 tools, recommended MCPs, top 3 anti-patterns to encode as red-lines, eval seed count.
