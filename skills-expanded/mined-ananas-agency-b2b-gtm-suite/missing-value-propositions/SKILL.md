---
name: missing-value-propositions
description: >
  Analyzing gaps in a B2B company's value propositions against buyer personas in the Ananas-Agency model. The skill compares an existing PSO (Problem · Solution · Outcome) list with the buyer personas and identifies
  missing value propositions that could strengthen sales. Each idea is assessed
  by implementation difficulty and impact on sales, and the result is presented as a priority
  matrix. Use this skill when the user wants to: find gaps in value propositions,
  check whether the values cover the needs of the buyer personas, generate ideas for new values,
  decide what to implement first, create a value priority matrix, identify missing
  competitive advantages. Not for creating value propositions from scratch — that's the Value
  Proposition skill (Skill 1); this skill only finds gaps in an existing list. Trigger:
  "missing values", "gaps in values", "gap analysis",
  "what are we missing", "what values don't we have", "what else can we offer", "priority
  matrix", "what to implement first", "PSO gap analysis", "missing PSO", "new values".
---

# Missing Value Propositions — Gap Analysis (Ananas-Agency)

## Goal

Using the existing list of value propositions (PSO (Problem · Solution · Outcome)) and the buyer personas, identify the gaps: values the company doesn't offer yet but that could solve real customer problems surfaced in the buyer personas. Score each missing value by implementation difficulty and impact on sales, then place it on an Impact/Effort priority matrix so that the cheap, simple, high-impact items come first.

## Prerequisites

**A gap analysis requires TWO completed documents:**
1. **List of value propositions (PSO (Problem · Solution · Outcome))** — without it, you don't know what the company already offers
2. **Buyer Persona (min. 1)** — without it, you don't know what values customers need

If the user is missing one or both, let them know:
> "A gap analysis requires a completed list of value propositions (PSO (Problem · Solution · Outcome)) and a buyer persona. Without them, I can't identify the missing values. Which of these documents would you like to create first?"

Do not generate the analysis without both documents.

If the user has run Persona Experiments (Skill 4), build on the **validated** PSO/persona: values tagged `Source: validated` are tested ground; treat `hypothesis` values with appropriate caution. If no experiments have been run yet, proceed with the hypotheses, but flag that the gap analysis rests on untested inputs.

## How to think about gaps

A gap in the value propositions appears when a buyer persona describes a customer problem or challenge that no value on the PSO (Problem · Solution · Outcome) list addresses, or where an existing value addresses it weakly (vaguely, with no concrete outcome, or not tailored to the role).

Gaps fall into three categories:

1. **Problems without a value** — the persona describes a problem the company has no answer for. This is the most serious gap, because the salesperson has no argument to make.
2. **Roles without a value** — values exist, but they don't speak to the needs of a specific role (e.g. the company has values for the CEO but none for the end user). The salesperson has nothing to bring to the conversation with that person.
3. **Stages without a value** — the values cover, say, the Purchase stage (price, terms) but not the Solution exploration stage (why change at all). The customer stalls and doesn't advance through the buying process.

## Conversation flow

