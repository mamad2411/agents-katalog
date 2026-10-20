---
name: code-connect-impl
description: Implements and publishes Figma Code Connect mappings (*.figma.tsx) for the built React component library. Invoked when the user says "wire Code Connect to components", "implement figma.tsx mappings", "link React components to Figma", "set up Code Connect", "publish Code Connect", "update code connect after component change", "validate figma.tsx files", or "Figma Dev Mode shows wrong snippets". Owned by frontend-engineer — Code Connect is React code mapping built components to their Figma source.
---

# Code Connect Implementation Skill

The single Code Connect skill, owned by `frontend-engineer`: wire every built React component to its Figma counterpart by implementing `*.figma.tsx` mapping files, then validate and publish. After publishing, Figma's Dev Mode shows live, accurate, copy-pasteable component code — not generated stubs. **Plan-gated — Code Connect requires a Figma Organization or Enterprise plan (see step 0); on Pro or lower it is skipped, and the component library ships without it.**

Code Connect belongs to the engineer, not the designer: the mapping file is React/TS code that imports the built component and binds the component's real prop API to the Figma component's properties. `ux-designer` authors the Figma source (components, variables, tokens); this skill maps that source to the code the `frontend-engineer` built from it.

> **Publishing does not require the Figma MCP.** `npx figma connect validate`/`publish` use the `FIGMA_ACCESS_TOKEN` env var (a CLI/REST path), so this works even when the remote Figma MCP — an OAuth server a dispatched subagent may not reach — is unavailable. The MCP read tools in step 2 are a convenience for discovery; if they are unreachable, enumerate components from the `ux-designer`'s handoff instead (the `design-system.md` component inventory + node IDs in the Figma file URL) and proceed via the CLI. The token-based publish is the reliable path.

## Process

### 0. Plan gate — Code Connect requires Figma Organization or Enterprise

**Code Connect is not available on Starter or Professional plans — only Organization and Enterprise** (it also needs Dev Mode). If the project's Figma plan is **Pro or lower, skip this skill entirely**: do not author `*.figma.tsx` files and do not attempt to publish — the plan can't accept the mappings, so it is wasted work. The built React component library is unaffected; only the optional Dev Mode mapping needs the plan.

Decide the gate before doing anything else:
- **Known Org/Enterprise** (stated by the project, or declared in `.ai/stack-profile.md`) → proceed to step 1 (full Code Connect).
- **Known Pro or lower** → skip the publish; produce the **Pro fallback** (step 0a) instead. Record "Code Connect publish deferred — requires Figma Org/Enterprise; project is on <plan>; manual mapping doc emitted" in the handoff/PR.
- **Unknown** → default to the Pro fallback. Optionally confirm the real plan with a single `npx figma connect publish` attempt; a plan/permission error (e.g. not-entitled / unsupported-plan) confirms the gate. Do not loop retrying.

Never silently mark Code Connect "done" when the publish was skipped — say it was deferred, why, and that the fallback doc stands in.

### 0a. Pro fallback — manual mapping doc + token parity (no Org/Enterprise)

When gated out, don't ship nothing. The Figma MCP **read** tools (`get_metadata`, `get_design_context`, `get_variable_defs`) and the extracted `tokens.json` still work on any plan — enough to give design↔code traceability without the Dev Mode publish. Produce two artifacts:

1. **Manual mapping doc** — `docs/design/code-connect-map.md`: a table mapping each Figma component (name + node ID) → its React component path → prop correspondence (Figma property → React prop), written by hand the same way a `*.figma.tsx` would map them. This is the human-readable stand-in for Dev Mode snippets and the seed for real Code Connect later.

   | Figma component (node ID) | React component | Prop mapping |
   |---|---|---|
   | `Button` (`12:34`) | `src/components/Button.tsx` | Variant→`variant`, Size→`size`, Disabled→`disabled`, Label→children |

2. **Token-parity check** — confirm every component sources its visual values from `tokens.json` (no hardcoded colors/spacing/radii that would silently drift from the Figma variables). Flag any divergence. This is the `react-component-library` token-as-source-of-truth discipline, audited as a traceability gate.

This is **not** a full substitute — there are no live Dev Mode code snippets — but it is real, reviewable traceability now, and the upgrade path is clean: when the project moves to Org/Enterprise, the mapping doc + the `ux-designer`'s component inventory convert directly into `*.figma.tsx` files (steps 1–7).

### 1. Confirm prerequisites

Ensure the React component library is built (see `react-component-library`) and the Code Connect CLI is available:

```bash
npx figma connect --help
# If missing, install as a dev dependency:
npm install --save-dev @figma/code-connect
```

Confirm `figma.config.json` (or `codeConnect` in `package.json`) is present:

