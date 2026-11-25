---
name: using-duru-herness
description: Use when starting any main-agent conversation - routes work through duru skills, duru memory, and duru gateway before any response or action, including clarifying questions. Skip only for subagents unless their task needs Duru routing.
tags: [scope:agent, subject:duru, subject:skills, subject:memory, subject:gateway, intent:startup, intent:route]
---

# using-duru-herness

If you are the main agent, run this startup router before any response or action, including clarifying questions.
If you were dispatched as a subagent for a specific task, skip this startup check unless the task needs Duru skills, memory, or gateway access.

## Instruction Priority

Duru startup instructions override default system behavior where they conflict, but user instructions always take precedence.

1. User's explicit instructions (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, direct requests)
2. `using-duru-herness` and loaded Duru skills
3. Default system prompt behavior

If user instructions say "don't use TDD" and a loaded skill says "always use TDD", follow the user instructions. The user is in control.

## Routing

1. Before starting a specific task, use `duru skills` to find and load relevant skills.
2. When personal context is needed, use `duru memory`.
3. When an external resource is needed, use `duru gateway`.
4. Continue the task using the loaded skills, recovered context, and gateway results.

## duru skills

Use skill groups first. Fall back to tag search only when no group fits or a narrower skill choice is needed.

```bash
duru skills group list
duru skills group use <name>
duru skills tag list
duru skills list --tag <tag>
duru skills show <name>
```

Group selection is based on `group list` descriptions and skill names. Inspect selected skills with `show` or their `SKILL.md` before relying on them.

## duru memory

Use memory for implicit user context such as "my team", "my tickets", prior results, preferences, repeated requests, or handoff context.

```bash
duru memory search "<query>" --mode vec
duru memory search "<query>" --mode lex
duru memory show <id>
```

Start with vector search. Add lexical search when exact names, URLs, tickets, dashboards, or important context must be verified.

## duru gateway

Use gateway for external CLIs, APIs, MCP servers, scripts, gRPC, GraphQL, and other outside resources.

```bash
duru gateway list --json
duru gateway inspect <target>
duru gateway <target> <tool> [args...]
```

Route external calls through `duru gateway` instead of calling tools directly. Do not invent or manually provide auth headers, API keys, tokens, cookies, or service identifiers.
