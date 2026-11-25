---
name: otto-command-center
description: >
  Generate the OTTO Command Center — a self-contained interactive HTML dashboard
  that consolidates all OTTO knowledge. Use when the user says "command center",
  "otto dashboard", "generate the dashboard", "otto center", "show me the personas",
  "skill explorer", "interactive wiki", or wants a visual overview of the OTTO system.
version: 0.1.0
---

# OTTO Command Center Generator

Generate the unified OTTO Command Center as a self-contained HTML file.

## What It Produces

A single HTML file (~1200 lines) with 7 interactive tabs:

1. **Overview** — Stats + persona × drives matrix
2. **Chambers** — Clickable Discovery→Build→Verify→Ship flow with skill loadouts and transition suggestions
3. **Personas** — 17-card grid with expandable profiles, drive visualizations, workspace prefs
4. **Task Router** — Type a task → get persona + chamber + skill recommendations
5. **Playbooks** — Browse canonical playbook templates with phase flows
6. **Wiki** — Skill taxonomy, chaining model, execution patterns
7. **Prompt Optimizer** — Generate Claude Project system prompt snippets

## Required Theme

Read `references/template-spec.md` for the exact visual specification. Key elements:
- Dark mode: bg #0a0a0f, surface #12121a, accent #6c5ce7
- Fonts: JetBrains Mono (code) + Inter (body) from Google Fonts
- Chamber colors: Discovery #00b894, Build #fdcb6e, Verify #e17055, Ship #0984e3
- Animated grid background, glow effects, smooth panel transitions
- Mobile responsive

## Data Sources

All data comes from the agent-otto skill references:
- `../agent-otto/references/personas.md` — 17 profiles with full data
- `../agent-otto/references/chambers.md` — 4 chambers with loadouts
- `../agent-otto/references/transitions.md` — transition rules
- `../agent-otto/references/skill-catalog.md` — full skill catalog
- `../agent-otto/references/playbooks.md` — canonical templates

## Critical: Chamber Transitions

Every chamber view must include a **transition card** at the bottom showing:
- What the next recommended chamber is
- Which persona should lead
- What quality gate must be met first
- A "Proceed →" visual element

This is the key differentiator from previous versions.

## Output

Save as `otto-command-center.html` in the user's workspace folder.
