---
name: competitor-analysis
description: >
  Full competitor analysis for a B2B company in the Ananas-Agency model. Profiles the main
  competitors, builds a differentiation table (your value propositions × competitors), reads where
  the company wins and where it's exposed, and produces the evidence that sets each value's
  `unique` flag and feeds the Messaging skill's "unlike [alternative]" contrast. Runs after the
  Value Proposition list (it needs the values as the rows of the table). Use this skill when the
  user wants to: analyze competitors, map the competitive landscape, understand differentiation,
  see how they compare to rivals, or decide what makes them genuinely unique. Trigger:
  "competitor analysis", "competitive landscape", "competitors", "competition", "differentiation",
  "how do we compare", "who do we compete with", "why do we win", "why do we lose", "unlike",
  "positioning vs competitors".
---

# Competitor Analysis (Ananas-Agency)

## Goal

Using the value propositions (and the Company Brief if available), profile the company's main competitors, build a **differentiation table** (your values × competitors), read **where the company wins and where it's exposed**, and produce the evidence that (a) sets each value's `unique` flag and (b) feeds the Messaging skill's "unlike [alternative]" contrast.

## Why a competitor analysis

Uniqueness claims and positioning have to rest on evidence, not gut feeling. The Value Proposition skill captures a quick competitor *snapshot* to set a first-pass `unique` flag; this skill turns that snapshot into a real competitive picture, so the company knows which values actually stand apart, where rivals beat them, and what honest "unlike [alternative]" it can claim in its messaging.

## Prerequisite: the value proposition list

**A competitor analysis needs a finished list of value propositions (PSO (Problem · Solution · Outcome)) with IDs**: those values are the rows of the differentiation table and what the `unique` flags attach to.

If the user doesn't have a PSO list, let them know:
> "A competitor analysis compares your value propositions against each competitor, so I need your finished PSO (Problem · Solution · Outcome) list (with IDs) first. Would you like to build that list first?"

If the user completed a **Company Brief**, it may already hold a seed list of 3–5 competitors: start from that rather than re-asking.

## What the analysis produces

1. **Competitor set** — the 3–5 most relevant competitors, each classified: **direct** (same offering), **indirect** (a different way to solve the same problem), or **status-quo / in-house** ("doing nothing", Excel, doing it themselves).
2. **Per-competitor profile** — what they offer, how they position themselves, their main strengths, and their main weaknesses.
3. **Differentiation table** — your values (by ID) × competitors, each cell: **yes** (they credibly claim it) / **partial** / **no** / **unsure**.
4. **Positioning read** — where the company **wins** (values no competitor credibly claims) and where it's **exposed** (problems a competitor covers better, or values everyone claims).
5. **Unique-flag evidence** — which values are genuinely `unique` (no competitor claims them), written back to the value list.
6. **"Unlike [alternative]" inputs** — the real alternatives named, ready for the Messaging skill's positioning statement.

## Conversation flow

> **How to run this session — read before you start.** Treat this as a **discovery conversation**: a guided working session with the user, closer to a strategy call or workshop than a questionnaire. The entire value of the result comes from what you draw out of them (and what you can research), so slow down and dig in. A rushed exchange that jumps straight to a table produces a generic, forgettable analysis; a proper working session produces one grounded in the user's real market.
> - **Open first, then move to choices — keep it balanced.** Make the *first* question on a topic open (*"before I ask specifics, tell me in your own words how you see this"*), then **stop asking everything open**: once you see the shape, switch to targeted questions and fill only genuine gaps with more open follow-ups.
> - **Prefer selectable answers to keep the pace.** Whenever a question has a small, knowable set of likely answers, present them as a **pickable list** (the user selects, and can add their own) rather than another open prompt — an all-open interview drags; balance one open opener with quick pickable questions. Always still push for the specifics behind whatever they pick.
> - **Pace and depth.** Work through the topics as a genuine back-and-forth, asking **2–3 questions at a time** so you never overwhelm the user. Across the whole session expect to ask roughly **8–12 questions** before you have enough to build. Where you have web access, research competitors directly instead of making the user recite everything. If you catch yourself building the table after only two or three answers, you have stopped too early.
> - **Cover the checklist before you build.** Do not move on to the positioning read (Step 5) or to producing the deliverable until every item in **Required inputs** below has genuinely been captured, or the user has explicitly chosen to skip it, or told you they don't know. A missing item is a gap to close in conversation or research, not a blank for you to quietly fill on their behalf.
> - **Push past the first answer.** People give you the surface answer first: "they're cheaper", "we're better". Treat every vague or general reply as an invitation to go one level deeper: ask for the specific offering, the concrete strength, the named weakness, the exact claim on their website. Stay on a single point until the answer is specific enough to actually act on.
> - **Ask before you assume.** Never invent a fact you could get from the user or from research. Your default is to ask or check first. If a competitor detail genuinely can't be verified, mark the cell **unsure** rather than guessing, and label any gap you fill yourself **[Assumption]** in the output.

### Required inputs — capture before drafting
Check each off (or mark "skip") before Step 5 (positioning read) and delivery:
- [ ] Value proposition list received, IDs intact (the table rows)
- [ ] Company Brief / competitor seed reviewed if available
- [ ] 3–5 competitors named as specific companies (not a category) and classified — direct / indirect / status-quo / in-house
- [ ] Each competitor profiled — offering, positioning, main strengths, main weaknesses
- [ ] Differentiation table filled — every value × every competitor (yes / partial / no / unsure)
- [ ] Positioning read done — where we win, where we're exposed
- [ ] Unique-flag evidence settled and written back to the value list

