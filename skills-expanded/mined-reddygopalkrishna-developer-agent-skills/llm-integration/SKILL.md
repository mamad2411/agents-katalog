---
name: llm-integration
description: Builds production features on top of LLM APIs - prompt structure, structured outputs with schema validation, streaming, retries and timeouts, cost and latency control, prompt-injection defenses, PII handling and tracing. Use when adding an LLM call to an app, designing a prompt for a product feature, parsing model output into data, or hardening an existing LLM feature for production. Not for retrieval pipelines (use rag-systems) or autonomous tool loops (use building-agents).
license: MIT
---

# LLM Integration

Treat an LLM call like any other unreliable, expensive, network dependency whose output is untrusted input. Every LLM feature needs a schema for its output, a test set that proves it works, limits on cost and time, and a plan for when the model fails.

## When to use

- Adding a summarize / classify / extract / generate / rewrite feature backed by a model API.
- Turning free-text model output into typed data the app depends on.
- An existing LLM feature is flaky, slow, expensive, or was never tested.

Not for: RAG design (use `rag-systems`), multi-step tool-using loops (use `building-agents`), building eval suites in depth (use `llm-evals`).

## Workflow

1. **Write down the contract first.** Input (types, max size), output (a JSON Schema or typed model), latency budget, cost budget per call, and what the product does when the model fails. If the user can't state it, ask before writing code.
2. **Collect 20-50 real examples** of inputs with the expected output or pass criteria. This is the smallest test set worth having. Include hard and adversarial cases.
3. **Choose the model by measurement.** Start with a capable model to prove the task is possible, then try smaller/cheaper ones against the same examples. Pick the cheapest one that passes. Do not choose from benchmarks or memory.
4. **Structure the prompt** (see below), store it as a versioned file or constant in the repo, never assembled ad hoc across the codebase.
5. **Get structured output** through the provider's JSON-schema / structured-output mode or tool calling, then validate with a schema library anyway (Pydantic, Zod, JSON Schema validator, a typed record).
6. **Wrap the call**: timeout, retry policy, max output tokens, tracing, error mapping (see "Reliability").
7. **Defend the boundaries**: untrusted input in, untrusted output out (see "Security").
8. **Run the examples** and record pass rate, p50/p95 latency and cost per call. Add them to CI as a regression check (see `llm-evals`).
9. **Ship behind a flag** with a fallback path, then watch production traces and add failures to the test set.

## Prompt structure

Order the prompt so stable parts come first (better for prompt caching) and the task-specific parts come last.

| Part | What goes in it |
|---|---|
| Role and goal | One or two sentences: what the model is doing and for whom. |
| Instructions | Numbered rules. Say what to do, not only what to avoid. Say what to do when input is missing or ambiguous. |
| Output format | The schema or an exact example. Say what value means "unknown" (e.g. `null`), never let the model invent. |
| Examples | 2-5 input/output pairs covering edge cases. Make them varied so the model doesn't copy one shape. |
| Context | Documents, user data, retrieved text, clearly delimited (XML-style tags or fenced blocks) and labeled as data. |
| Task input | The specific request, last. |

Rules:

- Keep prompts in version control next to the code that uses them, with the examples that test them.
- Change one thing at a time and re-run the examples after every change.
- Ask for reasoning before the answer only when the task needs it; put it in a separate field so you can drop it from what you show users.
- Don't stuff the prompt with everything; irrelevant context lowers quality and raises cost.

## Structured output

- Prefer native structured output (JSON schema constrained decoding) or a single forced tool call over "please reply in JSON".
- Keep schemas flat and small. Use enums for categories. Make fields required and allow `null` for unknown rather than optional fields that silently vanish.
- Always validate after parsing. On validation failure: retry once with the validation error appended, then fail to the fallback. Don't loop forever.
- Never `eval` or execute output. Parse it.

## Context window management

- Count tokens with the provider's tokenizer or token-count endpoint before sending large inputs; don't estimate from characters for hard limits.
- Reserve space for the output (`max_tokens`) inside the context budget.
- For long inputs choose deliberately: truncate (with a note), select relevant parts (retrieval), or map-reduce (summarize chunks, then combine).
- In conversations, keep the system prompt and recent turns; summarize or drop old turns.

## Streaming

