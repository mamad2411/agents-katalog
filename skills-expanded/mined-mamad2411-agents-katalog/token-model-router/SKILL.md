---
name: "token-model-router"
description: "Auto right-size model: 80% task pakai flash/mini (10-50x lebih murah), hanya task reasoning/code-complex pake model besar. Invoke sebelum SETIAP LLM call pilih model."
---

# Token Model Router — Cost-Routing Engine (30× cost cut avg)

## Decision Matrix (apply BEFORE every LLM call)
Classify the INTENDED task into 1 of 5 tiers, pick the CHEAPEST model that can reliably complete it.

```
╔═════════╦══════════════════════════════════════════════╦══════════════════════════════════════════╗
║  TIER   ║  DESCRIPTION & EXAMPLES                      ║  MODEL PICK (cheapest first)             ║
╠═════════╬══════════════════════════════════════════════╬══════════════════════════════════════════╣
║  TINY   ║  2–5 word answers; boolean; multiple choice ║  ministral-3b, llama3.1-8b, gpt-4o-mini ║
║         ║  reformat, regex, fix 1-line, classifying    ║  (≈ 30–50× cheaper than flagship)       ║
╠═════════╬══════════════════════════════════════════════╬══════════════════════════════════════════╣
║  SMALL  ║  Write <300 words, summarize short, extract ║  gpt-4o-mini, devstral-medium, haiku-3   ║
║         ║  from structured, translate, basic scripts  ║  (≈ 15–30× cheaper)                     ║
╠═════════╬══════════════════════════════════════════════╬══════════════════════════════════════════╣
║  MEDIUM ║  Code write <200 lines, debug non-obscure,  ║  sonnet-4, gpt-4o, mistral-large-2512   ║
║         ║  <1500 word write, multi-step analysis      ║  (≈ 3–8× cheaper than flagship)         ║
╠═════════╬══════════════════════════════════════════════╬══════════════════════════════════════════╣
║  LARGE  ║  Deep reasoning, hard math, novel code      ║  opus-4, o1, gemini-2.5-pro              ║
║         ║  architecture, legal, 2000+ word synthesis  ║  (full price — use sparingly)           ║
╠═════════╬══════════════════════════════════════════════╬══════════════════════════════════════════╣
║  XL+    ║  RESEARCH-GRADE only; novel theorem, audit  ║  Best available model, rate limit 1/hr   ║
║         ║  of complex systems, 10k+ line refactor     ║  User must type NEED_XL explicitly       ║
╚═════════╩══════════════════════════════════════════════╩══════════════════════════════════════════╝
```

## Explicit Downgrade Path (ALWAYS try smaller FIRST, escalate only on failure)
1. Try TIER ≤SMALL for ANY task unless user explicitly typed: `need_large`, `need_expert`, `complex`
2. If result is clearly wrong / truncated / 4/5 self-check questions fail → escalate ONE tier up, retry SAME prompt
3. 2 escalations max; if still fails, ask user notifying cost implication

## Provider Routing Preference
When multiple providers support equivalent model tier:
```
1. Self-hosted (Ollama/port 11434) / localhost (free) → ALWAYS try first for TINY/SMALL
2. xKiro mistralai/minstral-3b → devstral-medium (cheapest via omniroute:9router)
3. LiteLLM cached / prompt-caching eligible endpoints (4026 limit workaround!)
4. OpenAI / Anthropic official endpoints — only when (1-3) fail
```

## Output Annotation (every LLM call)
Append the following 1 line AFTER EVERY final assistant response (so user can verify cost discipline is active):
```
🧭 routed:[tier:SMALL|model:mistral-large-2512|cost:~$0.0012|vs_flagship_saved:94%]
```

## Hard Guard
> **Flagship model (LARGE/XL+) usage should be < 15% of total LLM calls in any session.**
> If you exceed 20%, invoke `token-budget-guard:hard_stop` and notify user.