### Step 1: Collect the inputs

Ask the user for the finished PSO (Problem · Solution · Outcome) list (with IDs). If they don't have one, stop (see the prerequisite). If they have a **Company Brief**, ask them to paste it and reuse its competitor seed and offering context instead of re-asking.

### Step 2: Identify the competitor set

Settle on the **3–5 most relevant competitors — as specific, named companies, not a category**. Ask the user directly: *"Who exactly do you compete with? Name the actual companies — the ones you lose deals to, and the ones a buyer would shortlist alongside you."* Start from the Company Brief's seed list if there is one.

**If the user answers with a type or category** ("other distributors", "the big agencies", "in-house teams"), push once for the real names before moving on — the whole analysis is built on named competitors, and a generic "competitor type" produces a generic, useless table. Only fall back to a representative named example if the user genuinely can't name any.

Classify each: **direct**, **indirect**, or **status-quo / in-house**. Don't skip the status quo: for many B2B purchases "doing nothing" or "keeping it in Excel" is the real competitor. Keep it to the ones that matter; more than 5 dilutes the analysis.

### Step 3: Profile each competitor

For each **named** competitor, **research that specific company directly in the background first** where you have web access — read their website, positioning, and materials — and only then confirm and fill the gaps with the user. Research the actual company, not the category. Capture:
- **Offering** — what they actually sell.
- **Positioning** — how they present themselves; who they target.
- **Strengths** — where they are genuinely strong (be honest).
- **Weaknesses** — where they fall short for this segment.

**Real, sourced data only — never hallucinate.** Every claim about a competitor must come from a **verifiable source**: the competitor's own website, their materials, or another trusted public source (reviews, analyst pages, the user's first-hand knowledge). **Do not invent or guess plausible-sounding facts.** If you have no web access or can't verify a detail, say so and either ask the user or mark it **unknown / unsure** — don't fill it in. Prefer to **note the source** for each non-obvious claim (e.g. "per their pricing page"), so the user can check it. A confident but unsourced profile is worse than an honestly incomplete one.

Probing questions and patterns — see: [references/rules-competitor-analysis.md](references/rules-competitor-analysis.md).

### Step 4: Build the differentiation table

Lay the company's values (rows, by ID) against the competitors (columns). For each cell, mark whether that competitor **credibly claims** the value: **yes / partial / no / unsure**. A value is a candidate for `unique` only when **no** competitor claims it. If you can't verify, mark **unsure**. Never overclaim. Table pattern — see: [references/rules-competitor-analysis.md](references/rules-competitor-analysis.md).

### Step 5: Read the positioning

From the table, read:
- **Where we win** — the values no competitor credibly claims (the real differentiators).
- **Where we're exposed** — problems a competitor covers better, and values that *everyone* claims (table stakes, not differentiators).

State both honestly. The exposed side is what the persona objections and the messaging have to work around.

### Step 6: Set the unique-flag evidence and write it back

Settle each value's `unique` status from the table: `unique` **only** when no competitor credibly claims it (unsure ≠ unique). Then **write the flags back** to the Value Proposition deliverable (`value-propositions.md` and the dossier's Value Propositions section): this analysis is the evidence base the `unique` flags should rest on, so the value list must reflect it. Also list the named **alternatives** (the real "unlike [alternative]" for each strong value) for the Messaging skill.

### Step 7: Deliver the analysis as files

Generate TWO files (`.md` and a styled, self-contained `.html`) and share them with the user. The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format). Format — see: [references/rules-competitor-analysis.md](references/rules-competitor-analysis.md), section "Output file format".

Save both files and share them with the user for download.

## Add to the Strategy Dossier

This suite runs as one continuous session. **Deliver only your own two files now** — the **Strategy Dossier** is an **internal running document**, not delivered until the end, so don't create or hand over a dossier file mid-session. Record the **Competitor Analysis** section into that internal dossier (its slot is right after Value Propositions) with the competitor set, the differentiation table, and the positioning read. Also **refresh the internal Value Propositions section** with the `unique` flags this analysis settled, so the value list reflects the evidence. Full format: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **No value list, no analysis.** The values are the rows of the differentiation table. Don't run this without them.
2. **Evidence, not gut — real sourced data only.** Every competitor claim must come from a verifiable source (their website/materials, a trusted public source, or the user), never invented. If a detail can't be verified, mark it **unsure/unknown** — don't guess. Every `unique` flag must trace to the table; note the source for non-obvious claims.
3. **Include the status quo.** "Doing nothing / in-house / Excel" is a real competitor. Name it where it applies.
4. **Be honest about weakness.** Name where competitors beat you; a flattering analysis is a useless one. The exposed side feeds objection handling and messaging.
5. **Write the flags back.** The value list is the source of truth: apply the settled `unique` flags there, not only in this file.
6. **A snapshot seeds this; this doesn't replace itself with a snapshot.** This is the deep analysis the Value Proposition snapshot only gestured at. Go past a single grid to real profiles and a positioning read.
7. **A discovery conversation, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you build, push every vague answer toward a specific, and label any gap you fill yourself **[Assumption]**.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
