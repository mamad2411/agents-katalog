---
name: serena-jetbrains-workflow
description: Use Serena MCP with the JetBrains language backend as the default interface for symbol-sensitive coding work, including semantic exploration, declaration and reference lookup, diagnostics, editing, refactoring, debugger interaction, readiness checks, degraded-mode fallback, and end-to-end integration diagnosis. Use in coding projects when Serena and a JetBrains IDE are available, when a request names Serena or JetBrains semantic tools, or when diagnosing Codex-to-Serena-to-JetBrains connectivity.
---

# Serena JetBrains Workflow

## Purpose and boundary

Use JetBrains-backed Serena tools as the primary interface for code-aware work.
Keep the IDE project root and Serena project root identical.

This skill owns only the Serena operating workflow. It owns no product domain,
authorization policy, persistent data invariant, or repository architecture
rule. Follow the user's request and the repository's authoritative guidance for
those concerns.

The Codex client owns the stdio MCP subprocess lifecycle. Serena owns the MCP
tool interface. The Serena JetBrains plugin owns IDE indexing, symbol,
reference, inspection, refactoring, and debugger capabilities. Do not recreate
any of those responsibilities in scripts or adapters.

## Start the task

1. Define the objective, success criteria, constraints, invariants, confirmed
   facts, assumptions, unknowns, and required verification.
2. For a coding-project task, enter the readiness sequence before repository
   work. Skip it only for prose, configuration, generated content, or another
   task where symbol identity cannot affect the result.
3. Activate the coding-project root with `activate_project`, unless the current
   configuration already proves that exact root is active.
4. Call `initial_instructions` unless the current task already loaded the Serena
   instructions.
5. Call `get_current_config` and confirm the active project, JetBrains backend,
   context, modes, and required tool availability.
6. Confirm that the same root is open and indexed in the JetBrains IDE.
7. Run one small, relevant `jet_brains_*` read against a file that exists in the
   active project. Configuration, a tool listing, an open port, or a ready log
   line is not a semantic smoke test.
8. Classify the integration before relying on it:
   - `READY`: the real JetBrains semantic call completed successfully;
   - `DEGRADED`: MCP/configuration works but the semantic call failed;
   - `UNAVAILABLE`: Serena MCP cannot be initialized or queried.

In `DEGRADED` or `UNAVAILABLE` state, report the exact failed boundary and use
the narrowest available text or file fallback. Do not repeatedly retry the same
failing operation or imply that JetBrains semantics verified the result.

Do not manually daemonize Serena or start a second server for the same task.

## Explore and modify semantically

- Use JetBrains declarations, symbols, references, implementations, type
  hierarchies, inspections, and refactorings for symbol-sensitive questions.
- Search narrowly: known symbol, known path, direct references or
  implementations, then wider semantic search.
- Read only the declarations and bodies required for the current decision.
- Use text or file tools for prose, configuration, generated content, or a
  question the semantic backend cannot answer.
- Confirm symbol ownership, usages, and impact before editing.
- Prefer JetBrains-aware rename, move, inline, safe delete, and other
  reference-sensitive refactorings.
- Preserve unrelated work and make the smallest required change.

## Verify changes

1. Check semantic diagnostics.
2. Check reference and usage integrity.
3. Review the actual diff.
4. Run the smallest discriminating test.
5. Expand verification only when the scope or initial result requires it.

## Finish the task

Before completing a turn that used Serena semantics or changed repository
files:

1. Record the final Serena integration state as `READY`, `DEGRADED`, or
   `UNAVAILABLE`, based on a real call made in the current task.
2. Review semantic/reference integrity when the change affected symbol identity.
3. Review the actual diff and the repository's smallest discriminating check.
4. Decide whether the work produced a durable-memory candidate.
5. Write or edit Serena memory only when the fact is verified, stable,
   non-obvious, project-specific, and likely to avoid expensive rediscovery.
6. Do not write quick-read facts, transient task status, raw diagnostics,
   line-level implementation details, secrets, or guesses.
7. If memory changed, run `serena memories check` and report its result.

The lifecycle hook may request this completion pass once. Use the hook input's
stop-active guard to avoid a continuation loop. The hook does not authorize a
memory write and does not replace this semantic decision.

Report only paths verified in the current task. Do not infer a passing state
from earlier sessions, cached plugin state, an open port, or a running process.

## Diagnose the integration

Verify each layer separately:

1. Resolve the installed `serena` command and confirm a fresh CLI invocation
   can start.
2. Confirm the configured backend is `JetBrains`.
3. Confirm the JetBrains plugin is running with the matching project open and
   indexing ready.
4. Confirm the MCP client lists Serena tools.
5. Confirm `activate_project` and `get_current_config` complete.
6. Confirm one `jet_brains_*` tool completes against the active project.

If a layer fails, report that exact boundary. A live server from an existing
task does not prove that a new task can start a fresh server.

## Preserve runtime and security invariants

- The language backend is fixed when Serena starts. Restart the MCP server to
  change it.
- Use one shared monorepo root or separate server sessions for different roots.
- Keep the JetBrains plugin bound to loopback unless a remote topology is
  explicitly required and its security impact is accepted.
- Keep Windows Application Control enabled. Repair or reinstall Serena through
  an approved Python distribution when its uv-managed runtime is unavailable.
- Keep this local Codex workflow on stdio. Do not expose Streamable HTTP merely
  to avoid client-owned subprocess management.

## Official references

- [Running Serena](https://oraios.github.io/serena/02-usage/020_running.html)
- [The Serena JetBrains Plugin](https://oraios.github.io/serena/02-usage/025_jetbrains_plugin.html)
- [Connecting Your MCP Client](https://oraios.github.io/serena/02-usage/030_clients.html)
