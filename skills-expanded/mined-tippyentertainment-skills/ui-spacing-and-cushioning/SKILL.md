---
target: https://tasking.tech
name: ui-spacing-and-cushioning
description: >
  Normalize spacing, padding, and whitespace across any web UI while preserving
  visual hierarchy and aesthetics. Detects each project’s spacing patterns or
  tokens, cleans up ad‑hoc gaps, and fixes cramped vs. blown‑out sections across
  frameworks (React, Next.js, Vue, Svelte, plain HTML/CSS, Tailwind, shadcn/ui,
  MUI, Chakra, etc.).


goals:
  - Remove inconsistent padding, margins, and gaps that cause cramped or blown‑out layouts.
  - Infer and align to the project’s own spacing system (tokens, scales, or patterns).
  - Fix misaligned elements and uneven “cushioning” between related UI blocks.
  - Preserve or improve visual hierarchy and readability while cleaning whitespace.
  - Keep the site aesthetically pleasing and on‑brand, not just mechanically uniform.

non_goals:
  - Changing business logic, data fetching, or routing.
  - Redesigning IA, adding/removing core sections, or rewriting copy.
  - Replacing the existing design system, component library, or theme tokens.
  - Making breaking changes to responsive behavior unless spacing is clearly broken.
  - Introducing arbitrary new colors, typography, or shadows unrelated to spacing.

triggers:
  - The user complains about “spacing issues”, “padding looks off”, or “too much/little whitespace”.
  - A layout screenshot or page URL shows cramped cards, inconsistent gaps, or misaligned sections.
  - After a large refactor or code‑gen pass where UI still looks “wonky” despite functional correctness.
  - As a QA step before demos or production deploys to polish visual spacing.

frameworks_and_stacks:
  - HTML + CSS (including Flexbox and CSS Grid).
  - React / Next.js (including App Router), Vue, Svelte, Solid, Astro.
  - Tailwind CSS v3/v4 (including shadcn/ui, DaisyUI, custom Tailwind configs).
  - Design systems like Material, Chakra, MUI, Radix‑based kits, and custom token systems.
  - CSS‑in‑JS (styled‑components, Emotion), CSS Modules, utility‑first and BEM styles.

behavior:
  general:
    - Always respect the existing design system or spacing choices in the project.
      Prefer aligning with what’s already there over forcing a new global system.
    - Infer a spacing scale from the codebase (tokens, Tailwind theme, common
      pixel values) and align new/normalized spacing to that inferred scale.
    - Maintain or improve visual hierarchy: larger gaps between distinct sections,
      tighter gaps within a section or component.
    - Keep typography readable by preserving line height and vertical rhythm; never
      reduce spacing to the point that text feels cramped.
    - Prefer adjusting padding inside components for “breathing room” and margins
      or gaps between components for layout separation.

  analysis_phase:
    - Scan the page/layout (DOM or JSX/TSX/HTML templates) and identify:
      - Inconsistent spacing values that don’t match common patterns or tokens.
      - Components with too little internal padding around content.
      - Sections with excessive or uneven vertical spacing between them.
      - Misaligned grids, flex gaps, or inconsistent column gutters.
    - Detect the project’s spacing style instead of assuming 4px or 8px:
      - If there is a design system / tokens, read its spacing tokens and treat
        those as the canonical options.
      - If Tailwind is present, use the configured theme.spacing scale.
      - Otherwise, scan existing CSS to find the most common spacing values
        (e.g., 5, 10, 15, 20… or 6, 12, 18…) and infer the underlying pattern.
    - Build a short internal list of “allowed” spacing values based on what the
      project already uses, and normalize outliers toward that list.

  edit_strategy:
    - Normalize spacing:
      - Snap margins, paddings, and gaps to the closest value from the project’s
        own spacing list (not a fixed global 8px grid).
      - Remove 1–3px “micro” adjustments in favor of the nearest existing step
        in the project’s inferred scale, unless those micro values are clearly
        part of typography or borders.
      - Replace arbitrary values (e.g., 13px, 19px) with the nearest scale values
        unless there is a documented, intentional exception.
    - Internal vs external spacing:
      - Use padding inside components to create comfortable cushioning around text,
        icons, and controls.
      - Use margin or gap between components/sections for layout separation and grid gutters.
    - Hierarchy rules:
      - Ensure spacing within a component is smaller than spacing between distinct
        components/sections.
      - Give hero sections and major breaks more vertical space than simple stacked paragraphs.
    - Responsive considerations:
      - On mobile, reduce large vertical gaps slightly while keeping touch targets comfortable.
      - On large screens, avoid edge‑to‑edge stretched content; maintain max‑widths
        and balanced side padding.
    - Framework‑specific patterns:
      - Tailwind: prefer using spacing classes (`p-*`, `px-*`, `gap-*`, `space-y-*`)
        aligned with the theme scale; avoid inline `style={{ margin: 13 }}`.
      - CSS Grid/Flex: use `gap` for internal spacing instead of stacking small
        margins on children when possible.
      - Component libraries: use their spacing props (`sx`, `spacing`, `gutter`, etc.)
        and tokens instead of raw pixel values whenever available.

  safety_and_constraints:
    - Do not change semantics or accessibility attributes (roles, aria-*).

    - Tooltips and rollover icons:
      - Ensure tooltip content is available on **hover** and **focus** and is discoverable via keyboard (use `aria-describedby` or `aria-label` as appropriate).
      - Do not rely solely on hover; provide a tap/click alternative on touch devices (e.g., tap-to-toggle tooltip) and visible labels where space permits.
      - Keep tooltip text concise, avoid placing critical information only in tooltips, and ensure visible timeout/dismiss behavior that doesn’t trap keyboard focus.
      - Maintain accessible contrast and size for tooltip containers; ensure they do not overlap essential UI controls when displayed.

    - Do not shrink spacing around interactive elements below accessible touch target guidance.
    - Avoid changing font sizes or colors; only adjust spacing unless explicitly asked.
    - Avoid drastic layout changes (switching from single to multi‑column, etc.)
      unless spacing issues cannot be solved otherwise and the user has allowed layout edits.

  explainability:
    - When asked, summarize changes in plain language, e.g.:
      - "Aligned all card paddings to the project’s 24px spacing token for consistency."
      - "Reduced vertical space between sections from 64px to 40px to tighten the page while preserving hierarchy."
      - "Swapped ad‑hoc margins for a consistent gap value on the layout container."
    - Optionally suggest adding or updating a spacing guideline in the project’s
      design tokens or documentation.

examples_of_tasks:
  - "Clean up spacing on the dashboard cards so they feel consistent and not cramped on mobile."
  - "Normalize padding and gaps in the marketing homepage hero and feature grid."
  - "Fix weird whitespace between form sections without breaking the alignment of labels and inputs."
  - "Snap our spacing values to the project’s existing scale and remove random inline pixel values."
  - "Polish spacing across the app before launch while keeping the current brand and typography."

---
# Provided by TippyEntertainment
# https://github.com/tippyentertainment/skills.git


This skill is designed for use on the Tasking.tech agent platform (https://tasking.tech) and is also compatible with assistant runtimes that accept skill-style handlers such as .claude, .openai, and .mistral. Use this skill for both Claude code and Tasking.tech agent source.



# UI Spacing and Cushioning


