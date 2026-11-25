---
name: figma-to-vanilla
description: Converting Figma designs into accurate static HTML/CSS/JS implementations using Figma MCP without frameworks. The main set of rules for implementing, adapting, analyzing, and verifying websites based on Figma designs, including layout, responsive behavior, components, styles, assets, animations, and visual verification.
license: MIT
metadata:
  author: "Andrey Gorokhov"
  upstream: "https://github.com/andrewalexeich/figma-to-vanilla"
  upstream_commit: "8a21e0309f88241794b4a3e3ad31f853d512991c"
  upstream_checked: "2026-11-16"
---

# 1. Purpose

These rules are instructions for the AI agent on implementing a static website based on a Figma design.

The main task is to reproduce the provided Figma design in HTML/CSS/JS as accurately as possible, preserving its visual structure, typography, dimensions, colors, spacing, components, and intended responsive behavior.

# 2. Project Architecture

At the beginning of a new project, if its architecture has not been specified by the user and cannot be clearly identified from the existing project structure, the AI agent must ask the user to choose between the two supported architectures:

- **Single-page** — a website consisting of one HTML document.
- **Multi-page** — a website consisting of separate HTML documents for individual pages.

Present this question using interactive selectable options whenever supported by the AI agent.

Do not determine the project architecture based on the number, names, or arrangement of Figma Frames. Do not scan the entire Figma document in advance to determine the website type independently.

If the architecture is already known from the conversation or the existing project structure, do not ask again. Do not change the agreed architecture without the user's approval.

## Single-page

A single-page website is implemented in one HTML document.

Two implementation approaches are supported:

- Implementing the entire page using its complete Figma Frame.
- Implementing individual sections sequentially as the user provides them.

When implementing sections sequentially, work only with the section provided by the user, account for the parts already implemented, and do not rewrite completed code without a valid reason.

Do not create additional HTML documents unless necessary.

## Multi-page

A multi-page website is implemented sequentially, one page at a time. Do not assume that the user will provide all pages at once.

Each page can be implemented in either of two ways:

- **As a whole** — the user provides the complete Figma Frame of the page.
- **Section by section** — the user provides individual page sections sequentially.

Different approaches can be used for different pages and can be changed during implementation.

When implementing a page section by section:

- Work only with the provided sections, account for the parts already implemented, and do not rewrite completed code without a valid reason.
- Do not start the next page until the current page is complete.
- Wait for an unambiguous confirmation from the user that all sections of the current page have been provided and its implementation can be considered complete. Do not require a specific confirmation phrase.
- After receiving confirmation, perform a final review of the entire page.

The final review requires access to the main Figma Frame containing all implemented sections of the page. If it has not yet been provided, ask the user to select and share it through Figma MCP. Do not begin the final review without access to this Frame.

During the final review:

- Check the relative positioning of all sections and the overall page composition.
- Check responsiveness and visual consistency with the complete Figma page.
- Correct any discrepancies within the scope of the current task.

Only after completing the review, agree with the user on proceeding to the next page. Do not start implementing it without the user's confirmation and the corresponding Figma Frame or section.

When moving to the next page, account for the existing project structure, implemented shared components, CSS Variables, and styles.

Do not inspect all Figma pages in advance solely to identify shared components. Compare new elements with previously implemented ones as subsequent pages are provided.

Reuse matching components and styles, avoid duplication, and do not rewrite completed implementations without a valid reason.

## CSS Organization

Use a hybrid CSS organization approach for both Single-page and Multi-page projects, separating styles into three levels:

- **Global CSS** — shared project styles, including reset, CSS Custom Properties, base typography, shared containers, and genuinely global rules.
- **Component CSS** — styles for reusable components. Load them only where the corresponding components are used.
- **Page/Section CSS** — styles specific to an individual page or section. Load them only where they are needed.

For Single-page projects:

- Use one HTML document for the website.
- Organize styles into global, component, and section-specific CSS where appropriate.
- Do not create separate CSS files for individual sections unless this is justified by the project structure.

For Multi-page projects:

- Use a separate HTML document for each page.
- Load global CSS on every page.
- Load component CSS only on pages where the corresponding components are used.
- Load page-specific CSS only on the corresponding page.

Use the following loading order:

1. Global CSS.
2. Component CSS.
3. Page/Section CSS.

Do not load unnecessary CSS files through a shared stylesheet or global `@import` statements.

Do not create a separate CSS file for every minor element.

Preserve the existing project structure if it is already organized differently. Do not enforce a mandatory directory structure or require a build tool.

Do not create HTML or CSS files in advance for pages whose implementation has not yet started.

Production output must contain ready-to-use HTML pages that do not depend on JavaScript runtime fetching of HTML fragments.

# 3. Interactive Questions

When clarification or user input is needed during the project, use interactive questions with selectable answer options whenever supported by the AI agent.

- Present clear and concise answer options.
- Allow the user to select one or multiple options, depending on the question.
- Use free-text input when the answer cannot reasonably be represented by predefined options.
- Do not ask questions whose answers are already known from the conversation or project files.

