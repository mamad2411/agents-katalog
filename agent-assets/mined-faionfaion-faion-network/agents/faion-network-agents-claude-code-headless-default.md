# Claude Code Headless As Default Agent Runtime

## Summary

**One-sentence:** For coding / devops / research tasks the first implementation is `claude -p` headless invocation — not a custom Agent SDK loop. The CLI already ships filesystem, bash, git, MCP, plan mode, sub-agents, hooks, compaction; drop down to the SDK only on documented switch-triggers.

**One-paragraph:** Teams reflexively reach for the Claude Agent SDK to build an autonomous agent and re-implement what the CLI already gives them — and ship a fragile version. This methodology produces a per-task decision record: default to `claude -p` with `--allowedTools`, `--max-turns`, `--output-format stream-json --verbose`; allow custom SDK loop ONLY on one of four switch-triggers (non-coding domain, custom tools beyond MCP, programmatic inner-loop control, SaaS embed that cannot shell out).

**Ефективно для:** Команд, які за тиждень намагаються повторити Claude Code SDK і отримують гірший продукт; одна сторінка decision record економить тиждень розробки і дає більш надійний agent.

## Applies If (ALL must hold)

- Task is coding, devops, research, or content authoring on a machine with shell.
- Claude Code CLI is installable (Anthropic API credentials available).
- The orchestrator can parse stream-json events.
- Task is not embedded inside a SaaS product that cannot shell out.
- A named eng owner can review the decision record.

## Skip If (ANY kills it)

- Task is non-coding domain with no shell affinity (pure structured-output extraction at scale).
- Custom tools required beyond MCP coverage.
- Inner-loop programmatic control needed (e.g. step-by-step state in a graph).
- SaaS product cannot shell out (regulatory / sandbox constraint).

## Prerequisites

| Artifact | Format | Source |
|---|---|---|
| Task brief | natural language | Operator |
| Tool requirements list | inventory | Tech lead |
| Allowed-tools policy | enum list | Sec/Ops |
| Iteration budget | int (max_turns) | Tech lead |
| Named owner | handle | Eng |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/headless-cli-four-guards/AGENTS.md` | Four CLI guards (-p, --allowedTools, --max-turns, stream-json). |
| `geek/ai/ai-agents/stream-json-orchestration/AGENTS.md` | Event-by-event orchestration pattern. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Background (why the CLI harness is the default, docs links) + 3 rules: CLI default, four guards, the four switch-triggers | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for the CLI-vs-SDK decision record | ~700 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (SDK-first, one-shot stdout parsing, wildcard tools, no turn cap) | ~650 |
| `content/04-procedure.xml` | medium | 5-step procedure | ~900 |
| `content/05-examples.xml` | recommended | Decision quickcheck (good/bad) and canonical `claude -p` argv vs unbounded invocation | ~550 |
| `content/06-decision-tree.xml` | essential | Tree: coding-ish? → tools fit MCP? → shell ok? → CLI/SDK | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `classify_task_for_cli_fit` | haiku | Mechanical. |
| `compose_decision_record` | sonnet | Per-instance. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the decision record. |
| `templates/output.example.json` | Filled example. |
| `templates/run-headless.sh` | Shell wrapper showing the canonical argv. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Validate the decision record. | Before kickoff. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `geek/ai/ai-agents/`
- peer: [[headless-cli-four-guards]], [[stream-json-orchestration]].

## Decision tree

See `content/06-decision-tree.xml`. Asks: (1) is the task coding/devops/research with shell affinity? (2) do tool requirements fit MCP catalogue? (3) is shell-out permitted? (4) is inner-loop control required? Leaves point to "use claude-code-headless" or "drop to SDK with named trigger".
