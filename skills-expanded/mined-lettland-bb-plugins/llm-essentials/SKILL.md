---
name: llm-essentials
description: Use when designing any LLM-backed feature, any provider — token economics, sampling, structured outputs, retries, eval harnesses.
metadata:
  added: 2026-05-19
  last_reviewed: 2026-05-19
  type: core
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-19"
  related: [claude-api, agent-design, python-openai-sdk, go-langchaingo, go-anthropic]
---

# LLM Essentials (Provider-Agnostic)

**Iron Law: every call has a deadline, a `max_tokens`, a retry cap, and a recorded `usage`. Output is text — never act on it without a schema check. Sampling near 0 for tools and structured output; higher only when you actively want variety. Eval is a first-class artifact, not an afterthought: a regression you can't detect is a regression you'll ship.**

## Token economics

| Lever         | Cost shape                             | Practical rule                                                                      |
| ------------- | -------------------------------------- | ----------------------------------------------------------------------------------- |
| Input tokens  | cheap (typically ~1/5 of output $/tok) | spend liberally on context; cache the stable prefix                                 |
| Output tokens | expensive (~5x input)                  | cap `max_tokens` aggressively; trim verbose system prompts that bait long responses |
| Cache reads   | very cheap (~1/10 of input)            | the highest-ROI optimization for any repeated-prefix workload                       |
| Cache writes  | premium over input (1.25–2x)           | only worth it when the prefix is read ≥2 times within the TTL                       |

**Cost model in one line:** `cost_per_call ≈ (input_tokens × in_$/1K) + (output_tokens × out_$/1K)` plus cache delta. Log `usage` on every call; sum by route/user/feature and alert on per-route regressions. Without per-route accounting, you find cost bugs in the bill, not in the code.

## Sampling

| Parameter           | Effect                                        | Default for...                                                       |
| ------------------- | --------------------------------------------- | -------------------------------------------------------------------- |
| `temperature` (0–2) | scales the distribution; higher = more random | `0` for tools/structured output; `0.2` for code; `0.7+` for creative |
| `top_p` (0–1)       | nucleus sampling: only consider top-p mass    | leave at `1` unless you know why; rarely tune alongside temperature  |
| `top_k`             | only consider top-k tokens                    | provider-specific; usually unset                                     |
| `stop_sequences`    | hard halt on substring match                  | use to enforce structured boundaries (`</done>`, `\n\n---`)          |

