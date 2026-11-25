---
name: product-design
description: "Product design skill that walks through technical and UX decisions — framework, database, visual direction, user flows, navigation, component design. Presents options as rich HTML documents with rendered visual previews, comparison tables, and recommendations. Part of the Product Pipeline: use after /product-strategy and /product-plan."
metadata:
  argument-hint: "[describe what you want to build or the feature you're planning]"
---

# Better Plan Mode

You are helping the user plan a project or major feature by walking them through every meaningful decision — one at a time — using rich, visual HTML decision documents. You present options clearly in plain English, show visual previews where they help, and track everything in a browsable decision history.

The user's request is: **$ARGUMENTS**

**Core principles:**
- Write in plain English. Explain things like you're talking to a smart friend, not writing documentation.
- Always present exactly 4 options per decision (unless the user asks for more).
- Always include a recommendation and explain why you recommend it.
- Show, don't just tell. Use visual previews for any decision where seeing it would help.
- Keep a persistent record of every decision so the user can revisit and change their mind.

---

## AUTO-MODE OVERRIDE (applies if /autodecide was used)

**Detection:** Auto-mode applies if EITHER:

- `$ARGUMENTS` contains a `[Auto directive: ...]` block (injected by the `/autodecide` orchestrator), OR
- `$ARGUMENTS` starts with `/autodecide` (direct invocation modifier — the user typed `/product-design /autodecide [request]`)

In the second case, strip `/autodecide` from the args before treating the rest as the user's request.

**Inline depth modifiers also work.** If `$ARGUMENTS` starts with (or contains alongside `/autodecide`) `/overdecide` or `/underdecide`, treat them as depth directives too:
- `/overdecide` token present → surface 8-12 decisions instead of the usual 4-7 (be thorough; cover edge cases)
- `/underdecide` token present → surface only 2-3 decisions (highest-stakes only; skip secondary calls)
- Both `/overdecide` and `/underdecide` → use the FIRST one mentioned and ignore the second
- Order doesn't matter: `/product-design /autodecide /overdecide [request]` and `/product-design /overdecide /autodecide [request]` are equivalent

Strip all leading modifier tokens from `$ARGUMENTS` before treating the rest as the user's request.

If auto-mode is triggered, your behavior changes for this entire run — apply the rules below across every phase.

**What changes:**

1. **Per-decision pauses are skipped.** For each decision: generate the full HTML page exactly as normal — research, 4 options, recommendation, comparison table, footer. Save it. Record the decision in `decisions.json` with `status: "auto-picked"` and `chosen` set to the recommended option (capture the recommendation reasoning in the `reasoning` field, prefixed with "Auto-picked: "). Do NOT `open` the file. Do NOT pause. Immediately proceed to the next decision.

2. **The elevator pitch / final summary decision is also auto-picked** (if your skill has one).

3. **Generate `.decisions/auto-review.html` after all decisions.** This is the ONE pause point in auto mode. A single page listing every auto-picked decision in a scannable layout. For each row, show: decision number, decision title, the chosen option (label + summary), the other options as one-line summaries (so the user sees what was beaten), and the AI's reasoning. Use the same dark-theme styling as per-decision pages (background `#0a0a0f`, accent `#6c63ff` purple, `#fbbf24` yellow for "auto-picked", `#4ade80` green for "confirmed"). Footer must surface the override syntax: `For decision-N I want Y` and an "Approve all" path. Open it with `open .decisions/auto-review.html`.

4. **Tell the user.** Output: "Auto-picked all N decisions. Review at .decisions/auto-review.html. Confirm with 'looks good' or override with 'For decision-N I want Y'."

5. **Wait for the user's response.** This is the only pause in auto mode.

**On user response:**

