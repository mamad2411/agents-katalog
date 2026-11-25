---
name: figma-generate-library
description: "Build or update a professional-grade design system in Figma from a codebase. Use when the user wants to create variables/tokens, build component libraries, set up theming (light/dark modes), document foundations, or reconcile gaps between code and Figma. This skill teaches WHAT to build and in WHAT ORDER â€” it complements the `figma-use` skill which teaches HOW to call the Plugin API. Both skills should be loaded together."
---

# Design System Builder â€” Figma MCP Skill

Build professional-grade design systems in Figma that match code. This skill orchestrates multi-phase workflows across 20â€“100+ `use_figma` calls, enforcing quality patterns from real-world design systems (Material 3, Polaris, Figma UI3, Simple DS).

**Prerequisites**: The `figma-use` skill MUST also be loaded for every `use_figma` call. It provides Plugin API syntax rules (return pattern, page reset, ID return, font loading, color range). This skill provides design system domain knowledge and workflow orchestration.

**Always pass `skillNames: "figma-generate-library"` when calling `use_figma` as part of this skill.** This is a logging parameter â€” it does not affect execution.

---

## 1. The One Rule That Matters Most

**This is NEVER a one-shot task.** Building a design system requires 20â€“100+ `use_figma` calls across multiple phases, with mandatory user checkpoints between them. Any attempt to create everything in one call WILL produce broken, incomplete, or unrecoverable results. Break every operation to the smallest useful unit, validate, get feedback, proceed.

---

## 2. Mandatory Workflow

Every design system build follows this phase order. Skipping or reordering phases causes structural failures that are expensive to undo.

```
Phase 0: DISCOVERY (always first â€” no use_figma writes yet)
  0a. Analyze codebase â†’ extract tokens, components, naming conventions
  0b. Inspect Figma file â†’ pages, variables, components, styles, existing conventions
  0c. Search subscribed libraries â†’ use search_design_system for reusable assets
  0d. Lock v1 scope â†’ agree on exact token set + component list before any creation
  0e. Map code â†’ Figma â†’ resolve conflicts (code and Figma disagree = ask user)
  âœ‹ USER CHECKPOINT: present full plan, await explicit approval

Phase 1: FOUNDATIONS (tokens first â€” always before components)
  1a. Create variable collections and modes
  1b. Create primitive variables (raw values, 1 mode)
  1c. Create semantic variables (aliased to primitives, mode-aware)
  1d. Set scopes on ALL variables
  1e. Set code syntax on ALL variables
  1f. Create effect styles (shadows) and text styles (typography)
  â†’ Exit criteria: every token from the agreed plan exists, all scopes set, all code syntax set
  âœ‹ USER CHECKPOINT: show variable summary, await approval

Phase 2: FILE STRUCTURE (before components)
  2a. Create page skeleton: Cover â†’ Getting Started â†’ Foundations â†’ --- â†’ Components â†’ --- â†’ Utilities
  2b. Create foundations documentation pages (color swatches, type specimens, spacing bars)
  â†’ Exit criteria: all planned pages exist, foundations docs are navigable
  âœ‹ USER CHECKPOINT: show page list + screenshot, await approval

Phase 3: COMPONENTS (one at a time â€” never batch)
  For EACH component (in dependency order: atoms before molecules):
    3a. Create dedicated page
    3b. Build base component with auto-layout + full variable bindings
    3c. Create all variant combinations (combineAsVariants + grid layout)
    3d. Add component properties (TEXT, BOOLEAN, INSTANCE_SWAP)
    3e. Link properties to child nodes
    3f. Add page documentation (title, description, usage notes)
    3g. Validate: get_metadata (structure) + get_screenshot (visual)
    3h. Optional: lightweight Code Connect mapping while context is fresh
    â†’ Exit criteria: variant count correct, all bindings verified, screenshot looks right
    âœ‹ USER CHECKPOINT per component: show screenshot, await approval before next component

Phase 4: INTEGRATION + QA (final pass)
  4a. Finalize all Code Connect mappings
  4b. Accessibility audit (contrast, min touch targets, focus visibility)
  4c. Naming audit (no duplicates, no unnamed nodes, consistent casing)
  4d. Unresolved bindings audit (no hardcoded fills/strokes remaining)
  4e. Final review screenshots of every page
  âœ‹ USER CHECKPOINT: complete sign-off
```

---

## 3. Critical Rules

