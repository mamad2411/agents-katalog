---
name: llm-cost-and-latency-optimization
description: >
  Guides reducing token cost and response latency of LLM-based agents
  without degrading quality. Use when a user asks to "reduce our LLM API
  bill," "make the agent respond faster," "our token usage is too high,"
  "should we use a smaller/cheaper model here," decide where to apply
  prompt caching, streaming, or batching, or needs to size a cost/latency
  budget before scaling an agent to more users.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: ai-agent
  maturity: stable
---

# LLM Cost and Latency Optimization

## Purpose

LLM API cost and response latency scale with tokens processed and number of
model calls — both of which are almost always higher than necessary in a
first working version of an agent, because it's easier to build without
budgeting either. Left unaddressed, this shows up as a surprising bill at
scale, or an agent that feels sluggish enough that users stop trusting it
to be interactive. Unlike raw model-quality tuning, most of the levers here
are structural and don't require changing which model you use at all:
reducing redundant context, caching stable prompt prefixes, choosing the
right model per step rather than the strongest model for everything, and
parallelizing or streaming where the task allows it. This skill treats cost
and latency together because most fixes affect both, though not always in
the same direction.

## When to use

- Token/API costs for an agent are higher than expected or growing faster
  than usage.
- An agent's end-to-end response time is too slow for its use case
  (interactive chat vs. background batch job have very different
  tolerances).
- Deciding whether a task step needs the strongest available model or can
  use a smaller/cheaper one.
- Evaluating whether prompt caching, batching, or streaming applies to a
  given workload.
- Sizing a cost/latency budget before scaling an agent from a prototype to
  production traffic.
- Reviewing an agent design for redundant or unnecessary model calls before
  it ships.

## Prerequisites & environment

- Access to per-call token usage and latency metrics from your model
  provider's API responses (most APIs return input/output token counts per
  call; capture and log these, don't estimate).
- Current pricing and context-window/caching capabilities for the specific
  model(s) in use — these vary by vendor and change over time, so verify
  against current provider documentation rather than assuming figures from
  memory or from a different model generation.
- A representative load profile (typical conversation length, typical tool
  call count per task) to reason about cost/latency at realistic scale,
  not just a single test call.

## Step-by-step guidance

1. **Measure before optimizing.** Instrument every model call with input
   tokens, output tokens, latency, and (if using tools) tool-call count.
   Aggregate by agent, by task type, and by pipeline stage — you cannot
   prioritize fixes without knowing which stage actually dominates cost or
   latency.

   ```python
   def call_llm(messages, tools=None):
       start = time.monotonic()
       response = client.messages.create(model=MODEL, messages=messages, tools=tools)
       metrics.record(
           stage="agent_loop",
           input_tokens=response.usage.input_tokens,
           output_tokens=response.usage.output_tokens,
           latency_ms=(time.monotonic() - start) * 1000,
       )
       return response
   ```

2. **Cut redundant context first — it's usually the largest and cheapest
   fix.** Audit what's actually being sent on each call: full conversation
   history with no windowing, full raw tool outputs instead of trimmed
   results, duplicated retrieved chunks across turns. See
   [prompt-and-context-engineering](../prompt-and-context-engineering/SKILL.md)
   for concrete history-management and budgeting techniques — this is
   usually higher-leverage than model choice.

3. **Use prompt caching for stable prefixes.** If your provider supports
   prompt/context caching, structure calls so the stable part (system
   prompt, tool definitions, static reference material) forms a consistent
   prefix, and only the per-turn variable content (user message, retrieved
   chunks) changes after it. This reduces both cost and latency on cache
   hits, often substantially, but the exact discount and minimum cacheable
   prefix length are provider- and model-specific — check current
   documentation for the model you're using.

4. **Right-size the model per step, not per agent.** A multi-step pipeline
   rarely needs the strongest available model at every step:

   ```
   plan step (ambiguous, needs strong reasoning)  -> strongest available model
   extraction/formatting step (well-specified)     -> smaller/faster model
   final safety/quality check                      -> smaller model or rule-based check
   ```

   Validate this split against your eval suite (see
   [agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md))
   before committing — a cheaper model may be entirely adequate for a
   well-specified step, or may not be, and that's an empirical question,
   not an assumption.

5. **Parallelize independent calls instead of serializing them.** If a
   task requires several independent tool calls or sub-agent calls with no
   data dependency between them (see
   [multi-agent-orchestration](../multi-agent-orchestration/SKILL.md)),
   issue them concurrently rather than one after another — this reduces
   wall-clock latency without changing total token cost.

6. **Stream output for interactive use cases.** For anything a human waits
   on synchronously, stream tokens as they're generated rather than
   waiting for the full response — this improves perceived latency
   significantly even when total generation time is unchanged, and costs
   nothing extra.

