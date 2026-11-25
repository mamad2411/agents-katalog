---
name: trend-radar
description: Scheduled Monday-morning trend radar — scans the user's chosen topic for 5 fresh signals, each triangulated across 2+ independent sources, with a so-what and suggested action per signal. Use when the user asks to "run my trend radar", "what's new in <my space> this week", "set up weekly market monitoring", or wants recurring awareness of a topic. Don't use for a one-off deep dive on a single competitor — that's competitor-teardown — or for sizing the market — that's market-sizing-tam.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, Trends, Monitoring, Automation]
    related_skills: [competitor-teardown, market-sizing-tam, seo-content-audit]
    requires_toolsets: [web]
    blueprint:
      schedule: "0 8 * * 1"
      prompt: "Run my weekly trend radar"
---

# Trend Radar

A blueprint skill: every Monday at 08:00 it scans the user's chosen topic and delivers exactly 5 signals — each triangulated across at least 2 independent sources, dated, and finished with a so-what and one suggested action. The standard: a signal with one source is a rumor and doesn't ship; a signal without a so-what is noise wearing a suit. Read-only web work, safe to run unattended.

## When to Use

- The Monday scheduled run (automatic via the blueprint above).
- Ad-hoc: "what happened in <topic> this week?", "run the radar now".
- Setting up: user names a topic they want watched weekly.
- **Not for:** deep single-company analysis (`competitor-teardown`); market size math (`market-sizing-tam`); auditing one page (`seo-content-audit`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Fresh news | web search: `<topic> ("launched" OR "announced" OR "raised" OR "shut down")`, filter to last 7–14 days |
| Community pulse | search `<topic> site:reddit.com` and `site:news.ycombinator.com` — sort/filter recent |
| Primary sources | `web_extract` the actual announcement/changelog/paper, not the article about it |
| Triangulate | second independent source per signal — different outlet/author, not a syndication |
| Date check | every source needs a publish date within the window; undated → doesn't count |
| Memory | compare against last week's radar (from notes/memory) to catch signal evolution |

## Procedure

1. **Precheck (first run only)** — confirm with the user: the topic (specific enough to search — "AI agents for real-estate teams", not "AI"), 3–6 seed sources they trust, and what decisions the radar feeds (build/marketing/investing). Store in memory. On scheduled runs, load these and go; if topic config is missing, deliver a setup request instead of a generic scan.
2. **Sweep** — run 4–6 searches: the news pattern, the community pattern, the seed sources' recent output, and one wildcard angle ("<topic> problems", "<topic> alternatives"). Collect candidate items with URL + publish date. Window: 7 days (stretch to 14 if thin, and say so).
3. **Shortlist** — keep candidates that are new (not in last week's radar), dated inside the window, and relevant to the user's stated decisions. Drop press-release fluff with no substance.
4. **Triangulate** — for each shortlisted item, find a second independent source (different outlet or the primary source itself). Syndicated copies of the same wire story count as one source. Can't find a second? The item ships only if flagged `single-source — unconfirmed`, and at most one such item per radar.
5. **Rank to 5** — score by relevance to the user's decisions × strength of evidence. Exactly 5 signals: fewer available means saying "quiet week — N real signals" rather than padding; more means the rest go in a one-line "also noticed" footer.
6. **So-what and action** — per signal, one sentence on why it matters *to this user*, and one concrete suggested action (test, post, outreach, watch-item) with a confidence label. Generic advice ("keep an eye on this") is banned.
7. **Deliver** — fill the template, save this week's signal list to memory for next week's comparison, and send through the run's normal delivery channel. On any failure (web down, no config), still deliver a short note saying why — the radar is never silently absent.

## Output Template

```
# Trend Radar — <topic> — week of <date>
Window: <dates> | Searches run: N | Candidates: N → shipped: 5

## Signals
1. **<headline in plain words>** (<date>)
   Sources: <url1> + <url2> [or: single-source — unconfirmed]
   So what: <why this matters to YOUR decisions>
   Suggested action: <one concrete step> (confidence: high/med/low)
2–5. ...

## Movement since last week
- <signal from a past radar that advanced/died — or "first run, no baseline">

## Also noticed
- <one-liners that didn't make the cut>
```

## Pitfalls

- **Old news dressed as new** — search surfaces a 2024 article and it reads like this week's signal. Recovery: hard date-check every source; undated pages are excluded; the radar header states the window and every signal carries its date.
- **One press release echoing across ten outlets** — looks triangulated, is actually one source syndicated. Recovery: triangulation requires independent authorship — check bylines and quoted material; syndications collapse to one.
- **Topic drift** — after a few weeks the radar quietly becomes generic industry news. Recovery: re-read the stored decision context each run; every so-what must reference the user's decisions, and a quarterly line asks the user if the topic config still fits.
- **Padding a quiet week** — 5 signals demanded, 2 exist, 3 get invented from thin air. Recovery: quiet weeks report honestly ("2 real signals this week"); credibility of the radar is worth more than the count.
- **Scheduled run fails silently** — web toolset hiccup means no Monday radar and nobody notices for a month. Recovery: on any failure, deliver a one-line failure note with the reason and the fix, so absence is always visible.

## Verification

- [ ] Exactly 5 signals or an explicit "quiet week" count — never padded
- [ ] Every signal: 2+ independent sources with URLs and dates inside the window (max one flagged single-source)
- [ ] Every so-what references the user's stored decision context
- [ ] Every action is concrete and confidence-labeled
- [ ] This week's signals saved to memory; last week's compared
- [ ] Failure note delivered if the run couldn't complete
