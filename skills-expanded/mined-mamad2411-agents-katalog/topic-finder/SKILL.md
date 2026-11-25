---
name: topic-finder
description: "Find fresh, relevant content topics for a creator's niche by pulling real headlines from web search and RSS feeds, deduping them, and handing the batch to the headline-virality-scorer for ranking. USE THIS SKILL when the user asks 'what should I post/make a video about', 'find me trending topics', 'what's happening in my niche', 'give me content ideas', 'what's worth covering this week', or otherwise wants topic/headline candidates SOURCED for them (not just scored). Defaults to an AI / tech / software / useful-apps niche but works for ANY niche the user names. Pairs with headline-virality-scorer: this skill fetches the candidates, that skill scores them."
---

# Topic Finder

Source fresh headline candidates for a creator's niche, then rank them for content potential. This is the **fetch** half of the content-idea pipeline; `headline-virality-scorer` is the **judge** half. This skill's job is to get real, current headlines into a clean list and hand them off.

## When this triggers

The user wants topics *found* for them — "what should I make content about", "what's trending in AI this week", "find me video ideas" — as opposed to pasting headlines they already have (that's a pure scorer job).

## Inputs

- **Niche / audience** (optional): default to **AI, tech, software engineering, and useful apps/software**. If the user names a niche ("home fitness", "personal finance", "indie game dev"), use that instead — this skill is niche-agnostic.
- **Sources** (optional): default to both web search and the RSS feeds in `feeds.txt`. User can restrict to one.
- **Timeframe** (optional): default to the last 7 days; treat older items as stale unless evergreen.
- **Count** (optional): default surface the top ~10 after scoring.

## The pipeline

Run these steps in order.

### 1. Fetch candidates

**RSS feeds** — run the fetch script:

```
python3 scripts/fetch_rss.py --feeds scripts/feeds.txt --max-per-feed 15 --since-days 7
```

It prints one JSON array of `{title, source, url, published}`. Edit `scripts/feeds.txt` to match the niche — it ships with strong AI/tech/software defaults. For a different niche, swap in that niche's feeds (one URL per line; `#` comments allowed).

**If the script's network is blocked** (some sandboxes allowlist outbound traffic — you'll see `403`/tunnel errors for every feed), don't abandon RSS. Instead fetch each feed URL with the `web_fetch` tool (or `WebFetch`), save the returned XML to a local file, and point the script at a `file://` path — the parser handles the XML the same way. Or just lean more on the WebSearch step below. Note which path you used.

**Web search** — also run 3–6 `WebSearch` queries tuned to the niche and timeframe, e.g. `"AI" news this week`, `new developer tools July 2026`, `<niche> launches this week`. Pull headline + source + URL from results.

Combine both sources into one candidate list. Prefer real, current items — do not invent headlines.

### 2. Dedup and clean

- Drop near-duplicate titles (same story from multiple outlets) — keep the clearest one, note the dupes exist.
- Drop pure press-release fluff, listicles older than the timeframe, and off-niche noise.
- Keep the source and URL on every item so the final output is traceable.

### 3. Score via headline-virality-scorer

Hand the cleaned batch to the **headline-virality-scorer** skill, passing the niche so it scores relevancy correctly. Let that skill produce the ranked table, top-3 detail, hooks, and JSON.

### 4. Deliver

Return the scorer's ranked output, but **each row must carry its source + URL** so the user can click through to the original story. Lead with the top handful of actual opportunities, not process narration.

## Notes

- **Freshness matters here** (unlike the pure scorer, which scores from intrinsic properties). Since topics are being sourced for immediate posting, prefer recent items and flag anything that may already be stale.
- If web search or a feed fails, continue with what you have and say which source came up short — don't block the whole run.
- This skill deliberately does not re-implement scoring; keep all scoring logic in `headline-virality-scorer` so there's one source of truth.
- To run this automatically, wrap it in a scheduled task (e.g. daily 7am): "Run topic-finder for my AI/tech niche and give me the top 10."
