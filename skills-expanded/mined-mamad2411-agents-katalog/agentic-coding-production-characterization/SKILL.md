---
name: agentic-coding-production-characterization
description: Applies the first production-scale characterization of AI coding-agent workloads (GitHub Copilot, 3.2M users, 13M sessions, 761M LLM calls, 95T tokens, June 2026) to design agent-aware serving infrastructure, workflow-aware scheduling, and archetype-tiered SLOs. Use when planning agentic coding infrastructure, optimizing KV-cache lifecycle for coding agents, designing tiered developer SLOs, sizing capacity for CLI/IDE agent fleets, or benchmarking agent serving systems against real production traces rather than synthetic SWE-bench evaluations.
---

# Agentic Coding Production Characterization

## Overview

The first production-scale empirical study of AI coding-agent workloads reveals that agentic coding is structurally distinct from chatbot LLM serving, requiring session-aware scheduling, KV-cache lifecycle management, and archetype-tiered resource policies. Based on Liu et al. (UIUC/Microsoft Azure Research, arXiv:2608.00101, August 2026), this skill translates production trace findings into actionable infrastructure and DevEx design patterns.

## When to Use

- Designing or optimizing LLM serving infrastructure for coding agents (vLLM, SGLang, LMCache, custom)
- Planning capacity for CLI/IDE agent fleets (GitHub Copilot, Claude Code, Codex, Cursor)
- Building workflow-aware schedulers or cache eviction policies for agentic workloads
- Designing tiered developer SLOs based on user archetypes
- Benchmarking agent serving systems against real production traces
- Estimating inference cost / token budgets for agentic coding products
- NOT for single-turn chatbot or completion workloads — the findings are specific to agentic loops

## Core Process / Workflow

### 1. Characterize the Agentic Workload (Structural Properties)

Use these seven production-validated properties to scope your infrastructure:

| Property | Evidence | Implication |
|---|---|---|
| 1:1 LLM↔Tool coupling | 87% agent-initiated calls; ~1:1 LLM:tool ratio | Treat LLM calls + tool invocations as inter-dependent pairs, not independent requests |
| Session-structured KV cache | 90% cache hit within turn; 55% at turn boundaries | Cache is session-aware, schedulable resource |
| Model switches destroy cache | only 8% cached after switch | Pin sessions to single model; proactive cache staging on target model |
| Context compaction costly | 7.8% of sessions, 44% of tokens; 67% cache drop | Incremental, prefix-preserving compaction strategies |
| Turn boundaries signal idle | 4.1 min container / 2.9 min KV cache cross-turn | Turn boundary = natural reclamation trigger |
| Tool failures amplify cost | 9% of turns → 4× compute via retry loops | Tool reliability + LLM verification = key serving efficiency lever |
| Heterogeneous users | 50× token range across 5 archetypes | Uniform resource policies are suboptimal |

### 2. Apply Workflow-Aware Serving Patterns

**Session-aware scheduling** — schedule at session/turn granularity, not individual request granularity. The 1:1 LLM↔tool coupling means serving systems must model entire agent execution chains.

**KV-cache lifecycle management**:
- Within a turn: retain cache in GPU memory (median KV idle 1.2s — eviction overhead > benefit)
- At turn boundary: deprioritize for offload to DRAM/disk (median 25.2 min user idle)
- After model switch: proactive cache staging on target model before switching
- After compaction: incremental/prefix-preserving compaction to maintain partial continuity

**Idle-time prediction** — train a lightweight (LightGBM, ~2MB) survival-curve predictor on turn-boundary features (session-level features dominate importance). ROC-AUC 0.73 for >60s idle prediction; captures 86–90% of total idle time even as pointwise accuracy decays.

### 3. Implement Archetype-Aware Tiered SLOs

Classify users into archetypes and apply differentiated resource policies:

| Archetype | % Users | Tokens/Turn | Cache Retention | Container Lifecycle |
|---|---|---|---|---|
| Readers | 41.7% | 203K | Aggressive eviction | Cold-start freely |
| Coders | 30.4% | 417K | Medium retention | Checkpoint, don't terminate |
| Terminal users | 11.0% | 213K | Medium retention | Stateful management |
| Deep-loop users | 9.2% | 1.1M | **Highest retention priority** | Never evict within session |
| Chat-only users | 7.6% | 23K | Aggressive eviction | Cold-start freely |

**Key insight**: A single cache miss costs 50× more for Deep-loop users (1.1M token re-prefill) than Chat-only users (23K). Uniform eviction timeout imposes disproportionate latency tax on the most resource-intensive segments.

### 4. Optimize for the Six Workflow Archetypes

Design serving policies around the six recurring turn-level workflow patterns:

| Archetype | % Turns | LLM Calls | Description |
|---|---|---|---|
| Deep-loop read | 30.5% | 9 | Extended code exploration; read-heavy |
| LLM-only | 20.2% | 1 | Pure reasoning; no tools |
| Multi-cycle edit | 19.0% | 5 | Read + edit + build feedback loops |
| Multi-cycle other | 13.2% | 4 | Read-dominant exploration |
| Deep-loop w/failures | 9.1% | 36 | Retry loops; **4× compute amplification** |
| Deep-loop run | 8.1% | 7 | Terminal-heavy execution |

**Failure-driven compute amplification** is unique to agentic workloads: in chat, a failed request returns an error; in an agentic loop, a failure triggers autonomous recovery cascading into dozens of additional LLM calls with growing context windows. Prioritize tool reliability and LLM verification as serving-efficiency levers.

### 5. Capacity Planning with Real Production Metrics

Use these medians (from 13.5M sessions) for sizing:

- Sessions/user/week: median 2, P90 8
- Turns/session: median 3, P90 15
- LLM calls/session: median 15, P90 100.5
- Session duration: median 4.2 min, P90 177.8 min (3 hours)
- Prompt tokens/call: median 68K (68:1 input-to-output ratio)
- Weekend sessions are fewer but longer (more LLM/tool calls per turn)

**Diurnal pattern**: Activity peaks 4–5× baseline during daytime, declines overnight. Medium-length prompts drive most diurnal fluctuation; extremely long prompts stay stable.

## References

- See [references/agentic-coding-production-evidence-base.md](references/agentic-coding-production-evidence-base.md) for full dataset, per-axis statistics, idle-time predictor specification, and serving-system design implications.