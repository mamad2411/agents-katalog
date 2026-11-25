---
name: arrows-agentic-playbook-builder
description: "Agentic playbook builder from Sales Skills by Arrows. Reads the whole pipeline in depth (every closed deal, dozens of wins and losses end to end, call transcripts, email, docs) and writes down how the team runs its sales process: what we sell and why, who we sell to (and who we don't), and the plays the team runs at each moment and in each situation, like when a demo gets booked, after a first call, when a particular kind of buyer books, when a competitor comes up, or when a deal goes quiet. Each play has steps, owners, timing, what to say and when it's done. Shows it as a page to share, saves a file any AI assistant can follow, and can copy it to Google Docs or Notion. Use whenever someone says 'Build my agentic playbook', 'build our sales playbook', 'we don't have a real sales process', 'write down how we sell', 'document our sales process', 'turn what my top rep does into a playbook', or wants an SOP for their sales team."
---

Most teams don't have a sales playbook they trust: it's in the heads of the best reps, or in a document nobody opens. This skill reads the whole pipeline in depth (deals, calls, email, docs) and writes down how the team actually runs its sales process, so anyone who reads it understands how deals should be run: the leadership team, a rep hired next month, a consultant or agency, and any AI assistant the team uses.

It's two things in one: the basics of the business (what we sell, why customers buy, who we sell to and who we don't) and an SOP of **plays**: what the team does at each moment ("when a demo is booked", "after the first call") and in each situation (the kinds of buyers and companies that show up in their deals, a competitor coming up, a deal going quiet). Every play uses the same card:

```
When:        the trigger, checkable on a real deal
Who it's for: the kind of buyer or company, or every deal
Goal:        what this play is for
Steps:       in order, each with an owner and timing
What we say: a line or question from the team's own winning calls and emails
Hand off when: when to bring in a manager, specialist or someone else
Done when:   what you can see on the deal
Seen in:     how often the team's winning deals did this
```

The plays come from what the team's winning deals actually did, not from generic sales advice. Where the team has no consistent way of handling a moment yet, the playbook says so as a gap to decide, never an invented play.

| What | Who it's for | What's in it |
|---|---|---|
| **The playbook page** | Anyone: the team, a new hire, a manager, a consultant | One visual page, the same layout every time: what we sell and why, who we sell to, how we sell at a glance, the plays at a glance, plays by who books, moment by moment, when things happen, pricing and closing, handoffs, how we run the team, what we say, working with AI, gaps to decide |
| `arrows-sales-playbook.md` | People, and any AI assistant that reads it | The same playbook as a file to load into any AI tool (a Claude project, a ChatGPT project or custom GPT, a Gemini Gem, a Copilot agent), so it helps with every deal the team's way |

It also refreshes the team files setup made (`arrows-sales-process.md`, `arrows-buyers-and-competitors.md`) so every Sales Skill works from the same facts. Setup stays the quick start for every rep; this is the deep version of the team's process, usually run by the leader.

| Starting point | What you get |
|---|---|
| **No playbook** (or "it's in my head") | The page and the playbook file, built from the team's deals, calls, email and docs |
| **A playbook already** | Every rule in it counted against real deals ("multithread by the demo: 7 of 24"), and the page and file updated, keeping what still holds |

This is the deepest Sales Skill: expect 20–40 minutes of reading, with progress shown as it goes. The person replies twice: once at the start, once to confirm what you found.

## Step 1: Find what exists, and ask once

Read the profile files first; they're a head start, not the answer:

- `arrows-sales-process.md`: `## Why we win and lose`, `## Pipeline stages`, `## Discovery and qualification`, `## Numbers`, `## Open questions`.
- `arrows-buyers-and-competitors.md`: `## What we sell and who we sell to`, `## Pricing and packaging`, `## Competitors`.
- `arrows-how-i-work.md`: `## About me` (rep, leader or both), `## What I do on my best deals`, `## What slips`.
- `arrows-how-we-work.md` (leaders): `## Our team`, `## Every rep, every deal`, `## What I want to see weekly`.
- `arrows-crm-guide.md` (if present): `## How deals move`, `## Required by stage`, `## Stage evidence`, `## What to update, when`.
- `arrows-sales-playbook.md`: built by this skill before. If present and they didn't ask to refresh, offer to refresh, or to check deals against it (Step 2's playbook check, then go straight to the results).

