---
name: rayden-use
version: 2.0.0
description: >
  Build and maintain Rayden UI components and screens in Figma using the
  use_figma MCP tool. Use when building new components, adding variants,
  composing screens, syncing React components to Figma, or auditing for
  design system compliance. Requires Figma MCP connected.
argument-hint: "[component-name|screen-name] [figma-file-url]"
allowed-tools: mcp__claude_ai_Figma__use_figma mcp__claude_ai_Figma__get_screenshot mcp__claude_ai_Figma__whoami Read
effort: high
---

# Rayden Figma Skill

Build Rayden UI components and screens in Figma. Every output must be
mechanically correct **and** visually premium. Craft is not optional.

## Style Mode

This skill accepts a `STYLE_MODE` argument that controls aesthetic output:

| Mode | Description |
|------|-------------|
| `conservative` | Tight whitespace, maximum restraint, pure utility |
| `balanced` | Default — generous whitespace, clean hierarchy, premium neutral |
| `expressive` | Bolder scale, more visual weight, stronger typography contrast |

**Usage:**
```
/rayden-use Button conservative https://figma.com/file/...
/rayden-use dashboard-screen expressive https://figma.com/file/...
```

If no mode is given, default to `balanced`.

Current task: `$ARGUMENTS`

---

## Environment Check

```!
# Verify Figma MCP is accessible
echo "Session: ${CLAUDE_SESSION_ID}"
echo "Skill dir: ${CLAUDE_SKILL_DIR}"
ls "${CLAUDE_SKILL_DIR}/supporting/" 2>/dev/null && echo "Supporting files: OK" || echo "Supporting files: not found"
```

---

## Prerequisites

Before any task, verify:
1. Figma MCP connected — call `mcp__claude_ai_Figma__whoami`
2. Write access — user must have Dev or Full Figma seat
3. File URL in arguments

If MCP is not connected, stop and tell the user to connect Figma in Claude's tool settings.

---

## Workflow

### Step 1 — Get Component Data

The agent needs access to Rayden component specs, anatomy, and tokens.
These come from the `@raydenui/ai` package. Check in this order:

**Option A — MCP server running (preferred):**
If the Rayden AI MCP server is connected, use its tools directly:
```
get_components()          → list all available components
get_component_props(name) → get props, variants, and examples for a component
get_tokens()              → get all design tokens (colors, spacing, radius, shadows)
get_layout_recipes()      → get layout patterns and composition rules
```

**Option B — Package installed in project:**
If `@raydenui/ai` is installed in the user's project (`node_modules/@raydenui/ai/`):
```
Read: node_modules/@raydenui/ai/dist/tokens/tokens.dtcg.json   → design tokens
Read: node_modules/@raydenui/ai/RAYDEN_RULES.md                → design rules
```
Component manifests and anatomy are bundled in JS — use `import` or the MCP server.

**Option C — Neither available:**
Install Rayden UI in the user's project first:
```bash
# Scaffolds a full project with Rayden configured
npx create-rayden-app my-app

# Or add to an existing project
npm install @raydenui/ui
```
Then read the component data from the installed package.

Optionally, configure the MCP server for richer tooling:
```json
{
  "mcpServers": {
    "rayden-ai": {
      "command": "npx",
      "args": ["@raydenui/ai"]
    }
  }
}
```

**Do not guess component props or token values.** If you cannot access the
manifest data through any of these methods, stop and ask the user.

### Step 2 — Load Craft Rules

Read these supporting files before writing any code:

- **[supporting/tokens.md](supporting/tokens.md)** — Resolved token values (hex, px, shadow values)
- **[supporting/craft-rules.md](supporting/craft-rules.md)** — Typography, radius, spacing, color craft rules
- **[supporting/anti-patterns.md](supporting/anti-patterns.md)** — Banned layouts and AI design smells

### Step 3 — Identify Task Type

| Task | Action |
|------|--------|
| Single component | Build all variants, then QA |
| Screen / page | Load craft-rules, plan layout, build shell → sections → components |
| Audit | Use `get_design_context`, check against tokens + craft rules |
| Add variants | Read existing component structure first via `get_design_context` |

### Step 4 — Apply Style Mode Adjustments

**conservative:**
- Spacing: use lower end of ranges (spacing.4 padding, spacing.6 section gaps)
- Shadow: flat cards only (`border border-grey-200`, no shadow)
- Typography scale: h4/h5 max for headings
- No decorative elements

**balanced (default):**
- Spacing: standard ranges (spacing.6 padding, spacing.8–10 section gaps)
- Shadow: `shadow-soft-xs` on cards, `shadow-soft-sm` on hover
- Typography: h3/h4 for page titles, full scale
- Subtle hover lifts

**expressive:**
- Spacing: upper end (spacing.8–12 padding, spacing.12 section gaps)
- Shadow: `shadow-soft-sm` resting, `shadow-soft-md` on elevated panels
- Typography: h2/h3 for page titles, `tracking-tight` enforced at h4+
- Larger MetricsCard values, more visual weight on KPIs

### Step 5 — Build

Include these helpers at the top of every `use_figma` code block:

```javascript
// ── Helpers ─────────────────────────────────────────────────────────────
function hexToRgb(hex) {
  return {
    r: parseInt(hex.slice(1,3),16)/255,
    g: parseInt(hex.slice(3,5),16)/255,
    b: parseInt(hex.slice(5,7),16)/255
  };
}

async function loadFonts() {
  await Promise.all(
    ["Regular","Medium","SemiBold","Bold"].map(
      style => figma.loadFontAsync({ family: "Inter", style })
    )
  );
}

function applyShadow(node, level = "soft-xs") {
  const s = {
    "soft-xs": { y:1, blur:2, spread:0, a:0.05 },
    "soft-sm": { y:1, blur:3, spread:0, a:0.10 },
    "soft-md": { y:4, blur:8, spread:-2, a:0.10 },
  }[level];
  node.effects = [{
    type:"DROP_SHADOW",
    color:{ r:0.063, g:0.094, b:0.157, a:s.a },
    offset:{ x:0, y:s.y }, radius:s.blur, spread:s.spread,
    visible:true, blendMode:"NORMAL"
  }];
}

function applyBorder(node, hex="#EAECF0", weight=1) {
  node.strokes = [{ type:"SOLID", color:hexToRgb(hex) }];
  node.strokeWeight = weight;
  node.strokeAlign = "INSIDE";
}
// ────────────────────────────────────────────────────────────────────────
```

**Auto layout is mandatory.** Every frame, every component, every section.
Never use `node.x` or `node.y` for layout positioning.

### Step 6 — Visual Validation Protocol

After each major build step, call `mcp__claude_ai_Figma__get_screenshot` and
validate the output systematically. **Do not skip this step.**

#### What to check

| Check | Pass criteria | Failure signal |
|-------|---------------|----------------|
| **Alignment** | All elements aligned to auto-layout grid, no stray offsets | Elements visually misaligned, uneven gaps between siblings |
| **Spacing** | Gaps between elements match token values (4px grid) | Gaps that look too tight or too loose relative to neighbors |
| **Color accuracy** | All fills/strokes match resolved token hex values | Colors that look off-brand (too saturated, too dark, wrong hue) |
| **Text legibility** | All text readable, no clipping, correct font weight | Text truncated, overlapping, or too light against background |
| **Hierarchy** | Clear visual order: heading → subtitle → body → meta | Everything same size/weight, no clear reading order |
| **Radius consistency** | Inner elements one step smaller than container | Same radius on nested elements, or inner larger than outer |
| **Shadow/border** | One elevation strategy per section, not both heavy | Heavy border + heavy shadow on same element |
| **Primary action count** | Maximum one `primary-500` button per section | Multiple orange buttons competing in same section |

#### Iteration rules

- **Max 3 iterations per stage.** If still failing after 3, report the issue to the user.
- **Fix one category at a time.** Don't try to fix spacing and color in the same iteration.
- **Always re-screenshot after fixes.** Never assume a fix worked without visual confirmation.
- **Stop iterating when:** all 8 checks pass, or you've hit the iteration limit.

### Step 7 — Self-Validation Checklist

Before reporting completion, run these programmatic checks mentally against
your generated code. Every check must pass.

```
□ Every hex value I used appears in tokens.md — no invented colors
□ Every frame uses layoutMode ("HORIZONTAL" or "VERTICAL") — no absolute positioning
□ Every text node uses { family: "Inter" } — no other font families
□ Count of primary-500 fills per section ≤ 1 — no competing CTAs
□ All cornerRadius values match a token (4, 6, 8, 12, 16, 9999) — no arbitrary radii
□ All spacing values are multiples of 4 — no 6px, 10px, 14px, 22px gaps
□ Nested elements use concentric radius (inner = one step smaller than outer)
□ No gradient fills on text nodes
□ All overlines use: fontSize 11, style "Medium", textCase "UPPER", letterSpacing +8%
□ Headings h3+ use negative letterSpacing (-0.5% to -2%)
□ Icon-only interactive elements are ≥ 44×44px
□ Content containers have maxWidth set (≤ 1280px)
```

If any check fails, fix it before reporting completion.

---

## Naming Conventions

**Component variants:**
```
Variant=Primary, Appearance=Solid, Size=SM, State=Default
```

**Screen layer hierarchy:**
```
[Page Name] / Shell
  Header
  Main
    [Section Name]
      Heading Block
      Content Area
```

---

## Error Handling

| Error | Fix |
|-------|-----|
| Font not found | Try/catch, fall back to `{ family:"Roboto", style:"Medium" }` |
| Token not resolved | Log warning, use nearest fallback, never guess |
| Permission denied | Verify Dev/Full seat, file not view-only, re-run `whoami` |
| `combineAsVariants` fails | Ensure all components share the same parent frame |

---

## Additional Resources

- [supporting/tokens.md](supporting/tokens.md) — Complete token → value reference
- [supporting/craft-rules.md](supporting/craft-rules.md) — All craft rules + QA checklist
- [supporting/anti-patterns.md](supporting/anti-patterns.md) — Banned patterns + alternatives
- [supporting/screen-patterns.md](supporting/screen-patterns.md) — Pre-built screen shells (dashboard, auth, settings, data table)

---

## Version History

| Version | Changes |
|---------|---------|
| 2.0.0 | Split into skill + supporting files. Added `STYLE_MODE` param, visual validation protocol with acceptance criteria, self-validation checklist, `!` preprocessing, `context:fork` screen-compose variant, `applyShadow`/`applyBorder` helpers, full craft rules in supporting files |
| 1.1.0 | Added Design Quality Rules, Screen Composition, craft details |
| 1.0.0 | Initial release |
