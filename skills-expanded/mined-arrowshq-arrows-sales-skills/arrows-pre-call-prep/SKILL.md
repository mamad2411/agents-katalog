---
name: arrows-pre-call-prep
description: "Arrows pre-call prep. A 60-second brief for one upcoming call: who you're meeting, what they want to solve, what happened last time and what's still owed, what you still don't know for your qualification method (like the economic buyer), what to push for and what could go sideways. Works for first calls (booking form, intro email) and later ones (every prior call, email and chat). Finds the call on your calendar by itself. For one call, not your whole day. Use whenever someone says 'Run the Arrows meeting prep for [company]', 'prep me for my call with [company]', 'pre-call prep on [company]', 'what do I need to know before my next call', asks to get ready for a specific sales meeting, or wants prep ready automatically before their meetings. The brief is for the person only; not for writing an agenda or anything to send to the buyer."
---

A brief for one upcoming call that the person can scan in 60 seconds before joining. It's for them only, never the buyer.

| Section | What's in it |
|---|---|
| What this call is for | The agenda and what the buyer wants from it |
| Who's on the call | Each attendee's role on the deal, with flags (new, skeptic, champion) |
| What they want to solve | Their pain, goals and numbers, in their words |
| Last time and what's owed | What happened before, and commitments still open on either side |
| Still unknown | Gaps against the person's qualification method |
| What to push for | 2–4 outcomes for this call |
| Watch out for | Real risks, each with how to handle it |
| Their words | Phrases the buyer uses, to echo on the call |

Every section is optional. A first call with no history might be three sections long; that's right.

## Step 1: Find the call

Look at the calendar for upcoming meetings with the company they named over the next 14 days, and match each one to a CRM deal.

