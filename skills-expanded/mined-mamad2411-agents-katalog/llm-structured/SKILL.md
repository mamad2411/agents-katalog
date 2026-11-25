---
name: llm-structured
description: "Implement structured outputs, validation, and recovery. Use for validated structured model output; api-client handles the provider transport boundary."
---

# llm-structured

Implement structured outputs, validation, and recovery.

## Choose this workflow

Use for validated structured model output; api-client handles the provider transport boundary.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [LLMs and retrieval methods](../../references/packs/llm.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; output schema, provider capabilities, validation rules, consumers, and retry budget.

**Pack prerequisites:** Task definition, model/provider configuration, representative permitted data, versioned prompts/corpus where relevant, and explicit token/cost/latency limits for remote calls. Use current provider interfaces during implementation. Retrieved content and model-generated tool arguments remain untrusted.

- **Infer from evidence:** Read current prompt/tool schemas, retrieval boundaries, installed SDK/provider config and permitted examples without reading secret values.
- **Reasonable default:** Use mocked calls for local contract tests when remote access is absent; do not infer model quality from mocks.
- **Ask only when needed:** Ask for budget and permitted data/provider before a paid or external run if not already set; local prompt/tool implementation can proceed in apply mode.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Structured generation, semantic validation, refusal/incomplete handling, and bounded recovery.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Resolve the schema features the provider supports, and define schema-compatible requests.
2. Validate semantics after parsing, separating refusal, truncation, invalid structure and downstream business rejection, and implement constrained retries.
3. Test downstream consumption with malformed, missing, refusal and truncation fixtures.

## Technical method

- **Inspect:** Read the exact schema, provider support, refusal/truncation signals and downstream invariants.
- **Method:** Validate syntax, schema and business constraints separately; bound retries and return typed failure when recovery cannot establish validity.
- **Avoid misdiagnosis:** Valid JSON can contain fabricated IDs or inconsistent totals; filling required fields with invented defaults corrupts meaning.
- **Check the result:** Exercise malformed, schema-valid-but-semantic-invalid, refused and truncated responses alongside a valid control.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [LLMs and retrieval worked example](../../references/examples/llm.md).


## Decision branches

- **When retries repeatedly fail the same constraint:** Stop at the cap with a typed error and retain diagnostics; never fabricate fields to satisfy the schema.

## Deliver and verify

- Structured-output integration with its schema/validation contract, recovery behavior and malformed, missing, refusal and truncation fixtures.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Syntactically valid but semantically invalid output is rejected; repeated failure terminates with a typed error.

## Stop and recover

- Never coerce fabricated fields into valid-looking data. Do not assume every provider supports identical schema features.

## Example requests

- **Normal (apply):** Implement schema validation and bounded recovery for invalid or truncated output.
- **Edge (apply):** Extract records when output parses but contains impossible dates.
- **Blocked (inspect):** Design structured output with unknown provider schema support; avoid assumed API flags.
