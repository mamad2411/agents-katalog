---
name: dual-mode
description: Dual-mode orchestration for Claude Code + Codex hybrid workflows with parallel headless workers
version: 1.0.0
tags: [dual-mode, codex, parallel, headless, orchestration]
triggers: [/dual-spawn, /dual-coordinate, /dual-collect]
---

# Dual-Mode Orchestration Skill

Orchestrate hybrid workflows using Claude Code for interactive reasoning and headless Codex workers for parallel background execution.

## Sub-Skills

| Command | File | Purpose |
|---------|------|---------|
| `/dual-spawn` | dual-spawn.md | Spawn headless Codex workers for parallel execution |
| `/dual-coordinate` | dual-coordinate.md | Coordinate hybrid Claude+Codex workflows |
| `/dual-collect` | dual-collect.md | Collect and aggregate results from headless workers |

## When to Use

- Tasks that benefit from parallel execution (multi-file implementation, bulk testing)
- Feature development requiring both design (interactive) and implementation (parallel)
- Documentation sprints across multiple modules
- Any task where spawning background `claude -p` workers speeds up delivery

## Architecture

```
Claude Code (Interactive)          Codex Workers (Headless)
+-------------------+             +------------------+
| Design & Planning |  -- spawn ->| Worker 1 (coder) |
| Quality Review    |             | Worker 2 (tester)|
| Final Integration |  <- collect-| Worker 3 (docs)  |
+-------------------+             +------------------+
        |                                  |
        +--- Shared Memory (claude-flow) --+
```

## Workflow Phases

1. **Route** -- Analyze task, determine platform split
2. **Design** -- Interactive reasoning in Claude Code (architecture, planning)
3. **Execute** -- Spawn headless Codex workers for parallel implementation
4. **Collect** -- Gather results from shared memory
5. **Review** -- Interactive quality review in Claude Code

## Quick Start

```bash
# Spawn 3 parallel implementation workers
/dual-spawn "Implement user authentication" --workers 3 --type coder

# Run a full hybrid workflow
/dual-coordinate --workflow hybrid_development --task "Build user API"

# Collect results from all workers
/dual-collect --format detailed
```

## Available Workflows

| Workflow | Description |
|----------|-------------|
| `hybrid_development` | Design interactively, implement in parallel, review interactively |
| `parallel_feature` | Spawn multiple workers for parallel implementation |
| `design_and_execute` | Interactive design phase, then batch execution |

## Worker Types

| Type | Platform | Use Case |
|------|----------|----------|
| `coder` | Codex | Implementation, code generation |
| `tester` | Codex | Test writing, coverage |
| `docs` | Codex | Documentation generation |
| `reviewer` | Claude | Code review, security analysis |

## Memory Coordination

All workers share state via claude-flow memory:

```bash
# Store context for workers
npx claude-flow@v3alpha memory store --namespace results --key "design" --value "..."

# Search worker results
npx claude-flow@v3alpha memory search --namespace results --query "authentication"

# List all results
npx claude-flow@v3alpha memory list --namespace results
```

## Related Agents

- `dual-orchestrator` -- Hybrid workflow orchestration
- `codex-coordinator` -- Parallel worker coordination
- `codex-worker` -- Headless execution worker
