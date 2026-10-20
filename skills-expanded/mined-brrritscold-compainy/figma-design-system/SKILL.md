---
name: figma-design-system
description: Builds and maintains a design system in Figma, then extracts and codifies it for code consumers. Invoked when the user says "build a design system in Figma", "create components in Figma", "extract design tokens", "extract Figma variables", "codify design system", "pull tokens from Figma", or "generate tokens.json". Uses the official Figma MCP (the `figma` companion plugin) to create frames, components, variables, and styles — and to read/export them as tokens.json.
---

# Figma Design System Skill

Build design systems directly in Figma using the official Figma MCP write tools, then extract and codify design intent as a portable, W3C design-tokens–style `tokens.json` plus a human-readable design-system spec. The design system in Figma is the source of truth; `tokens.json` is the code mirror for the frontend.

> **Seat requirement:** Writing to the Figma canvas requires a Figma Full seat on a paid plan (Dev seat = read-only outside drafts).

For write mechanics (`use_figma`, `create_new_file`, `generate_figma_design`), defer to the **`figma-use`** skill — it provides the reliable workflow patterns for driving Figma write tools.

## Write execution & verification

The Figma MCP is a remote, OAuth-authenticated server. **Verify reachability before relying on it — never assert it's unavailable.**

- **Probe**: call `whoami` first — success proves reachability + auth, not a write (Full) seat. Begin the build and let the first real write (`create_new_file`) test the seat. Writes go through ⇒ continue authoring directly. A reachability failure, or a seat/permission error on that first write ⇒ surface it and switch to the fallback below; don't silently skip the build.
- **Fallback (main-session executes)**: if the MCP is unreachable from your context (a common case for a dispatched subagent hitting a remote OAuth server), do not abandon or thin the design. Produce a **complete, deterministic build spec** — every frame, component, variant, state, breakpoint, variable, and the exact `use_figma`/`generate_figma_design` calls — and hand it to the main session, which performs the writes. The designer owns every decision; the executor only types.
- **Completeness gate**: a `tokens.json` + spec pass is *not* a built design system. "Done" requires every component authored, all breakpoints (desktop/tablet/mobile), all interactive states, plus `tokens.json` + `design-system.md` + a component inventory (component names + Figma node IDs, for the frontend's Code Connect) emitted and validated. Never present a stub as the deliverable — name what's missing instead. (Code Connect mapping itself is the `frontend-engineer`'s job, not this skill's.)

## Process

### 1. Build the design system in Figma

Use the official Figma MCP write tools (via the `figma` companion plugin) to create or extend the design system directly in Figma. Defer to the **`figma-use`** skill for step-by-step write mechanics.

Key write operations:
- `create_new_file` — create a new Figma file for the design system if one does not exist.
- `generate_figma_design` — generate frames, component structures, and layout from a prompt or spec.
- `use_figma` — the general-purpose write tool for creating/editing/deleting frames, components, variables, color styles, text styles, and auto-layout. Use this to:
  - Define color variable collections (light/dark modes)
  - Define typography styles (font families, sizes, weights, line-height)
  - Define spacing, radius, and shadow variables
  - Build component sets with variants (e.g. Button: size × variant × state)
  - Set up auto-layout on frames and components

Structure the file with dedicated pages:
- **Foundations** — color, typography, spacing, radius, shadow variables
- **Components** — component sets, documented with variants
- **Templates** — page-level layout examples

### 2. Read and inspect

After building (or when working from an existing file), read the design system state using the MCP read tools:
- `get_variable_defs` / `get_local_variable_collections` — enumerate all design variables and their mode values.
- `get_design_context` — inspect frames, components, and their computed properties.
- `get_metadata` — file metadata and structure.
- `search_design_system` — search for components, styles, and variables by name.
- `get_libraries` — list shared libraries linked to the file.

### 3. Categorize tokens

Map Figma primitives to W3C design-token categories:

| Figma source | Token category |
|---|---|
| Color variables / color styles | `color` |
| Typography styles (font, size, weight, line-height, tracking) | `typography` / `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing` |
| Number variables mapped to spacing | `spacing` |
| Number variables mapped to corner radius | `borderRadius` |
| Effect styles (box-shadow, drop-shadow) | `shadow` |
| Stroke / border widths | `borderWidth` |

Separate **primitive tokens** (raw values, e.g. `color.blue.500`) from **semantic tokens** (role-mapped aliases, e.g. `color.background.primary → {color.blue.500}`).

### 4. Output `tokens.json` (code mirror for the frontend)

Emit a W3C Design Tokens Community Group (DTCG) format file when a code mirror is needed for the frontend engineer:

```json
{
  "color": {
    "blue": {
      "500": { "$type": "color", "$value": "#3B82F6" }
    },
    "background": {
      "primary": { "$type": "color", "$value": "{color.blue.500}" }
    }
  },
  "fontSize": {
    "sm": { "$type": "dimension", "$value": "14px" },
    "base": { "$type": "dimension", "$value": "16px" },
    "lg": { "$type": "dimension", "$value": "18px" }
  },
  "spacing": {
    "1": { "$type": "dimension", "$value": "4px" },
    "2": { "$type": "dimension", "$value": "8px" },
    "4": { "$type": "dimension", "$value": "16px" }
  },
  "borderRadius": {
    "sm": { "$type": "dimension", "$value": "4px" },
    "md": { "$type": "dimension", "$value": "8px" },
    "full": { "$type": "dimension", "$value": "9999px" }
  },
  "shadow": {
    "sm": { "$type": "shadow", "$value": { "offsetX": "0px", "offsetY": "1px", "blur": "2px", "spread": "0px", "color": "#00000014" } }
  }
}
```

Write the file to the project root as `tokens.json`. If CSS custom properties are also needed, emit a `tokens.css` companion using `--token-name: value;` conventions (kebab-case, e.g. `--color-background-primary`).

### 5. Record auto-layout intent

For each auto-layout frame or component, note in the design-system spec:

- **Direction** → CSS `flex-direction` (`row` / `column`)
- **Spacing mode** (packed vs. space-between) → `justify-content`
- **Alignment** → `align-items`
- **Gap** → `gap` (map to a spacing token if one matches)
- **Padding** → individual padding sides, mapped to spacing tokens
- **Wrap** → `flex-wrap: wrap` when Figma wrapping is on

Write these as annotated component layout specs in `design-system.md` so the frontend engineer can reproduce layout in CSS/Tailwind without guessing.

### 6. Write the design-system spec

Produce `design-system.md` alongside `tokens.json`. Include:

1. **Token inventory** — summary table of each category and token count.
2. **Component inventory** — list of top-level component sets in the Figma file.
3. **Auto-layout intent** — per-component flex/grid mappings from step 5.
4. **Typography scale** — rendered table of all text styles with computed values.
5. **Color palette** — primitive palette + semantic role mapping.
6. **Usage notes** — any Figma constraints, mode variants (light/dark), or missing mappings that need designer clarification.

### 7. Validate before handing off

- Confirm every `$value` that is a reference (`{token.path}`) resolves to a defined token — no dangling references.
- Confirm `tokens.json` is valid JSON (`Bash: node -e "JSON.parse(require('fs').readFileSync('tokens.json','utf8'))" && echo valid`).
- Flag any Figma variable that has no clear token category mapping so it is not silently dropped.
