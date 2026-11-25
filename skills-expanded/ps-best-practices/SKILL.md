---
name: ps-best-practices
description: Suggest Process Street workflow design best practices — naming, field types, conditional logic, stops/approvals, assignments, due dates, automation, organization. Use when the user asks how to design a good workflow, wants recommendations, or how to improve their process design.
---

# Process Street best-practice guidance

Give concrete, opinionated workflow design advice grounded in `reference/best-practices.md` (read it before answering — it's the source of truth for this skill).

## How to use it

- **General "how should I design X" questions** → synthesize the relevant principles from `reference/best-practices.md` into a short, specific recommendation for *their* use case. Don't dump the whole guide; pull the 3–5 points that matter here.
- **"Is my workflow good?"** → that's an audit. Hand off to the `ps-audit` skill (it scores an existing workflow against the same guide).
- **"Build me one that follows best practices"** → give a quick design sketch, then offer the `ps-build` skill.

## Anchor every answer in these themes (full detail in the reference)

- **Naming & structure** — outcome-based names, 6–15 verb-named steps, one process per workflow, real-sequence order, front-load data capture.
- **Field types** — use the right type (Select/Date/Number/Members/Email), not free text everywhere; short forms per step; help text on ambiguous fields.
- **Control flow** — conditional logic to hide the irrelevant; stops/approvals only where they earn their friction; configure approval subject tasks.
- **Accountability** — an owner per task (assignment rules); dynamic due dates over fixed offsets.
- **Automation** — Code/AI tasks and webhooks to kill manual re-keying; Data Sets for shared option lists.
- **Polish & organization** — branded first step, media where it beats text; folders by team/function.

End with the **10-point scorecard** from the reference when the user wants a checklist.

## Be honest about limits
Required-field flag, brand theming (colors/cover/fonts), org/SSO, and deep native-integration config are set in the Process Street UI, not the API.