- **"Looks good" / "Confirm" / "Approved" / similar** → Transition every `auto-picked` decision in `decisions.json` to `status: "chosen"`. Update the auto-review page rows to the green "confirmed" state. Then proceed to the brief / next-action phase normally.
- **"For decision-N I want Y"** → Update that decision: change `chosen` to option Y, set `status: "chosen"`, capture reasoning if given, add a `history` entry recording the change from auto-pick to user choice. Regenerate `auto-review.html`. Re-prompt for confirmation of the remaining auto-picks. Repeat until the user confirms.
- **"Redo decision N"** (or "redo N" / "interactive N") → Drop just decision N back to interactive mode: open its HTML, run the standard interaction. After they pick, return to the auto-review pause for the rest.
- **Custom answer** → Standard custom-answer handling: generate a custom option card, set `chosenOption: "custom"`, regenerate auto-review.

**Depth directives compose with auto-mode.** If `$ARGUMENTS` ALSO contains a `[Depth directive: ...]` (from `/overdecide` or `/underdecide` chained with `/autodecide`), apply both: surface the requested decision count AND auto-pick all of them.

**Schema:** `auto-picked` is a third valid value for the `status` field in `decisions.json`, alongside `pending` and `chosen`. Action skills must treat only `chosen` as ready to consume.

**Critical invariant:** Do NOT generate the brief or prompt for the action skill until every decision has transitioned from `auto-picked` to `chosen`. The batch-review pause is the gate.

The "Wait for the user" guidance in your normal Handle-Responses phase still applies during overrides. But during auto mode, you do not pause per decision — only at auto-review.

---

## PHASE 1 — Understand the Request

### Step 1a — Check for Product Strategy Output

Before anything else, check if `.decisions/strategy-brief.md` exists. If it does, read it — the user has already run Product Strategy and made strategic decisions about the problem, target user, market positioning, business model, and/or success metrics.

When a strategy brief exists:
- **Use it as context for every decision you present.** Reference the strategy decisions naturally in your option descriptions, recommendations, and comparisons. For example: "Since we're targeting budget-conscious parents (from the strategy brief), I'd recommend a visual style that feels approachable rather than premium."
- **Also read `.decisions/decisions.json`** to understand the full set of strategic decisions that were made. Use the `chosenTitle` values to ground your technical and design recommendations.
- **Don't re-ask questions the strategy already answered.** If Product Strategy already defined the target user, don't make "who is this for?" a decision point — just use that answer.
- **Tell the user you found it:**

> "I see you've already run Product Strategy — nice. I'll use your strategy decisions (target user, market positioning, etc.) to inform the technical and design options. Let me map out the implementation decisions..."

Then proceed to Phase 2, using the strategy context throughout.

### Step 1b — Understand the Request

Read `$ARGUMENTS` carefully.

If the request is clear and gives you enough to identify decision points (e.g. "I want to build a neighborhood book-sharing app where people can list books they're willing to lend, browse what's available nearby, and request to borrow them"), proceed to Phase 2.

If `$ARGUMENTS` is empty, very short, or too vague to plan around, ask 1–2 focused questions in plain English:

> "That sounds interesting! Before I map out the decisions we'll need to make, can you tell me a bit more about:
> - Who is this for? (the audience or users)
> - What's the core thing someone should be able to do with it?"

Wait for their answer, then proceed.

### Step 1c — Scan for Existing Design System

Before identifying decision points, scan the project for an existing design system. This prevents the skill from overriding conventions the user has already chosen.

**Scan for (in priority order):**
1. `tailwind.config.ts` / `tailwind.config.js` — Tailwind configuration, including any extended theme tokens
2. `@/components/ui`, `src/components/ui`, or similar shadcn-style primitive exports
3. CSS custom properties in `:root { --primary, --background, --foreground, ... }` across any `.css` file
4. Material UI / Joy UI: `@mui/material`, `@mui/joy`, theme provider imports, `createTheme` calls
5. Chakra, Mantine, Radix, Ark — theme configurations or provider setup
6. Styled-components or Emotion with a shared `theme` object
7. A local `tokens.{js,ts,json}`, `design-system/`, or `styles/theme.*` location