If the AI agent does not support interactive questions, use a clear text-based question instead.

On the first task in a new environment, check the toolchain before implementing (`references/preflight.md`) and offer whatever is missing as one multiselect question.


# 4. Reference Rules

Detailed project rules are divided by task and located in the `references/` directory.

Do not read all reference files automatically for every task.

Before starting work, determine which aspects are affected by the current task and read only the corresponding reference files.

If a task affects multiple aspects, read all corresponding files.

If it becomes clear during the work that the task affects an additional area, read the corresponding reference file before implementing it.

| File | Read when the task involves |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `references/mcp-rules.md` | working with Figma MCP, retrieving data from Figma, analyzing a specific design, or visual verification through Figma MCP |
| `references/structure.md` | project structure, `index.html`, HTML/CSS/JS organization, JavaScript logic, favicon |
| `references/fluid-responsive.md` | dimensions, units of measurement, breakpoints, responsive behavior, fluid layout, behavior below/above 1920px, containers |
| `references/css-conventions.md` | CSS, BEM, classes, CSS variables, typography, colors, dimensions, and general CSS conventions |
| `references/figma-components.md` | Figma Components, Component Sets, Variants, Component Properties, Instances, component states |
| `references/design-system.md` | initial UI Kit analysis, design system preparation, identifying shared styles and reusable elements, and maintaining the design system across pages |
| `references/figma-layout.md` | Figma Auto Layout, Layout Grid, spacing, Grid/Flexbox, container structure, `position: absolute` |
| `references/assets.md` | fonts, images, SVG, favicon, WebP, asset import and processing |
| `references/animations.md` | animations, transitions, interactive states, storyboard, Prototype connections, GSAP |
| `references/verification.md` | visual verification, Live Server, responsive testing, and final result verification |
| `references/production-git.md` | minification, production files, `.gitignore`, Git, and GitHub |
| `references/sync-and-contribute.md` | checking this copy against the author's repository before work, updating it, or preparing a pull request with new rules |
| `references/preflight.md` | the first task in a new environment, checking the toolchain, and installing what is missing |

## Basic Combinations

For initial UI Kit analysis and design system preparation:

1. `mcp-rules.md`
2. `design-system.md`
3. `css-conventions.md`
4. `figma-components.md`
5. `figma-layout.md` — if layout parameters need to be analyzed
6. `fluid-responsive.md` — if responsive typography or layout needs to be analyzed

For ordinary Figma implementation:

1. `mcp-rules.md`
2. `structure.md`
3. `css-conventions.md`
4. `figma-layout.md`
5. `fluid-responsive.md`
6. `figma-components.md` — if Components/Variants are used
7. `design-system.md` — if a UI Kit or shared design system has already been analyzed, or if existing shared styles and components need to be reused across pages
8. `assets.md` — if images, fonts, or other assets are used
9. `verification.md` — before completing the task

For modifying existing HTML/CSS/JS:

1. `structure.md`
2. `css-conventions.md` — if CSS is affected
3. `fluid-responsive.md` — if responsive behavior is affected
4. `verification.md` — if the change affects the visual result

For animations:

1. `mcp-rules.md`
2. `animations.md`
3. `structure.md`
4. `css-conventions.md`
5. `figma-layout.md` — if the animation is related to layout
6. `fluid-responsive.md` — if the animation depends on a breakpoint
7. `verification.md`

For working with assets only:

1. `assets.md`
2. `structure.md` — if HTML/CSS references need to be changed

For production/Git:

1. `production-git.md`
2. `structure.md`
3. `assets.md`
4. `verification.md` — when production files or the final website need to be verified

## Rule for Figma

If a task involves a specific Figma design, use `mcp-rules.md` first, then read only the reference files related to the identified structure and task.

When a task involves the initial analysis of a UI Kit or design system, read `mcp-rules.md` first, followed by `design-system.md` and the corresponding reference files for the materials being analyzed or transferred.

For example, if a section needs to be implemented using Auto Layout, Components, and responsive versions, the following files must be read:

`mcp-rules.md`
`figma-layout.md`
`figma-components.md`
`fluid-responsive.md`
`structure.md`
`css-conventions.md`
`verification.md`

Do not read `animations.md`, `production-git.md`, or `assets.md` if the current task does not involve them.

## Priority Rule

Reference file rules are mandatory within the areas they describe.

If the current task involves multiple reference files, all applicable rules must be followed.

Do not consider the need to read a reference file as grounds for changing parts of the project that are unrelated to the current task.

If a reference file rule conflicts with the AI agent's own assumption, the project rule takes priority.

If two project rules genuinely conflict with each other, do not choose an option independently. Identify the conflict and ask the user for clarification.

## Rule for Re-reading

If a required reference file has already been read during the current task and its rules have not changed, it does not need to be read again unless necessary.

When moving on to a new task, determine the necessary reference files again based on the current context.