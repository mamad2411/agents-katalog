---
name: claude-agent-observability
description: Architectural blueprint for comprehensive AI agent observability, distributed trace telemetry, tool call latency profiling, token spend metering, and live session browser replays.
---

# AI Agent Observability Architecture

## Overview
Production agents require specialized observability architectures to track non-deterministic reasoning, multi-turn tool latencies, and token cost curves.

## Observability Dimensions
1. **Distributed Spans:** Captures every agent step, model inference round, and MCP tool call as an OpenTelemetry span.
2. **Token & Cost Profiling:** Separates cached prompt tokens, raw input tokens, and reasoning tokens with per-session spend ceilings.
3. **Tool Call Latency Heatmaps:** Identifies bottlenecks across external APIs and shell executions.
4. **Session Replay Browser:** Serializes agent trajectories into navigable JSON/HTML event trees for offline evaluation and auditing.
