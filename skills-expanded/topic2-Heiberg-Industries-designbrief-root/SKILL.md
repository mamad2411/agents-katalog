---
name: designbrief
description: A library of UI design direction files that provide style guardrails for building tasteful, consistent interfaces. Use when building any UI — select a style or let the AI recommend one based on the project context.
---

# designbrief

A library of rich design direction files — one per UI style — that provide guardrails for building tasteful, consistent interfaces without prescribing exact values.

## How It Works

Each style is a standalone markdown file in `styles/` that defines the **design DNA** of a visual direction: typography families, color theory, spacing philosophy, border/shadow characteristics, layout principles, component behavior, and implementation guidance.

These are **guardrails, not templates**. They define *what kind of* font, color, spacing — not the exact values. The developer (or AI) makes specific choices within the style's constraints.

## When This Skill Activates

Use this skill when the user:
- Asks to build any UI, page, component, or app
- Mentions a specific design style by name
- Asks for style recommendations or comparisons
- Wants to change the visual direction of an existing project

## Workflow

### 1. Determine the Style

**If the user specifies a style** (e.g., "use Bauhaus", "make it glassmorphic"):
- Read the corresponding file from `styles/{style-name}.md`
- Apply its guardrails to all UI decisions

**If the user does NOT specify a style**:
- Read `styles/_index.md` for the full catalog with mood/industry tags
- Ask the user what mood, audience, and industry they're targeting
- Recommend 2-3 styles with brief reasoning
- Let them choose, then load the full style file

### 2. Apply the Style

When generating UI code, use the style file as your design system:

- **Typography**: Choose specific fonts from within the style's recommended families/characteristics
- **Colors**: Build a palette that follows the style's color theory and contrast rules
- **Spacing**: Apply the style's spacing philosophy (generous vs. tight, rhythmic vs. uniform)
- **Components**: Shape buttons, cards, inputs, navbars according to the style's component guidance
- **Layout**: Follow the style's grid and composition principles
- **Effects**: Apply borders, shadows, blur, gradients per the style's visual depth rules
- **Dark/Light Mode**: Check the style's Dark Mode & Light Mode section. If the user hasn't specified, use the style's recommended primary mode. If they ask for both, implement the style's palette adaptation for each.
- **Responsive**: Apply the style's Responsive & Mobile guidance. Ensure touch targets (44px minimum), compress spacing and typography for mobile, and handle any performance concerns (e.g., heavy blur on mobile devices).
- **Content & Voice**: Match headline tone, body copy style, CTA language, and microcopy personality to the style's Content & Voice section.
- **Icons & Illustrations**: Choose icon sets and illustration approaches that match the style's guidance.
- **Accessibility**: Verify contrast ratios per the style's Accessibility section. Implement style-appropriate focus states. Add `prefers-reduced-motion` fallbacks for animations.

### 3. Teach Along the Way

When making a design decision, briefly explain *why* (one sentence) to help the user build taste over time. For example: "Using a warm off-white (#FAF8F5) instead of pure white because Japandi draws from natural materials — pure white feels clinical, not crafted." This is optional but encouraged, especially when the user is learning.

### 4. Stay Consistent

Once a style is selected for a project:
- Reference the style file for every new component or page
- Do not mix styles unless explicitly asked to create a hybrid
- When in doubt about a design decision, re-read the relevant section of the style file
- The style's "Don'ts" section is as important as its "Do's"
- Ensure dark mode, responsive behavior, content tone, and accessibility remain consistent across all pages

## File Structure

```
styles/
├── _index.md              # Catalog of all styles with tags, mood, best-for
├── bauhaus.md             # Each style is a rich guardrail document
├── glassmorphism.md
├── neubrutalism.md
├── flat-design.md
├── ... (21 styles total)
```

## Style File Anatomy

Every style file follows this structure:

0. **Non-Negotiables** — The 3 defining characteristics that MUST be present for the style to be recognizable
1. **Identity** — Name, origin, mood keywords, best-for industries
2. **Typography** — Font families/characteristics, scale philosophy, weight usage
3. **Color** — Palette theory, contrast approach, accent strategy
4. **Spacing & Layout** — Grid system, whitespace philosophy, rhythm, composition
5. **Borders & Shadows** — Radius, depth, elevation, visual effects
6. **Components** — How buttons, cards, inputs, navbars, modals should look and feel
7. **Motion** — Animation philosophy, transition characteristics
8. **Dark Mode & Light Mode** — Palette adaptation, mode preference, implementation
9. **Responsive & Mobile** — Typography scaling, spacing compression, layout collapse, touch targets, performance
10. **Content & Voice** — Headline tone, body copy style, CTA language, microcopy personality
11. **Icons & Illustrations** — Icon style, illustration approach, photography direction
12. **Accessibility** — Contrast verification, focus states, motion sensitivity, screen reader considerations
13. **Do's and Don'ts** — Critical guardrails to maintain style integrity
14. **Implementation Hints** — Tailwind classes, CSS custom properties, token ranges

## Important Notes

- These files define *direction*, not *specification*. Two projects using the same style should look related but not identical.
- Always prioritize readability and accessibility over style purity. If a style's aesthetic conflicts with usability, usability wins. Check the style's Accessibility section for known risks and remediation.
- The user can override any guardrail — the style file is a starting point, not a cage.
- When building for mobile, follow the style's Responsive & Mobile section — adapt the principles to touch targets and smaller viewports rather than abandoning them.
- Match the content tone to the visual style. A Neubrutalism site with corporate copy feels wrong; a Corporate Modern site with slang feels unprofessional. The Content & Voice section guides this.
- When teaching: good design is not arbitrary. Every rule exists for a reason — the "why" matters more than the "what." Help users understand the reasoning behind choices so they build taste over time.
