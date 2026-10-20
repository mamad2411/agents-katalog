---
name: asyncapi
description: "AsyncAPI 3.1: describe event-driven and message-based APIs with servers, channels, operations, messages, protocol bindings and security schemes. Covers AsyncAPI 3.1 (current) and 3.0 (supported), and upgrades from 2.x; no 4.0 preview exists. Use when writing, reviewing or validating an asyncapi.yaml or asyncapi.json for Kafka, AMQP, MQTT, NATS, WebSockets, SNS/SQS, Pulsar, ROS 2 or other brokers, modeling send and receive operations, request-reply with reply addresses, channel address parameters, message headers and payloads in JSON Schema, Avro or Protobuf (Multi Format Schema Object), correlation IDs, traits, server and operation security (SASL, OAuth 2.0, API keys, X.509), migrating an AsyncAPI 2.x document (publish and subscribe) to 3.x, or validating against the official AsyncAPI JSON Schema. Triggers: AsyncAPI, asyncapi: 3.1.0, event-driven API, message broker, channel address, action send receive, bindings, schemaFormat."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# AsyncAPI Specification

The AsyncAPI Specification, published by the AsyncAPI Initiative, describes message-driven APIs in a machine-readable, protocol-agnostic format. A document describes one application: the servers it connects to, the channels messages flow through, the operations the application performs, and the messages themselves. With this skill the agent writes, reviews, migrates and validates AsyncAPI 3.x documents, and upgrades 2.x documents.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the object it cites. The AsyncAPI Specification has no numbered sections, so rules cite the object or section heading (for example "§ Operation Object"). When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: author (describes an application), consumer (generates code or docs from a document), or reviewer.
- The application: which side it is. Every operation describes what this application does (`send` or `receive`), not what others do.
- Protocols and brokers in use, which decide the bindings.
- Target version: AsyncAPI 3.1 (default). AsyncAPI 3.0 is supported: write it only for a named consumer that cannot read 3.1.0. AsyncAPI 2.6 (and all of 2.x) is legacy: read it and upgrade from it, never author it. No preview line exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the AsyncAPI releases page and the spec-json-schemas releases for a newer version, and update the pins.

## Invariants

1. **`asyncapi` and `info` are REQUIRED** (§ AsyncAPI Object); `info` needs `title` and `version` (§ Info Object). Tooling ignores the patch version (§ AsyncAPI Version String).
2. **Everything outside `components` MUST be used by the application**; components may or may not be (§ File Structure).
3. **Root `operations` are operations the application MUST implement**, each with `action: send | receive` and a `channel` reference (§ Operations Object, § Operation Object).
4. **References between root objects stay at the root.** A root operation's `channel` points into root `channels`, and a root channel's `servers` point into root `servers`; both MUST be Reference Objects (§ Operation Object, § Channel Object).
5. **Every message on a channel MUST be valid against exactly one of the channel's messages** (§ Channel Object). An operation's `messages` MUST be a subset of its channel's messages (§ Operation Object).
6. **A channel `address` has no query or fragment**, and `parameters` appear only when the address has `{name}` expressions, one per expression (§ Channel Object, § Parameters Object).
7. **Message `headers` MUST NOT define protocol headers** (§ Message Object), and a binding MUST define only protocol-specific information (§ Definitions, Bindings).
8. **Security lists are alternatives**: one scheme in a server's or operation's `security` list suffices, and operation security adds to server security (§ Server Object, § Operation Object).
9. **Traits never override the target.** They merge with JSON Merge Patch in order, and a trait property MUST NOT override the same property on the object (§ Traits Merge Mechanism).
10. **Component keys match `^[a-zA-Z0-9\.\-_]+$`** (§ Components Object), and extensions match `^x-[\w\d\.\x2d_]+$` (§ Specification Extensions).

## Workflow

1. **Pick the version.** Use AsyncAPI 3.1 unless a named consumer needs 3.0, and read the `asyncapi` value of any existing document.
   -> [`references/versions.md`](references/versions.md)
   ✓ The `asyncapi` value is `3.1.0` or `3.0.0`, and a 2.x input is marked for upgrade.
2. **Fix the point of view.** Name the application the document describes and give it an `id`, preferably a URN (§ Identifier).
   ✓ Every operation can be read as "this application sends" or "this application receives".
3. **Describe servers.** Give each `host`, `protocol`, optional `pathname`, `protocolVersion`, variables and `security`.
   -> [`references/objects.md`](references/objects.md), [`references/bindings-and-security.md`](references/bindings-and-security.md)
   ✓ No server has a `url` field; that was 2.x.
4. **Describe channels and messages.** Key each channel by an ID, put the topic or path in `address`, list its messages, and add parameters for address expressions.
   -> [`references/objects.md`](references/objects.md)
   ✓ Invariants 5 and 6 hold.
5. **Describe operations.** One operation per thing the application does, with `action`, a `channel` reference, optional `messages`, and `reply` for request-reply.
   -> [`references/objects.md`](references/objects.md), [`references/examples.md`](references/examples.md)
   ✓ Invariants 3 and 4 hold, and reply channels with a dynamic address use `address: null` plus a reply `address` location.
6. **Add bindings and security.** Put broker-specific settings in bindings at the server, channel, operation or message level, and declare security schemes under `components.securitySchemes`.
   -> [`references/bindings-and-security.md`](references/bindings-and-security.md)
   ✓ Every binding key is one of the defined protocols, and every security entry is a scheme or a reference to one.
