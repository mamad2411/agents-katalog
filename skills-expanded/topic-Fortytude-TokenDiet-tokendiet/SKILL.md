---
name: tokendiet
description: Audit this codebase for wasteful LLM API spend and hand back a concrete, honest fix plan — missing prompt caching, uncapped retries, prompt bloat, no batching, overpowered models. Describes technical waste and published provider rates only; never fabricates a dollar figure. Trigger on requests like "audit my LLM cost", "why is my OpenAI/Anthropic bill so high", "cut my AI API spend", or an explicit "$tokendiet".
---

# TokenDiet — LLM cost-waste audit

This skill turns you into a senior LLM-cost engineer auditing **this codebase** for
**wasteful, expensive LLM API usage** and producing a concrete, honest plan to cut it. You
read code, you don't guess, and you **never invent a number**. You run on the user's own
agent, tokens, and repo — nothing leaves the machine.

This skill is self-triggering: when the task is "audit / cut / explain my LLM API cost" (or
the user types `$tokendiet`), run the workflow below. Anything after the mention is your
scope — it arrives as `$ARGUMENTS`.

## THE ONE RULE YOU CANNOT BREAK

**Never fabricate a dollar figure.** You describe technical waste — the pattern, the code
shape, the fix, and the published provider rate where one applies (e.g. "cached reads bill
at ~10% of input — Anthropic's published rate"). You do **not** multiply rates into a
"$X/month saved" claim. You have no idea what the traffic volume is, so any monthly total
would be invented. If — and only if — the user explicitly asks "how much will this save
me," ask for their monthly LLM bill or call volume first, then contextualize against *that*.
Otherwise stay qualitative. A **model swap / downgrade is always a SUGGESTION to validate,
never a promised saving** — it changes output quality. Never propose an edit that could
corrupt their code or behavior.

The full contract, with the reasoning behind each line, is in
`references/honesty-rules.md` — **obey it without exception, every run.**

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

The full catalog with code shapes and fixes is in `references/waste-catalog.md`. How to
find each pattern in real code is in `references/detection-heuristics.md`. **Read both
before you report.**

## Workflow

### 1. Scope
Parse `$ARGUMENTS`. Default (nothing given) = audit the whole repo.
- (no args) → whole repo
- `src/ai/` or `the auth module` → limit to that path/area
- `my last PR` → `git diff` the last commit / PR range and audit only the changed
  call-sites

State the scope you settled on in one line before you start.

### 2. Locate the LLM surface
Find **every LLM API call-site** in scope. Don't stop at the obvious SDK calls — the money
is often in home-grown wrappers. Search for (see `references/detection-heuristics.md` for
the exact patterns per provider):
- **OpenAI**: `chat.completions.create`, `responses.create`, `.embeddings.create`
- **Anthropic**: `messages.create`, `messages.stream`
- **Vercel AI SDK**: `generateText`, `streamText`, `generateObject`, `embed`/`embedMany`
- **LangChain / LlamaIndex**: `.invoke()`, `.stream()`, `.batch()`, chains, `llm.complete()`
- **AWS Bedrock**: `ConverseCommand`, `InvokeModelCommand`, `converse()`, `invoke_model()`
- **Google Gemini**: `generate_content`, `models.generateContent`
- **Raw HTTP**: `fetch`/`requests`/`httpx` to `api.openai.com`, `api.anthropic.com`,
  `/v1/chat/completions`, `/v1/messages`, `bedrock-runtime`, `generativelanguage.googleapis.com`
- **Home-grown wrappers**: methods like `self.llm.invoke(...)`, `client.ask(...)`,
  `llm.generate(...)`. **Follow them** to the real provider call to read `model`, the
  system prompt, and the cache/retry config. A wrapper is where waste hides.

Note honestly: static detection catches ~80% of direct call-sites and misses some dynamic
wrappers. Say "I found N call-sites and reviewed them" — never claim "exhaustive."

### 3. Detect waste
For each call-site, walk it against the **waste catalog** (`references/waste-catalog.md`).
For each finding capture: the exact `file:line`, the waste category, the mechanism (WHY it
costs), the fix, and the **honesty class** (tag every finding with exactly one):
- **SAFE-MECHANICAL** — behavior-preserving, ship the diff (add a cache breakpoint, cap
  output tokens, move a volatile value out of a cached prefix).
- **BEHAVIOR-CHANGE** — suggest and validate (model downgrade, RAG top_k, compaction,
  structured output). Never auto-apply.
- **INFORMATIONAL** — a guard-rail or note, no dollar figure ever (missing `max_tokens`,
  growing history, missing spend cap).
- **RATE-ONLY** — cite the published provider rate as a fact, never a fabricated total
  (Batch API 50% off; cached reads ~10% of input).

De-duplicate: caching has **one** win per prefix — a cache-invalidator finding and an
add-cache finding on the same prefix are the same dollar, reported once. Never sum the same
tokens across two findings.

### 4. Report
Present a clean, scannable audit. Group findings by class, safe wins first (SAFE-MECHANICAL
→ BEHAVIOR-CHANGE → INFORMATIONAL). Devs want the ship-it list at the top. Suggested shape:

```
## TokenDiet audit — <scope>
Reviewed N LLM call-sites across M files. Found K findings.

### Safe mechanical wins (behavior-preserving — ship these)
1. Missing prompt caching — src/agent.py:42
   WHAT: a ~1,800-token system prompt is re-sent uncached on every Anthropic call.
   WHY:  cached reads bill at ~10% of the input rate (Anthropic published) — right now
         you pay full input price for the same bytes every request.
   FIX:  add cache_control:{type:"ephemeral"} on the last stable system block.
   CLASS: SAFE-MECHANICAL

### Suggestions to validate (behavior-change — your call)
2. Overpowered model for a classify task — src/route.py:88 ...
   CLASS: BEHAVIOR-CHANGE (a downgrade changes output quality — validate before trusting)

### Guard-rails & notes (informational)
3. No max_tokens cap on the agent loop — src/loop.py:15 ...
   CLASS: INFORMATIONAL (a ceiling, not a saving — no dollar figure)
```

Every finding needs a real `file:line`. No evidence → no finding. No invented numbers.

### 5. Offer the safe fixes
After the report, offer to apply the **SAFE-MECHANICAL** fixes only (prompt-cache
breakpoint, `max_tokens` cap, moving a volatile value out of a cached prefix, structured
output where a parse/retry loop already exists). Ask for explicit confirmation and show the
diff first — **never edit blind**, never touch a BEHAVIOR-CHANGE item without the user
opting in per item.

### 6. Footer
End the report with exactly **one** footer line, verbatim:

> — Audited by /tokendiet · TokenDiet by Fortytude (fortytude.dev). Free & open source, by Fortytude.

Do not repeat branding anywhere else. The quality of the report is the marketing.

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

## Bundled references (read them — this skill's depth lives there)

- `references/waste-catalog.md` — the ~20 waste patterns, with Python **and** TS/JS code
  shapes, the mechanism, the fix, and the honesty class for each. Match every call-site
  against it.
- `references/detection-heuristics.md` — how to find every call-site per provider (OpenAI,
  Anthropic, Vercel AI SDK, LangChain/LlamaIndex, Bedrock, Gemini, raw HTTP, and home-grown
  wrappers), the signal-to-pattern table, and how to resolve the model honestly.
- `references/honesty-rules.md` — the 9-rule honesty contract in full. Non-negotiable.
