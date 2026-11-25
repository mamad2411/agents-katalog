---
name: agent-architecture
description: >-
  Agent design knowledge base for the RESEARCH/DESIGN phase of building AI
  agents — the 21 agentic design patterns from Antonio Gulli's "Agentic Design
  Patterns" (concepts only, code excluded by design; use the
  google-agents-cli-* skills for ADK implementation). Use when deciding WHICH
  patterns an agent needs and their trade-offs: prompt chaining, routing,
  parallelization, reflection, tool use, planning, multi-agent collaboration,
  memory, learning/adaptation, MCP, goal setting, exception handling,
  human-in-the-loop, RAG, A2A inter-agent comms, resource-aware optimization,
  reasoning techniques (CoT/ToT/ReAct/etc.), guardrails/safety, evaluation,
  prioritization, exploration/discovery. Trigger on "which agent pattern",
  "agent architecture", "design an agent", "agentic design pattern", or any
  named pattern above.
---

# Agent Architecture — Agentic Design Patterns

A research/design knowledge base distilled from **"Agentic Design Patterns: A
Hands-On Guide to Building Intelligent Systems"** by Antonio Gulli (Google, OCTO).
It carries the book's *concepts* — what each pattern is, when to reach for it,
trade-offs, pitfalls, and how patterns combine. **Code is intentionally
excluded.** For implementation in Google ADK, switch to the `google-agents-cli-*`
skills (`...adk-code`, `...scaffold`, `...eval`, `...deploy`, `...observability`).

## How to use this skill

1. **Designing an agent?** Scan the pattern tables below, pick the patterns whose
   "Use when" matches your problem.
2. **Need depth on one pattern?** Read `patterns/<nn>-<name>.md` — each is a full
   conceptual chapter (overview, mechanics, use cases, trade-offs, pitfalls,
   relationships, key takeaways, references).
3. **Combining patterns?** Read `conclusion.md` for a worked example weaving 5+
   patterns. Most real agents stack several.
4. **Then implement** with the ADK CLI skills. Treat any model IDs / API details
   in this book as possibly dated — the live skills + docs win on specifics.
5. Unfamiliar term? `glossary.md`.

> Source snapshot: mid-2025. Note: the book's Appendix F (Reasoning Engines) was
> absent from the source PDF and is not included.

---

## Part One — Foundations (the core loop)

| # | Pattern | What it is | Use when |
|---|---------|-----------|----------|
| 1 | [Prompt Chaining](patterns/01-prompt-chaining.md) | Break a task into a sequence of LLM steps, each step's output feeding the next | A single prompt overloads the model — instruction neglect, drift, error propagation |
| 2 | [Routing](patterns/02-routing.md) | Classify the input and dispatch it to the right handler/sub-agent/tool | One of several distinct paths should run depending on the request |
| 3 | [Parallelization](patterns/03-parallelization.md) | Run independent sub-tasks concurrently, then synthesize | Sub-tasks don't depend on each other and latency/throughput matters |
| 4 | [Reflection](patterns/04-reflection.md) | Agent critiques and revises its own output (self- or producer–critic) | Quality/correctness matters more than latency/cost; first drafts are unreliable |
| 5 | [Tool Use](patterns/05-tool-use.md) | Model calls external functions/APIs/services (function calling) | The agent needs live data, side effects, or capabilities beyond text |
| 6 | [Planning](patterns/06-planning.md) | Agent generates a multi-step plan to reach a goal before acting | The "how" must be discovered at runtime, not hard-coded |
| 7 | [Multi-Agent Collaboration](patterns/07-multi-agent.md) | Multiple specialized agents coordinate (supervisor/hierarchical/network/etc.) | A monolithic agent is too complex; roles benefit from separation |

## Part Two — State, Knowledge & Goals

| # | Pattern | What it is | Use when |
|---|---------|-----------|----------|
| 8 | [Memory Management](patterns/08-memory-management.md) | Short-term (context) + long-term (persistent) memory across turns/sessions | The agent must remember within or across interactions |
| 9 | [Learning & Adaptation](patterns/09-learning-and-adaptation.md) | Agent improves over time — in-context, fine-tuning, RL (PPO/DPO), self-modification | Behavior should adapt from experience/feedback, not stay static |
| 10 | [Model Context Protocol (MCP)](patterns/10-model-context-protocol.md) | Open client/server protocol standardizing tool/resource/prompt access | Tools/data must be discoverable & reusable across agents and hosts |
| 11 | [Goal Setting & Monitoring](patterns/11-goal-setting-and-monitoring.md) | Define goals + success criteria, then monitor progress against them | The agent needs explicit objectives and a way to know it's on track |

