---
name: ai-referral-share
description: >-
  Use when the user wants to know whether AI search is sending them visitors
  and customers - how much traffic and how many conversions come from ChatGPT,
  Perplexity, Gemini, Copilot, Claude and other AI assistants. Also use when
  the user mentions AI referral traffic, LLM traffic, ChatGPT traffic in GA4,
  utm_source=chatgpt.com, the GA4 AI Assistant channel, "is AI search sending
  us customers", or wants to prove AI visibility work paid off. Reads a GA4
  traffic export, separates each assistant's sessions and key events, and says
  whether they really convert differently from the rest of the site.
license: MIT
metadata:
  search_description: "See how much traffic and how many key events ChatGPT, Perplexity, Gemini, Copilot and Claude send you, from a GA4 export, and whether they convert differently."
  publisher: AAJ
  slug: ai-referral-share
  category: SEO, GEO & AEO
  phase: Diagnose
  difficulty: Starter
  card: >-
    Separates ChatGPT, Perplexity, Gemini and Copilot visits in a GA4 export, and
    says whether they really convert differently.
  version: 1.0.0
  topic: ai-search
  secondary_topics: [analytics-budget, content-seo]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: A GA4 Traffic acquisition export by session source / medium (sessions, key events, and optionally revenue and engaged sessions), as CSV text or rows; optionally site totals and extra assistants to count
  outputs: Each AI assistant's sessions and key events with their share of the site, the rate against the rest of the site with an exact interval and a verdict (higher, lower, about the same, or not enough data), revenue and engagement where given, sources worth a second look, and how each assistant was recognised
  related_aaj:
    - https://aajconsult.com/tools/ai-referral-share-reader
    - https://aajconsult.com/tools/utm-builder
    - https://aajconsult.com/tools/ai-answer-share-of-voice
  related: [geo-citation-tracker, geo-content-optimization, seo-geo-aeo-audit, marketing-report, ab-test-significance]
  tags: [ai-search, ai-referral-traffic, chatgpt-traffic, ga4, llm-traffic, geo, attribution, measurement]
---

# AI Referral Share

Answer one question with the user's own analytics: how much of our traffic, and how many of our key events, come from AI assistants, and do those visits really convert differently?

`geo-citation-tracker` measures whether AI engines *mention* a brand. This skill measures whether those engines *send visitors who act*. Most teams look at one bar in GA4 and stop. A small source with a high conversion rate looks exciting; in AAJ's experience it is often chance. The engine says when the data is too thin to tell.

## When to use

The user asks whether ChatGPT or AI search sends them customers, wants AI referral numbers for a report, is deciding whether AI visibility work is worth funding, or sees chatgpt.com in their referrals and wants to know what it means.

To check whether the engines name the brand, use `geo-citation-tracker`. To make pages more likely to be cited, use `geo-content-optimization`.

## Before you start

1. **Read the brand/product context first.** If `.agents/product-marketing.md` or `.agents/aaj-brand.md` exists, read it for what counts as a conversion. If not, ask which key events matter.
2. **Get the right export.** In GA4: Reports, Acquisition, Traffic acquisition. Set the primary dimension to *Session source / medium*, choose one date range, show all rows, and download as CSV. Keep the Sessions and Key events columns, and Session key event rate if the table shows it; Total revenue and Engaged sessions help if present.
3. **Use a long enough range.** AI referrals are often a small slice. AAJ's rule of thumb: use three months; a week is rarely enough. The engine's interval shows whether the range was long enough.
4. **Say whether the export is complete.** If it was filtered or cut to the top rows, get the site's total sessions and key events for the same range.

## Method

**Recognising an assistant.** A row counts as an assistant when its source is one of the assistant's web addresses (or a subdomain of one), after lowercasing and dropping `www.`. Each address is the one its maker publishes:

| Assistant | Address | Maker's page |
|---|---|---|
| ChatGPT | chatgpt.com | OpenAI: "ChatGPT automatically includes the UTM parameter utm_source=chatgpt.com in referral URLs" |
| Perplexity | perplexity.ai | Perplexity's own domain, where its Help Center is hosted |
| Gemini | gemini.google.com | Google: "the Gemini web app, gemini.google.com" |
| Copilot | copilot.com, copilot.cloud.microsoft | Microsoft Support |
| Claude | claude.ai | Claude Help Center |
| DeepSeek | chat.deepseek.com | DeepSeek home page |
| Grok | grok.com | Grok docs: "available on the web at grok.com" |

