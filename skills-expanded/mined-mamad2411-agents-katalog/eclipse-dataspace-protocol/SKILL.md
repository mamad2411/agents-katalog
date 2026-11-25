---
name: eclipse-dataspace-protocol
description: >-
  Dataspace Protocol: interoperable data sharing with usage control. Covers Dataspace Protocol 2025-1. Use when publishing or negotiating access to a dataset. Triggers: Dataspace Protocol, DSP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Dataspace Protocol

Dataspace Protocol 2025-1, a stable release published 12 August 2025. The scope says it specifies how datasets are advertised in catalogs, how usage requirements are expressed as policies, how agreements are negotiated, and how datasets are accessed. It does not apply to the data transfer protocol.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text when publishing a dataset or negotiating an agreement in a dataspace.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: a provider or a consumer.
- Target version: Dataspace Protocol 2025-1 (current) — default. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **text.** "The [=Catalog Service=] MUST respond with a [Catalog](#ack-catalog) that adheres to the schema linked above."
2. **text.** "The [=Catalog Service=] MUST respond with a [Dataset](#ack-dataset) that adheres to the schema linked above."
3. **text.** "(_NOTE: Since a Catalog may be dynamically generated for a request based on the requesting [=Participant=]'s credentials, it is possible for it to contain 0 matching [=Datasets=]._) - A [=Catalog=] MUST have one to many [=Data Services=] that reference a [=Connector=] where [=Datasets=] MAY be obtained."
4. **text.** "In case the states differ, the [=Contract Negotiation=] MUST be terminated and a new [=Contract Negotiation=] MAY be initiated."
5. **text.** "If the message includes a `providerPid` property, the request MUST be associated with an existing [=Contract Negotiation=] and a [=Consumer=] [=Offer=] MUST be created using either the `offer` or `offer.@id` properties."
6. **text.** "Different to a [=Catalog=] or [=Dataset=], the [=Offer=] inside a [Contract Request Message](#contract-request-message) MUST have a `target` attribute."
7. **text.** "The `consumerPid` property MUST refer to the transfer identifier of the [=Consumer=] side."
8. **text.** "The `agreementId` property MUST refer to an existing [=Agreement=] between the [=Consumer=] and [=Provider=]."
9. **text.** "The `dataAddress` MUST contain a transport-specific set of properties for pushing the data."
10. **text.** "Each [=Connector=] MUST provide a version metadata endpoint ending with Uniform Resource Identifier (URI) segments `/.well-known/dspace-version`."
11. **1.1.** "A [=Connector=] MUST respond to a respective HTTPS request by returning a [`VersionResponse`](#VersionResponse-table) with at least one item."
12. **text.** "Each Connector MUST provide a version metadata endpoint ending with Uniform Resource Identifier (URI) segments `/.well-known/dspace-version`."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Dataspace Protocol 2025-1](https://eclipse-dataspace-protocol-base.github.io/DataspaceProtocol/2025-1/): Release, 2025-1, published 12 August 2025, checked 2026-10-06.
- [Scope](https://raw.githubusercontent.com/eclipse-dataspace-protocol-base/DataspaceProtocol/2025-1/specifications/common/scope.md): Specification, tag 2025-1, checked 2026-10-06.
- [Catalog protocol](https://raw.githubusercontent.com/eclipse-dataspace-protocol-base/DataspaceProtocol/2025-1/specifications/catalog/catalog.protocol.md): Specification, tag 2025-1, checked 2026-10-06.
- [Contract negotiation protocol](https://raw.githubusercontent.com/eclipse-dataspace-protocol-base/DataspaceProtocol/2025-1/specifications/negotiation/contract.negotiation.protocol.md): Specification, tag 2025-1, checked 2026-10-06.
- [Transfer process protocol](https://raw.githubusercontent.com/eclipse-dataspace-protocol-base/DataspaceProtocol/2025-1/specifications/transfer/transfer.process.protocol.md): Specification, tag 2025-1, checked 2026-10-06.
- [Common protocol](https://raw.githubusercontent.com/eclipse-dataspace-protocol-base/DataspaceProtocol/2025-1/specifications/common/common.protocol.md): Specification, tag 2025-1, checked 2026-10-06.
