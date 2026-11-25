---
name: agent-quality-framework
description: core framework for defining and measuring agent quality. Use this to shift from traditional software verification to agent validation using the "Outside-In" approach and the Four Pillars of Quality.
---

# Agent Quality Framework

## Goal
Adopt a holistic evaluation strategy that moves beyond simple code verification ("Did we build it right?") to system validation ("Did we build the right product?"), addressing the non-deterministic nature of autonomous agents.

## The Paradigm Shift
Traditional software fails explicitly (crashes), but AI agents fail implicitly (quality degradation). Therefore, evaluation must focus on the entire decision-making process, not just the final output.


## The Four Pillars of Agent Quality
To measure success, you must track these four interconnected dimensions:

### 1. Effectiveness (Goal Achievement)
* **Definition:** Did the agent successfully and accurately achieve the user's intent?
* **Metrics:** Task Success Rate (e.g., PR acceptance rate, booking completion), User Satisfaction (CSAT), and Overall Quality (accuracy/completeness).

### 2. Efficiency (Operational Cost)
* **Definition:** Did the agent solve the problem using the optimal amount of resources?
* **Metrics:** Total tokens (cost), Wall-clock time (latency), and Trajectory complexity (total number of steps/tools used).
* **Anti-Pattern:** An agent that takes 25 steps and 5 failed tool calls to do a simple task is low-quality, even if it eventually succeeds.

### 3. Robustness (Reliability)
* **Definition:** How does the agent handle adversity, ambiguity, and environmental failures?
* **Capabilities:** Retrying failed API calls, asking for clarification on ambiguous prompts, and failing gracefully with helpful error messages instead of crashing or hallucinating.

### 4. Safety & Alignment (Trustworthiness)
* **Definition:** Does the agent operate within defined ethical boundaries and security constraints?
* **Scope:** Fairness/Bias checks, Prompt Injection defense, PII protection, and refusal of harmful instructions.

## Failure Modes to Watch
* **Algorithmic Bias:** Amplifying systemic biases from training data.
* **Hallucination:** Inventing plausible but incorrect facts or tool parameters.
* **Concept Drift:** Performance degrading as real-world data evolves away from training data.
* **Emergent Behaviors:** Developing unanticipated strategies (e.g., "proxy wars" with other bots).
