---
name: arrows-process-gaps-report
description: "Arrows process gaps report: finds what's falling through the cracks in your pipeline, measured against your own sales process. Part 1 is what should be happening and isn't: promised follow-ups that never went out, deals quiet 14+ days with money at stake, missing next steps, single-threaded deals, no economic buyer, stale close dates and stages, calls never logged in the CRM. Part 2 is the habits your best deals (or top rep) have that the rest don't. Gives $ at risk, an at-risk list with one line of why, and the 3–5 moves to make this week, with a by-rep view for leaders, as a shareable visual report. Use whenever someone says 'Run my Arrows process gaps report', 'Run my gaps report', 'What's falling through the cracks?', 'What am I dropping?', 'Where is my team slipping?', asks which follow-ups they forgot or which deals are quietly dying, or wants a pipeline health check against how they say they sell."
---

Finds what's falling through the cracks, measured against how this person (or their team) says they sell. Not a pipeline review of every deal: only the gaps, the money behind them, and what to do this week.

| Part | What it answers | Where the standard comes from |
|---|---|---|
| Headline | $ at risk, $ gone quiet, promises missed this month | CRM, email, calls |
| Part 1: Gaps by deal | What should be getting done and isn't: at risk (red), other gaps (gold), on track (green), with one line on why | Their stages, methodology and rules (`arrows-sales-process.md`, `arrows-how-we-work.md`), or the baseline below |
| Part 2: Habits | What they want to be doing that isn't happening, with counts | `## What I do on my best deals` and `## What slips` (`arrows-how-i-work.md`), `## Every rep, every deal` (`arrows-how-we-work.md`) |
| This week | The 3–5 moves that close the biggest gaps | Both parts |
| By rep (leaders) | Each rep's gaps and habits side by side, and what the top rep does that others don't | Same, per owner |

Delivered as a visual report they can share (the same page every run), with a short summary in the chat. No questions unless the scope is truly unclear.

## Progress

Post a short progress line once at the top, then one line per source as it finishes, with a real number:

```
Sales Skills by Arrows · Process gaps report  ■■□□□  Reading your calls

✓ CRM: 38 open deals ($1.2M), 4 owners
✓ Calls: 22 calls in the last 30 days
✓ Email: checked 31 threads for promised follow-ups
– Calendar: not connected (using CRM meeting dates)
```

Stages: `Reading your CRM` / `Reading your calls` / `Reading your email` ■□□□□ · `Checking against your process` ■■■□□ · `Building your report` ■■■■□ · `Done` ■■■■■.

## Step 1: Scope and standard

**Who's covered.** Use `scope` if given. Otherwise read `## About me` in `arrows-how-i-work.md` (rep, leader, or both). With no profile, match their email to a CRM owner: owns most open deals → rep; others own most → leader; a real share of both → both. Seeing every deal proves nothing (small-company reps often have admin access).

- **Rep or solo seller:** their own open deals.
- **Leader:** their team's open deals (from CRM team data, `## Our team`, or owners of deals they've touched in the last 90 days), rolled up by rep. If they also carry deals, show theirs as one of the reps.
- **Both (leads a team and carries any open deals of their own, even a few):** go by their words. "My deals", "what am I dropping", "my pipeline" → their own deals, with a one-line offer of the team view at the end. "My team", "where are we slipping", or just the trigger phrase → the team view, with their deals as one rep.
- A leader who owns no open deals gets the team view whatever the wording. If you truly can't tell, run it on their own deals and offer the team version at the end. Don't stop to ask.

Only live sales pipelines: skip onboarding, renewal or support pipelines unless asked, and skip pipelines that look retired (named old or archived, or with no activity in 90 days). If there are several live sales pipelines, cover them all and label each.

**The standard to measure against.** Gaps only mean something against a standard, so set it first and say which one you used (it goes in `measuredAgainst`).

1. Their profile: stages and exit criteria (`## Pipeline stages`), methodology (`## Discovery and qualification`, or `arrows-methodology.md` if present: its `## By stage` says what each stage needs and `## How to check a deal` what counts as known), rules (`## My rules`, `## Team rules`, `## Every rep, every deal`), best-deal moves and what slips.
2. With no profile, infer what you can from the CRM (stage names, required fields, methodology fields that exist) and fill the rest with this baseline:
   - Follow-up within 1 business day of every buyer call.
   - Every open deal has a next step with a date, and that date hasn't passed.
   - Two-way contact with the buyer at least every 14 days.
   - At least two buyer contacts engaged before proposal or pricing.
   - Economic buyer identified before proposal.
   - Close date backed by recent activity; stage matches what has actually happened.
   - CRM updated within 1 business day of a call.