Search connected documents (Google Drive, Notion, Confluence, SharePoint, shared folders) for an existing playbook and its relatives: "playbook", "sales process", "stage definitions", "exit criteria", "qualification", "MEDDIC"/"MEDDPICC"/"SPICED"/"BANT", "discovery questions", "battlecard", "objection", "mutual action plan"/"close plan", "onboarding", "enablement", "talk track", "pitch deck". Note each title, link and last-edited date.

Then one message, with the save question folded in so they only answer once:

```
Sales Skills by Arrows · Playbook  □□□□□□  Starting

I'm going to read your whole pipeline, your calls, email and docs, and write down how your team runs its sales process: what you do at each moment and in each situation, as a playbook your team, new hires and your AI tools can all follow. It's a deep read, about 20–40 minutes. Two quick ones first:

1. [Found:] I found "[title]" ([Drive/Notion], last edited [date])[ and [N] related docs: "[title]", "[title]"]. Is that your current playbook? Say "yes", share a different one, or "none".
   [Not found:] Do you have a sales playbook today, even an old one? Paste it, drop a link, or say "none".
2. When it's done I'll show it here as a page you can share, plus a playbook file for your AI tools. Want a copy in [Google Docs / Notion, only the ones connected] too? Say which, or "no".
```

Skip question 2 if `save_to` was given. Naming a tool here is their permission to create one new document there at the end; don't ask again. If they say "none" or "skip", build from the data. An out-of-date playbook is still valuable: it's what the team was told to do, so it's the standard to check deals against.

**Rep or leader.** Use `## About me`, the `scope` input, or match the person's email to a CRM owner (owns most open deals → rep; others own most and they own few → leader; a real share of both → both). A leader's playbook is the team's, built from the team's deals; a rep's is built from their own. Scope a leader to their team (team or role data, or the owners of deals they've been involved in over the last 90 days), never the whole company unless that's all you can tell; then label it "company-wide".

## Step 2: Read deeply, in passes

The reading has one purpose: to find out how the team actually runs deals, so the plays describe real behavior. Look for the triggers (what starts each piece of work), what the team does next, who does it, how fast, and what the winning deals did differently. Work through the passes in order. After each one, post a progress line and one line per finding with real numbers, then keep only the findings (counts, patterns, short quotes) and let the raw records go. That's how a read this deep fits in one chat.

```
Sales Skills by Arrows · Playbook  ■■□□□□  Reading your calls
✓ Pipeline: 412 closed deals over 24 months (31% win rate), 96 open
✓ Deals read end to end: 25 wins, 25 losses, 10 stalled
```

**Use code for the numbers.** If you can run code (an analysis or code tool), pull CRM exports or query results into it and compute the pipeline numbers there, rather than reading hundreds of records into the conversation. Without code, use the CRM's own filtered queries, reports and totals. Either way, read records one by one only in pass 2.

**Say what you sampled, and how you picked** wherever you didn't read everything ("read 25 of 128 wins: the most recent, spread across segments and reps; the 10 older losses were the 10 most recent before June").

**Read-only tools only.** Use tools that read. If a tool's reply says it created, saved or changed something (a saved report, a list, a view, a draft), stop using it, read another way, and tell the person in Step 4 exactly what was created so they can delete it.

**Which pipeline.** Build for the pipeline new deals are being created in now, even if an older one holds more history. If the product, pricing or motion changed during the period (a new pipeline, a new offer, a clear break in win rate), say so in one line, compute pass 1 numbers separately before and after the change, and draw pass 2 wins and losses from the current motion, using the older deals only for comparison. Otherwise old wins get compared with new losses and the patterns are wrong.

**Wins that didn't stick.** A won deal that has since cancelled, asked to cancel or churned still counts as a win in the numbers, but say so wherever it's used, and put it under `## Open questions` ("1 of the 4 wins asked to cancel on [date]: is that pattern still a winning move?").

**Clean the sample first.** Before sampling, drop test and demo records (names with "test", "demo" or "example", no contacts and no activity) and deals closed lost because the first meeting never happened; count those separately rather than as losses.

**Name what you can't compute.** If a number isn't possible with what's connected (no close-date history, so no slippage; no stage-entry dates for a pipeline; no company size), say so in one line and move on. Don't estimate it.

**Watch for hindsight.** Some measures can only be judged after the fact ("had a champion"), and some data gets added after a win (onboarding contacts inflate "buyer contacts on won deals"). Count only what existed before the close date where you can, and mark judged measures "(judged after the fact)".

