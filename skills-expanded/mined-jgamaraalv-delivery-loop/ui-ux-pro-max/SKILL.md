---
name: ui-ux-pro-max
description: UI/UX design intelligence — pick styles, color palettes, font pairings, layout & UX patterns across 10 stacks. Use when designing, building, reviewing, or restyling a web/mobile interface.
---

# UI/UX Pro Max - Design Intelligence

Comprehensive design guide for web and mobile applications. Contains 50+ styles, 161 color palettes, 57 font pairings, 161 product types with reasoning rules, 99 UX guidelines, and 25 chart types across 10 technology stacks. A searchable database (`scripts/search.py` over `data/` CSVs) gives priority-based design recommendations.

This SKILL.md is the thin entry point. Bulky reference material lives under `references/` and is read on demand — see **References** below.

## Workflow at a High Level

The skill is data-driven: a Python CLI (`scripts/search.py`) queries CSV catalogs under `data/` and returns priority-ranked design recommendations.

**To design or build a page/component:**

1. **Analyze requirements** — extract product type, target audience, style keywords, and stack.
2. **Generate a design system (REQUIRED first step)** — run `search.py "<keywords>" --design-system` to get a complete recommendation (pattern, style, colors, typography, effects + anti-patterns). Optionally `--persist` it as a Master + page-overrides set for cross-session reuse.
3. **Supplement with domain searches** — deep-dive any dimension you're unsure about with `--domain <domain>`.
4. **Add stack guidelines** — `--stack react-native` for implementation-specific best practices.
5. **Synthesize and implement**, then run the pre-delivery checks.

**To review or fix existing UI:** start from the [Quick Reference](references/quick-reference.md) 10-category checklist; jump to the category that matches the problem.

Full step-by-step procedure, examples, output formats, and tips: [`references/workflow.md`](references/workflow.md).

## How to Search the Data

```bash
# Full design-system recommendation (always start here when designing)
python3 skills/ui-ux-pro-max/scripts/search.py "<product> <industry> <keywords>" --design-system [-p "Project"]

# Deep-dive one dimension
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]

# Stack-specific implementation guidance
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack react-native
```

Domains: `product`, `style`, `color`, `typography`, `landing`, `chart`, `ux`, `google-fonts`, `react`, `web`, `prompt`. Requires Python 3 (`python3 --version`). See [`references/workflow.md`](references/workflow.md) for the full domain/stack tables, prerequisites, and persistence (`--persist`) details.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/workflow.md` — the full design-system generation workflow: prerequisites (Python), Steps 1–4 (analyze → `--design-system` → `--domain` searches → `--stack`), the `--persist` Master+overrides pattern, domain/stack tables, a worked example, output formats, and query tips · read when building or restyling a page/component.
- `references/quick-reference.md` — the 10 rule categories by priority (Accessibility, Touch & Interaction, Performance, Style Selection, Layout & Responsive, Typography & Color, Animation, Forms & Feedback, Navigation Patterns, Charts & Data) with every rule key and its standard · read when reviewing or fixing UI, or as a final quality pass.
- `references/app-ui-standards.md` — professional-polish rules for App UI (icons & visual elements, interaction, light/dark contrast, layout & spacing) plus the full pre-delivery checklist · read when delivering iOS / Android / React Native / Flutter UI.
