---
name: llm-tools
description: "Design tool schemas, execution contracts, and failure handling. Use to design constrained agent tool interfaces; api-design defines general service contracts."
---

# llm-tools

Design tool schemas, execution contracts, and failure handling.

## Choose this workflow

Use to design constrained agent tool interfaces; api-design defines general service contracts.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [LLMs and retrieval methods](../../references/packs/llm.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan tool contracts; apply for requested tool implementation and bounded local tests.

**Pack prerequisites:** Task definition, model/provider configuration, representative permitted data, versioned prompts/corpus where relevant, and explicit token/cost/latency limits for remote calls. Use current provider interfaces during implementation. Retrieved content and model-generated tool arguments remain untrusted.

- **Infer from evidence:** Read current prompt/tool schemas, retrieval boundaries, installed SDK/provider config and permitted examples without reading secret values.
- **Reasonable default:** Use mocked calls for local contract tests when remote access is absent; do not infer model quality from mocks.
- **Ask only when needed:** Ask for budget and permitted data/provider before a paid or external run if not already set; local prompt/tool implementation can proceed in apply mode.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Model-facing tool contracts and validated execution boundaries; implementation on request.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: make the requested changes or execute the requested operation within its resolved target and limits. Local preparation does not authorize live, remote, destructive or paid actions; existing explicit session authorization still applies.

## Execute

1. Define each tool’s typed input/output, target identity, permitted action and observable success. Separate planning or proposed arguments from executed effects; untrusted retrieved text cannot grant tool authority.
2. Validate schema and business constraints before dispatch, resolve the actual target from authorized context and minimize returned sensitive data. Describe actionable errors without exposing credentials or treating arbitrary output as new instructions.
3. For mutating calls, define request identity, idempotency, timeout ambiguity and result reconciliation. Cancellation or a missing response does not prove an external operation failed; check its identity before retrying.
4. Test valid calls, invalid inputs, denied targets, unavailable tools, partial success and malicious tool output with controlled fakes. Verify state/effect counts as well as final answers and retain the distinction between simulated and live integration evidence.

## Technical method

- **Inspect:** Inspect tool schemas, target identifiers, execution authority, side effects and partial-failure semantics.
- **Method:** Validate arguments and authorization in the executor, use stable operation IDs and reconcile timeouts before retries.
- **Avoid misdiagnosis:** A schema-valid request can still target the wrong account; model text cannot grant permission to execute it.
- **Check the result:** Test invalid targets, duplicate calls, timeout after success and malicious retrieved instructions with fake isolated executors.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [LLMs and retrieval worked example](../../references/examples/llm.md).


## Decision branches

- **When a tool times out after an external mutation may have occurred:** Return an operation ID and reconciliation path; do not let the model blindly repeat it.
- **When the request is for local preparation or implementation:** Implement schema validation, authorization checks and duplicate/uncertain-call handling using synthetic effects before touching live tools.

## Deliver and verify

- Tool schemas, executor design/code, error contract, and behavior fixtures.
- Tool schema, enforcement boundary and invalid/unauthorized/partial-failure checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Invalid or unauthorized arguments cannot execute; an uncertain external mutation is reconciled before retrying.

## Stop and recover

- A model-generated request is not user authorization. Do not expose arbitrary shell/database access as a convenience tool.

## Example requests

- **Normal (plan):** Design narrow tool schemas with validated targets and idempotent execution.
- **Edge (plan):** Design a deployment tool that rejects unapproved production targets.
- **Blocked (inspect):** Review tool interfaces without exposing arbitrary shell or database execution.