7. **Batch non-interactive workloads.** For background/bulk processing
   (e.g. classifying 10,000 tickets overnight) where no human is waiting
   synchronously, use a batch API if your provider offers one — batch
   endpoints commonly trade higher latency for meaningfully lower per-token
   cost, which is a good trade for offline work.

8. **Cap retrieval and tool-result size deliberately** (see
   [rag-pipeline-design](../rag-pipeline-design/SKILL.md)) — retrieving and
   injecting more chunks or more tool-result content than the task needs
   is a direct, avoidable token cost, not just a relevance-quality issue.

9. **Set a cost/latency budget per task type and alert on regressions.**
   Track cost and p50/p95 latency per task type over time; a prompt or
   tool change that silently doubles average tool-call count per task
   should show up as a tracked regression, not a surprise on the monthly
   invoice.

## Best practices

- Treat token usage as a first-class metric alongside quality in your eval
  harness — report cost and latency next to pass rate for every prompt/
  model change, so a quality improvement's cost isn't invisible.
- Default to the smallest/cheapest model that passes your eval suite for
  each pipeline step, and only escalate to a stronger model for steps
  where evaluation shows a real quality gap.
- Cache aggressively at the prompt level for stable content, and
  separately consider caching full results for identical or near-identical
  requests (e.g. the same document re-summarized) where correctness
  permits.
- Avoid few-shot examples in every call when a one-time fine-tune, a
  cached prefix, or a shorter instruction achieves the same effect for
  less recurring cost.
- Review tool schemas and system prompts periodically for unused bulk —
  content that made sense during prototyping but no longer earns its token
  cost in production.
- Don't chase the last 10% of cost reduction at the expense of reliability
  margins (e.g. removing a validation retry to save one call) — a failed
  task that needs manual rework costs far more than the tokens it would
  have taken to get it right the first time.

## Common pitfalls

- **Symptom:** Per-conversation cost grows steadily over a session's
  lifetime even though user requests stay similarly sized.
  **Fix:** This is almost always uncontrolled context growth (see
  [prompt-and-context-engineering](../prompt-and-context-engineering/SKILL.md))
  — audit what's actually in the context at each turn rather than assuming
  it's a model-pricing issue.

- **Symptom:** Switching to a cheaper model for a step reduces cost but
  increases the retry/failure rate enough that total cost (including
  retries) doesn't actually improve, or quality visibly degrades.
  **Fix:** Validate any model downgrade against the eval suite including
  its retry/failure rate, not just raw per-call price — measure end-to-end
  cost and quality together before adopting the change.

- **Symptom:** An interactive chat agent feels slow even though total
  token generation time hasn't changed.
  **Fix:** Add streaming so the user sees partial output immediately;
  perceived latency, not just raw generation time, is what interactive
  users experience.

- **Symptom:** A multi-step agent's latency is dominated by several
  independent tool calls executed one after another for no data-dependency
  reason.
  **Fix:** Identify which calls are genuinely independent and parallelize
  them; this is a wall-clock latency fix (not a cost fix) that requires no
  model or prompt change.

- **Symptom:** Prompt caching isn't producing the expected savings even
  though the system prompt is unchanged between calls.
  **Fix:** Check that the cached content is actually first in the prompt
  and that nothing before it (e.g. a timestamp, a session id) varies per
  call — even a small change earlier in the prefix invalidates the cache
  for everything after it in most caching implementations; verify the
  minimum cacheable length and current cache-hit behavior against your
  provider's documentation, since these details are provider-specific.

## Worked example

**Task:** a document-classification agent processing ~5,000 documents/day
was using the strongest available model for every document and running
fully synchronously, at higher cost and latency than the business need
(next-morning results) required.

Before:
```
model: strongest-tier model for every document
mode: synchronous, one call per document, serialized
avg cost/doc: $X (baseline)
avg latency/doc: ~4s, ~5.5 hours total for 5,000 docs run serially
```

After applying this skill's levers:
```
model: smaller/faster model for the classification step (validated against
       eval suite: pass rate within 1.5 points of strongest-tier model on
       the labeled eval set for this specific task)
mode: batch API, submitted as one batch job overnight
context: system prompt + label taxonomy cached as a stable prefix;
         per-document content is the only variable part
result: total batch cost reduced substantially per the provider's batch
        discount; total wall-clock time no longer matters since results
        are needed by morning, not synchronously
```

The model downgrade was only adopted after the eval suite (see
[agent-evaluation-and-guardrails](../agent-evaluation-and-guardrails/SKILL.md))
confirmed classification accuracy held within an acceptable margin on this
narrow, well-specified task — the same downgrade was explicitly not applied
to a separate, more ambiguous summarization step in the same pipeline,
which stayed on the stronger model after the eval suite showed a real
quality gap there.

## Cross-references

- [prompt-and-context-engineering](../prompt-and-context-engineering/SKILL.md)
- [rag-pipeline-design](../rag-pipeline-design/SKILL.md)
- [agent-architecture-design](../agent-architecture-design/SKILL.md)
