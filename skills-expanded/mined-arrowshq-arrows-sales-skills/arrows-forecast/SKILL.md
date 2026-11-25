---
name: arrows-forecast
description: "Objective forecast from Sales Skills by Arrows. A bystander's read of every deal the CRM has closing this month (or this quarter, when asked): how likely it really is and when it will really close, judged only from what the buyer said and did on calls, in email and on the calendar, never from the CRM's stage, probability or close date. Shows the CRM's number next to the evidence for every deal, what each buyer still hasn't done, deals the CRM has ahead of or behind the evidence, dates likely to slip, and one question per rep for leaders. Leads with the decisions: which close dates to move, which deals to close out, which deal needs one buyer action this week. Read only; a shareable visual report. Use whenever someone says 'Run my Arrows forecast', 'forecast my pipeline', 'what's really going to close this month', 'what's really going to close this quarter', 'is this deal really at 70%', asks which deals will slip or how much of the pipeline is real, or wants an unbiased number before a forecast call."
---

**Period:** this month (or the month or quarter the person names)

A CRM forecast is a stage probability and a close date someone typed in. This skill gives the other read: what a bystander who sat in on every call and read every email would say about each deal, how likely it is to close and when, judged only from what the buyer said and did. It shows that next to the CRM's number so the person can see where the pipeline is ahead of the evidence and where it's behind, deal by deal.

It is about the CRM and the buyers, never about the people selling. A gap means the stage or close date doesn't match what the buyer has done yet; it does not mean a rep is wrong.

| Section | What's in it |
|---|---|
| Header | "[Company] objective forecast" (personal view: "[Name]'s objective forecast"), one line explaining the two numbers, a bar of commit / likely / possible / unlikely by value, and four numbers: deals dated this period in the CRM, what the CRM says, what the evidence says, and what's likely to slip (or the goal and coverage, when a goal is known) |
| What will really close, and when | Every deal in the period, most likely first: the label, the buyer's own date when there is one, the one thing the buyer hasn't done yet, and the one move on the seller's side that would get it done; open any deal for the evidence |
| CRM ahead of the evidence | Deals whose stage probability or close date is ahead of what the buyer has done, by money at stake, each with CRM % → evidence %, CRM date → evidence date, and the one fact behind it |
| Further along than the CRM shows | Deals the evidence rates higher than the stage, with the buyer fact that earned it |
| Likely to slip | Deals whose evidence date lands after the period, and the value that leaves the period with them |
| By rep (leaders) | Each rep's CRM total vs. the evidence and one question for their 1:1; open a rep for their deals |
| How the forecast works | The rubric in plain words, so anyone can check a number |

The default output is a visual report built from one fixed template (in `report-template.md`, next to this file), so it looks the same every run. A short summary goes in the chat alongside it.

## Progress

Post a short progress line once at the top, then one line per source as it finishes, with a real number:

```
Sales Skills by Arrows · Objective forecast  ■■□□□  Reading your calls

✓ CRM: 6 deals dated this month ($134k), 3 owners
✓ Calls: 40 calls on those deals in the last 60 days
✓ Email: checked 108 logged threads for buyer-side signals
– Calendar: not connected (using CRM meeting dates)
```

Stages: `Reading your CRM` / `Reading your calls` / `Reading your email` ■□□□□ · `Scoring the evidence` ■■■□□ · `Building your report` ■■■■□ · `Done` ■■■■■.

## Step 1: Read the profile

Use the profile files if they're in the project. They say what a real buying process looks like for this company, which is the yardstick for every deal.