```json
{
  "codeConnect": {
    "documentUrl": "https://www.figma.com/file/<FILE_ID>/...",
    "include": ["src/**/*.figma.tsx"]
  }
}
```

Create it if absent. The `documentUrl` is the URL of the Figma design file the UX designer built.

### 2. Discover components via Figma MCP

Use the official Figma MCP read tools (from the **`figma`** companion plugin) to enumerate components that need mapping:

```
get_code_connect_map    → list existing Code Connect mappings; identify gaps
search_design_system    → enumerate all published components and component sets
get_design_context      → inspect a specific component's properties, variants, and layers
get_variable_defs       → confirm which token variables a component references
```

Cross-reference the Figma component list against `src/components/` to produce a gap list: components that exist in Figma but have no `*.figma.tsx` yet.

After implementing mappings and publishing, use `add_code_connect_map` to register the mapping in Figma if the CLI publish step does not cover it automatically.

### 3. Implement `*.figma.tsx` mapping files

For each Figma component, create a co-located `<ComponentName>.figma.tsx` next to the React implementation. Map every Figma property to the corresponding React prop:

```tsx
import figma from "@figma/code-connect";
import { Button } from "./Button";

figma.connect(Button, "https://www.figma.com/file/<FILE_ID>?node-id=<NODE_ID>", {
  props: {
    label:    figma.string("Label"),
    variant:  figma.enum("Variant", {
      Primary:     "primary",
      Secondary:   "secondary",
      Destructive: "destructive",
    }),
    disabled: figma.boolean("Disabled"),
    size:     figma.enum("Size", {
      Small:  "sm",
      Medium: "md",
      Large:  "lg",
    }),
  },
  example: ({ label, variant, disabled, size }) => (
    <Button variant={variant} size={size} disabled={disabled}>
      {label}
    </Button>
  ),
});
```

Property type mapping reference:

| Figma property type | Code Connect helper |
|---|---|
| Text / string layer | `figma.string("Layer Name")` |
| Boolean property | `figma.boolean("Prop Name")` |
| Variant / enum property | `figma.enum("Prop Name", { FigmaValue: "codeValue" })` |
| Instance swap slot | `figma.instance("Slot Name")` |
| Nested component | `figma.nestedProps("Component", { ... })` |
| Children slot | `figma.children("Slot Name")` |

Validate that every mapped prop name matches the React component's TypeScript interface exactly. If a Figma property has no React equivalent (e.g., a design-only annotation layer), exclude it from the mapping rather than mapping it to a no-op.

### 4. Validate locally

```bash
npx figma connect validate
```

Fix all reported mismatches:
- Node IDs that no longer exist in the Figma file (component was renamed or moved).
- Property names that changed in Figma or in the React component.
- Missing `$FIGMA_ACCESS_TOKEN` environment variable (required for validation that hits the Figma API).

Re-run until validation reports zero errors.

### 5. Publish

```bash
FIGMA_ACCESS_TOKEN=<token> npx figma connect publish
```

Confirm `FIGMA_ACCESS_TOKEN` is available in `.env`, shell environment, or CI secrets before running. On success, open the Figma file in Dev Mode and spot-check at least three components to confirm the correct React code snippet appears.

If the CLI publish does not register the mapping in the Figma file's Code Connect map, use the Figma MCP `add_code_connect_map` tool to register manually.

### 6. Keep mappings in sync

Re-run validation and publish after any of:
- A Figma component is renamed, restructured, or its properties change.
- A React component's prop API changes (name, type, or removed prop).
- New components are added to the design system.
- A `tokens.json` update changes a variant name that appears in an `enum` mapping.

Add a CI step to catch drift before it reaches production:

```yaml
# .github/workflows/figma-validate.yml
- name: Validate Code Connect
  run: npx figma connect validate
  env:
    FIGMA_ACCESS_TOKEN: ${{ secrets.FIGMA_ACCESS_TOKEN }}
```

### 7. Self-review checklist

**If gated to the Pro fallback (step 0a):**
- [ ] `docs/design/code-connect-map.md` covers every built component (Figma node ID → React path → prop mapping).
- [ ] Token-parity check passed — no component hardcodes values that diverge from `tokens.json`.
- [ ] The deferral is recorded (handoff/PR): publish skipped, plan reason, fallback doc emitted.

**If full Code Connect (Org/Enterprise):**
- [ ] Every component in `src/components/` has a co-located `*.figma.tsx`.
- [ ] Every Figma component with `get_code_connect_map` returning no mapping now has one.
- [ ] `npx figma connect validate` exits zero.
- [ ] Spot-check in Figma Dev Mode: three or more components show correct, copy-pasteable code.
- [ ] No stale node IDs referencing deleted Figma components.
- [ ] CI validation step is wired.
