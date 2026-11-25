---
name: llm-guardrails
description: Design guardrails for an LLM feature — input validation, prompt-injection defenses, output filtering/schema validation, allow-deny policy, and human-in-the-loop gates.
---

# llm-guardrails

> A model will be asked to do things you didn't intend and emit things you can't ship. Guardrails are the validation layer on both sides of the model — design them as code, not as prompt pleading.

## When to use

- Exposing an LLM to untrusted input (user text, retrieved docs, tool output) or letting it drive actions.
- A feature can emit unsafe, off-brand, or malformed output, or has shown prompt-injection susceptibility.
- A workflow invokes `polymath-ai:llm-guardrails`.

Not this when: you are auditing an existing LLM system end-to-end for security findings — that is `polymath-security:llm-security-review` (this skill *designs* the controls that review checks for). For agent stop conditions, see `polymath-ai:agent-design`.

## Inputs

- The data flow: where untrusted text enters, what the model can do with it, what it emits, and to whom.
- The actions the model can trigger and their blast radius.

## Procedure

1. **Map the trust boundaries**: every place untrusted text reaches the prompt (user input, RAG documents, tool results, prior turns). Retrieved/tool content is untrusted too — indirect prompt injection rides in there.
2. **Input guardrails**: validate/normalize input; detect and neutralize injection attempts (instruction-override phrasing); keep untrusted content in clearly delimited, lower-trust positions; never concatenate untrusted text into the system prompt.
3. **Privilege separation**: the model proposes, code authorizes. High-impact/irreversible actions go through deterministic checks and human confirmation — the model's output is never the sole authority for a mutating action.
4. **Output guardrails**: validate structure (parse/schema-check JSON, reject on failure), filter for safety/PII/secrets, and constrain to an allow-list of actions rather than a deny-list where possible.
5. **Ground and cite** where factuality matters; flag low-confidence/unsupported output instead of emitting it silently.
6. **Fail closed**: on a guardrail trip, the safe default is refuse/escalate, not pass-through. Define the user-visible behavior on each trip.
7. **Log and rate-limit**: record trips for monitoring; rate-limit to bound abuse and cost. Hand the adversarial test design to `polymath-security:llm-security-review`.

## Output

- A one-page guardrail design: the trust-boundary map, input controls, the propose-vs-authorize split for actions, output validation/filtering, fail-closed behaviors, and what is logged/rate-limited.

## Quality bar

- Untrusted retrieved/tool content is treated as untrusted, not just direct user input.
- No mutating action is authorized by model output alone.
- Output is schema-validated where structured; a parse failure is handled, not assumed away.
- Every guardrail trip fails closed with a defined user-visible behavior.