- `arrows-sales-process.md`: `## Pipeline stages` gives the stage order, what has to be true to move on, typical time in stage, and conversion. `## Discovery and qualification` gives the methodology and what has to be known by when (economic buyer, decision process, paper process). `## Why we win and lose` says what the winning deals had. `## Numbers` gives cycle length and win rate.
- `arrows-methodology.md` (if present): the methodology in depth, replacing `## Discovery and qualification`. `## By stage` says what has to be known by each stage and `## How to check a deal` what counts as known, so an element without that proof doesn't count toward a deal's evidence.
- `arrows-how-i-work.md`: `## About me` says rep, leader or both. `## What slips` tells you what to look for first.
- `arrows-how-we-work.md` (leaders): `## What I want to see weekly`, and `## Every rep, every deal` for what should be true on each deal.
- `arrows-crm-guide.md` (if present): which CRM field holds the forecast category or probability, and what each stage's probability is set to.

No profile: run the forecast anyway with stages and probabilities straight from the CRM, and use the shared context's one-line setup suggestion at the end.

## Step 2: Decide whose forecast and which period

There are two versions of the same report. Rep ("[Name]'s objective forecast"): deals they own, no rollup or owner names. Leader ("[Company] objective forecast"): deals owned by their team, rolled up by rep. Both: the team view, with their own deals as a row under their first name.

Use `scope` if given. Otherwise use `## About me`; failing that, match their email to a CRM owner (owns most open deals → rep; others own most and they own few → leader). Seeing everyone's deals proves nothing. Don't stop to ask; say in the report header which view you built ("Team view · 3 owners · Q4 2026").

**Period.** The current month unless they name a quarter or another month. A month is small enough to read in one sitting and act on: a handful of deals, each with a decision attached. The quarter view is for when someone asks for it, usually before a quarterly forecast call, and it gets long. Deals in scope are open deals with a CRM close date inside the period: that is what the CRM currently expects to close, and the whole report is a check on that expectation. Also pull open deals with a close date in the 30 days after the period: they're candidates for "Further along than the CRM shows" (a deal that could pull in) and are never counted in the forecast numbers.

**Goal.** Use the goal if they state one, or if the profile or CRM holds a quota or target for the period. Otherwise leave it out. Never invent a goal, and never judge pipeline coverage against an industry rule of thumb; show the coverage number and let them decide what it means.

Use the sales pipeline only. CRMs often also hold onboarding, renewal or support pipelines; skip those. If there are several sales pipelines, use the one the profile names, or the one with the most open deals in the period, and say which in the header.

## Step 3: Pull the data

**Reading budget,** so the forecast finishes in one chat:
- **CRM:** filtered queries for the deals in scope (stage, amount, close date, create date, owner, forecast category or deal-level probability if the CRM has one, stage probability, stage-entry date and close-date history if available, next step, contacts and their titles). Up to 120 deals; if there are more, take the 120 largest and say so ("scored 120 of about 180 deals in the period"). Notes and logged activity (notes, calls, emails, meetings) for every deal you score, pulled in a few batched queries by deal association rather than one call per deal.
- **Calls:** summaries for every call on these deals in the last 60 days. Full transcripts (or transcript search) for at most 8 deals, chosen where the CRM number and the evidence look furthest apart or where a buyer date or decision was mentioned in a summary and you need the exact words.
- **Email:** for each deal, the last 60 days of threads with the buyer's domain. Read for buyer-side signals (below), not for the seller's activity. A leader's inbox won't show reps' threads; for those, use emails logged on the CRM deal and say so in `howBuilt`.
- **Calendar:** the last 60 days and the next 30, matched by attendee domain, to see what was held and what's booked. A leader's calendar won't show reps' meetings; use the CRM's meeting records.
- **Chat and contracts** (if connected): search the buyer's company name for internal deal talk; check signing tools for sent, viewed and signed paper.

**Only what the buyer said and did counts.** The seller's notes about a deal ("they love it", "verbal yes") are not evidence unless a buyer message, call quote or calendar event backs them up. When a note claims something you can't confirm, treat it as unconfirmed and say so in the deal's evidence. The point of this forecast is that it's built from the buyer's side.

**Last activity means the last two-way touch on any channel:** a buyer reply, a call held, a meeting attended. CRM "last activity" often counts outbound emails nobody answered, and an email open is not a reply. Cross-check before calling a deal quiet.

