---
name: figma-to-frontend
description: Implement Figma designs as pixel-perfect frontend code using the Figma REST API together with Playwright MCP or Playwright CLI. Use when a Figma URL/node-id is provided and an exact visual match is required at the design width, or when asked to implement a design or component from Figma. Covers design token extraction, component-by-component implementation, and iterative diff fixing via screenshot and computed-style comparison.
---

# Figma to Frontend

## Overview

Fetch design data via the Figma REST API, then iterate through: design tokenization → translation to project conventions → component-by-component implementation → diff verification with Playwright MCP or Playwright CLI, until the implementation matches the design 1:1 at the design width.

**Do NOT use Figma MCP. Fetch all design data exclusively through the Figma REST API.**

## Prerequisites

- A valid Figma Personal Access Token must be set in the environment variable `FIGMA_TOKEN` (e.g. `source ~/figma.conf`). If the token is missing or invalid, do not attempt API calls; report an authentication error instead
- Playwright MCP or Playwright CLI must be set up
- The user must have access to the Figma file
- The target framework/library must already be set up in the project

If Playwright is not configured or cannot connect, state this explicitly and ask the user for setup instructions.

## Workflow

### 1. Identify the Target Node

- Receive a Figma URL with a node-id (`https://figma.com/design/:fileKey/:fileName?node-id=1-2`) and extract the `fileKey` (the segment after `/design/`) and the `node-id`
- Normalize the node-id from URL format (`1-2`) to API format (`1:2`)
- Scope the target to a frame/component, not the whole page. Split complex pages into sections, one node per section

### 2. Fetch Design Data via the Figma REST API

For API call details (endpoint selection, rate-limit handling, file caching), follow the conventions of the `figma-rest-api-coding` skill and route all calls through its `scripts/figma-api.sh`. Raw `curl` is for debugging only.

- Call `GET /v1/files/:fileKey/nodes?ids=1:2&depth=...` to fetch the target node's structure, layout, and styles
  - Data to extract: layout (Auto Layout, constraints, sizing), colors, typography, spacing, borders, shadows
  - Batch multiple nodes into a single call (`ids=1:2,3:4`)
- Call `GET /v1/images/:fileKey?ids=1:2` to export a screenshot (PNG/SVG) of the target node; keep it as the visual reference throughout implementation
- Call `GET /v1/files/:fileKey/variables/local` and the styles endpoints to resolve design tokens (variables/styles)
- Export image assets and icons via the images endpoint. If an asset cannot be retrieved, ask the user to export it from Figma. Never add new icon packages and never substitute placeholders

**If the response is too large or truncated:** first fetch a shallow `depth` to map the node structure, identify the child nodes needed, then fetch those child nodes individually.

### 3. Define Design Tokens

- Tokenize colors, typography, spacing, border radii, and shadows
- Use Figma's numeric values as-is; never round them arbitrarily
- Map Figma variables/styles to the project's design tokens

### 4. Translate to Project Conventions

Translate the Figma design data into the project's framework, styles, and conventions.

- Reuse existing components (buttons, inputs, typography, icon wrappers) instead of duplicating functionality. When a matching component exists, extend it rather than creating a new one
- Use the project's color system, typography scale, and spacing tokens consistently
- Respect existing routing, state management, and data-fetch patterns
- When design system tokens conflict with Figma values, prefer the design system tokens but make minimal spacing/size adjustments to match the visuals
- Avoid hardcoded values; extract them to constants or design tokens

### 5. Implement Incrementally

- Implement small components first, then assemble the page last
- Convert Auto Layout to Flexbox/Grid, faithfully reflecting `padding` and `gap`
- Mirror Figma's layer structure in the code structure as much as possible
- Verify frequently during implementation, not just at the end, to catch issues early

### 6. Verify and Fix with Playwright MCP or Playwright CLI

- Set the browser width to the Figma frame width; achieving an exact visual match at that width is the top priority
- Open the target page with `browser_navigate` and capture full-page/element screenshots with `browser_take_screenshot`
- Use `browser_evaluate` to read `getComputedStyle()` and compare against Figma values
- Fix any differences and re-screenshot, repeating until no diff remains

## Verification Priority Order

1. Layout and positioning
2. Sizing
3. Spacing
4. Typography
5. Colors
6. Decoration (border, radius, shadow)
7. States (hover, focus, active)

## Verification Checklist

Before declaring completion, compare against the exported Figma image and confirm:

- [ ] Layout matches (spacing, alignment, sizing)
- [ ] Typography matches (font, size, weight, line height)
- [ ] Colors match exactly
- [ ] Interactive states work as designed (hover, active, disabled)
- [ ] Responsive behavior follows Figma constraints
- [ ] Assets render correctly
- [ ] Accessibility standards (WCAG) are met

## Best Practices

- **Always start with context**: Never implement from assumptions. Always fetch the node data and exported image via the REST API before implementing
- **Reuse over recreation**: Always check for existing components before creating new ones. Codebase-wide consistency matters more than exact Figma replication
- **Design system first**: When in doubt, prefer the project's design system patterns over a literal Figma translation
- **Document deviations**: When deviating from the Figma design for accessibility or technical constraints, record the reason in a code comment

## Common Issues and Solutions

- **API response too large**: Map the structure with a shallow `depth`, then fetch child nodes individually by `ids`
- **Implementation doesn't match the design**: Compare side-by-side with the exported image and re-check spacing, color, and typography values in the node JSON
- **Design token values differ from Figma**: Prefer the project's tokens, adjusting spacing/sizing to maintain visual fidelity
- **Rate limit hit (429)**: Follow the rate-limit handling rules of `figma-rest-api-coding`: immediately stop ALL Figma API calls and wait

## Completion Criteria

- No visually detectable diff in screenshot comparison at the design width
- `getComputedStyle()` of key elements matches the Figma values
- Fonts and image assets are correctly applied
