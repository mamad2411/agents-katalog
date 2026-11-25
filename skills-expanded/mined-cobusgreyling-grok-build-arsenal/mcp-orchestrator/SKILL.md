---
name: mcp-orchestrator
description: |
  Discover available MCP servers, evaluate their fit, install and configure them safely,
  and then use them effectively within sessions. Use when the user needs new capabilities
  (browser control, advanced git, observability, etc.) or when existing MCPs are under-utilized.
  Triggers: "set up MCPs", "install the right tools", "add an MCP for...", "what MCPs do we need?"
version: 1.0.0
author: Cobus Greyling
---

# MCP Orchestrator

MCP (Model Context Protocol) is one of grok-build-0.1's strongest advantages. This skill makes it first-class.

## Responsibilities

1. **Inventory current state**
   - Run `grok inspect` (or equivalent) to see loaded MCPs.
   - List project and user-level MCP configuration.

2. **Identify the gap**
   - What real capability is missing for the current task?
   - Examples: visual QA, deep git history analysis, session introspection, architecture visualization, external service access.

3. **Evaluate and recommend specific MCP servers**
   - Prefer narrowly-scoped, well-documented servers over kitchen-sink ones.
   - Check security model, maintenance, and fit for agent use.
   - From this arsenal: recommend `agent-session-analyzer`, `repo-graph`, `test-intelligence`, `browser-qa`, `skill-validator` when appropriate.

4. **Guide installation and configuration**
   - Provide exact commands or config snippets.
   - Handle trust prompts and `.grok/config.toml` or project MCP files.
   - Create or update skills that know how to drive the new MCP.

5. **Integrate into workflow**
   - After installation, immediately demonstrate value with a small example.
   - Update relevant skills or the current plan to use the new capability.
   - Document in the project (README, AGENTS.md, or showcase notes).

## Safety Rules

- Never install untrusted or overly broad MCP servers without explicit review.
- MCP servers that can execute arbitrary code or access secrets must be treated like hooks — require trust and clear documentation.
- Prefer read-heavy MCPs for investigation phases.

## Recommended Arsenal MCPs

- `agent-session-analyzer` — for meta work on agent behavior
- `repo-graph` — architecture understanding at scale
- `test-intelligence` — surgical testing
- `browser-qa` — when building or changing UIs
- `skill-validator` — when extending the skill system itself

## Success Criteria
- The right MCPs are installed and discoverable via `grok inspect`.
- There is at least one concrete, working example of the agent using the new MCP in the session.
- Any new skill or documentation needed to make the MCP usable long-term has been created or updated.