## Step 2: Read the data

**Reading budget.** Stay inside this so the report finishes in one chat, and say when you sampled ("checked activity on the 40 largest of 112 open deals").

- **CRM:** all open deals in scope through filtered list queries (stage, amount, close date, owner, created, last activity, next step and its date, contact count, methodology fields). Up to 150 deals. Pull associated contacts and activity (emails, meetings, notes, tasks) for at most 40 deals, largest and closest-to-close first. For Part 2, won deals from the last 6 months, at most 20, summary fields only.
- **Calls:** list call summaries and action items from the last 30 days (summaries that come back in a list are cheap). Full transcripts for at most 3, only where a summary hints at a promise you can't confirm.
- **Email:** search sent mail for the buyer domains on deals with a call or promise in the last 30 days, at most 40 threads. Also scan the last 14 days of inbound mail from outside the company (every sender, not just contacts on open deals, and shared inboxes too) for questions or requests nobody answered, at most 30 threads: in a shared inbox, list the open or unassigned conversations from the last 14 days; in personal mail, look for inbound threads from outside the company with no reply after them. Unhappy customers and cancellation requests often come from people with no open deal, so a deal-by-deal search misses them. Check every place a follow-up could have gone out before calling it missed: each connected mailbox or shared inbox tool, emails logged on the CRM deal, and chat. People often send from a different tool than the one connected, so name which ones you could and couldn't check. Read only what you need to confirm a follow-up went out.
- **Calendar:** external meetings in the last 30 days and the next 14. Match them to deals by attendee domain.
- **Leaders:** the same per rep, but at most 15 activity reads per rep; per-rep totals for everything else.

**What counts as activity.** A two-way touch is a buyer reply, a meeting held, or a call. Outbound emails with no reply don't reset the clock; they count as attempts. Cross-check CRM "last activity" against email, calendar and chat before calling a deal quiet: the CRM often misses touches.

**Shared definition of at risk** (the same across every Sales Skill): quiet 14+ days with no two-way touch, no next step, or a promised next step that didn't happen. A deal created in the last 14 days isn't at risk just for having no next step yet; that's noise on a new deal.

## Step 3: Find the gaps (Part 1)

Check every deal in scope against the standard. For each gap, keep the evidence: a date, a quote, a count.