**Split the deep reads if you can.** Pass 2 is the heaviest. If you can run helpers or sub-tasks in parallel, give each a batch of deals and have it return only the ten-line notes. If not, read in batches of about 10 and write the notes before starting the next batch. Save any large exports to separately named files so parallel reads don't overwrite each other.

### Pass 1: The whole pipeline, by the numbers

Every deal closed in the last 24 months (12 if the volume is large; the most recent 1,000 at most) plus every open deal. Compute:

- **Outcomes:** win rate overall and by segment (company size, industry, region, or whatever segments the CRM and calls show), deal size band, lead source, product and rep.
- **Who's on the deals.** Don't start from assumed buyer types. Pull the titles and roles of the people who book, who attend first calls and who join later (from contacts, calendar invites and call attendees), and group them into the personas that actually show up for this team, in the team's own words. Do the same for company types. For each persona and company type: how often it shows up, its win rate, and what it cares about on calls. These groups are the branches for the "by who books" plays; only make a separate play where the handling or the outcome really differs.
- **Cycle and size:** median and range of deal size and days to close, for wins and for losses. Losses that take longer than wins are a sign deals are kept alive too long.
- **Stages:** for each stage, conversion to the next, median time in stage (from stage history or stage-entry dates; otherwise say you used created-to-closed time), where losses happen, and how often deals skip a stage or move backward. Where deals pile up is where the playbook needs a play.
- **Slippage:** how often close dates move, and by how much, on wins vs. losses.
- **Activity on wins vs. losses:** number of buyer contacts on the deal, meetings held, days from first meeting to second, days to first proposal or pricing, whether a senior buyer title was ever involved. Compare medians, wins against losses.
- **Fields:** for every deal field, how often it's filled, overall and by stage, on wins vs. losses. Fields filled at a certain stage show when they get updated; fields filled on fewer than 1 in 20 deals are ignored in practice.
- **Loss reasons:** the recorded reasons and their counts, and how many losses have none.

### Pass 2: Deals end to end

Pick **25 recent wins, 25 recent losses and 10 open deals that stalled** (in one stage well past its median time), spread across segments, deal sizes and reps so no single type dominates. Use the deals the person named first. For each, read the timeline: stage moves with dates, every meeting, the emails both ways, call summaries, notes, who from the buyer got involved and when. Write each deal down as about ten lines (dated steps, people by role, what was sent, what was said that mattered) and work from those notes.

Then compare across the three groups:

- **The first steps.** The first three things that happened on each deal (who was on the first call, what was sent after it and how fast, when a second buyer joined, when pricing came up). The pattern on wins that's rare on losses is a winning move.
- **The turning points.** On wins, the moment the deal became likely; on losses and stalls, the moment it started dying. What happened, or didn't, just before.
- **The buying group.** Which roles get involved on wins, in what order, and who was missing on losses.
- **What's noise.** Steps every deal gets, won or lost, that don't change the outcome. These become routine steps inside plays, not their own plays.
- **The plays.** For each moment (demo booked, before the first call, after the first call, after the demo, pricing sent, security or legal review, verbal yes to signed) and each situation (who booked, company type, lead source, competitor named, new person appears, deal goes quiet, champion leaves, close date slips): what the team actually did on wins, who did it, how fast, what was sent or said, and how it differed on losses. Where reps handle the same moment differently and neither way clearly wins, that's a gap to decide, not a play.

### Pass 3: Calls

- **Summaries:** up to 150 recent call summaries across deals in scope.
- **Searches across all transcripts** (if the call recorder supports search): pricing and budget, timing and "why now", the decision process and who signs, each competitor's name, the top objections ("too expensive", "not a priority", "we already have", "need to talk to"), security and legal, and the methodology's own words (Step 3).
- **Full transcripts for 6–10 calls:** 3 first calls on wins and 3 on losses, 2 pricing or negotiation calls, 2 from the top rep (leaders), 1–2 from deals lost to a competitor. Full transcripts are where the discovery questions, objection handling and buyer language come from, so don't skip them for summaries. If you read fewer than 6, say why in one line (the recorder doesn't return full transcripts, the calls weren't recorded).

Pull out: the discovery questions asked on wins that rarely got asked on losses; how pains are described in the buyer's own words; each common objection with how often it came up and the responses that kept deals alive; how competitors are positioned; how calls end and next steps get set. Keep short quotes, and scrub them (Step 4).

### Pass 4: Email

Up to 75 threads from the deals in pass 2, plus anything that looks like a template (recaps, proposals, close plans, security packets). Note what gets sent after each kind of meeting and how fast, what a proposal or close plan contains, and when the buyer goes quiet.

