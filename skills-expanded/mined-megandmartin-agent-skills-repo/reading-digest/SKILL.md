---
name: reading-digest
description: Turns a backlog of saved links into a prioritized reading digest — relevance-ranked, three-sentence summaries, and a read/skim/skip verdict for each. Use when the user says "digest my reading list", "summarize these links", "what's worth reading here", "clear my saved tabs", or pastes a pile of URLs. Don't use for deep multi-source research on one question — use a research workflow — or for the daily schedule brief — use morning-brief.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Reading, Research, Digest]
    related_skills: [morning-brief, weekly-review, file-organizer]
    requires_toolsets: [web]
---

# Reading Digest

Takes the guilt pile — 15 saved links nobody will ever "get to" — and converts it into a ranked digest with honest verdicts: read this one properly, skim these three, skip the rest and here's why. The standard: every summary comes from actually fetched content, never from what the headline implies, and "skip" is a first-class recommendation, not a failure.

## When to Use

- User has a list of saved links (text file, bookmarks export, pasted URLs) and wants to know what deserves attention.
- Weekly reading-list cleanout; prepping reading for a flight.
- **Not for:** answering one research question across many sources (that's a research task, not a digest). Not for daily news/calendar — use `morning-brief`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Load the list | `read_file` the links file, or take pasted URLs |
| Count + dedupe | `python3 -c "urls=[l.strip() for l in open('links.txt') if l.strip().startswith('http')]; print(len(urls), len(set(urls)))"` |
| Fetch an article | `web_extract` on the URL (the web toolset) |
| Fallback fetch | `curl -sL --max-time 15 "URL" \| head -c 4000` |
| Verdict scale | **Read** (whole thing, soon) · **Skim** (intro + headers) · **Skip** (with reason) |
| Save the digest | `reading-digest-<YYYY-MM-DD>.md` |
| Reading-time estimate | `python3 -c "print(round({word_count}/230))"` — minutes at ~230 wpm |
| Detect a paywall wrapper | fetched text < ~400 chars or contains "subscribe to continue" |

## Procedure

1. **Precheck** — get the link list and dedupe it (python3 one-liner). Ask one calibration question if you don't already know it: what is the user optimizing for right now (current projects, interests, deadlines)? Relevance ranking is meaningless without a "relevant to what".
2. **Fetch** — pull each URL with `web_extract` (curl fallback). Record per link: title, source, length estimate, publish date if visible. Paywalled or dead links aren't skipped silently — they go in the digest marked "couldn't fetch" with whatever the metadata reveals.
3. **Summarize** — for each fetched piece, exactly three sentences: (1) what it actually says/claims, (2) the strongest specific point, insight, or number in it, (3) who it's for / what you'd do with it. Summaries come from fetched text only — if you only got the intro, say so.
4. **Rank + verdict** — order by relevance to the user's stated priorities, factoring freshness and substance-per-minute. Assign Read / Skim / Skip. Be ruthless and honest: a well-written but irrelevant piece is a Skip; a clumsy but load-bearing one is a Read. Every Skip gets a one-clause reason so the user can overrule.
5. **Deliver** — top 3 "Read" items first with time estimates, then Skims, then Skips as a compact list. Close with the total: "reading the Reads costs ~{N} min; you just saved ~{M} min of backlog guilt." Save the file. Offer (don't do unprompted) to clear the processed links from the source list — never delete without an explicit yes.

## Output Template

```
# Reading Digest — {date} · {n} links → {r} read / {s} skim / {k} skip
Ranked for: {user's stated priorities}

## 📖 Read ({r}) — ~{N} min total
### 1. {Title} — {source} ({est. min})
{Three-sentence summary.}
Why it ranks: {one line tying it to the user's priorities}

## 👀 Skim ({s})
- **{Title}** — {source}: {three-sentence summary}. Skim: {which part}.

## ⏭️ Skip ({k})
- {Title} — {reason: outdated / duplicate of #1 / listicle padding / not your problem}

## ⚠️ Couldn't fetch
- {URL} — {paywall / 404} — {what the title suggests, labeled as guess}
```

## Pitfalls

- **Summarizing from the headline** — the cardinal sin; headlines routinely misrepresent the piece. Recovery: no fetched text, no summary — the link goes to "Couldn't fetch" with its guess clearly labeled, never into the ranked list.
- **Everything ranked "Read"** — a digest that recommends everything recommends nothing. Recovery: cap Reads at 3 (5 for lists over 25 links); force-rank; remember Skip-with-reason is the digest's main gift.
- **Paywall page summarized as the article** — you fetched a subscription pitch and summarized cookie-consent text. Recovery: sniff for paywall markers (very short text, "subscribe to continue"); mark as couldn't-fetch rather than summarizing the wrapper.
- **Ranking without calibration** — relevance to nothing in particular produces a generic list. Recovery: if step 1's priorities question went unanswered, rank by substance + freshness and say explicitly that ranking is uncalibrated.
- **Deleting the user's saved links after processing** — never unprompted. Recovery: offer removal, act only on explicit confirmation, and only ever remove links that appear in the digest.

## Verification

- [ ] Every summarized link was actually fetched; unfetchable links are in their own labeled section
- [ ] Each summary is exactly three sentences and contains at least one specific detail from the text
- [ ] Reads capped and force-ranked; every Skip has a reason
- [ ] Dedupe count reported (n links, m unique)
- [ ] Source list untouched unless the user explicitly approved cleanup
- [ ] Time estimates present on every Read item and the digest total