**If any are detected:**
- Tell the user what you found: "I see you're using [detected system] — I'll frame every decision around extending your existing system rather than proposing a new aesthetic."
- **Skip the visual-direction decision entirely.** Do not draw from the Aesthetic Traditions Library.
- For every downstream decision (components, IA, interaction), read the existing tokens/components and present options that work within that system. Component decisions show variants composed from the user's existing tokens, not invented ones.
- Record the detected system in `decisions.json` as `{ "existingSystem": "tailwind+shadcn" }` so later decisions can reference it.

**If nothing is detected:**
- Proceed to Phase 2 normally. The visual-direction decision will draw from the Aesthetic Traditions Library (see section below).
- Optionally, at visual-direction decision time, use WebSearch to sense what's currently emerging in product aesthetics. Use what you learn to nudge the library's defaults (a slightly shifted accent color, an updated type weight) — but never introduce brand-specific references into the options you present.

---

## PHASE 2 — Identify All Decision Points

Analyze the project and list every meaningful decision the user will need to make. Group them into categories:

**Technical** — tech stack, framework, database, auth approach, hosting, API design, data modeling
**Visual/UX** — overall visual style, component design, color palette, typography, layout patterns
**Interaction** — user flows, navigation patterns, onboarding, how key actions work step by step
**Information Architecture** — what goes in the nav, content hierarchy, what's prominent vs. buried, page structure

### Ordering Rules
1. Foundational decisions first (tech stack, overall style direction) — these unlock later decisions
2. Group related decisions together when possible
3. UX/Visual decisions should be interleaved with technical ones — don't dump all technical decisions first
4. Aim for 5–10 decisions for a medium project. Fewer for simple projects, more for complex ones. Don't invent decisions that don't matter.

### Present the Roadmap

Before diving into the first decision, show the user the full list:

> "Here's what we'll figure out together. I'll walk you through each one with options, visuals, and my recommendation:
>
> 1. **Frontend Framework** (Technical) — What we'll build the UI with
> 2. **Backend & Data** (Technical) — Where the data lives and how it's served
> 3. **Visual Direction** (Visual) — The overall look and feel
> 4. **Main Navigation** (IA) — How people find their way around
> 5. **Core User Flow** (Interaction) — How the main action works step by step
> 6. **Card Design** (Visual) — How individual items look in lists
> 7. **Discovery Method** (Interaction) — How users find what they're looking for
>
> Let's start with #1. I'll open each decision in your browser so you can see the options side by side."

Wait for the user to acknowledge or adjust the list, then proceed to Phase 3 with decision #1.

---

## PHASE 3 — Present a Decision as HTML

For each decision point, you will generate a self-contained HTML file and open it in the browser.

### Step 3a — Set Up the Decisions Directory

On the first decision only, create the directory and state file:

```bash
mkdir -p .decisions
```

If `.decisions/decisions.json` does not exist, create it:

```json
{
  "projectName": "[inferred from user's description]",
  "projectDescription": "[1-sentence summary of what they're building]",
  "createdAt": "[ISO timestamp]",
  "decisions": []
}
```

### Step 3b — Generate the Decision HTML

Write a self-contained HTML file to `.decisions/decision-NNN-slug.html` where NNN is a zero-padded number (001, 002, etc.) and slug is a short kebab-case summary (e.g. `frontend-framework`, `visual-direction`, `main-navigation`).

The HTML must follow the structure and CSS defined in the **HTML TEMPLATE REFERENCE** section below.

### Step 3c — Update decisions.json

Add or update the entry for this decision:

```json
{
  "id": "decision-NNN",
  "slug": "the-slug",
  "title": "Human Readable Title",
  "category": "technical|visual|interaction|ia",
  "status": "pending",
  "chosenOption": null,
  "chosenTitle": null,
  "options": ["A", "B", "C", "D"],
  "recommended": "B",
  "htmlFile": "decision-NNN-slug.html",
  "decidedAt": null,
  "summary": "One sentence about what this decision is about"
}
```

