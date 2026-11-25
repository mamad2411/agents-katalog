---
name: production-pipelines
description: strategies for building automated CI/CD pipelines for agents. Use this to implement "shift left" testing, staged validation, and evaluation-gated deployments.
---

# Production Pipelines for Agents

## Goal
Establish a disciplined pre-production process that trades manual uncertainty for automated confidence, ensuring no agent reaches users without passing rigorous quality and safety gates.

## The CI/CD Funnel (Shift Left)
Design your pipeline to catch errors as early and as cheaply as possible by following a structured three-phase workflow:

### Phase 1: Pre-Merge Integration (CI)
* **Trigger:** Automatically runs when a developer opens a Pull Request (PR).
* **Checks:**
    * Fast unit tests and code linting.
    * **Agent Quality Evaluation:** Run the evaluation suite against key scenarios to ensure performance hasn't degraded.
* **Goal:** Act as a gatekeeper for the main branch to prevent performance pollution.

### Phase 2: Post-Merge Staging (CD)
* **Trigger:** Runs after a change is merged into the main branch.
* **Environment:** A high-fidelity replica of production.
* **Tests:**
    * Resource-intensive load testing.
    * Integration tests against live remote services.
    * **Dogfooding:** Internal user testing to gather qualitative feedback.

### Phase 3: Gated Production Deployment
* **Trigger:** Requires manual approval from a Product Owner (Human-in-the-Loop).
* **Goal:** Promote the exact validated artifact from staging to the live environment.

## Core Automation Technologies
* **Infrastructure as Code (IaC):** Use tools like Terraform to ensure environments are identical, repeatable, and version-controlled.
* **Testing Frameworks:** Utilize tools like Pytest to handle agent-specific artifacts, such as conversation histories and reasoning traces.
* **Secrets Management:** Use dedicated services like Secret Manager to inject API keys at runtime instead of hardcoding them.