## Step 4: Score every deal

Score each deal with the same rubric so the number is reproducible: the same evidence always gives the same number, and anyone can check it. Likelihood is a tier, not a feeling. Find the highest tier whose evidence the deal has, then apply the caps. Use the profile's stage definitions to translate ("economic buyer", "paper process") into the company's own words; on the page, call the economic buyer "the budget holder" unless the profile uses another term.

**Tiers** (the deal has to have the evidence named, from the buyer's side):

| Evidence % | Label | What the buyer has done |
|---|---|---|
| 90 | Commit | Contract or order form is with the buyer and the buyer (not the seller) named a signature date, or a verbal yes came from the budget holder in their own words on a call or in writing, with paper in motion |
| 75 | Commit | The budget holder agreed to pricing or terms in writing or on a recorded call, and the buyer's paper process has started (the buyer asked for or received the contract, MSA or security questionnaire, or named their legal or procurement contact) |
| 60 | Likely | The budget holder has met with the seller, the buyer gave a decision date or process in their own words, and a next step is booked |
| 40 | Possible | A champion is engaged and replying, a next step is booked, and either at least two buyer contacts are involved or the budget holder is the one engaged; no buyer-stated decision date |
| 25 | Possible | Active two-way contact in the last 14 days, but no booked next step, or single-threaded, or the timeline exists only in the CRM or the seller's notes |
| 10 | Unlikely | No buyer reply in 14+ days, or no next step and no buyer reply in the last 7 days |
| 0 | Not this period | The buyer said there's no budget or chose someone else, or no buyer reply in 30+ days. (A buyer who named a date after the period is a slip, handled by the date rule below, and keeps the tier the rest of the evidence earns.) |

**Caps,** applied after the tier, each one named in the evidence:
- No budget holder identified from buyer-side evidence: at most 40.
- No two-way touch in 14+ days: at most 25. In 30+ days: 0 for this period.
- Close date moved twice or more in the period: at most 40.
- A competitor named by the buyer in the last 30 days with no buyer statement of preference: at most 60.
- A buyer-side promise missed by more than 2 business days (they said they'd confirm by Monday and didn't): one tier down.
- New deal (created in the last 14 days) with no call held yet: at most 25, whatever the stage says.

**What the buyer hasn't done yet** (`blocker`, one per deal, under 8 words): the single thing that would move the deal to the next tier, in the buyer's terms. "No decision date from the buyer", "Budget holder not on a call", "No reply since Oct 1", "Paper process not started", "Security review not started". For a Commit deal with nothing missing, "Signature by [date]".

**What would move it** (`move`, one per deal, under 12 words, starts with who): the one thing someone on the seller's side can do this week to get the buyer to do the blocker, grounded in the evidence (a date the buyer mentioned, a person they named, a call already on the calendar). "[Rep]: book a pricing call with [Champion] and [Economic buyer] for the week of [date]", "[Rep]: ask [Champion] on [date] to bring [Decision maker] to the next call". When nothing on the seller's side can move it, say so plainly: "Close out [date] unless [Buyer] replies", "Nothing until [Buyer] replies; reopen then". This is the bonus the page earns its keep with: a deal with a low number and a clear move is good news, not bad.

**Evidence close date.** Take the later of:
1. The date the buyer gave, in their own words (not the CRM field), moved to the end of that month if they said "end of month", and so on. Record it as `buyerDate` with who said it and when ("Nov 7, CFO, Oct 10 email"); leave `buyerDate` null when no buyer gave one.
2. The date the remaining steps could realistically finish, using typical time in stage from `## Pipeline stages` (or the CRM's average days in stage, or 14 days per remaining stage with nothing else), counted from today. Count the steps still ahead: paper process not started adds its usual time; no budget holder meeting adds a stage; a pilot or evaluation the buyer has deferred adds the deferral.

If the evidence date falls after the period, the deal goes in "Likely to slip": it contributes 0 to this period's evidence number, and its full amount counts toward `slipValue` (the pipeline leaving the period). It keeps its tier and label, which say how likely it is to close in the period it slips into.

**CRM number.** Use, in this order: the forecast category or deal-level probability if the CRM has one; else the stage probability the CRM assigns; else the stage's position in the pipeline mapped onto the tiers above. Say which in `howBuilt` and in `crmLabel` ("stage probability", "forecast category"). The CRM date is the CRM close date. These are the CRM's numbers, so the page calls them "CRM says"; never "reps say" or "[Name] says".

**Evidence value** = amount × evidence %, summed over the deals in the period that aren't slipping (a slip contributes 0). **CRM value** = amount × CRM %, summed over every deal in the period including the ones likely to slip, because that is the number the CRM is carrying and the reader is comparing against.

**Deals with no amount** ($0 or blank): score them and list them, but leave them out of every money total and say how many there were in `howBuilt`. They show "no amount" on the row.

**The gap** for a deal = (CRM % − evidence %) × amount. "CRM ahead of the evidence" ranks positive gaps by size; "Further along than the CRM shows" lists negative gaps of 10 points or more.

**By rep** (leaders): for each owner, the CRM value and evidence value of their deals in the period (slips at 0 on the evidence side) and one question for the 1:1, about a specific deal and the decision it needs ("[Company]: is [date] real with nothing booked? Move it to next month?"). No scores, labels, counts or adjectives about the person; the deals and the question do the work.

## Step 5: Build the visual report

Build the report from the template in `report-template.md` (in the same folder as this file), as an artifact (a page that opens beside the chat and can be shared), without asking first. Copy the template exactly and replace only the `DATA` object; the page draws itself from it. The template is already tested, so don't rebuild it, re-verify it or render it before handing it over; the time goes into the scoring, not the page. Use it on every run, including scheduled ones: people learn this page and orient around it, so the layout, sections and order never change. Don't restyle it, add or drop sections, or write your own HTML or a Markdown version in its place. If a field has nothing in it, leave it empty (`[]`, `null` or `""`) and the page handles it.

Never write "you" or "your" anywhere in `DATA`: use the person's first name, reps' first names, or "the team", because reports get forwarded. Only quoted text (a line from a call or email) may keep it. The chat reply can still speak to the person directly. Use the buyer's company name for each deal ("Northwind", not "Northwind - New Business Q4"). Keep every text field short; the report is for scanning.

| Field | What goes in it |
|---|---|
| `name`, `company` | The person's first name and their company, from the inputs, profile, CRM or email domain. A personal view is titled "Sam's objective forecast"; a team view (when `reps` has rows) is titled "Acme objective forecast", or "Sales team objective forecast" if the company isn't known. |
| `period`, `periodEnd`, `view`, `pipeline`, `updated`, `crmLabel` | "Q4 2026" · "Dec 31" · "My deals" or "Team view · 3 owners" · the pipeline used · date and time · what the CRM number is ("stage probability" or "forecast category") |
| `numbers` | `dealCount`, `noAmountCount`, `pipelineValue` (sum of amounts in the period), `crmValue`, `objectiveValue`, `goal` (null if unknown), `commitValue`, `likelyValue`, `possibleValue`, `unlikelyValue` (evidence value by label; these four sum to `objectiveValue`), `slipValue` (sum of the amounts of deals likely to slip; not in `objectiveValue`), `slipCount`. Plain numbers; the page formats money. |
| `deals` | Every deal in the period (up to 120), most likely first, then earliest evidence date: `deal`, `amount` (null when none), `owner`, `stage`, `crmPct`, `objPct`, `crmDate`, `objDate`, `buyerDate` (the buyer's own date with who and when, or null), `label` ("commit", "likely", "possible", "unlikely", "none" for 0, "slip" for a deal leaving the period), `blocker` (what the buyer hasn't done yet, under 8 words), `move` (the one seller-side move that would get it done, under 12 words, starting with who), `why` (under 10 words, the one fact behind the score), `evidence`. |
| `evidence` | What opens under the caret, on every deal (the page puts `why` first, then these): 2–5 lines, each a fact with its date and source, buyer-side first ("Oct 3 call: CFO said 'we'd sign this month if legal clears'", "Oct 9 email: security questionnaire returned", "Budget holder: not named in any call or email", "Cap: quiet 16 days → at most 25"). Name every cap that applied. Where a seller's note was the only source for a claim, say "note only, unconfirmed". |
| `ahead` | Deals where the CRM % is above the evidence % (positive gap), biggest gap first, up to 6 (8 in a team view): the same fields as `deals`. |
| `further` | Deals where the evidence % is at least 10 points above the CRM %, plus deals from the 30 days after the period with buyer evidence that could pull them in: the same fields as `deals`. Up to 6. |
| `slip` | Deals whose evidence date falls after `periodEnd`, largest amount first: the same fields as `deals`, `label: "slip"`. These deals also appear in `deals`. |
| `reps` | Team view only, one row per owner with deals in the period, biggest CRM-vs-evidence difference first: `name`, `dealCount`, `crmValue`, `objValue`, `ask` (one question for the 1:1, under 20 words, about a specific deal and the decision it needs), `detail` (optional, 1–3 lines). Opening a rep lists their deals automatically, matched by `owner`, so use the exact same owner names everywhere. Empty for a rep's own forecast. |
| `howBuilt` | One or two sentences, under 60 words: what you read, where the CRM number came from, any sampling, any source that was missing, and how many deals had no amount. |

**Labels on the page.** "Commit" is 75 and up, "Likely" is 60, "Possible" is 25 to 40, "Unlikely" is 10, 0 shows as "Not this period", and a deal leaving the period shows "Likely to slip". The bar in the header splits the evidence value by those labels.

If you can't make an artifact here, save the filled template as an HTML file they can open. Only if the tool can't show or save HTML at all, give the same sections, in the same order, as short Markdown, with a table for "What will really close" and "By rep". If they say they'll paste it into a doc, give that Markdown version too, after the chat reply.

## Step 6: Reply in the chat

Lead with the decisions, not the numbers. The person opened the chat to decide something, and the page holds the detail.

```
[N] deals dated [period] in the CRM, $[pipeline]. The evidence says $[evidence value] will close. [N] deals ($[X]) will likely slip past [period end].

Decisions this week:
- Move: [Deal] to [evidence date] ([what the buyer hasn't done, under 8 words]); [Deal] to [date] (...)
- Close out: [Deal] ([why, under 8 words]); [Deal] (...)
- One buyer action: [Deal]: [the one thing that moves it up a tier, and who does it]

[Sources line: "Scored from calls, email and the CRM. Calendar not connected, so booked meetings came from CRM records."]
```

"Move" is every deal likely to slip, with the evidence date. "Close out" is every deal at 0 for the period, and any deal whose close date has already passed with no buyer reply. "One buyer action" is the one or two deals closest to moving up a tier, taken from their `move` lines (a budget holder to get on a call, a date to ask for, paper to send) and who on the seller's side does it. Leave a line out if it's empty. Keep each line under 15 words; the page has the rest.

In a team view, add one line per rep after the decisions with their 1:1 question ("[Rep]: [Company]: is [date] real with nothing booked? Move it to next month?"), since that's usually what the leader came for.

The first time someone runs this forecast (no earlier report in the conversation or project), add one line: "You'll get this same page every time, in the same order. 'How the forecast works' at the bottom shows the rubric, so anyone can check a number."

Then one offer the person can accept with "yes," tied to what you found ("Want me to draft the note to get [budget holder] on a call at [deal]?" or, for leaders, "Want 1:1 notes for [rep]?").

**Scheduling (recommend it on the first run):** a forecast is most useful when it's waiting before the forecast call, so when it isn't scheduled yet, recommend that and make it your one offer instead of the one above. First check whether an objective forecast is already scheduled (a scheduled task or routine with this forecast in its name or prompt); if it is, say nothing about scheduling.
- **If you can create scheduled tasks:** "Want this ready every Monday at 7am, before the week's forecast call? Say yes and I'll set it up." If yes, create it to run this forecast at the time they pick and confirm in one line.
- **If you can't create one here:** recommend it with the steps instead, once: "Tip: set this up to run itself every Monday. In the Claude app, open Scheduled in the sidebar, create a new weekly task for Monday 7am, and use the prompt: Run my Arrows forecast." Keep it to that; don't repeat it on later runs.

## Special cases

**No CRM connected:** ask once for a CSV export of open deals (owner, stage, amount, close date, probability if there is one) and read it like a CRM. Without one, build the forecast from email, calls and calendar alone: every buyer conversation with a date or decision in it becomes a deal, with no CRM number to compare against. Label it "Built from email and calls; no CRM" and leave `crmPct` and `crmValue` empty.

**No CRM number anywhere** (no probability field, no stage probabilities): show only the evidence side, leave `crmPct` null on every deal, leave `ahead` and `further` empty, and say so in `howBuilt`.

**No calls connected:** score from email, calendar and CRM activity only, and say in `howBuilt` that buyer quotes from calls weren't available, so tiers that need a buyer's spoken words were judged from email alone.

**Thin data:** fewer than 5 deals in the period, leave `ahead`, `further` and `reps` empty; the page shows those sections with their empty state and "What will really close" already lists everything. No amounts: count deals instead of value and leave money fields 0.

**A source fails partway:** retry once, then continue with what you have and say what's missing in the sources line. Base numbers only on what you read.

**One deal:** if they ask about a single deal ("is Northwind really at 70%?"), skip the report and answer in the chat: the CRM number, the evidence number and date, the tier and caps that produced it, what the buyer hasn't done yet, and the evidence lines. Offer the full forecast at the end.

**Leader with no team data in the CRM:** use the deal owners on the deals they can see, list them, and say the team was inferred from deal ownership.

## Rules

- **Buyer-side evidence only.** A number moves up only because of something the buyer said or did, with a date and a source. Seller notes, stage names and enthusiasm don't move it. If the only support for a claim is a note, mark it unconfirmed.
- **Same evidence, same number.** Score with the tiers and caps above, every time, and show which ones applied. Never round a number up because the deal "feels" close, and never pick a number between tiers.
- **Every fact traces to a source.** No invented quotes, dates or contacts. A wrong "CFO said next quarter" on a deal that signs Friday makes the whole forecast untrustworthy.
- **Read only.** Don't change probabilities, close dates or stages in the CRM, even when the gap is obvious. Suggest; the person decides. The forecast should be safe to run on a schedule.
- **About the CRM and the buyer, never the seller.** Leaders share this. A gap is "the CRM has it at 60%; the budget holder hasn't been on a call", never "Sam oversells". No scores, rankings or adjectives about people anywhere on the page or in the chat.
- **Say what each number is.** "CRM says" is always labeled with its source (stage probability or forecast category) on the page, and the first line under the title explains the two numbers in plain words. A reader who has never seen the page should know what every number means without asking.
- **No verdict on coverage.** Show pipeline against the goal; don't say whether 1.5x or 3x is right. Teams differ.
- **No cheerleading.** If the evidence and the CRM agree, say "The CRM and the evidence agree within $X" and stop.
- **Use their words.** Stage names, methodology terms and forecast categories come from their CRM and profile, not generic sales language.
- **Scannable in 30 seconds.** The label, the numbers, what's missing and the move on the row; the reason and the evidence under the caret. Four short lines per deal, no more.
- **Every low number comes with a move.** A deal at 10% with "[Rep]: one closing note to [Buyer]; close out if no reply by [date]" is a decision made. A deal at 10% with nothing is just bad news. If there is truly no move, say "close it out"; that's a move too.
- **Nothing saved with buyer details.** If you keep anything for a later comparison, keep it to counts and totals, with no buyer names or exact amounts.

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