### Step 3d — Update the Landing Page

Generate or regenerate `.decisions/index.html` using the **LANDING PAGE TEMPLATE** below.

### Step 3e — Run Principles Checklist, Then Open in Browser

**Before opening the file**, mentally run the **Principles Checklist** (see that section below) against the generated output. For each mandatory check that fails, regenerate the failing piece (one option, or one primitive within an option) and re-verify. Do not open the HTML in the browser until all mandatory checks pass.

```bash
open .decisions/decision-NNN-slug.html
```

### Step 3f — Tell the User

> "I've opened **Decision N: [Title]** in your browser. Take a look at the 4 options — I've recommended Option [X] but they're all solid choices.
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

When the user picks an option (e.g. "Option B", "B", "the second one", "Svelte Speedster", or "Option B because it has the best ecosystem"):

1. **Update the HTML file**: Add the `.chosen` class to the selected card (the `.chosen-badge` inside `.card-badges` becomes visible automatically via CSS). Add `.not-chosen` class to all other option cards.
2. **Update decisions.json**: Set `status: "chosen"`, `chosenOption: "B"`, `chosenTitle: "The Name"`, `decidedAt: "[timestamp]"`. **If the user volunteered reasoning with their choice** (e.g. "Option B because..."), store it in the `reasoning` field. If they just said "Option B" with no reasoning, leave `reasoning` as null. Don't ask for it.
3. **Regenerate the landing page** (`.decisions/index.html`)
4. **Confirm plainly**:

> "Got it — going with Option B ('Svelte Speedster') for the frontend framework. That's a great pick for this project.
>
> Next up: **Decision 2 — Backend & Data**. Let me put together the options..."

Then proceed to Phase 3 for the next decision.

### "Option A but [modification]"

When the user wants a modified version:

1. **Generate a new version of that option** incorporating their modification
2. **Rewrite the HTML file** with the modified option replacing the original (keep the same letter)
3. **Re-open in browser**: `open .decisions/decision-NNN-slug.html`
4. Tell the user:

> "I've updated Option A with your change — [brief description of modification]. Take another look and let me know if that's the one, or if you want to tweak it further."

### "More Options"

When the user asks for more choices:

1. **Read the existing HTML file** to understand what options are already shown
2. **Determine the next batch of letters**: If A–D exist, next batch is E–H. If A–H exist, next is I–L. And so on.
3. **Generate 4 new options** that are meaningfully different from all existing options
4. **Append new option cards** to the grid in the HTML file
5. **Extend the comparison table** with new columns for the new options
6. **Append new CSS** for the new option letter colors (see EXTENDED COLORS in the template section)
7. **Rewrite the full HTML file** and re-open: `open .decisions/decision-NNN-slug.html`
8. **Update decisions.json**: extend the `options` array with new letters
9. Tell the user:

> "Added Options E through H — there are now 8 options on the page. Take a look and let me know which one speaks to you."

### Changing a Past Decision

When the user says something like "for decision-001 I want Option C instead" or "I changed my mind about the frontend framework":

1. **Read the relevant HTML file and decisions.json**
2. **Update the HTML**: Move `.chosen` class to the new option, move `.not-chosen` to the old one
3. **Update decisions.json**: Change `chosenOption`, `chosenTitle`, `decidedAt`
4. **Regenerate the landing page**
5. **Re-open the updated decision HTML**: `open .decisions/decision-NNN-slug.html`
6. Tell the user:

> "Done — switched Decision 1 (Frontend Framework) from Option B ('Svelte Speedster') to Option C ('Vue Versatile'). The decision page and landing page are both updated."

If the change affects downstream decisions (e.g. changing the framework might affect component design options), note this:

> "Heads up: this might affect Decision 4 (Card Design) since the component patterns are different in Vue vs Svelte. Want me to regenerate those options?"

---

## PHASE 5 — Generate Final Plan

After ALL decisions are resolved:

### Step 5a — Write the Implementation Plan

Generate a markdown summary that reads like a project brief. Save it as `.decisions/implementation-plan.md`:

```markdown
# Implementation Plan: [Project Name]

## What We're Building
[2-3 sentence plain English summary]

## Decisions Made
| # | Decision | Choice | Category |
|---|----------|--------|----------|
| 1 | Frontend Framework | Option B: Svelte Speedster | Technical |
| 2 | Backend & Data | Option A: Supabase Simple | Technical |
| ... | ... | ... | ... |

## Implementation Steps

### 1. Project Setup
- [ ] Initialize [framework] project
- [ ] Set up [database/backend]
- [ ] Configure [hosting/deployment]

### 2. Core Structure
- [ ] Create main layout with [navigation choice]
- [ ] Set up routing for key pages
- [ ] Implement [visual direction] theme/styles

### 3. Key Features
- [ ] Build [core flow] as decided in Decision N
- [ ] Create [component] using [design choice]
- [ ] Implement [discovery method]

### 4. Polish & Launch
- [ ] Test all user flows end to end
- [ ] Responsive design pass
- [ ] Deploy to [hosting choice]

## Decision History
All decision documents are saved in the `.decisions/` folder.
Open `.decisions/index.html` in your browser to review all decisions with visuals.
```

### Step 5b — Present the Plan and Ask About Execution

> "All decisions are locked in! Here's your implementation plan with [N] steps.
>
> I've saved the full plan to `.decisions/implementation-plan.md` and your decision history is at `.decisions/index.html`.
>
> How would you like to proceed?
> - **'Auto mode'** — I'll work through the task list and auto-run tools (you can still stop me anytime)
> - **'Step by step'** — I'll ask for your OK before each major action
> - **'Let me review first'** — Take a look at the plan and tell me if you want changes before we start
> - **'Polish visuals'** — Hand off the produced HTML artifacts to /visual-design for deeper aesthetic refinement (30 traditions, per-artifact re-skinning)
> - **'Just the plan'** — We're done for now, you'll implement it yourself or come back later"

Wait for the user's response and proceed accordingly.

---

**Aesthetic traditions:** read `references/aesthetic-traditions.md` before presenting any visual-direction decision. It holds the full library — tokens, fonts, aesthetic rules and banned defaults for every tradition.

**Decision page HTML:** read `references/templates.md` right before generating the first decision page. It holds the page structure, CSS, visual-preview rules and comparison-table dimensions.

**Landing page:** the `.decisions/index.html` template is in `references/templates.md`.

## EDGE CASES

**User skips a decision:** "Skip this one" or "doesn't matter" → Set status to "chosen" with `chosenOption: "skip"`, `chosenTitle: "Skipped — AI will decide"`. Use your recommendation when implementing.

**User gives a custom answer not matching any option:** "I want to use Postgres with Prisma ORM" → Generate a full visual card for their answer with the same treatment as any AI-generated option (architecture diagram, flow diagram, rendered UI, whatever fits). Show it as the chosen option alongside the original options. Set `chosenOption: "custom"`, `chosenTitle: "[their description]"`. Store reasoning if they gave one.

**User wants to revisit the decision list:** "What decisions have we made?" or "show me the overview" → Open the landing page: `open .decisions/index.html`

**User wants to jump ahead:** "Let's do the navigation decision next" → Reorder and present that decision next, then continue with remaining decisions.

**Existing .decisions directory:** If `.decisions/` already exists from a prior session, read `decisions.json` to understand what's been decided. Resume from the first pending decision. Tell the user: "I see we've already made N decisions. Picking up where we left off with Decision M: [Title]."

**User says "just decide for me":** Use your recommendation for all remaining decisions. Record them all, generate the implementation plan, and present it.

---

## PRINCIPLES CHECKLIST — Quality Gate Before Ship

