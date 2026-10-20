---
name: authzen
description: "AuthZEN Authorization API: PEP-to-PDP access evaluation and search over HTTPS JSON. Use when building or reviewing a Policy Enforcement Point (PEP) that asks a Policy Decision Point (PDP) for access decisions, or a PDP that implements the API: the subject, resource, action and context information model, decision and decision context, the Access Evaluation endpoint (/access/v1/evaluation), the Access Evaluations batch endpoint with default values and evaluations_semantic (execute_all, deny_on_first_deny, permit_on_first_permit), Subject, Resource and Action Search with pagination (page, next_token), PDP metadata at /.well-known/authzen-configuration and signed_metadata, HTTP error codes, X-Request-ID, PEP authentication, the interop test vectors, and the Basic, Batch, Search and Discovery certification levels, and upgrading a PEP or PDP from the 1.0 Implementer's Draft. Targets the OpenID AuthZEN Authorization API 1.0 Final; no newer draft line exists."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# AuthZEN Authorization API

The Authorization API lets a Policy Enforcement Point (PEP) ask a Policy Decision Point (PDP) for access decisions without either knowing the other's internals. The PDP serves the API and the PEP calls it (Authorization API § 1). It has evaluation endpoints that return decisions, search endpoints that list permitted subjects, resources or actions, and a metadata document for discovery.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), cited inline as (AuthZEN § section) for the specification and (Cert § anchor) for the certification scenario. If a rule is not in a source, it is not in this skill.

## Inputs (fill in, or ask before starting)