- **One match:** go straight on. Name the call in the brief's header so a wrong pick is obvious. Don't stop to confirm; an extra round trip right before a call is the moment people give up.
- **Several meetings, same deal:** prep the next one and mention the later ones in a line at the end.
- **Meetings for different deals or groups at the same company** (for example two business units): ask which one, in one line per option with date, time, attendees and deal. This is the only time to ask.
- **No company named:** prep their next sales call: an external meeting with a buyer, prospect or customer (a CRM deal or contact, or a booking from a prospect), today or the next working day. Skip vendors, partners, agencies, recruiting and personal meetings (a partner or customer who booked through a sales or demo link counts as a sales call), and name what you skipped in one line at the end ("Skipped the 8:00 agency kickoff: not a sales call.").
- **The company named is a vendor or partner** (they sell to the person, or there's no buyer relationship): say so under the header and give a short meeting brief instead: who's attending, what's open on both sides, and what to get out of the call. Leave out the deal and qualification sections.
- **No match:** say so in two lines with the likely reason (different name on the invite, a calendar you can't see, not booked yet), and ask for the buyer's name or the meeting details.

## Step 2: Gather

Read broadly, then keep only what helps on this call. Reading budget:

- **CRM:** the deal (stage, amount, close date, next step, source, owner, custom fields that are filled in) and each attendee's contact record; notes and the last 15 activities; any form submission that created the contact.
- **Call recordings:** summaries of every prior call with this company, however old; full transcripts of the most recent one or two. Prep is cumulative: the first calls often hold their original goal, their definition of success and early doubts, which matter on every later call.
- **Email:** threads with each attendee in the last 90 days, read to the end, including replies from teammates the person was copied on and emails the deal owner logged in the CRM. Before calling anything owed, check that nobody on the team already answered it. For a first call, read the thread that booked it closely: buyers often state their goal or timeline there and it's forgotten by call time.
- **Chat, if connected:** direct messages with attendees and internal threads about the deal.
- **Contracts, if connected:** pending documents and signature status.
- **Web:** a quick look at attendees who have no CRM or call history (role, how long they've been there). Company news only if it connects to something the buyer said matters.

Then work out the call number (the Nth call with this buyer, counting real meetings) and whether there's any buyer-side content yet: a booking form, an intro reply, SDR handoff notes or prior calls. A first call with a filled-in form isn't a blank slate.

## Step 3: Check it against the profile

This is what turns a recap into prep. Use the profile files (see the shared context):

- **Qualification gaps.** Take the method in `arrows-methodology.md` if the project has it (`## By stage` for what this stage needs, `## How to check a deal` for what counts as known, and `## Questions to ask` for the questions to suggest), otherwise in `arrows-sales-process.md` under `## Discovery and qualification` (MEDDIC, SPICED, BANT or their own) and the exit criteria for the deal's current stage under `## Pipeline stages`. For each element, decide from the evidence whether it's known, partly known or unknown. Unknown items that matter at this stage become "Still unknown" ("You still don't know the economic buyer. Only the champion has been on calls."). No profile: use the gaps a standard discovery would check (budget, decision maker, timeline, the problem, competition) and say that's what you used.
- **Best-deal moves.** If `arrows-how-i-work.md` lists moves from their best deals under `## What I do on my best deals`, suggest the one that fits this call ("On your best deals you get the decision maker on before the pilot starts.").
- **What slips.** Check this deal for each item under `## What slips` and flag any that apply.
- **Competitors.** If a competitor came up, use `arrows-buyers-and-competitors.md` for how they usually win or lose against it.
- **At risk.** The deal is at risk if there's been no two-way touch in 14+ days, no next step, or a promised next step that didn't happen. Say so in the header if it is.

## Step 4: Write the brief

The brief is a report page with a fixed design. Copy the template in `report-template.md` (in the same folder as this file) exactly and replace only the `DATA` object. Don't restyle it, add or drop sections, or write your own HTML, so the person finds things in the same place before every call, scheduled runs included. An empty list shows a short "nothing here" line, which is right for a first call.

Show it as an artifact. If you can't, save the filled template as `pre-call-[company].html` and share the file. Only if you can't show or save HTML at all, write the same sections in the same order as Markdown (below). On someone's first run, add one chat line: "You'll get the same page before every call; 'How this report works' at the bottom explains each section."

**Filling `DATA`.** Rows are a few words; anything longer goes in `detail` (a list of dated facts with their source). Amounts are plain numbers (24000). Never write "you" or "your" in `DATA`: use the person's first name ("Dana owes this"), reps' first names, or "the team", since the page gets forwarded and "you" means nothing to the next reader. Quoted text (email subjects, call quotes) can keep it; the chat message can still speak to the person directly. Every row that states a fact gets a `source` ("call, Sep 22", "email, Oct 1", "CRM note").

| Field | What goes in it | Limit |
|---|---|---|
| `name`, `company`, `updated` | First name; the buyer's company; when this ran | |
| `when`, `callNumber` | "Mon Oct 5 · 4:00pm · 30 min"; "Call 3" or "First call" | |
| `agenda`, `theyWant` | From the invite or booking email; what the buyer asked to cover (with source) | 20 words each |
| `deal` | `stage`, `amount`, `close`, `owner` (first name). Leave a value empty when you can't source it; never guess a stage. No deal means stage "" | |
| `atRisk` | The at-risk reason, if the deal is at risk; else "" | 12 words |
| `note` | Leader prepping a rep's call: "[Rep]'s deal. Where [Name] helps: ..."; vendor or partner meeting: say so; else "" | 25 words |
| `numbers` | `gaps` (items in `unknown`), `owed` (open commitments in `lastTime`) | numbers |
| `want` | `point`, `quote` (their words), `source`, optional `detail` | 3–5 items; point 8 words |
| `watch` | `risk`, `source`, `handle` (how to handle it), optional `detail` | 3 items |
| `push` | `outcome` (something to leave the call with, bold on the page), `why`, `steps` (required: 2–3 numbered steps on how to get it on the call), optional `context` | 2–4 items; outcome 8 words |
| `people` | `name`, `title`, `flag` ("new", "skeptic", "champion", "decision maker" or ""), `role`, `source`, optional `detail` | role 12 words |
| `lastTime` | `text`, `status` ("done", "open" for a commitment still owed, or ""), `source`, optional `detail` | 4 items; 12 words |
| `unknown` | `item` (an element of their qualification method), `why` (why it matters at this stage, phrased so it turns into a question) | 1–4 items |
| `words` | `phrase` (exact), `source` | 3–5 items |
| `howBuilt` | What was read, anything that failed or isn't connected | 40 words |

Markdown version, only when HTML isn't possible:

```
**Pre-call: [Company]** · [Day] [time] · [length] · call [N]
[Deal name] · [stage] · $[amount] · close [date][ · at risk: reason]

**What this call is for**
- Agenda: [from the invite or booking email]
- They want: [what the buyer asked to cover, with source]

**Who's on the call**
- **[Name], [title]**: [their role on the deal, what they care about]. [Flag]
- **[Name], [title]**: [role]. New to the deal; [LinkedIn link]

**What they want to solve**
- [Pain or goal]: "[their words]" ([source, date])

**Last time and what's owed**
- [What happened or was decided] ([source, date])
- You promised [deliverable] by [date]: [sent / not sent yet]
- They promised [thing]: [done / still open]

**Still unknown**
- [Element of their method]: [what's missing and why it matters at this stage]

**What to push for**
1. [Specific outcome]: [why, and what you need to hear]

**Watch out for**
- [Risk] ([where it came from]) → [how to handle it]

**Their words**
- "[exact phrase]" ([source])
```

Section notes:

- **Sources:** end each bullet under Who's on the call, What they want to solve, Last time and Their words with a short source tag ("(call, Sep 22)", "(email, Oct 1)", "(CRM note)"). The person needs to know what's fact and where to check it.
- **Who's on the call:** flags are New (not on earlier calls), Skeptic (pushed back before; give the quote), Champion (has sold internally; point to the moment) and Decision maker (title plus behavior on calls, not title alone). Only use a flag you can back up, since a wrong "champion" label is worse than none. If you know nothing about someone, say so and suggest asking the host who they are.
- **What they want to solve:** 3–5 bullets, cumulative across every touchpoint, in the buyer's own words where possible.
- **Still unknown:** 1–4 items, most important for this stage first. Phrase each so it turns into a question on the call.
- **What to push for:** things to leave the call with (a date, a name, a number, a yes), not topics ("discuss pricing") or approaches ("reframe around the new product"). If the buyer asked to see something specific, showing it is usually push #1. Tie each to a gap, a stage requirement or something the buyer asked for.
- **Watch out for:** only risks with a real source: a competitor that came up, a promise not kept, a new stakeholder, a slipped close date, a long silence.
- **Their words:** 3–5 phrases from transcripts or emails. Skip if there are no real quotes.

## Step 5: Close

The chat message next to the page stays short, four lines at most: (1) the call and the single most important thing; (2) on a first run only, the first-run line; (3) a missing-source or skipped-meeting note, if any; (4) one offer.

- **If you can create scheduled tasks and none already preps their calls:** "Want this ready before every external call? I can run it each weekday at 7am for that day's calls." If yes, create a weekday task (default 7:00 local) whose prompt is "Run Arrows pre-call prep for each external call on my calendar today", confirm in one line, and don't offer again. If they decline, stop there.
- **Otherwise:** "After the call, say 'Run my Arrows post-call' and I'll draft the follow-up and CRM note from this context."

## Special cases

- **First call, nothing on the buyer side:** header, Who's on the call, What to push for, and Still unknown (which is most of discovery). Say "First call, no prior touchpoints."
- **Leader prepping a rep's call** (the deal owner is someone else on their team): add one line under the header: "[Rep]'s deal. Where [Name] helps: [the gap or decision a leader can unlock, like getting the exec on]." Keep the rest the same.
- **No CRM connected:** work from calendar, email and calls; mark stage and amount as unknown rather than guessing. Mention once at the end that connecting the CRM or pasting the deal record sharpens the gaps.
- **No calendar connected:** ask for the date, time and attendees in one line, or work from the `meeting_date` and notes given.
- **A source fails:** retry once, continue, and say in one line what's missing.

## Rules

- **Every fact traces to a source.** CRM, a call, an email, chat, a contract or the web. If you can't point to it, leave it out. One invented detail is enough to make the person double-check everything.
- **Drop empty sections.** A three-section brief with real content beats an eight-section one with filler.
- **Sixty seconds.** The person reads this right before joining: keep the visible rows to about 450 words and put the rest in `detail`.
- **Facts and prompts, no pep talk.** No "This is a big call!"
- **No emojis.** The template carries the structure; in the Markdown version, bold labels do.
- **Read only.** Don't update the CRM, send or draft anything, or create a scheduled task without the person saying yes.

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
