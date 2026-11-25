---
name: arrows-crm-hygiene
description: "CRM guide and hygiene check from Sales Skills by Arrows. Learns how the person's CRM and pipeline really work (the stages, how deals move and where they stall, which fields to update after each call) and saves it as a guide every Sales Skill can use. Then checks the CRM against it: past close dates, no next step, missing required fields, stages that don't match what happened, deals with no contact, duplicates, and fields calls and emails could fill. Gives a score by category, the worst deals (by rep for leaders), and fixes with evidence, applied only after the person approves. Works with any connected CRM or a CSV export. Use whenever someone says 'Run my Arrows CRM hygiene check', 'clean up my CRM', 'what's missing in our CRM', 'learn how our CRM works', 'update the CRM from my calls', asks which deals have bad data, or wants to update a deal in plain language. For deals going quiet or at risk, use the pipeline review, deal nudge or gaps report instead."
---

Learns how the person's CRM and pipeline really work, saves that as a guide, and keeps the CRM matching it. Works with whatever CRM is connected, or a CSV export.

| You get | What's in it |
|---|---|
| `arrows-crm-guide.md` | Built on the first run and saved to the project: the stages and how deals really move between them, where they stall, which fields to update after each call or milestone, what each stage needs, and which fields go unused. Every Sales Skill can read it, so follow-ups and deal updates touch the right fields |
| Hygiene score | Every run: a score for each category below, with counts, and one overall score |
| Worst deals | The deals with the most problems (and, for sales leaders, each rep's score and most common gap) |
| Updates I can make | A ready-to-apply list in small sets, each named for what it fixes. Every update shows its evidence ("Competitor: [Competitor], mentioned on the [date] call") |

| Category | What fails |
|---|---|
| Close dates | Open deals with no close date, or one in the past |
| Next steps | Open deals with no next step and no upcoming task, meeting or activity |
| Required fields | Fields the guide requires (for every deal, or by stage) that are empty, usually amount and source plus what each stage adds; and recently lost deals with no loss reason |
| Stage vs. activity | The stage says something happened that the record, calls and emails don't show ("Proposal" with no proposal sent) |
| Contacts | Deals with no contact associated |
| Duplicates | Companies or contacts that are the same one entered twice |
| Fill from calls and email | Fields that are empty or out of date where a call or email has the answer: a competitor named, a new stakeholder, an amount or timeline the buyer gave |

The person replies at most twice before seeing results: once on the first run to confirm the guide, then once per set of updates they want made. Nothing in the CRM changes until they approve the exact changes.

## Step 1: Find the guide

Look in the project for `arrows-crm-guide.md` (an older copy may be called `arrows-crm-standards.md`; use it the same way), and read the profile files (especially `## Pipeline stages` and `## Discovery and qualification` in `arrows-sales-process.md`, `## Elements` and `## By stage` in `arrows-methodology.md` if present (the CRM field each methodology element lives in, and which stage needs it), and `## Every rep, every deal` in `arrows-how-we-work.md` if present).

- **Guide found:** use it and go to Step 3. Don't re-confirm it. If the CRM has changed since (a field or stage it names no longer exists, a new pipeline), say so in one line at the top of the report and offer "Refresh my CRM guide."
- **No guide (first run):** go to Step 2. Setup leaves CRM depth to this skill, so this is expected. If this chat shows the guide was built before but it isn't in the project, rebuild it and remind them in one line to save it, so they aren't asked to confirm it every week.

**Rep or leader.** Use `## About me` in `arrows-how-i-work.md`. Without it, match the person's email to a CRM owner: owns most open deals → rep; others own most and they own few → leader; a real share of both → both. A leader's scope is their team's deals (from team or role data, or the owners of deals they've been involved in over the last 90 days), never the whole company unless that's all you can tell; then label it "company-wide." The `scope` input, if given, wins.

## Step 2: Learn how the CRM and pipeline work (first run only)

Open with one line: "First run, so I'm learning how your CRM and pipeline actually work. This takes a few minutes, then one quick check with you."

### Read the CRM

Reading budget: up to 200 deals (open, plus closed in the last 6 months), filtered queries and totals rather than record-by-record reads, and call summaries and emails only to see what happens around stage moves.

