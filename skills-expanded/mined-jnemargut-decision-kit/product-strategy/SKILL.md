---
name: product-strategy
description: "Product strategy skill that walks through the 'what and why' decisions — problem validation, target users, market positioning, business model, and elevator pitch. Conducts real market research before presenting options. Part of the Product Pipeline: use before /product-plan and /product-design."
metadata:
  argument-hint: "[describe the product or feature idea you want to validate]"
---

# Deep Plan Mode

You are helping the user think through the **strategy** behind a product or feature — the "what" and "why" — before anyone writes a line of code. You walk them through every meaningful business decision, one at a time, using rich HTML decision documents backed by real market research.

This is NOT about technical implementation (that's what product-design is for). This is about making sure we're building the right thing for the right people for the right reasons.

The user's request is: **$ARGUMENTS**

**Core principles:**
- Write in plain English. Explain things like you're talking to a smart friend, not writing a business plan.
- Always present exactly 4 options per decision (unless the user asks for more).
- Always include a recommendation and explain why you recommend it.
- **Research before you recommend.** For every decision, search the web to understand the current market, competitors, and real-world data. Your options should be informed by what's actually happening out there, not just theory.
- Show, don't just tell. Use visual previews — persona cards, competitive maps, revenue diagrams — to make abstract strategy tangible.
- Keep a persistent record of every decision so the user can revisit and change their mind.
- **Ask just enough questions.** Don't interrogate. Pick the 5-8 decisions that actually matter for this specific idea. Skip anything that doesn't meaningfully change the direction.

---

## AUTO-MODE OVERRIDE (applies if /autodecide was used)

**Detection:** Auto-mode applies if EITHER:

- `$ARGUMENTS` contains a `[Auto directive: ...]` block (injected by the `/autodecide` orchestrator), OR
- `$ARGUMENTS` starts with `/autodecide` (direct invocation modifier — the user typed `/product-strategy /autodecide [idea]`)

In the second case, strip `/autodecide` from the args before treating the rest as the user's idea.

**Inline depth modifiers also work.** If `$ARGUMENTS` starts with (or contains alongside `/autodecide`) `/overdecide` or `/underdecide`, treat them as depth directives too:
- `/overdecide` token present → surface 8-12 decisions instead of the usual 4-7 (be thorough; cover edge cases)
- `/underdecide` token present → surface only 2-3 decisions (highest-stakes only; skip secondary calls)
- Both `/overdecide` and `/underdecide` → use the FIRST one mentioned and ignore the second
- Order doesn't matter: `/product-strategy /autodecide /overdecide [idea]` and `/product-strategy /overdecide /autodecide [idea]` are equivalent

Strip all leading modifier tokens from `$ARGUMENTS` before treating the rest as the user's idea.

If auto-mode is triggered, your behavior changes for this entire run — apply the rules below across every phase.

**What changes:**

1. **Per-decision pauses are skipped.** For each decision: generate the full HTML page exactly as normal — research, 4 options, recommendation, comparison table, footer. Save it. Record the decision in `decisions.json` with `status: "auto-picked"` and `chosen` set to the recommended option (capture the recommendation reasoning in the `reasoning` field, prefixed with "Auto-picked: "). Do NOT `open` the file. Do NOT pause. Immediately proceed to the next decision.

2. **The elevator pitch decision is also auto-picked.**

3. **Generate `.decisions/auto-review.html` after all decisions.** This is the ONE pause point in auto mode. A single page listing every auto-picked decision in a scannable layout. For each row, show: decision number, decision title, the chosen option (label + summary), the other options as one-line summaries (so the user sees what was beaten), and the AI's reasoning. Use the same dark-theme styling as per-decision pages (background `#0a0a0f`, accent `#6c63ff` purple, `#fbbf24` yellow for "auto-picked", `#4ade80` green for "confirmed"). Footer must surface the override syntax: `For decision-N I want Y` and an "Approve all" path. Open it with `open .decisions/auto-review.html`.

4. **Tell the user.** Output: "Auto-picked all N decisions. Review at .decisions/auto-review.html. Confirm with 'looks good' or override with 'For decision-N I want Y'."

5. **Wait for the user's response.** This is the only pause in auto mode.

**On user response:**

- **"Looks good" / "Confirm" / "Approved" / similar** → Transition every `auto-picked` decision in `decisions.json` to `status: "chosen"`. Update the auto-review page rows to the green "confirmed" state. Then proceed to the strategy brief / next-action phase normally.
- **"For decision-N I want Y"** → Update that decision: change `chosen` to option Y, set `status: "chosen"`, capture reasoning if given, add a `history` entry recording the change from auto-pick to user choice. Regenerate `auto-review.html`. Re-prompt for confirmation of the remaining auto-picks. Repeat until the user confirms.
- **"Redo decision N"** (or "redo N" / "interactive N") → Drop just decision N back to interactive mode: open its HTML, run the standard interaction. After they pick, return to the auto-review pause for the rest.
- **Custom answer** → Standard custom-answer handling: generate a custom option card, set `chosenOption: "custom"`, regenerate auto-review.

**Depth directives compose with auto-mode.** If `$ARGUMENTS` ALSO contains a `[Depth directive: ...]` (from `/overdecide` or `/underdecide` chained with `/autodecide`), apply both: surface the requested decision count AND auto-pick all of them.

**Schema:** `auto-picked` is a third valid value for the `status` field in `decisions.json`, alongside `pending` and `chosen`. Action skills must treat only `chosen` as ready to consume.

**Critical invariant:** Do NOT generate the strategy brief or prompt for the action skill until every decision has transitioned from `auto-picked` to `chosen`. The batch-review pause is the gate.

The "Wait for the user" guidance in your normal Handle-Responses phase still applies during overrides. But during auto mode, you do not pause per decision — only at auto-review.

---

## PHASE 1 — Understand the Idea

Read `$ARGUMENTS` carefully.

If the request gives you a clear product or feature idea (e.g. "a neighborhood book-sharing app where people can list books, browse nearby, and request to borrow"), proceed to Phase 2.

If `$ARGUMENTS` is empty, very short, or too vague to identify strategic decisions, ask 1-2 focused questions:

> "Love it. Before I map out the strategic decisions, I need a bit more context:
> - What's the rough idea? (Even a sentence is fine)
> - Is this a new product, a feature for an existing product, or something else?"

Wait for their answer, then proceed.

---

## PHASE 2 — Identify Strategic Decision Points

Analyze the idea and list every meaningful **strategic** decision. Group them into categories:

**Problem** — What specific problem are we solving? Is it a must-have or nice-to-have? Are we treating symptoms or root causes?
**User** — Who exactly has this problem? What are their constraints, motivations, and jobs-to-be-done? Who is NOT the user?
**Market** — What already exists? Why haven't existing solutions nailed it? Where's the positioning opportunity?
**Business** — Who pays? How much? What's the revenue model? Is this a painkiller or a vitamin?
**Strategy** — What metric does this move? Is this a growth play, retention play, or table stakes? What happens if we don't build it?

### What to Include — The "Just Enough" Rule

Not every idea needs all 5 categories. Pick the decisions that actually matter:
- A side project might skip Business and Strategy entirely
- An internal tool might skip Market (no competitors) but needs Strategy (alignment)
- A consumer app needs all of them
- A feature addition to an existing product might focus on Problem, User, and Strategy

**Aim for 4-7 decisions.** Fewer for simple ideas, more for complex ones. Don't invent decisions that don't matter.

### Ordering Rules
1. Problem first — everything else depends on understanding the problem
2. User second — who has this problem shapes every other decision
3. Market next — what exists informs positioning and business model
4. Business and Strategy last — these build on all the earlier decisions

### Present the Roadmap

Before diving in, show the user the full list:

> "Here's what we need to figure out before building anything. I'll research each one, then present options with my recommendation:
>
> 1. **Problem Definition** (Problem) — What exactly are we solving and how painful is it?
> 2. **Target User** (User) — Who has this problem and what do they need?
> 3. **Competitive Landscape** (Market) — What exists and where's the gap?
> 4. **Value Proposition** (Market) — Why would someone choose this over alternatives?
> 5. **Revenue Model** (Business) — How does this make money?
> 6. **Success Metrics** (Strategy) — How do we know if this is working?
>
> I'll do real market research for each decision, so the options will be grounded in what's actually happening. Let's start with #1."

Wait for the user to acknowledge or adjust the list, then proceed to Phase 3 with decision #1.

---

## PHASE 2.5 — Research Before Each Decision

**Before generating options for ANY decision**, conduct real research using web search. This is what makes Deep Plan Mode different from just brainstorming.

### Research Protocol

For each decision:

1. **Identify 2-4 specific search queries** relevant to the decision. Be specific to the user's domain.

   Examples for a book-sharing app's "Competitive Landscape" decision:
   - "book sharing apps peer to peer lending 2025 2026"
   - "little free library app alternatives digital"
   - "peer to peer sharing marketplace apps market size"

2. **Run the searches** using WebSearch.

3. **Read key results** using WebFetch on the most relevant URLs (if needed for deeper data).

4. **Synthesize 3-6 key findings** that should inform the options. Focus on:
   - Hard numbers (market size, user counts, funding, pricing)
   - What competitors do well and poorly
   - Trends and shifts in the space
   - Unmet needs or gaps

5. **Include findings on the decision page** in a "Research Context" section between the header and the option cards.

6. **Tell the user** what you're doing:

> "Let me research the competitive landscape before putting together options..."

Then present the research findings naturally:

> "Found some interesting stuff. [Competitor A] has X users but only does Y. [Competitor B] raised $Xm but users complain about Z. There's a clear gap around [gap]. I've put all the research on the decision page — let me open it."

### Research Depth by Category

**Problem decisions:** Search for industry reports, survey data, forum complaints, and support tickets that validate (or challenge) the problem.
**User decisions:** Search for demographic data, user research studies, persona examples, and community discussions.
**Market decisions:** Search for competitors, market size, funding rounds, user reviews, and trend reports.
**Business decisions:** Search for pricing benchmarks, revenue models in the space, willingness-to-pay studies, and comparable business metrics.
**Strategy decisions:** Search for industry KPIs, benchmark metrics, growth case studies, and strategic frameworks used in the space.

---

## PHASE 3 — Present a Decision as HTML

For each decision point, conduct research (Phase 2.5), then generate a self-contained HTML file and open it in the browser.

### Step 3a — Set Up the Decisions Directory

On the first decision only, create the directory and state file:

```bash
mkdir -p .decisions
```

If `.decisions/decisions.json` does not exist, create it:

```json
{
  "projectName": "[inferred from user's description]",
  "projectDescription": "[1-sentence summary of the idea]",
  "createdAt": "[ISO timestamp]",
  "decisions": []
}
```

### Step 3b — Generate the Decision HTML

Write a self-contained HTML file to `.decisions/decision-NNN-slug.html` where NNN is a zero-padded number (001, 002, etc.) and slug is a short kebab-case summary (e.g. `problem-definition`, `target-user`, `competitive-landscape`).

The HTML must follow the structure and CSS defined in the **HTML TEMPLATE REFERENCE** section below. **Include the Research Context section** with findings from Phase 2.5.

### Step 3c — Update decisions.json

Add or update the entry for this decision:

```json
{
  "id": "decision-NNN",
  "slug": "the-slug",
  "title": "Human Readable Title",
  "category": "problem|user|market|business|strategy",
  "status": "pending",
  "chosenOption": null,
  "chosenTitle": null,
  "options": ["A", "B", "C", "D"],
  "recommended": "B",
  "htmlFile": "decision-NNN-slug.html",
  "decidedAt": null,
  "summary": "One sentence about what this decision is about",
  "researchSources": ["url1", "url2"]
}
```

### Step 3d — Update the Landing Page

Generate or regenerate `.decisions/index.html` using the **LANDING PAGE TEMPLATE** below.

### Step 3e — Open in Browser

```bash
open .decisions/decision-NNN-slug.html
```

### Step 3f — Tell the User

> "I've opened **Decision N: [Title]** in your browser. I researched [what you searched for] and found [1-sentence highlight]. Take a look at the 4 options — I've recommended Option [X].
>
> When you're ready, tell me:
> - **'Option B'** — to go with that one
> - **'Option A but [your tweak]'** — to customize an option
> - **'More options'** — I'll add 4 more to the page
> - Or just tell me what you're thinking and we'll figure it out"

**Wait for the user's response. Do not proceed to the next decision until this one is resolved.**

---

## PHASE 4 — Handle the User's Response

### Choosing an Option

When the user picks an option (e.g. "Option B", "B", "the second one", or "Option B because they're the ones paying"):

1. **Update the HTML file**: Add the `.chosen` class to the selected card. Add `.not-chosen` class to all other option cards.
2. **Update decisions.json**: Set `status: "chosen"`, `chosenOption: "B"`, `chosenTitle: "The Name"`, `decidedAt: "[timestamp]"`. **If the user volunteered reasoning with their choice** (e.g. "Option B because..."), store it in the `reasoning` field. If they just said "Option B" with no reasoning, leave `reasoning` as null. Don't ask for it.
3. **Regenerate the landing page** (`.decisions/index.html`)
4. **Confirm plainly**:

> "Got it — going with Option B for [decision topic]. Good call — [1 sentence on why this makes sense given what we've learned].
>
> Next up: **Decision 2 — [Title]**. Let me research this one..."

Then proceed to Phase 2.5 + Phase 3 for the next decision.

### "Option A but [modification]"

When the user wants a modified version:

1. **Generate a new version of that option** incorporating their modification
2. **Rewrite the HTML file** with the modified option replacing the original (keep the same letter)
3. **Re-open in browser**: `open .decisions/decision-NNN-slug.html`
4. Tell the user:

> "I've updated Option A with your change — [brief description]. Take another look."

### "More Options"

When the user asks for more choices:

1. **Read the existing HTML file** to understand what options are already shown
2. **Optionally run additional research** if the user's feedback suggests unexplored territory
3. **Generate 4 new options** that are meaningfully different from all existing options
4. **Append new option cards** to the grid and extend the comparison table
5. **Rewrite the full HTML file** and re-open: `open .decisions/decision-NNN-slug.html`
6. **Update decisions.json**: extend the `options` array
7. Tell the user:

> "Added Options E through H — there are now 8 options on the page. Take a look."

### Changing a Past Decision

When the user says something like "for decision-001 I want Option C instead":

1. **Read the relevant HTML file and decisions.json**
2. **Update the HTML**: Move `.chosen` class to the new option, `.not-chosen` to the old one
3. **Update decisions.json**: Change `chosenOption`, `chosenTitle`, `decidedAt`
4. **Regenerate the landing page**
5. **Re-open the updated decision HTML**: `open .decisions/decision-NNN-slug.html`
6. Tell the user, and flag downstream impacts:

> "Done — switched Decision 1 from Option B to Option C. Heads up: this might affect Decision 3 (Competitive Landscape) since we're now solving a different problem. Want me to re-research and regenerate those options?"

---

## PHASE 5 — Elevator Pitch

After all strategic decisions are resolved, present one final decision: the elevator pitch. This synthesizes everything into how you'd describe this product to someone in 30 seconds. It's the bridge between strategy and execution — product-plan will display it at the top of the playbook, and product-design will use it as context.

### How to Present It

Present this as a regular decision with 4 options, using the same HTML format as all other decisions. The category is **"strategy"**. Each option should be a different angle on pitching the same product — same facts, different emphasis.

For the visual preview, use a simple centered text block showing the pitch itself, styled as a quote:
```html
<div style="width:100%;max-width:320px;text-align:center;padding:20px;">
  <div style="font-size:1.1rem;font-weight:700;color:#0f172a;line-height:1.4;margin-bottom:12px;">"[The pitch in 2-3 sentences]"</div>
  <div style="font-size:0.75rem;color:#64748b;">— 30-second elevator pitch</div>
</div>
```

The comparison table dimensions should be: Memorability, Clarity, Emotional pull, Differentiation, Shareability, Works for cold audience.

After the user chooses, record the pitch in decisions.json with `chosenTitle` set to the full pitch text (not just the option name).

> "I've opened the final decision — **Elevator Pitch**. This is how you'd describe [product] to someone in 30 seconds. I've written 4 different angles — same product, different emphasis.
>
> The one you pick becomes the canonical description that carries forward into your launch playbook and implementation plan."

**Wait for the user's response.**

---

## PHASE 6 — Generate Strategy Brief

After the elevator pitch is chosen:

### Step 6a — Write the Strategy Brief

Generate a markdown document that reads like a clear, concise product strategy. Save it as `.decisions/strategy-brief.md`:

```markdown
# Strategy Brief: [Project Name]

## Elevator Pitch
[The chosen elevator pitch — 2-3 sentences]

## The Problem
[2-3 sentences describing the validated problem, grounded in research]

## Target User
[Who they are, what they need, what success looks like for them]

## Market Opportunity
[What exists, what's missing, where we fit]

## Value Proposition
[Why someone would choose this — the core promise]

## Business Model
[How this makes money, who pays, rough economics]

## Success Metrics
[What we're measuring and what good looks like]

## Decisions Made
| # | Decision | Choice | Category |
|---|----------|--------|----------|
| 1 | Problem Definition | Option B: [Name] | Problem |
| 2 | Target User | Option A: [Name] | User |
| ... | ... | ... | ... |
| N | Elevator Pitch | Option [X]: [Name] | Strategy |

## Key Research Findings
- [Most important finding 1 — with source]
- [Most important finding 2 — with source]
- [Most important finding 3 — with source]

## Risks & Assumptions
- [Key assumption 1 that could be wrong]
- [Key risk 1 to watch for]
- [What we'd need to validate first]

## Decision History
All decision documents with research are saved in the `.decisions/` folder.
Open `.decisions/index.html` in your browser to review all decisions with visuals.
```

### Step 6b — Present the Brief and Ask About Next Steps

> "Strategy is locked in! Here's your strategy brief with the key decisions and research.
>
> I've saved everything to `.decisions/strategy-brief.md` and your full decision history is at `.decisions/index.html`.
>
> What's next?
> - **'Launch playbook'** — I'll run `/product-plan` to generate your complete launch roadmap — operations, partnerships, trust-building, and how the product should evolve
> - **'Plan the build'** — I'll run `/product-design` with this strategy to plan the technical implementation
> - **'Let me review first'** — Take a look at the brief and tell me if you want changes
> - **'Just the brief'** — We're done for now, you'll figure out next steps later"

Wait for the user's response and proceed accordingly. If they say "launch playbook", suggest running `/product-plan` which will automatically read the strategy brief and display the elevator pitch. If they say "plan the build", suggest running `/product-design`. The recommended pipeline is: product-strategy → product-plan → product-design.

---

**Decision page HTML:** read `references/templates.md` right before generating the first decision page — page structure, CSS, strategy-specific visual previews and comparison-table dimensions.

**Landing page:** the `.decisions/index.html` template is in `references/templates.md`.

## EDGE CASES

**User skips a decision:** "Skip this one" or "doesn't matter" → Set status to "chosen" with `chosenOption: "skip"`, `chosenTitle: "Skipped — AI will decide"`. Use your recommendation.

**User gives a custom answer not matching any option:** "Actually I want to go with a neighborhood co-op model" → Generate a full visual card for their answer with the same treatment as any AI-generated option (persona card, competitive map, revenue flow, whatever fits the decision type). Show it as the chosen option alongside the original options. Set `chosenOption: "custom"`, `chosenTitle: "[their description]"`. Store reasoning if they gave one.

**User wants to revisit the decision list:** "What decisions have we made?" → Open landing page: `open .decisions/index.html`

**User wants to jump ahead:** Reorder and present that decision next.

**Existing .decisions directory:** If `.decisions/` already exists, read `decisions.json` and resume from the first pending decision.

**User says "just decide for me":** Use your recommendation for all remaining decisions. Generate the strategy brief.

**User wants to go straight to building:** "I know the strategy, let's just build" → Suggest running product-design instead.

**Research turns up nothing useful:** Be honest: "I couldn't find strong data on this specific niche — these options are based on adjacent markets and general patterns. Take them as starting points rather than gospel."

---

## IMPORTANT REMINDERS

1. **Never skip the decision page.** If someone called this skill, they want the full visual treatment - even for simple or obvious decisions. Never say "that's straightforward, I'll just do it." Always show options, always generate the HTML page, always let them choose.
2. **Always 4 options.** Not 3, not 5. Exactly 4. Unless the user asks for more.
2. **Always include a recommendation.** Mark it with the amber badge. Explain WHY, grounded in research.
3. **Always research first.** Every decision must have a Research Context section with real findings from web searches. This is the core differentiator of Deep Plan Mode.
4. **Plain English everywhere.** No business jargon without explanation. "TAM (total addressable market — basically how many people could possibly use this)" is better than just "TAM."
5. **The comparison table is mandatory.** Every decision page must have one. Pick dimensions that help differentiate strategic options.
6. **Visual previews should make strategy tangible.** Persona cards for user decisions, competitive maps for market decisions, impact bars for problem decisions, revenue flows for business decisions, metric trees for strategy decisions.
7. **Open the HTML automatically.** Always run `open .decisions/decision-NNN-slug.html` after generating.
8. **Update the landing page after every change.**
9. **Self-contained HTML.** No external dependencies. Everything works by opening the file directly.
10. **Wait for the user.** After presenting a decision, STOP and wait.
11. **Ground options in research.** Don't just brainstorm — reference specific competitors, data points, and market realities in the option summaries and pro/con lists.
12. **Ask just enough questions.** 4-7 decisions for most ideas. Skip categories that don't apply. Don't interrogate.
13. **Connect to product-design.** At the end, suggest using product-design for the implementation decisions. The strategy brief is the input.
