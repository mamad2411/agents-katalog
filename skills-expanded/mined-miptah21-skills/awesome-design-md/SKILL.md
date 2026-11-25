---
name: awesome-design-md
description: Reference and apply design system specifications from the VoltAgent awesome-design-md collection (Stripe, Linear, Vercel, Notion, etc.). Use this skill to initialize DESIGN.md in the project root or audit/format UI styling decisions.
---

# Awesome Design MD (DESIGN.md)

This skill integrates the **awesome-design-md** paradigm, which uses a structured `DESIGN.md` file in the project root as the "visual source of truth" for AI-native code generation. This prevents generic AI aesthetics and ensures high-fidelity, brand-aligned interfaces.

## When to Invoke

- The user mentions `"awesome-design-md"`, `"DESIGN.md"`, or `"visual source of truth"`.
- The user requests a specific brand's aesthetic (e.g., `"Stripe style"`, `"Linear theme"`, `"Vercel look"`, `"Notion styling"`).
- Building or refactoring UI components and needing a strict design system specification.
- Auditing UI code against specific brand standards.

## Core Workflow

### Step 1: Locate or Initialize the Design System
Check if a `DESIGN.md` file exists in the workspace root.
- If it **does not exist**, ask the user which design aesthetic they prefer (Stripe, Linear, Vercel, Notion, or custom) and initialize it:
  1. Load the corresponding template from the local `references/` directory.
  2. Write it as `DESIGN.md` in the project root.
- If it **does exist**, load and read it before writing any UI code.

### Step 2: Apply Design Primitives to Code
When implementing components or styles:
1. **Define Design Tokens:** Map the colors, font family stacks, font sizes, spacing scales, and border-radii from `DESIGN.md` directly into CSS variables, Tailwind configuration, or utility classes.
2. **Commit to the Aesthetic:** Adhere strictly to the brand’s layout density, border styling, glow/shadow conventions, and text hierarchy.
3. **Avoid Generic fallbacks:** Do not fall back to browser defaults or standard generic styles (e.g., plain system font stacks, standard purple/indigo gradients unless specified).

### Step 3: Run the Visual Compliance Audit
Before finalizing UI changes, inspect the files to verify compliance against `DESIGN.md`:
- Check contrast ratios and palette matches.
- Confirm exact spacing values (no magic numbers outside the spacing scale).
- Verify dark/light mode styles align with the spec.

---

## The DESIGN.md Schema Structure

Every `DESIGN.md` file should follow this structure to remain highly legible to AI:

```markdown
# Brand Design Specification (e.g. Stripe)

## 1. Core Philosophy & Vibe
- Define the general visual tone (e.g., "Refined Slate and Indigo, Trustworthy, Precision").

## 2. Design Tokens
- **Colors:** Primary, Secondary, Background, Accent, Borders (Hex or HSL).
- **Typography:** Display Font, Body Font, Weights, Line Heights.
- **Spacing:** Spacing grid (e.g., 8px base: 4px, 8px, 16px, 24px, 32px, 64px).
- **Radius & Borders:** Border widths, border-radius values, default border colors.
- **Shadows & Glows:** Shadow levels, elevation details, light source directions.

## 3. Core Component Layouts
- **Buttons:** Styling for primary, secondary, and tertiary states.
- **Cards:** Background, borders, hover micro-animations.
- **Inputs & Fields:** Focus ring styling, error state colors, labels.
- **Headers & Navigation:** Visual density, border/separator rules.
```

---

## Available Reference Templates

When initializing `DESIGN.md`, you can leverage these vendor-replicated templates:

> **Reference:**
> - [Stripe Design System](references/Stripe.md) — Clean slate/indigo, trust-focused, blurred gradients, light mode.
> - [Linear Design System](references/Linear.md) — Deep dark mode, crisp borders, high layout density, keyboard cues, micro-glows.
> - [Vercel Design System](references/Vercel.md) — stark geometric minimal contrast, monochrome, clean borders, sharp corners.
> - [Notion Design System](references/Notion.md) — warm clean layout, organic serifs, soft shadows, cozy rounded borders.
