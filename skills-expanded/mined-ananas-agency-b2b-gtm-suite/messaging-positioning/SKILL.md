---
name: messaging-positioning
description: >
  Turning the Ananas-Agency strategy (value propositions, buyer personas, buying
  process) into ready-to-use messaging and outreach assets. This is the capstone skill:
  it converts PSO (Problem · Solution · Outcome) values, DMU roles, objections, and
  buying-journey stages into a positioning statement, a messaging matrix, an
  objection-handling cheat sheet, competitor battlecards, a message house with company
  boilerplates and elevator pitches, and send-ready copy for sales and marketing (per-role
  cold-email sequences, a forwardable email, LinkedIn outreach and ads, discovery questions,
  a full-copy one-pager and landing page, content topics). Use this skill when the user wants
  to: write their positioning, build sales/marketing messaging, turn value propositions into
  copy, create cold emails or LinkedIn outreach, prepare a sales playbook or battlecards,
  write company boilerplate or an elevator pitch, or produce a one-pager or landing page. Not for creating the underlying strategy — build the
  value propositions (Skill 1), personas (Skill 3), and buying process (Skill 5) first.
  Trigger: "messaging", "positioning", "positioning statement", "sales playbook",
  "messaging matrix", "cold email", "outreach copy", "LinkedIn outreach", "one-pager",
  "landing page copy", "objection handling", "how do we say it", "sales copy",
  "battlecard", "boilerplate", "elevator pitch", "message house", "taglines".
---

# Messaging & Positioning Playbook (Ananas-Agency)

## Goal

Convert the strategy the earlier skills produced into assets a user can send and publish: a full activation kit, not outlines. Starting from the value propositions (with IDs), the buyer personas (DMU roles + objections + matched values), the competitor analysis, and the buying process (5 stages), produce four asset groups:

1. **Positioning & story kit** — positioning statement, a **message house** (core message + 3 pillars), 25/50/100-word **boilerplates**, 10s/30s **elevator pitches**, 3-5 taglines.
2. **Per-role outreach** — a cold-email sequence **per key DMU role** (champion + economic buyer, with A/B subject lines), a **forwardable email** for the champion, LinkedIn opener + follow-ups, a call opener.
3. **Sales enablement** — a **battlecard per competitor**, 8-10 **discovery questions**, a messaging matrix, an objection-handling cheat sheet.
4. **Marketing assets** — a **full-copy one-pager**, landing-page **hero variants + section copy**, 3 LinkedIn-ad variants, 5-7 content topics.

This is where the strategy stops sitting in a drawer and becomes communication.

## Why this skill

Every earlier skill answers *what* and *who*. This one answers *how we say it*. Without it, a company finishes the strategy work with nothing to actually send: great value propositions and personas, but no copy in front of a customer. This skill is the bridge from strategy to activation.

## Prerequisites

**Messaging builds on the earlier deliverables:**
1. **List of value propositions (PSO)** with stable IDs (`PV-/SV-/AV-`), the `unique` flag, and the competitor snapshot — *required* (Skill 1).
2. **Buyer Persona(s)** with DMU roles, objections, and matched values — *required* (Skill 3).
3. **Competitor Analysis** — *recommended* (Skill 2); it feeds the battlecards and the "unlike [alternative]" contrast. Without it, build battlecards from the Skill-1 competitor snapshot (shorter, flagged as snapshot-based).
4. **Buying Process** (5 stages) — *recommended* (Skill 5); without it, build the messaging matrix without the stage axis and note that gap.

If the required documents are missing, let the user know:
> "Messaging builds on your value propositions (with IDs) and at least one buyer persona. Without them I can't ground the copy in real values and roles. Which would you like to create first?"

**Prefer validated inputs.** If the user has run Persona Experiments (Skill 4), build on values tagged `Source: validated`, because untested (`hypothesis`) claims make weaker copy. If nothing has been validated yet, proceed but flag that the messaging rests on untested assumptions.

## Key concepts

### The positioning statement
One sentence that anchors everything else:

> **For [ICP / segment] who [priority problem], we [category] that [core value / outcome], unlike [alternative], because [reason to believe].**

- **[core value / outcome]** leads with the **strongest value overall** (by Score), cited by ID. It does **not** have to be `unique`. Prefer a `validated` one.
- **[alternative]** comes straight from the **competitor snapshot** in Skill 1, or, if the user ran the **Competitor Analysis** skill, from its positioning read (which names the real alternative per value). Name the real alternative (a competitor, the status quo, or "doing it in-house / in Excel"). Pair the contrast with a `unique` value where you have one, so the "unlike" actually lands.

