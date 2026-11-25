---
name: deck-pipeline
description: Multi-agent pipeline that builds a polished presentation deck from a single topic. Four agents work in sequence — Strategist defines the narrative, Builder creates the deck, Critic reviews it like a McKinsey EM, Fixer applies the top fixes. Use when you need a presentation that survives senior audiences.
---

# Deck Pipeline

A 4-agent pipeline that transforms a topic into a critique-proof presentation deck. Each agent has a distinct role — the output of one feeds the next. The result is a deck that has been strategically structured, built, reviewed, and fixed before you ever touch it.

## The Four Agents

```
Topic
  │
  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ STRATEGIST  │───▶│   BUILDER   │───▶│   CRITIC    │───▶│    FIXER    │
│             │    │             │    │             │    │             │
│ Defines the │    │ Creates the │    │ Reviews like│    │ Applies the │
│ narrative   │    │ actual deck │    │ a McKinsey  │    │ top 3 fixes │
│ and outline │    │             │    │ EM at 2am   │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Agent 1: Strategist

**Role:** Define the audience, governing thought, and full slide outline before anything gets built.

**What it does:**
- Identifies the target audience and what they care about
- Defines the governing thought (the one sentence the whole deck proves)
- Creates a 10-12 slide outline using Situation → Complication → Resolution structure
- Each slide title is a **claim**, not a label ("RTD market will reach $42.5B by 2028" not "Market Overview")
- Groups slides into clear narrative blocks

**Output:** A structured outline with:
- Audience definition
- Governing thought
- Slide-by-slide titles with supporting points
- Narrative flow markers (Situation / Complication / Resolution)

**Why this matters:** A deck without a strategy is just a collection of slides. The strategist ensures every slide earns its place in the argument.

---

## Agent 2: Builder

**Role:** Convert the strategist's outline into an actual presentation.

**What it does:**
- Takes the outline and creates the full deck content
- Writes slide body text, data points, and supporting evidence
- Structures visual elements: comparison tables, stat callout boxes, framework diagrams
- Maintains consistent formatting and tone throughout
- Ensures each slide has a clear "so what"

**Output:** A complete deck as a native `.pptx` (via python-pptx) with editable text and editable charts. Optional: markdown or formatted text as an intermediate artifact for review.

- Claim-based titles on every slide
- Data points with sources where available
- Visual structure suggestions (tables, callout boxes, charts)
- Section transitions between narrative blocks

**Tools the Builder uses:**
- **[mckinsey-charts](../mckinsey-charts/SKILL.md)** for native editable charts — bar+callout for single-number stories, stacked column for mix over time, waterfall for bridges. The audience can right-click → Edit Data inside PowerPoint. Use this instead of pasting chart images.
- **python-pptx** for native text, tables, and layout. No screenshots, no image-based content — everything stays editable.

**Tips for the Builder:**
- Stat callout boxes work well for key numbers (large font, contrasting color)
- Comparison tables > bullet lists when presenting options
- Keep body text to 3-5 points per slide maximum
- Every data slide needs at least one source
- Every quantitative slide uses a chart from `mckinsey-charts`, not a screenshot

---

## Agent 3: Critic

**Role:** Review the deck like a senior engagement manager would — find every structural problem, weak argument, and missing element.

**What it does:**
- Grades the overall deck (Green / Yellow / Red)
- Reviews each slide with a status and specific issue
- Identifies the **top 3 fixes** ranked by impact
- Calls out one thing that works (to protect it)

**Grading:**
| Grade | Meaning |
|-------|---------|
| Green | Ready for stakeholders |
| Yellow | Fixable overnight, do not send as-is |
| Red | Core argument broken, needs rework |

**What it checks:**
- Narrative flow and structure
- Data rigor (sources, specificity, comparisons)
- "So what" on every slide
- Financial framing where needed
- Claim-based titles vs topic titles
- Frameworks vs bullet lists

**Output:** A critique document with section-by-section grades and top 3 prioritized fixes.

> See the [McKinsey Critic](../mckinsey-critic/SKILL.md) skill for the full review framework.

---

## Agent 4: Fixer

**Role:** Apply the critic's top 3 fixes to produce the final deck.

**What it does:**
- Takes the critic's specific fix instructions
- Applies each fix to the deck
- Documents what changed and why
- Produces the final, polished version

**Common fixes the Fixer applies:**
- Adding source footnotes to data slides
- Rebuilding bullet lists as comparison tables (columns = options, rows = evaluation dimensions)
- Adding financial frames (market size × share = revenue, margin analysis, investment required)
- Sharpening headlines from descriptions to claims
- Naming competitors instead of describing them generically
- Linking disconnected slides back to the core argument

**Output:** The final deck with all fixes applied, plus a change log showing before → after for each fix.

---

## How to Use

### Quick Start
```
"Build me a deck on [topic] for [audience]. Use the full pipeline — 
strategist, builder, critic, fixer."
```

### With More Context
```
"I need a deck for [audience] arguing that [governing thought].

