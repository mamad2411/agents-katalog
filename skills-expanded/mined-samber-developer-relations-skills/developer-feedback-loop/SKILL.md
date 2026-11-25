---
name: developer-feedback-loop
description: >-
  Designs the loop carrying developer feedback from Discord, Slack, forums, support, GitHub
  issues, sales calls and events to product and back - one record of truth, dedup rules, records
  product acts on, product-owned decisions, public status replies including the no, and loop
  metrics. Use whenever feature requests pile up in the community and product never sees them,
  or someone asks how DevRel should hand feedback to product, close the loop with developers,
  triage feature requests across channels, say no publicly, or show what feedback shipped -
  even if they only say "product ignores what our users ask for". Not surveys, NPS or office
  hours. Do NOT use for the issue queue - use samber/developer-relations-skills@oss-issue-triage;
  not community health - use samber/developer-relations-skills@developer-community-health.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.2"
---

# Developer Feedback Loop

You design how developer feedback travels from wherever developers say it to the people who decide what gets built, and back to the developers who asked.

The usual complaint is "product never sees what the community asks for". The cause is rarely a missing tool. It is three gaps: nobody on the product side agreed to receive and decide, requests arrive as solutions with no evidence, and nobody owns telling the requester what happened. Design around those three, in that order.

The loop makes three promises. Every request is captured once. Every captured request gets a decision. Every requester hears the decision, including when it is no.

Stay out of neighbouring jobs:

- The issue queue itself, labels for bugs, stale policy: samber/developer-relations-skills@oss-issue-triage
- Community health metrics: samber/developer-relations-skills@developer-community-health
- DevRel's company-wide KPIs: samber/developer-relations-skills@devrel-metrics
- Writing the release note a shipped request links to: samber/developer-relations-skills@changelog-writing
- Who the segments are: samber/developer-relations-skills@developer-segmentation
- The high-influence members whose feedback carries furthest: samber/developer-relations-skills@developer-champions
- Running the product tag on Stack Overflow, where bug reports and requests also surface: samber/developer-platform-skills@stackoverflow-playbook

## Interview

Ask one question at a time, multiple-choice where you can, skipping what the user already said. Questions 1-4 gate the design.

**Memory: Store a few info about the current task or project context. When memory lives in a file, use `devrel-context.md`; if a different memory system is in use, rely on that instead. Separate task info in different sections. Remove finished tasks. Add a date to a task; no date for general project context. Some interview responses may differ between 2 tasks.**

1. Is there a named person on the product side who will receive feedback and make decisions on it - yes, someone informally, or nobody yet?
2. How many hours a week can the feedback work get, from whom (DevRel, support, community moderators)?
3. Is there a date this must feed - a planning cycle, a launch, a board review?
4. Do you want to clear today's pile once, or a loop that still runs next year?
5. Where does feedback arrive today, and roughly how many requests a week per channel?
6. Where does product track ideas and planned work, can developers see it, and what are the product areas and customer segments called there?
7. Open-source project, commercial API or dev-tool, or both? Can requests be linked to accounts and revenue?
8. Trace one recent request: where was it asked, who saw it, what happened to it?
9. Who is allowed to say no in public, and is a public roadmap allowed?
10. What does product say decides priority today, and what does leadership expect from feedback work - a report, a number, nothing?

Question 1 sets the order of work:

- **Nobody yet:** do not design intake. Deliver the leak trace and the contract pitch (Steps 1-2) and stop there; an intake pipe feeding nobody produces a better-organized pile.
- **Someone informally:** run Steps 1-2 first, then design intake in parallel while the contract is being agreed. An informal receiver is a contract waiting to be written, not a substitute for one.
- **Yes:** run every step in order.

Answers to 2, 3 and 4 re-rank the menus below. Say which answer moved which option, in one block at the top of the intake spec:

- A near date promotes what acts this cycle - the redirect-to-record capture move, one decision review - and demotes the planning seat.
- "Still runs next year" promotes the seat in product planning and the quarterly report, both slow to pay.
- Both at once: sequence them. The near date governs the first cycle; the slow options start after two review cycles have run.
- A low hour ceiling deletes options instead of demoting them. Divide weekly hours by weekly requests: under about five minutes per request (a planning figure this skill sets, not a benchmark), logging on behalf survives only for paying accounts and blockers, and the weekly digest goes. Above that line, still budget logging on behalf as a line in the hour table, never for every request.

## Step 1 - Trace the leak

Sample 20-30 requests from the last 60-90 days, at least three per channel from question 5, so a low-volume channel such as sales still shows. Take the most recent requests per channel, never the memorable ones, which are the ones that already got attention. For each one, record whether it was captured, reached product, got a decision, and whether the requester was told. Count "captured" as written anywhere durable beyond the original message, and "first human reply" as a reply from staff - community members answering each other is healthy, but it is not the loop. The sheet and how to read it: [./references/loop-metrics.md](./references/loop-metrics.md).

Fix the stage that loses the most requests first. When two stages lose about the same number, fix the one question 1 points at: an informal or missing receiver means the decision stage. Requests lost at capture need capture rules. Requests that reach product and sit undecided need the contract. Requests decided but never answered need the reply step. Read the result back to the user before proposing anything.

## Step 2 - Write the contract with product

Agree the decision rights before building anything. Product decides what gets built and sets planned, not planned and shipped. DevRel captures, merges, writes the evidence, drafts public wording and tells requesters. A DevRel team that ranks the roadmap becomes an unpaid product manager without the authority or the engineering capacity behind the role.

The contract names:

- the product receiver per area, with a backup
- the review cadence and who chairs it
- product's promise: every record on the agenda leaves with a status, and "revisit next cycle" may be used at most twice
- DevRel's promise: records meet the template, duplicates merged, community requesters told within a stated window
- support's and sales' promise: they tell the requesters who came through their channels
- what leaves this loop (Step 3) and who may publish dates (only product, only when committed)
- what happens when product misses a review

Pitch it as an hour per cycle, already deduplicated, with discovery contacts product would otherwise recruit. Template, pitch, agenda and the political failure modes: [./references/product-contract-and-politics.md](./references/product-contract-and-politics.md).

## Step 3 - Choose the record of truth

Pick where canonical records live. Rank by how likely product is to read it, per hour of setup:

- efficiency: product's existing idea or backlog space with a feedback type > a public tracker or discussion space developers can see > a DevRel-owned board bridging to product > a new feedback tool
- effort (least first): product's existing space (one field and a view) > DevRel board (an afternoon) > public tracker (forms, status labels, a moderation habit) > new tool (procurement, migration, a second place product must check)
- value: public tracker (developers subscribe, vote and get notified without DevRel relaying) > product's existing space (decisions land where planning happens) > new tool > DevRel board (product reads it only when reminded)

Efficiency starves the public tracker: highest value, more setup. Promote it to first for an open-source project or any product whose developers already file issues in public - there, a private record splits the conversation in two.

When the product is both - open-source SDKs around a closed service, say - make the public tracker the record developers see, and link each reviewed record one-to-one from an item in product's own space. Requesters check one place; product plans in another; the link keeps them the same record.

When the record of truth is private, two later moves change shape. The redirect capture move points to a public intake form instead of the record. Status replies go to the channel where the requester asked, because they cannot see the record.

Keep account names, revenue and private support text out of any public record; link a private record instead.

Route three kinds of input out of this loop at capture, because each has a faster owner:

- bugs → the issue queue or support
- security reports → the private disclosure channel
- how-to questions → support and docs

Feature requests filed as public issues stay where they are. This loop owns their decision and the reply; the issue-queue process owns their other labels. Exempt every issue linked to a loop record from automatic staleness closing, and write the exemption into the contract: a bot closing an "under review" request reads as a no nobody decided.

## Step 4 - Capture, merge and write the record

