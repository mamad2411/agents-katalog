---
name: context-engineering-collection
description: A Microsoft-native adaptation of context engineering skills for production agent systems. Use when building, optimizing, evaluating, governing, publishing, or debugging agent systems with core context-engineering mechanisms plus Azure AI and Microsoft Foundry implementation defaults.
---

# Agent Skills for Context Engineering

This collection provides structured guidance for building production-grade AI agent systems through effective context engineering, with Azure AI and Microsoft Foundry defaults included in the standard distribution.

## When to Activate

Activate these skills when:
- Building new agent systems from scratch
- Optimizing existing agent performance
- Debugging context-related failures
- Designing multi-agent architectures
- Creating or evaluating tools for agents
- Implementing memory and persistence layers
- Designing autonomous research or evaluation harnesses
- Binding agent systems to Microsoft Foundry, Azure AI Search, Fabric, Entra identity, Responsible AI controls, and Azure memory/state

## Skill Map

### Foundational Context Engineering

**Understanding Context Fundamentals**
Context is not just prompt text—it is the complete state available to the language model at inference time, including system instructions, tool definitions, retrieved documents, message history, and tool outputs. Effective context engineering means understanding what information truly matters for the task at hand and curating that information for maximum signal-to-noise ratio.

**Recognizing Context Degradation**
Language models exhibit predictable degradation patterns as context grows: the "lost-in-middle" phenomenon where information in the center of context receives less attention; U-shaped attention curves that prioritize beginning and end; context poisoning when errors compound; and context distraction when irrelevant information overwhelms relevant content.

### Architectural Patterns

**Multi-Agent Coordination**
Production multi-agent systems converge on three dominant patterns: supervisor/orchestrator architectures with centralized control, peer-to-peer swarm architectures for flexible handoffs, and hierarchical structures for complex task decomposition. The critical insight is that sub-agents exist primarily to isolate context rather than to simulate organizational roles.

**Memory System Design**
Memory architectures range from simple scratchpads to sophisticated temporal knowledge graphs. Vector RAG provides semantic retrieval but loses relationship information. Knowledge graphs preserve structure but require more engineering investment. The file-system-as-memory pattern enables just-in-time context loading without stuffing context windows.

**Filesystem-Based Context**
The filesystem provides a single interface for storing, retrieving, and updating effectively unlimited context. Key patterns include scratch pads for tool output offloading, plan persistence for long-horizon tasks, sub-agent communication via shared files, and dynamic skill loading. Agents use `ls`, `glob`, `grep`, and `read_file` for targeted context discovery, often outperforming semantic search for structural queries.

**Hosted Agent Infrastructure**
Background coding agents run in remote sandboxed environments rather than on local machines. Key patterns include pre-built environment images refreshed on regular cadence, warm sandbox pools for instant session starts, filesystem snapshots for session persistence, and multiplayer support for collaborative agent sessions. Critical optimizations include allowing file reads before git sync completes (blocking only writes), predictive sandbox warming when users start typing, and self-spawning agents for parallel task execution.

**Tool Design Principles**
Tools are contracts between deterministic systems and non-deterministic agents. Effective tool design follows the consolidation principle (prefer single comprehensive tools over multiple narrow ones), returns contextual information in errors, supports response format options for token efficiency, and uses clear namespacing.

### Operational Excellence

**Context Compression**
When agent sessions exhaust memory, compression becomes mandatory. The correct optimization target is tokens-per-task, not tokens-per-request. Structured summarization with explicit sections for files, decisions, and next steps preserves more useful information than aggressive compression. Artifact trail integrity remains the weakest dimension across all compression methods.

**Context Optimization**
Techniques include compaction (summarizing context near limits), observation masking (replacing verbose tool outputs with references), prefix caching (reusing KV blocks across requests), and strategic context partitioning (splitting work across sub-agents with isolated contexts).

**Latent Briefing (KV Memory Sharing)**
Orchestrator-worker systems can compound tokens when supervisors accumulate long trajectories but workers see only narrow text slices. Latent Briefing compacts the orchestrator trajectory in the worker model's KV cache using task-guided attention (Attention Matching-style compaction) so workers receive relevant latent state without full-text replay when the stack exposes worker KV state and the models are compatible.

**Evaluation Frameworks**
Production agent evaluation requires deterministic checks and multi-dimensional rubrics covering factual accuracy, completeness, tool efficiency, and process quality. Use model judges only after structure, evidence, and rubric math are valid; route judge design, pairwise comparison, and bias mitigation to Advanced Evaluation.

**Harness Engineering**
Reliable autonomous agents need explicit operating loops around the model: locked metrics, editable surfaces, durable logs, novelty checks, rollback rules, and human approval boundaries. Harnesses prevent agents from weakening the evaluator, losing state across compaction, or turning ambiguous goals into unreviewable changes.

### Development Methodology

**Project Development**
Effective LLM project development begins with task-model fit analysis: validating through manual prototyping that a task is well-suited for LLM processing before building automation. Production pipelines follow staged, idempotent architectures (acquire, prepare, process, parse, render) with file system state management for debugging and caching. Structured output design with explicit format specifications enables reliable parsing. Start with minimal architecture and add complexity only when proven necessary.

### Cognitive Architecture

**BDI Mental States**
Belief-desire-intention modeling provides a formal way to translate structured external context into agent mental states. Use it for rational agency, explainability, and systems that need auditable links between beliefs, goals, and chosen actions.

### Microsoft-native Adaptation

**Azure Identity for Agents**
Agent access should be bound to Entra identity, managed identity, RBAC, on-behalf-of flows, tenant boundaries, and per-user authorization instead of broad service-account shortcuts.

