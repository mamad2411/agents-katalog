---
name: openapi-arazzo
description: "Arazzo 1.1: describe and run multi-step API workflows over OpenAPI and AsyncAPI operations, with inputs, steps, success criteria, outputs and retry or goto actions. Covers Arazzo 1.1 (current), 1.0 (supported) and the 1.2 draft with WSDL sources (tracked only). Use when writing, reviewing or executing an arazzo.yaml or arazzo.json, chaining API calls into an end-to-end flow (login then fetch, create then poll), declaring sourceDescriptions of type openapi, asyncapi or arazzo, passing data between steps with runtime expressions ($inputs, $steps, $response.body, $message.payload), writing successCriteria with simple, regex, JSONPath or XPath conditions, adding onSuccess and onFailure actions, using AsyncAPI send and receive steps with correlationId and timeout, upgrading from Arazzo 1.0, or validating against the official Arazzo JSON Schema. Triggers: Arazzo, OpenAPI workflows, arazzo: 1.1.0, workflowId, stepId, successCriteria, operationPath, channelPath, application/vnd.oai.workflows."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Arazzo Specification

The Arazzo Specification, published by the OpenAPI Initiative (OAI), describes sequences of API calls and their dependencies as workflows over one or more source descriptions (OpenAPI, AsyncAPI or other Arazzo documents). With this skill the agent writes, reviews, validates and executes Arazzo Descriptions.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Section numbers are those of Arazzo 1.1.0. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: author (writes the description), executor (a tool, test runner or agent that runs workflows), or reviewer.
- Source descriptions: the OpenAPI and AsyncAPI documents the workflows call, and their `operationId`s.
- Target version: Arazzo 1.1 (default). Arazzo 1.0 is supported: write it only for a named tool that cannot read 1.1. Arazzo 1.2 is a preview (posture: track): never emit it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check [spec.openapis.org/arazzo](https://spec.openapis.org/arazzo/) for a newer version or schema iteration, check the `v1.2-dev` branch for movement, and update the pins.

## Invariants

1. **`arazzo`, `info`, `sourceDescriptions` and `workflows` are REQUIRED**, and both lists have at least one entry (§ 5.8.1.1). Tooling MUST interpret the document by `arazzo` (§ 5.8.1.1).
2. **`workflowId` is unique in the description and `stepId` is unique in its workflow**; both are case-sensitive and SHOULD match `[A-Za-z0-9_\-]+` (§ 5.8.4.1, § 5.8.5.1).
3. **A step targets exactly one of `operationId`, `operationPath`, `channelPath` or `workflowId`** (§ 5.8.5.1). With more than one non-`arazzo` source description, `operationId` MUST be written as `$sourceDescriptions.<name>.<operationId>` (§ 5.8.5.1).
4. **Prefer `operationId` over `operationPath` or `channelPath`** when the target operation has one (§ 5.8.5.1).
5. **Every `successCriteria` entry MUST pass** for the step to succeed, and the list is non-empty when present (§ 5.8.5.1, § 5.8.11.4.6).
6. **Defaults: success goes to the next step, failure ends the workflow** (§ 5.8.5.1). The first matching action in order is executed (§ 5.8.5.1).
7. **Operation step parameters set `in`**; with a `workflowId` step, parameters map to the target workflow's inputs (§ 5.8.6.1).
8. **Steps run in an order that satisfies `dependsOn` and every `$steps.<id>.outputs` reference** (§ 5.8.5.2.4). In a sequential workflow, a reference to a later step's outputs is an error (§ 5.8.5.2.5).
9. **Workflows from other Arazzo documents are listed in `sourceDescriptions`** (§ 5.3) and referenced by `$self` when the target has one (§ 5.5.2).
10. **Processing a description can perform unsafe operations on arbitrary hosts**; the consumer must make sure they are not harmful (§ 6).

## Workflow

1. **Pick the version.** Use Arazzo 1.1 unless a named tool needs 1.0, and read the `arazzo` value of any existing description.
   -> [`references/versions.md`](references/versions.md)
   ✓ The `arazzo` value is `1.1.0` or `1.0.1`, never `1.2.0`, and no feature newer than that value is used.
2. **List the source descriptions.** Give each a `name`, `url` and `type` (`openapi`, `asyncapi` or `arazzo`). API URLs come from the source description's servers, not from the Arazzo document (§ 5.7).
   -> [`references/objects.md`](references/objects.md)
   ✓ Every operation the workflows call resolves in one of the listed sources.
3. **Define each workflow's contract.** Write `inputs` as JSON Schema 2020-12 and name the `outputs` the caller gets back.
   -> [`references/objects.md`](references/objects.md)
   ✓ Every `$inputs.*` used in steps is declared in `inputs`.
4. **Write the steps.** Point each at one operation or workflow, pass parameters and a request body with runtime expressions, and expose the values later steps need as `outputs`.
   -> [`references/expressions.md`](references/expressions.md), [`references/examples.md`](references/examples.md)
   ✓ Invariants 2, 3, 7 and 8 hold.
5. **Say what success means.** Add `successCriteria` to every step that can return more than one outcome, and to every AsyncAPI receive step.
   -> [`references/expressions.md`](references/expressions.md), [`references/asyncapi-steps.md`](references/asyncapi-steps.md)
   ✓ Each criterion with a `type` also has a `context` (§ 5.8.11.5).
6. **Handle the other paths.** Add `onFailure` retries with `retryAfter` and `retryLimit` for transient errors, `goto` for branches, and workflow-level actions for shared handling. Factor repeats into `components`.
   -> [`references/execution.md`](references/execution.md)
   ✓ Every retry has a limit, and every `goto` target exists in the same workflow or is a resolvable `workflowId`.
7. **Validate.** Validate against the official Arazzo schema for the declared version, then check what the schema cannot.
   -> [`references/validation.md`](references/validation.md)
   ✓ Schema validation passes, and every reference resolves.
8. **Execute safely** (executor role). Run steps in dependency order, evaluate criteria as specified, and treat the description as untrusted input.
   -> [`references/execution.md`](references/execution.md)
   ✓ No step runs against a host or operation the operator has not approved.
9. **Upgrade** (only when asked). Follow the upgrade section from the declared version to the target, one minor at a time.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded description validates against the target schema and runs the same steps with the same data.

## Verify before done

- [ ] The description validates against the schema for its declared version, for Arazzo 1.1 iteration 2026-04-15 ([`references/validation.md`](references/validation.md)).
- [ ] Nothing from the Arazzo 1.2 draft is emitted: no `arazzo: 1.2.0`, `type: wsdl` or `operationName`.
- [ ] Every `operationId`, `operationPath`, `channelPath` and `workflowId` resolves in a listed source description (§ 5.8.5.1).
- [ ] Every runtime expression matches the ABNF in § 5.9, and every referenced step output exists on an earlier or `dependsOn` step (§ 5.8.5.2).
- [ ] Every component key matches `^[a-zA-Z0-9\.\-_]+$` (§ 5.8.9.1), and every Reusable Object `reference` points to an existing component (§ 5.8.10).
- [ ] Every AsyncAPI step sets `action`, and every receive step has `successCriteria` or meets both conditions for omitting it (§ 5.8.5.3).
- [ ] The entry document is named `arazzo.yaml` or `arazzo.json` (RECOMMENDED, § 5.3).

## Reference index

- **`references/versions.md`**: the Arazzo 1.2, 1.1 and 1.0 lines with their status, which to use, what changed, upgrade steps and the 1.2 preview. Load for steps 1 and 9.
- **`references/objects.md`**: every object and field: root, Info, Source Description, Workflow, Step, Parameter, Success and Failure Actions, Components, Reusable Object. Load for steps 2 to 4.
- **`references/expressions.md`**: runtime expressions, Criterion conditions and their evaluation, Selector, Expression Type, Request Body and Payload Replacement Objects. Load for steps 4 and 5.
- **`references/asyncapi-steps.md`**: send and receive steps, `channelPath`, `correlationId`, `timeout`, and asynchronous success. Load for step 5.
- **`references/execution.md`**: execution order, action semantics, retries, and security for executors. Load for steps 6 and 8.
- **`references/validation.md`**: the official schemas per version and what a schema cannot check. Load for step 7.
- **`references/examples.md`**: complete workflows in YAML. Load for step 4.

## Related skills

- `openapi` for the OpenAPI descriptions that steps call: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `asyncapi` for the AsyncAPI descriptions that send and receive steps use: `npx skills add ScaleDockHQ/scaledock-skills --skill asyncapi`.
- `openapi-overlay` to add `operationId`s or other fields to a source description you cannot edit: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi-overlay`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Arazzo Specification v1.1.0](https://spec.openapis.org/arazzo/v1.1.0.html): Released, 1.1.0 (2026-05-17), checked 2026-10-02.
- [Arazzo 1.1.0 release notes](https://github.com/OAI/Arazzo-Specification/releases/tag/1.1.0): Released, 1.1.0 (tagged 2026-05-18), checked 2026-10-05.
- [Arazzo Specification v1.0.1](https://spec.openapis.org/arazzo/v1.0.1.html): Released, 1.0.1 (2025-01-16), checked 2026-10-05.
- [Arazzo 1.0.1 release notes](https://github.com/OAI/Arazzo-Specification/releases/tag/1.0.1): Released, 1.0.1 (tagged 2025-01-20), checked 2026-10-05.
- [Arazzo versions and schema iterations](https://spec.openapis.org/arazzo/): OAI index, latest v1.1.0, checked 2026-10-02.
- [Arazzo 1.1 JSON Schema](https://spec.openapis.org/arazzo/1.1/schema/2026-04-15): Published schema, iteration 2026-04-15, checked 2026-10-02.
- [Arazzo 1.0 JSON Schema](https://spec.openapis.org/arazzo/1.0/schema/2025-10-15): Published schema, iteration 2025-10-15, checked 2026-10-02.
- [Arazzo `v1.2-dev` branch text](https://raw.githubusercontent.com/OAI/Arazzo-Specification/6e089558f8a4eebe81162010b3d46842c8fb9892/src/arazzo.md): In development, commit 6e08955 (2026-09-30), draft posture: track, checked 2026-10-05.
- [RFC 9535: JSONPath: Query Expressions for JSON](https://www.rfc-editor.org/rfc/rfc9535): RFC (Proposed Standard), RFC 9535, checked 2026-10-02.
