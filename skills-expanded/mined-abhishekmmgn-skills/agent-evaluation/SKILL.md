---
name: agent-evaluation
description: methodologies for assessing agent capabilities, tool-use trajectories, and final response quality. Use this to implement automated testing and human-in-the-loop validation for agents.
---

# Agent Evaluation Frameworks

## Goal
Implement a multi-layered evaluation strategy that assesses not just the final answer, but the reasoning process (trajectory) and core capabilities of the agent.

## 1. Evaluating Trajectory (The "How")
* **Definition:** Assessing the sequence of steps (thoughts, tool calls, observations) the agent took to reach a conclusion.
* **Metrics:**
    * **Exact Match:** The agent's path perfectly mirrors the ideal reference trajectory (rigid).
    * **In-Order Match:** The agent completed the core steps in the correct sequence, ignoring harmless extra steps (flexible).
    * **Any-Order Match:** The agent performed all necessary actions, regardless of sequence.
    * **Tool Precision/Recall:** Did the agent call relevant tools and avoid irrelevant ones?.

## 2. Evaluating Final Response (The "What")
* **Definition:** Assessing the quality, relevance, and correctness of the final output provided to the user.
* **Mechanism:**
    * **Golden Datasets:** Compare output against manually curated "correct" answers.
    * **Autoraters (LLM-as-a-Judge):** Use a strong model to grade the response against specific criteria (e.g., "Is the tone helpful?", "Is the answer grounded in the context?").

## 3. Assessing Capabilities
* **Benchmarks:** Use standard benchmarks to test fundamental skills before deployment:
    * **Tool Calling:** Berkeley Function-Calling Leaderboard (BFCL) to test tool selection accuracy.
    * **Planning:** PlanBench to assess reasoning and multi-step logic.

## 4. Human-in-the-Loop (HITL)
* **Purpose:** Calibrate automated metrics and assess subjective qualities like "creativity" or "nuance" that machines miss.
* **Methods:**
    * **Direct Assessment:** Experts score performance on specific tasks.
    * **A/B Testing:** Compare the new agent version against the old one in production.
