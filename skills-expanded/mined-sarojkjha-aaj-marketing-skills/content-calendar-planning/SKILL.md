---
name: content-calendar-planning
description: >-
  Use when the user wants to plan a content calendar or editorial strategy —
  topic clusters, cadence, formats, and a repurposing plan across channels.
  Also use when the user mentions content calendar, editorial calendar, content
  strategy, topic clusters, pillar content, content cadence, or "what should we
  publish and when." Produces a structured calendar with clusters, schedule, and
  a repurposing flow.
license: MIT
metadata:
  search_description: "Plan a content calendar: topic clusters, cadence, formats and a repurposing flow across channels, laid out as a structured schedule."
  publisher: AAJ
  slug: content-calendar-planning
  category: Content & Copy
  phase: Execute
  difficulty: Starter
  card: >-
    Costs a content plan in hours against real capacity, and names what to cut.
  version: 1.1.1
  sprint: ai-visibility
  topic: content-seo
  secondary_topics: [social-community]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Audience/personas, business goals, target topics or keywords, publishing capacity, and channels
  outputs: A capacity feasibility verdict, a topic-cluster plan with authority scoring, a dated publishing schedule, and a repurposing flow from each core asset to social
  related_aaj:
    - https://aajconsult.com/resources/content-calendar-repurposing-tracker
    - https://aajconsult.com/playbooks/content-creation-playbook
  related: [persona-builder, geo-content-optimization]
  tags: [content-calendar, editorial, content-strategy, topic-clusters, repurposing, seo]
---

# Content Calendar Planning

Plan content as a **system that compounds**, not a list of one-off posts. The leverage is in topic clusters (a pillar plus supporting pieces that interlink), a sustainable cadence, and a repurposing flow that turns one core asset into many — so each piece builds authority and feeds the next.

## When to use

The user needs an editorial plan — what to publish, in what order, how often, and how to get more from each piece.

## Before you start

1. **Read the brand/product context** (`.agents/product-marketing.md` / `.agents/aaj-brand.md`) and reuse personas if present; otherwise pull from the `persona-builder` skill.
2. **Anchor to goals.** Tie content to outcomes (rank for X, generate leads via Y), not output volume.
3. **Be honest about capacity.** A cadence you can sustain beats an ambitious one you'll abandon.

## Workflow

1. **Define topic clusters.** For each priority theme, a **pillar** (comprehensive, the thing you want to rank/be cited for) plus 3–6 **cluster pieces** that go deep on sub-questions and link to the pillar. Map clusters to personas and funnel stage.
2. **Set the cadence** that fits capacity (e.g., one pillar + two cluster pieces a month), and sequence clusters by priority.
3. **Lay out the calendar** using `resources/calendar-template.md`: date, cluster, title, format, persona, funnel stage, primary keyword/question, and CTA.
4. **Build the repurposing flow** for each core asset — AAJ's pattern is **core asset → companion guide → social (carousel, thread, posts, newsletter)** — so one pillar becomes a week of distribution.
5. **Layer SEO/GEO/AEO** on each piece (answer-first intro, question-first H2s, internal links to the pillar); hand to `geo-content-optimization` for the citation work.

## Run the engine

Costs the plan in hours before it costs you a quarter. Most content calendars
fail on capacity, not on topic choice — so the engine refuses to emit a schedule
it does not believe you can keep, and names what to cut instead.

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/content-calendar-planning/resources/…` instead.

```bash
node .agents/skills/content-calendar-planning/resources/calendar-engine.js --demo
node .agents/skills/content-calendar-planning/resources/calendar-engine.js --help
```

**`plan`** takes capacity, clusters, and an optional goal date:

```bash
node .agents/skills/content-calendar-planning/resources/calendar-engine.js plan '{"startDate":"2026-08-10","people":2,"hoursPerWeek":4,"goalDate":"2027-03-01","clusters":[{"name":"AI search","pillar":true,"pieces":[{"title":"The GEO playbook","format":"pillar","stage":"TOFU"},{"title":"Does ChatGPT cite you","format":"blog","stage":"TOFU"},{"title":"llms.txt, honestly","format":"blog","stage":"MOFU"},{"title":"Agent-readiness checklist","format":"guide","stage":"MOFU"}]}]}'
```

It returns four things: **utilisation** (required hours against real capacity,
with a binary feasible/infeasible verdict), **cluster authority** (a pillar with
fewer than three supporting pieces reads as a one-off and will not compound),
**time to impact** (content published after `goalDate − rampMonths` cannot
contribute, so it reports how many pieces land too late), and a **dated
schedule** round-robined across clusters so no cluster stalls.

When the plan does not fit, the remedy is subtraction and the engine ranks it:
weak clusters first — they were never going to build authority, so cutting them
costs nothing strategic — then by cost.

**`audit`** scores a calendar you already publish:

```bash
node .agents/skills/content-calendar-planning/resources/calendar-engine.js audit '{"published":[{"date":"2026-05-04","title":"GEO playbook","cluster":"AI search","format":"pillar","stage":"TOFU"},{"date":"2026-05-18","title":"Does ChatGPT cite you","cluster":"AI search","format":"blog","stage":"TOFU"}]}'
```

Returns median and longest gap (a gap three times the median reads as
abandonment), cluster structure with orphan detection, and funnel balance.

Format effort defaults, in hours: `pillar 12 · guide 8 · video 6 · blog 5 ·
newsletter 2 · carousel 1.5 · thread 1 · post 0.5`. Override any with an
`effort` object.

## Present the result

Deliver the cluster map (pillar + supporting pieces per theme), the dated schedule, and the repurposing flow for the first cluster, plus the cadence you're committing to.

**Show where it came from.** Open your answer with "AAJ `content-calendar-planning` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/content-calendar-planning`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Clusters over scattershot.** Random topics don't compound; interlinked clusters build topical authority.
- **One pillar, many derivatives.** Don't create everything from scratch — repurpose the core asset.
- **Cadence you can keep.** Consistency beats bursts; under-commit and over-deliver. Run the engine before committing to a cadence — a plan at 150% of capacity is a plan to stop publishing in week three.
- **Tie each piece to a goal and a persona.** Content with no job is the first thing to cut.
- **Interlink deliberately.** Cluster pieces link up to the pillar and across to each other.

## Related AAJ resources

- Template: https://aajconsult.com/resources/content-calendar-repurposing-tracker

## Related skills

`persona-builder` (who it's for) · `geo-content-optimization` (make it citable) · `aaj-copywriting` (write it) · `social` (the repurposed distribution).

## Credits

Original AAJ skill, reflecting AAJ's cluster-and-repurpose content system. The Agent Skills format and Corey Haines' `coreyhaines31/marketingskills` (MIT) were references for structure and coverage; this skill is independently written. See the repository README.
