---
name: ai-engineering
description: Building production features powered by LLMs — model selection, prompt design as engineering, structured output, RAG, evals, cost/latency budgets, and guardrails. Use when adding AI features to a product (chat, extraction, summarization, classification, search), designing prompts that ship to production, building RAG pipelines, or when the user says "LLM feature", "integrate AI", "prompt engineering", "RAG", "embeddings", or "evals".
---

# AI Engineering

An LLM feature is a probabilistic component inside a deterministic system. The engineering is not the prompt — it's everything around the prompt that makes unreliable output safe to ship: schemas, fallbacks, evals, and budgets. Treat the model like a talented but occasionally wrong remote API, because that is exactly what it is.

## Rule 0: Do you even need a model?

Regex, a lookup table, or a SQL query that solves 95% of the cases beats an LLM that solves 98% — cheaper, faster, deterministic, debuggable. Use an LLM where the input is genuinely open-ended (natural language, unstructured documents, judgment calls). Hybrid is usually right: deterministic code for the structure, the model only for the irreducibly fuzzy step.

## Prompts are code — manage them like code

- Prompts live in version control, named and versioned, never inline string-concatenated across the codebase. A prompt change is a deploy: reviewable, diffable, revertible, and eval-gated (see below).
- Structure every production prompt the same way: role/goal → constraints and refusal conditions → the input (clearly delimited — assume user input is hostile and may contain instructions; label it as data, never let it sit where instructions sit) → output format specification → 2–5 few-shot examples of hard cases (examples move behavior more than adjectives).
- Test prompts against the *ugly* inputs: empty, enormous, wrong-language, adversarial ("ignore previous instructions"), and out-of-domain. The demo input tells you nothing.

## Structured output — the highest-ROI habit

Never parse prose. Demand JSON against a schema (native structured-output/tool-calling modes where the provider has them), then **validate with a real schema layer** (Pydantic/zod) before the data touches your system. On validation failure: one retry with the error fed back, then fallback path. This one habit converts "AI feature is flaky" into ordinary input validation.

## The reliability ladder — climb only as far as needed

1. Better prompt + examples (always first — cheapest lever by far)
2. Structured output + validation + retry
3. Split one mega-prompt into a pipeline of small single-job calls (classify → extract → format), each independently testable
4. RAG — give the model your data at answer time
5. Fine-tuning — last resort: for style/format at volume, not for knowledge; only with an eval set already proving the gap

## RAG, minus the hype

RAG is search wearing a trenchcoat — its quality ceiling is your *retrieval* quality, not the model:
- Chunk by semantic boundary (sections/paragraphs) with metadata (source, date, tenant); tune chunk size empirically, don't cargo-cult 512.
- Hybrid retrieval (keyword/BM25 + vector) beats either alone for most business data; rerank the top-k when precision matters.
- **Debug retrieval separately from generation**: log what chunks were retrieved for each query; most "the AI answered wrong" bugs are "the right chunk was never retrieved". Evaluate retrieval (did the gold chunk appear?) and generation (was the answer faithful to the chunks?) as two metrics.
- Ground truth rules: instruct the model to answer *only* from provided context and say "not found" otherwise; cite chunk sources in output; multi-tenant data MUST filter retrieval by tenant before ranking — cross-tenant leakage via embeddings is a breach (threat-model-security).

## Evals — the tests of AI engineering (non-negotiable)

Shipping an LLM feature without evals is shipping code without tests, except the code also changes behavior when the provider updates the model.
- Build a golden set from day one: 20–50 real(istic) input→expected pairs, weighted toward the hard cases and past failures (every production miss becomes an eval case — the regression-pin rule from testing-strategy).
- Grade with the cheapest sufficient method: exact/schema match where output is structured; assertion checks ("mentions the refund policy", "no amounts invented") where it's prose; LLM-as-judge (different model, pinned version, spot-audited against human judgment) only where necessary.
- Run evals on every prompt change and every model/version swap, in CI if possible. Track the score over time; a prompt "improvement" that drops the eval is a regression with better vibes.

## Production posture

- **Budgets before launch**: cost per request (tokens × price, measured not guessed) and latency budget. Long outputs stream to the user; anything slower than the UI budget moves async (system-design). Cache identical/near-identical requests where the product tolerates it.
- **Failure design**: the provider WILL have outages, rate limits, and slow days. Timeouts, bounded retries with backoff, and a designed degraded mode (queue it, use the deterministic fallback, or honestly say "unavailable") — never a spinner forever (product-ux-quality).
- **Log every call**: prompt version, model+version, input hash, output, tokens, latency, validation result. This is your incident forensics and your future eval mining. Redact PII per observability-readiness rules.
- **Safety gates scaled to blast radius**: model output shown to a user needs escaping (it's untrusted content — XSS applies); output that triggers actions needs allowlists and the agent rules (ai-agent-design); output that goes to *other* users or money paths needs human review or hard validation. Prompt injection is unsolved — design so that a fully compromised model output still can't do real damage.
- Abstract the provider behind an adapter (architecture-design): model routing, fallback providers, and next year's migration become config, not surgery.
