---
name: value-proposition
description: >
  Creating a list of value propositions for a B2B company in the Ananas-Agency model (PSO (Problem · Solution · Outcome)).
  Use this skill when the user wants to: create value propositions for their company,
  build a PSO (Problem · Solution · Outcome) list, describe competitive advantages in a sales
  format, prepare material for sales/marketing communication, diagnose
  or improve existing descriptions of the company's value. Not for finding gaps or missing
  values in an existing list — that's the Missing Value Propositions skill (Skill 6); this
  skill creates the list from scratch. Trigger: "value proposition",
  "list of values", "PSO", "company advantages", "what sets us apart", "why should a customer buy
  from us", "product value", "service value", "added value".
---

# Creating Value Propositions (Ananas-Agency — PSO (Problem · Solution · Outcome))

## Goal

Guide the user through building a complete, prioritized list of value propositions for a B2B company in the PSO (Problem · Solution · Outcome) format, organized into 3 categories. Aim for a minimum of 20 values, with 30+ as the ideal target.

## Key definitions

### PSO (Problem · Solution · Outcome) format

Every value proposition is a triple. PSO (Problem · Solution · Outcome) is Ananas-Agency's operational take on the **Value Proposition Canvas** and **Jobs-to-Be-Done**: P = the customer's job/pain, S = the pain reliever / gain creator, O = the quantified gain. PSO (Problem · Solution · Outcome) remains the primary term throughout this skill.

- **P (Problem/Challenge)** — a specific, painful customer problem. The sharper the pain, the stronger the value.
- **S (Solution)** — what the company does to solve that problem. Concrete and clear, never vague.
- **O (Outcome)** — a measurable business result for the customer. Use a number whenever possible; fall back to a qualitative description only when no number genuinely exists.

### Three value categories — decisive definitions

1. **Product value** — features of the product or service itself that the customer "buys on the invoice". For services: scope, methodology, tooling. For physical products: material, technical parameter, durability, performance, construction, product certification.
2. **Service value** — how the company delivers and supports the product/service, i.e. the customer experience surrounding the purchase (response time, ordering method, onboarding, implementation, after-sales service, SLA, dedicated account manager, reporting, contract and payment terms, logistics, warehousing, delivery, complaints).
3. **Added value** — what the company gives the customer BEYOND the product and service: things the customer doesn't pay for directly, yet that still create an edge (education, content, community, partnerships, location, brand/social proof, industry know-how that goes beyond the scope of the service/product, technical advisory).

**Categorization test:** "Does the customer pay for it directly?" (-> Product value), "Is it about HOW we deliver?" (-> Service value), "Is it a bonus that goes beyond the transaction?" (-> Added value).

**Note:** The balance between categories can vary widely from company to company. A company selling a commodity (e.g. steel, screws) may have 2 product values and 15 service values. That's perfectly normal. Don't force an artificial balance.

### Scoring the strength of a value

- **Problem weight**: 1-10 (1 = "nice to have", 10 = "critical pain")
- **Outcome magnitude**: 1-10 (1 = marginal, 10 = transformational)
- **Uniqueness flag**: mark the value *unique* if competitors do NOT have it (shown as a tag, not added to the score). Set this from the **competitor snapshot** (Step 5): evidence, not gut.
- **Score** = Problem weight + Outcome magnitude (max 20)

> **Two scores live in this suite — keep them separate.** This strength score (Problem + Outcome, max 20) ranks the *values you already have*. The Missing Value Propositions skill uses a different **Impact/Effort priority score** (impact on sales × implementation effort, 1-10 each) to prioritise *new values you might build*. One ranks what you have; the other sequences what to add. Don't compare the two numbers directly.

### Value ID

This skill assigns every value a durable ID by category: Product value -> `PV-01, PV-02, …`, Service value -> `SV-01, SV-02, …`, Added value -> `AV-01, AV-02, …` — numbered within each category in descending score order. These IDs are how later skills reference the value.

The ID is a **stable identifier, not a live ranking.** The descending-score order holds at creation, but once a value is re-scored (e.g. after Persona Experiments, Skill 4) its ID stays put, so the numbers may no longer be in score order. When you need the current ranking, **sort by the Score, not by ID.**

## Conversation flow

Guide the user step by step. Each step is a separate turn. Don't jump ahead.

