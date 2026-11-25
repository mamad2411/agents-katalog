---
name: Flow Discovery
slug: flow
description: Interactive interview to map and document user flows before building. Two modes — inventory (Stage 3) and deep-dive (Stage 5+).
category: development
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "flow"
  - "flow discovery"
  - "flow inventory"
  - "flow deep-dive"
  - "map flows"
  - "user flow"
  - "flow interview"
tags:
  - flow
  - ux
  - planning
  - pipeline
  - interview
---

# Flow Discovery


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

Interactive interview system that maps user flows BEFORE building features. This skill enforces the rule: **no feature gets built without a signed-off flow spec.**

Two modes serve two pipeline stages:

| Mode | Pipeline Stage | Purpose | Output |
|------|---------------|---------|--------|
| **Inventory** | Stage 3 (Architecture) | Map ALL flows in the product | Flow inventory doc + HTML flow map |
| **Deep Dive** | Stage 5+ (Feature Blocks) | Detail ONE flow before building it | Flow spec + HTML flow diagram |

## CRITICAL RULES

1. **NEVER skip the interview.** Do not fill in flow details from assumptions or inference. Every field comes from Eddie's answers.
2. **Use AskUserQuestion for structured choices.** Use natural conversation for open-ended descriptions.
3. **Generate BOTH outputs.** Every run produces a markdown doc AND an HTML visualization.
4. **Stop building if a flow is missing.** If you're about to implement a feature and realize no flow spec exists, run `/flow deep-dive` FIRST.

---

## Mode 1: Flow Inventory (Stage 3)

**When:** Starting a new project or entering Stage 3 (Architecture Sketch).
**Goal:** Identify every user flow in the product and how they connect.
**Duration:** 15-30 minute interview.

### Interview Process

**Step 1 — Identify User Types**

Ask Eddie using AskUserQuestion:
- "Who are the different types of users in this product?"
- For each type: what's their primary goal?

**Step 2 — Map Entry Points**

Ask Eddie:
- "How do users first encounter this product?" (direct URL, invite, signup, OAuth, etc.)
- "Are there different entry points for different user types?"

**Step 3 — List Every Flow**

Walk through the product systematically. For each area, ask:
- "What can the user DO here? Walk me through every action."
- "What happens when they complete that action?"
- "Where do they go next?"

Cover these categories (adapt to the product):
- [ ] Authentication (signup, login, logout, password reset, OAuth)
- [ ] Onboarding (first-time setup, profile, preferences)
- [ ] Core Features (the main value proposition — usually 2-5 flows)
- [ ] Settings & Profile (account management, preferences, billing)
- [ ] Navigation (how users move between areas)
- [ ] Error Recovery (what happens when things go wrong)
- [ ] Admin/Management (if applicable — roles, permissions, moderation)

**Step 4 — Prioritize**

Ask Eddie using AskUserQuestion:
- For each flow: "Is this Critical (V1), Secondary (V1 if time), or Deferred (post-V1)?"

**Step 5 — Map Connections**

Ask Eddie:
- "After completing [Flow A], where does the user typically go next?"
- "Can the user reach [Flow C] without going through [Flow B] first?"
- Build the connection map.

### Output Generation

1. **Markdown:** Fill in `prep-templates/flow-discovery.md` and save to `workspace/prep/flow-discovery.md`
2. **HTML:** Generate an interactive flow map using `/visualize` and save to `~/Development/artifacts/[project]/flow-map.html`
3. **Report:** Summarize the inventory — total flows, critical count, deferred count, any gaps identified

---

## Mode 2: Deep Dive (Stage 5+)

**When:** About to build a specific feature. MUST happen before any code for that feature.
**Goal:** Document every detail of ONE user flow so it can be built exactly right.
**Duration:** 10-20 minutes per flow (complex flows may take longer).

### Interview Process

Run through all 9 categories below. For each, use AskUserQuestion for structured choices and conversation for open-ended descriptions.

**Category 1: Context**

- "What is this flow in one sentence?"
- "Who triggers it and under what circumstances?"
- "Why does this flow exist — what problem does it solve?"
- "Which other flows does this connect to?"

