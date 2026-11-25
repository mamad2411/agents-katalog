---
name: idea-scout
description: >-
  Find what to build from what people are struggling with right now, not from the model's memory. Scans
  live sources (GitHub issues and new repos, Hacker News, Reddit, changelogs, launches) for dated, linked
  evidence of real problems, then hands back ranked idea briefs: open-source tools, side projects and
  company-size ideas, each with proof, what exists, the gap and why now. A dig mode goes deep on one
  idea. Use for "what should I build", "give me project ideas", "OSS ideas", "startup ideas", "what's
  missing in <area>", "find problems in <niche>", "is this idea any good", "dig into <idea>".
---

# Idea scout

The model's memory of what exists, what is missing and what people want ends at its training cutoff,
and new tools ship every week. An idea from memory alone is often already built, already abandoned, or
solves a problem nobody has any more. This skill only accepts ideas that rest on evidence found live in
this run: real people, their own words, a link and a date.

**The one rule: no link, no claim.** Every problem, number and "nothing does this" needs a source you
opened in this run. Anything you could not check is labelled `unverified`.

## Before you start

- **You need web access**: a web search tool, plus page fetching or a shell with `curl`. Without them,
  say so and stop. Only if the user insists, give ideas from memory, labelled "from memory, not
  checked, may already exist" at the top.
- **Today's date** comes from the environment, not your memory. The default evidence window is the last
  90 days; anything older counts as background only.
- **The user's frame**, read from the request, never asked for in scan mode:
  - size: `oss` (open-source tools and libraries), `side` (side projects and small paid tools),
    `startup` (company-size), or `any` (the default: about half oss/side, half startup);
  - topic: an area such as "devtools for agents", "self-hosting" or "fintech ops". With none, scan
    broadly across developer tools, AI and agent workflows, infrastructure, and work that is still done
    by hand;
  - the user's stack or skills, if they mention them; use them to rank what is buildable.

## Mode 1: scan (default)

Gives back 5-8 ranked idea briefs. Budget: about 30-60 searches and fetches.

### 1. Gather 25-40 raw signals

A signal is one person, in their own words, hitting a problem: "is there a tool that…", "I wish…", "how
do you all handle…", "we ended up writing a script for…", an issue with many 👍, a popular project gone
quiet. Log each signal in a scratch file as you go: the quote, link, date, where it was posted, and
how many people engaged with it (upvotes, 👍, replies).

Where to look, and how:

| Source | What it gives | How |
| --- | --- | --- |
| Hacker News | Developers' unfiltered pain; Ask HN and comment threads | `https://hn.algolia.com/api/v1/search?query=<words>&tags=comment&numericFilters=created_at_i%3E<unix time 90 days ago>` (`tags=ask_hn` for Ask HN posts). Encode `>` as `%3E`. |
| GitHub issues | Missing features users keep asking for, with vote counts | `gh search issues "<words>" --state open --sort reactions-+1 --json title,url,updatedAt,reactionGroups`. GitHub search is rate-limited: about 10 calls per run, spaced out. |
| GitHub repos | What just took off (demand), what's popular but abandoned (a gap) | `gh search repos --created ">YYYY-MM-DD" --sort stars`; for a known tool, open its repo and check the last commit and the open-issue count. |
| Reddit | Practitioners in niches: r/selfhosted, r/devops, r/sysadmin, r/LocalLLaMA, r/ExperiencedDevs, and the topic's own subreddits | Reddit refuses direct fetches, so use your web search with `site:reddit.com/r/<sub>` and the pain phrases below. |
| Changelogs and launches | Why now: new APIs, models, standards, price changes, deprecations, licence changes | Platform blogs and release notes, Product Hunt, Show HN. |
| Job posts and RFPs | Work people are paid to do by hand ("eliminate manual…", "own our internal tooling") | Web search for job posts in the topic. |
| YC Requests for Startups and recent batches | Startup-size only: what investors are asking for, and who is already funded to do it | ycombinator.com/rfs and the batch company lists. |

Pain phrases worth searching: "is there a tool", "I wish there was", "how do you handle", "we built an
internal", "spreadsheet to track", "still doing this manually", "alternative to <tool>", "<tool> pricing",
"<tool> is dead", "migrating off <tool>".

If your host can run subagents, you may split the gathering by source, with three helpers at most, each
writing its signals to a file. Merge before step 2.

### 2. Group the signals into problems

- Merge signals describing the same problem. A problem needs **at least two independent sources**
  (different sites or different authors). A single loud post is a lead, not a problem.
