---
name: agent-security-governance
description: comprehensive security layers for autonomous agents. Use this to implement system instructions as constitutions, multi-stage filtering, and continuous red-teaming.
---

# Agent Security & Governance

## Goal
Build trust and safety into the agentic lifecycle by implementing multi-layered defenses that manage risks unique to autonomous systems, such as rogue actions and data leakage.

## Core Risks of Autonomy
Autonomous agents make independent decisions, which introduces distinct security vulnerabilities:
* **Prompt Injection:** Malicious users tricking agents into bypassing restrictions or performing unintended actions.
* **Data Leakage:** Inadvertent exposure of sensitive or confidential information through agent responses or tool outputs.
* **Memory Poisoning:** Corruption of future interactions by storing false or malicious information in the agent's long-term state.

## The Three Layers of Defense

### 1. Policy Definition (The Constitution)
* **System Instructions (SIs):** Engineer clear policies for desired and undesired behavior directly into the agent's core instructions.
* **Scope Definition:** Explicitly define the boundaries of what the agent can and cannot do.

### 2. Enforcement Layer (Guardrails)
* **Input Filtering:** Use classifiers to analyze user prompts and block malicious intents before they reach the reasoning model.
* **Output Filtering:** Run agent responses through safety filters to check for PII, toxic language, or policy violations before delivery.
* **HITL Escalation:** Program the system to pause and require human approval for high-risk or ambiguous actions, such as financial transactions or data deletion.

### 3. Continuous Assurance (Testing)
* **Dedicated RAI Testing:** Use simulation agents and dedicated datasets to test for specific risks like bias (Parity evaluations) or harmful viewpoints (NPOV).
* **Proactive Red Teaming:** Actively attempt to break the system through creative manual testing and AI-driven adversarial simulations.
* **Continuous Re-evaluation:** Trigger a full safety evaluation pipeline for every change made to the model or its instruction set.

## Secure Response Playbook
When a threat is detected in production, follow this sequence:
1. **Contain:** Immediately stop the harm using "circuit breakers" or feature flags.
2. **Triage:** Route suspicious requests to a human review queue to investigate impact.
3. **Resolve:** Develop a permanent logic patch and deploy it through the automated CI/CD pipeline.