## Part Three — Robustness & Interaction

| # | Pattern | What it is | Use when |
|---|---------|-----------|----------|
| 12 | [Exception Handling & Recovery](patterns/12-exception-handling-and-recovery.md) | Detect, handle, and recover from errors (retry/fallback/circuit-breaker) | Tools/environments fail and the agent must degrade gracefully |
| 13 | [Human-in-the-Loop](patterns/13-human-in-the-loop.md) | Insert human approval/escalation/correction at key points | Stakes are high, or confidence is low, or oversight is required |
| 14 | [Knowledge Retrieval (RAG)](patterns/14-knowledge-retrieval-rag.md) | Retrieve relevant external knowledge to ground generation | The agent needs facts beyond its training data / must cite sources |

## Part Four — Advanced / Scaling

| # | Pattern | What it is | Use when |
|---|---------|-----------|----------|
| 15 | [Inter-Agent Communication (A2A)](patterns/15-inter-agent-communication-a2a.md) | Open protocol for agents to discover & task each other (Agent Cards, tasks) | Independent agents (possibly across orgs) must interoperate |
| 16 | [Resource-Aware Optimization](patterns/16-resource-aware-optimization.md) | Route work by cost/latency/compute; budget tokens; model fallback | Cost or latency budgets matter; cheap vs. expensive models per task |
| 17 | [Reasoning Techniques](patterns/17-reasoning-techniques.md) | CoT, Tree-of-Thought, Self-Correction, ReAct, debate, inference-time scaling | The task needs deliberate multi-step reasoning, not a single shot |
| 18 | [Guardrails / Safety](patterns/18-guardrails-safety.md) | Layered input/output/behavioral/tool constraints + moderation | Untrusted input, harmful-output risk, prompt injection, policy needs |
| 19 | [Evaluation & Monitoring](patterns/19-evaluation-and-monitoring.md) | Assess responses & trajectories (LLM-as-judge, tool-use metrics), monitor prod | You need to measure quality and watch agents in production |
| 20 | [Prioritization](patterns/20-prioritization.md) | Rank tasks/goals/actions by urgency, importance, dependencies, cost | The agent juggles competing tasks and must choose what to do next |
| 21 | [Exploration & Discovery](patterns/21-exploration-and-discovery.md) | Agents explore unknown spaces, generate & test hypotheses (e.g. co-scientist) | The goal is open-ended discovery, not optimizing a known objective |

---

## Appendices (supporting material)

| File | Covers |
|------|--------|
| [appendices/advanced-prompting.md](appendices/advanced-prompting.md) | ~23 prompting techniques (zero/few-shot, system/role, CoT, self-consistency, ToT, ReAct, APE/DSPy, structured output, multimodal, …) |
| [appendices/frameworks-overview.md](appendices/frameworks-overview.md) | LangChain, LangGraph, ADK, CrewAI, AutoGen, LlamaIndex, Haystack, MetaGPT, SuperAGI, Semantic Kernel, Strands — what each is and how to choose |
| [appendices/gui-to-real-world.md](appendices/gui-to-real-world.md) | Agents acting on GUIs / computer-use / physical-world interfaces |
| [appendices/agentspace.md](appendices/agentspace.md) | Google AgentSpace platform overview |
| [appendices/cli-agents.md](appendices/cli-agents.md) | Command-line agents (Gemini CLI, Claude Code, Copilot CLI) |
| [appendices/coding-agents.md](appendices/coding-agents.md) | "Vibe coding", context staging, leading an AI-augmented eng team |
| [conclusion.md](conclusion.md) | How patterns combine — worked multi-pattern example |
| [glossary.md](glossary.md) | Core agentic-AI term definitions |

---

## Quick decision guide

- **Task too big for one prompt?** → Prompt Chaining (sequential), Parallelization (independent), or Planning (unknown steps).
- **Need to pick among handlers?** → Routing.
- **Output quality unreliable?** → Reflection (+ Goal Setting for criteria, Evaluation to measure).
- **Needs external data/actions?** → Tool Use → standardize with MCP → ground with RAG.
- **One agent too complex?** → Multi-Agent; if agents span systems/orgs → A2A.
- **Must remember things?** → Memory Management.
- **High stakes / untrusted input?** → Guardrails + Human-in-the-Loop + Exception Handling.
- **Cost or latency pressure?** → Resource-Aware Optimization (+ Prioritization to sequence work).
- **Hard reasoning?** → Reasoning Techniques (CoT/ToT/ReAct/…).
- **Open-ended discovery?** → Exploration & Discovery.

Real agents combine several — see `conclusion.md`.
