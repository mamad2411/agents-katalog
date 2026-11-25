---
name: agent-contracts
description: framework for implementing "Contract-Adhering Agents." Use this to define precise task specifications, deliverables, and negotiation loops to reduce ambiguity in complex workflows.
---

# Agent Contracts Strategy

## Goal
Transform vague agent instructions into formal "Contracts" that specify deliverables, scope, and validation criteria, mirroring real-world service agreements to ensure reliability.

## 1. The Contract Data Model
Define tasks using a structured schema to eliminate ambiguity. A valid contract must include:

| Field | Description | Required |
| :--- | :--- | :--- |
| **Task Description** | Specific, unambiguous description of the objective. | Yes |
| **Deliverables & Specs** | Precise outcomes and the specific criteria (validators) that make the deliverable acceptable. | Yes |
| **Scope** | Detailed boundaries of what is included and, critically, what is *out of scope*. | No |
| **Expected Cost/Duration** | Constraints on resource usage or time. | Yes |
| **Reporting** | The feedback loop mechanism (e.g., "Update every 5 steps"). | Yes |

## 2. The Contract Lifecycle
Agents should not just "execute"; they should negotiate. Implement this lifecycle state machine:

1.  **Submission:** The requester submits a draft contract.
2.  **Assessment:** The agent analyzes feasibility, cost, and ambiguity.
3.  **Negotiation/Revision:**
    * If ambiguous: Agent requests clarification (e.g., "Define 'brief summary'").
    * If too costly: Agent rejects and suggests a narrower scope.
4.  **Acceptance:** Both parties agree on the specs.
5.  **Execution:** The agent generates a plan and executes tasks.
6.  **Resolution:** Deliverables are scored against the initial specifications.

## 3. Feedback & Iteration
Allow the agent to push back during the **Assessment** phase using these structured feedback categories:
* **Underspecification:** "The requirements for X are missing."
* **Cost Negotiation:** "I cannot complete this within the requested token limit."
* **Risk:** "This task requires access to restricted data I do not have."

## 4. Subcontracts (Task Decomposition)
* **Concept:** If a contract is too complex, the agent (Contractor) becomes a "Client" and generates **Subcontracts** for other agents.
* **Mechanism:** The agent decomposes the main deliverable into smaller, self-contained contracts, managing the flow and aggregation of results from sub-agents.
