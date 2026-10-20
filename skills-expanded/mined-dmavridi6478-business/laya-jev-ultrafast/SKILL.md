---
name: laya-jev-ultrafast
description: Laya (Apache-2.0, a free open decision engine that answers typed pick-one, score and yes/no questions in one forward pass on your own machine) and Jev Ultrafast (Browser Use's MIT web agent built on TypeSafe's Jev), each cloned and checked, with the install routes, what each really needs (a TypeSafe key for Jev Ultrafast; an extra text-model key for typing), and the caveats the slides leave out (zero-shot accuracy varies beyond about 4,000 tokens; fine-tune on your own decisions). Use alongside jev-vs-llm when choosing a hosted or self-hosted decision model, or before running either repo.
---

# Laya and Jev Ultrafast

Source: two @aiclawbots slides in a week-of-trending-repos carousel. Repos cloned and read on 4 October 2026. Nothing was installed or run. Star counts are as printed on the slides and are unverified.

| Repo | Slide figures | Licence | Last commit |
|---|---|---|---|
| `NandhaKishorM/laya` | 24,091 stars, 2,072 forks, +20.1k this week | Apache-2.0 | 2026-10-05 |
| `browser-use/jev-ultrafast` | 20,079 stars, 1,355 forks, +8.3k this week | MIT | 2026-09-18 |

## Laya

A non-autoregressive "System 1" decision engine: typed decisions (pick one, score, yes/no) over 100+ languages in a single forward pass, about 33 ms per its README. Install: `python -m pip install laya` (Python 3.10+). Extras listed in the README include `laya[serve]` (HTTP server), `laya[mcp]` (an MCP server), and LangChain, LlamaIndex and CrewAI integrations; a TypeScript package exists as `laya-ts`.

- **The slide says** it runs free on your laptop; minutes to load the first time, then 24 to 29 ms per answer, no GPU. Plausible against the README; not timed here.
- **Accuracy caveat from its own README:** on its test, 16 to 18 of 20 requests were right with up to about 4,000 tokens of text, and 8 to 17 of 20 beyond that. Check long-document accuracy yourself. [Certain]
- **Zero-shot works, fine-tuning is where accuracy jumps** (README, with a notebook). Plan to label examples from your own domain.
- **Release timing:** the slide says it appeared the same day as TypeSafe's Jev; a web article gives 18 September. I did not resolve the difference. Search-result figures (about 19.3k stars, 421M parameters) are secondary and unverified.

## Jev Ultrafast

Give it one goal. Jev picks the next operation and element from a numbered list of what is on the page; a small LLM writes text only when the operation is typing. The slide's demo: a Zurich to London flight search in 7.1 seconds.

- **What it needs, from its README:** `uv sync`, then `uv run jev`, with a `TYPESAFE_API_KEY` and a `TEXT_MODEL_API_KEY` (OpenRouter in the example). It connects to your real Chrome through Browser Harness. The slide prices Jev at $42 per billion input tokens with early access; that equals $0.042 per million and matches the published Jev price (see `jev-vs-llm`). The slide says the agent "won't run until you add the keys". [Certain]
- **Risk:** it clicks and types in your own browser. Run it in a separate Chrome profile with nothing logged in that you cannot afford to have clicked. Do not point it at banking, admin or purchase pages. A decision model can be steered by page text (injection). [Certain]
- The README also advertises a Browser Use Cloud waitlist.

## Which to use

| Need | Pick |
|---|---|
| Typed classification or routing, offline, no per-call fee | Laya, after measuring it on 50 to 200 of your own labelled cases |
| Fast browser automation and you accept a vendor key | Jev Ultrafast, in an isolated browser profile |
| Both and unsure | Start with Laya for the decision, keep the action in your own code |

A probability never authorises an action by itself; see `jev-vs-llm` for the test procedure.