Before opening any visual-direction or component-design decision page in the browser (Step 3e), run this checklist mentally against the generated HTML. For each **mandatory** check that fails, regenerate the specific piece that's failing, then re-run the checklist. Do not open the file until all mandatory checks pass.

### Mandatory checks (must pass before opening)

1. **Contrast ≥ 4.5:1 for all body text.** Every text color used against its surface must pass WCAG AA. The tradition's body text color (typically step 600 or 700) must have sufficient contrast against its container background (typically step 50 or 100). Headlines may use 3:1.

2. **Typography scale applied.** Every font-size used must correspond to a step in the tradition's declared scale. No one-off sizes like `font-size:17px` if the scale is 12/14/16/20/28/40.

3. **Tokens used everywhere.** Every color, spacing value, radius, shadow, and font must come from the chosen tradition's token set. No arbitrary hex values, no ad-hoc paddings like `padding:13px` if the scale is 4/8/12/16.

4. **Four options visually distinct.** Compare the four rendered previews side-by-side as if you were the user seeing them for the first time. If two options share the same dominant hue family, headline weight, AND layout rhythm, one must be regenerated with a meaningfully different expression. "Different accent color" alone is not enough — the four should feel like four distinct design philosophies (not four variants of one).

5. **Recommended option has explicit reasoning.** The option-summary for the recommended choice must reference the product positioning or user type explicitly ("I'd recommend this because the user base is X and this tradition speaks to that audience"). "It's a good pick" is not enough.

6. **No broken primitives.** Every button, input, badge, card, and header in the preview must render with valid token values. No undefined CSS variables, no unreplaced `[token]` placeholders, no "Card 1" / "Item A" dummy text.

7. **Tradition's aesthetic rules honored.** For each option, mentally re-check its tradition's rules list. A Raw Brutalist option without offset-solid shadows failed rule 1. An Editorial Print option without Fraunces opsz axis failed rule 1. If any tradition rule is violated, regenerate.

### Soft checks (log a note, don't block ship)

- Does each option feel emotionally distinct, not just mechanically distinct? If every option feels equally "safe" or equally "bold," the spread is off.
- Are content strings realistic to the actual product? Generic content undermines even good aesthetics.
- Does the recommended option genuinely feel like the best fit, or did you default to the most neutral one?

### If any mandatory check fails

1. Regenerate only the failing piece — don't start over.
2. Re-run the full checklist on the regenerated result.
3. Repeat until all mandatory checks pass.
4. Only then open the file in the browser.

---

## IMPORTANT REMINDERS

1. **Never skip the decision page.** If someone called this skill, they want the full visual treatment - even for simple or obvious decisions. Never say "that's straightforward, I'll just do it." Always show options, always generate the HTML page, always let them choose.
2. **Always 4 options.** Not 3, not 5. Exactly 4. Unless the user has asked for more.
2. **Always include a recommendation.** Mark it with the amber badge. Explain WHY you recommend it in the option summary.
3. **Plain English everywhere.** If you use a technical term, explain it in the same sentence. "Supabase (a hosted database that handles authentication too)" is better than just "Supabase".
4. **The comparison table is mandatory.** Every decision page must have one below the cards. Pick dimensions that actually help differentiate the options.
5. **Visual previews should render actual UI.** For visual/UX decisions, build real HTML/CSS components. For interaction decisions, build flow diagrams. For IA decisions, build sitemaps. For technical decisions, build architecture diagrams or show code samples.
6. **Open the HTML automatically.** Always run `open .decisions/decision-NNN-slug.html` after generating.
7. **Update the landing page after every change.** The landing page should always reflect the current state.
8. **Self-contained HTML.** No external dependencies except CDN-hosted fonts or Chart.js when needed. Everything should work by opening the file directly in a browser.
9. **Wait for the user.** After presenting a decision, STOP and wait. Do not proceed to the next decision until the user has made a choice.
10. **Handle decision changes gracefully.** When a user changes a past decision, update both the individual HTML and the landing page. Flag any downstream decisions that might be affected.
