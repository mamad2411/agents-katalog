---
name: "claude-design-branding"
description: "Create consistent brand systems with Claude Design including logos, colors, and typography"
---

# Claude Design Brand System Setup

## When to activate

- First time configuring Claude Design for a project or company — no prior design system exists in the tool
- Starting a new client project in Claude Design where the client has an existing brand
- Design outputs from Claude Design do not match company brand (colors are off, typography is wrong, spacing feels inconsistent)
- Team members are getting inconsistent results across sessions because there is no shared starting point

## When NOT to use

- One-off prototype that will not be reused or handed off — the setup cost exceeds the value
- Exploring a brand-new visual identity where no existing brand exists yet — you are defining the brand, not translating it
- Quick throwaway mockup for one-time validation — skip setup and prompt directly

## Instructions

### Step 1: Brand Foundation

Before touching colors or typography, give Claude the context that governs all visual decisions.

Provide:

- Company name and industry
- Target audience (be specific — "enterprise procurement managers aged 35-55" is more useful than "B2B")
- Three brand personality adjectives (e.g., "precise, approachable, modern" or "bold, playful, energetic")
- Tone descriptor: professional / casual / playful / authoritative
- Any existing brand statement or positioning line

Claude uses this to generate foundational visual principles — the reasoning layer that sits behind every color and spacing choice. When you later ask "does this look right," Claude is evaluating against these principles, not guessing.

Document the output. Paste it at the top of every new session as part of your session primer.

### Step 2: Color System

Define all color roles explicitly. Do not let Claude infer palette from a single primary color — name every role.

**Primary palette:**
- Primary: the dominant action color (buttons, links, key highlights)
- Primary hover: darkened 10-15% for interaction states
- Primary subtle: lightened 85-90% for backgrounds and tints

**Secondary palette:**
- Secondary: supporting accent color
- Secondary hover
- Secondary subtle

**Neutral palette:**
- Neutral 50 through Neutral 950 (or equivalent scale) — used for surfaces, borders, text