**Foundry Hosted Agents**
Microsoft Foundry Hosted Agents provide the preferred managed runtime for production agent endpoints, sandboxing, runtime state, scaling, and operational controls.

**Foundry IQ Knowledge Layer**
Foundry IQ is the default shared enterprise knowledge layer when reusable, permission-aware grounding is needed across multiple agents or applications.

**Foundry Tool Governance**
Foundry Toolbox, tool catalogs, MCP, OpenAPI tools, Azure Functions, and API Management AI Gateway provide the Microsoft-native path for curated, versioned, governed tool surfaces.

**Azure Agentic Retrieval**
Azure AI Search, File Search, SharePoint grounding, knowledge sources, citations, and access-controlled indexes are the default retrieval surfaces for private grounded answers.

**Responsible AI Guardrails**
Microsoft Responsible AI controls cover content filters, Prompt Shields, groundedness, task adherence, red teaming, safety evaluation, and monitoring.

**Agent Publishing**
Publishing guidance covers Foundry versions, stable endpoints, Teams and Microsoft 365 Copilot distribution, Entra Agent Registry, environment promotion, rollout, and rollback.

**Fabric Data Agent**
Fabric Data Agent grounds analytical answers in semantic models, lakehouses, warehouses, and Power BI aligned metrics.

**Azure Memory and State**
Cosmos DB, Blob or ADLS scratchpads, Azure Cache for Redis, session stores, episodic memory, entity state, vector memory, and append-only logs provide Microsoft-native memory and state options.

## Core Concepts

The collection is organized around five themes. First, context fundamentals establish what context is, how attention mechanisms work, and why context quality matters more than quantity. Second, architectural patterns cover the structures and coordination mechanisms that enable effective agent systems. Third, operational excellence addresses optimization, evaluation, and harness reliability. Fourth, development methodology and cognitive architecture cover project execution and formal mental-state modeling. Fifth, Microsoft-native adaptation binds those mechanisms to Foundry, Azure AI, Fabric, Entra, and Azure operational controls.

## Practical Guidance

Each skill can be used independently or in combination. Start with fundamentals to establish context management mental models. Branch into architectural patterns based on system requirements. Reference operational skills when optimizing production systems. For Microsoft-native implementations, pair the relevant core skill with the Azure skill that owns the product binding, security boundary, deployment surface, and operational caveat.

The standard package includes both the mechanism-first core skills and the Microsoft-native Azure skills by default. The core `researcher/` corpus remains platform-agnostic for mechanism provenance; Azure metadata lives under `azure/` so product-specific bindings do not pollute the core mechanism registry.

## Integration

This collection integrates with itself. The fundamentals skill provides context for all other skills. Architectural skills can be combined for complex systems. Operational skills apply to any system built using the foundational and architectural skills. Azure skills should usually be activated with their core counterpart: `tool-design` with `foundry-tool-governance`, `memory-systems` with `foundry-iq-knowledge-layer` or `azure-memory-state`, `context-optimization` with `azure-agentic-retrieval`, `hosted-agents` with `foundry-hosted-agents`, and `harness-engineering` with `agent-publishing` or `responsible-ai-guardrails`.

## References

Core skills in this collection:
- [context-fundamentals](skills/context-fundamentals/SKILL.md)
- [context-degradation](skills/context-degradation/SKILL.md)
- [context-compression](skills/context-compression/SKILL.md)
- [multi-agent-patterns](skills/multi-agent-patterns/SKILL.md)
- [memory-systems](skills/memory-systems/SKILL.md)
- [tool-design](skills/tool-design/SKILL.md)
- [filesystem-context](skills/filesystem-context/SKILL.md)
- [hosted-agents](skills/hosted-agents/SKILL.md)
- [context-optimization](skills/context-optimization/SKILL.md)
- [latent-briefing](skills/latent-briefing/SKILL.md)
- [evaluation](skills/evaluation/SKILL.md)
- [advanced-evaluation](skills/advanced-evaluation/SKILL.md)
- [harness-engineering](skills/harness-engineering/SKILL.md)
- [project-development](skills/project-development/SKILL.md)
- [bdi-mental-states](skills/bdi-mental-states/SKILL.md)

Microsoft-native skills in the default package:
- [azure-identity-for-agents](azure/skills/azure-identity-for-agents/SKILL.md)
- [foundry-hosted-agents](azure/skills/foundry-hosted-agents/SKILL.md)
- [foundry-iq-knowledge-layer](azure/skills/foundry-iq-knowledge-layer/SKILL.md)
- [foundry-tool-governance](azure/skills/foundry-tool-governance/SKILL.md)
- [azure-agentic-retrieval](azure/skills/azure-agentic-retrieval/SKILL.md)
- [responsible-ai-guardrails](azure/skills/responsible-ai-guardrails/SKILL.md)
- [agent-publishing](azure/skills/agent-publishing/SKILL.md)
- [fabric-data-agent](azure/skills/fabric-data-agent/SKILL.md)
- [azure-memory-state](azure/skills/azure-memory-state/SKILL.md)

External resources on context engineering:
- Research on attention mechanisms and context window limitations
- Production experience from leading AI labs on agent system design
- Framework documentation for LangGraph, AutoGen, and CrewAI

Distribution guidance:
- [Azure AI / Microsoft-native distribution](azure/AZURE-DISTRIBUTION.md)

---

## Skill Metadata

**Created**: 2025-12-20
**Last Updated**: 2026-05-24
**Author**: Agent Skills for Context Engineering Contributors
**Version**: 2.4.0