> **How to run this session — read before you start.** Treat this as a **discovery conversation**: a guided working session with the user, closer to a strategy call or workshop than a questionnaire. The entire value of the result comes from what you draw out of them, so slow down and dig in. A rushed exchange that jumps straight to a draft produces a generic, forgettable gap analysis; a proper working session produces one grounded in the user's real business.
> - **Open first, then move to choices — keep it balanced.** Make the *first* question on a topic open (*"before I ask specifics, tell me in your own words how you see this"*), then **stop asking everything open**: once you see the shape, switch to targeted questions and fill only genuine gaps with more open follow-ups.
> - **Prefer selectable answers to keep the pace.** Whenever a question has a small, knowable set of likely answers, present them as a **pickable list** (the user selects, and can add their own) rather than another open prompt — an all-open interview drags; balance one open opener with quick pickable questions. Always still push for the specifics behind whatever they pick.
> - **Pace and depth.** Work through the topics as a genuine back-and-forth, asking **2–3 questions at a time** so you never overwhelm the user. Across the whole session expect to ask roughly **6–10 questions** before you have enough to build. If you catch yourself moving to a draft after only two or three answers, you have stopped too early. There is almost always more to uncover, and the difference shows in the output.
> - **Cover the checklist before you build.** Do not move on to scoring the gaps (Step 4) and building the matrix or to producing the deliverable until every item in **Required inputs** below has genuinely been captured, or the user has explicitly chosen to skip it, or told you they don't know. A missing item is a gap to close in conversation, not a blank for you to quietly fill on their behalf.
> - **Push past the first answer.** People give you the surface answer first: "we're faster", "better service", "good quality". Treat every vague or general reply as an invitation to go one level deeper: ask for a concrete example, a number, a percentage, an amount in €, a timeframe, or the specific situation that prompted it. Stay on a single point, following up, until the answer is specific enough to actually act on. This is where a good session earns its value.
> - **Ask before you assume.** Never invent a fact the user could have given you. Your default is always to ask them first. If the user genuinely cannot answer, or would rather not, you may fill the gap yourself, but you must label it clearly as **[Assumption]** in the output and flag it so they can confirm or correct it later.

### Required inputs — capture before drafting
Check each off (or mark "skip") before Step 4 (scoring) and the matrix:
- [ ] PSO (Problem · Solution · Outcome) list + Buyer Persona(s) received
- [ ] Coverage mapped per persona — every problem, challenge and objection checked against a value ID
- [ ] Gaps swept exhaustively (every persona/role/problem/challenge/objection/stage checked; aim 8–12+ candidates), then 2–3 PSO ideas per gap generated and vetted with the user for realism
- [ ] Impact + effort scores proposed and validated with the user

### Step 1: Collect the input documents

Ask the user for the PSO (Problem · Solution · Outcome) list and the buyer persona. If either is missing, stop the process (see Prerequisites).

If the user has more than one buyer persona, analyze all of them but report the gaps per persona.

### Step 2: Map value coverage per persona

For each buyer persona, work systematically through:
- Each **person involved in the purchase** and their problems and challenges
- Each **problem**, checking whether a PSO (Problem · Solution · Outcome) value addresses it
- Each **challenge**, checking the same way
- Each **objection**, checking whether a value defuses it

When a problem IS covered, cite the covering value by its stable ID **paired with a short label** (e.g. `PV-03 (one-order logistics)`), never a bare code, and not by title alone.

Build a coverage table (see [references/rules-missing-pso.md](references/rules-missing-pso.md), section "Coverage table").

Show the user: "Here's how your current values cover the problems raised in the buyer personas. Green = covered, red = gap."

### Step 3: Generate ideas for the missing values

Aim for a **thorough, generous set of gaps** — a gap analysis earns its value by surfacing the ones the company can't see itself, so don't stop at the first two or three obvious ones. Work through **every** persona, role, problem, challenge, objection, and buying stage from Step 2, and raise a gap wherever coverage is **missing _or_ weak** (vague, no concrete outcome, not tailored to the role). Aim to surface on the order of **8–12+ candidate gaps** for a typical persona set before you narrow — it's fine to generate broadly and then let the user rule some out.

For each gap you identify, propose **2-3** ideas for a new value proposition in the PSO (Problem · Solution · Outcome) format:
- **P (Problem)** — the problem from the buyer persona (already identified)
- **S (Solution)** — what the company could do to solve that problem
- **O (Outcome)** — the business outcome it would deliver for the customer

Give each proposed missing value a stable ID, **`MV-01`, `MV-02`… (MV = Missing Value)**, as you generate it. `MV-` marks a value that is *proposed, not yet built*, distinct from the `PV-/SV-/AV-` IDs of values the company already has; if the company later builds it, it graduates to a regular `PV-/SV-/AV-` value in the Value Proposition skill. Refer to gaps by their `MV-` ID in the score table, the priority matrix, and the recommendations.

