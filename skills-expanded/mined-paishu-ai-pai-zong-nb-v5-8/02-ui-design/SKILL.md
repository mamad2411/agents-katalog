---
name: ui-design
description: Design practical user interfaces, flows, information architecture, layout systems, component states, and design tokens. Use for page design, UX redesign, dashboards, tools, mobile/web UI, interaction design, and before frontend implementation when visual or workflow decisions matter.
---

# UI Design

## Workflow

1. Identify the primary user, job-to-be-done, and main workflow.
2. Define information hierarchy before visual treatment.
3. Specify layout, navigation, components, and interaction states.
4. Cover loading, empty, error, disabled, permission-limited, and success states.
5. Map responsive behavior across mobile, tablet, and desktop.

## Quality Bar

- Match the product type: tools and dashboards should be dense, calm, and scannable; marketing pages may be expressive.
- Use design tokens for color, spacing, type, radius, shadow, and motion.
- Do not rely on generic "modern" language; specify concrete UI decisions.
- Prefer familiar controls: tabs, segmented controls, switches, sliders, menus, and icon buttons where appropriate.
- Avoid decorative card-heavy layouts unless cards represent repeated items or framed tools.

## Handoff

Provide component hierarchy, key states, responsive rules, and implementation notes. Mention accessibility and i18n risks when they affect the design.

## Output Contract

- State the selected workflow, assumptions, and concrete deliverable.
- Include verification, limitations, or next-step handoff when relevant.
- If tool output, files, deployments, scans, or external actions are claimed, cite the command/tool evidence.