**Plugin API basics** (from use_figma skill â€” enforced here too):
- Use `return` to send data back (auto-serialized). Do NOT wrap in IIFE or call closePlugin.
- Return ALL created/mutated node IDs in every return value
- Page context resets each call â€” always `await figma.setCurrentPageAsync(page)` at start
- `figma.notify()` throws â€” never use it
- Colors are 0â€“1 range, not 0â€“255
- Font MUST be loaded before any text write: `await figma.loadFontAsync({family, style})`

**Design system rules**:
1. **Variables BEFORE components** â€” components bind to variables. No token = no component.
2. **Inspect before creating** â€” run read-only `use_figma` to discover existing conventions. Match them.
3. **One page per component** *(default)* â€” exception: tightly related families (e.g., Input + helpers) may share a page with clear section separation.
4. **Bind visual properties to variables** *(default)* â€” fills, strokes, padding, radius, gap. Exceptions: intentionally fixed geometry (icon pixel-grid sizes, static dividers).
5. **Scopes on every variable** â€” NEVER leave as `ALL_SCOPES`. Background: `FRAME_FILL, SHAPE_FILL`. Text: `TEXT_FILL`. Border: `STROKE_COLOR`. Spacing: `GAP`. Radii: `CORNER_RADIUS`. Primitives: `[]` (hidden).
6. **Code syntax on every variable** â€” WEB syntax MUST use the `var()` wrapper: `var(--color-bg-primary)`, not `--color-bg-primary`. Use the actual CSS variable name from the codebase. ANDROID/iOS do NOT use a wrapper.
7. **Alias semantics to primitives** â€” `{ type: 'VARIABLE_ALIAS', id: primitiveVar.id }`. Never duplicate raw values in semantic layer.
8. **Position variants after combineAsVariants** â€” they stack at (0,0). Manually grid-layout + resize.
9. **INSTANCE_SWAP for icons** â€” never create a variant per icon. Cap variant matrices: if Size Ã— Style Ã— State > 30 combinations, split into sub-component.
10. **Deterministic naming** â€” use consistent, unique node names for idempotent cleanup and resumability. Track created node IDs via return values and the state ledger.
11. **No destructive cleanup** â€” cleanup scripts identify nodes by name convention or returned IDs, not by guessing.
12. **Validate before proceeding** â€” never build on unvalidated work. `get_metadata` after every create, `get_screenshot` after each component.
13. **NEVER parallelize `use_figma` calls** â€” Figma state mutations must be strictly sequential. Even if your tool supports parallel calls, never run two use_figma calls simultaneously.
14. **Never hallucinate Node IDs** â€” always read IDs from the state ledger returned by previous calls. Never reconstruct or guess an ID from memory.
15. **Use the helper scripts** â€” embed scripts from `scripts/` into your use_figma calls. Don't write 200-line inline scripts from scratch.
16. **Explicit phase approval** â€” at each checkpoint, name the next phase explicitly. "looks good" is not approval to proceed to Phase 3 if you asked about Phase 1.

---

## 4. State Management (Required for Long Workflows)

> **`getPluginData()` / `setPluginData()` are NOT supported in `use_figma`.** Use `getSharedPluginData()` / `setSharedPluginData()` instead (these ARE supported), or use name-based lookups and the state ledger (returned IDs).

| Entity type | Idempotency key | How to check existence |
|-------------|----------------|----------------------|
| Scene nodes (pages, frames, components) | `setSharedPluginData('dsb', 'key', value)` or unique name | `node.getSharedPluginData('dsb', 'key')` or `page.findOne(n => n.name === 'Button')` |
| Variables | Name within collection | `(await figma.variables.getLocalVariablesAsync()).find(v => v.name === name && v.variableCollectionId === collId)` |
| Styles | Name | `getLocalTextStyles().find(s => s.name === name)` |

Tag every created **scene node** immediately after creation:
```javascript
node.setSharedPluginData('dsb', 'run_id', RUN_ID);        // identifies this build run
node.setSharedPluginData('dsb', 'phase', 'phase3');        // which phase created it
node.setSharedPluginData('dsb', 'key', 'component/button');// unique logical key
```

**State persistence**: Do NOT rely solely on conversation context for the state ledger. Write it to disk:
```
/tmp/dsb-state-{RUN_ID}.json
```
Re-read this file at the start of every turn. In long workflows, conversation context will be truncated â€” the file is the source of truth.

