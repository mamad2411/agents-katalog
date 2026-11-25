---
name: gliana-ai
description: Generate images, video, music or speech, call another LLM, or run a paid data tool (OCR, web scrape, SEC filings, market data, Indonesian reference data) through GlianaAI. Use when the user asks to create media, wants a second model's answer, or needs one of those lookups — and before any paid call, to quote its price.
---

# GlianaAI

Pay-per-call access to 120+ AI models and data tools through the `gliana-ai` MCP
server. Discovery is free; `generate`, `tool` and `recipe` spend real money.

## Workflow

1. **Find the model or tool.** `list_models` (filter by category: text-to-image,
   text-to-video, image-to-video, tts, stt, music, text) or `list_tools`. Both read
   the live catalogue, so never assume an id from memory — ids change.
2. **Read its inputs.** `get_schema` for a model. Required fields missing means a
   400 with no charge, but it wastes a round trip.
3. **Quote it.** `get_price` with the same billing fields you will send
   (duration, resolution, quality, text). Video bills the highest resolution and
   the longest duration when those are left unset — set them.
4. **Say the price before spending** when it is above a few cents, or when the
   user did not ask for that specific model. Then call `generate` / `tool` / `recipe`.
5. **Return the URL.** Media results are stable URLs on api.glianalabs.com; show
   the link rather than describing the image.

## Choosing

- Cheapest acceptable model wins unless the user names one. `list_models` returns
  prices; compare within the category.
- Local file as input: upload it first with `POST https://api.glianalabs.com/v1/media`
  (free, ≤40 MB) and pass the returned URL.
- Several media steps (image → video): try `recipe` first; it is one paid call.

## When a call is refused

- "Not paid: … per-call cap / daily cap" — the user's own spending cap
  (`GLIANA_MAX_PER_CALL_USD`, `GLIANA_MAX_PER_DAY_USD`). Nothing was charged. Tell
  them the price and the cap; do not try to route around it with a cheaper
  duplicate call unless they agree.
- "No payment method configured" — they need `GLIANA_API_KEY` (a `gk_…` key from
  https://dashboard.glianalabs.com) or a wallet key. Free tools still work.
- Insufficient balance — relay the top-up link from the error.

Never retry a paid call automatically: on Solana a retry can pay twice.