Key data points I have: [list any data, stats, or sources you want included]

Run the full pipeline: outline it, build it, critique it, fix it."
```

### Step by Step (if you want control between stages)
```
Step 1: "Act as the strategist. Define the audience, governing thought, 
        and 10-slide outline for [topic]."

Step 2: "Now act as the builder. Turn this outline into a full deck."

Step 3: "Now act as the McKinsey critic. Grade this deck and give me 
        the top 3 fixes."

Step 4: "Now act as the fixer. Apply the top 3 fixes."
```

---

## Example: What Each Agent Produces

**Topic:** "Should a premium coffee company enter the RTD (Ready-to-Drink) market?"

**Strategist output:**
- Audience: Board of directors + CEO
- Governing thought: "The premium RTD market offers a $425M revenue opportunity that plays to our existing capabilities — but only if we move within 12 months."
- 10 slides: 3 Situation (market size, specialty growth, RTD growth) → 3 Complication (consumer shift, competition, first-mover window) → 4 Resolution (path comparison, RTD recommendation, sustainability, roadmap)

**Builder output:** Full deck with data, stat callouts, comparison tables

**Critic output:**
- Grade: YELLOW
- Fix 1: Cite every number (no source footnotes on any slide)
- Fix 2: Slide 7 is a bullet list — needs comparison table (3 paths × 5 dimensions)
- Fix 3: No financial frame — add $425M revenue at 1% share, $15-25M Phase 1 investment

**Fixer output:** Final deck with all sources added, comparison table rebuilt, financial frame on recommendation slide

---

## When to Use

- Board presentations and investor updates
- Strategy recommendations to leadership
- Product launch proposals
- Market entry analysis
- Any deck that needs to survive tough questions

## What replaced the old Gamma path

Earlier versions of this repo paired the storyline with the Gamma API to generate finished decks. The current version uses **native python-pptx + the [mckinsey-charts](../mckinsey-charts/SKILL.md) skill** instead. Reasons:

- **Editable, not generated.** Charts are real PowerPoint chart objects, not images. The audience can change colors, edit data, copy to their own deck.
- **No third-party dependency.** No Gamma account, no API key, no per-deck credit cost.
- **Better defaults.** Single highlight color, no gridlines, claim-shaped titles — already wired into mckinsey-charts. The Gamma path required prompt-engineering the look every time.

The `gamma-automation/` folder is preserved for reference but is deprecated.

## Why a Pipeline Instead of One Prompt

A single "build me a deck" prompt produces mediocre work because it tries to think strategically AND write content AND self-critique simultaneously. By separating the roles:

- The **strategist** focuses purely on narrative architecture
- The **builder** focuses on content and visuals, with a clear brief
- The **critic** is adversarial — it's not trying to protect what was built
- The **fixer** has specific, prioritized instructions — not vague "make it better"

The result is a deck that has been through the equivalent of a junior consultant → senior associate → engagement manager review cycle.
