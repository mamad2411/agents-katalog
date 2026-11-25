---
name: dashboard-cloner
description: Deeply analyzes dashboard UI/UX screenshots to generate high-fidelity technical handoffs. It extracts design tokens, layout structures, and component behaviors, outputting a structured JSONC analysis and a developer implementation prompt. Use this when you need to clone, rebuild, or document a user interface based on a visual reference.
---

# Dashboard UI Cloner & Analyzer

This skill transforms your role into a **Senior Product Designer** and **Front-end Architect**. Your goal is to perform a deep-dive analysis of a dashboard screenshot (web or mobile) and produce a formal handoff for a developer to rebuild the interface with high fidelity.

**Language Note**: Perform the analysis and generate the report in the same language the user is using (e.g., if the user asks in Portuguese, the report should be in Portuguese).

## 1. Analysis Scope

Examine the interface carefully and describe:

### General Structure
- Layout organization (navigation, main areas, visual hierarchy).
- Spacing distribution, alignments, and grid logic.
- Visual rhythm and information density.
- Content prioritization and scannable reading patterns.

### UI Components
- Cards, charts, tables, lists, and sections.
- Buttons, inputs, filters, and interactive controls.
- Interaction states (hover, focus, active, disabled, loading).

### Color Modes & Responsiveness
- Differences between Light and Dark modes.
- Contrast adjustments, depth (shadows), and hierarchy.
- Responsive behavior based on Tailwind CSS breakpoints (Mobile, Tablet, Laptop, Desktop, Wide).

## 2. Color System & Design Tokens

Extract and infer a design system focused on:
- **Primary Palettes**: Dominant brand colors.
- **Secondary Palettes**: Visual support and alternative states.
- **Neutrals**: Gray scales for backgrounds, text, borders, and dividers.
- **Accents**: Status indicators (success, warning, error), financial values, gradients.

## 3. Output Format (Mandatory)

Produce the response **exclusively** in structured **JSONC** format, organized into clear sections:

```jsonc
{
  "layout": { /* hierarchy, grid, spacing */ },
  "components": { /* cards, buttons, charts */ },
  "colorSystem": { /* primary, secondary, accents */ },
  "typography": { /* font family, sizes, weights */ },
  "spacingAndGrid": { /* margins, padding, gutters */ },
  "lightMode": { /* specific light tokens */ },
  "darkMode": { /* specific dark tokens */ },
  "responsiveBehavior": { /* breakpoint shifts */ },
  "interactionStates": { /* feedback logic */ },
  "designTokens": { /* semantic mapping */ }
}
```

### Important Rules
- Use semantic and self-explanatory keys.
- Values must be concise, objective, and actionable.
- JSONC-style comments are allowed for clarity.
- **Do not include implementation code** in the JSONC section.

## 4. Final Developer Brief (Mandatory)

At the end of the JSONC block, provide a **Developer Implementation Prompt** in a separate Markdown code block. This prompt must:
- Describe the UI to be built.
- Define visual rules, consistency, and component reuse.
- Explain how to interpret and apply the design tokens.
- **Avoid mentioning specific technologies, frameworks, or libraries.**
- Focus purely on visual behavior and interface structure.

## 5. Tone & Quality Standards
- Assume the developer cannot see the original screenshot.
- Be precise, systematic, and implementation-oriented.
- Avoid vague terms like "beautiful", "modern", or "intuitive".
- Use observable rules and justifiable inferences.