- **Role:** PEP (the caller), PDP (the server), or both, for example a gateway that enforces decisions from a hosted PDP.
- **Target version:** AuthZEN Authorization API 1.0 (current, the Final; the default). AuthZEN Authorization API 1.0 Implementer's Draft 1 is legacy: read it and upgrade from it, never author it. No preview line exists. Later revisions may add to the API but MUST NOT change 1.0 (AuthZEN § 4). See [`references/versions.md`](references/versions.md).
- **APIs in scope:** Access Evaluation is the core feature. Access Evaluations, the three Search APIs and metadata are optional for a PDP (AuthZEN § 3, § 9.1.1).
- **PEP authentication:** mutual TLS, OAuth or an API key. The choice is out of scope of the specification (AuthZEN § 11.2).
- **Certification target:** none, or one or more of Basic, Batch, Search and Discovery, each with Core and Properties sub-levels (Cert § certification-levels).
- **Sources refresh:** before relying on a pin, compare it with the [OpenID Foundation specifications index](https://openid.net/developers/specs/) and the latest commit of the [AuthZEN repository](https://github.com/openid/authzen). If a revision changed, re-read the source and update `metadata.json` and [Sources](#sources).

## Invariants

1. Every API call is an HTTPS `POST` with `Content-Type: application/json` and a JSON object body. A successful response is `200` with `Content-Type: application/json` (AuthZEN § 10.1, § 10.1.1).
2. A deny is `200` with `{ "decision": false }`. The error codes `400`, `401`, `403` and `500` describe the request or its processing and never mean deny (AuthZEN § 10.1.2).
3. `decision: false` MUST NOT be permitted to go forward. A PEP MAY reject `decision: true` when it does not understand the decision `context` (AuthZEN § 5.5).
4. A Subject and a Resource each need string `type` and `id`, with `id` scoped to `type`. An Action needs a string `name`. `properties` is an optional object (AuthZEN § 5.1, § 5.2, § 5.3).
5. An evaluation request needs `subject`, `action` and `resource`, and `context` is optional (AuthZEN § 6.1). A PDP returns `400 Bad Request` when a required attribute is missing (AuthZEN § 10.1.1).
6. In a batch, the top-level `subject`, `action`, `resource` and `context` are defaults that each evaluation may override. Decisions come back in request order. With no `evaluations` array, or an empty one, the request behaves as a single evaluation (AuthZEN § 7.1, § 7.1.1, § 7.2).
7. Per-item errors in a batch are returned as `decision: false` with details in that item's `context`. Errors about the whole payload use HTTP status codes (AuthZEN § 7.2.1).
8. Search results contain only entities of the searched type. When a response is partial it MUST include `page` with `next_token`, and that token is an empty string after the last page (AuthZEN § 8.2.2, § 8.3).
9. The `policy_decision_point` in metadata MUST equal the identifier used to build the metadata URL, or the metadata MUST NOT be used (AuthZEN § 9.2.3).
10. The PEP–PDP connection MUST be secured, for example with TLS. The PDP SHOULD authenticate the PEP and answers a failed authentication with `401`, which SHOULD carry `WWW-Authenticate` (AuthZEN § 11.1, § 11.2, § 11.3).

## Workflow

1. **Pick the version.** Target the 1.0 Final. An existing PEP or PDP built against draft 01, 02 or 03 is legacy input to an upgrade.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is the Final, and any draft-era PEP or PDP is marked for upgrade.
2. **Model the request.** Map your principal, target, operation and environment to `subject`, `resource`, `action` and `context`.
   -> [`references/information-model.md`](references/information-model.md)
   ✓ Every subject and resource has a string `type` and `id`, and every action has a `name`.
3. **Call or serve the Access Evaluation API.**
   -> [`references/evaluation-apis.md`](references/evaluation-apis.md)
   ✓ A deny returns `200` with `decision: false`, and a missing `subject`, `action` or `resource` returns `400`.
4. **Add the Access Evaluations API when you batch.**
   -> [`references/evaluation-apis.md`](references/evaluation-apis.md)
   ✓ Tests cover default inheritance, per-item override, response order, an empty array, and each `evaluations_semantic` value.
5. **Add the Search APIs when you list permitted entities.**
   -> [`references/search-apis.md`](references/search-apis.md)
   ✓ The searched entity carries no `id` (or it is ignored), Action Search omits `action`, and pagination ends with an empty `next_token`.
6. **Publish or consume PDP metadata.**
   -> [`references/metadata-transport.md`](references/metadata-transport.md)
   ✓ The PEP compares `policy_decision_point` with the identifier it used, and falls back to the default paths when an endpoint is not published.
7. **Secure the transport.** Authenticate the PEP, echo `X-Request-ID`, and limit payload size and request rate.
   -> [`references/metadata-transport.md`](references/metadata-transport.md)
   ✓ An unauthenticated call returns `401` with `WWW-Authenticate`, and a request carrying `X-Request-ID` gets the same value back.
8. **Upgrade** (only when asked). Follow the Implementer's Draft to Final checklist.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded PEP or PDP passes the Final's checks and returns the same decisions as before.
9. **Check conformance.** Load the certification fixture and run the interop vectors that match your scope.
   -> [`references/conformance.md`](references/conformance.md)
   ✓ The eight fixture decisions hold and the prerequisites for each certification sub-level are met.

## Verify before done

- [ ] Every request and response body is a JSON object over HTTPS `POST`, with `application/json` both ways (AuthZEN § 10.1).
- [ ] A deny is always `200` with `decision: false`, never an HTTP error status (AuthZEN § 10.1.2).
- [ ] Per-item batch errors come back as `decision: false` with details in `context` (AuthZEN § 7.2.1).
- [ ] The PEP enforces `decision: false`, and decides what to do with a `context` it does not understand (AuthZEN § 5.5).
- [ ] Batch requests fill omitted fields from the top-level defaults, and `execute_all` is the default semantic (AuthZEN § 7.1.1, § 7.1.2.1).
- [ ] Mid-pagination requests change only `page.token` (AuthZEN § 8.2.1).
- [ ] Metadata unknown to the PEP is ignored, and supported `signed_metadata` is verified and takes precedence over plain values (AuthZEN § 9.1.3, § 9.2.2, § 9.2.3).
- [ ] Endpoints include `v1` in their path (AuthZEN § 4).
- [ ] JSON follows I-JSON, and `null` properties are omitted (AuthZEN § 11.5).
- [ ] The certification scenario and interop vectors in use match the commit pinned in [Sources](#sources).

## Reference index

| File                                                                   | Covers                                                                                                                                |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| [`references/versions.md`](references/versions.md)                     | The 1.0 Final and the Implementer's Draft, what changed between them, the upgrade checklist, and why no preview is listed             |
| [`references/information-model.md`](references/information-model.md)   | Subject, Resource, Action, Context, Decision and decision context, with JSON examples                                                 |
| [`references/evaluation-apis.md`](references/evaluation-apis.md)       | Access Evaluation and Access Evaluations, defaults, `evaluations_semantic`, per-item errors, PEP and PDP sketches                     |
| [`references/search-apis.md`](references/search-apis.md)               | Subject, Resource and Action Search, search semantics, pagination, the response shape                                                 |
| [`references/metadata-transport.md`](references/metadata-transport.md) | PDP metadata and discovery, `signed_metadata`, the HTTPS JSON binding, default paths, errors, `X-Request-ID`, security considerations |
| [`references/conformance.md`](references/conformance.md)               | Certification levels, the required fixture, search fixture, transport and discovery requirements, interop vectors                     |

## Related skills

- `openid`: the umbrella skill that routes between the OpenID Foundation specifications. `npx skills add ScaleDockHQ/scaledock-skills --skill openid`
- `oauth`: OAuth-based authentication of the PEP to the PDP. `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`
- `jwt`: JWS and JWT processing for `signed_metadata`. `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`
- `rego`: writing PDP policies in Rego for Open Policy Agent. `npx skills add ScaleDockHQ/scaledock-skills --skill rego`
- `openfga`: a relationship-based (Zanzibar-style) PDP model. `npx skills add ScaleDockHQ/scaledock-skills --skill openfga`
- `cel`: PDP conditions written as Common Expression Language expressions. `npx skills add ScaleDockHQ/scaledock-skills --skill cel`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Authorization API 1.0](https://openid.net/specs/authorization-api-1_0.html): Final, 1.0 (published 11 January 2026), checked 2026-10-05.
- [Authorization API 1.0 – draft 01](https://openid.net/specs/authorization-api-1_0-01.html): Implementer's Draft (superseded by the Final), draft 01 (6 September 2024; approved as Implementer's Draft November 2024), checked 2026-10-05.
- [Authorization API 1.0 – draft 02](https://openid.net/specs/authorization-api-1_0-02.html): Working group draft (superseded by the Final), draft 02 (23 January 2025), checked 2026-10-05.
- [Authorization API 1.0 – draft 03](https://openid.net/specs/authorization-api-1_0-03.html): Working group draft (superseded by the Final), draft 03 (18 March 2025), checked 2026-10-05.
- [AuthZEN Working Group – Specifications](https://openid.net/wg/authzen/specifications/): Publisher index, as published, checked 2026-10-05.
- [Authorization API current editors' draft](https://openid.github.io/authzen/): Editors' draft, titled Authorization API 1.0 and dated 5 October 2026; text identical to the Final apart from date and status, checked 2026-10-05.
- [AuthZEN Authorization API 1.0 Certification Scenario](https://raw.githubusercontent.com/openid/authzen/b304f68cb206e8be3dfde093142005296582c509/certification/authorization-api-1_0-scenario.md): Working group draft, commit b304f68 (1 October 2026), checked 2026-10-02. Draft posture: build when targeting certification, otherwise track, pinned to commit b304f68.
- [AuthZEN interop scenarios and test vectors](https://github.com/openid/authzen/tree/b304f68cb206e8be3dfde093142005296582c509/interop): Working group repository, non-normative, commit b304f68 (1 October 2026), checked 2026-10-02.
