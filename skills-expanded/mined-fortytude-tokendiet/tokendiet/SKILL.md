---
name: tokendiet
description: LLM cost-waste detection knowledge — how to find and fix expensive AI API usage patterns (prompt caching, batching, retry caps, model routing, prompt bloat) in a codebase, honestly and without fabricated dollar figures.
---

# TokenDiet — LLM cost-waste detection

This skill teaches you to audit a codebase for **wasteful, expensive LLM API usage** and
produce a concrete, honest plan to cut it. It is the knowledge behind the `/tokendiet`
command. You are acting as a senior LLM-cost engineer: you read code, you don't guess, and
you never invent a number.

## What LLM cost waste actually is

Hosted LLM APIs bill per token — flat, not quadratic. Cost is driven by three things:
**how many tokens you send** (input), **how many you generate** (output), and **how many
times** you do it (call volume). Waste is any pattern that inflates one of those without
buying you quality:

- **Re-sending the same bytes uncached** — the single biggest, safest win. A static system
  prompt / tool schema / few-shot block sent on every call, with no cache breakpoint (or a
  volatile value busting the cache).
- **Paying full price for offline work** — bulk/cron/eval loops on the sync API instead of
  the Batch API (50% off, published rate).
- **Generating more than you need** — no `max_tokens` cap, verbose free-text where
  structured output would do, `reasoning_effort` cranked high on trivial calls.
- **Sending more context than you need** — RAG over-fetch, unbounded growing history,
  pretty-printed JSON payloads, tool schemas re-sent every turn.
- **Doing the work more than once** — re-embedding unchanged content, duplicate calls,
  uncapped retries that re-send the whole request on failure.
- **Using an overpowered model** — a flagship on a classify/extract/route task a cheaper
  tier could handle. Always a *suggestion*, never a promise (it changes quality).

The full catalog with code shapes and fixes is in **`references/waste-catalog.md`**. How to
find each pattern in real code is in **`references/detection-heuristics.md`**.

## THE HARD HONESTY RULE (read this every run)

This is non-negotiable — it is what keeps the report trustworthy.

1. **Never fabricate a dollar figure.** You do not know the user's traffic volume, so you
   cannot state a "$X/month saved." Describe waste qualitatively: the pattern, the
   mechanism, the fix.
2. **Published provider rates are facts you MAY cite** — "cached reads bill at ~10% of the
   input rate (Anthropic published)", "the Batch API is 50% off (provider published)". You
   may state the rate. You may **not** multiply it into a monthly total.
3. **Pricing only on explicit request.** If the user explicitly asks "how much will this
   save me," *then* ask for their monthly LLM bill or call count, and contextualize against
   that. Never volunteer a number.
4. **A model swap / downgrade is ALWAYS a suggestion to validate, never a saving.** Sonnet→
   Haiku, gpt-4→gpt-4o-mini — these change output quality. Flag them as behavior-change,
   tell the user to test on their own outputs. Never attach a dollar figure to a downgrade.
5. **Never propose a corrupting edit.** A fix must be behavior-preserving (for a
   SAFE-MECHANICAL apply) or explicitly flagged as behavior-change for the user to validate.
6. **Cite evidence.** Every finding references a real `file:line`. No evidence → no finding.
7. **Never claim "exhaustive."** Say "I reviewed N call-sites and found K issues."

The full contract, with the reasoning behind each line, is in **`references/honesty-rules.md`**.

## The fix taxonomy (tag every finding with exactly one)

| Class | Meaning | Dollar? | Apply? |
|---|---|---|---|
| **SAFE-MECHANICAL** | Behavior-preserving; the model sees the same thing, only billing changes | Cite the published rate only | Yes, with a shown diff + confirmation |
| **BEHAVIOR-CHANGE** | Changes what the model sees/does; needs the user to validate quality | Never — it's a bet on their output | Suggest only, never auto-apply |
| **INFORMATIONAL** | A guard-rail or enablement note (missing cap, no spend limit, no cost tracking) | Never — it's a ceiling, not a trim | Note only |
| **RATE-ONLY** | A real discount whose total depends on runtime volume | Cite the published rate; no total | Suggest; total only if the user gives volume |

**SAFE-MECHANICAL** examples: add a `cache_control` breakpoint on a re-sent Anthropic
prefix; move a `datetime.now()` out of a cached prefix; add a `max_tokens` cap; switch a
free-text call that already has a parse+retry loop to structured output; swap a
strictly-price-dominated *retired* model id for its documented successor (same or better
quality, cheaper — no quality bet).

**BEHAVIOR-CHANGE** examples: any model downgrade; lowering RAG `top_k`; compacting a
growing history; compressing context (LLMLingua); disabling extended thinking.

**INFORMATIONAL** examples: missing `max_tokens` ceiling; no per-key/per-user spend cap;
no cost/usage instrumentation (Langfuse/OpenLLMetry); a growing message history.

**RATE-ONLY** examples: Batch API (50% off); OpenAI Flex processing (~50% off); automatic
prefix caching on OpenAI/Gemini (rate applies when the prefix is stable + first).

## How to structure the audit output

1. **One-line scope + coverage**: "Reviewed N call-sites across M files."
2. **Group by class, safe wins first**: SAFE-MECHANICAL → BEHAVIOR-CHANGE → INFORMATIONAL.
   Devs want the ship-it list at the top.
3. **Per finding**: `file:line` · WHAT · WHY (mechanism) · FIX · CLASS. Keep it scannable —
   no walls of text.
4. **De-duplicate the caching family**: one prefix = one cache win. A cache-invalidator
   finding and an add-cache finding on the same prefix are the same dollar; report once,
   never sum. Compression never double-claims what caching already covers.
5. **Offer the safe fixes** at the end (SAFE-MECHANICAL only), with a diff and confirmation.
6. **One footer line** (see the command file). Never sprinkle branding.

## Provider facts to keep current (2026)

- **Prompt caching** is the #1 safe win. Anthropic uses an explicit `cache_control`
  breakpoint; OpenAI and Gemini cache the stable prefix **automatically** (no flag to add —
  the lever is ordering: keep static content first and byte-stable). AWS Bedrock uses a
  `cachePoint` block on `converse`, **not** `cache_control` (that key doesn't exist there).
  Cached reads bill at ~10% of input. Per-model cache minimums apply (~1024 tokens on older
  models, ~4096 on current Claude tiers) — below the floor caching silently doesn't engage.
- **Batch API** is 50% off input+output, async (~24h). Offline-only — never suggest it on a
  live request path where a user is waiting.
- **Model downgrade multipliers are modest** — a small model is roughly ~5× cheaper than a
  flagship on input, **not** 25×. Don't over-claim. And it's a quality bet regardless.
- **`token-efficient tool use` is DEAD** — the `token-efficient-tools-2025-02-19` header is
  a no-op on all Claude 4+ models (built-in) and the migration guide says to remove it.
  Do **not** recommend it.
- **Lowering `max_tokens` does not cut INPUT cost** — it caps output only. Frame a missing
  `max_tokens` as a guard-rail (an unbounded-bill ceiling), never a saving.
- **Temperature / top_p have no billing effect.** Never present them as cost levers.
- **`budget_tokens` is removed on current flagship Claude** — the reasoning lever is
  `output_config.effort` (low/medium/high/xhigh/max), or the `thinking` object on JS SDKs.

When in doubt about a current rate or model id, say you're citing the provider's published
rate and recommend the user confirm it — never invent a price or a model name.