Capture moves, ranked by requests correctly captured per DevRel hour:

- efficiency: redirect the requester to the record (a reply with a link) > weekly channel sweep by one owner > log on the requester's behalf > automated aggregation from chat
- effort (least first): redirect (seconds) > weekly sweep (an hour a week) > log on behalf (minutes per request) > aggregation (setup, tuning, a duplicate stream to clean)
- value: log on behalf (full evidence, requester consent captured) > weekly sweep (catches what nobody redirected) > redirect (loses requesters who never click) > aggregation (volume without evidence)

Efficiency starves logging on behalf: the richest records, the most minutes. Promote it for paying accounts and for blockers, where one well-written record moves a review. Aggregation earns a place once the weekly sweep can no longer merge duplicates inside its hour; use it to suggest merges, never to make them.

Write every record problem-first. The title names the problem in the developer's words; the requested fix sits in its own field. Product decides between solutions, so a record that names only one solution asks for a yes/no vote on a design. When a request arrives as a solution, ask the requester one question before logging it: "what were you trying to do when you needed this?"

Count requesters, not mentions:

- A requester is a person who asked or stated a use case. Count each once per record, across channels.
- Reactions and votes are a separate signal, reported beside the requester count.
- Prospects from sales calls get the segment "prospect"; their opportunity reference stays in the private record.
- A friction log or DX audit by the team itself becomes one record per friction point; the advocate counts as a requester, alongside the developers who confirmed it.
- A vote spike traced to one outside link counts as one event, noted in the record, not as many independent requesters.

For a one-off pile (question 4), cluster it into problems and log only the largest clusters before the first review, up to what the review can decide. Mark the rest received with an honest note that they wait for the next cycle.

Keep the label set to three single-valued axes - type, area, status - plus two per-requester fields rolled up into counts: segment and severity. A record shared by free and enterprise developers needs the mix, which one segment label would erase. Record template, a good and bad pair, dedup rules and the weighting worksheet: [./references/feedback-record-and-taxonomy.md](./references/feedback-record-and-taxonomy.md).

## Step 5 - Run the handoff

Handoff formats, ranked by decisions produced per hour of product attention:

- efficiency: a decision review per planning cycle > a DevRel seat in product planning > a quarterly voice-of-developer report > a weekly digest
- effort (least first): weekly digest (well under an hour of writing, no meeting) > quarterly report > decision review (an hour of product time per cycle) > planning seat (political capital, a standing commitment)
- value: planning seat (feedback shapes options before they harden) > decision review (statuses on named records) > quarterly report (trend and credibility) > weekly digest (informs; decides nothing)

Efficiency starves the planning seat: highest value, highest political cost. Ask for it once the decision review has run two cycles and product has seen records ship.

Order the review agenda blockers first, then by distinct requesters, never by date or by who asked loudest. Show segment mix and private account value beside each record rather than folding them into one score: weighing them is the decision product owns. Schedule the review before planning, not after, or its statuses arrive once the cycle is already set. Write the status into each record before the meeting ends. A review that ends with minutes and no status changes did not happen.

## Step 6 - Close the loop, including the no

Publish the status vocabulary: received, under review, needs discovery, planned, not planned, shipped, duplicate. Each status change triggers a reply, posted on the record and in the channel where the requester asked. Tracker notifications reach subscribers only; a developer who asked in chat or support learns nothing unless someone tells them there.

Time the replies by status:

- received: at capture.
- under review: when the agenda is frozen, before the review.
- decided statuses: in one batch in the week after each review, so that load follows the review cadence rather than the inflow.
- revisited records: keep "under review" with the next review date; the second revisit is the last before a decision.

Say no as no. A "not planned" reply carries the reason product approved, the best workaround, and what would change the decision. "On our radar" reads as yes to the asker and as evasion to everyone watching, so the request returns every month.

Two decisions cost the most trust and get their own reply: a "planned" record that becomes "not planned", and a shipped change that solves the problem differently from the fix requesters asked for. Say what changed and why, and name the requested fix that was not built.

