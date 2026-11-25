---
name: company-brief
description: >
  One-time intake for the Ananas-Agency B2B Go-to-Market Suite. Captures a company's
  fundamentals — industry, offering, customers, commercial model, and competition —
  into a reusable Company Brief that every other skill (Value Proposition, Buyer Persona,
  Buying Process, Persona Experiments, Missing Value Propositions) consumes instead of
  re-asking the basics. Use this skill when the user wants to: set up their company
  profile, start the Ananas-Agency process, onboard, or give background before building
  value propositions or personas. Trigger: "company brief", "company intake", "company
  profile", "company background", "onboarding", "start here", "set up my company", "tell
  you about my company".
---

# Company Brief (Ananas-Agency — Intake)

## Goal

Run a short, one-time interview that produces a reusable **Company Brief**: the shared foundation for every other Ananas-Agency skill. Fill it in once, then paste it into the next skill instead of answering the same company questions again.

## Why a Company Brief

The Value Proposition, Buyer Persona, Buying Process, Persona Experiments, and Missing Value Propositions skills all need the same starting facts about the company. Capturing them once:

- removes repetition across skills,
- keeps every downstream document consistent (same segments, same competitors, same numbers),
- gives you a single profile you can update as the company evolves.

This skill is intake only — it does NOT produce strategy. It feeds the skills that do.

## What the brief captures

1. **Company & offering** — the company name and a one-line description; industry, sub-industry; whether you sell a physical product, a service, software, or a mix; what the customer "buys on the invoice".
2. **Customers** — the segments you sell to today; which bring in the most revenue; segments you'd like to reach but haven't yet.
3. **Commercial model** — typical deal size, average sales-cycle length, and how you currently reach customers (inbound, outbound, referrals, channel).
4. **Competition & differentiation** — main competitors; whether your offering is differentiated or closer to a commodity.
5. **Context & assets** — website URL and any existing materials (deck, one-pager, case studies).

## Conversation flow

Guide the user step by step, 2-3 questions per turn. Don't overwhelm.

> **How to run this session — read before you start.** This is a short **discovery chat**, not a deep workshop: the brief is intake, not strategy, so keep it to one focused pass (roughly **5–8 questions**, 2–3 at a time). It's only useful if it's concrete, though, so don't settle for vague answers.
> - **Let them describe first, then switch to choices.** Let the user describe the company in their own words first, then move to targeted questions — don't keep everything open.
> - **Prefer pickable options to keep it quick.** When a question has a small, knowable set of likely answers (product / service / software / mix; inbound / outbound / referrals / channel), offer them as a pickable list rather than open prompts — an all-open intake drags. Still push for the concrete detail behind the pick.
> - **Get specifics, not labels.** When an answer is generic ("we serve SMEs", "we're competitive"), ask one follow-up for the concrete detail: a real number (deal size, cycle length, headcount), a named segment, a named competitor. Capturing real facts now saves every later skill from re-asking.
> - **Cover the checklist.** Don't deliver the brief until every item in **Required inputs** below is captured, or the user has explicitly marked it unknown.
> - **Ask before you assume.** Never invent a fact the user could give you. Ask first. Anything the user genuinely doesn't know stays **TBD**, never a guess, so the downstream skills know to fill it.

### Required inputs — capture before delivering
Check each off (or mark **TBD**) before Step 4 (Confirm & deliver):
- [ ] Company name, one-line description, **website URL**, and any **presentation / deck / materials** (all asked up front in Step 1)
- [ ] Company & offering — industry, sub-industry; product / service / software / mix; what the customer pays for "on the invoice"
- [ ] Customers — segments sold to today; which bring the most revenue; segments wanted but not yet reached
- [ ] Commercial model — typical deal size; average sales-cycle length; how customers are reached today
- [ ] Competition — main competitors; differentiated vs commodity
- [ ] Context & assets — website + presentation/deck/one-pager/case studies (captured in Step 1) reviewed and analysed

### Step 1: Company, website & materials

Open by capturing the essentials up front, so you can analyse the company's own sources early:
- **Company name** and a **one-line description** (what the company does, in one sentence) — these head the brief and every downstream document.
- **Website URL** — ask for it now; if the user gives it, analyse the site and pull preliminary facts to confirm with them later.
- **A company presentation / deck** (or one-pager, case studies) — ask the user to share or paste any existing materials, and analyse them for the same reason.

Then ask what the company does in more detail (industry, sub-industry) and whether it sells a product, a service, software, or a mix — and what exactly the customer pays for "on the invoice".

### Step 2: Customers & commercial model

Ask which segments they sell to today, which bring in the most revenue, typical deal size and sales-cycle length, and how they currently reach customers.

### Step 3: Competition & context

Ask about the main competitors and whether the offering is differentiated or commodity-like.

(The website and any materials were already requested in Step 1 — if the user hadn't provided the URL then, ask for it now, analyze it, and extract preliminary facts to confirm with them.)

### Step 4: Confirm & deliver

Summarize the brief back to the user and ask them to confirm or correct it. Mark anything unknown as "TBD" rather than guessing. Then deliver the files.

### Step 5: Hand off

Tell the user the brief is ready and that the recommended next skill is **Value Proposition** (everything else builds on it). From here on, they paste this brief in whenever a later skill asks about the company.

## Output: deliver the brief as files

Generate TWO files (`.md` and a styled, self-contained `.html`) and share them with the user. The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format). Format — see: [references/rules-company-brief.md](references/rules-company-brief.md), section "Output file format".

Save both files and share them with the user for download.

## Add to the Strategy Dossier

This suite is meant to run as one continuous session, start to finish. **Deliver only your own two files now** (`.md` + `.html`). Keep the **Strategy Dossier** as an **internal running document** — do **not** create, show, or hand over a dossier file mid-session; it is assembled and delivered only at the very end (by the final skill). As the usual first skill, start that internal record and add the **Company Brief** section from what you just captured. Full format and section order: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **Intake, not strategy.** Keep it to one short pass; don't drift into building value propositions or personas.
2. **Don't invent.** Mark unknowns as "TBD". The downstream skills fill the gaps as they surface the facts, and the final skill (Messaging & Positioning) runs a reconciliation pass that backfills any TBDs still open at the end — so leave a genuine unknown as "TBD" rather than guessing.
3. **Be specific where it's cheap.** Capture real numbers (deal size, cycle length, headcount) whenever the user knows them.
4. **One brief, reused everywhere.** Remind the user to paste this into the other skills instead of re-answering the same questions.
5. **It's a living document.** Update the brief whenever the company changes.
6. **A discovery chat, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you deliver, ask for the concrete detail behind vague answers, and keep anything unknown as **TBD**, never a guess.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
