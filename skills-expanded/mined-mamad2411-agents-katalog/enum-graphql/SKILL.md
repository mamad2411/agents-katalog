---
name: enum-graphql
description: GraphQL API enumeration covering endpoint discovery, schema introspection, type and field mapping, authentication-requirement classification, and query-depth analysis. Passive-first approach using introspection and documentation; active probing only after authorization and scope validation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft, schema-map, auth-classification]
---

# Enum GraphQL

Use this skill to enumerate GraphQL APIs and map their full surface: endpoints, schema types, fields, mutations, subscriptions, and authentication boundaries. GraphQL consolidates many operations into a single endpoint, so enumeration focuses on discovering what operations are available and which require privilege, rather than finding many endpoints.

## Required inputs

- Validated target with known or suspected GraphQL endpoint paths.
- Scope file defining allowed testing methods and rate limits.
- Authorization cache valid for all in-scope hosts.
- Session tokens at multiple privilege levels, if available, to classify field-level authentication requirements.
- Optional: GraphQL schema file or SDL if provided by the target owner.

## Required gates

1. Use `pentest_agent_load_config` and `pentest_agent_validate_policy` before planning.
2. Use `pentest_agent_parse_scope` and `pentest_agent_validate_target` for every GraphQL endpoint before contact.
3. Use `pentest_agent_check_authorization` before any request that includes credentials.
4. Use `pentest_agent_build_command` for dry-run preview when using catalog tools for GraphQL introspection or endpoint discovery.
5. Use `pentest_agent_execute_tool` for all active probing with rate-limit and output policy enforcement.
6. Use `pentest_agent_append_evidence` for schema maps, type inventories, and auth-classification matrices.

## Workflow

### Phase 1 — Endpoint discovery

Locate every GraphQL endpoint before analyzing any single one.

- Test common GraphQL path prefixes: `/graphql`, `/api/graphql`, `/v1/graphql`, `/v2/graphql`, `/gql`, `/query`, `/graphiql`, `/playground`, `/graphql/v1`, `/api/v1/graphql`, `/__graphql`.
- Send a simple query (`{__typename}`) via POST with `Content-Type: application/json` to each candidate path. A GraphQL response (even an error) confirms the endpoint; an HTML response or 404 suggests the path is not a GraphQL endpoint.
- Also test GET with query parameters: `?query={__typename}`. Some GraphQL servers accept GET for queries and POST for mutations.
- Test WebSocket paths for subscriptions: `wss://TARGET/graphql`, `wss://TARGET/subscriptions`. GraphQL subscriptions use WebSocket transport.
- Test for GraphiQL or Playground IDE exposure: these interactive consoles leak schema details visually and should be flagged even if introspection is disabled.
- Search JavaScript bundles for GraphQL endpoint URLs, Apollo Client configuration, or Relay environment setup that reveals the production endpoint.

### Phase 2 — Schema introspection

Extract the full type system when introspection is enabled.

- Send the standard introspection query to retrieve the schema: `{__schema{types{name kind fields{name args{name type{name kind ofType{name kind}}}}}}}`
- Parse the response to build a type inventory: object types, input types, enums, unions, interfaces, and scalars.
- Extract all query fields and their arguments. This reveals every read operation the API supports.
- Extract all mutation fields and their arguments. This reveals every write, update, and delete operation.
- Extract all subscription fields. This reveals real-time data streams.
- Check for deprecated fields (`isDeprecated: true`). Deprecated fields often remain accessible and may have weaker validation.
- If introspection is disabled, record it and move to Phase 3. Do not attempt to brute-force field names via error-based inference at this stage.

### Phase 3 — Field inference without introspection

When introspection is disabled, use documentation and safe inference.

- Check for the GraphQL SDL (Schema Definition Language) file at common paths: `/schema.graphql`, `/graphql/schema.graphql`, `/api/schema.graphql`.
- Check the GraphiQL or Playground IDE if accessible. The schema tab in GraphiQL loads the full schema even when introspection queries are blocked from external clients.
- Use `__typename` introspection on known objects. If you can obtain a valid query (from documentation, JavaScript, or API docs), add `__typename` to each field to learn the concrete types returned.
- Use field-suggestion errors cautiously. Sending a query with a typo (`{usr{id}}`) may return an error like `Cannot query field "usr"... Did you mean "user"?`. This leaks field names.
- If no schema information is recoverable, document the limitation and request documentation from the target owner. Do not engage in large-scale field-name brute-force.

