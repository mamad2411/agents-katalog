---
name: product-plan
description: "Product planning skill that generates a research-backed launch roadmap — operations, partnerships, trust-building, product evolution, and go-to-market execution. Each task tagged as human-only, AI-assisted, or automatable. Part of the Product Pipeline: use after /product-strategy and before /product-design."
metadata:
  argument-hint: "[describe your product or paste your strategy brief]"
---

# Launch Playbook

You are generating a comprehensive, research-backed operational playbook for launching a product. This covers everything OUTSIDE the code — the partnerships, the trust-building, the supply seeding, the legal groundwork, the community cultivation, and the go-to-market execution that actually makes a product succeed in the real world.

Uber had to convince people to drive their cars for strangers. Airbnb had to convince people to sleep in stranger's homes. Spotify had to negotiate music licenses. Every successful product has a "big how" that goes far beyond the app. That's what this playbook covers.

The user's request is: **$ARGUMENTS**

**Core principles:**
- This is NOT about how to code the app. That's what product-design is for.
- This IS about everything else: operations, partnerships, trust, legal, community, content, go-to-market execution — AND what the product needs to DO at each phase (not how to build it, but what it needs to be capable of).
- **Include a "Product at This Phase" section in each phase** that describes what the app/product should look like and be capable of at that stage. This bridges the gap between strategy and implementation. Think of it as the product requirements that change as you progress — the app at Week 1 (might be a Google Form) is very different from the app at Month 3 (needs real-time matching). This is NOT technical specs — it's "what does the user need to be able to do right now?" framed as capabilities.
- **Research real launch stories.** Search for how similar products actually launched — not theory, but what Uber, Airbnb, Nextdoor, and relevant competitors actually did.
- Every task gets tagged: 🧑 **Human** (requires a real person), 🤖 **AI-Assisted** (a person with AI help), or ⚡ **Automatable** (AI or software can handle it).
- Write in plain English. This should feel like advice from a friend who's launched three startups, not a McKinsey deck.
- Be specific to THIS product. Generic advice ("build a community") is useless. Specific advice ("post in 5 local Facebook groups for neighborhoods with new construction") is gold.

---

## PHASE 1 — Understand the Product

### Step 1a — Check for Strategy Brief

First, check if `.decisions/strategy-brief.md` exists. If it does, the user has already run Product Strategy. Read it carefully — the problem definition, target user, market positioning, business model, and go-to-market strategy should all inform the playbook.

When a strategy brief exists:
- **Use every decision as context.** The playbook should be a direct execution plan for the strategy.
- **Look for the "Elevator Pitch" section** in the strategy brief. If it exists, use it verbatim at the top of the playbook in the elevator-pitch section. This is the canonical description of the product chosen by the user in Product Strategy's final decision.
- **Tell the user:**

> "I found your strategy brief from Product Strategy — including your elevator pitch. I'll build the playbook around your decisions. Let me research how similar products actually launched..."

### Step 1b — Understand the Request

If there's no strategy brief, read `$ARGUMENTS` carefully.

If the request is clear enough to identify what the product is, who it's for, and roughly how it works, proceed to Phase 2.

If `$ARGUMENTS` is too vague, ask 1-2 questions:

> "Before I can build a launch playbook, I need to understand the product. Can you tell me:
> - What does it do and who is it for?
> - What's the hardest non-technical challenge? (e.g. getting initial supply, building trust, securing partnerships)"

Wait for their answer, then proceed.

---

## PHASE 2 — Research Real Launch Stories

Before generating anything, research how similar products actually launched. This is the foundation of a useful playbook.

### Research Protocol

1. **Identify 2-3 comparable products** that faced similar challenges (marketplace cold start, trust building, supply acquisition, partnership dependencies, etc.)

2. **Search for their actual launch stories:**
   - "[company] how they got first users"
   - "[company] launch strategy first city"
   - "[company] cold start problem how they solved it"
   - "[industry] marketplace operations playbook"

3. **Search for operational specifics:**
   - "[industry] partnership strategy"
   - "[industry] trust and safety operations"
   - "[industry] supply acquisition tactics"
   - "[product type] legal requirements launch checklist"

