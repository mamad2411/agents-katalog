---
name: arrows-win-loss-analysis
description: "Win-loss analysis from Sales Skills by Arrows. A deep read of closed deals (every won and lost deal counted, about 25 of each read end to end, calls and email) that answers why the team wins and why it loses: which segments win (size, source, industry, new vs. existing customers), the 3–5 moves that show up on wins and not on losses (with counts) and what's noise, where and why deals really die compared with what the CRM says, who was missing from the buying group on losses, which parts of the sales methodology predict a win, a rep comparison for leaders, and the 3 things to change this quarter. A shareable visual report. Use whenever someone says 'Run my Arrows win-loss analysis', 'why do we win and why do we lose', 'why are we losing deals', 'what do our wins have in common', 'what are our real loss reasons', 'win rate by segment', or wants a win-loss review for a quarterly or board meeting. For open deals slipping right now, use the process gaps report instead."
---

Answers one question from the team's own closed deals: **why do we win, and why do we lose?** Every number comes from their CRM, calls and email, with the counts on both sides, so it's clear what actually separates a win from a loss.

| Section | What it answers |
|---|---|
| Three things to change this quarter | The changes most likely to raise the win rate, each with the evidence and steps |
| Who wins | Win rate by segment: company size, lead source, industry, the buyer's current tools, existing customers vs. new |
| The moves that win | The 3–5 things that happen on wins and not on losses, counted on both sides, plus what every deal gets that doesn't decide anything |
| Where and why deals die | The stage and timing where losses happen, and the real loss reasons from reading the deals compared with what the CRM says |
| The buying group | Which roles were involved on wins and who was missing on losses |
| Methodology | Which parts of the team's methodology (MEDDPICC, SPICED, BANT or their own) actually predict a win |
| By rep (leaders) | Each rep's win rate and cycle, and what the top rep does that the others don't |

This looks back at closed deals. It isn't a list of open deals to chase this week; that's the process gaps report. A few stalled open deals are read only as a comparison, to show whether today's pipeline looks like the wins or the losses.

It's a deep read: expect 15–30 minutes, with progress shown as it goes. No questions before the report unless the scope is truly unclear.

## Progress

Post a progress line at the start and after each pass, with one line per finding and real numbers:

```
Sales Skills by Arrows · Win-loss analysis  ■■□□□  Reading deals end to end

✓ Pipeline: 184 deals closed in the last 12 months (22% win rate), 61 open
✓ Cleaned: left out 14 tests, no-shows and stray bookings
```

Stages: `Counting your closed deals` ■□□□□ · `Reading deals end to end` ■■□□□ · `Reading your calls and email` ■■■□□ · `Comparing wins and losses` ■■■■□ · `Done` ■■■■■.

## Step 1: Scope and what already exists

**Who's covered.** Use `scope` if given. Otherwise read `## About me` in `arrows-how-i-work.md` (rep, leader, or both). With no profile, match their email to a CRM owner: owns most deals → rep (their own closed deals); others own most → leader (the team's closed deals, with a by-rep view); a real share of both → leader, with their own deals as one rep. Seeing every deal proves nothing (small-company reps often have admin access). If you can only tell the whole company, label it "company-wide".

**Which deals.** Use `period` if given; otherwise the last 12 months of the pipeline new deals are being created in now. If that gives fewer than 40 closed deals, go back to 24 months, unless the pipeline or offer is newer than that (then use all of it and say so). Label the period with the real range of close dates. If close dates look wrong (years off, or in the future on a closed deal), use the date each deal entered its won or lost stage instead, and say so. Skip onboarding, renewal and support pipelines unless asked.

**What the profile already says.** These are claims to test, not answers. Read `## Why we win and lose`, `## Pipeline stages`, `## Discovery and qualification` and `## Numbers` in `arrows-sales-process.md`; `## What we sell and who we sell to` and `## Competitors` in `arrows-buyers-and-competitors.md`; `## What I do on my best deals` in `arrows-how-i-work.md`; `## Our team` and `## Every rep, every deal` in `arrows-how-we-work.md`; and `arrows-win-loss.md` if an earlier run saved one (then compare with it: what changed since). Where the data disagrees with the profile, say so with counts; that's often the most useful line in the report.

## Step 2: Read deeply, in passes

Work through the passes in order. After each one, post the progress line and its findings, keep only the findings (counts, patterns, short quotes) and let the raw records go. That's how a read this deep fits in one chat.