### The messaging matrix
A grid that says *what to say to whom, when*: **DMU role × value ID × buying stage**. Each cell is one line, the single most relevant point for that role at that stage. Not every cell needs filling; prioritise the decisive ones (economic buyer at Supplier selection, end user at Requirements building, etc.).

### The objection-handling cheat sheet
For each persona objection (raw + expanded form from Skill 3), a short rebuttal grounded in a specific value ID. Reuse the persona's own wording of the objection so reps recognise it in the wild.

### The message house
The reusable hierarchy: one **core message** (the roof) held up by **3 pillars**, each pillar a theme clustering 2-3 values (by ID) with at least one Outcome number as proof. Boilerplates, pitches, ads, and page copy all derive from it: build it once, reuse everywhere.

### Competitor battlecards
One card per competitor, built from the Competitor Analysis: their pitch (stated fairly), when **they** win, when **we** win (by value ID), 2-3 "kill questions" the buyer should ask them, landmines we must never claim, and the proof point that settles it. Honest by construction — a card that only praises us is useless mid-deal.

### Send-ready copy, per role
Every outreach and marketing asset is **finished copy the user can paste**, not an outline, and outreach is written **per DMU role**: the champion and the economic buyer get different sequences, because they have different pains, values, and language.

## Conversation flow

Guide the user step by step. Each step is a separate turn, so don't jump ahead.

> **How to run this session — read before you start.** Treat this as a **discovery conversation**: a guided working session with the user, closer to a strategy call or workshop than a questionnaire. The entire value of the result comes from what you draw out of them, so slow down and dig in. A rushed exchange that jumps straight to a draft produces a generic, forgettable set of messaging assets; a proper working session produces copy grounded in the user's real business.
> - **Open first, then move to choices — keep it balanced.** Make the *first* question on a topic open (*"before I ask specifics, tell me in your own words how you see this"*), then **stop asking everything open**: once you see the shape, switch to targeted questions and fill only genuine gaps with more open follow-ups.
> - **Prefer selectable answers to keep the pace.** Whenever a question has a small, knowable set of likely answers, present them as a **pickable list** (the user selects, and can add their own) rather than another open prompt — an all-open interview drags; balance one open opener with quick pickable questions. Always still push for the specifics behind whatever they pick.
> - **Pace and depth.** Work through the topics as a genuine back-and-forth, asking **2–3 questions at a time** so you never overwhelm the user. Across the whole session expect to ask roughly **10–15 questions** before you have enough to build, because this skill now produces the largest deliverable in the suite. If you catch yourself moving to a draft after only two or three answers, you have stopped too early. There is almost always more to uncover, and the difference shows in the output.
> - **Cover the checklist before you build.** Do not move on to writing the outreach assets (Step 6) or to producing the deliverable until every item in **Required inputs** below has genuinely been captured, or the user has explicitly chosen to skip it, or told you they don't know. A missing item is a gap to close in conversation, not a blank for you to quietly fill on their behalf.
> - **Push past the first answer.** People give you the surface answer first: "we're faster", "better service", "good quality". Treat every vague or general reply as an invitation to go one level deeper: ask for a concrete example, a number, a percentage, an amount in €, a timeframe, or the specific situation that prompted it. Stay on a single point, following up, until the answer is specific enough to actually act on. This is where a good session earns its value.
> - **Ask before you assume.** Never invent a fact the user could have given you. Your default is always to ask them first. If the user genuinely cannot answer, or would rather not, you may fill the gap yourself, but you must label it clearly as **[Assumption]** in the output and flag it so they can confirm or correct it later.

### Required inputs — capture before drafting
Check each off (or mark "skip") before Step 6 (writing the outreach assets):
- [ ] Value list received — IDs, `unique` flags, competitor snapshot
- [ ] Buyer persona(s) received — DMU roles, objections, matched value IDs
- [ ] Competitor Analysis received, or its absence noted (battlecards then use the snapshot)
- [ ] Buying process (5 stages) received, or its absence explicitly noted
- [ ] The two priority outreach roles chosen with the user (default: champion + economic buyer)
- [ ] Tone check — 2-3 answers on voice (formal vs direct, jargon comfort, taboo phrases)
- [ ] Positioning statement drafted and validated with the user
- [ ] Message house pillars agreed (3 themes) before any copy is written

