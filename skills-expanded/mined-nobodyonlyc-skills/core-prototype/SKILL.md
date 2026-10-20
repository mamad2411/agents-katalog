---
name: core-prototype
description: Single-agent quick mock UI — render a screen or two as static HTML/CSS for fast visual feedback. UI only, no backend or DB.
---

> **[Persona Directive]** You must execute this skill acting in the role of a **UI/UX Prototyper**. Adopt their exact mindset, priorities, and vocabulary. Do NOT spawn a subagent for this.


Mock UI to build: $ARGUMENTS

The lightweight, single-agent path for a **mock UI**. Use it to throw together one or a few screens as static **HTML/CSS** for quick visual feedback. **UI only** — placeholder data, no backend, no database, no business logic.

> **Scale check:** this is the right skill for **1–2 screens** (e.g. the UI design gate of a single feature). For a **whole app / the full FE SPEC** with many screens, use [workflow-prototype](../workflow-prototype/SKILL.md) (multi-agent, coverage checklist) instead.

> **Reuse the design system:** if `docs/spec/design-system.md` exists, it is the source of truth — link its `:root` token block (palette, typography, spacing, components) so a new per-US screen matches the look already approved for the project. Do not invent a fresh palette/font; if the screen genuinely needs a new token, add it back to `docs/spec/design-system.md`. See [design-system](references/design-system.md).

> For the full, SPEC-driven mock (every screen/function from `docs/spec/frontend.md`, choice of HTML/CSS or Figma-via-MCP, mandatory browser preview + feedback loop), use [workflow-prototype](../workflow-prototype/SKILL.md).

```bash
ls -la
find . -name "package.json" -o -name "*.css" | head -3   # reuse existing FE stack / tokens if any
```

## Ground Rules
- **UI only** — never build or stub a backend, DB, or real logic. Hardcode all sample data.
- **Static HTML/CSS/JS** — generate JavaScript to handle UI events (e.g., toggling sidebars, opening modals, dropdowns).
- **Responsive by default** — the prototype MUST support Mobile and Tablet modes seamlessly.
- **No placeholder text** like `[Image here]` or `TODO` — use placeholder images (e.g. `https://placehold.co/600x400`) and realistic copy.

## References
Please follow the guidelines in these references carefully:
- **[Design System & CSS Patterns](references/design-system.md)**: Pick a style direction, then standard tokens, typography, and responsive layout guidance.
- **[Quality Rubric](references/quality-rubric.md)**: The 8-dimension bar each screen must pass — self-check against it before every preview.
- **[Iteration Loop](references/iteration-loop.md)**: The lifecycle for rendering, self-reviewing (screenshot + rubric), previewing, and refining the prototype.

## Examples
- **[Sample Prototype Output](examples/sample-prototype.md)**: See an example of a well-structured prototype.

## Workflow Phases
1. **Confirm Requirements**: Clarify the screen(s) and what they must show. Set up the basic layout.
2. **Choose direction & apply tokens**: Commit to a concrete style direction (don't default to generic blue + Inter), then apply the full token set per `references/design-system.md`.
3. **Build the Mock**: Write the HTML/CSS with realistic content and complete interaction states.
4. **Self-review before preview**: Screenshot your own output and score it against `references/quality-rubric.md`; fix every Fail **before** the user sees it.
5. **Preview & Iterate**: Follow `references/iteration-loop.md` to host the files, show them to the user, and iterate on feedback.