> **How to run this session — read before you start.** Treat this as a **discovery conversation**: a guided working session with the user, closer to a strategy call or workshop than a questionnaire. The entire value of the result comes from what you draw out of them, so slow down and dig in. A rushed exchange that jumps straight to a draft produces a generic, forgettable value list; a proper working session produces one grounded in the user's real business.
> - **Open first, then move to choices — keep it balanced.** Make the *first* question on a topic open (*"before I ask specifics, tell me in your own words how you see this"*), then **stop asking everything open**: once you see the shape, switch to targeted questions and fill only genuine gaps with more open follow-ups.
> - **Prefer selectable answers to keep the pace.** Whenever a question has a small, knowable set of likely answers, present them as a **pickable list** (the user selects, and can add their own) rather than another open prompt — an all-open interview drags; balance one open opener with quick pickable questions. Always still push for the specifics behind whatever they pick.
> - **Pace and depth.** Work through the topics as a genuine back-and-forth, asking **2–3 questions at a time** so you never overwhelm the user. Across the whole session expect to ask roughly **15–25 questions** before you have enough to build. This is the deepest interview in the suite. If you catch yourself moving to a draft after only a handful of answers, you have stopped too early; there is almost always more value to uncover.
> - **Cover the checklist before you build.** Do not move on to building the PSO sentences (Step 4) and scoring until every item in **Required inputs** below has genuinely been captured, or the user has explicitly chosen to skip it, or told you they don't know. A missing item is a gap to close in conversation, not a blank for you to quietly fill on their behalf.
> - **Push past the first answer.** People give you the surface answer first: "we're faster", "better service", "good quality". Treat every vague or general reply as an invitation to go one level deeper: ask for a concrete example, a number, a percentage, an amount in €, a timeframe, or the specific situation that prompted it. Stay on a single point, following up, until the answer is specific enough to actually act on. This is where a good session earns its value.
> - **Ask before you assume.** Never invent a fact the user could have given you. Your default is always to ask them first. If the user genuinely cannot answer, or would rather not, you may fill the gap yourself, but you must label it clearly as **[Assumption]** in the output and flag it so they can confirm or correct it later.

### Required inputs — capture before drafting
Check each off (or mark "skip") before you score the list (Step 6). The competitor snapshot is the last item, so it must be run (or explicitly skipped) before scoring:
- [ ] Company & offering understood — industry; product / service / software / mix; typical customer; commodity vs differentiated
- [ ] Main competitors named (3–5)
- [ ] Raw values collected across every area — **minimum 20, aim for 30+** (hunt with the gaps checklist before you stop)
- [ ] Each Outcome quantified — a number, %, € or timeframe, or the user explicitly confirmed no number exists
- [ ] Competitor snapshot built — values × competitors grid, so `unique` flags rest on evidence

### Step 1: Get to know the company

If the user has already completed a **Company Brief** (from the `company-brief` skill), ask them to paste it and skip the questions it already answers. Otherwise, ask the questions below.

Ask:
- What does the company do? (industry, product/service, customer segment)
- Does the company sell a physical product, a service, software, or a mix?
- Who is the typical customer? (role, company size)
- Who are the main competitors?
- Does the product/service stand apart from the competition, or is it more of a commodity (much the same everywhere)?

If the user provides a website URL, analyze it and pull out preliminary information.

Use the answers to tailor your follow-up questions. For commodity companies, focus on service and added values. For companies with a unique product, start with product values.

### Step 2: Extract raw values

Ask probing questions, no more than 2-3 per turn. Don't overwhelm the user.

Probing questions — see: [references/rules-pso.md](references/rules-pso.md)

After each answer:
1. Pull out specific values.
2. Dig deeper and ask for numbers: "You said X — how much exactly? What % increase/savings does that give the customer?"
3. Keep a running count of the values collected and report it back: "We have 14 values, we still need at least 16 more."

**Collection completion threshold: 20 values (minimum), 30+ is the ideal target.** Below 20, actively hunt for missing areas. Use the gaps checklist (see: [references/rules-pso.md](references/rules-pso.md), section "Checklist of areas to review"). When you reach 20, **stop and ask outright**. Don't silently proceed past 20: "We've hit 20 values — a solid base. Want to keep going to 30+ (recommended: the more we have, the more material to work with across sales and marketing), or lock the list here?"

### Step 3: Deduplication

Before building the PSO (Problem · Solution · Outcome), review the raw values and merge those that say the same thing from a different angle. Two values are duplicates when:
- They solve the same customer problem through the SAME mechanism
- They differ only in wording, not in substance
- One is a subset of the other (e.g. "flexible scope" is part of a "subscription model")

It's fine for the same company resource to appear in two values, but ONLY if it solves two DIFFERENT customer problems. For example, "40 consultants" can be a product value (industry fit) and a service value (project continuity), because the underlying customer problems differ.

After deduplication, report back: "I merged X values that were repeating. Y unique ones remain."

### Step 4: Build the PSO (Problem · Solution · Outcome) and enforce numbers in the outcomes