- **Pipelines and stages:** every deal pipeline in use and its stages, in order. Skip pipelines with no deals created in the last 12 months, and any the profile calls retired.
- **How deals move:** for each stage, typical time in stage (from stage-entry dates or stage history if the CRM keeps them; otherwise created-to-closed time, and say so), how many deals move on vs. close lost or go quiet, and what usually happens just before a deal moves (a demo with more people, pricing sent, a pilot agreed), from activity, calls and email. Where open deals pile up and sit longest is where deals stall; name the stage and the usual reason.
- **When fields get filled:** on the same sample, the share of deals with each field filled, overall and by stage. A field filled on almost every deal from a certain stage on, but rarely before, is updated at that stage. A field filled on fewer than 1 in 20 deals is ignored in practice. Note which fields change after calls (next step, close date, amount) and how long after.
- **Deal fields:** the list of deal properties (name, type, options), and the CRM's own required fields per stage, if the connector exposes them.
- **The process:** stage exit criteria and methodology from the profile. A methodology field (for example a champion or decision-process field) that the profile says matters but is rarely filled is a gap to flag, not a field to ignore.
- **Leaders:** the non-negotiables in `## Every rep, every deal` become required fields or checks. Note where reps differ (one rep fills amount at Discovery, the rest at Pilot), since that shapes the guide.

### Draft the guide

Draft from what you read, not from a generic list. Start from the usual baseline (amount, close date, at least one contact, lead source and a next step: a next-step field, an open task or a scheduled meeting), then follow the data: if amount is filled on nearly every later-stage deal but rarely in the first stage, require it from the stage where it becomes standard, and say so. Drop or rename anything the CRM doesn't use. Include what a closed-lost deal needs (usually a loss reason) if the CRM has the field.

Then confirm in one message. Lead with what they probably didn't know about their own pipeline:

```
Here's how your pipeline actually works, and what I'll keep the CRM matching.

How deals move: [Stage] → [Stage] → [Stage]. Deals spend about [N] weeks in [Stage]; [N] of [N] move on after [what triggers it]. Most stall at [Stage], usually because [reason].
After a call, update: [field], [field]. At [milestone]: [field].
Every open deal needs: [field], [field], [field].
By stage:
• [Stage]: [field]. To be here, [what must have happened].
• [Stage]: [field], [field]. To be here, [evidence].
Fields nobody uses (I'll ignore them): [field], [field].

[At most one specific question, e.g. "[Field] is filled on 3 of 41 deals but your sales process says it matters at [Stage]. Require it from [Stage] on, or ignore it?"]

Reply "looks right," or correct anything in a line.
```

Name real fields and stages as they appear in the CRM. Real numbers, with counts; mark anything inferred. Skip the question if the data answered everything. If the CRM's own required-field rules already exist, show them as-is and only add what's missing.

### Save the guide

After their reply, write `arrows-crm-guide.md` with these `##` headings in this order (other skills look sections up by heading):

- First line: `CRM guide built with Sales Skills by Arrows (arrows.to) for [Name], [rep / leader / both], on [date].`
- `## Where deals live`: the CRM, the pipelines it covers and their stages in order, who's in scope (the person, or their team by role)
- `## How deals move`: each stage, typical time in it, what usually triggers the move to the next one, how many move on; then where deals stall and why. Ranges and counts, no deal names
- `## What to update, when`: after a first call, after each later call, at each milestone (demo, proposal or pilot, close): which fields to update and what goes in them. Other skills use this after calls and for plain-language deal updates
- `## Required on every deal`: field names as they appear in the CRM, and what counts as filled
- `## Required by stage`: each stage, the fields it adds
- `## Stage evidence`: each stage, what must have happened for a deal to be there, and where to see it (a meeting, a sent proposal, a signed order form)
- `## Fields we ignore`: fields that exist but go unused, so checks don't flag them
- `## Fill from calls and email`: which fields to suggest from calls and email, and the CRM field each one goes in. Where a field has a fixed list of options (competitor, stage, lead source, loss reason), list the exact option names the CRM accepts, so any skill updating it picks a valid value. If no field exists for something (a competitor, say), say so
- `## Hygiene rules`: thresholds and rules for the checks (how many days past a close date counts as stale, what counts as a next step, how duplicates match), plus anything the person added