**Category 2: Entry Conditions**

- "How does the user arrive at this flow? List every path."
- "What state is the user in when they enter?" (auth status, existing data, mental state)
- "Are there any prerequisites — things that must be true before this flow starts?"

**Category 3: Steps (THE CORE — spend the most time here)**

For each step in the flow, ask:
- "What does the user SEE on this screen? Describe the layout and key elements."
- "What can the user DO here? List every possible action."
- "For each action, what HAPPENS? Where do they go next?"
- "Is there any validation? What are the field requirements and error messages?"
- "Can the user go back? Skip? Leave and return?"

Keep asking "and then what?" until Eddie says the flow is complete.

Use AskUserQuestion to confirm branching:
- "When the user does [X], do they go to [A] or [B]?"
- "Is [this step] required or optional?"

**Category 4: States**

Ask about each state explicitly:
- **Empty:** "What does this screen look like when there's NO data yet?"
- **Loading:** "What does the user see while data loads? How long should they wait?"
- **Error:** "What are the specific things that can go wrong? For each, what message do we show and how do they recover?"
- **Success:** "What does completion look like? Is there a confirmation? A celebration?"
- **Partial:** "If the user leaves mid-flow and comes back, what do they see?"

**Category 5: Decision Points**

- "Are there any steps where the user has to CHOOSE between options?"
- For each: "What are the options? Which do we recommend? How does the choice affect what happens next?"

**Category 6: Permissions**

- "Who can access this flow? Are there different roles?"
- "What happens if someone WITHOUT access tries to reach this flow?"
- "Are any steps restricted to certain roles?"

**Category 7: Edge Cases**

Walk through each explicitly:
- "What if the user hits the browser back button mid-flow?"
- "What if they open this in two tabs?"
- "What if the network drops during submission?"
- "What if they're on 3G?"
- "What if their session expires mid-flow?"
- "What if another user is editing the same thing?"

**Category 8: Responsive**

- "Any differences on mobile vs desktop?"
- "Are there touch-specific interactions? Swipes? Long press?"
- "Should anything be hidden or rearranged on smaller screens?"

**Category 9: Exit**

- "Where does the user go after this flow completes?"
- "Is progress saved if they abandon mid-flow?"
- "Can they undo the result of this flow? If so, how and for how long?"

### Output Generation

1. **Markdown:** Fill in `doc-templates/flow-spec.md` and save to `workspace/prep/flows/flow-[slug].md`
2. **HTML:** Generate a step-by-step flow diagram using `/visualize` and save to `~/Development/artifacts/[project]/flow-[slug].html`
3. **Checklist:** Confirm all sections are filled — flag any gaps for follow-up

---

## Quick Reference

| Command | Action |
|---------|--------|
| `/flow` | Choose between inventory and deep-dive mode |
| `/flow inventory` | Run Stage 3 flow inventory interview |
| `/flow deep-dive` | Run Stage 5+ per-feature flow interview |
| `/flow check` | Audit current project — which flows have specs, which don't |
| `/flow list` | Show all documented flows for current project |

## Pipeline Integration

### Stage 3 Gate Addition
Flow inventory MUST exist before passing Stage 3. Checkpoint question:
> "Are all user flows identified and mapped?"

### Stage 5 Gate Addition
Each feature MUST have a flow spec before building. Checkpoint:
> "Does this feature have an approved flow spec?"

### Stage 8 Gate Addition
All flow specs MUST match the built implementation. Checkpoint:
> "Do the actual flows match the documented flow specs?"

## Red Flags (Stop and Interview)

- You're about to build a multi-step user interaction with no flow spec
- You're making assumptions about what happens after a user action
- You're designing error states, empty states, or loading states without asking
- You're writing onboarding, signup, or checkout code without a spec
- You realize mid-build that you don't know what happens on mobile
- Two features need to connect but there's no documented handoff

## Anti-Patterns

- **DO NOT** fill in flow details from engineering assumptions
- **DO NOT** skip the interview because "it's obvious"
- **DO NOT** combine multiple flows into one spec (one flow = one spec)
- **DO NOT** build first and document later
- **DO NOT** approve your own flow specs — Eddie must sign off