Maintain a state ledger tracking:
```json
{
  "runId": "ds-build-2024-001",
  "phase": "phase3",
  "step": "component-button",
  "entities": {
    "collections": { "primitives": "id:...", "color": "id:..." },
    "variables": { "color/bg/primary": "id:...", "spacing/sm": "id:..." },
    "pages": { "Cover": "id:...", "Button": "id:..." },
    "components": { "Button": "id:..." }
  },
  "pendingValidations": ["Button:screenshot"],
  "completedSteps": ["phase0", "phase1", "phase2", "component-avatar"]
}
```

**Idempotency check** before every create: query by name + state ledger ID. If exists, skip or update â€” never duplicate.

**Resume protocol**: at session start or after context truncation, run a read-only `use_figma` to scan all pages, components, variables, and styles by name to reconstruct the `{key â†’ id}` map. Then re-read the state file from disk if available.

**Continuation prompt** (give this to the user when resuming in a new chat):
> "I'm continuing a design system build. Run ID: {RUN_ID}. Load the figma-generate-library skill and resume from the last completed step."

---

## 5. search_design_system â€” Reuse Decision Matrix

Search FIRST in Phase 0, then again immediately before each component creation.

```
search_design_system({ query, fileKey, includeComponents: true, includeVariables: true, includeStyles: true })
```