### Step 1: Collect the inputs

Ask the user to paste their value-proposition list (with IDs), their buyer persona(s), and, if they have them, the competitor analysis and the buying-process description. Confirm you can see: value IDs + `unique` flags + the competitor snapshot; DMU roles + objections + matched value IDs; and the 5 buying stages. If a required piece is missing, stop and point them to the right skill.

### Step 2: Draft the positioning statement

Fill the positioning formula using the ICP, the top-priority problem, the strongest `unique` value (by ID), and the `[alternative]` from the competitor snapshot. Draft 2–3 variants and let the user pick and refine. Validate: "Does this sound like *you*, and is the 'unlike' honest?"

### Step 3: Build the message house & story kit

From the agreed positioning, build the **message house** (core message + 3 pillars, each clustering 2-3 value IDs with a number). Validate the pillar themes with the user, then derive the **boilerplates (25/50/100 words)**, the **10s and 30s elevator pitches**, and **3-5 tagline options**. Patterns: [references/rules-messaging.md](references/rules-messaging.md).

### Step 4: Build the messaging matrix

For each DMU role, and (if available) each buying stage, write the single most relevant line, citing the value ID it draws on. Prioritise the decisive cells; don't force a line into every box. Present the matrix and ask the user which rows feel off.

### Step 5: Objections, discovery questions & battlecards

- **Objection cheat sheet:** for each persona objection, a concise rebuttal anchored to a value ID, keeping the raw phrasing. Validate: "Are these the objections you actually hear?"
- **Discovery questions:** 8-10 first-call questions derived from persona problems/triggers, each noting the value ID it opens.
- **Battlecards:** one per competitor from the Competitor Analysis (their pitch · they win when · we win when, by ID · kill questions · landmines · proof). If only the Skill-1 snapshot exists, build shorter cards and flag them snapshot-based. Templates: [references/rules-messaging.md](references/rules-messaging.md).

### Step 6: Write the outreach assets — per role

Draft **finished copy**: a 3-4-touch cold-email sequence for **each of the two priority roles** (different pains, values, and language; A/B subject lines where useful), the **forwardable email** the champion can send their boss, LinkedIn opener + 2 follow-ups, and the call opener. Every asset cites its value IDs and maps to a buying stage.

### Step 7: Write the marketing assets

Full copy, not outlines: the **one-pager** (paste-ready text), the **landing page** (3 hero-headline variants + subhead + real section copy), **3 LinkedIn-ad variants** (headline + body + CTA, different angles), and **5-7 content topics** (title + stage served + value ID). Templates: [references/rules-messaging.md](references/rules-messaging.md).

### Step 8: Deliver the playbook as files

Generate TWO files (`.md` and a styled, self-contained `.html`). The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format). For the format, see [references/rules-messaging.md](references/rules-messaging.md), section "Output file format". Save both files and share them with the user for download.

## Finalize the Strategy Dossier

This suite runs as one continuous session, and this is the last skill in the sequence. Add or refresh the **Messaging & Positioning** section of the running **Strategy Dossier** with the assets you just produced. Then finalize:

1. **Reconcile the Company Brief's open `TBD`s.** Before summarizing, revisit every `TBD` the Company Brief still carries and **backfill the ones the session has since answered** — later skills (Competitor Analysis, Buyer Persona, Buying Process, Persona Experiments) surface many facts the intake left open. Fill each now-known item from what was actually captured in the session, leave anything still genuinely unknown as `TBD`, and **refresh both the `company-brief` deliverable and the dossier's Company Brief section** so the finished pack doesn't ship stale `TBD`s. Don't invent facts — only fill what the session established.
2. **Generate the executive summary** at the top of the dossier: positioning statement, top 3 values by ID, primary persona, validation status (validated vs hypothesis), and the biggest gap.
3. **Deliver the Sales Strategy Dossier** — the dossier rendered as **one merged entry document**, `_[company]-strategy-dossier` (`.md` + `.html`, e.g. `_meridian-strategy-dossier.html`; the leading underscore sorts it to the top of the folder). It opens with the executive summary from step 1, then carries **every dossier section with real substance** (the full value table with scores/statuses, all DMU roles, the complete hypothesis results, all five stages, every gap with its priority, the positioning and key message lines), each section heading carrying an "Open full document →" **button** (`class="openbtn"`, right-aligned) to that skill's `.html`. In the header, use the **audited company's logo** if their website yields one (embed as a data URI; otherwise the company name as text; never invent a logo), and phrase the attribution "**by Ananas Agency**". There is no separate summary page: this file is both the start page and the complete document; it opens the walk (no Previous; its Next leads into `company-brief.html`). See [dossier-format.md](../dossier-format.md), section "The Sales Strategy Dossier". The executive summary is unnumbered; section numbering starts at Company Brief = 1.
4. **Generate the What's-Next page** (`whats-next.md` + `.html`) — the closing page between this playbook and the Dossier: the first-two-weeks checklist, the 30–60 and 60–90 day moves, the keep-the-documents-alive triggers table, a **navigation grid with a button to every document in the pack**, and the agency CTA block (the only CTA in the pack). It is the final page of the walk (no Next button). Build it from the run's own data: the Priority-1 gap, the outreach sequences, the battlecards. See [dossier-format.md](../dossier-format.md), section "The What's-Next page".
5. **Regenerate every deliverable's `.html` for consistency.** The per-skill files were generated as the session progressed, so before bundling, regenerate each `.html` with the finished cross-link graph (every reference to another deliverable linked, every value ID tooltipped and linked to `value-propositions.html`), the **Next** buttons wired in sequence order, and any statuses that changed during the session (e.g. `hypothesis` → `validated`) brought up to date. This final pass is what makes the pack navigate as one consistent set.
6. **Bundle everything into one ZIP** `[company]-sales-strategy.zip` — a flat archive holding the Sales Strategy Dossier and every per-skill deliverable (**`.md` and `.html` only, no `.txt`**), using the exact canonical filenames so the Dossier's relative links resolve after unzip. Build it with code execution; if that's unavailable, list the files and tell the user to place them in one folder. Offer the ZIP as the **primary download** and tell the user to open `_[company]-strategy-dossier.html` first. If the sequence was only run partially, bundle what exists and note what's missing. See [dossier-format.md](../dossier-format.md), section "Deliverables bundle".
7. **Close the suite — then stop.** Present the ZIP with a short, clear wrap-up: what the pack contains, that every skill's section is now consolidated in the Sales Strategy Dossier, and that the user should open `_[company]-strategy-dossier.html` first. **This is the fixed end of the suite.** Do **not** offer to build — or start building — anything outside the defined deliverables (no extra decks, campaigns, CRM setups, ad accounts, or bonus documents). The finale runs the same complete way every time: steps 1–6, then this clean close. If the user wants something more, let them ask; otherwise the run is complete.

Full format and section order: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **No strategy, no messaging.** Require the value list (with IDs) and at least one persona. Don't invent values or personas here. Send the user to Skills 1 and 3.
2. **Every asset cites value IDs — never bare.** Copy must trace back to specific values, so the messaging stays grounded and updatable. Whenever you show an ID to the user in the conversation, pair it with a short label, e.g. `PV-03 (one-order logistics)` — never a bare code.
3. **The "unlike" must be honest.** Pull `[alternative]` from the competitor snapshot; never claim a differentiator the snapshot doesn't support.
4. **Prefer validated values.** Lead with `Source: validated` values; flag when copy rests on untested (`hypothesis`) claims.
5. **Match message to role and stage.** A line for the economic buyer at Supplier selection is not the line for the end user at Requirements building.
6. **Reuse the persona's own words.** Objections and pains should sound the way the customer actually says them.
7. **Keep it send-ready.** Outreach copy should be usable with light edits: specific, concise, one clear CTA per asset.
8. **Finished copy, never outlines.** The one-pager, landing page, and every email ship as complete text the user can paste. If an asset would come out as a skeleton, ask the missing questions instead.
9. **Battlecards stay honest.** "They win when" is mandatory on every card, and every "we win" claim must trace to the differentiation table. Never arm a rep with a claim the evidence doesn't support.
10. **Per-role, not one-size.** The champion and the economic buyer get different sequences; never send the CFO the operator's email.
11. **A discovery conversation, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you build, push every vague answer toward a specific, and label any gap you fill yourself **[Assumption]**.
12. **Ship one bundle.** Deliver the whole pack as a single ZIP with the `_[company]-strategy-dossier.html` file sorted on top. The Dossier's links are relative, so every file must travel together in one flat folder. Never hand it over on its own.
13. **Fixed end — then stop.** Once the ZIP is delivered, the suite is complete. Give a clean wrap-up and stop; do **not** offer or begin creating anything beyond the defined deliverables. The suite has a definite, consistent ending — don't drift past it.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
