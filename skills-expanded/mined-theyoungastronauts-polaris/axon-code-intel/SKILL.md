---
name: axon-code-intel
description: "When and how to use Axon code-intelligence tools (call graphs, impact analysis, dead-code detection, execution-flow tracing) during exploration, implementation, and review. Apply when reasoning about structural impact or navigating an unfamiliar codebase; requires Axon installed."
---

# Skill: Axon Code Intelligence

## Purpose
Guide the use of Axon's MCP tools for structural code analysis during planning, execution, and verification.

## What Axon Provides
Axon indexes codebases into a knowledge graph — call graphs, type references, execution flows, communities, and dead code detection. It answers questions that text search can't: "what breaks if I change this?", "what calls this function?", "is this code reachable?"

## MCP Tools Reference

| Tool | What it does | When to use |
|------|-------------|-------------|
| `axon_query` | Hybrid search (text + semantic + fuzzy) grouped by execution flow | Finding relevant code by concept, not just name |
| `axon_context` | 360° view of a symbol — callers, callees, types, dead code status | Understanding a symbol's full dependency web before modifying it |
| `axon_impact` | Blast radius grouped by depth with confidence scores | Before changing a function/class — see what breaks |
| `axon_dead_code` | All unreachable symbols by file | Cleaning up after refactors, verifying nothing was orphaned |
| `axon_detect_changes` | Maps a git diff to affected symbols and flows | During verification — did the changes touch everything they needed to? |
| `axon_list_repos` | Lists indexed repositories with stats | Checking if a repo is indexed and current |
| `axon_cypher` | Read-only Cypher queries against the knowledge graph | Advanced structural queries not covered by other tools |

## When to Use at Each Stage

### Planning
- `axon_query` to explore the codebase by concept ("authentication", "payment processing")
- `axon_context` on key symbols to understand existing architecture before designing changes
- `axon_impact` to assess risk of proposed changes and inform phase ordering

### Execution
- `axon_context` before modifying any symbol — understand callers, callees, and type dependencies
- `axon_impact` before changing a function's signature or behavior — check the blast radius
- Use impact results to identify tests and call sites that need updating alongside your change

### Verification
- `axon_detect_changes` to map the phase's diff to affected symbols and execution flows
- `axon_dead_code` to check if refactors orphaned any code
- `axon_impact` to verify all affected call sites were updated

### Bug Fixing
- `axon_context` to trace callers and callees around the buggy symbol
- `axon_impact` to understand what a fix might break
- `axon_query` to find related code when the bug's root cause isn't in the obvious location

## Re-indexing

If the MCP server runs with `axon serve --watch`, the index stays current automatically (file-local phases update immediately, global phases batch every 30 seconds). A full re-index is only needed after:
- A large merge or rebase while watch mode was not running
- Switching branches with significant structural changes

To re-index: `axon analyze .` (or `axon analyze --full` to skip incremental logic).

## Checking Availability

Before relying on Axon tools, verify the index exists:
- Run `axon_list_repos` to check if the current repo is indexed
- If not indexed, inform the user and suggest running `axon analyze .`