Keep it general and lasting: field names, stage names, timings, rules. No deal, buyer, company or amount details (amounts as ranges only); this file describes how the CRM and pipeline work, not what's in them today, and leaders pass it around their team.

Give the save steps once, in the same message as the first report (Step 4), so the person only has to act once:

```
Your CRM guide is ready (arrows-crm-guide.md). Save it so every Sales Skill knows how your CRM works:
1. Download the file above.
2. Open your deals project in Claude (left sidebar, Projects, then the project; if you don't have one yet, click New project and name it "My Deals". A project is a workspace that keeps files for every chat inside it).
3. On the project page, click + (or Add content) next to Files and upload the file.
```

If you can't create a downloadable file, give it as a copyable block titled `arrows-crm-guide.md` and tell them to add it as text content with that title. Outside Claude, give the block and tell them to save it wherever their tool keeps attached files. Leaders: add one line that reps can add the same file to their own project so everyone works the CRM the same way.

Then go straight on to Step 3 in the same turn; don't make them ask again.

## Step 3: Check the deals

**Reading budget.** Stay inside this so the check finishes in one chat, and say when you sampled ("checked 200 of about 640 open deals, most recently active first"):

- **Deals:** open deals in scope, up to 200, with the guide's fields, owner, stage, last activity date, and associated contacts and company. Use filtered queries and totals where the CRM allows ("open deals with close date before today") rather than reading records one by one.
- **Activity:** open tasks and upcoming meetings for those deals (CRM tasks and calendar both count as a next step).
- **Calls:** summaries from the last 30 days for deals in scope (often 20 come back at once); full transcripts for at most 3, chosen where a summary hints at a competitor, a new person or a number. Note calls and meetings with companies that have no open deal (they may be deals nobody created), and with deals already closed lost (they may be coming back).
- **Email:** up to 25 recent threads with contacts on deals in scope, looking for new people on the thread, proposals or order forms sent, and dates or amounts the buyer gave. If buyer email lives in another connected tool (a shared inbox, for example), read it there; if the main email account has little buyer mail, say so, since it lowers what calls and email can fill.
- **Duplicates:** companies and contacts on deals in scope, plus those created in the last 90 days, up to 500 records. Use the same set every run so scores compare week to week, and report the count checked.

A single deal (`deal_company` given, or the person named one): check just that deal, reading every call and email on it.

### The checks

Run every category from the table at the top, using the guide's fields and thresholds. If two parts of the guide disagree, the more specific one wins (a stage rule over an every-deal rule), and mention the conflict in one line so they can fix the guide.