4. **Synthesize the research** into actionable patterns. Focus on:
   - What they did BEFORE launch (supply seeding, partnerships, legal)
   - What they did DURING launch (first users, first transactions)
   - What they did to GROW (scaling operations, expanding markets)
   - What almost killed them (operational failures, trust breakdowns)

5. **Tell the user** what you found:

> "Researched how [Company A], [Company B], and [Company C] actually launched. Key insight: [most important finding]. Building your playbook now..."

---

## PHASE 3 — Generate the Playbook

Generate a self-contained HTML file and open it in the browser. The playbook is organized into phases, each containing specific tasks.

### Step 3a — Set Up Directory

```bash
mkdir -p .playbook
```

### Step 3b — Determine the Phases

Organize tasks into 4-6 phases based on the product. Typical phases:

**For a marketplace/platform:**
1. Foundation (legal, tooling, accounts)
2. Supply Seeding (getting initial inventory/providers)
3. Trust Infrastructure (verification, safety, insurance)
4. Soft Launch (first neighborhood/city, first 10 transactions)
5. Growth & Expansion (scaling to more markets)
6. Sustainability (retention, operations, team)

**For a B2B product:**
1. Foundation (legal, positioning, collateral)
2. Partnerships & Integrations
3. Pilot Program (first 3-5 customers)
4. Sales Infrastructure
5. Scale

**For a consumer app:**
1. Foundation (legal, accounts, content)
2. Community Seeding
3. Launch & PR
4. Growth Loops
5. Retention & Engagement

Adapt the phases to what THIS product actually needs. Don't use generic phases.

### Step 3c — Generate Phase Overview and "Product at This Phase" Section

For each phase, include TWO callout boxes BEFORE the tasks:

**1. Phase Overview** (`.phase-overview` box) — A brief description of what this phase is about, why it matters, and what success looks like. This orients the reader before they dive into tasks. Include:
- **What you're doing** — 2-3 sentences describing the goal of this phase in plain English
- **Why this matters** — What fails if you skip this? Ground it in research or real examples.
- **Success looks like** — Concrete, measurable outcome. "15 lenders with 100+ tools listed" not "enough supply."

**2. Product at This Phase** (`.product-phase` box) — described below.

For each phase, include a "Product at This Phase" callout box BEFORE the tasks. This describes what the app/product needs to be capable of at this stage — not how to build it, but what users need to be able to do. Think of it as the product requirements that evolve as you progress.

This section should cover:
- **What form the product takes** at this stage (could be a spreadsheet, a landing page, a basic app, or a full platform)
- **Core capabilities needed** — what must users be able to do?
- **What can wait** — explicitly call out features that are NOT needed yet
- **The transition trigger** — what signals it's time to level up the product

Example progression for a marketplace:
- Phase 1: "No app needed. Use a Google Form for tool listings and a group text for borrow requests."
- Phase 2: "You need a way to list tools with photos and a landing page. A Notion database or Airtable works fine."
- Phase 3: "Now you need user accounts, verification, and a basic borrow flow. This is when you build the real app."
- Phase 4: "Add messaging, reviews, and payment processing. The app needs to handle the full borrow lifecycle."
- Phase 5: "Add notifications, automated matching, and neighborhood analytics. The app needs to scale across neighborhoods."

The key insight: the product should be as simple as possible for as long as possible. Don't build features before you need them. Many successful startups launched with spreadsheets and manual processes before building software.

Use the `.product-phase` CSS class for this section in the HTML template.

### Step 3d — Generate Tasks

For each phase, generate 5-12 specific, actionable tasks. Each task must have:

- **Title** — short, action-oriented (verb first)
- **Why it matters** — 1-2 sentences grounding it in research or the strategy
- **How to do it** — 2-4 bullet points with specific, actionable steps
- **Effort tag** — 🧑 Human, 🤖 AI-Assisted, or ⚡ Automatable
- **Priority** — Critical, Important, or Nice-to-have
- **Estimated effort** — Hours, days, or weeks

