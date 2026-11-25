---
name: mcp-chaining
description: Research-to-implement pipeline chaining 5 MCP tools with graceful degradation. Grok-native with Production Contract, hooks, compound.
keywords: [mcp, chaining, research, implement, graceful-degradation, pipeline]
---

# MCP Chaining — Grok Edition

Research-to-implement pipeline that chains up to 5 MCP tools (web search, fetch, code analysis, etc.) with automatic fallback and graceful degradation when a tool is unavailable or slow.

## When to Use
- Complex research + code tasks that require multiple external sources/tools.
- When a single tool call is insufficient (e.g. " find the API fetch docs generate client write tests\).
- Brownfield migration or unfamiliar tech where you need to discover + implement in one flow.

## Grok Integration (Production Contract — Mandatory)
- Ledger: record each step in the chain as attempt (success/fail + tokens + time).
- Handoff: after each successful chain step, emit structured handoff to next agent or the implementer.
- Preflight: before long chains, check available MCP servers + token budget.
- Friction: on repeated tool failures or slow paths → compound learns better routing or caching.
- Claim-verif: two-pass on every fact pulled from external (fetch the page or run the code).
- Hooks: on_mcp_step_complete, on_bounded_loop_end (for chain success rate), on_pre_compact (persist partial chain state in palace).
- Spawn discipline: use worktree isolation for any code-gen sub-steps in the chain.

## Pipeline Stages (Typical 5-tool chain)
1. Discovery (search or repo-research-analyst)
2. Fetch / Extract (web_fetch or harvest or firecrawl)
3. Analysis (tldr or code-knowledge-graph or ast)
4. Synthesis / Plan (architect or prd-writer)
5. Implement + Verify (implement or test-enforcement + verifier)

Graceful degradation: if a tool times out or is unavailable → skip or use fallback skill (e.g. no web → use local docs + tldr on cached).

## Output Contract
Always return:
- Chain steps executed (with success/fail + why)
- Key artifacts (links, code snippets, decisions)
- Token/time summary
- Next recommended action or handoff

## References
- mcp-registry, mcp-scripts
- research-external, firecrawl-scrape, web_fetch
- layered-recall (store intermediate facts)
- preflight (budget check before chain)
- compound-learnings (learn good chains from past successes)

This turns \do research and implement\ into a reliable, observable, self-improving pipeline.
