---
name: ansvar-ai-compliance
description: Scope an AI system's EU compliance questions and guide a supported AI Act gap analysis, FRIA, DPIA or AI threat model using Ansvar evidence. Use for AI product or deployment compliance reviews, not generic AI coding or automatic certification.
license: CC-BY-4.0
---

# Ansvar AI Compliance

Read [account and evidence boundaries](references/grounding.md) first.

## Scope the decision

Use facts already supplied. Establish the intended purpose, who provides and
deploys the system, affected people, countries, deployment date, personal-data
categories, significant decisions, and human oversight. Ask only for missing
facts that change the route. Use categories and synthetic examples, not real
people's records.

For an initial obligations question, discover served AI Act sources, search the
relevant provisions and follow their exact lookup hints. Separate the customer's
role, use-case classification and applicable dates. Fetch dates and exceptions;
do not embed a statutory deadline in this skill. A sector-level
`check_applicability` result cannot determine an AI system's risk class.

Return a scoping brief: supplied facts, assumptions, potentially relevant
obligations with sources, unresolved questions and the suitable next assessment.
Do not spend a workflow run just to explain the available routes.

## Select a supported assessment

Call `list_workflow_types` on each new run. Use `scope_workflow` to narrow
ambiguous choices, following its question options rather than guessing values.
The live registry decides ids, input requirements and access. Candidate families:

- AI Act gap analysis: check the row's scope. The current high-risk-provider
  variant does not cover every deployer, chatbot, GPAI provider or AI system.
  Start it only after evidence and confirmed facts support that scope.
- FRIA: establish the AI-system and deployer conditions before selecting it.
  Do not declare a FRIA mandatory merely because someone uses AI.
- DPIA: assess one processing activity and its screening conditions.
- AI threat model: assess technical security boundaries and AI-specific threats.
  It does not substitute for the legal assessments above.

If no served workflow matches, explain the unsupported scope and provide only
the requested source-backed scoping brief. Never force a user into a mismatched
workflow to produce a report.

Before a run, read [workflow execution](references/workflow-loop.md) and
[report delivery](references/delivery-rules.md). Explain state storage and
allowance use as described in the account boundaries. Follow the engine's
current steps; these instructions do not redefine the workflow.

For citation-producing assessment steps, perform and record the five enrichment
passes: primary regime; horizontal regimes (evaluate GDPR, NIS2, the AI Act,
EN 301 549, CSRD and sectoral cyber rules for relevance); sector-regulator
sources; case-law validation where accessible; and authority guidance.
Resolve source ids first. Mark inapplicable passes with reasons and gated or
empty evidence as unresolved. Do not fetch court text outside admitted scope.
Never invent case law or quote licensed standards without entitlement.

Deliver the server's receipt and report according to the bundled delivery
rules and account boundaries. Keep unsupported metrics, unresolved sources,
human review gates and artifact expiry visible.

Example: Using Ansvar, scope the EU AI Act obligations for our customer-support
AI system and identify which facts you need before recommending an assessment.
