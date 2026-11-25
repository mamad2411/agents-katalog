---
name: agent-quality-flywheel
description: operational strategy for continuous agent improvement. Use this to implement the "Flywheel" lifecycle: Define Quality, Instrument, Evaluate, and Architect Feedback Loops.
---

# Agent Quality Flywheel

## Goal
Establish a self-reinforcing operational loop that turns production data into actionable insights, driving continuous improvement of agent reliability and trust.



## The Four Steps of the Flywheel

### 1. Define Quality (The Target)
* **Action:** Establish concrete targets based on the Four Pillars of Quality: Effectiveness, Cost-Efficiency, Safety, and User Trust.
* **Purpose:** Align evaluation efforts with true business value rather than abstract ideals.

### 2. Instrument for Visibility (The Foundation)
* **Action:** Instruct agents to produce structured **Logs** (the diary) and end-to-end **Traces** (the narrative).
* **Purpose:** Generate the rich evidence needed to measure the quality pillars. You cannot manage what you cannot see.

### 3. Evaluate the Process (The Engine)
* **Action:** specific judgment frameworks to assess both the final **Output** and the internal **Reasoning Process**.
* **Mechanism:** Use a hybrid engine of scalable **LLM-as-a-Judge** systems for speed and **Human-in-the-Loop (HITL)** for the "gold standard" ground truth.

### 4. Architect the Feedback Loop (The Momentum)
* **Action:** Convert production failures into permanent regression tests.
* **Workflow:** When a failure is captured and annotated, programmatically add it to the "Golden" Evaluation Set.
* **Result:** Every failure makes the system smarter, preventing regression and driving relentless improvement.

## Core Principles for Trustworthy Agents

### 1. Evaluation is an Architectural Pillar
* **Concept:** Do not treat quality as a final QA phase. Design agents to be "evaluatable-by-design," instrumented with telemetry ports from the first line of code.

### 2. The Trajectory is the Truth
* **Concept:** The final answer is just the last sentence of a long story. To understand success or failure, you must analyze the end-to-end "thought process" (Process Evaluation).

### 3. The Human is the Arbiter
* **Concept:** Automation (LLM judges) is for scale; humanity is for truth. Humans must define the rubric, validate nuanced outputs, and make the final judgment on safety and fairness.
