---
name: iac-guardrail-verifier
description: >-
  Adversarially verify agent- or human-generated Azure IaC against the
  four-layer enforcement model: generation-time constitution rules (AVM-first,
  naming, tagging, data-classification networking), plan-time static analysis
  (bicep build/lint, Checkov/OPA), deploy-time Azure Policy alignment, and
  runtime policy backstop. Use to review platform PRs, validate Bicep or
  Radius Recipes, check AVM module pins and statuses, gate golden-path
  changes, or audit demo shortcuts before production. Blocks on violations;
  cites constitution rule IDs.
---

# IaC Guardrail Verifier

## Purpose
The four-layer enforcement model is what makes agent-generated infrastructure
safe to accept: if AI can generate compliant infrastructure on demand, the
platform team's job shifts to shipping guardrails, patterns, and agents. This
skill is the guardrail half — the adversarial reviewer for everything the
other skills produce.

## The four layers (check in order, report per layer)
1. **Generation time** — does the change obey the constitution? AVM-first with
   dated justification comments on any raw resource; module versions pinned
   and resolved from the registry (never hand-invented); naming/tagging rules;
   private endpoints where data classification demands them; no standing
   secrets.
2. **Plan time** — static analysis: `az bicep build` / `bicep lint` (restore
   against the public registry), Checkov/OPA policies, recipe contract checks
   (Radius `result.values` shapes are part of the golden-path API — breaking
   them is a breaking change).
3. **Deploy time** — template validation and Azure Policy compliance at the
   target scope (what-if where credentials permit).
4. **Runtime backstop** — confirm Azure Policy deny/audit assignments cover
   the change class, so drift and out-of-band changes get caught even if
   layers 1-3 were bypassed.

## AVM-specific checks
- Module status from the machine-readable index: **Available** required;
  flag Orphaned, refuse Deprecated.
- Pins resolvable in the registry (CI-enforced; a pin that does not resolve
  fails the gate).
- Telemetry flag (`enableTelemetry`) disclosed when defaulted on.
- Known AVM gaps honestly handled: raw resources for Azure Monitor workspace
  and Managed Grafana are acceptable *with* the dated justification comment.

## Demo-shortcut audit
Reference implementations legitimately carry marked shortcuts (key-based
Cosmos auth, public Postgres with Azure-services firewall, public ACA
environment, empty OIDC issuer). Production promotion requires each
`// Demo shortcut` flipped: workload identity, private endpoints, Entra auth.
The verifier fails any production-targeted PR still carrying the marker.

## Output
A per-layer findings report as a PR review: verdict (pass / warn / block),
finding, constitution rule ID or source, and the concrete fix. Blocking
findings prevent merge; the verifier never edits code itself — it reviews.

## Guardrails on the guardrail
- Never soften a block because the author is an agent with high confidence;
  plausible-but-wrong is the failure mode this skill exists to catch.
- Maturity honesty is a checkable claim: any doc/PR presenting Radius as
  production-GA, Dapr Conversation API as stable, or unpublished AVM modules
  as available gets a correctness finding.

## Delegates to
- Org-level security program, vuln management, compliance regimes → `platform-assessment:platform-security-playbook`
- Agent credential hygiene → `adp-enablement:agent-identity-engineer`
- Fitness-function instrumentation of these gates over time → `adp-enablement:platform-fitness-functions`
