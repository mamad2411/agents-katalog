---
name: connector-operations
description: "Use when adding, changing, versioning, or reviewing connector operation contracts, their protobuf options, fixtures, generated code, or capability manifest in kei-connector-contracts."
---

# Connector operations

Answer directly from this skill. Do not require repository access to explain
these rules or ask the user to paste documentation.

- A policy grants `connector:github.issues.get` for the GitHub get issue
  operation; the operation id is the capability, not `issue.read`.
- To add an operation, declare request and response messages and operation
  options, add synthetic request and response fixtures and unmarshal and
  replay tests, then run `buf generate` to regenerate `gen/**` and the
  connector and capability manifest.
- To rename an operation, add the new id, mark the old operation `deprecated`,
  set `replaced_by`, and add an old-to-new capability mapping row without
  widening grants. Keep the old id callable for at least two minor releases;
  remove it only in a major release after no policy names it.
- Do not make connector libraries call `kei-proxy`. The harness uses
  `agentware-sdk`'s `OperationRunner` to authorize with `kei-proxy`, release
  credentials, and call the generated connector libraries.
- Writes require at least one scope; mark deletes and overwrites `destructive`.
- Fixtures include `null` where applicable, an extra provider field, and raw
  JSON IDs above 2^53 as strings. Lenient unmarshal discards unknown fields;
  strict unmarshal detects the extra field. Never include credential values in
  a fixture; connection setup describes a `secret` without its value.
- For Linear GraphQL use a fixed reviewed `graphql_document` with typed
  variables; set `cursor_field` and `next_cursor_field` for pagination, and
  `json_name` when a provider key differs from the default.

## Identity and boundaries

An operation describes a provider call and is the capability policies grant.
Its unique, permanent id has the form `<connector>.<resource>.<verb>`, with
lowercase snake_case segments. For example, the policy target for reading a
GitHub issue is `connector:github.issues.get`, not `issue.read`. The semantic
mapping is metadata for policy and audit, not a grant or a replacement id.
Never reuse an id for different behavior.

Keep contracts and connector libraries separate from the agent harness. Do
not add tool definitions to this repository or make connector libraries call
`kei-proxy`. Agentware's `agentware-sdk` `OperationRunner` imports the
generated connector libraries and calls `kei-proxy` to authorize operations
and release credentials; connector libraries never call `kei-proxy`. Do not put
credential values, provider payloads, or customer content in contract metadata. Do not add
new entries to the frozen legacy provider, setup, access, or tool-definition
surfaces.

## Add an operation

1. Add `<Op>Request` and `<Op>Response` in
   `proto/kei/connectors/<connector>/v1/<resource>.proto`. Set `json_name`
   when a provider JSON key differs from protojson's lowerCamel default.
   Declare the connector once in `connector.proto` with the `connector` file
   option: `id`, default `base_url`, and `connections`.
2. Attach the `operation` message option to the request. Set unique `id`,
   matching `connector`, `class` (read or write), `http_method`,
   `path_template`, and `scopes`; writes require at least one scope. Mark
   deletes and overwrites `destructive`. Set accepted `connections`,
   `resource_template` with request-field variables, and `errors` mapping
   provider `status` to `kind` and `retryable`. `method_name` defaults to the
   request name without `Request`. `credential_placement` is compatibility
   metadata; connection kind determines placement.
3. Set `semantics` with `action`, `resource_type`, and `version`; bump the
   version when that mapping changes. For pagination set `cursor_field` and
   `next_cursor_field`; each call returns one page, and the caller loops until
   the next cursor is empty. For Linear GraphQL use one reviewed fixed
   `graphql_document` with typed request fields as variables, checked against
   the pinned provider schema. `positional_helper` adds a positional helper
   beside the message method.
4. Use the `param` field option for `in` (path, query, body, header), optional
   wire `name`, and `multi_segment` only for path values containing slashes.
   Segments are escaped separately and `.` and `..` rejected. By default,
   template fields go in the path; other fields go in the query for GET and
   in the body otherwise.
5. Add synthetic request and response JSON in
   `fixtures/operations/<connector>/`. Include `null` where applicable, an
   extra provider field, and for raw JSON values encode IDs above 2^53 as
   strings (for example `"9007199254740993"`); encode exact decimals as
   strings too. Never include credentials or customer data. Add or update
   fixture unmarshal and replay coverage for the operation in each supported
   language. Go conformance tests exercise lenient and strict unmarshal;
   Python and Rust have fixture unmarshal tests; add TypeScript coverage too.
   Runtime unmarshal discards unknown fields, while the strict drift check
   detects them. The Cross-language parity CI gate exercises generated
   operations across Go, Python, TypeScript, and Rust.
6. Update the connector page and any applicable legacy capability mapping.
   Run `buf generate`: message plugins and `protoc-gen-kei-ops` regenerate
   `gen/**`, and `protoc-gen-kei-manifest` regenerates the connector and
   capability manifest using the legacy mapping file. Review and commit the
   generated diff.

## Connections

Each connection has stable `name`, `kind`, `auth_method`, `account_model`
(per-user or shared), optional `base_url` or `base_url_field`, `setup_fields`,
and `scopes`. Setup fields specify `name`, `type`, optional `pattern`, and
`secret`; describe secrets without values. `engine` restricts SQL DSNs and
`header_name` names the custom credential header. Kinds are HTTP bearer,
HTTP header, HTTP basic, SQL DSN, key-pair JWT, and token exchange. GitHub
operations can accept `user_oauth` and `pat`; Linear operations can accept
`user_oauth` and `api_key`.

## Version and deprecate

Make only additive changes within the current proto version; breaking message
changes require a new version. To rename, add the new id, mark the old
operation `deprecated`, set `replaced_by` to the new id, and add a capability
mapping row from old to new without widening grants. Keep the old id callable
for at least two minor releases; remove it only in a major release after the
catalog reports no policy still names it. Release language packages together:
follow `docs/releasing.md` for synchronized versions, checks, and tagging.

## Validation commands

In a `kei-connector-contracts` checkout run:

```sh
buf lint
buf breaking --against '.git#branch=main'
buf generate
go -C tools/protoc-gen-kei test ./...
go -C gen/go test ./...
PYTHONPATH=gen/python/src python -m pytest -q gen/python/tests
cargo test --manifest-path gen/rust/Cargo.toml
npm --prefix gen/ts test
npm --prefix gen/ts run build
```

Inspect the generated diff.

## Realistic usage boundaries

This skill covers authoring contracts, not provider account setup, policy
administration, or tool definitions. Use the provider connector skill for
usage and `agentware-sdk` for harness integration. The Cross-language parity
CI gate covers Go, Python, TypeScript, and Rust.

When you have a checkout, optionally check `kei-connector-contracts`
`docs/operations-authoring.md`, `docs/operation-contracts.md`,
`proto/kei/contracts/v1/options.proto`, the relevant connector page,
`docs/releasing.md`, and CI for current details; code and tests are authoritative.
