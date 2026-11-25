---
name: ouroboros-self-developing-coding-agent
description: Design self-developing agent harnesses where tools, context assembly, prompts, and core implementation improve through reviewed commits. Use when building self-evolving agents, implementing experience-driven core evolution, or designing operational safety for agents that can rewrite their own code and select model APIs.
---

# Ouroboros: Self-Developing Coding Agent with Reviewed Core Evolution

## Overview

Ouroboros is a self-developing agent harness whose tools, context assembly, prompts, and core implementation improve through reviewed commits that become the runtime for later work. Core evolution proceeds in two modes: recursive free evolution (improvement itself is a task) and experience-driven core evolution (ordinary work exposes bugs and inefficiencies leading to structural changes). It achieves state-of-the-art on Terminal-Bench 2.1 (86.97%), OSWorld-Verified (90.69%), and CL-Bench (0.2301), with model-matched parity on SWE-bench Pro and GAIA.

## When to Use

- Building self-evolving or self-improving agent systems
- Implementing experience-driven core evolution from task execution and social feedback
- Designing operational safety for agents that can modify their own code
- Creating persistent, multi-surface agent deployments with memory and identity
- Establishing governance boundaries that remain binding under evolutionary pressure
- NOT for: fixed-harness agents, single-task optimization, or systems without version control

## Core Process / Workflow

### 1. Understand the Two Modes of Core Evolution

**Recursive Free Evolution**
- Improvement itself is a task
- Agent reviews current system, selects and implements a change
- Completion can schedule another evolution cycle
- Produces a continuing sequence of reviewed updates rather than a fixed optimization run

**Experience-Driven Core Evolution**
- Begins with ordinary work (task execution, reflection, review blockers, social feedback)
- Bugs, rough edges, context-assembly failures, inefficient tool paths become candidate improvements
- Agent records durable error classes and proposed repairs
- Decides whether to open maintenance work under the same commit gate
- Accepted fixes pass through the same reviewed commit gate as all other core changes

### 2. Implement the Commit Pipeline

**Three owner-selected runtime modes:**
- **Light**: blocks repository edits
- **Advanced**: permits ordinary edits, protects governance surfaces
- **Pro**: permits protected edits subject to review

**Commit path:**
1. Deterministic preflight (version, data-boundary, size-health checks)
2. Fingerprint the staged diff
3. Collect reviewer evidence
4. Check fingerprint again before commit (invalidates on mid-review mutation)
5. Diff-review panel is blocking in every context mode
6. In max mode: whole-repository scope reviewer evaluates goals, coupling, prompts, functional code
7. Rollback restores earlier reviewed state via separate recovery path

### 3. Design Operational Safety Controls

**Risk: agents that choose their own model APIs**
- Re-routing to new provider/version can increase capability, alter refusal behavior, enlarge prompt-injection surface, change cost by orders of magnitude
- Model routing is an audited configuration change, not ordinary runtime choice
- Owner-selected context mode controls whether whole-repository scope review runs

**Guardrails in use:**
- Constitution loaded through untruncatable path, always in context, cannot be written/deleted wholesale
- Multi-model adversarial review with quorum (sub-quorum cannot produce clean pass)
- Deterministic preflight and diff fingerprinting (before and after review)
- Isolated operator channel and non-bypassable /panic (halts all processes before media handling)
- Pattern register: recurring failures become durable rows (error class, count, root cause, structural fix)

### 4. Task Outcomes and Verification

- Separate axes: execution, objective, review, artifact
- Host-run verification commands create revision-bound receipts
- Finalization preserves latest typed answer
- Distinguishes capability failures from infrastructure errors, timeouts, budget exhaustion, incomplete evidence

### 5. Persistent Identity and Memory

- Versioned constitution (editable identity profile)
- Scratchpad and chronicle projections
- Project memory, review ledgers, Git history
- These artifacts shape observable behavior across sessions and model routes

### 6. Subagents and Patch Integration

- Readonly planning scouts and mutative acting subagents under configurable task tree
- Acting children write in isolated worktrees or admitted external workspaces
- Cannot commit the live system repository
- Parent verifies lineage, patch hashes, protected paths before three-way indexed integration
- Submittable benchmark profiles disable task delegation to preserve pass@1

## Benchmark Results

| Benchmark | Model | Ouroboros | Named Baseline |
|-----------|-------|-----------|----------------|
| Terminal-Bench 2.1 | Opus 5 high | 86.97% raw; 86.74% audited | Claude Code + Fable 5: 83.8% |
| OSWorld-Verified | Opus 5 | 90.69% | Intelligence-Indeed: 90.19% |
| CL-Bench | Sonnet 4.6 | 0.2301 | ICL: 0.1960; Claude Code: 0.1855 |
| SWE-bench Pro | GPT-5.6 Luna | 58.2% | Codex: 59.4% (p=0.40, n.s.) |
| GAIA | Sonnet 5 | 78.2% | Claude Code: 78.8% |

## Hope Deployment (161-day living agent experiment)

- 7 interaction surfaces (web chat, voice, Telegram, Discord, Twitter/X, website comments, email)
- $110.6K model spend, 79.7B tokens, 175,755 LOC, 227 MB memory artifacts
- 1,085 self-modification commits (94.2% agent-authored)
- 1,522 reviewed self-edit attempts; recent review block rate 63.5%
- 40 pattern classes / 659 recurrences
- Social feedback is advisory, not imperative — Hope decides which proposals to pursue

## References

- See [references/evidence-base.md](references/evidence-base.md) for full architecture details, safety controls, and deployment statistics.