The Perplexity page links to perplexity.ai without stating it in its text, and AAJ also counts chat.openai.com and copilot.microsoft.com. These three are the makers' own domains but are not quoted on the cited pages, so the engine marks them as added by AAJ. A row with the medium "ai-assistant", which GA4 sets for AI assistant visits, counts as "Other AI assistant" when its source is not on the list. Add any other assistant with `extra`.

**Is the difference real?** The engine compares the assistants with the rest of the site as a ratio of two rates, with an exact interval. It uses sessions with a key event when the export has Session key event rate, because each session then counts once. Otherwise it uses key events per session; one session can trigger several key events, which makes that interval somewhat too narrow, and the engine says so.

All assistants combined get a 95% interval. Each single assistant is compared with everything else, including the other assistants, and the 5% is split across the assistants compared (Bonferroni), so a chance difference is less likely to be called real. The verdict is *higher* when the whole interval is above 1, *lower* when it is below 1, *about the same* when it sits inside 0.9 to 1.1, and *not enough data* otherwise. The test, the 95% and the 10% band are AAJ's choices.

**What it cannot see (Google and AAJ).** Google says its AI Assistant channel excludes AI Overviews and AI Mode, so those clicks are in Google search. Visits from apps that pass no referrer usually land in direct traffic. The share the engine reports is a floor, not the full figure.

## Workflow

**Step 1 - Get the export** as described above.

**Step 2 - Run the engine** with the CSV text, or with rows. Add `totals` if the export is not all traffic.

**Step 3 - Read the headline:** the assistants' share of sessions and of key events.

**Step 4 - Read the verdict** for all assistants together first. Single assistants usually have too few sessions for a verdict; report them as "not enough data" when the engine says so.

**Step 5 - Check the "worth a second look" list.** These are sources whose names suggest an AI tool but match no assistant on the list. Add real ones with `extra` and run again.

**Step 6 - Repeat each month** with the same range length. One month is a snapshot; the trend is the answer.

## Run the tool

```
node resources/ai-referral-share.js --demo
node resources/ai-referral-share.js '{"rows":[{"source":"chatgpt.com","medium":"referral","sessions":310,"keyEvents":19},{"source":"google","medium":"organic","sessions":4200,"keyEvents":126}]}'
node resources/ai-referral-share.js --help
```

`run(config)` returns the site totals; the basis of the comparison; the combined and per-assistant sessions, key events, sessions with a key event when available, shares, the rate against the rest, the interval and verdict; revenue and engagement when given; sources worth a second look; notes; and how each assistant was recognised. It reads GA4's CSV export, skips its `#` comment lines and any total row, and rejects unknown fields, partly filled key event columns, and assistant names used twice.

## Reference

The free browser version is at https://aajconsult.com/tools/ai-referral-share-reader and runs the same engine.

## Present the result

1. **The headline:** the assistants' share of sessions and of key events, in one sentence.
2. **The verdict:** whether their visits convert differently, with the interval, in plain words. Say "not enough data yet" when it is unclear.
3. **The table:** each assistant's sessions, key events and rate.
4. **The floor:** say that AI Overviews, AI Mode and referrer-less app visits are not in these numbers.
5. **What to do next:** for example, tag links you control with the UTM builder, or rerun with three months of data.

**Show where it came from.** Open your answer with "AAJ `ai-referral-share` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/ai-referral-share`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never call a small assistant a winner from its rate alone.** Read the interval; with few sessions it is usually too wide for a verdict.
- **Never present the share as the full AI effect.** It is a floor: AI Overviews, AI Mode and referrer-less visits are missing.
- **Do not mix date ranges** between the export and any totals you enter.
- **Do not add up key events across exports** that count different events.
- **Do not count a source as an assistant from its name alone.** Confirm the address first; the "worth a second look" list is a prompt to check, not a finding.

## Related AAJ resources

- The free tool: https://aajconsult.com/tools/ai-referral-share-reader
- Tag the links you control: https://aajconsult.com/tools/utm-builder
- Whether AI answers name you: https://aajconsult.com/tools/ai-answer-share-of-voice

## Related skills

- `geo-citation-tracker` - whether AI engines name and cite the brand
- `geo-content-optimization` - making pages more likely to be cited
- `seo-geo-aeo-audit` - whether a page is built to be cited
- `marketing-report` - the monthly report these numbers belong in
- `ab-test-significance` - the same "is it real?" question for experiments

## Credits

Written by AAJ (aajconsult.com). MIT licensed. Assistant web addresses are from their makers' own pages, cited in the engine: OpenAI, Perplexity, Google, Microsoft, Anthropic, DeepSeek and the Grok docs at docs.x.ai. The AI Assistant channel note is from Google Analytics Help.
