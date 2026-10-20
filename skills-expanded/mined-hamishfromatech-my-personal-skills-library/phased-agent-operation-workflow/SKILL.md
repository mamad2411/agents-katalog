---
name: phased-agent-operation-workflow
description: Applies Infobip's four-phase workflow for operating LLM coding agents (CIKM '26 industry paper) — front-load human effort, increase delegation as artifacts mature, apply four context-management strategies per phase to counter known failure modes, and treat upstream research/planning errors as compounding. Use when structuring team workflows around coding agents, designing context-management policy, or training engineers on agent operation discipline.
---

# The Phased Workflow for Operating Coding Agents

## Overview
A production AI research team's workflow for agent-assisted development, published as a CIKM '26 industry paper: structure the work into **four phases where human effort is front-loaded and delegation increases as artifacts mature**. Context management is the central concern, addressed through four strategies applied at each phase. Two observations from practice carry the weight: upstream errors in research and planning compound across later phases, and correcting generated code introduces bloat and fragility — both argue for front-loading human review rather than inspecting at the end.

## When to Use
- Designing a team's standard operating procedure for coding agents
- Diagnosing why agent output quality degrades downstream (upstream compounding)
- Building context-management policy (what enters the window, when)
- Content: "How a production team actually runs coding agents — phase by phase"

**NOT for**: the five-skill curriculum map (use `context-engineering-skills-map-2026`), agent-builder workflow research (use `se-agent-building-practice`), sandbox/containment architecture (use `ai-coding-agents-sandbox-first`).

## Core Process

### 1. The four-phase structure
Human effort concentrates in **Phase 1 (research & planning)** — the phases that precede code. Delegation rises as artifacts mature: plans get agent-reviewed, then agent-executed, then agent-maintained. The design principle is the inverse of "generate and check at the end": review the plan, the architecture, and the constraints *before* tokens are spent generating against them.

### 2. The four context-management strategies (applied at each phase)
The paper's central contribution is treating context management as a per-phase discipline with four named strategies, chosen to counter known failure modes (context overload, stale context, semantic confusion, silent context loss). Operationally: **curate what enters** (task-specific selection over "load everything"), **compress deliberately** (summaries and task notes over raw transcripts), **sequence disclosure** (progressive loading as the task unfolds), and **persist decisions in the repo** (state notes and decision records where both humans and agents can find them). Keep context "short and specific rather than overly complex" — semantic confusion from context overload is a named failure, and the fix is selection, not capacity.

### 3. The two practice observations (why front-load)
1. **Upstream errors compound**: a wrong assumption in research/planning propagates through every downstream phase and multiplies the correction cost. The cheapest defect to fix is the one before generation starts.
2. **Correction bloat**: agent-generated fixes to agent-generated code add layers rather than reorganizing — long functions, if-statement accretion, duplicate utilities, dead code left behind. Post-hoc correction is where fragility enters; front-loaded review is where it's prevented.

### 4. Two open problems (the honest edge)
The authors name them explicitly: **no metrics exist for workflow effectiveness** (is the four-phase split actually reducing rework? nobody can measure yet), and **a gap between formalized context-management components and the workflow-level patterns practitioners need** — the components exist (retrieval, compression, memory), the composition discipline doesn't.

### 5. Deployment checklist (derived from the structure)
- Front-load: human-reviewed plan/spec sign-off before any generation phase.
- Phase-gate delegation: each maturation step (plan → scaffold → implementation → maintenance) widens agent autonomy explicitly, not implicitly.
- Context budget per phase: define what may enter the window at each stage; reject task-agnostic loads.
- Decision records in-repo: state notes, ADRs, and constraints as first-class artifacts (echoes the spec-as-artifact shift).
- Correction policy: prefer regeneration from corrected specs over iterative patching when bloat indicators appear (duplication, dead code, function length growth).

## References
- Pairs with `se-agent-building-practice` (the seven-stage agent-building workflow — building agents vs operating them), `spec-quality-bottleneck-agentic-delivery` (spec quality as the rate-limiter — same front-loading logic), `context-engineering` and `context-engineering-skills-map-2026` (the component layer this composes), `agent-friendly-documentation-behavior` (what artifacts agents actually consume), `committed-ai-configuration-ramp-2026` (the config artifact that gates the whole loop).
- A-Tech alignment: open source (workflow patterns portable to any harness; pairs naturally with open runtimes like the DeepSeek Harness), privacy (context curation IS the data-minimization layer — what you never load, you never leak), financial freedom (fewer correction cycles = fewer tokens; front-loading is a cost-control device), practical (checklist usable as a team SOP on day one).