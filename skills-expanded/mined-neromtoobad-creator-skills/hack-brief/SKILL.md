---
name: hack-brief
description: Start a new hackathon, buildathon or bounty right, from the event link to a picked idea with a design. Writes HACK.md in the project folder with the event facts and quoted judging, scans what other teams already submitted and which track is empty, reads what the sponsor says it wants and how past winners shipped, gives 3 strong ideas, kills dead premises with live data, checks the name, and ends on a design v1 ready to build. Use whenever the user drops a hackathon/bounty link or says "let's build here", "check existing builds", "what does the team want", "give me 3 ideas", "which track is unsaturated", "stronger ideas" or "let's start this", even if they never name this skill.
---

# Hack brief

The first hour of every hackathon. Goal: walk into the build with an idea the
field doesn't already have, that the sponsor asked for, that works on real
data today, with every fact written down in one file.

Output: `<projects folder>/<event-slug>/HACK.md`, updated after every step,
plus a short project note (memory file, if your setup keeps them). Building
starts only after step 8.

Rules that apply here:
- Plain words. Each idea opens with one sentence a non-crypto person gets.
- No code and no repo before the event start date: most events disqualify or
  cap entries with code committed before the start.
- Write facts with the date checked ("checked Nov 23") because they change.

## 1. Event facts → HACK.md

Read the event page, rules, FAQ, tracks and any docs it links. Write the top
of HACK.md:

```
# <Event name> (<platform>)
- Page: <url> (platform id if any)
- **Start: <date time UTC>** (first commit must come after this)
- **Deadline: <date time UTC>** (+ the user's local time if it's close to a day boundary)
- Prize: <total, how paid> · per track amounts
- Submit: <exactly what they ask for: repo, addresses, tx hashes, video length…>
- Rules: <built-at-event rule, network rules (mainnet/testnet), multi-track rule>

## Judging (quoted)
- **<Criterion>**: "<exact words from the page>"
- Who judges (sponsor team / community vote / an AI judge that reads the repo)

## Track asks
- **<Track>**: what they ask for, in their words. Hard requirements as a list.
  Anything that says "not scored without X" goes in bold.

## Key addresses / endpoints / SDK versions
```

Quote judging and track text exactly. Mark gates ("entries without X aren't
scored further") in bold: they decide what the demo must show.

## 2. Field scan: what others already built

Pull every submission so far and group them by theme and by track.

| Platform | Where the builds are |
|---|---|
| DoraHacks | `https://dorahacks.io/api/v1/hub/hackathons/<id>/buidls?page=N&page_size=12`. curl hits a human check, so call it with `fetch` from a dorahacks.io tab in Claude in Chrome. Output with URLs gets blocked: write the text into a `<pre>` in the DOM and read it with get_page_text. The `tracks` field is an array. |
| Loops House | the event's playground / projects pages; registered repos are public on GitHub. |
| Devpost | `<event>.devpost.com/project-gallery` (+ each project page). |
| ETHGlobal | `ethglobal.com/showcase?events=<slug>`. |
| Others | the event's gallery, Discord showcase channel, or X search for the event hashtag. |

Write a table in HACK.md:

```
## Field on <date> (<N> builds)
| Theme | Builds |
|---|---|
| Stop-loss / take-profit | ~19 |
| …                       |     |
```

Then 2–4 lines: what nearly everyone does (testnet + mock tokens?), which
tracks are crowded vs empty, which asks from the track list **nobody** has
touched, and the strongest numbers anyone claims (so we know the bar).
When the user asks "which track is unsaturated", answer from this table with
build counts per track and prize per build.

## 3. What the sponsor wants

Look past the event page:
- Their roadmap, blog, announcements, recent X posts, docs changelog. Quote the
  lines that name use cases ("Bots become smart contracts…").
- Products they launched in the last month (new SDK, MCP, feature). Using
  something brand new is a strong Integration signal.
- **Past winners** of their earlier hackathons: open the repos. For each, note
  network (mainnet?), live domain, video, README order, what proof they showed
  (address tables, tx tables, deploy records, CI), and the one move that made
  it win. End with **What we copy / What we skip**.

```
## What <sponsor> has said it wants
## Past winners: how they built and shipped (checked <date>)
```

## 4. Three ideas

Give exactly 3, each aimed at a track (or two tracks, if allowed). For each:
- **Name** (working name) + track.
- One plain sentence of what it does.
- How it works in 3–5 lines, naming the sponsor primitive that does the real
  work. If a database or cron job would do the same, drop it.
- Why it's new: the field table says nobody does it, or name 2 similar
  products and the difference.
- The WOW moment in the demo (the thing that reverts, freezes, pays, refuses
  live onchain).
- Proof on real data: a number measured today (unclaimed balance, live
  liquidity, latency) that shows the problem is real.
- Honest limit, in one line.

Save them in HACK.md as `## Ideas` (later rounds: `## Round 2 ideas (<date>,
why)`). Keep old rounds and say why each died: it stops the same idea coming
back.

When the user says "stronger" or "better ideas": don't tweak the last three.
Go back to steps 2–3, find a track ask nobody touched or a real money/safety
problem you can measure, and come back with 3 new ones.

## 5. Kill dead premises (before the user commits)

For the idea the user picks (or the top one), check with live data that the
premise still holds:
- Does the feature/contract it depends on still exist and work the way we think?
  Read the contract, call it, pull its logs. (One idea of ours, an auto-restaker,
  died here: the staking seasons it automated had already ended, and only
  checking the contract showed it.)
- Is there liquidity / users / traffic at the size we need? Quote it.
- Measure the number the pitch rests on.

Write it as `## <Idea> check (<date>)`: addresses, ABI bits, live state,
measured numbers, and the verdict. If it's dead, say so in the first line and
go back to step 4.

## 6. Rules questions and open checks

```
## Open checks before building
- Organizer questions (multi-track entry? does X count?) → where to ask
- Named user outside the team (if judging asks for one) + their wallet
- Funding: what tokens, how much, on which chain
- Accounts / API keys the user must create (they do sign-ups, not us)
```

Ask the organizer early (Discord / Telegram / DoraHacks message) for anything
the rules leave open. The user sends these messages, we draft them.

## 7. Name

Before the name hits a repo (some events tie attribution codes to the repo
name, so it must be final before the first mainnet tx):
- Web search "<name> crypto", "<name> app", the sponsor's ecosystem, and the
  field list from step 2.
- Give the pick, one backup, and the rejected names with the reason.

## 8. Design v1

```
## Picked: <name> (<track(s)>) — design v1 (<date>)
One sentence.
Flow (one job): numbered steps from the user's first click to the onchain result.
WOW: the live moment.
### Research facts that shape the build  (SDK quirks, fees, limits, gotchas)
### Not built yet / open
```

Then:
1. Save/refresh the project note (event, deadline UTC, idea, folder, what's
   open) so a later session can pick it up.
2. Start building: fresh repo after the start date, real onchain use (no
   faked tx hashes or simulated payments), every README claim true today with
   a `file:line`, plans under a "Not built yet" heading, and a check of the
   repo against the judging criteria before submitting.

## Pacing

- One step per reply is fine; always say which step is next.
- Do the research yourself (browser, RPC, docs, `llms-full.txt` /
  OpenAPI files); the user only picks ideas and does sign-ups, funding and
  messages.
- Long research goes in HACK.md, not chat. Chat gets the short version: the
  table, the 3 ideas, the verdict.