- Stream when a human is waiting on long text; it cuts perceived latency to the first token.
- Don't stream when you need the whole output validated before use (structured data) unless you parse incrementally and can recover.
- Handle mid-stream errors: show partial output as incomplete, offer retry, and log the failure.

## Reliability

| Failure | Handling |
|---|---|
| Rate limit (429) | Retry with exponential backoff and jitter; honor `Retry-After` when present. |
| Overloaded / 5xx | Retry with backoff, a small fixed number of times (2-3). |
| Timeout | Set a client timeout matched to the latency budget; on timeout retry once or fall back. |
| 4xx other than 429 | Do not retry. It's a bug in the request (bad schema, too many tokens, auth). |
| Invalid output | One repair retry with the validation error, then fallback. |
| Refusal or empty answer | Treat as a distinct outcome; log it and use the fallback or a user-facing message. |

- Make calls idempotent from the app's side: retries must not double-charge users or double-write data.
- Put a ceiling on total retries per request so a bad prompt can't multiply cost.
- Fallbacks, in order of preference: a smaller/other model, a cached previous answer, a deterministic non-LLM path, a clear "unavailable" message. Never a silent wrong answer.

## Cost and latency

- **Measure first**: log input tokens, output tokens, latency and model per call.
- **Prompt caching**: keep the long, stable prefix (instructions, examples, shared documents) identical across calls and put variable content last. Check your provider's docs for how caching is enabled and priced.
- **Right-size models**: route easy steps (classification, extraction, routing) to smaller models; reserve large models for hard steps that the eval shows need them.
- **Cap output** with `max_tokens` and by asking for concise formats. Output tokens are usually slower and pricier than input tokens.
- **Batch** offline/non-urgent work through the provider's batch API if it has one.
- **Cache results** for identical inputs where the answer is deterministic enough (temperature 0, same prompt version) and data isn't user-sensitive.
- **Parallelize** independent calls; don't chain calls that don't depend on each other.

## Security

Prompt injection is not solved by prompting. Design so a fully hijacked model can't do damage.

- Treat everything that isn't your own instructions as untrusted data: user input, web pages, files, emails, retrieved chunks, tool results. Delimit it and tell the model it is data, but don't rely on that alone.
- **Never pass model output unvalidated to a sink**: shell, SQL, `eval`, file paths, URLs you will fetch, HTML (escape or sanitize before rendering; markdown images can exfiltrate data via URLs), emails or messages.
- Give tools least privilege: read-only where possible, scoped to the current user's data, with server-side authorization checks that don't trust the model's claims about who the user is.
- Require human confirmation for actions with side effects (sending, deleting, paying, publishing).
- Don't put secrets in prompts. Assume prompts can be extracted.

## Privacy and data handling

- Know what data leaves your system. Check the provider's data-retention and training-use terms with the user before sending personal or confidential data.
- Minimize: send only fields the task needs. Redact or pseudonymize PII where the task allows.
- Apply the same retention and access rules to logged prompts/responses as to the source data; they often contain PII.

## Observability

Log per call: request ID, feature name, prompt version, model, input/output token counts, latency, finish reason, retries, validation result, and (subject to privacy rules) the prompt and response. Trace multi-call flows end to end. OpenTelemetry has GenAI semantic conventions for this; they are still marked experimental, so check the current attribute names before relying on them. Review a sample of real traces weekly and turn failures into test cases.

## Anti-patterns

- **Vibe-checking** - trying three inputs by hand and shipping. Use a test set.
- **Regex-parsing prose** - ask for structured output instead.
- **Prompt sprawl** - prompts built by string concatenation in many files with no version or tests.
- **Retrying everything** - retrying 400s, or unbounded retries that multiply cost.
- **Trusting the model with authorization** - "only return data for user X" in the prompt instead of enforcing it in code.
- **Rendering raw output as HTML** - XSS and data exfiltration via links/images.
- **Picking the biggest model by default** - often several times the cost and latency for no measurable gain.
- **Hard-coding a model name everywhere** - keep it in config so you can switch and A/B test.

## Done when

- The input/output contract and failure behavior are written down.
- Output is schema-validated, with a bounded repair retry and a fallback.
- Timeouts, retry policy and `max_tokens` are set; non-retryable errors are not retried.
- A versioned prompt and a test set of real examples exist, with pass rate, latency and cost recorded.
- No model output reaches a shell, SQL, HTML or other sink without validation; side-effecting actions need confirmation.
- Calls are traced with prompt version, model, tokens and latency.
