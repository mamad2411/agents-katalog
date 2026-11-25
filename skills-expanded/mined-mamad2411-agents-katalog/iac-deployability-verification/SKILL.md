---
name: "iac-deployability-verification"
description: "Make generated Infrastructure-as-Code READY TO DEPLOY, for any cloud/provider/format. Enforces API authenticity (no hallucinated functions/methods/attributes/resource arguments), self-containment (every referenced variable/secret/dependency declared), deployment-topology correctness, and native-tool verification — so 'syntactically valid' is never mistaken for 'deployable'. Use as the final gate on any IaC the workflow emits."
version: 1
created: "2026-06-25T03:34:24+05:30"
updated: "2026-06-26"
---
## When to Use
Use as the FINAL gate before emitting any IaC artifact (Terraform, Bicep, ARM, CloudFormation/SAM, Pulumi,
OpenAPI, provider policy documents). Provider- and format-agnostic: resolve the target from the artifact/TSA,
then apply the checks below. The goal: the emitted file deploys unchanged through the user's normal pipeline.

## Core Principle
**Well-formed ≠ deployable.** Passing an XML/JSON/HCL parser proves only syntax. Deployability additionally
requires: every identifier the provider must resolve actually EXISTS, every referenced input is DECLARED, the
config is correct for the deployment TOPOLOGY, and a provider-native tool (or a documented-API audit) confirms
it. Never report PASS/DEPLOYABLE on syntax alone.

## Procedure
1. **Resolve target** — provider + IaC format + the runtime that will execute any embedded expressions
   (e.g. APIM C# policy expressions, AWS VTL/`$context`, Apigee JS/Message Templates, CloudFormation
   intrinsics). Each runtime has its OWN API surface; check against THAT, not general programming knowledge.
2. **API-authenticity audit** — for every function, method, property, attribute, resource type, and resource
   argument used: confirm it exists in the provider's documented surface (provider skill, RAG, or docs). If you
   cannot confirm it exists, DO NOT use it — pick a documented alternative. Hallucinated APIs are the #1 cause
   of "valid-but-undeployable" output.
3. **Self-containment audit** — every variable/parameter/secret/local/module/data-source the file references
   must be declared (with type + a safe example value) or emitted as a companion file (`variables.tf` +
   `*.tfvars.example`, ARM `parameters`, CFN `Parameters`, Bicep `param`, Helm `values.yaml`, etc.). Zero
   dangling references. No literal secrets — use variables/secret refs, but DECLARE them.
4. **Topology correctness** — apply the deployment topology (fronting CDN/WAF/LB/API-front such as Azure Front
   Door, CloudFront, Cloud Armor, ALB). Behind a fronting layer, client identity/IP/host/scheme come from
   FORWARDED headers, not the socket/peer. Cross-origin + credentials ⇒ third-party-cookie rules apply.
5. **Native verification** — the validation CLI is usually NOT pre-installed: PROVISION it on demand and run
   basic OFFLINE, login-free checks per `iac-toolchain-provisioningv2` (e.g. terraform fmt -check; terraform
   init -backend=false; terraform validate; bicep build; cfn-lint; spectral lint). Capture exit code + output.
   If the toolchain genuinely cannot be installed (no network/locked registry), fall back to the documented-API
   audit and explicitly mark each gate `tool-verified` or `review-only` — never a false pass.
6. **Pin & idempotency** — provider/runtime versions pinned; re-applying is a no-op; deterministic ordering.
7. **Verdict** — emit DEPLOYABLE only if API-authenticity + self-containment + topology + (native or audited)
   verification all pass; else NOT_DEPLOYABLE with the exact unresolved items.

## Patterns
- Prefer the lowest-common-denominator DOCUMENTED accessor over a "nicer" one you are unsure exists.
- Emit a companion variable/parameter file with every run so the artifact is self-contained.
- Drive topology, region, domain, and identity decisions from declared inputs — never from hard-coded guesses.
- Treat embedded-expression runtimes (policy C#, VTL, JS, intrinsics) as separate languages with their own,
  narrower API surface than the host language.
- Run the native validator first; let its output, not your assumption, decide PASS.

## Anti-Patterns
- Inventing a function/method/attribute because it "should" exist (e.g. calling a collection method from a
  different type's API on the provider's header/dictionary type). If unverified → forbidden.
- Reporting PASS because a parser accepted the file (well-formedness ≠ deployability).
- Referencing variables/parameters/secrets the file never declares → pipeline fails at plan/deploy.
- Using socket/peer client IP, Host, or scheme when a CDN/WAF/LB sits in front.
- Leaving provider/runtime versions unpinned; emitting non-idempotent resources.

## Tool Selection
- command_line — run the native validator/formatter and capture exit code + output:
  - Terraform: `terraform fmt -check`, `terraform init -backend=false`, `terraform validate`
  - Bicep: `bicep build`/`az bicep build` ; ARM: `az deployment … validate` / arm-ttk
  - CloudFormation/SAM: `cfn-lint`, `aws cloudformation validate-template`, `sam validate`
  - Pulumi: `pulumi preview`
  - OpenAPI / API specs: `spectral lint`, `openapi-generator validate`
  - Provider policy docs (APIM/Apigee/Kong): schema/lint where available; otherwise documented-API audit.
- read_file / write_file — load the generated artifact; emit corrected artifact + companion variable file.
- get_rag_context / get_account_project_access_details (Slingshot-ASK) — verify a specific provider API exists
  and retrieve the correct documented signature/attribute when uncertain.
- todo — track each NOT_DEPLOYABLE item to closure.

## Validation Rules
- DEP-1  API-AUTHENTICITY: zero unverifiable functions/methods/attributes/resource args. (FAIL ⇒ NOT_DEPLOYABLE)
- DEP-2  SELF-CONTAINED: zero undeclared variables/params/secrets/refs; companion declarations emitted.
- DEP-3  TOPOLOGY: client IP/host/scheme/identity sourced correctly for the declared fronting layer.
- DEP-4  NATIVE-VERIFY: provider validator run and clean — OR each gate explicitly marked review-only.
- DEP-5  PIN+IDEMPOTENT: versions pinned; re-apply is a no-op; no literal secrets.
- DEP-6  NO-FALSE-PASS: never DEPLOYABLE on syntax/well-formedness alone.
FAIL ⇒ emit NOT_DEPLOYABLE and the precise unresolved items.

## RAG Sources
When use_rag is on, call `get_rag_context` to confirm uncertain provider APIs (exact method/attribute names and
signatures), the deployment topology, and prior incidents where invented/misused APIs broke a deploy. Prefer
retrieved provider documentation over recall; cite what you verified.
