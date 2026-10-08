---
title: Agent Skill Installation
description: Install the Figma-to-code skill for production-ready UI implementation
---

The TemPad Dev agent skill (`figma-design-to-code`) provides coding agents with specialized workflows for translating Figma selections into production-ready UI code using TemPad Dev MCP as the authoritative source of design evidence.

## What It Does

The skill teaches agents to:

1. **Detect repo conventions** (framework, styling, tokens, assets, components)
2. **Fetch baseline snapshots** using `get_code` with proper parameters
3. **Resolve warnings** (depth-cap, auto-layout, budget limits) before implementing
4. **Handle assets** according to your project's asset pipeline policy
5. **Map tokens** from Figma variables to your theme system
6. **Translate** Tailwind-like IR into your repo's native styling approach
7. **Apply semantics** (accessible HTML, keyboard interaction, ARIA labels)
8. **Exit gracefully** with evidence caveats and next steps when incomplete

<Note>
The skill treats MCP outputs as **design facts**. Agents will not guess colors, typography, spacing, or other critical styles.
</Note>

## Requirements

- **Node.js 18+** (the same requirement as the MCP server)
- **MCP-compatible agent** with skill support (e.g., agents built on skills framework)
- **TemPad Dev MCP** already installed and configured

## Installation

<Steps>
  <Step title="Copy the Installation Command">
    In TemPad Dev, open **Preferences → MCP server** and click the copy icon next to **Agent skill**. This copies the installation command to your clipboard.
  </Step>

  <Step title="Run the Command">
    Open your terminal and run the copied command:

    ```bash
    npx skills add https://github.com/ecomfe/tempad-dev/tree/main/skill
    ```

    The skills CLI will:
    - Download the skill from the GitHub repository
    - Install it to your agent's skill directory
    - Register it as `figma-design-to-code`
  </Step>

  <Step title="Verify Installation">
    Check that the skill is available:

    ```bash
    npx skills list
    ```

    You should see `figma-design-to-code` in the output.
  </Step>
</Steps>

## How to Use

Once installed, the skill is automatically available to your coding agent. You can invoke it by asking the agent to implement UI from Figma:

<CodeGroup>
```text Simple Request
Implement the button component from my Figma selection
```

```text With Node ID
Implement the card layout from nodeId "123:456"
```

```text Complex Component
Create a production-ready implementation of the modal dialog I have selected in Figma, matching our repo's React + Tailwind conventions
```
</CodeGroup>

## Workflow Overview

The skill follows this evidence-based workflow:

### 1. Repo Convention Detection

The agent first analyzes your repository to understand:
- Framework and runtime (React, Vue, SFC conventions)
- Styling approach (Tailwind, CSS Modules, styled-components, etc.)
- Token/theme system (CSS variables, token files, dark mode)
- Asset policy (public folder vs imports, icon pipeline)
- Existing components and primitives

### 2. Baseline Snapshot

The agent calls `get_code` with:
- `resolveTokens: false` (to enable token mapping)
- `preferredLang` matching your repo (jsx or vue)
- Optional `nodeId` if you specified one

### 3. Warning Resolution

<AccordionGroup>
  <Accordion title="depth-cap Warnings">
    If the response includes a `depth-cap` warning, the agent will:
    - Extract the list of capped node IDs from `warnings[].data.cappedNodes`
    - Call `get_code` again for each node ID
    - Stitch the results together before implementing
    - Stop if `cappedNodeOverflow=true` (too many nodes to handle)
  </Accordion>

  <Accordion title="Budget Exceeded Errors">
    If the payload is too large (~4MB limit):
    - The agent will report current consumption, limit, and overage
    - Ask you to select a smaller subtree or prioritize specific sections
    - Retry with a narrower `nodeId` scope
  </Accordion>

  <Accordion title="Auto-Layout Uncertainty">
    If warnings indicate inferred or uncertain layout:
    - The agent calls `get_structure` to clarify hierarchy and overlap
    - Uses geometry data to resolve contradictions
    - Stops if contradictions cannot be resolved
  </Accordion>
</AccordionGroup>

### 4. Asset Handling

The agent follows your repo's asset policy:
- Downloads bytes via `asset.url` from the response
- Saves to the correct path (e.g., `public/images/` or `src/assets/`)
- References assets using your repo's import conventions
- Warns if assets cannot be stored under project policy

<Warning>
The skill will **only** download assets from TemPad-provided URLs, never from the public internet.
</Warning>

### 5. Token Mapping

Token evidence from `get_code` includes:
- Canonical CSS variable names (e.g., `--color-primary`)
- Single-mode values or multi-mode maps (`Collection:Mode` keys)
- References to other variables (preserved)

The agent will:
1. Look for equivalent tokens in your existing theme system
2. Map based on value equivalence + semantic alignment
3. Add new tokens only if your repo has an established token workflow
4. Keep explicit values when mapping is ambiguous

### 6. Repo-Native Translation

The agent translates TemPad Dev's Tailwind-like IR into your conventions:

<Tabs>
  <Tab title="Utility-First Repos">
    For Tailwind/UnoCSS projects:
    - Preserves utility classes
    - Adjusts formatting to match your repo's class ordering
    - Respects your Tailwind version and config
  </Tab>

  <Tab title="Non-Utility Repos">
    For CSS Modules, scoped CSS, or CSS-in-JS:
    - Translates utilities into your styling approach
    - Preserves exact values (no rounding or simplification)
    - Maintains high-fidelity details (pseudo-elements, filters, blend modes)
  </Tab>
</Tabs>

<Note>
The skill will **not** introduce new frameworks or styling systems. It works within your existing architecture.
</Note>

### 7. Semantics and Accessibility

For container elements that need interactivity, the agent applies:
- Native HTML elements (`button`, `a`, `input`/`label`)
- Keyboard interaction and focus management
- Accessible names (`aria-label`, `alt` text)

It assumes your repo has a CSS reset/normalize and will not add new global styles.

### 8. Exit and Wrap-Up

The agent stops implementation when:
- MCP is unavailable or unauthorized
- Evidence is contradictory and cannot be resolved
- Required assets cannot be retrieved or stored

Otherwise, it ships the best-evidence implementation with:
- **Evidence caveats**: Warnings, omissions, inferred conventions
- **Asset notes**: Stored vs TemPad URLs, policy constraints
- **Token notes**: Mapped vs explicit values, ambiguities
- **Dependencies**: Whether any were added (and if user confirmation was obtained)

## Configuration

The skill has no configuration file. It adapts to your repository by:
- Reading existing code patterns
- Analyzing framework and tooling config files
- Inferring conventions from file structure

<Tip>
For best results, maintain consistent patterns in your repo. The skill relies on convention detection to produce accurate code.
</Tip>

## Evidence Rules

The skill follows strict evidence rules:

<ResponseField name="Priority Order" required>
  1. `get_code` output (authoritative)
  2. `get_structure` (for hierarchy/geometry clarification)
</ResponseField>

<ResponseField name="Never Guess" required>
  The agent will **never invent**:
  - Colors, typography (size/weight/line-height/letter-spacing)
  - Spacing, radius, borders, shadows, gradients
  - Opacity, overlays, blur effects
</ResponseField>

<ResponseField name="High-Fidelity Preservation" required>
  The agent preserves:
  - Pseudo-elements and pseudo-classes
  - Uncommon style properties
  - Filters, masks, blend modes, backdrop effects
  - Non-default compositing details
</ResponseField>

<Warning>
`data-hint-*` attributes from `get_code` are for agent reasoning **only**. The skill strips them from final output.
</Warning>

## Retry Policy

The skill retries **only once** for transient failures:
- Network timeouts or disconnects
- Extension reconnection or activation issues

It does **not** blind-retry deterministic errors:
- `depth-cap` warnings (requires scope changes)
- Budget exceeded (requires smaller `nodeId`)
- Invalid selection or node not visible

## Skill Metadata

<ResponseField name="Name" type="string">
  `figma-design-to-code`
</ResponseField>

<ResponseField name="Description" type="string">
  Implement integration-ready UI code from a Figma selection or nodeId using TemPad Dev MCP as the only source of design evidence.
</ResponseField>

<ResponseField name="Repository" type="string">
  `https://github.com/ecomfe/tempad-dev/tree/main/skill`
</ResponseField>

## Troubleshooting

<AccordionGroup>
  <Accordion title="Skill not found">
    - Verify you ran the installation command successfully
    - Check `npx skills list` output
    - Ensure your agent supports the skills framework
  </Accordion>

  <Accordion title="Agent ignores design facts">
    - Confirm MCP is enabled and active in TemPad Dev
    - Verify the agent is actually invoking MCP tools (check logs)
    - Ensure you're selecting a visible node in Figma
  </Accordion>

  <Accordion title="Code doesn't match repo conventions">
    - Review your repo for consistent patterns
    - Check framework and styling config files
    - Provide explicit guidance in your prompt
  </Accordion>

  <Accordion title="Assets not downloading">
    - Verify `asset.url` is accessible from your environment
    - Check your project's asset directory permissions
    - Ensure the HTTP asset server is running (part of MCP)
  </Accordion>
</AccordionGroup>

## Best Practices

<CardGroup cols={2}>
  <Card title="Select Precise Scopes" icon="bullseye">
    Select individual components or small sections rather than entire pages to avoid depth-cap and budget limits.
  </Card>

  <Card title="Maintain Repo Consistency" icon="arrows-rotate">
    Keep consistent naming, import paths, and styling patterns. The skill relies on convention detection.
  </Card>

  <Card title="Provide Context in Prompts" icon="comment">
    Tell the agent about special requirements (e.g., "this is a modal, needs focus trap").
  </Card>

  <Card title="Review Token Mapping" icon="palette">
    Check that mapped tokens match your theme's semantic intent, not just values.
  </Card>
</CardGroup>

<Tip>
For complex components, implement in stages: fetch evidence first, review warnings, then ask the agent to implement specific sections.
</Tip>
