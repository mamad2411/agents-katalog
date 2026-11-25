---
name: openadr
description: >-
  OpenADR 3: build demand response and dynamic pricing APIs between a VTN and VENs from the OpenADR 3 OpenAPI definition. Covers OpenADR 3.1.0 (current) and 3.0.1 (supported), with 3.0.0 and OpenADR 2.0b as legacy; only the public OpenAPI YAML and enumeration schemas are pinned, not the Definition or User Guide. Use when implementing or calling a VTN, a VEN or business logic client: programs, events, reports, subscriptions, vens and resources, the OAuth2 client credentials token endpoint, webhook or MQTT notifiers. Triggers: OpenADR, OpenADR 3, VTN, VEN, demand response API, openadr3.yaml, PRICE event, intervalPeriod.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OpenADR 3

OpenADR 3 is the OpenADR Alliance's REST API between a Virtual Top Node (VTN) and Virtual End Nodes (VENs) and business logic (BL) clients for demand response and price signals. This skill reads the OpenAPI definition `openadr3.yaml` and the Alliance's enumeration schemas.

**Scope.** The OpenADR Alliance hands out the Definition and User Guide only after account registration. This skill pins only the machine-readable parts: the OpenAPI YAML (which declares the Apache License 2.0 in its `info.license`), taken from the `grid-coordination/openadr3-specification` public copy at a fixed commit, and the Alliance's own `oadr3-org/openadr3-schemas` enumeration repository. Behaviour that the YAML defers to the User Guide (`See User Guide`) is out of scope; read the Alliance documents for it.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: VTN (server), VEN client, or business logic (BL) client.
- Target version: OpenADR 3.1.0 (current); OpenADR 3.0.1 (supported); OpenADR 3.0.0 (legacy); OpenADR 2.0b (legacy). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **`securitySchemes.oAuth2ClientCredentials` scopes.** "read_targets: VENs may only read objects with targets by providing matching targets"
2. **`securitySchemes.oAuth2ClientCredentials` scopes.** "read_ven_objects: VENs may only read objects whose clientID matches their own"
3. **`securitySchemes.oAuth2ClientCredentials` scopes.** "write_programs: Only BL can write to programs"
4. **`securitySchemes.oAuth2ClientCredentials` scopes.** "write_reports: only VENs can write to reports"
5. **`clientCredentialRequest.grant_type`.** "OAuth2 grant type, must be 'client_credentials'"
6. **`subscription.objectOperations.bearerToken`.** "To avoid custom integrations, callback endpoints should accept the provided bearer token to authenticate VTN requests."
7. **`notifiersResponse.WEBHOOK`.** "'Currently MUST be true'"
8. **`objectID`.** "URL safe VTN assigned object ID."
9. **`dateTime`.** "datetime in RFC 3339 format"
10. **`duration`.** "duration in ISO 8601 format"

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Every endpoint enforces the OAuth2 scope listed for it in `openadr3.yaml`, and VEN reads are filtered by `clientID` or matching targets.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `openapi`, `oauth`, `problem-details`, `mqtt`, `standard-webhooks`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenADR 3.1.0 OpenAPI definition (openadr3.yaml)](https://raw.githubusercontent.com/grid-coordination/openadr3-specification/17b91725e0f07203574ddc946e28def31cb11e44/3.1.0/openadr3.yaml): OpenADR Alliance Final Specification, public copy, OpenADR 3.1.0, mirror commit 17b9172, checked 2026-10-06.
- [OpenADR 3.0.1 OpenAPI definition (openadr3.yaml)](https://raw.githubusercontent.com/grid-coordination/openadr3-specification/17b91725e0f07203574ddc946e28def31cb11e44/3.0.1/openadr3.yaml): OpenADR Alliance release, public copy, OpenADR 3.0.1, mirror commit 17b9172, checked 2026-10-06.
- [OpenADR 3 enumeration schemas: event interval payloads](https://raw.githubusercontent.com/oadr3-org/openadr3-schemas/80b67b43e698a70256ae76298935396b3c9fe13e/OpenADR_Alliance/event-interval-payloads.schema.yaml): OpenADR Alliance repository, oadr3-org/openadr3-schemas commit 80b67b4, 2026-10-05, checked 2026-10-06.