**Reuse if** all of these are true:
- Component property API matches your needs (same variant axes, compatible types)
- Token binding model is compatible (uses same or aliasable variables)
- Naming conventions match the target file
- Component is editable (not locked in a remote library you don't own)

**Rebuild if** any of these:
- API incompatibility (different property names, wrong variant model)
- Token model incompatible (hardcoded values, different variable schema)
- Ownership issue (can't modify the library)

**Wrap if** visual match but API incompatible:
- Import the library component as a nested instance inside a new wrapper component
- Expose a clean API on the wrapper

**Three-way priority**: local existing â†’ subscribed library import â†’ create new.

---

## 6. User Checkpoints

Mandatory. Design decisions require human judgment.

| After | Required artifacts | Ask |
|-------|-------------------|-----|
| Discovery + scope lock | Token list, component list, gap analysis | "Here's my plan. Approve before I create anything?" |
| Foundations | Variable summary (N collections, M vars, K modes), style list | "All tokens created. Review before file structure?" |
| File structure | Page list + screenshot | "Pages set up. Review before components?" |
| Each component | get_screenshot of component page | "Here's [Component] with N variants. Correct?" |
| Each conflict (code â‰  Figma) | Show both versions | "Code says X, Figma has Y. Which wins?" |
| Final QA | Per-page screenshots + audit report | "Complete. Sign off?" |

**If user rejects**: fix before moving on. Never build on rejected work.

---

## 7. Naming Conventions

Match existing file conventions. If starting fresh:

**Variables** (slash-separated):
```
color/bg/primary     color/text/secondary    color/border/default
spacing/xs  spacing/sm  spacing/md  spacing/lg  spacing/xl  spacing/2xl
radius/none  radius/sm  radius/md  radius/lg  radius/full
typography/body/font-size    typography/heading/line-height
```

**Primitives**: `blue/50` â†’ `blue/900`, `gray/50` â†’ `gray/900`

**Component names**: `Button`, `Input`, `Card`, `Avatar`, `Badge`, `Checkbox`, `Toggle`

**Variant names**: `Property=Value, Property=Value` â€” e.g., `Size=Medium, Style=Primary, State=Default`

**Page separators**: `---` (most common) or `â€”â€”â€” COMPONENTS â€”â€”â€”`

> Full naming reference: [naming-conventions.md](references/naming-conventions.md)

---

## 8. Token Architecture

| Complexity | Pattern |
|-----------|---------|
| < 50 tokens | Single collection, 2 modes (Light/Dark) |
| 50â€“200 tokens | **Standard**: Primitives (1 mode) + Color semantic (Light/Dark) + Spacing (1 mode) + Typography (1 mode) |
| 200+ tokens | **Advanced**: Multiple semantic collections, 4â€“8 modes (Light/Dark Ã— Contrast Ã— Brand). See M3 pattern in [token-creation.md](references/token-creation.md) |

Standard pattern (recommended starting point):
```
Collection: "Primitives"    modes: ["Value"]
  blue/500 = #3B82F6, gray/900 = #111827, ...

Collection: "Color"         modes: ["Light", "Dark"]
  color/bg/primary â†’ Light: alias Primitives/white, Dark: alias Primitives/gray-900
  color/text/primary â†’ Light: alias Primitives/gray-900, Dark: alias Primitives/white

Collection: "Spacing"       modes: ["Value"]
  spacing/xs = 4, spacing/sm = 8, spacing/md = 16, ...
```

---

## 9. Per-Phase Anti-Patterns

**Phase 0 anti-patterns:**
- âŒ Starting to create anything before scope is locked with user
- âŒ Ignoring existing file conventions and imposing new ones
- âŒ Skipping `search_design_system` before planning component creation

**Phase 1 anti-patterns:**
- âŒ Using `ALL_SCOPES` on any variable
- âŒ Duplicating raw values in semantic layer instead of aliasing
- âŒ Not setting code syntax (breaks Dev Mode and round-tripping)
- âŒ Creating component tokens before agreeing on token taxonomy

**Phase 2 anti-patterns:**
- âŒ Skipping the cover page or foundations docs
- âŒ Putting multiple unrelated components on one page

**Phase 3 anti-patterns:**
- âŒ Creating components before foundations exist
- âŒ Hardcoding any fill/stroke/spacing/radius value in a component
- âŒ Creating a variant per icon (use INSTANCE_SWAP instead)
- âŒ Not positioning variants after combineAsVariants (they all stack at 0,0)
- âŒ Building variant matrix > 30 without splitting (variant explosion)
- âŒ Importing remote components then immediately detaching them

**General anti-patterns:**
- âŒ Retrying a failed script without understanding the error first
- âŒ Using name-prefix matching for cleanup (deletes user-owned nodes)
- âŒ Building on unvalidated work from the previous step
- âŒ Skipping user checkpoints to "save time"
- âŒ Parallelizing use_figma calls (always sequential)
- âŒ Guessing/hallucinating node IDs from memory (always read from state ledger)
- âŒ Writing massive inline scripts instead of using the provided helper scripts
- âŒ Starting Phase 3 because the user said "build the button" without completing Phases 0-2

---

## 10. Reference Docs

Load on demand â€” each reference is authoritative for its phase:

Use your file reading tool to read these docs when needed. Do not assume their contents from the filename.

| Doc | Phase | Required / Optional | Load when |
|-----|-------|---------------------|-----------|
| [discovery-phase.md](references/discovery-phase.md) | 0 | **Required** | Starting any build â€” codebase analysis + Figma inspection |
| [token-creation.md](references/token-creation.md) | 1 | **Required** | Creating variables, collections, modes, styles |
| [documentation-creation.md](references/documentation-creation.md) | 2 | Required | Creating cover page, foundations docs, swatches |
| [component-creation.md](references/component-creation.md) | 3 | **Required** | Creating any component or variant |
| [code-connect-setup.md](references/code-connect-setup.md) | 3â€“4 | Required | Setting up Code Connect or variable code syntax |
| [naming-conventions.md](references/naming-conventions.md) | Any | Optional | Naming anything â€” variables, pages, variants, styles |
| [error-recovery.md](references/error-recovery.md) | Any | **Required on error** | Script fails, multi-step workflow recovery, cleanup of abandoned workflow state |

---

## 11. Scripts

Reusable Plugin API helper functions. Embed in `use_figma` calls:

| Script | Purpose |
|--------|---------|
| [inspectFileStructure.js](scripts/inspectFileStructure.js) | Discover all pages, components, variables, styles; returns full inventory |
| [createVariableCollection.js](scripts/createVariableCollection.js) | Create a named collection with modes; returns `{collectionId, modeIds}` |
| [createSemanticTokens.js](scripts/createSemanticTokens.js) | Create aliased semantic variables from a token map |
| [createComponentWithVariants.js](scripts/createComponentWithVariants.js) | Build a component set from a variant matrix; handles grid layout |
| [bindVariablesToComponent.js](scripts/bindVariablesToComponent.js) | Bind design tokens to all component visual properties |
| [createDocumentationPage.js](scripts/createDocumentationPage.js) | Create a page with title + description + section structure |
| [validateCreation.js](scripts/validateCreation.js) | Verify created nodes match expected counts, names, structure |
| [cleanupOrphans.js](scripts/cleanupOrphans.js) | Remove orphaned nodes by name convention or state ledger IDs |
| [rehydrateState.js](scripts/rehydrateState.js) | Scan file for all pages, components, variables by name; returns full `{key â†’ nodeId}` map for state reconstruction |