**Rules of thumb:** lower temperature when correctness matters more than novelty; one knob at a time (don't co-tune `temperature` and `top_p`); the same prompt at `temperature=0` is _near_-deterministic but not strictly so — providers don't guarantee bit-exact reproducibility.

## Structured outputs

Three strategies, in order of preference:

1. **Constrained tool-use** (best): declare a tool with a tight JSON Schema (`additionalProperties:false`, enums, numeric bounds). Force selection via `tool_choice: {type:"tool", name:"..."}` or its provider equivalent. The model fills the schema; you `json.Unmarshal`. Lowest hallucination risk.
2. **JSON mode** (provider feature, e.g., OpenAI `response_format: json_object`): the model emits valid JSON but the _shape_ is up to the prompt. Pair with schema validation post-hoc.
3. **Free-text + parsing** (worst): only when neither tool-use nor JSON mode is available. Wrap with retries and a strict validator; expect 1–5% failure rate.

**Always validate** server-side after parsing — `pydantic` in Python, `ajv` in TS, `santhosh-tekuri/jsonschema` v6 in Go. The model is a stochastic generator; the schema is the contract. See [[claude-api]] for tool-use shape; [[python-openai-sdk]] for OpenAI's `responses.parse(...)` typed return.

## Prompt patterns (cheat sheet)

| Pattern                    | When                                    | Shape                                                                                     |
| -------------------------- | --------------------------------------- | ----------------------------------------------------------------------------------------- |
| **System role**            | every call                              | "You are a careful X. Answer in Y format." — 1–3 sentences                                |
| **Few-shot**               | classification, format-sensitive output | 3–8 examples in `user` / `assistant` pairs; quality > quantity                            |
| **Chain-of-thought (CoT)** | multi-step reasoning, math, planning    | "Think step by step" or use a `thinking` mode if the provider has one                     |
| **Role / persona**         | tone shaping                            | "Respond as a senior reviewer." Avoid theatrical roles — they degrade accuracy            |
| **Negative instructions**  | curb known failure modes                | "Do not invent fields not in the schema." Sparingly — too many constraints reduce quality |
| **Output framing**         | structured short outputs                | "Reply with one of: APPROVE, REJECT, ESCALATE." Pair with `stop_sequences`                |

**Anti-patterns:** stacking 10+ negative instructions ("don't do X, don't do Y...") — accuracy drops; "you MUST" / "VERY IMPORTANT" caps lock — diminishing returns past one or two; few-shot examples of poor quality — the model imitates the floor, not the ceiling.

## Retry + backoff math

Production-quality retry loop:

```
attempt = 0
while attempt <= MAX (3):
    try call with timeout=T
    if 200: return
    if 4xx and not 429: raise (permanent — bad request)
    if 401/403: raise (auth — retrying just burns budget)
    sleep = min(CAP, BASE * 2**attempt) * jitter(0.5..1.5)
    if response has Retry-After: sleep = max(sleep, Retry-After)
    attempt += 1
raise after-cap
```

Constants that work: `BASE=1s`, `CAP=30s`, `MAX=3`, jittered. Honor `Retry-After` always. Use an **idempotency key** for any call that has external side-effects (DB writes via a tool, payment) — providers honor it; the SDK usually generates one if you don't. **Never retry 4xx other than 429** — permanent failures don't get better with patience.

## Eval

A regression you can't detect is a regression you'll ship. Minimum viable eval:

- **Golden set** (~30-200 examples): real inputs paired with the expected output (exact string, regex, or structural). Versioned in git alongside the prompt. Re-run on every prompt or model change.
- **Deterministic scorers first** (exact match, regex, JSON-schema validity, contains-required-key). Cheap, fast, no API call.
- **LLM-as-judge for subjective criteria** (helpfulness, tone, safety): a separate model call with a _clear rubric_ and binary or 1–5 scoring; sample-audit human-vs-judge agreement quarterly.
- **Track per-eval pass rate over time** in your CI / metrics. A 3-point drop after a prompt change = revert and investigate.
- **Don't tune on the eval set.** Hold out a separate _test_ set that you only run when graduating a prompt to production.

For agent workflows (multi-turn, tool-using), evals get harder — see [[agent-design]] for trajectory-level scoring.

## Cost guardrails

| Guardrail                   | Why                                       | How                                                                         |
| --------------------------- | ----------------------------------------- | --------------------------------------------------------------------------- |
| `max_tokens` cap            | unbounded output = unbounded $            | always set; size for the expected response + small buffer                   |
| Per-request timeout         | hanging providers stall workers           | wrap every call in a `context.WithTimeout` or `httpx.Timeout`               |
| Concurrency cap             | rate-limit storms cost retries            | semaphore sized to your RPM headroom                                        |
| Per-user / per-route budget | one runaway user shouldn't eat the budget | track `usage` per identity; throttle/reject above quota                     |
| Model downshift             | Opus for everything is wasteful           | route by complexity — Haiku for triage, Sonnet default, Opus for hard cases |
| Cache the long prefix       | repeat-input is the biggest cost lever    | see [[claude-api]] §Prompt caching                                          |

## Context-window strategies

| Strategy                | When                                  | Trade-off                                                                 |
| ----------------------- | ------------------------------------- | ------------------------------------------------------------------------- |
| **Truncate oldest**     | conversation tail grows beyond budget | loses early-turn context; cheap and predictable                           |
| **Summarize-then-drop** | long-running agent loops              | extra LLM call to summarize; preserves gist; nondeterministic compression |
| **Sliding window**      | known-bounded interaction length      | fixed cost; cliff if window crosses an important earlier message          |
| **Retrieval (RAG)**     | corpus too big to load                | retrieval quality dominates answer quality; eval the retriever separately |
| **Hierarchical**        | docs with structure                   | summarize sections, retrieve specifics on demand; complex pipeline        |

**Always measure**: log the input-token count per call and watch for drift toward the window limit. Hitting the cap once = your truncation strategy works. Hitting it every call = your strategy is broken (or you need a bigger model).

## Anti-patterns

- No `usage` logging — you find cost bugs on the invoice, not in code
- Same temperature for tools and prose — tools want 0, prose wants 0.2+
- Free-text output with a regex parser — works in dev, fails in prod under format drift
- Prompt edits with no eval re-run — silent regressions compound
- One mega-prompt for all use cases — split by use case; each gets simpler and faster
- Untracked prompts (in DB rows, in code strings) — version your prompts in git like any other code
- `max_tokens` unset or set to the window max — runaway output, runaway cost
- Retrying 4xx — permanent failures don't heal; only 429 + 5xx + network errors are retryable
- Pinning to a model alias (`latest`) — silent model swaps re-baseline evals; pin specific versions

## Red flags

| Thought                                            | Reality                                                                        |
| -------------------------------------------------- | ------------------------------------------------------------------------------ |
| "I'll add eval later, once it's stable"            | The eval IS what makes it stable — write it first                              |
| "Temperature=0 is deterministic"                   | Near-deterministic; providers don't guarantee bit-exactness                    |
| "Negative instructions stack"                      | They don't — past ~3, accuracy drops; restructure as positive constraints      |
| "I'll parse the JSON in the response with a regex" | One unicode quirk away from breaking; use a real parser + schema               |
| "Bigger model fixes everything"                    | Sometimes a smaller model + better prompt + tool-use wins on accuracy AND cost |

## Hand-off

For the Anthropic-specific shape of caching, thinking, tool-use: [[claude-api]]. For the Go SDK ergonomics: [[go-anthropic]]. For OpenAI in Python: [[python-openai-sdk]]. For multi-provider Go: [[go-langchaingo]]. For agent loop architecture (when LLM calls compose into a workflow): [[agent-design]].
