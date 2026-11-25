---
name: botkits-overheard-setup
description: >-
  Needs Grok Bot. First-run watch-list interview. Also use when the user wants to reconfigure
  names, brands, URLs, or sources.
compatibility: Needs Grok Bot (sets up the Overheard Grok Bot).
---
# Overheard setup

Run on first import, or whenever the user wants to change what Overheard watches.

## Goal

End with: the watch list and source choices saved to memory, a profile Description that uses the user's real names (no `[NAME]`, `[BRAND]`, or `[SITE_URL]` left behind), a paused weekday routine, one ask to turn it on, and the starter menu.

## Opening

One line: Overheard finds third-party mentions on weekdays and stays quiet when nothing clears the bar. No "what do you want an assistant for?". No Create, Export, Harden, or Tweak cards.

## Questions (one per message)

1. The name to track, plus common misspellings.
2. Brands, products, newsletter or podcast names.
3. Their own sites and handles, which are excluded from results.
4. Terms that cause false hits (a brand that is also a common word) and words to exclude with it.
5. Sources. Default on: Reddit, Hacker News, news, X. Opt-in: YouTube, Instagram, TikTok.
6. What clears the bar (optional). Default: any real third-party mention.
7. Digest time. Default 8:30 local, weekdays.

## Then

1. Save to memory: watch list, misspellings, exclusions, own sites and handles, sources, bar, digest time, dead-day rule, chat-only delivery, and the ledger path `/workspace/overheard-YYYY-MM-DD.md`.
2. Rewrite the profile Description in a short public form with their real details.
3. Create the routine `Daily mention monitor` on weekdays at their time (default `30 8 * * 1-5`) with `enabled=false`, and put the watch list, exclusions, and sources in its prompt. Ask once whether to turn it on.
4. Offer a sample digest now so they can tune the bar before the first scheduled run.
5. If X or Slack connectors are available, mention once that X improves coverage and Slack allows channel delivery. Neither is required.
6. Show the menu: Run sample digest now, Edit watch list or sources, Enable weekday monitor, Skip for now. Close with one "ready" line.

## Later

If memory already has a watch list, skip the questions; short hello and the same menu. Ask again only if the user wants changes or memory is empty.

## Inspired by

- [Lenny Rachitsky, Overheard](https://x.ai/bot/marketplace/bots/overheard) (marketplace template; no reuse license shown, so no text is copied). Does well: an interview before anything runs, a paused routine with a single ask to enable, and no leftover placeholders. Missing: its listing doesn't ask about misspellings or ambiguous terms that cause false hits.
- [F5Bot](https://f5bot.com/). Does well: setup is just keywords plus filters such as excluded terms and required co-occurring words. Missing: no interview; the user has to know which filters they need.
- [Google Alerts help](https://support.google.com/websearch/answer/4815696?hl=en). Does well: frequency, sources, language, and region set per alert. Missing: no step that tests the alert before it starts sending.

## What this version adds

- Misspellings and false-hit exclusions in the interview.
- A sample digest before the first scheduled run, to tune the bar.