**Rules for every pass:**

- **Use code for the numbers.** If you can run code (an analysis or code tool), pull CRM exports or query results into it and compute pass 1 there, rather than reading hundreds of records into the conversation. Without code, use the CRM's own filtered queries and totals. Read records one by one only in pass 2.
- **Read-only tools only.** Use tools that read. If a tool's reply says it created, saved or changed something (a saved report, a list, a view, a draft, a report section), stop using it, read another way, and tell the person exactly what was created so they can delete it.
- **Current motion first.** If the product, pricing or motion changed during the period (a new pipeline, a new offer, a clear break in win rate), say so in one line, compute pass 1 separately before and after, and take pass 2 wins and losses from the current motion, using older deals only as a labeled comparison. Otherwise old wins get compared with new losses and the patterns are wrong.
- **Clean the sample.** Before counting, leave out deals that were never real opportunities: test and demo records (names with "test", "demo" or "example", no contacts and no activity), deals lost because the first meeting never happened (no-shows), and research, partner or stray bookings with no buying intent. Count them separately rather than as losses, and say how many of each.
- **Wins that didn't stick.** A won deal that has since cancelled, asked to cancel or churned (check billing or customer records if connected, and recent email or chat) still counts as a win, but say so wherever it's used and add it to the open questions.
- **Early signal.** With fewer than 5 deals on either side of a comparison, call the pattern "early signal", never a rule, and say what would confirm it ("check again after the next 5 wins").
- **Watch for hindsight.** Some data gets added after a win (onboarding contacts inflate "buyer contacts on won deals"), and some steps are results of a deal going well rather than moves ("pilot agreed", "contract sent"). Count only what existed before the close date, compare moves the seller chose to make, and mark judged measures "(judged after the fact)".
- **Name what you can't compute.** If a number isn't possible with what's connected (no stage history, so no time in stage; no company size field), say so in one line and move on. Don't estimate it.
- **Say what you sampled, and how you picked** ("read 25 of 128 losses: the most recent after a real first call, spread across reps and sizes").

### Pass 1: Every closed deal, by the numbers

Every deal closed in the period (at most the most recent 1,000) plus every open deal. Compute:

- **Win rate** overall and by segment: company size or team size, industry, region, lead source, deal size band, product, the buyer's current tools (CRM or the incumbent they use, when recorded), existing customers vs. new, and rep. Keep only segments with enough deals to mean something, and mark the rest early signal.
- **Cycle and size:** median deal size and days to close, for wins and for losses. Losses that take longer than wins are a sign deals are kept alive too long.
- **Where losses happen:** the stage each lost deal was in before it closed, as counts. Many CRMs only keep "Closed lost" once a deal closes; without stage history, use the furthest step each lost deal reached (first call held, demo, pilot or trial, pricing or proposal sent) from its activity and dates, and say the stages were judged that way. Stage conversion and time in stage only if stage history or stage-entry dates exist; otherwise say so.
- **Activity on wins vs. losses:** buyer contacts on the deal (if most deals have only one contact recorded, count the buyer's people on calls and email threads instead), meetings held, days from first meeting to second, days to first pricing, whether a senior buyer title was ever involved. Compare medians.
- **Loss reasons as recorded:** each reason with its count, and how many losses have none.

### Pass 2: Deals end to end

Pick **about 25 recent wins, 25 recent losses after a real first call, and 10 open deals that stalled** (in one stage well past its usual time), spread across segments, sizes and reps so no single type dominates. With fewer wins, use every win. Pick losses from deals that had a real first call. For each deal, read the timeline: stage moves with dates, every meeting, emails both ways, call summaries, notes, and who from the buyer got involved and when. Write each deal down as about ten lines (dated steps, people by role, what was sent, what was said that mattered, why it really closed the way it did) and work from those notes.

Fill in the same checklist for every deal, so wins and losses can be counted the same way: who from the buyer was on the first call and on later calls (by role), whether the person who signs was on a call and when, what was sent after the first call and how fast, when price was first said, whether the next meeting was booked on the call, whether success was defined before a pilot or trial, the furthest step reached, the real reason it closed the way it did, and whether the CRM reason matches. Mark anything you couldn't tell as "unknown" rather than no.

If you can run helpers or sub-tasks in parallel, give each a group of deals (for example wins, losses, stalled) and the checklist, and have it return the checklist answers and the ten-line notes. If not, read about 10 deals at a time and write the notes before starting the next. Save any large exports to separately named files so parallel reads don't overwrite each other.

### Pass 3: Calls

- **Searches across transcripts** (if the call recorder supports search): pricing and budget, "why now", who signs and how they decide, each competitor's name, and the top objections ("too expensive", "not a priority", "we already have", "we'll build it ourselves", "need to talk to").
- **Full transcripts for 6–10 calls:** 3 first calls on wins and 3 on losses, 1–2 pricing calls, and 1–2 from deals lost to a competitor or to doing nothing. Full transcripts are where the real loss reasons and buyer language come from. If you read fewer than 6, say why in one line.

### Pass 4: Email

Up to 75 threads from the pass 2 deals (the person's mailbox, and emails logged on the CRM deal for teammates' deals): what was sent after each meeting and how fast, when pricing went out, when the buyer went quiet and what the last message was, and the reason the buyer gave when they said no.

## Step 3: Compare wins and losses

Work from the pass notes and pass 1 numbers. Each finding needs counts on both sides.

- **Who wins.** The segments with a win rate clearly above or below the overall rate, with the deal counts behind each.
- **The moves that win.** Compare the first steps (who was on the first call, what was sent after it and how fast, when a second buyer joined, when pricing came up, how the next step was set) and the turning points (on wins, the moment the deal became likely; on losses, the moment it started dying, and what happened or didn't just before). Keep the 3–5 moves that show up on clearly more wins than losses, each as "[N] of [N] wins, [N] of [N] losses". Check every move on both sides; one checked on wins only doesn't count.
- **Noise.** Steps most deals get, won or lost, that don't change the outcome ("every deal gets a full demo"). Naming these saves the team time.
- **Where and why deals die.** The stage and timing where most losses happen. Then the real reason from your reads of each lost deal, compared with the reason in the CRM: give each lost deal you read one main reason, then for each reason count how many of the losses read it explains and how many times the CRM records it (or note that the CRM has no option for it). Note reasons the CRM hides under another label (for example "building it in-house" recorded as "timing") and losses with no reason.
- **The buying group.** Which roles get involved on wins, in what order, and which were missing on losses (for example "the person who signs was on a call before pricing: 9 of 11 wins, 3 of 20 losses").
- **Methodology.** Find the methodology on paper (CRM fields, docs, job posts, call language: MEDDIC or MEDDPICC, SPICED, BANT, Challenger, Sandler, Command of the Message, or their own) and in practice (what reps actually capture). For each element, count how often it was known by a given stage on wins vs. losses ("economic buyer known by proposal: 19 of 25 wins, 6 of 25 losses"). That shows which elements predict a win for this team. With no methodology in use, say so and measure the elements their wins already show, named in the terms of the framework that fits their motion, marked as a suggestion.
- **By rep (leaders).** Each rep's closed deals, win rate and median cycle (a rep who has left keeps a row, marked as left, and deals closed in a bulk cleanup with no activity are noted rather than treated as normal losses), and what the top rep does that the others don't, with counts for both. If ownership changed (a rep left and their deals were reassigned), use who ran the deal (first-call attendee, the rep on the emails) rather than the current owner, and say so. Describe the work, not the person; this report may be shared with the team.
- **Stalled deals now.** How many of the 10 stalled open deals are missing the moves that win, as one line ("8 of 10 stalled deals have no second buyer involved, like the losses").
- **Three things to change this quarter.** From everything above, the 3 changes most likely to raise the win rate, ranked by evidence and how much of the pipeline they touch. Each is specific and checkable on a real deal ("No deal moves past Demo until the person who signs has been on a call: true on 9 of 11 wins, 3 of 20 losses"), never "improve discovery".

Drop any finding you can't back with counts; five true lines beat ten padded ones.

## Step 4: Build the visual report

Build the report from the template in `report-template.md` (in the same folder as this file), as an artifact (a page that opens beside the chat and can be shared), without asking first. Copy the template exactly and replace only the `DATA` object; the page draws itself from it. Every run looks the same, so anyone who has seen one knows where to look. Don't restyle it, add or drop sections, or write your own HTML. If a field has nothing in it, leave it empty (`[]`, `""` or 0) and the page hides that section or says there's nothing to show.

Keep every text field short; the page is for scanning, and `detail` holds the evidence. Every count on the page must match your pass notes and pass 1 numbers. Detail lines can name the deals behind a count (company names only) so every number traces to real deals.

**Never write "you" or "your" in `DATA`.** The page gets forwarded to managers and teammates. Use first names ("Dana's wins") or "the team". Quoted buyer words keep their wording.

| Field | What goes in it |
|---|---|
| `name`, `company` | The person's first name; their company. A personal report is titled "[Name]'s win-loss analysis"; a team view (when `reps` has rows) is "[Company] win-loss analysis", or "Sales team win-loss analysis" if the company is unknown |
| `period`, `pipeline`, `updated` | "Closed Oct 2025 – Oct 2026" · the pipeline(s) covered · the date |
| `numbers` | `closed`, `won`, `lost` (after cleaning), `excluded` (deals left out as not real opportunities: tests, no-shows, research or stray bookings), `winCycle` and `lossCycle` (median days to close), `wonValue` and `lostValue` (0 if no amounts). Plain numbers; the page computes the win rate and formats money |
| `basis` | Counts read: `readWins`, `readLosses`, `readStalled`, `calls`, `callsFull`, `emails` (email threads, or logged emails where only those were available) |
| `changes` | The 3 things to change this quarter: `change` (under 12 words, starts with a verb), `why` (under 20 words, with the counts), `owner` (team view, optional: who drives it), `steps` (2–4 numbered steps someone could follow, naming who and by when; never empty), `context` (optional, one line) |
| `segments` | Segments worth showing, grouped by `dimension` ("Team size", "Lead source", "Industry", "Current CRM", "Customer type"): `name`, `won`, `closed`, `note` (under 12 words), `detail`. The page computes each win rate, colors it against the overall rate and marks fewer than 5 closed as early signal |
| `moves` | The 3–5 moves that win: `move` (under 10 words), `wins`, `winsOf`, `losses`, `lossesOf`, `why` (under 12 words), `detail` (2–4 lines of evidence, naming the deals) |
| `noise` | Steps that don't decide deals: `what`, and the same four counts when you have them |
| `lossStages` | Where losses happen: `stage` (the stage, or the furthest step reached when there's no stage history), `lost` (count), `note` (under 12 words). In stage order |
| `timing` | One sentence on timing, with numbers ("Losses run 48 days at the median, wins 21: lost deals are kept alive too long") |
| `reasons` | Real loss reasons: `reason` (plain words), `found`, `foundOf` (losses read that it explains), `crm`, `crmOf` (how often the CRM records it, out of all losses; `crm: null` when the CRM has no option for it), `note` (under 15 words: what the CRM calls it instead), `detail` |
| `noReason` | Number of losses with no reason in the CRM |
| `buyingGroup` | Each role: `role`, `wins`, `winsOf`, `losses`, `lossesOf` (involved on each side), `note` (when they show up on wins, what they care about) |
| `methodology` | `name`, `onPaper`, `inPractice` (one sentence each), `recommended` (true if suggested rather than found), `elements`: `element`, `byStage`, the four counts, `note`. The page marks an element "Predicts a win" when wins have it at least 25 points more often than losses |
| `stalled` | One line on the stalled open deals compared with wins and losses, with counts |
| `reps` | Team view only, most closed deals first: `name` (first names, including the leader's own row), `won`, `closed`, `cycle` (median days to win), `note` (under 12 words: what stands out in their deals), `detail` |
| `topRep` | Team view: one sentence on what the top rep does that the rest don't, with counts for both. Otherwise "" |
| `profileCheck` | Where the sales profile and the data disagree, one line each with counts ("Profile says we win on price; 2 of 11 wins mention price"). Empty if no profile |
| `openQuestions` | Unresolved questions with the evidence: wins that later cancelled, segments with too few deals, data that couldn't be measured |
| `howBuilt` | Under 40 words: what was read, how it was sampled, what was left out and what couldn't be measured |

If you can't make an artifact here, save the filled template as an `.html` file they can open. Only if you can't show or save HTML at all, give the same sections in the same order as short Markdown.

## Step 5: Reply in the chat

Next to the report, keep the chat short. Lead with what they probably didn't know:

```
[N] closed deals over [period]: [X]% win rate ([N] won, [N] lost; [N] deals left out as not real opportunities).
Read end to end: [N] wins, [N] losses, [N] stalled deals; [N] calls ([N] in full); [N] email threads.

Who wins: [segment] wins [X]% vs. [Y]% overall ([N] deals).
The moves that win:
1. [Move]: [N] of [N] wins, [N] of [N] losses
2. [Move]: ...
Where deals die: [stage], [N] of [N] losses; the real reason is usually [reason] (the CRM says [reason]).

Change this quarter:
1. [Change]
2. [Change]
3. [Change]
```

Leaders: add the top-rep line after the moves. If a source couldn't be read, say so in one line. On the first run, add: "You'll get this same page every time. 'How this report works' at the bottom explains each section."

Then at most one question, only where the answer changes the report (a conflict between the profile and the data, or a segment you can't tell apart), with the likely answer offered.

## Step 6: Save and close

End with these, in this order, kept short:

1. **Save a summary**, as an offer they can accept with "yes": "Want me to save a short summary (`arrows-win-loss.md`) so the other Sales Skills use these findings, and next quarter's run can show what changed?" On yes, write it with these `##` headings, in this order: `## Who wins`, `## The moves that win`, `## Why we lose`, `## Change this quarter`, `## Open questions`. First line: `Win-loss analysis built with Sales Skills by Arrows (arrows.to) for [Name / team], on [date]. Based on [N] closed deals, [N] read in full.` Under 500 words. **Scrub it:** no buyer names, buyer companies, exact amounts or open-deal details; amounts become ranges and examples are described by type ("a mid-market win, closed in 5 weeks"). Competitors stay named. If `arrows-sales-process.md` exists, also offer to refresh just its `## Why we win and lose` section (two short paragraphs, same scrub), leaving every other section as is. Give the file to download, and say how to add it to their Claude project (left sidebar, Projects, open the project, then + next to Files) or wherever their AI tool keeps files.
2. **Quarterly schedule**, only if you can create scheduled tasks and this isn't already scheduled: "Want this to run at the start of every quarter?" Explain a scheduled task in a few words the first time (a saved request Claude runs on its own at the time you pick).
3. **One next step** from the findings: "Want me to check the team's open deals for [the top move] and show which are missing it?" (the process gaps report).

## Special cases

- **No CRM and no CSV.** Say it plainly: "The win-loss analysis needs your closed deals: connect your CRM (click your name at bottom left, then Settings, then Connectors; on a work plan your admin may need to add it first) or drop a CSV export of won and lost deals here (owner, stage, amount, created and close dates, lead source, loss reason, company size)." Any CRM works. Don't build a deal list from guesses.
- **CSV instead of a CRM.** Read it like a CRM in pass 1. Pass 2 then relies on calls and email for each deal; say which comparisons the missing columns ruled out.
- **Few wins** (fewer than 10 on the current motion, say after a product or pricing change): use every current win and compare them with current losses. Still show the 3–5 moves and the 3 changes, since that's what the person needs, but say once at the top of the chat that every pattern is early signal and when to run it again ("after the next 5 wins"), and phrase the changes as things to try and check. If an older pipeline sold a different product, quote its win rate as a reference only; don't mix its wins into the comparison.
- **Thin data** (fewer than 10 closed deals): skip win-vs-loss comparisons, describe what the closed deals have in common, say so at the top, and offer to run it again after the next few closes.
- **No call recorder.** Real loss reasons and buyer language come from email and notes; say the reasons section is thinner and why.
- **No email.** Use CRM activity, calls and notes for the timelines; say so in `howBuilt`.
- **A source fails partway.** Retry once, then use what you have and label totals as partial.
- **The chat is getting long.** Finish the current pass, post its findings, and carry on from the findings rather than re-reading records.
- **Rep on a team.** Their own closed deals only, with the team's files as the standard to compare against. Don't show other reps' deals.
- **Several sales pipelines.** Cover the new-business pipeline new deals are created in now, and offer the others as a follow-up.

## Rules

- **Only what you can trace.** Every number, move and reason comes from their deals, calls and email, with counts on both sides. A wrong pattern teaches the whole team the wrong lesson.
- **Both sides, always.** A move that "happens on 9 of 11 wins" means nothing until you know how often it happened on losses.
- **Evidence over best practice.** Don't fill gaps with generic sales advice. If the data doesn't show what wins, say so; one true move beats five borrowed ones.
- **Real reasons, not the dropdown.** The CRM's loss reason is a starting point; the deal's own calls and emails say what happened.
- **Fair to reps.** Describe the work ("second buyer by the demo on 3 of 12 deals"), never the person, and credit what reps do well.
- **Read only.** Never change the CRM, send anything, or create anything in a connected tool. The only thing saved is the summary file, and only when they say yes.
- **No buyer details in anything saved.** The summary file is shared and reused for months; scrub it as above.

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
