---
name: implement-structured-outputs
description: Implements strict constrained decoding and validation for LLM responses. Use when enforcing JSON Schema guarantees on model generations, eliminating regex parsing, or integrating structured LLM outputs into backend services.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Implement Structured Outputs

Use this skill when integrating LLM responses into application code to guarantee schema adherence and eliminate parsing errors.

## Core Rules

- **No Regex Parsing**: Never use regex to extract JSON from raw LLM output — this is strictly prohibited in production backend pipelines
- **Constrained Decoding First**: Use provider-native constrained decoding (`response_format: { type: "json_schema", strict: true }` for OpenAI/Gemini; XGrammar, Outlines, or SGLang grammar constraints for self-hosted inference) — this guarantees JSON syntax compliance at the token generation layer
- **Contract-First Schema DSL**: Define schemas once in Zod or Pydantic v2 with `strict: true` / `additionalProperties: false`; consider BAML for cross-language type-safe prompt functions; export to JSON Schema 2020-12 for provider compatibility
- **Dual-Layer Runtime Validation**: After constrained decoding, parse through the application-layer validator (`schema.safeParse()` / `TypeAdapter.validate_json()`) to enforce business invariants, enum bounds, and cross-field rules not expressible in JSON Schema
- **Bounded Repair Loops**: On validation failure, inject the exact schema violation diff into a one-turn repair prompt; limit to **maximum 2 retry attempts** before returning a structured domain error — never loop indefinitely
- **Format Tax Mitigation**: Include a `thought_process` or `reasoning` field in the schema before final output fields to preserve model reasoning space under grammar constraints; strip this field before returning to callers
- **Centralized Gateway Routing**: Route all LLM structured output requests through a centralized LLM gateway responsible for token budgeting, provider fallback, rate limiting, and prompt injection filtering

## Suggested Process

### 1. Define Canonical Schema Contract

Create a strict schema definition using Zod or Pydantic:
- Ensure all object properties are explicitly typed and marked as required (or given explicit default values).
- Add field descriptions to guide the LLM's generative decoding.
- Compile or export the definition to a strict JSON Schema object matching OpenAPI / JSON Schema 2020-12 specs.

### 2. Configure Model Provider Constrained Decoding

Wire the schema into the provider-specific SDK call:
- OpenAI: set `response_format: { type: "json_schema", json_schema: { name: "...", strict: true, schema: ... } }`.
- Google Gemini: configure `responseMimeType: "application/json"` and pass `responseSchema`.
- Local / Self-Hosted (vLLM, Ollama): pass guided decoding grammars or JSON Schema constraints.

### 3. Integrate Dual-Layer Runtime Validation

Implement defensive validation around the decoded response:
- Parse the received string payload through the canonical validator (e.g., `schema.safeParse()` or `TypeAdapter.validate_json()`).
- Verify data types, enum bounds, and domain invariant constraints that JSON Schema alone cannot enforce.
- Map validation errors to structured domain error types.

### 4. Implement Error Recovery & Context-Injected Retries

Handle rare edge cases such as token limit truncation or refusal:
- Check for provider refusal signals (`refusal` field or safety finish reasons).
- If validation fails, capture the validation error list and pass it back into a one-turn repair prompt with bounded backoff.
- Set a hard retry ceiling (max 2 retries) before raising a structured error.

### 5. Add Unit & Contract Tests

Use skill: `write-tests`
- Test schema generation and serialization.
- Author unit tests using mock provider responses (valid payload, partial payload, malformed payload, refusal).
- Assert that invalid model responses never reach core business logic without triggering the recovery flow.

## Failure Modes

- **Schema drift from the source spec**: a generated output diverges from the JSON Schema the spec declares. **Mitigation:** validate every output against the source JSON Schema before returning; reject outputs that fail validation.
- **Constrained decoding disabled**: a tool returns free-form text instead of a schema-validated object. **Mitigation:** enforce structured outputs (constrained decoding) at the model gateway; reject free-form responses.
- **Field rename in a future model version**: a model version change renames a field. **Mitigation:** validate every output against the schema; surface the rename in the eval report; update the schema and the prompt.
- **Ungrounded output**: the model returns a value that is not in the source data. **Mitigation:** enforce a grounding check (cosine similarity ≥ 0.7) on retrieval-augmented outputs; surface the ungrounded output as `[UNVERIFIED]`.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/implementation-result.json`** — Required fields: `change_summary`, `files_touched[]`, and `validation_run` output proving the schema validation handles both valid and invalid mock responses.

## Checklist

- [ ] Strict canonical schema defined with Zod/Pydantic without untyped fields.
- [ ] Provider-native constrained decoding parameters configured.
- [ ] Runtime validation layer verifies response payload before business logic.
- [ ] Refusal handling and targeted error-repair retry logic implemented.
- [ ] Unit tests with valid and invalid mock responses written and passing.
- [ ] `implementation-result.json` emitted.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: a malformed or adversarial prompt may try to escape the constrained decoding envelope. Validate every output against the JSON Schema before returning to the caller.
- **ASI04 Supply Chain**: schema validators, constrained decoding libraries, and model SDKs must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct schema, prompts, or constrained-decoding configs from external content without strict validation.
- **ASI07 Inter-Agent Communication**: the structured output is consumed by downstream agents; require schema validation at the boundary.
- **ASI09 Human-Agent Trust Exploitation**: do not present the structured output as "schema-valid" without a successful validation run; surface the actual validation status.

## Related Skills

- **build-mcp-server**: Apply structured output validation to MCP tool call results and argument parsing
- **setup-llm-gateway**: Route structured output requests through centralized gateway proxies
- **add-api-endpoint**: Integrate validated LLM output payloads into service endpoints and domain flows
- **write-tests**: Create test suites covering schema validation, constraint failures, and retry logic
- **review-code**: Verify schema strictness, error boundaries, and absence of regex parsing
