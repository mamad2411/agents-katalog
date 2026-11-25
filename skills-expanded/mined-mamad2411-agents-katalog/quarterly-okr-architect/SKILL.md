---
name: quarterly-okr-architect
description: Build rigorous, emotionally resonant quarterly or annual goal architectures for business unit, marketing, or executive-facing plans by fusing four frameworks — 4DX (lead measures, scoreboard, accountability cadence), MASTER Goals (specificity, trackability, reward), DUMB Goals (dream-driven, uplifting emotional framing), and Backward Goal Setting (end-state-to-milestone-to-action cascade). Use this skill whenever the user wants to set, structure, refine, or present quarterly/annual goals, OKRs, BU targets, GTM targets, or strategic objectives — especially for CEO, Business Unit Manager, or board-facing material. Trigger on phrases like "set goals for", "build OKRs", "quarterly targets", "build a goal cascade", "backward planning from [end goal]", "lead measures for", or "turn this objective into a plan." Do NOT use for personal life-balance self-assessment (see life-wheel-assessment) or for routine project task lists with no strategic framing.
---

# Quarterly OKR Architect

A composite goal-architecture skill. It does not implement any one framework alone — it fuses four into a single output, because each framework alone has a documented weakness:

| Framework alone | What it's missing |
|---|---|
| 4DX | Lead measures without emotional buy-in — teams execute mechanically, motivation decays by week 6 |
| MASTER | Specificity/trackability without a narrative — goals read as compliance checklists |
| DUMB | Emotional resonance without measurement — inspiring but unfalsifiable, can't tell if you're on track |
| Backward Goal Setting | Milestone cascade without a scoreboard — milestones get set then forgotten between check-ins |

This skill forces all four functions into one document so none of them can be skipped.

## When NOT to use this

- Personal, non-professional goal setting (fitness, relationships, hobbies) → that's `life-wheel-assessment` or plain conversation, not this.
- Simple to-do lists or single-task tracking → overkill, just make a list.
- The user explicitly only wants ONE framework applied in isolation (e.g., "just give me the 4DX lead measures") → honor that, don't force the full fusion. Use this skill's relevant section only.

## Output Format

**Default: inline markdown only.** Do not create a .docx, .pdf, or artifact file unless the user explicitly asks for a downloadable/shareable document (e.g., "make this a Word doc for the CEO meeting," "I need to send this to the BU manager"). If they do ask for a file, use the `docx` skill and apply business-formal structure — this is a deliverable for senior commercial/clinical audiences, not a casual memo.

## The Workflow

### Step 1 — Establish the Wildly Important Goal (WIG)

Before anything else, get one sentence answering: **what is the single goal that, if achieved, would make everything else matter less?**

If the user gives you a vague domain ("improve marketing") instead of a WIG, push back and ask them to narrow it — a goal architecture built on a vague input produces a vague output. Don't silently narrow it for them; that's their strategic call, not yours to make unilaterally. Exception: if they've given you enough surrounding context (e.g., a business intelligence report, a known structural problem) that the WIG is obviously implied, state your inferred WIG and ask for confirmation rather than asking an open question.

### Step 2 — DUMB framing pass (narrative layer)

Reframe the WIG using DUMB's four lenses. This is not optional decoration — it's the layer that makes Step 3-5's mechanics survive contact with a room full of stakeholders who don't care about scoreboards yet.

