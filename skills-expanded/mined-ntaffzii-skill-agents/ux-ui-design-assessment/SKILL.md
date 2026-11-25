---
name: ux-ui-design-assessment
description: Analyze and document the UX/UI of a project against the full UX/UI body of knowledge, or design the UX/UI for a new project from scratch. Use when the user wants to know "how is this project's UX/UI", to audit/review/evaluate an existing interface, to produce a UX/UI assessment report, or to design UX/UI for a new product (personas, empathy maps, information architecture, wireframe/prototype plan, color and typography, responsive strategy, moodboard, usability test plan). Triggers include "วิเคราะห์ UX/UI", "สแกน UI ของโปรเจกต์", "ออกแบบ UX/UI", "เขียนเอกสาร UX/UI", "audit the UI", "evaluate UX", "UX/UI ของโปรเจกต์นี้เป็นอย่างไร", "design the UX for a new app". Produces a written file (UX-UI-ASSESSMENT.md or UX-UI-DESIGN-DOC.md). This skill documents and plans; it hands code implementation to the companion `ui-design-engineering` skill.
---

# UX/UI Design Assessment

Produce an evidence-based UX/UI document for a project — either by **auditing** an existing interface or by **designing** the UX/UI for a new one. The methodology is the ten-topic UX/UI body of knowledge in [references/ux-ui-knowledge.md](references/ux-ui-knowledge.md).

This skill **documents and plans**. It does not implement UI code — that is the job of the companion `ui-design-engineering` skill.

## Choose The Mode

- **Audit mode** — evaluate an existing project's interface against the ten UX/UI dimensions; produce a report file describing how the project's UX/UI currently is.
- **Design mode** — design the UX/UI for a new (or redesigned) product; produce a design document.

If unsure, ask the user one question: "Is there an existing interface to evaluate (Audit), or are we designing UX/UI for something new (Design)?"

## Knowledge Base (read on demand)

- [references/ux-ui-knowledge.md](references/ux-ui-knowledge.md) — the ten topics: UX/UI foundations, Design Thinking, user research (persona/empathy map/affinity), information architecture, wireframe/mockup/prototype, visual hierarchy, color and typography, responsive design, moodboard, usability testing.
- [references/audit-rubric.md](references/audit-rubric.md) — Audit mode: ten-dimension rubric, severity scale, evidence rules.
- [references/design-workflow.md](references/design-workflow.md) — Design mode: the 7-step loop and sub-templates (persona card, empathy map, problem statement, user flow, wireframe checklist, moodboard).
- [references/external-techniques.md](references/external-techniques.md) and [references/credits.md](references/credits.md) — what was adapted from external skills (design-lab, ui-ux-pro-max, improve-ui, rams, web-design-guidelines).

## Audit Mode Workflow

1. **Inspect the project** — read the framework, routes, components, design tokens, and any `DESIGN.md`. Open the real pages in a browser when possible.
2. **Identify user and task** — name the primary user, their immediate goal, the environment, and how often the workflow runs.
3. **Evaluate against the ten dimensions** — for each, find evidence and apply the rubric. Never guess; every candidate must pass the three-part proof gate (contract + runtime + correction) and survive falsification.
4. **Rate and prioritize** — assign a rating (Strong/Adequate/Weak/Missing/N/A) and a severity (P0-P3) to each finding. If nothing survives falsification for a dimension, write "No supported findings".
5. **Write the report** — fill [templates/UX-UI-ASSESSMENT.md](templates/UX-UI-ASSESSMENT.md): overall summary, dimension table, findings by severity, responsive/accessibility/usability sections, prioritized fix list.

## Design Mode Workflow

Follow [references/design-workflow.md](references/design-workflow.md) for the full loop. Summary:

1. **Empathize** — interview with open-ended questions (never leading).
2. **Define** — write a problem statement and top pain points.
3. **Ideate** — generate meaningfully distinct variants.
4. **Information architecture + wireframe plan** — sitemap, user flow, taxonomy, wireframe structure before any styling.
5. **Visual design** — color, typography (max 2 fonts), hierarchy, moodboard.
6. **Prototype + usability test plan** — clickable flow, full component states, open-ended test tasks.
7. **Finalize** — write [templates/UX-UI-DESIGN-DOC.md](templates/UX-UI-DESIGN-DOC.md).

## Output Files

- Audit mode -> `UX-UI-ASSESSMENT.md` (place at repo root or under `docs/`; do not overwrite existing project files unless asked).
- Design mode -> `UX-UI-DESIGN-DOC.md`.

## Companion Skill

After Audit mode, the prioritized fix list is handed to `ui-design-engineering`, which implements and browser-validates the changes. This keeps assessment and implementation separate: this skill stays evidence-based and read-only toward code.

## Guardrails

1. **Evidence, not opinion.** Every finding cites a `file:line` reference or an observed browser behavior on the real route. If you cannot prove it, do not report it.
2. **Open-ended questions only.** In Design mode and usability planning, never ask leading questions. Ask "What would you expect this to do?" rather than "Is this easy to use?".
3. **No emoji in output files.** Use named icons (e.g., Lucide) or named SVGs for any visual indicator.
4. **Do not edit UI code.** This skill produces documentation only; code changes go to `ui-design-engineering`.
5. **Quantitative bars.** Apply the shared thresholds: contrast 4.5:1 text / 3:1 UI, touch targets 44x44px, base font ~16px / line-height ~1.5, max 2 fonts per screen, visible `:focus-visible`, respect `prefers-reduced-motion`.
6. **Honesty.** If a dimension has no supported findings after falsification, say so. Do not invent problems to fill a template.

## Source And Attribution

This skill is an original Skill-Agents synthesis. It adapted techniques from public UI Skills directory skills; it is not official or verbatim upstream content. See [references/credits.md](references/credits.md) for full attribution and [references/external-techniques.md](references/external-techniques.md) for exactly what was adapted.
