---
name: context-engineering
description: Manage AI agent context effectively — what to include, what to exclude, compression strategies, and context hierarchy for optimal performance.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: meta
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global]
priority: high
dependencies:
  mcp: []
  skills: []
  apis: []
  data: []
update_sources:
  - url: "https://www.augmentcode.com/guides/how-to-build-agents-md"
    check_frequency: "quarterly"
    last_checked: "2026-04-17"
license: MIT
---

# Context Engineering

Based on ETH Zurich research: overly detailed instructions reduce task success by 3%, increase token cost by 20%, and add 2-4 reasoning steps.

## When to Use

- Writing SKILL.md, AGENTS.md, or system prompts
- Debugging poor agent performance
- Optimizing token costs
- Designing multi-agent workflows
- Reducing context window pressure

## Context Hierarchy (5 Levels)

Most persistent → most transient:

| Level | Content | Persistence | Example |
|-------|---------|-------------|---------|
| 1. Rules | Project-wide standards | Always loaded | CLAUDE.md, AGENTS.md |
| 2. Spec | Feature/session scope | Per feature | PRD, architecture docs |
| 3. Source | Per task | Per task | Relevant source files |
| 4. Errors | Per iteration | Per attempt | Test failures, stack traces |
| 5. History | Accumulates | Session | Conversation history |

**Principle**: Levels 1-2 are curated (high leverage). Levels 3-5 are per-call (keep minimal).

## What to Include

Include ONLY what the agent cannot discover independently:
- Non-obvious conventions ("we use snake_case for DB columns")
- Project-specific constraints ("never modify the auth module")
- Architectural decisions not in code ("we chose Drizzle over Prisma because...")
- External dependencies not discoverable ("deploy via internal CI, not GitHub Actions")

## What NOT to Include

The agent can discover these itself — including them wastes tokens:
- Tech stack (visible in package.json / requirements.txt)
- File structure (visible via ls / find)
- Key files (visible via search)
- Build commands (visible in scripts / Makefile)
- Standard patterns (the model already knows React, Express, etc.)

## Sizing Guidelines

| Context Type | Max Size | Rationale |
|-------------|----------|-----------|
| AGENTS.md | 500-1000 tokens | ETH Zurich: more = worse |
| SKILL.md (core) | 1000-2500 tokens | Balance detail vs overhead |
| references/ per skill | 500-1000 tokens | Support data, not duplicate |
| System prompt total | < 5K tokens | Beyond this: diminishing returns |

## Compression Strategies

1. **Remove examples when the pattern is clear** — one example > three redundant ones
2. **Use tables over prose** — 50% fewer tokens for structured info
3. **Remove "obvious" instructions** — "write clean code" is noise
4. **Use references for static data** — move schemas/checklists to files
5. **Lazy-load context** — only load what's needed for current task

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| "Always be thorough" | Forces effort=high, +35% tokens | Remove — model handles this |
| "Think step by step" | Redundant with adaptive thinking | Remove on modern models |
| Repeating the same rule 3x | Token waste, no benefit | State once, clearly |
| Including full API docs | Context overflow | Link to docs, summarize key parts |
| "You are a helpful assistant" | Generic, no value | Use specific task context |

## What This Skill Does NOT Do

- Does not manage conversation memory (different problem)
- Does not optimize the model itself (skill ≠ fine-tuning)
- Does not handle multi-agent coordination (orchestration concern)