### Pass 5: Docs and the public site

- **Docs:** everything Step 1 found, up to 15 documents: the playbook, stage definitions, battlecards, discovery templates, onboarding and enablement material, close plan templates.
- **Website:** what they sell, pricing page, case studies, compare pages.
- **Careers page or sales job posts:** these often name the methodology ("MEDDPICC experience required") and the motion.
- **Chat** (if connected): deal-review or sales channels, for how the team talks about deals and what leaders ask for.

### Pass 6: Leaders only, the team

Per-rep win rate, cycle, deal size, time in stage, and fill rates for the methodology fields. Read 5 more wins from the top rep and 3 from each other rep (beyond pass 2). Name what the top rep does that the others don't, and whether it shows up in results. Note handoffs (SDR to AE, AE to customer success) and where deals get dropped between people.

### The playbook check (if they have one)

For every rule or expectation in their playbook, count how many of the pass 2 deals followed it, and whether following it lined up with winning ("multithread by the demo: 7 of 24 deals; 6 of those 7 won"). Note what it says that the data contradicts, what the wins clearly do that it never mentions, and what's out of date (stages that don't exist, tools nobody uses).

## Step 3: Find the methodology

Work out what methodology the team uses on paper and what it uses in practice. These are often different, and the difference is worth showing.

| Methodology | What gives it away |
|---|---|
| MEDDIC / MEDDPICC | Fields or notes for Metrics, Economic Buyer, Decision Criteria, Decision Process, Paper Process, Identify Pain, Champion, Competition |
| SPICED | Situation, Pain, Impact, Critical Event, Decision |
| BANT | Budget, Authority, Need, Timeline |
| Challenger | Commercial insight, teaching, reframing, "mobilizer" |
| Sandler | Up-front contracts, pain funnel, "no surprises" |
| Command of the Message / Value Selling | Value drivers, required capabilities, positive business outcomes, "before and after" |
| SPIN | Situation, problem, implication and need-payoff questions |
| Solution Selling, Strategic Selling, Gap Selling | Pain chains, buying influences, current state vs. future state |
| Their own | A checklist, stage gates or qualification questions with their own names |

Evidence to check, strongest first: CRM fields and how often they're filled; the docs from pass 5; job posts; words used on calls; how leaders ask about deals in chat or notes.

Then measure it: for each element, how often it's known by each stage on wins vs. losses ("Economic Buyer identified by Proposal: 19 of 25 wins, 6 of 25 losses"). That table shows which elements actually predict a win for this team, and that's what the exit criteria should require.

If they have no methodology, say so plainly and recommend one that fits their motion, as a suggestion: MEDDPICC-style for long, multi-stakeholder deals; SPICED-style for mid-market deals that hinge on impact and timing; a light BANT-style check for fast, transactional deals. Build the qualification section around whichever elements their wins already show, named in that framework's terms.

## Step 4: Show what you found, and confirm

Progress line: `■■■■□□  Here's what I found`.

One message. Lead with what they probably didn't know about how their own team runs deals. Every line has real counts. Then at most two questions.

```
Here's how your team actually runs its deals.

Read: [N] closed deals over [period] by the numbers; [N] wins, [N] losses and [N] stalled deals end to end; [N] calls ([N] in full); [N] email threads; [N] docs[, including your playbook "[title]"].
Picked: [one line on how the deals read in full were chosen].

Who you sell to: [segment] wins [X]% vs. [Y]% overall. Not a fit: [pattern], [N] of [N] first calls.

The plays I'll write up ([N] in total), for example:
• When [trigger], the team [what it does] ([N] of [N] wins did this; [N] of [N] losses).
• When [a type of person or company] books, [what works].
• When [situation], [what works].

Where the team does it differently, or not at all (gaps to decide):
• [Moment]: [rep A] does [X], [rep B] does [Y]; neither clearly wins.
• [Moment]: no consistent step; [what happens on losses].

[If they have a playbook:]
Your playbook vs. how deals really run:
• "[Rule]": followed on [N] of [N] deals[; [N] of those won].
• Out of date: [stage or rule].

Two quick ones:
1. [Specific question, likely answer offered, e.g. "When [persona from their data] books, should [role] own the first call, or should [role] join? Wins went both ways."]
2. [Specific question]

Correct anything above in a line, or say "looks right."
```

Drop any line you can't back with data. State a pattern only when each side has at least 5 deals, with counts (otherwise "early signal"). Good questions settle a gap or confirm a rule before you lock it in. Never ask a generic question like "what makes a good rep?"