- Name each problem in the user's words, not in solution words: "can't tell which test change made the
  agent worse", not "an eval platform".

### 3. Open the box: five lenses for less obvious ideas

Run every problem, and the signal pile as a whole, through these. Most good ideas come from one of them:

1. **New capability × old pain**: something released in the last few months (an API, a model ability, a
   standard, a cheaper price) makes a long-standing annoyance solvable now.
2. **Refugees**: a price rise, licence change, shutdown or deprecation pushes users off a tool. They need
   a migration path or a replacement.
3. **Abandoned but loved**: a popular project with no commits for months and a pile of open issues.
4. **The shared script**: people passing around gists, templates or spreadsheets to work around a gap.
   That is a product with its first users already found.
5. **Agents as users**: a tool built for humans that agents now use badly, or a task agents now do that
   has no tools for the agent.

Also try one cross-pollination: something common in one ecosystem but missing in another (a tool every
Rust project uses with no Python equivalent; a SaaS staple with no self-hosted version).

### 4. Check what already exists, for every candidate

Search before you claim a gap. For each candidate:
- the 2-4 closest existing tools or projects: link, stars or pricing, last activity, and what their own
  users complain about (their issues, reviews, threads);
- whether a big platform or AI lab has shipped or announced it. If so, drop it unless a clear gap is
  left, and say what the gap is;
- "Already exists" is not a reason to drop an idea when users say the existing option is bad. Quote
  them.

### 5. Score, rank and drop

Score 1-5 on each: **pain** (strength of the evidence), **frequency** (how many people, how often),
**gap** (how badly existing options serve them), **why now**, and **buildable** at the requested size (a
weekend for `side`, weeks for `oss`, a real team for `startup`). For `startup`, also say who pays and
roughly how many of them there are, from sources.

Keep the top 5-8. Keep a short drop list: one line per idea dropped and why ("Vercel shipped this in
October", "one post, no echo").

### 6. Write the briefs

Save to `idea-scout/YYYY-MM-DD-<topic>.md` in the current folder, unless the user names a place. In
chat, give one line per idea and the file path. Each brief:

```
## <n>. <name>  [oss | side | startup]   score <total>/25
Problem: <one sentence, in users' words>
Proof:
  - "<quote>" (<source>, <date>, <engagement>) <link>
  - "<quote>" (<source>, <date>, <engagement>) <link>
Who has it: <role, team type, how many if known>
What exists: <tool> (<link>, <stars or price>, <last activity>): <its gap, ideally quoting its users>
The gap: <what nobody does well>
Why now: <the dated change that opens it>
First build: <the smallest version that solves the core pain; for side or oss, what fits in a weekend>
First users: <the actual threads, issues or communities to show it to>
Risk: <the hard part, platform risk, or why it might not work>
```

End the file with the drop list and the date window you searched. Then offer to dig into any of the ideas.

## Mode 2: dig `<idea>`

For one idea, from a scan or from the user. Same rule: no link, no claim. Budget: about 20-40 searches.

1. **Demand**: gather 10+ more signals for this exact problem. Count them by source and over time. Is it
   growing? Quote the three strongest.
2. **Landscape**: a table of every existing option (open source, paid, a platform's own feature, "a
   script"), with link, traction, pricing, last activity, and the top complaint from its own users.
3. **Why now**: the dated changes that make it possible or needed now, and what could close the window.
4. **The wedge**: the smallest version that a specific group would switch to, and why they would.
5. **First 10 users**: where they are (named threads, issues, communities), and the message you would
   post there. Draft it; the user sends it.
6. **For `startup` size**: who pays, a rough market size from sources (show the arithmetic), the business
   model, a matching YC Request for Startups if there is one, and the funded competitors.
7. **A test for this week**: the cheapest action that gets a real signal (answer the thread, open a
   discussion, a landing page with a waitlist, a prototype shown in an issue), and what result would
   mean go or stop.
8. **Verdict**: build, test first, or skip, in one line with the reason.

Append the dig to the same file under the idea, or write `idea-scout/YYYY-MM-DD-<idea>.md`.

## Rules

- Quote people's real words. Never paraphrase a quote, and never write a quote you didn't read.
- Read every number (stars, downloads, upvotes, prices) on the page. Never estimate one and present it as
  read.
- Date everything. Evidence older than the window is background, marked as such.
- No filler ideas: "an AI assistant for X" or "a dashboard for Y" only when the evidence names that exact
  pain and the existing options miss it.
- Say plainly when the evidence is thin. Three solid ideas beat eight padded ones.
- Never post, comment or reach out yourself. Draft it; the user sends it.