### Phase 4 — Authentication-requirement classification

Map which fields and mutations require authentication and which do not.

- Send the introspection query or a known valid query without authentication. Record which fields return data and which return errors.
- Send the same queries with a low-privilege authenticated token. Record which previously blocked fields become accessible.
- Send the same queries with an elevated-privilege token, if available. Record which fields require higher privilege.
- Test mutations specifically: an unauthenticated user accessing a mutation that modifies data is a critical finding.
- Test field-level authorization: can a user query `{me{organization{allUsers{email}}}}` — accessing admin-level data through a nested field on an otherwise-accessible object? GraphQL resolvers often skip authorization checks that the parent resolver performed.
- Produce an auth-requirement matrix: type, field, whether accessible unauthenticated, with user token, with admin token.

### Phase 5 — Query-depth and complexity analysis

Assess operational risk from unbounded queries.

- Test the maximum query depth the server accepts. Send a deeply nested query (`{a{b{c{d{e{f{g{h{id}}}}}}}}`) and observe whether the server rejects it with a depth-limit error or processes it.
- Test alias-based batching. Send a query with many aliased fields (`{a1:user(id:1){email} a2:user(id:2){email} ... a100:user(id:100){email}}`). Unbounded alias batching enables brute-force and data scraping.
- Test array-based batching. Send a JSON array of queries in a single POST body. Some servers process them sequentially, enabling rate-limit bypass.
- Test circular fragment references. Send a query with a fragment that references itself. If the server does not detect the cycle, it may enter unbounded recursion.
- Document the query-complexity limits (or lack thereof) as operational findings.

### Phase 6 — Directive and configuration audit

Audit GraphQL-specific configuration that affects security.

- Check for `@skip` and `@include` directive behavior. These should not bypass field-level authorization.
- Check for custom directives (`@auth`, `@hasRole`, `@requirePermission`) in the schema. Document them as authorization hints; test whether they are actually enforced or merely declarative.
- Check whether the server exposes tracing or debug extensions in responses (`extensions: {tracing: {...}}`). Query tracing reveals resolver execution times and internal architecture.
- Check for error-level configuration. Verbose GraphQL errors may leak field names, type information, stack traces, database errors, or internal IP addresses.
- Test whether the server accepts the `application/graphql` content type (non-standard, used by some older clients). Alternate content types sometimes bypass middleware.

## Decision points

- Introspection disabled: if introspection is disabled, GraphiQL is not exposed, and no schema file is available, classification is limited. Prioritize auth testing on known queries from documentation and JavaScript extraction.
- Field-level auth testing: if the schema contains hundreds of fields, test a representative sample: top-level query fields, mutations, and one level of nested object access.
- Query-complexity testing: start with small depth increments (5, 10, 20). Stop increasing depth once the server rejects a query.
- Alias batching: if the server accepts 100+ aliases and returns data, record it as a finding and stop the alias-count escalation.

## Prohibited behavior

No brute-force of GraphQL field names using large wordlists. No exploitation of discovered mutations — this is enumeration, not validation. No creation, modification, or deletion of data during enumeration. No credential guessing via login mutations. No probing of out-of-scope GraphQL endpoints. Do not run raw shell commands when a `pentest_agent_*` gate exists.

## Stop conditions

Stop on an endpoint when the schema is fully mapped, all field auth tiers are classified, and query-depth characteristics are documented. Stop if a mutation is accidentally triggered and modifies data — immediately record the incident as evidence and halt active testing on that endpoint. Stop if the authorization cache expires.

## Evidence

Append evidence via `pentest_agent_append_evidence`:
- Discovered GraphQL endpoint list with response characteristics.
- Schema type inventory (object types, input types, enums, unions) with field counts.
- Query, mutation, and subscription field lists.
- Auth-requirement matrix per field per privilege level.
- Query-depth limit test results.
- Directive inventory and configuration audit notes.

Never store GraphQL responses containing user data, PII, credentials, tokens, or internal identifiers. Redact introspection results that contain internal architecture details before storage.

## Report handoff

Record findings via `pentest_agent_record_finding` for: introspection enabled (high if schema exposes admin mutations), GraphiQL/Playground exposed (medium), missing query-depth limits (medium), unauthenticated mutation access (critical), field-level authorization gaps (high), verbose error messages with stack traces (medium), and query tracing exposed (low). Render the final report with `pentest_agent_render_report`.
