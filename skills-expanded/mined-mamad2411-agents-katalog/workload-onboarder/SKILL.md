---
name: workload-onboarder
description: >-
  Execute a disposition map: onboard existing Azure workloads onto the
  platform per their assessed disposition — Recipe-wrap (absorb existing
  Terraform/Bicep unchanged behind a Radius Recipe), Refactor (regenerate on
  the golden path with AVM modules), Leave in place (register for visibility
  only), or Retire (decommission plan). Use for brownfield onboarding,
  migrating workloads into a platform, wrapping legacy IaC, or turning an
  estate assessment into merged PRs. Works workload-by-workload, PR-gated,
  with rollback notes per move.
---

# Workload Onboarder

## Purpose
The bridge from assessment to platform: `azure-estate-assessor` decides what
should happen to each workload; this skill makes it happen, one PR at a time.
Brownfield onboarding is the gap official guidance leaves open — this is the
execution half of that differentiator.

## Playbook per disposition
1. **Recipe-wrap** (lowest effort, first choice when IaC exists). Radius
   Recipes accept existing Terraform modules and Bicep templates as-is — wrap
   the workload's IaC in a Recipe, register it against the abstract Resource
   Type in the target environment, and the workload joins the platform's app
   graph without a rewrite. Validate the wrapped recipe's `result.values`
   against the golden-path contract (host/port/baseUrl etc.).
2. **Refactor** (no IaC, or IaC failing the guardrail gate). Derive the
   workload's spec from the estate evidence (reverse-SDD: deployed state ->
   spec -> regenerate), then rebuild on the golden path with AVM modules via
   `radius-golden-path-builder`. Exports are drafts — "Export is not
   guaranteed to succeed" — so exported HCL/Bicep informs the spec; the
   golden path generates the production IaC.
3. **Leave in place.** Register in the catalog/app graph for visibility
   (ownership, dependencies) without platform management; record the reason
   and a revisit date.
4. **Retire.** Decommission plan: dependency check from the estate evidence,
   data retention per constitution, deletion PR with approval gate.

## Workflow
1. Take the disposition map; sequence by effort and risk (S before M/L;
   non-prod before prod; Recipe-wrap before Refactor).
2. Per workload: branch -> implement the disposition -> run
   `iac-guardrail-verifier` -> PR with the disposition row, evidence refs,
   and rollback note -> human approval -> merge; GitOps reconciles.
3. Update the disposition map status per row (proposed -> PR open -> merged
   -> verified); the updated map is the onboarding progress report, and can
   be returned as a follow-up I9 assessment delta.

## Guardrails
- One workload per PR; never batch dispositions across risk classes.
- No destructive action (Retire) without the constitution's approval chain.
- Every wrapped or regenerated workload must pass the verifier before the PR
  opens — onboarding does not grandfather violations.

## Delegates to
- Portal/catalog registration mechanics beyond the app graph → `platform-assessment:idp-adp-architect` (portal design) and the org's Backstage guidance
- IaC verification → `iac-guardrail-verifier`
- Golden-path regeneration → `radius-golden-path-builder`
