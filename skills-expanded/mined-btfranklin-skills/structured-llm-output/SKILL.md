---
name: structured-llm-output
description: >-
  Design, implement, or review typed LLM output. Use constrained generation, validation, limited retries, and explicit failure handling. Use this skill when extracted, classified, or generated objects enter application code. Do not use it for ordinary prompts, unstructured chat, validation without an LLM, or API-key setup.
---

# Structured LLM Output

## Workflow

For a design or review, assess these steps without changing project files or deployed services. Identify proposed changes and checks. For implementation, perform the applicable steps.

1. Inspect the source material, downstream consumer, provider, SDK, and existing validation conventions.
2. Define the smallest schema that represents the required facts. Define required, optional, nullable, unknown, and unavailable values explicitly.
3. Prefer provider-native constrained generation to prose instructions or manual JSON extraction.
4. Validate syntax, field constraints, cross-field invariants, and source faithfulness separately.
5. Retry only failures that another model attempt can repair. Set an attempt limit. Preserve the final validation error.
6. Define the response to each failure condition before implementation:
   - Fail closed when an incomplete or incorrect value can cause an unsafe or irreversible action.
   - Return a typed partial result only when the consumer supports missing values. Confirm that the consumer cannot treat missing values as complete.
   - Request human review when a person can resolve the ambiguity and the workflow can wait safely.

   Use different responses for different failure conditions when needed. Never invent a default for missing source evidence.
7. Test representative success, ambiguity, refusal, malformed input, unsupported values, injection attempts, and exhausted retries.
8. Report the schema contract, data flow, failure policy, observability, and unresolved risks.

Keep prompts in external Markdown files when you implement a repository workflow. Preserve the repository's provider and library choices unless the user asks for a migration.

## Verify Current Information

Before you give provider-specific or library-specific code, verify the current official documentation. Check schema support, SDK interfaces, model compatibility, and retry behavior. Record the checked provider and library versions or the verification date in the review or implementation notes. Do not describe a model, SDK, or library release as latest without checking its primary source.

## Resources

- Read [references/structured-output-patterns.md](references/structured-output-patterns.md) when choosing schema, validation, retry, and production patterns.
- Read [examples/schema-review-output.md](examples/schema-review-output.md) when you need a report example.