Never publish a date product has not published, and treat "next cycle" or a cycle number as a date. A missed date costs more trust than an honest no.

If question 9 allows a public roadmap, start it only after two review cycles have produced statuses: a roadmap built before decisions exist is a list of hopes. Show statuses, and dates only where product committed and published them. Product approves each public reason; the person question 9 names approves publication.

For the roadmap's posture, commitment vocabulary, exclusion gate and sales guardrails, see `samber/developer-platform-skills@public-roadmap-strategy`. Feedback from an API preview or design-partner cohort runs on that program's own cadence, set by `samber/developer-platform-skills@api-beta-program`; only requests outside the feature enter this loop.

Templates per status, the public feedback policy page and privacy rules: [./references/close-the-loop-replies.md](./references/close-the-loop-replies.md).

## Step 7 - Measure the loop

Keep three to five metrics, each with an owner and the action it triggers:

- time to first staff reply on a feature request (bots excluded); community-wide responsiveness belongs to the community health sheet
- capture rate
- decision rate
- closure rate
- shipped-from-feedback, under an attribution rule written before counting

First-response time is the only one with even correlational outcome evidence, from code contributions rather than feature requests: a direction, not a target. Set every target from the team's own leak trace and label it self-set. Capture rate comes from the quarterly re-trace, so it moves four times a year; the others move every cycle. Feedback volume is not a success metric.

Report to leadership in the shape question 10 named. When they asked for a number, shipped-from-feedback is the line; the leak trace before and after is the evidence behind it. Definitions and starting targets: [./references/loop-metrics.md](./references/loop-metrics.md).

## Invocation examples

| The user says | You produce |
|---|---|
| "Feature requests pile up in our Discord and product never sees them" | The interview, then the leak trace before any tool or label |
| "Product ignores what DevRel sends them" | The contract and the decision review; the digest is cut |
| "How do we say no to the community without a backlash?" | Status vocabulary, the not-planned template, the public policy page |
| "Our biggest customer wants X and Discord wants Y" | A record each, requesters by segment beside private account value, for product to decide |
| "Leadership asks what feedback work achieved" | Shipped-from-feedback with its attribution rule, plus the leak-trace before and after |

## Deliverable

Produce these in order, each validated with the user before the next:

1. **Leak trace** - the sheet, a stage table (count, ratio, requests lost) and the stage to fix first.
2. **Product contract** - decision rights, receiver, cadence, promises on both sides, plus the pitch.
3. **Intake spec** - the re-ranking block, record of truth, a routing table (channel, weekly volume, capture move, owner, notes), an hour budget per task against question 2, and out-of-loop routes.
4. **Record template and label set** - in the area names and segments from question 6.
5. **Handoff calendar** - dated events through the next two review cycles and the first re-trace - and the review agenda.
6. **Status vocabulary, a reply template per status and the public feedback policy page.**
7. **Metric sheet** - columns: metric, definition, owner, baseline from the leak trace, self-set target, action if it slips; plus the next re-trace date.

A filled example of deliverables 1, 3 and 5 for a two-person team: [./references/worked-example.md](./references/worked-example.md).

With persistent memory available, store the contract terms, the receiver names, the status vocabulary, the record-of-truth location and the last leak-trace numbers. The next review is a diff against them.

## Failure modes

| Failure | Fix |
|---|---|
| Tool first - a feedback portal bought before anyone agreed to decide | Contract first; the record of truth is wherever product already reads |
| Vote-count priority - the biggest thread wins | Distinct requesters by segment, representation, severity; product weighs |
| Silent "later" - records parked for a year | "Revisit" allowed twice, then not planned with a reason |
| Taxonomy sprawl - forty labels nobody applies the same way | Three single-valued axes plus per-requester segment and severity |
| Promise leak - DevRel tells the community "coming soon" | Relay only statuses product set; no dates |
| Closure only on yes - nobody hears about the no | A reply per status change, the no included |
