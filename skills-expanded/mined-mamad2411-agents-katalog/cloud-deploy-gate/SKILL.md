---
name: cloud-deploy-gate
description: "The pre-deployment gate for managed AI platforms (Azure AI Foundry, Google Vertex AI, AWS Bedrock), evals packed, budget set, guardrails on, owner named. Use before any cloud deployment."
version: 1.0.0
author: Zorost Intelligence
license: MIT
metadata:
  zorost:
    tags: [cloud, deployment, foundry, vertex, bedrock, governance, ship]
    related_skills: [agent-ops-handoff, agent-loop-safety, eval-first-development]
    program_weeks: [18, 19, 20]
---

# Cloud Deploy Gate

## 1 · Purpose

Make "deploy to the cloud platform" a checklist with an owner, so the same agent
that passed locally cannot become an unbudgeted, unguarded, unowned cloud workload.

## 2 · When to use

- Before deploying any model endpoint, RAG app, or agent to Azure AI Foundry,
  Google Vertex AI, AWS Bedrock, or Databricks Model Serving.
- When a cloud deployment already exists and nobody can answer the gate questions.

## 3 · Inputs

- The working local artifact with its eval scores and traces.
- The target platform account with billing access visible.
- The spec's refused tradeoffs (they now become platform settings).

## 4 · Procedure

1. **Pack the evals.** The golden set and scorer travel with the deployment. First
   action in the cloud: re-run the eval there. The cloud score must match the local
   score within noise before anything else proceeds.
2. **Set the budget alarm before the first request.** Every platform has billing
   alerts; set one at the week's number (e.g. $25) and one at the panic number
   (e.g. $100). An unbudgeted experiment is how tutorials become invoices.
3. **Turn on the platform guardrails mapped to the spec.** Foundry content filters,
   Bedrock Guardrails, Vertex safety settings, map each refused tradeoff to its
   setting, in writing.
4. **Pin the model version.** Deploy an explicit model version/ARN, not "latest".
   Record it in the spec.
5. **Scope the credentials.** A dedicated service account / managed identity with
   least privilege: only the data sources this deployment reads. No personal
   credentials in any deployment.
6. **Enable logging and tracing** at the platform level (invocation logs, prompt/
   response logging where policy allows) and verify one request shows up end-to-end.
7. **Smoke-test the four failure modes**: empty retrieval, over-long input,
   rate-limit, and guardrail block. Each must produce the designed response, not a
   stack trace.
8. **Name the owner** in the deployment description/tag: the human who gets the
   budget and guardrail alerts. No orphan deployments.
9. **Write the teardown** commands before leaving the page, delete endpoint,
   release resources, revoke credentials. A training deployment lives exactly as
   long as its exercise unless its owner says otherwise.

## 5 · Anti-rationalization

| Excuse | Answer |
|---|---|
| "It's a free tier; budgets don't matter." | Free tiers end, and habits don't. Set the alarm when it costs nothing. |
| "The platform handles safety." | Platform defaults are not your spec. Map your refused tradeoffs explicitly. |
| "I'll clean up at the end of the week." | Endpoints bill by the hour and forget nothing. Teardown is part of deploy. |
| "The team account owns it collectively." | Collective ownership is no ownership. One name gets the alerts. |

## 6 · Red flags

- The eval has never run in the cloud environment.
- Billing alerts do not exist or route to a mailbox nobody reads.
- The deployed model is "latest".
- The deployment predates anyone's memory of creating it.

## 7 · Verify

- Cloud eval score recorded and within noise of local.
- Two budget alarms exist and route to the named owner.
- Guardrail mapping table: refused tradeoff → platform setting → verified.
- Smoke tests of the four failure modes recorded.
- Teardown commands written.

## 8 · ZoroLogistics example

Weeks 18 to 20 deploy the same support agent three ways. The gate is identical each
time: ZoroEval re-run in the cloud (Foundry: 0.88 vs local 0.90, within noise;
Vertex: 0.89; Bedrock: 0.90), $25/$100 alarms on the training subscription, refund
tool behind the platform's approval/action group, invocation logging on, owner
tagged, teardown scripted. The week ends with a three-platform comparison table,
cost per resolved ticket, latency, guardrail fit, which is exactly the artifact a
platform-selection decision needs.

---
© 2026 Zorost Intelligence LLC · zorost.com
