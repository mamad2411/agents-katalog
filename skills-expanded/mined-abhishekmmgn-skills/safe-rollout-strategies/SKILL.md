---
name: safe-rollout-strategies
description: techniques for de-risking agent releases. Use this to implement Canary, Blue-Green, and A/B testing strategies while leveraging GitOps for reliable rollbacks.
---

# Safe Rollout Strategies

## Goal
Minimize business risk during deployment by releasing agent changes incrementally and maintaining the ability to revert instantly to a known-good state.

## Release Patterns

### 1. Canary Deployment
* **Workflow:** Start by routing 1% of user traffic to the new agent version.
* **Focus:** Monitor closely for prompt injections, unexpected tool usage, or high error rates.
* **Action:** Gradually scale up to 100% or roll back instantly if issues are detected.

### 2. Blue-Green Deployment
* **Workflow:** Maintain two identical production environments ("Blue" for current live, "Green" for new).
* **Action:** Switch traffic instantly to "Green" once validated. If production-only bugs emerge, switch back to "Blue" for zero-downtime recovery.

### 3. A/B Testing
* **Workflow:** Run two agent versions simultaneously for different user segments.
* **Focus:** Compare versions based on real-world business metrics—like goal completion or conversion—to make data-driven release decisions.

### 4. Feature Flags
* **Workflow:** Deploy the code to production but keep it hidden behind a toggle.
* **Action:** Enable the new capability dynamically for specific users or teams to test in the "wild" before a general release.

## The Production "Undo" Button
Rigorous **versioning** is the foundation of safe rollouts. You must version every component:
* **Code and Prompts:** Core logic and instruction sets.
* **Model Endpoints:** Specific foundation model versions.
* **Tool Schemas:** API definitions and parameter requirements.
* **Memory Structures:** How the agent stores state.

## GitOps Workflow
Treat your repository as the single source of truth for your deployment history:
* **Deploy:** Every deployment should be triggered by a git commit.
* **Rollback:** Every rollback should be a simple `git revert`.
