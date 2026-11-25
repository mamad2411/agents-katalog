---
name: api-spec
description: "Design or validate API wire contracts after business acceptance, or reconstruct API source evidence as an observed candidate without defining unknown wire rules."
---

# API Specification

## Entry Gate

Own bounded API contract artifacts and their validation. Resolve the service, native
authority, consumers, and accepted business semantics before defining wire behavior.
Missing identity, permission, lifecycle, success, or failure decisions block the
affected definition; return the exact gap to the product or domain owner. Evidence-only reconstruction uses its separate profile and cannot satisfy those definition preconditions.

## Route Map

| Request condition | Read or route | Result |
| --- | --- | --- |
| Explicitly reconstruct API source evidence without accepted wire authority | [source reconstruction](references/source-reconstruction.md) | Observed projection, source refs and unresolved semantics; no normative schema |
| Create or revise an API contract | [Contract design](references/contract-design.md) | One declared authority and scoped artifact change |
| Author or validate OpenAPI fields, security, or compatibility | Applicable [OpenAPI authoring](references/openapi-authoring.md) sections | Wire definitions and separate validation evidence |
| Confirm an already accepted contract without changes | [Existing baseline](references/contract-design.md#existing-baseline) | Bounded no-op evidence |
| Feature behavior or shared business meaning is undecided | `product-spec` or `domain-modeling` | Owner decision before the dependent contract |
| Implement source or review a fixed change | Matching `dev-*` owner or `repo-review` | No implementation or independent review inside API authoring |

## Invariants

- Declare `code-first` or `contract-first` per service; never hand-maintain competing
  endpoint, request, response, or error authorities.
- Preserve project-native envelope, authentication, gateway, naming, pagination, and
  error conventions. Frontend wrappers, old prose, and parser success cannot establish
  backend truth. Read only sources allowed by the task and project.
- Keep business context in its Markdown owner and wire structures in OpenAPI. Link
  definitions instead of copying schemas into prose; create no unneeded companion file.
- Only the accepted owner can promote a draft contract. Distinguish structural checks,
  compatibility, implementation, consumers, runtime/gateway, and deployment evidence.
- Write contract artifacts only. Do not edit implementation, generate clients, operate
  runtime services, change Git state, or invent new validation infrastructure here.

## Output Map

Return native authority path and strategy, phase/status, content identity and accepted
owner evidence when applicable, changed operations, compatibility, validation results,
and unresolved decisions. Mark missing required evidence `Not verified`; no-op requests
retain their accepted artifact unchanged. A capability handoff references these native
artifacts and does not require a new project-side metadata format. Reconstruction returns an observed projection and exact source/content identity separately from any accepted native contract; its unknown semantics remain unresolved.

## Reference Map

- Load [contract design](references/contract-design.md) for authority, lifecycle, and
  authoring workflow; use [OpenAPI authoring](references/openapi-authoring.md) for the
  changed wire or validation concern.
- Load [source reconstruction](references/source-reconstruction.md) for evidence-only reverse documentation.
- Maintainers only: [eval cases](references/eval-cases.md); do not load during ordinary
  API authoring.
