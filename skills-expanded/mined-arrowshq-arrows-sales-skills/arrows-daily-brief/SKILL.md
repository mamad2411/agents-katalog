---
name: arrows-daily-brief
description: "Arrows daily brief. A short read for the start of the day, built for a phone: what to do first, what changed since yesterday (new replies, stage changes), today's calls with deal context, messages waiting on a reply, deals at risk, and open time. Sales leaders also get a line per rep. Pulls calendar, CRM, call recordings, email and chat, and uses the person's sales profile. Use whenever someone says 'Run my Arrows daily brief', asks what's on today, what they missed overnight, what needs them this morning, or wants a rundown of their day and pipeline."
---

A daily brief for today, short enough to read on a phone before the first call:

| Section | What's in it |
|---|---|
| Do first | The 2–5 things that matter most today, in order |
| Since yesterday | Buyer replies, stage changes, wins, losses, signed contracts |
| Today's calls | Each external call: who, where the deal stands, what's open |
| Replies waiting | Buyers who are waiting on the person |
| At risk | Deals that are going quiet or slipping |
| Team (leaders) | One line per rep: what's at risk, what's closing, what needs the leader |
| Open time | Free blocks of 30+ minutes |

## Step 1: Read the profile

Use the profile files (see the shared context) to decide what matters, not just to describe it:

- `arrows-how-i-work.md`: `## What slips` is the person's own list of things to flag; check today's calls and deals for each one. `## Where my time goes` tells you which prep to do for them. `## My rules` apply to every suggested action.
- `arrows-sales-process.md`: stage names, what has to be true to move on, and the methodology under `## Discovery and qualification`. Use them to judge whether a deal is stuck.
- `arrows-buyers-and-competitors.md`: competitor names, so you recognize them when they come up.
- `arrows-how-we-work.md` or a leader role in `## About me`: turn on the Team section (Step 3).

No profile, or it doesn't say: they lead a team if other people own most deals they're involved in (as a contact, follower or meeting attendee), or their calendar has recurring 1:1s with reps. If so, turn on Team.

No profile: run the brief anyway and use the CRM's stage names.

## Step 2: Gather

Read everything before writing. Stay inside this budget so the brief finishes quickly:

- **Calendar:** every meeting on today. Sort them into sales calls (with a buyer, prospect or customer: a CRM deal or contact, or a booking from a prospect), other external meetings (vendors, partners, agencies, recruiting) and internal ones. Note open blocks of 30+ minutes.
- **Each sales call:** the matching CRM deal (stage, amount, close date, next step), the last 3–5 activities, the most recent call summary, and the latest email or chat thread with the attendees. Look for what was promised and whether it happened. If CRM is thin on a new contact, a quick web search for their role is enough. Deeper research belongs to pre-call prep.
- **Since yesterday:** everything since the start of the previous working day (on Monday, since Friday morning): buyer emails and chat messages received, deal stage changes, deals created, won or lost, contracts signed or viewed. Use CRM activity or stage history where it exists; otherwise compare last-modified dates and say the stage change is inferred.
- **Replies waiting:** buyer or prospect emails and direct messages from the last 7 days where the buyer wrote last and the person hasn't answered. Skip newsletters, automated mail, internal threads, group channels, and replies to a mass email (a webinar or newsletter) unless they ask the person something.
- **Pipeline:** open deals the person owns (for leaders, their team's), up to 150, using filtered queries rather than reading each record. Read notes only on deals that look at risk. If there are more, say how many you read.

**At risk** means any of: no two-way touch (a buyer reply, call or meeting) in 14+ days, no next step on the deal, or a promised next step that didn't happen (a date passed, a deliverable not sent, a meeting that never got booked). Check email, chat and call history before calling a deal quiet: a buyer reply in chat yesterday means it isn't quiet, even if the CRM says otherwise. A passed close date on its own is "slipped", not at risk: mention it in the deal's `why` when the deal is at risk for another reason. A contract unsigned for 7+ days counts as a promised next step that didn't happen. Deals with no activity in 60+ days (often in an old pipeline) go in `closeOut` by name instead of `atRisk`, so the at-risk list stays about deals that can still be saved. A deal created in the last 14 days isn't at risk just for having no next step yet; that's noise on a new deal.

## Step 3: Write the brief

The brief is a report page with a fixed design. Copy the template in `report-template.md` (in the same folder as this file) exactly and replace only the `DATA` object. Don't restyle it, add or drop sections, or write your own HTML: the person should find everything in the same place every morning, scheduled runs included. Empty lists show a short "nothing here" line, which is right on a quiet day.

Show it as an artifact. If you can't, save the filled template as `daily-brief.html` and share the file. Only if you can't show or save HTML at all, write the same sections in the same order as Markdown (below). On someone's first run, add one chat line: "You'll get the same page every morning; 'How this report works' at the bottom explains each section."

**Filling `DATA`.** Rows are a few words; the full story goes in `detail` (a list of dated facts with their source, for example "Sep 30 call: asked for the security doc"). Amounts are plain numbers (24000); leave them out when they're 0 or unknown. Use first names for people, including in `owner`. Never write "you" or "your" in `DATA`: use the person's first name ("Dana owes this"), reps' first names, or "the team", since the page gets forwarded and "you" means nothing to the next reader. Quoted text (email subjects, call quotes) can keep it; the chat message can still speak to the person directly. Use company names, not CRM deal names.

| Field | What goes in it | Limit |
|---|---|---|
| `name`, `company`, `date`, `view`, `updated` | First name; their company (from the profile, CRM or email domain; titles the page when there's a Team section, "Sales team" if unknown); "Tuesday, October 6"; "My day" or "My day + team · 3 reps"; when this ran | |
| `numbers` | `calls` (sales calls today), `replies`, `atRisk` (the full count, even if fewer are listed), `changes` (items in New since yesterday) | numbers |
| `doFirst` | `deal` (the company, shown in bold so the eye finds the account first), `amount`, `owner` (leaders: whose deal), `action` (starts with a verb and names who to contact, "Email Dana to book the security review"), `why`, `steps` (required: 2–3 numbered steps, who, how, by when), optional `context` (date and source) | 2–5 items; action 8 words, why 12 |
| `sinceYesterday` | `kind` ("good": moved forward, won, signed; "bad": lost, slipped; "" for a reply or neutral news), `deal`, optional `amount` and `owner`, `what`, `detail` | 6 items; what 10 words |
| `atRisk` | Every at-risk deal, worst first (up to about 40; the page shows the top 5, or the 6 biggest team-wide for leaders, and groups the rest by rep): `deal`, `amount`, `owner`, `stage`, `quietDays` (number, or null if no touch is logged), `channel` of the last touch, `why` (which at-risk reason), `next` (one action), `detail` | why 12 words |
| `calls` | `time`, `company`, `type`, `people` ("Name (title) · Name (title)"), `deal` ("Stage · $24k · close Nov 16 · last two-way touch 6 days ago"), `open` (what happened last time and what's still open), optional `prep` (one action), `detail` | sales calls only; open 25 words |
| `otherMeetings` | One line for vendor, partner and internal meetings | 15 words |
| `closeOut` | Names of deals with no activity in 60+ days, shown as one line | names only |
| `replies` | `name`, `company`, `channel`, `ask`, `waitingDays` (number), `detail` | 5 items |
| `team` | Leaders only, one per rep, most at risk first: `name` (exactly as in `owner`, since opening a rep lists their at-risk deals), `atRiskCount`, `closingCount` (this week), `ask` (the one thing that needs the leader), optional `detail` | ask 15 words |
| `openTime` | `start`, `end`, `length` for blocks of 30+ minutes | |
| `howBuilt` | What was read, any sampling, anything that failed or isn't connected | 40 words |

Markdown version, only when HTML isn't possible:

```
**Daily brief · [Weekday], [Month] [Day]**
[N] calls · [N] replies waiting · [N] at risk

**Do first**
1. [Specific action] — [why today, one line]
2. [Specific action] — [why today]

**Since yesterday**
- [Company]: [Buyer] replied — [what they said or asked, a few words]
- [Company]: moved [stage] → [stage]
- [Company]: [won / lost / contract signed]

**Today's calls**
**[Time] · [Company]** · [call type]
[Name] ([title]) · [Name] ([title])
[Stage] · $[amount] · close [date] · last two-way touch [N] days ago
[One or two lines: what happened last time and what's still open.]
→ [One action before the call, if there is one]

**Replies waiting**
- [Name], [Company] · [email / chat] · [what they asked] · [N] days

**At risk**
- [Company] · [stage] · $[amount] · [the reason: quiet [N] days / no next step / promised [X] by [date], not done] → [action]

**Team**
- [Rep]: [N] at risk, [N] closing this week. [The one deal or decision that needs the leader.]

**Open time**
[Start]–[End] · [Start]–[End]
```

**Do first** pulls the most important items from every other section, ranked by what's due soonest: something blocking a call today goes first. Each item is concrete ("Send the security doc to [Buyer] before the 2pm call"), not general ("Follow up with [Company]"). Use `## What slips` from the profile to decide what rises to the top. On a clean day write "Nothing urgent. Just show up to your calls."

**Today's calls:** sales calls only, at most five lines each. Mark a first call, or a person new to the deal (with their LinkedIn link, since that's the one time it's worth the space). If a profile methodology gap is glaring for this stage (for example a pilot with no economic buyer named), say it in the "still open" line. Vendor, partner and internal meetings share one line at the end ("Also: 8:00 agency kickoff, 3 internal"), plus one flag only if something is due before it.

**At risk:** list every at-risk deal in `DATA`, worst first; the page shows the top few and summarizes the rest. Every line names the specific reason and one action.

**Team (leaders only):** one line per rep, under 30 words, worst first: counts, then the single deal or decision that most needs the leader (a close this week going quiet, an approval, an exec intro, a call they're on). The full list belongs in the weekly pipeline review, not here. Keep the leader's own deals in the sections above.

**Open time:** list the blocks and stop. Don't plan the time for them.

**Length:** the visible rows should read in a minute (about 400 words, 500 for a leader); everything else goes in `detail`. Stick to the item limits above and group the rest ("+4 stage moves on the team"). In the Markdown version, if they say they're on their phone or in a hurry, keep it under 300 words: Do first and Since yesterday in full, then only what needs action today.

## Step 4: Close

The chat message next to the page stays short, four lines at most: (1) what's most urgent; (2) on a first run only, the first-run line; (3) one offer: the scheduling offer if it applies, otherwise the next skill (with no profile, the setup suggestion); (4) a missing-source note, if any.

1. **One next skill, only if earned:** "Want me to run pre-call prep on the [time] [Company] call?" or "The [Company] call yesterday has no follow-up yet. Want me to run post-call on it?" or "Want me to draft a nudge for [Company]?" Skip it on a clean day.
2. **Scheduling, only if you can create scheduled tasks and none already runs the daily brief:** "Want this waiting for you every weekday at 7am? Say yes, or give me a time." Check the existing scheduled tasks first. If they say yes, create a weekday task (default 7:00 local) whose prompt is "Run my Arrows daily brief", confirm it in one line, and don't offer again. If you can't create scheduled tasks, say nothing about scheduling.

## Special cases

- **No calendar connected:** use the pasted calendar if given; otherwise skip Today's calls and Open time, and add one line at the end: "Connect your calendar (your name at bottom left, then Settings, then Connectors) and I'll include today's calls."
- **No CRM connected:** use pasted deals if given. Otherwise build the call and pipeline view from email, calls and calendar, mark deal stages as inferred, and mention once at the end that connecting the CRM or pasting a CSV export of open deals makes the at-risk list complete.
- **A source fails partway:** retry once, then continue with what you have and say so in one line at the end ("Email didn't load, so Replies waiting may be incomplete").
- **No calls today:** lead with Do first, then Since yesterday and At risk. That's still a useful brief.
- **Weekend or holiday date:** brief the next working day and say so in the header.
- **Leader with no deals of their own:** skip Today's calls if they have no external meetings; Team becomes the main section, right after Since yesterday.

## Rules

- **Only what you verified.** If there's no data for a call, write "No history found", rather than guessing what the call is about. A wrong fact in a daily read teaches the person to stop trusting it.
- **Specific over general.** Quote the commitment and the date ("You said you'd send the case study by Friday. Not sent yet."). Vague flags get skipped.
- **No cheerleading, no padding.** It's a memo, not a pep talk. Suggested actions after → are fine; "Big day!" isn't.
- **Background research only when it changes the call.** Company news, funding or LinkedIn posts go in only if they tie to something in the deal. Competitors only when they came up in a real conversation.
- **No emojis.** The template carries the structure; in the Markdown version, bold labels do.
- **Read only.** Don't update the CRM, send, draft into the inbox or create anything without the person approving it. The scheduling task is created only after they say yes.

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