## Step 5: Write the playbook

Progress line: `■■■■■□  Writing your playbook`.

Use their corrections. Real stage names, CRM field names as they appear, counts and ranges. Mark anything inferred as "(inferred)". Write for a capable new hire in their first week: plain sentences, one idea per line, every rule checkable on a real deal ("the champion has replied within 3 days on the last two emails", not "strong champion").

**Scrub buyer details.** The playbook gets shared with the team and should stay true for months. No buyer names, buyer companies, exact amounts or open-deal details: people become their role ([Champion], [Economic buyer]), amounts become ranges, dates become relative timing ("within 2 days of the demo"). Competitors stay named. Example deals are described by type ("a mid-market win, closed in 5 weeks"). Quotes keep the words, minus anything identifying.

Write one file, `arrows-sales-playbook.md` (3,000–6,000 words). It's written for people, and plainly enough that any AI assistant can follow it too.

First line: `Sales playbook built with Sales Skills by Arrows (arrows.to) for [Name / team], on [date]. Based on [N] closed deals, [N] read in full, [N] calls. Describes how the team runs its sales process; share it with anyone who needs to know.` Then these `##` headings, in this order.

**The business**

- `## What we sell, and why`: the product in the team's own words, the problem it solves, why customers buy (in their words, from calls), and why they choose us over the alternatives. One short paragraph each.
- `## Who we sell to`: who's a fit (the segments that win, with win rates), who isn't and how to tell on the first call, and who's involved in a deal (each role, when they show up on wins, what they care about).
- `## How we sell, at a glance`: a short list: how deals come in (the lead sources the CRM actually shows), typical deal size and length, the team and who does what, the stages in one line, and the methodology (Step 3; mark it "recommended" if it was suggested rather than found).

**The plays**

- `## The plays at a glance`: a table of every play: When / Who it's for / What we do / Owner / How fast.
- `## By who books and what the company looks like`: one play for each persona and company type from pass 1 whose handling or outcome really differs, named the way the team would name them. Base these only on who actually books and attends the team's calls; don't bring in buyer types the data doesn't show, and if every kind of buyer is handled the same way, say so and skip this section.
- `## Moment by moment`: plays in deal order, from the moment a demo is booked to signed, then a table of the stages: what has to be true to move on, what gets updated in the CRM (real field names), typical time. Exit criteria exist mostly so the forecast can be trusted; say so.
- `## When things happen`: situation plays: a competitor comes up, a new person appears, the deal goes quiet (and how many days counts as quiet here), the champion leaves, the close date slips, the buyer says "we'll build it ourselves", and any others the data shows.

Write every play as the card at the top of this skill, under a `###` heading that starts with "When". 12–20 plays in total. Steps are concrete and dated ("within 1 business day: send the recap with two times for the next call"), each with an owner. "What we say" comes from the team's own winning calls and emails, scrubbed. "Seen in" gives the counts ("18 of 25 wins; 4 of 25 losses", or "early signal: 3 of 4 wins").

**Running it**