### Step 3d — Write the HTML

Generate the playbook as `.playbook/playbook.html` using the **PLAYBOOK HTML TEMPLATE** below.

### Step 3e — Open in Browser

```bash
open .playbook/playbook.html
```

### Step 3f — Tell the User

> "Your launch playbook is open in your browser. It has [N] phases and [N] tasks covering everything from [first phase] to [last phase]. Each task is tagged with whether it needs a human, AI assistance, or can be automated.
>
> The research behind it is based on how [Company A] and [Company B] actually launched — real stories, not theory.
>
> You can check off tasks as you go. Want me to dive deeper into any specific phase?"

---

**Playbook HTML:** read `references/playbook-template.md` before generating the playbook. It holds the full template — structure, CSS, phase/task markup and the tagging legend.

## PHASE 4 — Present and Iterate

After generating the playbook:

> "Your launch playbook is ready — [N] tasks across [N] phases. It's interactive: click any task to check it off, and your progress is saved in your browser.
>
> The playbook is based on how [Company A] and [Company B] actually launched, adapted to your specific strategy.
>
> Want me to:
> - **Dive deeper** into any specific phase or task?
> - **Add more tasks** to a particular area?
> - **Research a specific challenge** (e.g. 'how do I actually approach realtors?')
> - **Generate templates** (email scripts, pitch decks, partner proposals)?"

Wait for the user's response.

### Handling Follow-up Requests

**"Dive deeper into [phase]":** Research more specifically and add 5-10 additional detailed tasks to that phase. Regenerate the HTML.

**"Add tasks for [topic]":** Add a new section or expand an existing phase. Regenerate the HTML.

**"Generate a template for [task]":** Create the specific asset (email template, pitch script, checklist, etc.) and save it as a separate file in `.playbook/templates/`. Reference it from the task.

**"Research [specific challenge]":** Run targeted searches and update the relevant tasks with more specific, research-backed steps.

---

## EDGE CASES

**No strategy brief exists:** Build the playbook from the user's description. Ask clarifying questions if needed about the target user, business model, and go-to-market approach — these heavily influence the operational tasks.

**User wants to focus on one phase only:** Generate only that phase in detail. Don't force the full playbook if they know what they need.

**User asks for the technical stuff too:** Point them to better-plan-mode: "The app implementation is a separate set of decisions — run `/product-design` for that. This playbook is everything else."

**Product doesn't need much operational work:** Some products (developer tools, SaaS with no marketplace dynamics) need less operational setup. Scale down to 2-3 phases with fewer tasks. Don't pad it.

---

## IMPORTANT REMINDERS

1. **Research real stories.** Every playbook should include research on how 2-3 comparable products actually launched. Real tactics, not theory.
2. **Be absurdly specific.** "Email 5 realtors" not "build partnerships." "Post in the Elm Street Neighbors Facebook group" not "do social media."
3. **Tag every task.** Human, AI-Assisted, or Automatable. This helps the user prioritize where to spend their irreplaceable human time.
4. **Ground tasks in the strategy.** Reference the strategy decisions throughout. "Since we chose trust-first positioning (Decision 3), our onboarding needs to emphasize verified profiles."
5. **Interactive HTML.** The playbook must have clickable checkboxes that persist via localStorage. This is a living document people use over weeks.
6. **Self-contained.** No external dependencies. Works by opening the file directly.
7. **Connect the pipeline.** Reference product-strategy (strategy) and product-design (technical) in the footer. The user should understand where this fits.
8. **Don't overlap with product-design on technical HOW.** No tasks about choosing frameworks, designing UI components, or writing code. BUT DO include "Product at This Phase" sections that describe what the app needs to be CAPABLE of at each stage. Think product requirements, not technical specs. "Users need to be able to browse tools with photos" (yes) vs. "Use React with a Supabase backend" (no — that's product-design's job).
9. **Phases should have realistic timeframes.** "Week 1-2" not "Phase 1." Help people plan their actual calendar.
10. **The first phase should be doable THIS WEEK.** Don't front-load with weeks of research. Put quick wins early to build momentum.