**Semantic colors** — always specify hex values, do not rely on defaults:
- Success: typically a green (#16A34A as a reference point)
- Warning: typically amber (#D97706)
- Error: typically red (#DC2626)
- Info: typically blue (#2563EB)

Each semantic color needs a foreground pair — the text color that sits on top of it and passes WCAG AA contrast (4.5:1 for body text, 3:1 for large text).

**Surface colors:**
- Background: page-level background
- Surface: card and panel background
- Surface raised: elevated components (modals, dropdowns)
- Overlay: scrim behind modals

**Text colors:**
- Text primary: body text on light surfaces
- Text secondary: supporting text, labels
- Text disabled: muted, non-interactive text
- Text inverse: text on dark or colored backgrounds

Include explicit WCAG AA validation for every text/background combination you define. Claude will flag failures if you ask, but it is faster to validate at definition time than to discover contrast issues during component generation.

### Step 3: Typography Scale

Specify font pairings that match brand personality — the pairing choice signals more about brand character than any other single decision.

Common pairing patterns:

- Authoritative/enterprise: geometric sans for headings (Inter, DM Sans) + humanist sans for body (Source Sans Pro)
- Editorial/premium: serif for display (Playfair Display, Libre Baskerville) + sans for body (Inter)
- Technical/developer: mono for code accent (JetBrains Mono) + neutral sans for everything else (Inter)
- Playful/consumer: rounded sans for headings (Nunito, Poppins) + neutral sans for body

Define the full scale with semantic names, not size numbers:

**Headings:**

| Token | Size | Weight | Line height | Use |
|---|---|---|---|---|
| display | 3rem | 700 | 1.1 | Hero headings, splash screens |
| h1 | 2.25rem | 700 | 1.2 | Page titles |
| h2 | 1.875rem | 600 | 1.25 | Section headings |
| h3 | 1.5rem | 600 | 1.3 | Subsection headings |
| h4 | 1.25rem | 600 | 1.35 | Card headings, sidebar titles |

**Body:**

| Token | Size | Weight | Line height | Use |
|---|---|---|---|---|
| body-large | 1.125rem | 400 | 1.6 | Lead paragraphs, introductions |
| body | 1rem | 400 | 1.6 | Default paragraph text |
| body-small | 0.875rem | 400 | 1.5 | Supporting text, metadata |
| caption | 0.75rem | 400 | 1.4 | Image captions, fine print |

**Utility:**

| Token | Size | Weight | Line height | Use |
|---|---|---|---|---|
| label | 0.875rem | 500 | 1.2 | Form labels, table headers |
| overline | 0.75rem | 600 | 1.2 | Category labels, section markers — always uppercase |
| code | 0.875rem | 400 | 1.6 | Inline code, code blocks |

Claude Design applies these tokens automatically to every generated element once the system is established. You do not need to re-specify sizes per prompt.

### Step 4: Logo Guidelines

Provide Claude with constraints it must respect in every output. This prevents Claude from improvising with your logo in ways that violate brand standards.

Specify:

- **Variants available:** primary (full logo), reversed (white/light version for dark backgrounds), icon-only (mark without wordmark)
- **Approved color combinations:** primary logo on white, reversed logo on primary-color background, etc.
- **Clear space rule:** minimum clear space on all sides, expressed as a multiple of a logo unit (typically the height of the mark's x-height or cap height)
- **Minimum sizes:** minimum width in pixels for digital use, minimum width in millimeters for print
- **Prohibited modifications:** no color alteration, no rotation, no stretching, no drop shadows, no outline strokes

If you have a brand guide PDF with logo specifications, upload it during Session 0. Claude reads and respects these constraints in subsequent outputs without you needing to re-specify them per session.

### Step 5: Component Library — Start with High-Frequency Components

Build the components Claude will use most often first. High-frequency components appear in almost every screen; getting them right eliminates the largest source of brand drift.

Priority order:

**Buttons** — define four base variants:
- Primary: filled, uses `color-primary`, white text
- Secondary: outlined, `color-primary` border and text, transparent background
- Ghost: no border, `color-primary` text, transparent background
- Destructive: filled, uses `color-error`, white text

For each variant, specify: height, horizontal padding, border radius, font token, and all interaction states (default, hover, active, focus-visible, disabled). Disabled state must use reduced opacity or a specific muted color — never remove the element from the layout.

**Form inputs** — define: text input, textarea, select, checkbox, radio button. For each: height (inputs), border color (default, focus, error, disabled), label position, helper text position, error message styling.

**Cards** — define variants by content type:
- Content card: image + heading + body + optional CTA
- List card: icon or avatar + heading + secondary text + optional action
- Stat card: metric value + label + optional trend indicator

Include hover state (elevation change or border highlight) for interactive cards.

**Navigation** — define: primary header (logo + nav links + CTA + mobile menu trigger), sidebar nav (grouped links + active state + nested links), breadcrumb.

For every component: specify exact spacing (use your spacing scale tokens, not pixel values), colors (use your color tokens), border radius (consistent with your global radius token), typography tokens, and all interaction states.

### Step 6: Documentation Layer

For each component in your library, write a compact usage contract. This is the layer that prevents misuse and makes the system self-teaching for team members.

For each component document:

**When to use** — specific scenarios where this component is the right choice. "Use primary button for the single highest-priority action on a page or modal."

**When NOT to use** — anti-patterns. "Do not use primary button for more than one action per screen. Do not use for navigation — use a link instead."

**Related components** — navigation guide. "If you need a secondary action, use secondary button or ghost button. If you need inline navigation, use a text link."

**Accessibility notes** — minimum requirements:
- Focus state: visible focus ring (2px offset, `color-primary` or equivalent high-contrast ring)
- ARIA role: specify for non-native elements
- Color independence: never convey state through color alone (add icon or text label alongside color)
- Minimum touch target: 44x44px for interactive elements

### Step 7: Export and Maintain

Output your complete design system in three formats simultaneously so it can be consumed by any downstream toolchain.

```css
/* CSS custom properties — paste into :root in global stylesheet */
:root {
  /* Color — primary */
  --color-primary: #2563EB;
  --color-primary-hover: #1D4ED8;
  --color-primary-subtle: #EFF6FF;

  /* Color — semantic */
  --color-success: #16A34A;
  --color-warning: #D97706;
  --color-error: #DC2626;
  --color-info: #2563EB;

  /* Color — surface */
  --color-background: #FFFFFF;
  --color-surface: #F9FAFB;
  --color-surface-raised: #FFFFFF;

  /* Color — text */
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;
  --color-text-disabled: #D1D5DB;
  --color-text-inverse: #FFFFFF;

  /* Typography */
  --font-display: 'Inter', sans-serif;
  --font-body: 'Inter', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
  --spacing-12: 3rem;
  --spacing-16: 4rem;

  /* Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;
}
```

```json
{
  "color": {
    "primary": { "value": "#2563EB" },
    "primary-hover": { "value": "#1D4ED8" },
    "primary-subtle": { "value": "#EFF6FF" },
    "success": { "value": "#16A34A" },
    "warning": { "value": "#D97706" },
    "error": { "value": "#DC2626" },
    "info": { "value": "#2563EB" },
    "background": { "value": "#FFFFFF" },
    "surface": { "value": "#F9FAFB" },
    "text-primary": { "value": "#111827" },
    "text-secondary": { "value": "#6B7280" },
    "text-disabled": { "value": "#D1D5DB" },
    "text-inverse": { "value": "#FFFFFF" }
  },
  "spacing": {
    "1": { "value": "0.25rem" },
    "2": { "value": "0.5rem" },
    "4": { "value": "1rem" },
    "6": { "value": "1.5rem" },
    "8": { "value": "2rem" }
  },
  "radius": {
    "sm": { "value": "0.25rem" },
    "md": { "value": "0.5rem" },
    "lg": { "value": "0.75rem" },
    "full": { "value": "9999px" }
  }
}
```

```js
// tailwind.config.js — extend theme with brand tokens
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#2563EB',
          hover: '#1D4ED8',
          subtle: '#EFF6FF',
        },
        success: '#16A34A',
        warning: '#D97706',
        error: '#DC2626',
        info: '#2563EB',
        surface: '#F9FAFB',
        'text-primary': '#111827',
        'text-secondary': '#6B7280',
        'text-disabled': '#D1D5DB',
      },
      borderRadius: {
        sm: '0.25rem',
        md: '0.5rem',
        lg: '0.75rem',
      },
    },
  },
}
```

Version-control the tokens JSON file. Treat it as source of truth — the CSS and Tailwind configs derive from it. When the brand evolves, update the tokens JSON first, then regenerate the other formats.

### Validation Step

Before using the system on any real project, run a validation check. Generate one test component — a button group containing primary, secondary, ghost, and destructive variants — and verify:

- Colors match your defined hex values exactly
- Typography tokens are applied (not Claude's defaults)
- Spacing and border radius are consistent with your scale
- Hover states are present and correct

If output looks off in any dimension, re-upload your finished product screenshots and the session primer, then regenerate. Misalignment at validation time is almost always caused by incomplete context in Session 0, not Claude Design drift.

Fix it before building real screens. Correcting brand drift across 12 generated screens is expensive. Correcting it at the button-group stage costs one prompt.

## Example

An agency setting up a client e-commerce brand — sportswear company, direct-to-consumer, target audience 25-40 active urban professionals.

**Session 0 color system prompt:**

```
Define the complete color system for Velo, a sportswear brand.
Personality: bold, energetic, precise.
Primary: #E11D48 (rose-600). Compute primary-hover at 15% darker, primary-subtle at 90% lighter.
Secondary: #0EA5E9 (sky-500). Same derivation.
Neutral scale: use slate (slate-50 through slate-950).
Semantic: success #16A34A, warning #D97706, error #DC2626, info #0EA5E9.
Surface: background white, surface slate-50, surface-raised white.
Text: primary slate-900, secondary slate-500, disabled slate-300, inverse white.
Output as CSS custom properties, design tokens JSON, and Tailwind config extension.
Validate WCAG AA contrast for all text/background pairs and flag failures.
```

**Expected output:** complete token set in all three formats, with a contrast validation table noting any failures (white text on primary-subtle will fail — Claude should flag it and suggest slate-900 or primary as the correct foreground).

**Subsequent session use:** paste the 150-word session primer (brand personality, primary color, typography pair) at the start of every new session. Claude applies the full token set without re-uploading files. Product page, cart drawer, checkout flow — all generated with consistent brand application across sessions.
