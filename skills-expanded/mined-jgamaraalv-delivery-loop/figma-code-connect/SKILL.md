---
name: figma-code-connect
description: Create or update Figma Code Connect template files (.figma.ts/.figma.js) that map Figma components to code. Use for Code Connect, Figma component mapping, design-to-code.
---

# Code Connect

## Overview

Create Code Connect template files (`.figma.ts`) that map Figma components to code snippets. Given a Figma URL, follow the six-step workflow below to produce a validated template.

> **Note:** This project may also contain parser-based `.figma.tsx` files (using `figma.connect()`, published via CLI). This skill covers **templates files only** — `.figma.ts` files that use the MCP tools to fetch component context from Figma.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/template-patterns.md` — the Step 5 deep dive: property mapping per Figma type, exhaustive variant handling, interpolation rules, finding descendant layers, nested configurable instances, the full `instance.*`/InstanceHandle/TextHandle/SelectorOptions/Export quick reference, and the Rules & Pitfalls checklist · read when writing or reviewing the template body, or when Step 6 flags an issue.
- `references/worked-example.md` — a complete start-to-finish walkthrough of all six steps on one Button component · read when you want a concrete end-to-end example to adapt.
- `references/api.md` — the full Code Connect template API reference: `figma.config.json` configuration, the complete `figma`/`instance` API, publishing/CLI commands, type reference, best practices, and troubleshooting · read for authoritative API details, config, or publishing.
- `references/advanced-patterns.md` — advanced nesting: descendant/recursive templating, `metadata.props` passing between parent/child templates, `findConnectedInstances` filtering, and a multi-generation inheritance example · read for multi-level nested components or metadata prop passing.

## Prerequisites

- **Figma MCP server must be connected** — verify that Figma MCP tools (e.g., `get_code_connect_suggestions`) are available before proceeding. If not, guide the user to enable the Figma MCP server and restart their MCP client.
- **Components must be published** — Code Connect only works with components published to a Figma team library. If a component is not published, inform the user and stop.
- **Organization or Enterprise plan required** — Code Connect is not available on Free or Professional plans.
- **URL must include `node-id`** — the Figma URL must contain the `node-id` query parameter.
- **TypeScript types** — for editor autocomplete and type checking in `.figma.ts` files `@figma/code-connect/figma-types` must be added to `types` in `tsconfig.json`:
  ```json
  {
    "compilerOptions": {
      "types": ["@figma/code-connect/figma-types"]
    }
  }
  ```

## The 6-step workflow

```
Parse URL → Discover → Fetch props → Identify component → Create template → Validate
```

### Step 1: Parse the Figma URL

Extract `fileKey` and `nodeId` from the URL:

| URL Format                                          | fileKey          | nodeId               |
| --------------------------------------------------- | ---------------- | -------------------- |
| `figma.com/design/:fileKey/:name?node-id=X-Y`       | `:fileKey`       | `X-Y` → `X:Y`        |
| `figma.com/file/:fileKey/:name?node-id=X-Y`         | `:fileKey`       | `X-Y` → `X:Y`        |
| `figma.com/design/:fileKey/branch/:branchKey/:name` | use `:branchKey` | from `node-id` param |

Always convert `nodeId` hyphens to colons: `1234-5678` → `1234:5678`.

**Worked example:** Given `https://www.figma.com/design/QiEF6w564ggoW8ftcLvdcu/MyDesignSystem?node-id=4185-3778` → `fileKey` = `QiEF6w564ggoW8ftcLvdcu`, `nodeId` = `4185-3778` → `4185:3778`.

### Step 2: Discover Unmapped Components

The user may provide a URL pointing to a frame, instance, or variant — not necessarily a component set or standalone component. Call the MCP tool `get_code_connect_suggestions` with:

- `fileKey` — from Step 1
- `nodeId` — from Step 1 (colons format)
- `excludeMappingPrompt` — `true` (returns a lightweight list of unmapped components)

This tool identifies published components in the selection that don't yet have Code Connect mappings.

**Handle the response:**

- **"No published components found in this selection"** — the node contains no published components. Inform the user they need to publish the component to a team library in Figma first, then stop.
- **"All component instances in this selection are already connected to code via Code Connect"** — everything is already mapped. Inform the user and stop.
- **Normal response with component list** — extract the `mainComponentNodeId` for each returned component. Use these resolved node IDs (not the original from the URL) for all subsequent steps. If multiple components are returned (e.g. the user selected a frame containing several different component instances), repeat Steps 3–6 for each one.

### Step 3: Fetch Component Properties

Call the MCP tool `get_context_for_code_connect` with:

- `fileKey` — from Step 1
- `nodeId` — the resolved `mainComponentNodeId` from Step 2
- `clientFrameworks` — determine from `figma.config.json` `parser` field (e.g. `"react"` → `["react"]`)
- `clientLanguages` — infer from project file extensions (e.g. TypeScript project → `["typescript"]`, JavaScript → `["javascript"]`)

For multiple components, call the tool once per node ID.

The response contains the Figma component's **property definitions** — note each property's name and type:

- **TEXT** — text content (labels, titles, placeholders)
- **BOOLEAN** — toggles (show/hide icon, disabled state)
- **VARIANT** — enum options (size, variant, state)
- **INSTANCE_SWAP** — swappable nested instances tied to a specific component (icon, avatar)
- **SLOT** — flexible content regions (freeform layout, mixed children); use `getSlot()` in templates (not the same as INSTANCE_SWAP)

Save this property list — you will use it in Step 5 to write the template.

### Step 4: Identify the Code Component

If the user did not specify which code component to connect:

1. Check `figma.config.json` for `paths` and `importPaths` to find where components live
2. Search the codebase for a component matching the Figma component name. Check common directories (`src/components/`, `components/`, `lib/ui/`, `app/components/`) if `figma.config.json` doesn't specify paths
3. Read candidate files and compare their props interface against the Figma properties from Step 3 — look for matching variant types, size options, boolean flags, and slot props
4. If multiple candidates match, pick the one with the closest prop-interface match and explain your reasoning to the user
5. If no match is found, show the 2 closest candidates and ask the user to confirm or provide the correct path

**Confirm with the user** before proceeding to Step 5. Present the match: which code component you found, where it lives, and why it matches (prop correspondence, naming, purpose).

Read `figma.config.json` for import path aliases — the `importPaths` section maps glob patterns to import specifiers, and the `paths` section maps those specifiers to directories.

Read the code component's source to understand its props interface — this informs how to map Figma properties to code props in Step 5.

### Step 5: Create the Template File (.figma.ts)

**File location** — place the file alongside existing Code Connect templates (`.figma.tsx` or `.figma.ts` files). Check `figma.config.json` `include` patterns for the correct directory. Name it `ComponentName.figma.ts`.

**Template structure** — every template file follows this shape:

```ts
// url=https://www.figma.com/file/{fileKey}/{fileName}?node-id={nodeId}
// source={path to code component from Step 4}
// component={code component name from Step 4}
import figma from "figma";
const instance = figma.selectedInstance;

// Extract properties from the Figma component (see property mapping below)
// ...

export default {
  example: figma.code`<Component ... />`, // Required: code snippet
  imports: ['import { Component } from "..."'], // Optional: import statements
  id: "component-name", // Required: unique identifier
  metadata: {
    // Optional
    nestable: true, // true = inline in parent, false = show as pill
    props: {}, // data accessible to parent templates
  },
};
```

**Write the template body** using the property list from Step 3. The full how-to — per-type property mapping, exhaustive variant handling (every enum value must be mapped), interpolation wrapping rules, finding descendant layers, nested configurable instances, conditional props, the `instance.*`/InstanceHandle/SelectorOptions/Export quick reference, and the **Rules & Pitfalls** checklist — lives in **[references/template-patterns.md](references/template-patterns.md)**. For multi-level nesting or metadata prop passing between templates, see **[references/advanced-patterns.md](references/advanced-patterns.md)**.

### Step 6: Validate

Read back the `.figma.ts` file and review it against the following:

- **Property coverage** — every Figma property from Step 3 should be accounted for in the template. Flag any that are missing and ask the user if they were intentionally omitted.
- **Valid, correctly typed code** — all emitted code must be valid and correctly typed against the code component's `Props` interface. Never make up component properties — if a Figma property has no corresponding code prop, omit it rather than invent one.
- **No hardcoded children** — verify that every INSTANCE_SWAP property and child component slot uses the dynamic APIs (`getInstanceSwap()`, `findInstance()`, `findConnectedInstance()`, etc.) with `executeTemplate()`. No slot should contain hardcoded component content.
- **Rules and Pitfalls** — check for the common mistakes listed in [references/template-patterns.md](references/template-patterns.md) (string concatenation of template results, unnecessary `hasCodeConnect()` guards, missing `type === 'INSTANCE'` checks, etc.)
- **Interpolation wrapping** — strings (`getString`, `getEnum`, `textContent`) wrapped in quotes, instance/section values (`executeTemplate().example`) wrapped in braces, slot sections (`getSlot`) interpolated as snippet sections inside `` figma.code`...` ``, booleans using conditionals

If anything looks uncertain, consult [references/api.md](references/api.md) for API details and [references/advanced-patterns.md](references/advanced-patterns.md) for complex nesting.

For a full worked walkthrough of all six steps on one component, see **[references/worked-example.md](references/worked-example.md)**.