- **Dream-driven:** What's the bigger ambition this goal serves? One sentence, no hedging.
- **Uplifting:** Who does this energize, and why would they want to come to work for this?
- **Method-friendly:** What existing system/process/cadence will this goal actually run on? (If the answer is "none yet," say so — don't invent one.)
- **Behavior-triggered:** What specific recurring behavior does achieving this require? Not an outcome — a behavior. ("Send the BU dashboard every Friday," not "improve visibility.")

Keep this section to 4 short bullets. If the user's context is clinical/regulatory (tender feasibility, public hospital sales), tone down "dream" language — emotional storytelling has a ceiling in formal Greek procurement contexts, and overselling it will read as out of place to a CEO or BU manager. Use judgment; flag if you're toning it down.

### Step 3 — Backward cascade (structural layer)

Work backward from the WIG to today:

```
[Ultimate Goal] ← Step 1's WIG, restated
  └─ Milestone 1 (latest, closest to end goal)
       └─ Milestone 2
            └─ Milestone 3
                 └─ Milestone N (earliest)
                      └─ Action(s) — what starts THIS WEEK
```

Rules:
- Minimum 3 milestones, maximum 6. Fewer than 3 means you haven't actually decomposed it; more than 6 means you're tracking tasks, not milestones — push the excess down a level.
- Each milestone needs a **date or trigger condition**, not just a label. "Milestone: secure tender shortlist" is incomplete. "Milestone: secure tender shortlist — by [date], triggered by ΕΑΔΗΣΥ decision window closing" is usable.
- The bottom-most action must be something startable within 7 days. If it isn't, you haven't cascaded far enough — add another milestone layer.

### Step 4 — MASTER conversion (specification layer)

Convert the cascade into the MASTER structure as a table — this is what makes it trackable, not just inspiring:

| Element | Requirement | Your input |
|---|---|---|
| **M**otivation | Why this matters to the stakeholder, in their terms (not yours) | |
| **A**chievable | Stretch but real — state the specific constraint that makes it hard | |
| **S**pecific | One unambiguous definition of "done" | |
| **T**rackable | The exact metric(s) and where they're measured | |
| **E**ngaging | What makes people want to check progress, not dread it | |
| **R**ewarding | The actual recognition/reward mechanism — name it, don't gesture at "celebrating wins" | |

Push back if "Trackable" is vague ("we'll know it when we see it") — that's the single most common failure point in goal architectures and the one most worth being blunt about.

### Step 5 — 4DX execution layer (accountability layer)

This is where most goal-setting exercises die — they stop at Step 4 and never get an execution rhythm. Build:

1. **Lead measures** (1-3 max): the few predictive, influenceable activities that drive the WIG. Distinguish explicitly from lag measures (the WIG metric itself, which you can't directly influence day-to-day).
2. **Compelling scoreboard**: what gets displayed, where, updated how often. If the user has no existing dashboard/reporting cadence, say so plainly rather than assuming a Power BI build exists — ask, don't assume.
3. **Cadence of accountability**: the specific recurring meeting/check-in (weekly is the 4DX default; don't default to it blindly if the user's org runs monthly BU reviews — match their actual rhythm).

### Step 6 — Assemble and red-team

Present the full architecture as one document (template below), then **add a short "Where this breaks" section** — 2-4 sentences identifying the most likely failure mode of this specific plan (resourcing gap, dependency on a stakeholder who hasn't bought in, a metric that's gameable, a milestone with no real owner). Do not skip this section even if the plan looks solid — a goal architecture without a stated failure mode is not rigorous, it's optimistic.

## Output Template

```markdown
# [WIG Title] — Quarterly Goal Architecture

## Wildly Important Goal
[One sentence]

## Narrative (DUMB)
- Dream-driven: ...
- Uplifting: ...
- Method-friendly: ...
- Behavior-triggered: ...

## Cascade (Backward Goal Setting)
[Ultimate Goal] → Milestone 1 (date/trigger) → Milestone 2 (date/trigger) → ... → This week's action

## Specification (MASTER)
| Element | Detail |
|---|---|
| Motivation | |
| Achievable | |
| Specific | |
| Trackable | |
| Engaging | |
| Rewarding | |

## Execution (4DX)
- Lead measures: ...
- Scoreboard: ...
- Accountability cadence: ...

## Where this breaks
[2-4 sentences, named failure mode, not generic risk language]
```

## Notes on tone

This skill is for business-formal, senior-audience output by default (BU managers, CEO, board). Avoid the infographic-poster tone of the source frameworks ("Top 1%" energy) — strip that out entirely. The fusion logic stays; the delivery should read like a strategist's working document, not a motivational graphic.

## Related skills in this repo

- **business-decision-frameworks**: Prioritize and score candidate initiatives (RICE, Value vs Effort) before architecting them into a goal cascade here.
- **business-intelligence-report** / **ceo-reporting-skill**: Use the OKRs and lead measures produced here as the targets those reporting skills track progress against each period.
- **pptx** / **premium-html-presentation**: Present the goal cascade as an actual deck for a BU/board meeting.
- **xlsx**: Build a scoreboard workbook tracking the lead measures defined here.
- **product-strategy-session** / **saas-idea-validator** / **the-productize-yourself-blueprint**: For a brand-new business, validate the idea and product/service format with these before setting quarterly goals around it.
- **advisory-board**: Sanity-check the resulting goal cascade with `/ask-the-board` before committing to it.
- **growth-operating-framework**: Use that skill to pick *what* to build growth goals around (North Star metric, data foundation) before architecting the OKR cascade here.
- **kpi-reference-handbook**: OKRs and KPIs are not the same thing —
  an OKR (this skill) is the direction and the stretch: an ambitious,
  time-boxed objective with a few key results that prove it's on track.
  A KPI (that skill) is an ongoing health metric for something already
  running, tracked continuously rather than for one quarter. In practice
  they compose: pull a formula from `kpi-reference-handbook` to serve as
  a Key Result or a Step 5 lead/lag measure here, rather than inventing a
  metric from scratch — and once this cascade is running, the same KPI
  keeps getting tracked in `kpi-reference-handbook`'s terms long after
  this particular OKR closes out.