For each value, write a complete PSO (Problem · Solution · Outcome) sentence. Rules and patterns — see: [references/rules-pso.md](references/rules-pso.md)

**Enforcing numbers in outcomes:** For every O (Outcome) without a number, ask the user: "What's the measurable outcome? E.g. by what % is the time reduced, how much the customer saves (EUR), how much does the risk drop?" If the user doesn't know the number, propose an estimate or a range ("20-30% faster"). Accept a qualitative outcome ONLY when the user explicitly confirms that no number exists.

### Step 5: Competitor snapshot (sets the unique flag)

Before scoring, capture a lightweight competitor snapshot so the `unique` flag rests on evidence, not gut. If the user completed the **Company Brief**, it may already hold a competitor snapshot (a 3–5 competitor list): **start from that and extend it here** rather than rebuilding it; otherwise reuse the competitors the user named in Step 1.

1. Take the **3–5 main competitors** (from the Company Brief's snapshot if it has one).
2. For each value, ask whether each competitor also credibly claims it: "Do any of these competitors offer the same thing?" Build a small grid: values (rows) × competitors (columns), each cell yes / no / unsure.
3. A value is **unique** only when **no competitor** credibly claims it. If unsure, leave it un-flagged rather than over-claiming.

Keep it quick: this is a snapshot, not a full competitive analysis. If the user genuinely doesn't know a competitor's offering, mark the cell "unsure" and don't flag the value unique. The snapshot is also the source of the "unlike [alternative]" contrast used later by the Messaging skill.

For a fuller picture (per-competitor profiles, a differentiation table, and a win/exposed positioning read), run the **Competitor Analysis** skill after this one; it takes this snapshot deeper and refines these `unique` flags on real evidence.

### Step 6: Score, categorize and sort

**Before you score:** the competitor snapshot (Step 5) must exist, or the user must have explicitly opted out of it. Never assign a `unique` flag without it: if the snapshot wasn't run, no value may be marked `unique` (a missing snapshot means "not evidenced", not "everything is unique").

1. Assign each value to a category using the categorization test (see definitions above).
2. Assign a score (Problem weight + Outcome magnitude, max 20), then set the `unique` flag from the competitor snapshot (Step 5).
3. Sort in descending order within each category.
4. Assign each value its category ID (PV-/SV-/AV-) in descending-score order. These IDs are how later skills (persona, buying process, gap analysis) reference the value.
5. Tag every value `Source: hypothesis`. It stays a hypothesis until a Persona Experiment (Skill 4) tests it; the experiment then flips tested values to `validated`. IDs stay fixed once assigned. Never re-number on a later re-score.

### Step 7: Deliver the final list as files

**One last expansion offer before you finalize:** tell the user the current count and offer to add more: "We have [N] values. Want to add any more before I finalize, or shall I deliver?" Generate the files only once they're happy with the list.

Generate TWO files (`.md` and a styled, self-contained `.html`) and share them with the user. The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format). Format — see: [references/rules-pso.md](references/rules-pso.md), section "Output file format".

Save both files and share them with the user for download.

## Add to the Strategy Dossier

This suite runs as one continuous session. **Deliver only your own two files now** — the **Strategy Dossier** is an **internal running document**, not delivered until the end (by the final skill), so don't create or hand over a dossier file mid-session. Record the **Value Propositions** section into that internal dossier with the list you just built (IDs, `unique` flags, `Source` tags, and the competitor snapshot). Full format: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **Minimum 20 values, ideal 30+.** Below 20, actively hunt for missing areas from the checklist. At 20, explicitly ask whether to push to 30+ or lock the list, and offer once more before finalizing. Never stop at 20 silently.
2. **Non-obviousness above all.** Reject generic, empty values.
3. **Always a complete PSO (Problem · Solution · Outcome).** Never leave a value without a P (Problem) and an O (Outcome).
4. **Numerical effect as the default.** Ask for numbers with EVERY outcome. Accept a description ONLY after the user explicitly confirms that no number exists.
5. **A specific value.** Not "a large warehouse" but "4500 SKUs" or "the largest on the market".
6. **The "So what?" test** — after S (Solution), if the customer would ask "So what?", the O (Outcome) is missing.
7. **Deduplication before building the PSO (Problem · Solution · Outcome).** Merge values that say the same thing. Allow a duplicated resource only when it addresses different customer problems.
8. **Uniqueness is evidence-based.** Only flag a value `unique` when the competitor snapshot (Step 5) shows no competitor claims it. When in doubt, don't flag it.
9. **A discovery conversation, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you build, push every vague answer toward a specific, and label any gap you fill yourself **[Assumption]**.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