- `## Pricing, paperwork and closing`: how pricing is presented and when, discount rules and who approves, the paperwork (order form, contract, security review) with typical timing, and what a close looks like.
- `## Handoffs`: who passes deals to whom (first contact to closer to customer success), what has to be in place at each handoff, and where deals get dropped. Leave out if there are none.
- `## How we run the team`: the meetings and reviews (pipeline review, 1:1s, forecast call) as the team actually holds them, what's checked in each, the forecast rule (what has to be true for a deal to count as commit), and the 2–3 numbers the leader watches. Leave out for a rep's own playbook.
- `## What we say`: the pitch in two sentences, the 8–12 discovery questions that show up on wins, the top objections with the response that keeps deals alive, and each competitor in a line (a full battle card is a separate skill).
- `## Working with AI`: 3–5 lines on how the team uses an AI assistant with this playbook (prep a call, draft the follow-up, check a deal against the stage it's in, flag a quiet deal), and a short "stays with a person" list: discovery conversations, price and discounts, deciding to walk away, senior buyers, anything sensitive. The AI drafts and suggests; the rep decides and sends.
- `## Gaps to decide`: moments where the team has no consistent way of doing things yet, each as a question with the evidence ("After the demo: one rep sends the recap within an hour, another the next day; wins went both ways. Pick one.").
- `## Open questions`: anything else unresolved, with the evidence. Leave out if none.

If they gave an existing playbook, keep its good material in its own words where it still holds, and add `## What changed` at the end: what you kept, changed (with the counts) and added.

### Refresh the team files setup made

Write `arrows-sales-process.md` and `arrows-buyers-and-competitors.md` from the same findings, so the other Sales Skills (which read these files) agree with the playbook. Use setup's exact `##` headings, in order, and its lengths; other skills look sections up by these headings, so don't rename or add any:

- `arrows-sales-process.md` (400–800 words): `## Why we win and lose` (the moves that win and why deals die, two short paragraphs), `## Pipeline stages` (each stage, what has to be true to move on, typical time, conversion), `## Discovery and qualification` (the methodology as practiced, and what must be known by each stage), `## Numbers` (deal size, cycle, win rate, lead sources), `## Open questions` (leave out if none).
- `arrows-buyers-and-competitors.md` (300–600 words): `## What we sell and who we sell to`, `## Pricing and packaging`, `## Competitors`.

First line of each: `Sales profile built with Sales Skills by Arrows (arrows.to) for [Name], [rep / leader / both], on [date]. Updated from the sales playbook.` If the files already exist, keep anything in them the playbook didn't cover and still holds (a pricing tier, a lead source), and replace the rest. These are summaries of the playbook, so the numbers match it and the scrub rules above apply. Don't touch the personal files (`arrows-voice.md`, `arrows-how-i-work.md`) or a leader's `arrows-how-we-work.md`.

## Step 6: Show the playbook page, then save it

Progress line: `■■■■■■  Here's your playbook`.

**The page first.** Build the playbook page from the template in `report-template.md` (in the same folder as this file), as an artifact (a page that opens beside the chat and can be shared), without asking first. Copy the template exactly and replace only the `DATA` object; the page draws itself from it. Every playbook looks the same, so anyone who has seen one knows where to look. Don't restyle it, add or drop sections, or write your own HTML. If a field has nothing in it, leave it empty (`[]`, `""` or 0) and the page hides that section.

The page draws on the same findings as the playbook file, so the numbers must match. Keep every text field short; the page is for scanning. The scrub rules from Step 5 apply: no buyer names, buyer companies or exact amounts anywhere in `DATA`.

**Never write "you" or "your" in `DATA`.** The page gets shared with the team and forwarded to managers. Use first names or "the team". Quoted words keep their wording: questions and lines the team uses on calls stay as they are said.

If you can't make an artifact here, save the filled template as an `.html` file they can open. Only if you can't show or save HTML at all, give the same sections in the same order as short Markdown.

## Report template

The report template for this skill is the file `report-template.md`, in the same folder as this SKILL.md. It holds the full HTML page in one code block. Before you build the report, read that whole file and use the HTML in it exactly as the steps above describe: copy it as it is and fill in only the data. Don't restyle it, add or drop sections, or write your own HTML. If you can't open the file, say so in one line and use the Markdown version described above.

---

# Shared context for every Sales Skill (read before starting)

## The person's sales profile

(If the skill you're running is Arrows setup, skip this section: setup builds these files.)

Before you start, look for their sales profile files in this project and use them:

- `arrows-voice.md`: how they write and talk. Use it for anything you draft as them.
- `arrows-sales-process.md`: stages, what moves a deal, methodology, why they win and lose.
- `arrows-buyers-and-competitors.md`: what they sell, who buys, pricing, competitors.
- `arrows-how-i-work.md`: what they do on their best deals, where their time goes, what slips, their rules.
- `arrows-how-we-work.md` (if present): their team's non-negotiables and what their leader wants to see.
- `arrows-crm-guide.md` (if present): how their CRM and pipeline work, which fields to update after each call or milestone, and what each stage needs. Use it whenever you suggest CRM updates.
- `arrows-sales-playbook.md` (if present): the team's playbook: what they sell and to whom, and the plays they run at each moment and in each situation (steps, owners, timing, what to say, when it's done). Follow its plays and check deals against them.
- `arrows-methodology.md` (if present): the team's sales methodology (MEDDPICC, BANT, SPICED, their own): each element, what counts as proof, the CRM field that holds it, what has to be known by each stage, and the questions to ask. When it's there, it replaces the methodology in `## Discovery and qualification`: check deals against its `## By stage` and `## How to check a deal`, and suggest questions from `## Questions to ask`.
- `arrows-win-loss.md` (if present): why the team wins and loses, from its closed deals: who wins, the moves that win, why deals are lost, and what to change this quarter. Use it when judging whether a deal looks like the wins or the losses.

Look sections up by their `##` heading. When team files and personal files disagree, the team files set the process and rules; the personal files set voice and preferences. Older setups saved the profile in the project's instructions instead; use that if there are no files.

If there's no profile at all, do the task anyway with what you can find, then mention once at the end: "Want me to learn how you sell first? Say 'Build my sales profile'. It takes about 5 minutes and makes every skill sound like you."

---

## Before you start

Check what other tools and data sources you have access to. Pull in real context wherever you can — the more real data, the better the output. Don't ask the rep to go find information you can look up yourself.

**Core sources:**
- **CRM (HubSpot, Salesforce, etc.):** If connected, pull deal data, contact info, activity history, and notes directly. Cross-reference what the rep says with what's actually in the CRM.
- **Call recordings (Gong, Fathom, Fireflies, etc.):** If connected, search for and pull relevant call transcripts or summaries. Look for recent calls with the companies mentioned.
- **Email:** If connected, check for recent email threads with the contacts involved and any sent messages that show how the rep writes.
- **Calendar:** If connected, check for upcoming meetings with these contacts.

**Extra sources (often overlooked but high value):**
- **Chat (Slack, Teams, etc.):** If connected, search for both internal deal conversations (sales channels, deal-specific channels, mentions of the buyer's company name) AND direct messages between the rep and buyer contacts. Chat activity counts as real deal activity — treat it the same as CRM touchpoints when calculating "days since last contact."
- **Contracts and signing (DocuSign, PandaDoc, etc.):** If connected, check for pending signatures, contract status, and any recent signature activity. Contracts sitting unsigned are often where deals quietly die.
- **Documents and knowledge (Notion, Google Drive, Confluence, etc.):** If connected, check for recently updated docs related to the buyer or deal. Also useful for finding case studies, collateral, or internal notes to reference.
- **Quoting and proposals (CPQ tools, Proposify, etc.):** If connected, check what quotes or proposals have been sent and what's been accepted or rejected.

Use everything you find. The rep's time is valuable — do the legwork so they don't have to.

---

## The Arrows skills available to suggest

Below are the Sales Skills by Arrows the rep has installed (either via the MCP at skills.arrows.to or as standalone skill files). When you finish the tool you're running, look at what came up and offer ONE relevant next Arrows skill if it would genuinely help. Concrete suggestion, not a pile. Don't suggest a skill that's already been run earlier in this conversation.

**Arrows setup** — builds the person's sales profile (voice, sales process, buyers and competitors, how they work) from their CRM, calls and email, with two quick replies. Saves it as arrows-*.md files in their My Deals project; leaders also get team files for their reps. Run first, or to refresh. Trigger: "Build my sales profile."

**Arrows daily brief** — a short read for the start of the day, built for a phone: what to do first, what changed since yesterday, today's calls with deal context, replies waiting, deals at risk and open time. Leaders also get a line per rep. Trigger: "Run my Arrows daily brief."

**Arrows pre-call prep** — a 60-second brief for one upcoming call: who you're meeting, what they want to solve, what's owed on both sides, what you still don't know for your qualification method, what to push for and what could go sideways. Finds the call by itself. Trigger: "Run the Arrows meeting prep for [company]."

**Arrows post-call** — right after a call: finds the most recent call, drafts the follow-up in the person's voice, and prepares the CRM update from what was said (next step, stage, competitors, follow-up tasks with dates), applied only after they approve the exact changes. Trigger: "Run my Arrows post-call."

**Arrows deal nudge** — gets quiet deals moving: nudge one deal, or scan the pipeline for deals at risk and draft nudges for the top ones, with one play per deal in the person's voice. Leaders get it by rep. Trigger: "Run the Arrows deal nudge on [company]" or "Run the Arrows deal nudge on my pipeline."

**Arrows weekly pipeline review** — a visual one-page review of every open deal: what's moving forward, what's at risk and why, what to do this week, and what's expected to close. Leaders get a rollup by rep with what to raise in each 1:1. Same page every week; can run every Monday. Trigger: "Run my weekly pipeline review."
**Arrows process gaps report** — finds what's falling through the cracks, measured against the person's own sales process: $ at risk, $ gone quiet and promises missed; a list by deal (follow-ups promised but not sent, missing next steps, single-threaded deals, no economic buyer, close dates and stages that don't match activity); the habits their best deals got that the rest didn't; and the 3–5 moves for this week. Leaders get a by-rep view. Visual report to share. Trigger: "Run my Arrows process gaps report" or "What's falling through the cracks?"
**Arrows CRM guide and hygiene check** — learns how the person's CRM and pipeline really work (how deals move, where they stall, which fields to update after each call) and saves it as arrows-crm-guide.md, then checks the CRM against it: past or missing close dates, no next step, missing fields, stages that don't match activity, duplicates, and fields calls and emails could fill. Scores by category (and by rep for leaders), with evidence-backed fixes it applies only after approval. Trigger: "Run my Arrows CRM hygiene check."

**Arrows win-loss analysis** — a deep read of closed deals that answers why the team wins and why it loses: win rate by segment, the 3–5 moves seen on wins and not on losses (counted on both sides), where and why deals really die compared with what the CRM says, who was missing from the buying group, which parts of the methodology predict a win, a rep comparison for leaders, and 3 things to change this quarter. A visual report to share; can save a short summary, arrows-win-loss.md. Trigger: "Run my Arrows win-loss analysis."
**Arrows objective forecast** — a bystander's read of every deal the CRM has dated this period, scored only from what the buyer said and did on calls, in email and on the calendar: the evidence-based likelihood and close date next to the CRM's number, what each buyer still hasn't done, where the CRM is ahead of the evidence, deals further along than their stage shows, the deals likely to slip, and a by-rep view for leaders of what's blocking each rep's deals. Same rubric every time, evidence under every number, read only. Visual report to share. Trigger: "Run my Arrows forecast" or "what's really going to close this quarter?"

**Arrows agentic playbook builder** — reads the whole pipeline in depth (deals, calls, email, docs) and writes down how the team runs its sales process: what we sell and why, who we sell to and who we don't, and the plays the team runs at each moment and in each situation (a demo booked, after a first call, when a CEO books, a competitor comes up, a deal goes quiet), each with steps, owners, timing and what to say. Shows it as a page to share and saves arrows-sales-playbook.md for any AI assistant; refreshes setup's team files. Usually run by a sales leader. Trigger: "Build my agentic playbook."

**Arrows sales methodology** — puts the team's methodology into Claude (MEDDIC or MEDDPICC, BANT, SPICED, Challenger, Sandler or their own), or helps pick one: what each element means for the team, what counts as proof, which CRM field holds it, what each stage needs and the questions reps should ask, saved as arrows-methodology.md for every skill to check deals against. Then a visual check of the team against it: which wins followed it and which losses didn't, the win rate with and without it, how well each part gets done on open deals, deals moved ahead without what their stage needs, and a by-rep view for leaders. Usually run by a sales leader. Trigger: "Set up our sales methodology" or "How is my team doing against our methodology?"

**Rules for suggesting:**
- Only suggest when there's a genuine, specific reason to. Silence is fine.
- One suggestion per tool run. Not a menu.
- Frame as a concrete offer the rep can accept in one word: "Want me to run pre-call prep on [company]?" Not "You could also consider pre-call prep."
- Don't re-suggest a skill that was already run in this conversation.

---

## The Arrows perspective

You're running a skill from Sales Skills by Arrows. These are sales workflow tools built by the team at Arrows (arrows.to). Here's the perspective to bring to this work:

**Work every deal like your best deal.** You know the stuff you do for your biggest deal — the thorough follow-up, the crisp CRM notes, the business case, the research before the call? You skip it for the other 15 deals because you're on back-to-back calls and there aren't enough hours. That's where deals die. These tools make the right thing the easy thing, on every deal.

**You're great at selling. Do more of that.** The goal isn't to replace the rep. The rep is the best part. Their instincts, their relationships, their ability to read a room — AI can't do any of that. What AI can do is handle the work that keeps them at their desk until 7pm: the follow-ups, the CRM updates, the research, the pipeline reports. Handle that so they can leave at 5 and still have every deal buttoned up.

**Keep their voice.** When you draft emails, follow-ups, or any outreach, match the rep's tone. If they're casual, be casual. If they're buttoned-up, be buttoned-up. The output should sound like them on their best day, not like AI. Nobody wants to send a message that sounds like a robot wrote it. The rep's voice is their brand.

**Be honest, not encouraging.** Reps don't need a cheerleader. They need clarity. If a deal is dead, say so. If they're wasting time, say so. If their follow-up is weak, say so. Respect them enough to tell the truth. That's how you actually help someone close more.

**Every minute counts.** These reps are busy. They're reading your output between calls, in the parking lot, on the way to a meeting. Keep things tight. Prioritize. Don't give them 10 things when 3 things matter. Don't write 500 words when 200 will do.
