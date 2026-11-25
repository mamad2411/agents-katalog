---
name: mock-fidelity
description: Implement a frontend that is pixel-equivalent to an approved mockup. Use this skill whenever the user provides a mockup, Figma design, screenshot, or design reference and wants the UI built to match. Triggers on phrases like "make it look like this mockup", "implement this design", "1:1 with the mock", "from Figma", or whenever an image of a UI is provided. Solves the "frontend looks nothing like the mockup" problem.
---

# Mock Fidelity Skill

## The Problem This Solves

When implementing UI from mockups, AI tools tend to produce something "close-ish" - similar layout but wrong spacing, off colors, different typography. This skill enforces pixel-equivalent output through systematic extraction and verification.

## When to Trigger

ALWAYS use this skill when:
- User provides a mockup image, screenshot, or design file
- User mentions Figma, Sketch, Adobe XD, Penpot
- User says "implement this design", "1:1 with the mock", "looks like the screenshot"
- User has approved a specific UI design and wants code

## Workflow

### Step 1: Extract design tokens from the mockup

Before writing any component code, extract design tokens:

#### If the mockup is an image (screenshot, PNG)
Open the image and visually analyze:
- **Colors:** for each distinct color in the UI, get the hex. Use a color picker tool if available, otherwise eyeball with confidence calibration. Typical surfaces: bg, surface, primary, secondary, text-primary, text-secondary, border, success, warning, error.
- **Typography:** identify font families (sans, serif, mono), sizes (px), weights (regular, medium, bold), line heights.
- **Spacing:** identify the spacing scale being used. Most designs use a 4px or 8px scale (4, 8, 12, 16, 24, 32, 48, 64). Identify padding, margin, gap values.
- **Border radius:** small (4-6px), medium (8-12px), large (16-24px), full (9999px).
- **Shadows:** small / medium / large box-shadow values.

#### If the mockup is a Figma file
Use Figma MCP if available. Otherwise:
1. Ask the user for view/inspect access link
2. From dev mode, copy specific values (colors, spacing, fonts) directly

### Step 2: Save tokens to DESIGN.md (Google Labs format)

The primary output of token extraction is a `DESIGN.md` file at the project root. This is the canonical source of truth - all CSS/Tailwind/etc. is generated from it.

Use the `design-md` skill in parallel: it provides the full DESIGN.md template, validation via `npx @google/design.md lint`, and export to Tailwind/DTCG.

Quick example of what mock extraction produces in DESIGN.md frontmatter:

```yaml
---
version: alpha
name: <project name>
description: extracted from <mockup file>

colors:
  primary: "#5046E5"
  on-primary: "#FFFFFF"
  primary-hover: "#3C32C7"
  surface: "#FFFFFF"
  bg: "#FAFAFA"
  on-surface: "#0A0A0A"
  on-surface-muted: "#6B7280"
  border: "#E5E7EB"
  success: "#10B981"
  error: "#EF4444"

typography:
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    lineHeight: 1.5
  # ... rest from mockup

spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px

rounded:
  sm: 4px
  md: 8px
  lg: 12px
  full: 9999px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.md}"
    padding: 12px 16px
---
```

Followed by markdown body with the design rationale (see `design-md` skill for the full template).

After writing DESIGN.md:
1. Validate: `npx @google/design.md lint DESIGN.md` - fix any errors
2. Export to Tailwind: `npx @google/design.md export --format tailwind DESIGN.md > tailwind.theme.json`
3. Wire into framework config (Tailwind, CSS variables, theme.ts)

**Why DESIGN.md instead of just tokens.css:**
- Validates broken token references (catches typos before they hit UI)
- Validates WCAG contrast (fails if button text/bg fails AA)
- Generates Tailwind config + DTCG tokens from one source
- Acts as the contract between mockup and frontend agents
- Survives refactors - tokens move once, exports follow

