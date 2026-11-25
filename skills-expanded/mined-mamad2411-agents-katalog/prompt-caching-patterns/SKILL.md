---
name: prompt-caching-patterns
description: Use provider prompt caching (Anthropic, OpenAI, Gemini, Bedrock) to cut input costs 50-90% and latency 30-70%. Use when designing system prompts, agent harnesses, or any workflow that calls the same model with overlapping context repeatedly.
source: self
date_added: 2026-05-01
---

# Prompt Caching Patterns

Prompt caching is the highest-ROI lever after model fit. Most teams leave 5-10x on the table because their prompt prefix isn't byte-stable.

## When to Use

- Same system prompt or tool list reused across many calls.
- Multi-turn chat or agent loops within a session.
- RAG with stable schemas and rotating user queries.
- Few-shot pipelines where the examples don't change per call.
- Anywhere `cached_input_tokens` in your usage logs is near zero but should be high.

## Provider Quick Reference (2026)

| Provider | Mechanism | Min cacheable | Default TTL | Discount on hit |
| --- | --- | --- | --- | --- |
| Anthropic | Explicit `cache_control` breakpoints | 1024 tokens (Sonnet/Opus) | 5 min (1h tier available) | ~90% off cached input |
| OpenAI | Automatic on prefix ≥ 1024 tokens | 1024 tokens | ~5-10 min idle | ~50-75% off cached input |
| Google Gemini | Implicit (auto) + Explicit (`cachedContents`) | model-dependent | Configurable on explicit | ~75% off cached input |
| AWS Bedrock | Per-model (Anthropic / Nova) | Per-model | Per-model | Per-model |

Always check the current pricing page; numbers move.

## The Golden Rule: Stable Prefix

Caches key on the **byte-exact prefix** of the prompt. Order content **stable → volatile**:

```
1. System prompt
2. Tool / function definitions
3. Project conventions, style guide
4. Long-lived references (schemas, glossaries)
5. Few-shot examples
6. Retrieved chunks (per-task)
7. Conversation history
8. User message (most volatile)
```

Anything that changes per call must come **after** everything you want cached.

## Killing the Cache by Accident

Common mistakes that break the prefix hash:

- Injecting a timestamp ("Today is 2026-05-01...") at the top.
- User name or session ID in the system prompt.
- Reordering tool definitions between calls.
- Reformatting JSON (whitespace, key order) before sending.
- Swapping model versions or `temperature` mid-session (some providers key on these).
- Trimming whitespace differently across code paths.

Fix: serialize the cacheable prefix once, at module load, and reuse the exact bytes.

## Anthropic-Specific

- Place `cache_control: {"type": "ephemeral"}` on the **last** content block of each cacheable segment.
- Up to 4 breakpoints — use them at: end of system, end of tools, end of references, end of last stable user turn.
- Use the 1-hour cache tier for workflows with > 5 min gaps between calls (worth the higher write cost when reused).
- Cache writes cost ~25% more than uncached input; reads cost ~10% of input. Break-even ≈ 2 reads.

## OpenAI-Specific

- Caching is automatic; you don't mark breakpoints.
- Discount applies once prefix ≥ 1024 tokens; granularity in 128-token chunks.
- Cache lives ~5-10 min idle, longer under load.
- `prompt_cache_key` (when supported) helps route consistent traffic to a warm cache.

## Gemini-Specific

- Implicit caching now on by default for Gemini 2.5 family — works automatically when prefix ≥ ~1k tokens.
- Use **explicit** `cachedContents` for very large, long-lived prefixes (whole codebases, large PDFs) and reference them by name.
- Set TTL explicitly when using `cachedContents`.

## Cache Warming

- For latency-sensitive endpoints, fire a tiny dummy request after deploy to populate the cache.
- For batch workloads, group requests by shared prefix so the first call warms the rest.
- Avoid "thundering herd" warm-up that exceeds rate limits.

## Measuring

Every provider exposes cached vs uncached input tokens in usage. Track:

- `cache_hit_ratio = cached_input / total_input`
- `cache_savings_$ = cached_input * (input_price - cached_price)`
- TTFB / p50 latency vs uncached baseline

Targets for a well-tuned workflow: hit ratio > 70% on agent loops, > 50% on chat, > 30% on bursty RAG.

## Anti-Patterns

- Personalization fields (user name, locale) injected into the system prompt — move them to the user message.
- Per-call random IDs in the prefix (e.g., trace IDs sent to the model).
- Caching everything including the user query — defeats the purpose.
- Using cache only on production, not on evals — eval cost balloons.
- Not measuring hit ratio, then "optimizing" prompts blindly.
- Pruning cached few-shots to "save tokens" — cached tokens are nearly free; pruning may *raise* cost by reducing accuracy and triggering retries.

## Quick Wins Checklist

- [ ] Cacheable prefix serialized once, reused byte-exact
- [ ] Order is stable → volatile, user query last
- [ ] No timestamps / IDs / personalization in the prefix
- [ ] Anthropic breakpoints placed at segment ends (≤ 4)
- [ ] `cache_hit_ratio` logged per call and dashboarded
- [ ] Cache warming on deploy for latency-critical paths
- [ ] 1h tier (Anthropic) or `cachedContents` (Gemini) used where prefixes are huge

## References

- Anthropic prompt caching documentation
- OpenAI prompt caching documentation
- Google Gemini context caching documentation
- AWS Bedrock prompt caching per-model docs
- Related skills: `token-efficient-prompting`, `context-window-management`, `llm-cost-optimization`