Keep the ideas realistic — grounded in what the company already does and the resources and competencies it has. Don't propose anything that would require changing the business model (unless the user asks for it).

After each batch of ideas, ask the user: "Which of these ideas are realistic to implement? Which do you rule out?"

### Step 4: Score each missing value

For each approved missing value, score two dimensions:

> **How this differs from the value-strength score.** Skill 1 (Value Proposition) scores the *strength of existing values* (Problem + Outcome, max 20) to rank your current list. The Impact/Effort score below prioritises *new values to build* (impact on sales × implementation effort, 1-10 each). They answer different questions. Use the strength score to rank what you have, and this matrix to sequence what to add.

Score each dimension 1-10, then read off its band (**Easy/Low = 1-3, Medium = 4-7, Hard/High = 8-10**) to place the value on the priority matrix.

**Implementation difficulty / cost (1-10):**
- **1-3 = Easy** — the company can implement it immediately or within weeks, at no significant cost. Mostly a matter of a decision and communication, not infrastructure. Example: changing how the offer is presented, adding a section to the website, creating a checklist for customers.
- **4-7 = Medium** — requires an investment of time or money (a few weeks to months, a moderate budget). May call for new processes, tools, or team training. Example: building an ROI calculator, creating an onboarding program, launching regular reporting.
- **8-10 = Hard** — requires a significant investment (months of work, a large budget, new competencies, hiring). May call for changes to the product, infrastructure, or business model. Example: developing a new product module, certification, building a buffer warehouse.

**Impact on sales (1-10):**
- **1-3 = Low** — the value is nice to have, but it doesn't change the buying decision. Nice-to-have, not must-have. Affects few customers or a peripheral problem.
- **4-7 = Medium** — the value strengthens the offer and can tip the scales against the competition. Addresses a significant (but not critical) customer problem.
- **8-10 = High** — the value addresses a critical customer problem that currently blocks sales. Without it, the company loses deals. Affects many customers in the segment.

Validate the scores with the user: they know best what is easy and what is hard in their company.

### Step 5: Build the priority matrix

Plot the values (each by its `MV-` ID) on a 3×3 Impact/Effort priority matrix (difficulty × impact) and sort them by implementation priority.

For the order of priorities, see [references/rules-missing-pso.md](references/rules-missing-pso.md), section "Priority matrix".

Show the user the matrix and the recommendation: "Start with these [X] values — they're simple to implement and have a big impact on sales."

### Step 6: Deliver the result as files

Generate TWO files (`.md` and a styled, self-contained `.html`). The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format). For the format, see [references/rules-missing-pso.md](references/rules-missing-pso.md), section "Output file format".

Save both files and share them with the user for download.

## Add to the Strategy Dossier

This suite runs as one continuous session. **Deliver only your own two files now** — the **Strategy Dossier** is an **internal running document**, not delivered until the end, so don't create or hand over a dossier file mid-session. Record the **Missing Value Propositions** section into that internal dossier with the gap analysis and the Impact/Effort priority matrix. Full format: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **No PSO (Problem · Solution · Outcome) and buyer persona, no gap analysis.** Don't generate without both documents.
2. **A gap is the absence of a value for a REAL problem.** Don't invent problems. Anchor everything in the buyer persona.
3. **The ideas must be realistic.** Build on what the company already does and knows how to do. Don't propose a business revolution without reason.
4. **Score together with the user.** You propose the scores; the user verifies them, because they know better what is easy or hard in their company.
5. **Quick wins first.** The priority matrix exists so the company doesn't start with the hardest items. Easy + big impact = do it immediately.
6. **PSO (Problem · Solution · Outcome) format.** Every missing value must have a complete P-S-O (not a loose idea) and a stable **`MV-`** ID (`MV = Missing Value`: proposed, not yet built).
7. **Per persona, per role.** Gaps can differ across personas and across roles, so don't average them out.
8. **A discovery conversation, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you build, push every vague answer toward a specific, and label any gap you fill yourself **[Assumption]**.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
