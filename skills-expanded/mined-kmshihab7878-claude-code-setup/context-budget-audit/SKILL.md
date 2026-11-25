---
name: context-budget-audit
description: >
  Measure and optimize token overhead across agents, skills, MCP servers, and CLAUDE.md.
  Identifies bloated components and produces prioritized savings recommendations.
risk: low
tags: [process, optimization, meta]
created: 2026-03-25
updated: 2026-03-25
---

# Context Budget Audit

Estimates token consumption per component in your Claude Code setup and identifies
optimization targets. Inspired by everything-claude-code's context budget system.

## How to use

- `/context-budget-audit`
  Run a full audit of all agents, skills, MCP servers, hooks, and CLAUDE.md files.

- `/context-budget-audit <component>`
  Audit a specific component (agents, skills, mcp, hooks, claude-md).

## When to use

- Context window feels constrained or sessions compact early
- After adding new agents, skills, or MCP servers
- When troubleshooting slow response times
- Periodic maintenance (monthly recommended)

## When NOT to use

- During active development (audit after changes stabilize)
- For code-level token optimization (use tokenizers directly)

## Token Estimation Rules

| Content Type | Formula | Notes |
|-------------|---------|-------|
| Prose/Markdown | words x 1.3 | CLAUDE.md, SKILL.md, agent descriptions |
| Code blocks | chars / 4 | Python, YAML, JSON in skills |
| MCP tool schema | ~500 tokens/tool | Each declared tool in an MCP server |
| Agent YAML frontmatter | ~100 tokens | Metadata overhead per agent |

## Audit Process

### 1. Scan Components
```
For each category:
  - Read all files matching the pattern
  - Calculate token estimate per file
  - Sum category total
```

### 2. Component Categories

| Category | Path Pattern | Expected Count |
|----------|-------------|----------------|
| Agents | `~/.claude/agents/*.md` | ~61 core |
| Skills | `~/.claude/skills/*/SKILL.md` | ~116 |
| MCP Servers | `~/.claude.json` mcpServers | 21 servers |
| Hooks | `~/.claude/settings.json` hooks | 7 hooks |
| Global CLAUDE.md | `~/.claude/CLAUDE.md` | 1 file |
| Project CLAUDE.md | `<project>/.claude/CLAUDE.md` | Per-project |
| Memory | `~/.claude/projects/*/memory/MEMORY.md` | 1 file |
| Docs | `~/.claude/docs/*.md` | ~15 files |

### 3. Budget Thresholds

| Level | Token Range | Action |
|-------|------------|--------|
| Green | < 50K total | Healthy, no action needed |
| Yellow | 50K-100K | Review largest components |
| Red | > 100K | Active optimization required |

### 4. Key Insights

- Each MCP server with 30+ tools costs ~15,000 tokens in schema alone
- A single verbose SKILL.md can cost more than 10 lean agents combined
- CLAUDE.md files load on EVERY conversation start — keep them lean
- Agent descriptions in REGISTRY.md multiply: loaded once for routing, again per dispatch
- Progressive loading (load skills on demand, not all at once) saves the most

### 5. Report Format

```
## Context Budget Report

### Summary
| Category | Files | Est. Tokens | % of Budget |
|----------|-------|-------------|-------------|
| Agents | 61 | XX,XXX | XX% |
| Skills | 116 | XX,XXX | XX% |
| MCP Schemas | 21 | XX,XXX | XX% |
| CLAUDE.md | 2 | XX,XXX | XX% |
| Memory | 1 | XX,XXX | XX% |
| Docs | 15 | XX,XXX | XX% |
| Hooks | 7 | XX,XXX | XX% |
| **TOTAL** | | **XXX,XXX** | **100%** |

### Top 10 Heaviest Components
[ranked list with file path, token estimate, and savings potential]

### Optimization Recommendations
[prioritized by token savings, easiest first]
```

## Optimization Strategies

| Strategy | Savings | Effort |
|----------|---------|--------|
| Trim verbose SKILL.md preambles | 10-30% per file | Low |
| Use progressive skill loading | 40-60% of skill budget | Medium |
| Consolidate similar agents | 5-15% of agent budget | Medium |
| Reduce MCP server declarations to actually-used ones | 20-50% of MCP budget | Low |
| Move reference docs to on-demand loading | 80-90% of docs budget | Low |
| Compress MEMORY.md (remove stale entries) | Variable | Low |

## Cross-references

- **operating-framework** skill: maintenance cadence for budget reviews
- **prompt-reliability-engine** skill: Mode 8 (Language Pruning) for content trimming
- **setup-audit** skill: broader setup health checks
