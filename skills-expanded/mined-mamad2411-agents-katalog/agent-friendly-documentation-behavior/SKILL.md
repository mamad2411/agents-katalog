---
name: agent-friendly-documentation-behavior
description: Applies the first behavior-grounded study of how coding agents discover, read, and write technical documentation, finding that agents prefer agent-facing artifacts (60.5%) over classical docs (10.6%), documentation consultation is self-initiated not failure-driven, and widely assumed "agent-friendly" properties lack empirical support. Use when designing documentation for agent-driven development, evaluating whether current docs serve agents, or building agent-facing instruction files.
---

# Agent-Friendly Documentation Behavior

## Overview
The first empirical study grounded in actual agent behavior (not assumptions) reveals that coding agents primarily consult agent-facing artifacts, not classical technical documentation, and that two widely assumed "agent-friendly" documentation properties — actionability and verifiability — lack behavioral support.

## When to Use
- Designing documentation for repositories that accept agent-generated PRs
- Creating agent-facing instruction files (AGENTS.md, CLAUDE.md, .cursorrules)
- Evaluating whether existing documentation serves agent workflows
- Building documentation strategies for agent-driven development
- NOT for human-only documentation design
- NOT for API reference optimization

## Core Process / Workflow

### 1. Understand Agent Documentation Preferences

| Documentation Type | Share of Interactions | Agent Behavior |
|-------------------|----------------------|----------------|
| Agent-facing artifacts (instructions, working notes) | 60.5% | Primary source; self-initiated |
| Classical technical documentation | 10.6% | Rarely consulted |
| API references | 1.3% | Almost never consulted |

### 2. Design for the Two-Lobed Cycle
Agent documentation interaction follows a two-lobed cycle, NOT a linear journey:
- **Lobe 1: Code-focused work** — agents write and modify code, with documentation consultation trailing code changes (code touched first 4.7x more often in multi-commit PRs)
- **Lobe 2: Documentation-focused work** — agents create documentation, often unadjusted from existing patterns

### 3. Optimize for Self-Initiated Discovery
- 70.2% of documentation consultation is self-initiated (agent decides to look)
- Only 7.5% is failure-driven (agent looks after an error)
- Implication: documentation must be discoverable through normal exploration, not error recovery
- Place instructions where agents naturally look during code work

### 4. Question "Agent-Friendly" Assumptions
Two widely assumed properties of agent-friendly docs lack behavioral support:
- **Actionability** (docs that tell agents what to do): no consistent behavioral evidence
- **Verifiability** (docs that let agents check their work): no explicit validation sequence observed

What DOES work:
- Instruction files that agents read at session start
- Working notes that accumulate during a task
- Context files positioned where agents explore early

### 5. Documentation-Code Coupling
- Direct link between doc consultation and immediate code editing is WEAK (adjacent transition probability 0.002)
- Documentation consultation is associated with LESS immediate testing (lift 0.23)
- Agents create documentation elevated above baseline (lift 1.67) but adjusted interval includes unity
- Implication: don't expect doc reading to immediately trigger code changes; docs inform later work

## Key Evidence
- Study: Gao & Chen (arXiv:2608.20195, August 2026)
- Datasets: 557 agentic coding sessions from SWE-chat (94,813 events, 3,033 doc interactions) + 33,097 agentic PRs from AIDev (690,260 file-level changes)
- Four findings challenge current documentation practice
- Released pipeline, coding scheme, and event-level data

## Cross-Domain Synthesis
- The 60.5% preference for agent-facing artifacts connects to the SE Agent Building skill's finding that "agents retrieve written, not unsaid" (76% agreement) — agents work with what is explicitly written in instruction files
- The self-initiated discovery pattern connects to the MCP code execution pattern: agents explore filesystems progressively, not through error-driven lookups
- The weak doc-to-code link connects to the SWE-chat dataset finding that most common user intent is understanding existing code (19%), not writing code (13.4%)

## A-Tech Alignment
- Open-source: findings apply to Cline/OpenCode and any MCP-based agent
- Data privacy: behavior-based analysis from public datasets, no content exposure
- Financial freedom: prevents over-investment in documentation that agents don't use
- Practical implementation: clear guidance on what documentation to create for agent-driven repos

## References
- See [references/evidence-base.md](references/evidence-base.md) for full event-level analysis, transition probabilities, stage-adjusted models, and the descriptive two-lobed cycle model.