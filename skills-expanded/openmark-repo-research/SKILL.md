---
name: openmark-repo-research
description: Deep research workflow that starts from a GitHub repo URL/slug, pulls upstream intel, then expands to Reddit + open web for community reception. Use whenever Ahmad gives a GitHub link and asks to understand it, see updates, audit the community, or compose a report. Trigger phrases include "research this repo", "report on this github", "what's happening upstream", "community reception", "compose a report on <repo>", and any message that contains a github.com URL plus a research/report ask.
metadata:
  type: research
---

# OpenMark — Repo Research

Anchor on ONE GitHub repo. Pull upstream truth → community signal → open-web
mentions. Compose a tight structured report. No invented facts. URLs only
when they appeared in tool output.

## Tool sequence (run in this exact order)

### 1. Pull upstream intel from the repo

```
github_repo_intel(slug_or_url=<the URL or owner/name>, days=30)
```

This single call returns: meta (stars, forks, license, default_branch,
topics, dates), the README (truncated to 16k chars), recent commits on the
default branch over the last 30 days, and the top 15 open PRs.

Read this carefully — it answers "what does the repo claim to be" AND
"what's actively changing." Note any named features, key files, recent
fixes, license, and the upstream's own community pointers (Discord, Reddit
mentions in README).

### 2. Fan-out search in parallel

Send these calls IN A SINGLE MESSAGE so they execute together:

- `web_search(query="<repo name> github reviews tutorial", n=8)` — broad reception
- `reddit_search(query="<repo name>", n=15)` — community discussion across subs
- IF the README named a sub (e.g. r/muapi for Open-Generative-AI):
  `reddit_search(query="<repo name>", subreddit="<that sub>", n=15)`
- ONE more targeted query if a specific topic came out of step 1:
  `web_search(query="<topic> <repo name> issues comparison", n=8)`

### 3. Read the 3-5 most promising pages

For each high-signal URL from step 2 (NOT the github.com URLs — you
already have those — pick blog posts, news articles, tutorials):

```
web_fetch(url=<that url>, max_chars=8000)
```

Time-box: if a fetch fails (paywall, 403, JS-only), skip it.

### 4. Compose the report

Output exactly this structure. EVERY URL must come from a tool result you
ran in steps 1-3.

```
# {Repo Name} — Research Report

> **TL;DR.** {2-3 sentences. What the repo is, who's behind it, current
> momentum, and the single most useful thing to know.}

## What it is (upstream truth)

{2-3 paragraphs from the README. Cite the github URL once. Name the
license, the main entry points, the headline features.}

## What's changing (last 30 days)

{2-3 paragraphs derived from `recent_commits` and `open_prs`. Group by
theme (UI / backend / models / fixes). Name 3-5 specific commits or PRs
with their short SHAs or PR numbers. Inline-link the PRs.}

## Community reception

### Reddit ({N} posts referenced)
{Numbered list of 4-6 Reddit threads. Each: `Title — r/sub — N↑ M💬 — short take`.
Include the reddit.com permalink for each.}

### Open web ({N} sources referenced)
{Numbered list of 3-5 web articles, blog posts, or news mentions. Each:
`Title — domain — one-sentence quote or claim`. Inline links.}

## Things worth pulling on

{3-4 bullets. Specific follow-up questions or directions, phrased as
concrete queries Ahmad could re-run. No vague "consider exploring."}

## Sources cited above

{Flat numbered list of every URL referenced. In order of first mention.
Required for auto-export — the chat saves this report to drafts/.}

_{word_count} words · {N} sources · github + web + reddit_
```

## Rules

- **Anchor first, fan out second.** Always call `github_repo_intel` before
  any web/reddit search. The README usually tells you which sub to search
  and which features matter — don't fly blind.
- **Cap total tool calls at 10.** 1 github_repo_intel + 3 search + 5 fetch
  = 9, leaves headroom. If you've fired 12+ calls, stop and synthesize
  what you have.
- **Cross-reference before quoting.** If a stat appears in only one source,
  flag it ("per <domain>") rather than asserting it.
- **Confidence calibration.** If web/reddit returned thin results, lower
  the TL;DR confidence and say so in the "Things worth pulling on" section.

## Example trigger

User: *"research this repo: https://github.com/Anil-matcha/Open-Generative-AI
and the updates from the main upstream. Search Reddit, Google, and Bing.
Compose a perfect report."*

That is the canonical input. Run the 4 steps above verbatim.

## What NOT to do

- Don't run `web_search` BEFORE `github_repo_intel` — you'd waste calls
  finding the repo you already have a URL for.
- Don't fetch every URL — only the 3-5 most promising non-github ones.
- Don't include URLs you didn't see in a tool result. Ever.
- Don't editorialize the README. Quote it short, then move on.