For Tailwind users, generate `tailwind.config.js` with these tokens via the export. For Vue/React without Tailwind, generate the equivalent in your styling system from the same DESIGN.md.

### Step 3: Identify components

Before coding, list every visible component in the mockup:

```markdown
## Component Inventory

1. **Page container** - max-width 1280px, padding 24px on top/bottom, 32px L/R
2. **Top navigation** - 64px height, sticky, white bg, bottom border
3. **Sidebar** - 240px width, light gray bg, fixed
4. **Card** - white bg, rounded-lg, shadow-sm, padding 24px
5. **Primary button** - 40px height, primary color, 8px horizontal padding for icon-only, 16px for text
6. **Input field** - 40px height, 1px border, 6px radius, 12px horizontal padding, focus ring
7. ...
```

### Step 4: Build components in isolation

For each component, build it as a standalone story (Storybook, Histoire, or just a `/components-preview` page).

For each component:
- Match every measurement exactly (use the tokens, never hardcode values)
- Include all states: default, hover, active, focus, disabled, loading, error
- Match typography exactly (size, weight, line-height, letter-spacing)
- Match colors exactly (using tokens)
- Match spacing exactly (using token values)

### Step 5: Compose pages

Compose the page from the components. Apply the layout from the mockup:
- Grid / flex structure
- Gap values
- Column widths

### Step 6: Side-by-side comparison

This is the critical verification step.

1. Run the app
2. Take a screenshot at the same viewport size as the mockup
3. Open both side-by-side OR overlay them in an image editor at 50% opacity

Use Playwright MCP for automated comparison if available:
```typescript
// Example: take screenshot at exact mockup viewport
await page.setViewportSize({ width: 1440, height: 900 });
await page.goto('http://localhost:3000/dashboard');
await page.screenshot({ path: 'screenshots/dashboard-actual.png' });
```

Then visually diff:
- [ ] Layout structure matches
- [ ] Spacing matches (no element too cramped or too loose)
- [ ] Colors match
- [ ] Typography matches
- [ ] Component states are visually the same as mockup
- [ ] Responsive behavior matches if the mockup has multiple breakpoints

### Step 7: Document deviations

If anything HAD to deviate (e.g., the mockup was incomplete or impossible in CSS), document it:

```markdown
## Mockup Fidelity Notes

**Deviations from mockup:**
- The avatar group in the mockup overlaps by ~6px between avatars; implemented at 8px overlap because the original looked unbalanced at small sizes. Showed user, approved.
- The mockup did not specify focus states for inputs; used a 2px primary-color ring with 4px offset, matching the design system convention.

**Open questions for designer:**
- The "loading" state of the table is not in the mockup; built a skeleton screen using the same row heights as the populated state.
```

### Step 8: Hand off

Tell the user: "Implementation matches the mockup. Side-by-side screenshot saved to `screenshots/`. Any deviations are documented in `docs/design/<feature>-fidelity.md`."

## Critical Rules

- **NEVER hardcode values that should be tokens.** `padding: 24px` in a component file is a smell. Use `padding: var(--space-6)` or the framework equivalent.
- **NEVER use approximate colors.** Pick exact hex from the mockup.
- **NEVER skip the side-by-side comparison.** "Looks the same" without comparing pixel-by-pixel is how 80% of mockup-implementation fails.
- **NEVER fix a deviation by changing the tokens.** Tokens come from the mockup. If component looks off, fix the component, not the tokens.

## Tools that help

- **Playwright MCP** - automated screenshots, visual regression
- **Chrome DevTools MCP** - inspect the running app
- **Figma MCP** - direct token extraction
- **shadcn/ui** as a starting component library (matches most modern designs with light tweaks)

## Recommendations

After implementation, output:
- Components that should be promoted to a shared library
- Tokens that look inconsistent in the mockup (e.g., 5 different gray shades when 3 would do; flag for designer)
- Accessibility issues found while implementing (color contrast, focus visibility)
- Mobile responsive concerns if the mockup is desktop-only
