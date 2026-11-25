---
name: production-operations
description: managing live agents through the Observe-Act-Evolve loop. Use this to maintain performance, manage unpredictable costs, and strategically improve agents based on production data.
---

# Production Operations for Agents

## Goal
Establish a continuous operational model that manages the inherent autonomy of agents, keeping them reliable, cost-effective, and safe as they interact with real-world users.

## The Continuous Operational Loop
Unlike static services, agents require an integrated cycle of intervention:

### 1. Observe (The Sensory System)
Gain deep insight into the agent's internal "thought process" using three pillars:
* **Logs:** Granular, factual records of every tool call, error, and decision.
* **Traces:** Narrative threads that reveal the causal path of why an agent took a certain action.
* **Metrics:** Aggregated reports on performance (latency), cost (token count), and operational health.

### 2. Act (Tactical Reflexes)
Real-time levers to stabilize the system:
* **Scaling:** Decouple logic from state. Use stateless, containerized services with externalized state management (e.g., Vertex AI Agent Engine's session service) to scale horizontally.
* **Reliability:** Implement automatic retries with exponential backoff for failed calls. Ensure tools are **idempotent** to prevent duplicate actions (like double-charging) during retries.
* **Security Containment:** Use "circuit breakers" (feature flags) to instantly disable tools if a threat is detected.

### 3. Evolve (Strategic Improvement)
Proactively fix root causes identified in the "Observe" phase:
* **Data-Driven Refinement:** Analyze production failures to create new, permanent test cases for your evaluation dataset.
* **Rapid Deployment:** Use an automated CI/CD pipeline to commit refined prompts, new tools, or updated guardrails and deploy them in hours or days rather than months.

## Optimization Levers
* **Speed:** Work in parallel and use smaller, efficient models for routine tasks.
* **Cost:** Shorten prompts, use cheaper models for easy steps, and batch requests where possible.
* **Granularity vs. Overhead:** Set a lower default log level (INFO) in production and use **dynamic sampling** (e.g., trace 10% of successes but 100% of errors).
