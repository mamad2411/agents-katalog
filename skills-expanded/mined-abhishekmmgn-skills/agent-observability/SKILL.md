---
name: agent-observability
description: strategies for agent observability (logging, tracing, metrics). Use this to instrument agents for debugging, performance tracking, and quality assurance.
---

# Agent Observability Strategies

## Goal
Move beyond simple monitoring ("Is it running?") to deep observability ("How is it thinking?"), enabling the diagnosis of complex failures in non-deterministic systems.

## The Three Pillars of Observability

### 1. Structured Logging (The Diary)
* **Definition:** Immutable, timestamped records of discrete events.
* **Best Practice:** Use structured JSON logs to capture the full context: prompt/response pairs, intermediate reasoning (Chain of Thought), and tool inputs/outputs.
* **Pattern:** Record the *intent* before an action and the *outcome* after to distinguish between decision failures and execution failures.

### 2. Distributed Tracing (The Narrative)
* **Definition:** A visual "yarn" connecting individual log entries (spans) into a single end-to-end task execution.
* **Usage:** Essential for root cause analysis. It reveals if a bad final answer was caused by a retrieval failure (RAG), a tool error, or an LLM hallucination.
* **Standard:** Use OpenTelemetry to link spans across services.



### 3. Metrics (The Scorecard)
Aggregated data points for tracking health over time. Separate these into two dashboards:

#### System Metrics (Operational Health)
* **Audience:** SREs / DevOps.
* **Key Metrics:** P99 Latency, Error Rate (traces with `error=true`), Token Consumption, and API Cost per Run.

#### Quality Metrics (Decision Health)
* **Audience:** Product / Data Science.
* **Key Metrics:**
    * **Trajectory Adherence:** Did the agent follow the ideal path?
    * **Hallucination Rate:** Frequency of ungrounded statements.
    * **Task Completion Rate:** Percentage of traces reaching a "success" state.

## Operational Best Practices
* **Dynamic Sampling:** To save costs, log 100% of errors but only sample 10% of successful traces in production.
* **PII Redaction:** Integrate PII scrubbing directly into the logging pipeline to sanitize user inputs before storage.