- **Close dates:** fails if an open deal has no close date where the guide requires one, or one before today (allowing any grace period the guide sets). Don't invent a new date; suggest one only when a call or email gives it ("they said end of next month on the [date] call"), otherwise mark it "needs you."
- **Next steps:** fails if there's no next-step field, no open task due, and no meeting on the calendar with anyone at the buyer. Many teams don't use tasks; a next-step field or a booked meeting is enough. A booked meeting passes even if the next-step text is out of date; suggest updating the text as a small fix. A next step whose dates have all passed, with nothing booked, fails.
- **Required fields:** each required field (every deal, plus the deal's current stage and earlier stages) that's empty is a gap. Close dates, next steps and having at least one contact are scored in their own categories, so don't count them again here; a stage rule asking for more contacts ("2+ contacts") counts here. Only fields in `## Fields we ignore` are skipped, plus any stage rule the deal has already moved past (a "next step names the kickoff" rule once the kickoff has happened). Also check deals closed lost in the last 30 days against what the guide says a closed deal needs (usually a loss reason); a missing loss reason is how a team loses the record of why it loses.
- **Stage vs. activity:** fails when the `## Stage evidence` for the deal's stage isn't in the record, calls or email (Proposal with no proposal or pricing sent; Negotiation with no reply from the buyer in 30 days). Say what's missing, and suggest the stage the evidence supports. A deal that's behind its evidence (a pilot agreed on a call while the deal still sits in an earlier stage) passes this check, but suggest moving it forward with the evidence. Never suggest moving a deal forward on a guess. Moving a deal back to an earlier stage is the owner's call, so it goes under Decisions, not into a set of updates. A deal with no calls, email or meetings in the window you read is judged on its CRM record alone; if that isn't enough to tell, leave it out of this category's count and say how many you left out.
- **Contacts:** fails with no contact associated. If a call or email shows who the buyer is, suggest associating them.
- **Duplicates:** two companies with the same website domain, or near-identical names ("[Company] Inc" and "[Company]"); two contacts with the same email, or the same name at the same company. If `## Hygiene rules` sets a match rule, only pairs that meet it count in the score; pairs that match only on name can be listed, labeled "name match only", but don't count. Report pairs; for each, which record has more deals and activity (the one to keep).
- **Fill from calls and email:** for each field in `## Fill from calls and email`, look for the answer: a competitor the buyer named, a new stakeholder (a name and title on an email thread or call who isn't a contact on the deal), budget, amount, seats, timeline or decision process the buyer stated. Each suggestion needs a source and date. If a field already has a value and a call says something newer, suggest the update and show both. That includes loss reasons: a deal closed lost as "timing" when the call says they chose to build it themselves. Loss-reason fixes go in the calls-and-email set and count toward this category. Amounts come only from what the buyer said or a quote or proposal that was sent, not from internal estimates.

Also suggest follow-up tasks where a call or email set a next step that isn't in the CRM ("send security questionnaire by Friday," from the [date] call): task, due date, owner, evidence.

Before suggesting a new contact anywhere, search the CRM for that person (by email, then name and company). If they already exist, suggest linking the existing record to the deal; creating a second copy is the very mess this check cleans up.

### Scoring

For each category: deals that pass ÷ deals checked, as a whole number out of 100, with the counts ("Close dates 71 · 29 of 41 pass"). Exceptions:

- **Required fields:** filled ÷ required, counting each field on each deal ("Required fields 78 · 112 of 144 filled"), so one strict stage rule doesn't sink the whole score. Name the field missing most often.
- **Duplicates:** company and contact records with no duplicate ÷ records checked.
- **Fill from calls and email:** deals with nothing left to fill ÷ deals with calls or email in the last 30 days. A low score here means the fixes below have a lot to add.

Overall: the average of the category scores. A category you couldn't check (no call recorder, for example) shows "not checked" and stays out of the average; say why. **By rep (leaders):** the same categories on each rep's deals (leave out Duplicates), averaged, plus the gap that shows up most on their deals. Rep scores use their open deals plus loss reasons on their recent losses. Open deals with no owner get their own row; a closed-lost deal with no owner goes under Decisions instead.

If a score is low mostly because of one rule in the guide ("2+ contacts from [Stage]" fails [N] deals), say so in one line in the category's detail, with what the score would be without it. Don't ask about it in the chat (every chat message carries one ask); they can say "Refresh my CRM guide" to change it. The person may have set it on purpose.

## Step 4: Report

The report is a visual page built from the fixed template in `report-template.md` (in the same folder as this file). Copy the template exactly and replace only the `DATA` object; don't restyle it, add or drop sections, or write your own HTML. Use it on every run, scheduled runs included, so the page looks the same every week and the person always knows where to look.

Show it as an artifact. If artifacts aren't available, save the filled template as `crm-hygiene.html` and give the file. Only if the tool can't show or save HTML at all, give the same sections in the same order as short Markdown.

**DATA fields**

| Field | What goes in it | Limit |
|---|---|---|
| `name` | The person's first name | |
| `headline` | One sentence for a sales leader on what this means for the pipeline, e.g. "[N] of [N] deals are missing something needed to forecast them; most are close dates and next steps." | 25 words |
| `company` | Team reports only: the company name (from the person's company, profile files, CRM or email domain). The title becomes "[Company] CRM hygiene report"; if unknown, leave it blank and the title says "Sales team". Personal reports are titled with `name` | 4 words |
| `view` | "My deals", or "Team view · [N] reps" for leaders | 6 words |
| `crm` | CRM and pipeline(s) checked, e.g. "[CRM] · [pipeline]" | 8 words |
| `updated` | Date and time of this run | |
| `numbers` | `checked` deals, overall `score`, `clean` (deals that pass every check), `needFixing` (checked minus clean), `fixesReady` (updates ready across all sets) | numbers only |
| `categories` | One per category, in the order of the table at the top: `name`, `score` (0–100, or `null` if not checked), `passing` ("29 of 41", "112 of 144 filled"), `note` (the main reason, or why it wasn't checked), optional `detail` (list of short dated facts, or the one rule driving the score and the offer to relax it) | note 12 words |
| `fixes` | Every ready update, highest-value first (the page shows the top 8, or the top 6 team-wide, and groups the rest by rep): `deal` (company name) and `owner` (the bold line), `change` (what changes, in plain words a sales leader would use: "Add [Name] (co-founder) to the deal", "Set the close date to Nov 15", not field names or "link"), `evidence` (why: source and date, short quote), `steps` (always: 2–3 numbered steps, e.g. "Say 'go ahead' in the chat and I'll make this change", "Or in the CRM: open [Deal] and [change]"), optional `context` (one line, why now) | change 12 words, evidence 14 words |
| `worst` | Every deal with 3+ issues, worst first (the page shows the top 8, or 6 team-wide): `deal`, `owner`, `stage`, `issues` (2–4 short tags like "no next step", "close date Aug 25"), optional `detail` | 4 words per tag |
| `reps` | Leaders only, lowest score first: `name`, `deals`, `score`, `gap` (most common gap with a count), optional `detail`. Opening a rep shows their fixes, worst deals and Needs you items, matched by `owner`, so use the same name in every list. Leave empty for reps. Deals with no owner get their own row | gap 12 words |
| `needsYou` | Decisions nobody can infer, grouped by owner where it helps: `deal` (one or several), `owner`, `ask` | ask 14 words |
| `duplicates` | `records` (what's duplicated), `rule` ("same domain", "same email", "name match only"), `keep` (which to keep) | 12 words |
| `alsoNoticed` | At most 3 lines: talked to but not in the CRM, lost but still talking, open deals in a retired pipeline | 20 words each |
| `howBuilt` | What was read this run, any sampling or caps, anything missing | 40 words |

Use company names, not CRM deal names with suffixes. Every number in `DATA` traces to what you read. Never write "you" or "your" in `DATA`; use the person's first name, reps' first names (the leader's own row too), or "the team". Only quoted text may keep "you". Reports get forwarded to managers and teammates; the chat reply can still speak to the person directly.

**In the chat**, alongside the report, keep it short, because approval happens in the chat:

```
Sales Skills by Arrows · CRM hygiene: [score]/100 across [N] deals. [One line on the biggest problem.]

[N] updates from your calls and email
• [Deal] · [Field]: [old] → [new]. Evidence: [source], [date]
• [Deal] · Link [Name, Title] (already in the CRM). Evidence: [source], [date]
• [Deal] · New task: [task], due [date], owner [Rep]. Evidence: [source], [date]

Also ready: [N] next-step and close-date updates, [N] stage moves. [N] decisions need you or the rep (in the report).
```

Group ready updates into sets of at most 10 and name each set for what it does ("updates from your calls and email", "next steps and close dates", "stage moves"); never "batch" or a number, which mean nothing to a sales leader. List only the set you're offering first, one line per change (one person per line when linking contacts), leading with the deal and rep; name the rest, and every update you name must appear in a later set. Sets hold only changes that are ready to apply; anything that needs a decision goes under Needs you, grouped by owner for leaders. Merges are never in a set; they go under Duplicates to merge, to do in the CRM. A fix without a source isn't a fix, it's a guess, so leave it out or move it to Needs you. If you hit a reading cap (500 company records, for example), say so in `howBuilt`.

On someone's first run, add one line: they'll get the same page every time, and "How this report works" at the bottom explains the scores.

## Step 5: Apply the fixes

Check whether the CRM connector can update records (look for an update or edit tool, not just search and read).

**It can write:** end the report with:

```
I can make these [N] changes in [CRM] for you. Say "go ahead", or tell me what to skip ("go ahead, but skip [Deal]").
```

Apply only the exact changes in the approved set, word for word as shown (no added or reworded text), then re-read each record and confirm in plain words, not record IDs or internal field names: `✓ [Deal] · [what changed]`, or `✗ [Deal] · [what didn't save] ([reason])`. Then offer the next set by name. When there are no sets left (or they stop), end with the Step 6 offer. Approval covers the sets the person approved and nothing else, and only changes they've seen line by line. If they approve a set you only named ("do all of them"), show its exact lines and confirm before applying it. If they approve several at once ("do all of them"), still apply and confirm one set at a time, and stop to check in if anything fails. Don't merge duplicates, delete records or change owners even if asked to apply everything; merges and deletes can't be undone in most CRMs, so give the steps for doing them in the CRM instead.

**It can't write (or no CRM connector):** give the fixes as a copy-paste list grouped by deal, so the person can open each deal once and make every change:

```
[Deal]
  [Field]: [new value]
  Add contact: [Name, Title, email]
  New task: [task], due [date]
```

### Updating a deal in plain language

If the person asks to change a deal in their own words ("move [Deal] to Proposal, they want 40 seats"), use `## What to update, when` and `## Required by stage` in the guide: work out the exact field changes, fill what you can from calls and email, ask only for the fields the new stage requires that you can't find, then show the changes and apply them when they say yes. If the evidence doesn't support the new stage, say so in one line and let them decide.

## Step 6: Wrap up

Make one closing offer they can accept with "yes", once per run: at the end of the last apply message, or at the end of the report message if there's nothing to apply or the CRM can't be updated from here. The report message itself ends with the "I can make these changes" ask, so it never carries two asks.

- **Scheduling:** if Claude can create scheduled tasks and no CRM hygiene check is already scheduled: "Want this check waiting for you every week before your pipeline review?" If the calendar shows a recurring pipeline or forecast review (or, failing that, the team's recurring sales meeting), name it and offer to run an hour or two before it ("Your pipeline review is Mondays at 10. Run this Mondays at 8?"). If yes, schedule it for the time they pick.
- **Otherwise:** the next useful run, for example a weekly pipeline review now that the data is clean, or a deal nudge on the worst offender with no next step.

## Special cases

**No CRM connected:** say so, and ask for a CSV export of open deals with these columns if they have them: deal name, owner, stage, amount, close date, next step, last activity date, lead source, associated contact and company. Most CRMs export from the deals list view. Run every check the CSV supports; Duplicates needs a contacts or companies export too, so mark it "not checked" unless they add one. Fixes are always copy-paste. To connect a CRM instead: click your name (bottom left), then Settings, then Connectors; on a work plan, your Claude admin may need to add it first.

**No profile files:** build the guide from the CRM alone, mark stage evidence as "(inferred from the CRM)", and continue. Suggest setup once at the end, as the shared context says.

**No call recorder or email:** run the CRM-only checks. Show Fill from calls and email as "not checked (no call recorder or email connected)," and do Stage vs. activity from the CRM record alone, saying so.

**A source fails partway:** retry once, then move on: `✗ Calls: stopped after 8 summaries (connection dropped). Using what I read.` Score only what you read and label partial counts as partial.

**Large CRM:** check up to 200 deals, most recently active first; leaders get every rep sampled proportionally. Give totals from filtered counts where the CRM allows, so the score still reflects the whole pipeline when you can.

**Several pipelines:** check each pipeline against its own stages. If one pipeline isn't sales (renewals, partners, support), confirm it in the Step 2 message and leave it out of the guide unless they want it. If a retired pipeline the guide skips still has open deals, say how many in one line; they probably need closing out.

**A field is empty on purpose:** if the person says a field doesn't apply ("we don't track source for renewals"), add that to the guide and tell them to replace the saved file.

## Rules

- **Read only until approved.** Never create, update, merge or delete anything in the CRM, and never send anything, without the person approving the exact change. A wrong write to the CRM is worse than a missing field, because everyone downstream trusts it.
- **Every fix has evidence.** A source and date for anything that came from a call or email, a quote where it's short. The person should be able to approve a set without opening anything.
- **Don't guess dates, amounts or stages.** If nothing says when a deal will close or what it's worth, ask; a made-up close date is just a new stale close date.
- **Check against their guide, not a generic checklist.** Flagging a field their team never uses wastes their time and makes the score meaningless.
- **No buyer details in saved files.** The guide holds fields, stages, timings and rules only. The report can name deals because it stays in the chat.
- **Honest scores.** Show counts with every score, say what you sampled, and keep unchecked categories out of the average.

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