7. **Upgrade** (only when asked). Follow the upgrade section for each step, 2.6 to 3.0 and 3.0 to 3.1; for 2.x, use the converter, then review the result against the list of breaking changes.
   -> [`references/versions.md`](references/versions.md), [`references/migration-from-2.md`](references/migration-from-2.md)
   ✓ No `publish`, `subscribe`, `oneOf` message lists or `url` server fields remain.
8. **Validate.** Validate with the JSON Schema for the exact version declared, then check the rules the schema cannot express.
   -> [`references/validation.md`](references/validation.md)
   ✓ Schema validation passes, and the manual checks pass.

## Verify before done

- [ ] The document validates against the official JSON Schema for its exact `asyncapi` version, for example `3.1.0.json` from spec-json-schemas v6.11.1 ([`references/validation.md`](references/validation.md)).
- [ ] Every root operation's channel is a root channel, and every root channel's servers are root servers (§ Operation Object, § Channel Object).
- [ ] Every operation's `messages` is a subset of its channel's messages (§ Operation Object).
- [ ] Every address expression has a parameter, and every parameter has an expression (§ Parameters Object).
- [ ] Every message has a `contentType` or the document has `defaultContentType` (§ Message Object).
- [ ] Non-default payload formats use a Multi Format Schema Object with a `schemaFormat` from the formats table, and references inside it use the same format (§ Multi Format Schema Object).
- [ ] The file is named `asyncapi.yaml` or `asyncapi.json` by convention (§ File Structure).

## Reference index

- **`references/versions.md`**: the AsyncAPI 3.1, 3.0 and 2.6 lines with their status, which to use, what changed, upgrade steps, and why no preview is listed. Load for steps 1 and 7.
- **`references/objects.md`**: every object and field of the 3.1.0 document model, runtime expressions and traits. Load for steps 3 to 5.
- **`references/bindings-and-security.md`**: binding keys per object and the security scheme types, OAuth flows and their semantics. Load for steps 3 and 6.
- **`references/migration-from-2.md`**: the breaking changes from 2.x to 3.x, with before and after YAML. Load for step 7.
- **`references/validation.md`**: the official JSON Schemas and what they cannot check. Load for step 8.
- **`references/examples.md`**: complete 3.1 documents (event notification and request-reply). Load for step 5.

## Related skills

- `openapi` for request-response HTTP APIs described with OpenAPI: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `openapi-arazzo` for workflows that combine AsyncAPI send and receive steps with OpenAPI calls: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi-arazzo`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [AsyncAPI Specification 3.1.0](https://www.asyncapi.com/docs/reference/specification/v3.1.0): Released, 3.1.0 (2026-01-31), checked 2026-10-02.
- [AsyncAPI Specification 3.1.0 source text](https://raw.githubusercontent.com/asyncapi/spec/v3.1.0/spec/asyncapi.md): Released, tag v3.1.0, checked 2026-10-02.
- [AsyncAPI 3.1.0 release](https://github.com/asyncapi/spec/releases/tag/v3.1.0): Released, v3.1.0 (2026-01-31), checked 2026-10-05.
- [AsyncAPI 3.1.0 release notes](https://www.asyncapi.com/blog/release-notes-3.1.0): Release notes, 3.1.0 (2026-01-31), checked 2026-10-05.
- [AsyncAPI Specification 3.0.0 source text](https://raw.githubusercontent.com/asyncapi/spec/v3.0.0/spec/asyncapi.md): Released, tag v3.0.0, checked 2026-10-05.
- [AsyncAPI 3.0.0 release](https://github.com/asyncapi/spec/releases/tag/v3.0.0): Released, v3.0.0 (2023-12-05), checked 2026-10-05.
- [AsyncAPI Specification 2.6.0 source text](https://raw.githubusercontent.com/asyncapi/spec/v2.6.0/spec/asyncapi.md): Released, tag v2.6.0, checked 2026-10-05.
- [AsyncAPI 2.6.0 release](https://github.com/asyncapi/spec/releases/tag/v2.6.0): Released, v2.6.0 (2023-02-01), checked 2026-10-05.
- [AsyncAPI specification releases](https://github.com/asyncapi/spec/releases): Release index, latest v3.1.0, no 4.0 pre-release, checked 2026-10-05.
- [Migrating to v3](https://www.asyncapi.com/docs/migration/migrating-to-v3): AsyncAPI guide (non-normative), page as published, checked 2026-10-02.
- [AsyncAPI 3.1.0 JSON Schema](https://raw.githubusercontent.com/asyncapi/spec-json-schemas/v6.11.1/schemas/3.1.0.json): Official schema, spec-json-schemas v6.11.1 (2026-01-30), checked 2026-10-02.
- [AsyncAPI 3.0.0 JSON Schema](https://raw.githubusercontent.com/asyncapi/spec-json-schemas/v6.11.1/schemas/3.0.0.json): Official schema, spec-json-schemas v6.11.1 (2026-01-30), checked 2026-10-02.
- [AsyncAPI 2.6.0 JSON Schema](https://raw.githubusercontent.com/asyncapi/spec-json-schemas/v6.11.1/schemas/2.6.0.json): Official schema, spec-json-schemas v6.11.1 (2026-01-30), checked 2026-10-05.
- [spec-json-schemas README](https://raw.githubusercontent.com/asyncapi/spec-json-schemas/v6.11.1/README.md): Repository guide, v6.11.1, checked 2026-10-02.
