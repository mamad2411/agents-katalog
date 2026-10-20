---
name: cma-specialist-coordinator
description: Claude Managed Agents (CMA) pattern for heterogeneous specialist teams. A frontier coordinator model orchestrates parallel worker agents with role-scoped toolsets, advisor escalation, and live subagent streaming.
---

# CMA Specialist Coordinator Architecture

## Overview
Rather than equipping a single model with dozens of tools, the coordinator architecture splits tasks across specialized subagents with strictly scoped capabilities.

## Architecture Principles
1. **Hierarchical Delegation:** A frontier coordinator plans work and spawns domain specialists (researcher, code editor, test runner).
2. **Tool Scoping:** Each worker agent has access only to the exact tools needed for its role, preventing hallucination cascades.
3. **Advisor Escalation:** Mid-tier workers can consult a stronger advisor model mid-turn for high-stakes decisions without incurring full-turn token costs.
4. **Live Subagent Streaming:** Coordinator streams subagent event deltas in real time for responsive UI feedback.