| Gap | How to check it |
|---|---|
| **Promise missed** | Commitments the seller made on a call ("I'll send the security doc Friday") or in email ("I'll get you pricing tomorrow"), from call action items, summaries and sent mail. Missed if nothing matching went to the buyer by the promised date, or within 2 business days if no date was given. If you couldn't check where it would have been sent, mark it "couldn't confirm" rather than missed. Count only the seller's promises, not the buyer's. Include promises the person made on calls they joined for someone else's deal (an exec on a teammate's call, for example): list those under the deal with "([Name] owes this)". |
| **Quiet with $ at stake** | No two-way touch in 14+ days. Show days and amount. |
| **No next step / next step passed** | No future meeting booked and no next step with a date, or the next-step date passed with no matching activity. "Waiting on the buyer to get back to us" with no date counts as no next step: someone on the seller's side should own the next touch. A next step counts only if it has a date: a meeting on the calendar with someone from the buyer, or a dated task or promise. "Waiting on approvals", "next week" with no date, or a meeting you can't see the date of doesn't count. Allow 2 business days after a two-way touch to book it; a buyer who wrote yesterday isn't at risk yet, just a deal that needs a meeting booked (an other gap). A deal created in the last 14 days isn't at risk just for having no next step yet; that's noise on a new deal. |
| **Single-threaded** | Only one buyer contact engaged (emailed, met, or on a call) and the deal is past the stage where their process expects more (or past the first third of their stages with no profile). |
| **No economic buyer** | No contact with a decision-maker title or role at or after proposal. |
| **Methodology gaps** | Fields or topics their methodology requires by this stage that are missing (for example MEDDIC's metrics or decision process; for SPICED, impact or critical event). Name the specific missing piece. |
| **Close date doesn't match activity** | Close date this month or already past, but quiet, early stage, or no pricing or paperwork sent. Or the close date has been pushed 2+ times. |
| **Stage doesn't match what happened** | The stage claims something the activity doesn't show (Proposal with no proposal sent, Demo Done with no demo on the calendar), or a deal has sat in a stage much longer than their typical time. |
| **Call with no CRM update** | A buyer call on the calendar or recorder with no note, activity or field change on the deal within 1 business day. |
| **Buyer waiting on a reply** | A buyer or customer asked something or asked for something (pricing, a document, a cancellation, a meeting time) by email or chat, and nobody on the seller's side answered within 2 business days. Check the person's inboxes, including shared ones; a cancellation or complaint from a customer counts even without an open deal. These are promises in reverse, so list them under promises as missed. |
| **Buyer conversation with no deal** | External calls in the last 30 days, or booked in the next 14, with a prospect or customer who has no open deal (a win-back, an expansion, a pilot set up informally, a demo booked tomorrow). List these after the deals, one line each, in Part 1. |

**Sort every deal into one of three groups.** **At risk** (red) if any one of these is true: quiet 14+ days, no next step (as defined above), a next-step date passed, or a promise to the buyer was missed. That's the at-risk definition, applied strictly, so the same deal gets the same status in every skill; a big, otherwise healthy deal waiting on the buyer with no date is still at risk. **Other gaps** means there are gaps (single-threaded, methodology, close date or stage mismatch, no CRM update) but none of the at-risk ones. **On track** means nothing found. Rank at risk by amount, then by how close the close date is. Statuses, not scores: a rep can act on "at risk because the pricing you promised on the 12th never went out"; they can't act on "62/100". In the report, red is at risk, gold is other gaps (needs attention, not bad yet) and green is what's going well.

**Headline numbers.**
- **$ at risk:** total amount on red deals.
- **$ gone quiet:** total amount on deals with no two-way touch in 14+ days (overlaps with at risk; say so).
- **Promises missed this month:** count, plus how many you couldn't confirm.

Leave a number out if you can't compute it (for example, no amounts in the CRM) rather than guess.

## Step 4: Check the habits (Part 2)

Pick 3–5 habits and measure each one across the deals in scope over the last 30–90 days, as a count: "recap within a day of a demo: 4 of 13 demos".

Where the habits come from, in order:
1. `## What I do on my best deals` and `## What slips` in `arrows-how-i-work.md`: what their best deals got that the rest didn't.
2. `## Every rep, every deal` and `## Team rules` in `arrows-how-we-work.md` (leaders and their reps).
3. With no profile: compare up to 20 recent wins with the open deals. Habits most wins had that open deals lack (second contact by a given stage, a recap after the demo, next meeting booked on the call, a business case before pricing). Mark these "(inferred from your wins)". If there are fewer than 5 wins, use the baseline habits above.

**Leaders:** for each habit, show it per rep, find the top rep (by win rate, or by how consistently they do the habits if win rates are too thin to compare) and name what they do that the rest of the team doesn't, with counts for both. Keep it factual and about the work, not the person: this report may be shared with the team.

Only report a habit you could actually measure. If a habit can't be checked from the connected data (for example, call quality with no recorder), say so in one line instead.

## Step 5: Pick the moves for this week

3–5 moves, ranked by money and time sensitivity. Each is one specific action on a specific deal or habit, doable this week: "Send [Company] the pricing promised on the 12th, today", not "improve follow-up". Leaders: name the rep who owns each move, and make at least one a team habit to raise in the next team meeting.

## Step 6: Build the visual report

Build the report from the template in `report-template.md` (in the same folder as this file), as an artifact (a page that opens beside the chat and can be shared), without asking first. Copy the template exactly and replace only the `DATA` object; the page draws itself from it. Use it on every run, including scheduled ones: people learn this page and know where to look each week, so the layout, sections and order never change. Don't restyle it, add or drop sections, or write your own HTML in its place. If a field has nothing in it, leave it empty (`[]`, `""` or 0) and the page handles it.

Use the buyer's company name for each deal ("Northwind", not "Northwind - New Business Q3"). Keep every text field short: the page is for scanning, and the full story goes in `detail`.

**Never write "you" or "your" in `DATA`.** The page gets forwarded to managers and teammates, and "you owe this" means nothing to them. Use the person's first name ("Dana owes this", "Dana's Oct 2 call", "Dana's what-slips list") and reps' first names; for the team as a whole, "the team". The chat reply can still talk to the person directly.

| Field | What goes in it |
|---|---|
| `name` | The person's first name. A personal report is titled "[Name]'s process gaps report". |
| `company` | Their company, from the conversation, profile files, CRM or email domain. A team view (when `reps` has rows) is titled "[Company] process gaps report"; leave it "" if unknown and it reads "Sales team process gaps report". |
| `period`, `view`, `pipeline`, `updated` | "Week of Oct 5" · "My deals" or "Team view · 4 reps" · the pipeline(s) covered · date and time |
| `numbers` | `open`, `value` (open pipeline), `atRiskValue`, `atRiskCount`, `gapsValue` (value on other-gaps deals), `quietValue`, `quietCount`, `promisesMissed`, `promisesUnconfirmed`. Plain numbers; the page formats money. Use 0 when unknown and say so in `howBuilt`. On individual deals, leave `amount` empty ("") when the CRM has none; never put 0, which reads as a $0 deal. |
| `goingWell` | 2–4 things that are working, so the page isn't only bad news: a habit done consistently, a deal that moved, a promise kept fast. `what` (under 8 words), `note` (under 12 words, with a count or date), `detail` |
| `atRisk` | Every at-risk deal (up to 40), most important first: `deal`, `amount`, `owner` (team view; spelled exactly as in `reps`), `stage`, `gaps` (2–4 short tags, the reason it's at risk first: "Quiet 17d", "No next step", "Promise missed", "Next step passed", "[Name] owes this", "No economic buyer", "Single-threaded", "Close date passed"), `why` (under 12 words, with a date or day count as evidence), `next` (under 6 words, a concrete action), `detail` |
| `doThisWeek` | The 3–5 moves: `deal` (the company name, or "Team habit"; it leads the row in bold, because the company is what people scan for), `amount`, `owner` (team view), `action` (its own line under the company, under 8 words, starts with a verb and names who to contact: "Email Dana to book the security review"), `why` (under 10 words), `steps`, `context` |
| `steps` | For `doThisWeek`, always: 2–4 numbered steps someone could follow without thinking, each naming who, how and when ("Email Dana today: ask whether the Oct 15 board date still holds", "If no reply by Thursday, call her"). This is what opens under the arrow, so never leave it empty. |
| `context` | For `doThisWeek` only: one line on why now, with date and source |
| `otherGaps` | Every deal with gaps that isn't at risk (up to 40), most important first: `deal`, `amount`, `owner`, `stage`, `gaps` (short tags), `why` (under 12 words), `detail` |
| `onTrack` | `count` and `names` of deals with no gaps |
| `promises` | Promises the seller made on calls or in email in the last 30 days that matter now, plus buyers still waiting on a reply (status "missed", promise "Reply to [what they asked]"): `deal`, `owner`, `when` ("due Oct 6", "promised Sep 9"), `promise` (under 12 words), `status` ("missed", "due", "unconfirmed" or "kept"), `detail` (where you looked). Include promises the person made on teammates' calls, marked "([Name] owes this)". |
| `noDeal` | Buyer conversations in the last 30 days, or booked in the next 14, with no open deal: `who` (company), `note` (under 15 words), `detail` |
| `habits` | 3–5 habits: `habit` (in their words), `done`, `total` (the "N of M"), `source` (where it comes from: "Best deals", "What slips", "Team rule", "Inferred from wins", "Baseline"), `note` (under 15 words: where it slipped), `reps` (team view: `name`, `done`, `total` per rep), `detail` |
| `topRep` | Team view: one sentence on what the top rep does that the rest don't, with counts for both. Otherwise "". |
| `reps` | Team view only, most value at risk first: `name` (first names, including the leader's own row), `open`, `value`, `atRiskValue`, `atRiskCount`, `gapsCount`, `promisesMissed`, `weakest` (habit and its "N of M"), `detail` (optional coaching note). Empty for a rep's own report. |
| `detail` | What opens under the caret: 2–4 short lines, each a dated fact with its source ("Oct 2 call: promised the integration details by Tuesday", "Checked email, the shared inbox and the CRM: nothing sent since"). Real facts only. |
| `measuredAgainst` | Which standard: "Your sales process files" or "Your CRM stages plus the standard baseline (no sales profile yet)" |
| `howBuilt` | Under 40 words: what you read, any sampling, and what couldn't be checked |

**How the page handles size.** Every list runs full width in two even columns, so nothing ends up long on one side and short on the other. A personal report shows up to 8 at-risk deals and 8 other gaps and names the rest. The page opens with habits, then (team view) "By rep" (one line per rep; opening a rep lists that rep's at-risk deals and other gaps, taken from `atRisk` and `otherGaps` by `owner`), then the at-risk deals (a team view shows only the 6 biggest team-wide), the moves for this week, what's working, other gaps and promises. With more than 6 reps, each habit's per-rep bars sit behind its arrow. So a team of 15 adds 15 short rep lines, not a wall of deals: give every deal in `atRisk` and `otherGaps` and let the page sort it out.

If you can't make an artifact here, save the filled template as an HTML file they can open. Only if the tool can't show or save HTML at all, give the same sections in the same order as short Markdown (headline numbers, habits, by rep, deals at risk, moves this week, what's working, other gaps, promises), with tables for "By rep" and "At risk". If they say they'll paste it into a doc, give that Markdown version too, after the chat reply.

## Step 7: Reply in the chat

Next to the report, keep the chat short:

```
$[X] at risk across [N] deals · $[Y] gone quiet · [N] promises missed this month ([N] couldn't confirm)

Do this week:
1. [Action] on [deal], [why now]
2. [Action] on [deal], [why now]
3. [Action] on [deal], [why now]

Weakest habit: [habit], [N] of [M].
[Sources line: what was checked and what couldn't be, e.g. "Checked CRM, email, your shared inbox, calls and calendar. Chat isn't connected, so 2 promises are 'couldn't confirm'."]
```

In a team view, add one line per rep (at-risk $ and weakest habit) after the moves. If the pipeline is genuinely clean, say so in a line: habits are where a healthy pipeline still has room.

The first time someone runs this report (no earlier one in the conversation or project), add one line: "You'll get this same page every time, in the same order. 'How this report works' at the bottom explains each section."

## Step 8: Close

End with these, in this order, kept short:

1. **One concrete offer on the top gap**, acceptable with "yes": "Want me to draft the follow-up to [Company] with the pricing you promised?" (for leaders: "Want me to draft a note to [Rep] about [Deal]?"). Draft only; nothing is sent or changed without their approval. Use `arrows-voice.md` for anything drafted as them.
2. **Weekly schedule**, only if you can create scheduled tasks and this report isn't already scheduled: "Want this every Monday at 8am?" Explain a scheduled task in a few words the first time (a saved request Claude runs on its own at the time you pick).

## Special cases

**No CRM and no CSV.** Say it plainly at the start: "The process gaps report needs your deals: connect your CRM (click your name at bottom left, then Settings, then Connectors; on a work plan your admin may need to add it first) or drop a CSV export of your open deals here (owner, stage, amount, close date, last activity, next step)." Any CRM works. If calls and email are connected, offer one thing you can do now: "Meanwhile, I can check your last 30 days of calls for follow-ups you promised and whether they went out." Don't build a deal list from guesses.

**CSV instead of a CRM.** Read it like a CRM. Missing columns limit which gaps you can check; say which ones in `howBuilt` ("no next-step column, so next steps weren't checked").

**No call recorder.** Skip call-based promises and "call with no CRM update"; use calendar meetings for the CRM-update check if available. Say so in `howBuilt`.

**No email.** Promises can't be confirmed as sent: list them as "couldn't confirm" and count them separately. Quiet days come from CRM, calendar and chat only.

**A source fails partway.** Retry once, then use what you have and label totals as partial: `✗ Email: stopped after 18 threads (connection dropped). Promise checks are partial.`

**Thin data.** Fewer than 5 open deals: the template still works; the lists are just short. No amounts in the CRM: count deals instead of dollars, put 0 in the money fields and say so in `howBuilt`.

**Rep on a team.** Use the leader's team files for the standard and their own how-i-work file for habits. Don't show other reps' deals.

**No profile.** Run on the baseline, say so in `measuredAgainst`, and the shared context's one-line setup suggestion covers the rest.

## Rules

- **Only flag what you verified.** A wrong "you never sent it" when they did kills trust in the whole report. When a source is missing, say "couldn't confirm" rather than "missed".
- **Read only.** Never update the CRM, send, or draft into anyone's mailbox without the person approving the exact change. This report is about finding gaps, not acting on them unasked.
- **Their standard, not a generic one.** Use their stage names, methodology and rules in their words. The point is "you said you do X; here's where it didn't happen."
- **Money and dates, not adjectives.** Every red line has an amount, a date or a count. "Quiet 19 days, $45k, close date Friday" is actionable; "losing momentum" isn't.
- **Statuses, not scores.** At risk, other gaps, on track, with one line of why. Scores hide the reason and invite arguing about the number.
- **Fair to reps.** Leaders may share this. Describe the work ("no recap after 6 of 9 demos"), never the person, and credit the habits reps do well.
- **Nothing saved with buyer details.** If you save anything for next week's comparison, keep it to counts and habits, with no buyer names, companies or exact amounts.

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
