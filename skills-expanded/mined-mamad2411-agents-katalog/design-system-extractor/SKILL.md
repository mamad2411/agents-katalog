---
name: design-system-extractor
description: Extract and document a frontend repo's foundation design system (fonts, colors, transitions, layout, spacing, component styles) into a readable DESIGN-SYSTEM.md reference. Use when the user says "extract the design system", "document our design tokens", "what fonts/colors does this app use", "build a design system reference", or "audit our styling".
---

# Design System Extractor

Scan a frontend repository, discover where design tokens are defined, extract the
actual values in use, and synthesize them into a single human-readable
`DESIGN-SYSTEM.md` reference covering typography, color, spacing/layout,
transitions, elevation, and component styles.

This skill works on any frontend stack. It auto-detects token sources rather than
assuming a framework: Tailwind config, CSS custom properties, SCSS/LESS variables,
CSS-in-JS themes (styled-components, emotion, vanilla-extract, stitches), design-token
JSON, and global stylesheets / font declarations.

## Thinking Process

When activated, follow this structured thinking approach.

### Step 1: Locate the Repo Root and Frontend Surface

**Goal:** Establish the boundary of what you are documenting before scanning.

**Key Questions to Ask:**
- Is the design system in this repo, or a `packages/*` workspace inside a monorepo?
- Is there a dedicated `ui`, `design-system`, or `tokens` package?
- Which directories are source vs. generated (`dist`, `build`, `.next`)?

**Actions:**
1. Confirm the repo root with the user (default: current working directory).
2. If a monorepo, ask whether to scan the whole tree or a specific package.

**Decision Point:** You can state: "I will scan `<root>`, excluding build/vendor output."

### Step 2: Discover Token Sources (Where)

**Goal:** Find every place design decisions are encoded, without assuming a stack.

**Actions:**
1. Run `scan-tokens.sh` against the root.
2. Read the JSON: which source categories are populated
   (`tailwind_config`, `css_variables`, `preprocessor_variables`, `css_in_js`,
   `token_json`, `global_stylesheets`, `font_definitions`)?

**Thinking Framework:**
- "A populated category tells me the *authoritative* source for that token type."
- "Tailwind config present → colors/spacing/fonts likely live in `theme.extend`."
- "Many `css_variables` files → the system is CSS-custom-property driven."
- "`token_json` present → there may be a single source of truth to read first."

**Decision Point:** You can name the primary token source(s) for this repo.

### Step 3: Extract Raw Values (What)

**Goal:** Quantify which concrete values are actually used, and how often.

**Actions:**
1. Run `extract-values.sh` against the root.
2. Read the frequency-ranked maps for `colors`, `font_families`, `font_sizes`,
   `spacing`, `radius`, `transitions`, `shadows`, `z_index`.

**Thinking Framework:**
- "High-frequency values are the real tokens; one-off values are likely drift."
- "Compare extracted values against the declared source from Step 2 — gaps mean
   hardcoded values that bypass the token system."
- "A cluster of near-identical colors (#3b82f6, #3a82f5) signals an inconsistency
   worth flagging, not documenting as separate tokens."

**Decision Point:** You can distinguish *canonical tokens* from *drift/noise*.

### Step 4: Read the Authoritative Sources Directly

**Goal:** Turn raw frequencies into named, semantic tokens.

**Actions:**
1. Open the top files from Step 2 (e.g. `tailwind.config.js`, `tokens.json`,
   `theme.ts`, `:root` blocks) and read the *named* token definitions.
2. Map names → values (e.g. `--color-primary: #3b82f6`, `colors.brand.500`).

**Thinking Framework:**
- "Prefer the author's names over inventing my own."
- "If a value has no name, propose a clear semantic name and mark it as inferred."

**Decision Point:** You have a name→value table per category.

### Step 5: Capture Component Styles

**Goal:** Document recurring component patterns, not just primitives.

**Actions:**
1. Identify component-level style rules (`.btn`, `.card`, styled `Button`, etc.).
2. For each, record the tokens it composes (padding, radius, color, transition).

**Thinking Framework:**
- "A component entry should read as a recipe of foundation tokens."
- "Document the *default* variant; note variants briefly rather than exhaustively."

**Decision Point:** You can list the core components and the tokens they consume.

### Step 6: Synthesize DESIGN-SYSTEM.md

**Goal:** Produce one readable reference, organized by foundation category.

**Sections to emit (in order):**
1. **Overview** — stack detected, primary token source(s).
2. **Typography** — font families, sizes, weights, line-heights.
3. **Color** — named palette with hex swatches in a table.
4. **Spacing & Layout** — spacing scale, container/breakpoint values.
5. **Radius & Elevation** — border-radius scale, shadow tokens.
6. **Motion** — transition durations/easings.
7. **Components** — recipes referencing the tokens above.
8. **Drift & Inconsistencies** — hardcoded/near-duplicate values worth reconciling.

**Thinking Framework:**
- "Every value should trace back to a source file path."
- "Tables over prose for token lists; prose only for guidance."

**Decision Point:** The doc lets a new developer style a feature without grep.

### Step 7: Review with the User

**Goal:** Confirm fidelity before treating the doc as canonical.

**Actions:**
1. Present a summary: # of token sources, # of tokens per category, drift count.
2. Ask whether to write `DESIGN-SYSTEM.md` to the repo root or a chosen path.

**Decision Point:** User confirms the output location and accuracy.

## Usage

```bash
# Step 1: discover WHERE tokens are defined
bash /mnt/skills/user/design-system-extractor/scripts/scan-tokens.sh [repo_root]

# Step 2: extract WHAT values are used, ranked by frequency
bash /mnt/skills/user/design-system-extractor/scripts/extract-values.sh [repo_root]
```

**Arguments:**
- `repo_root` - Path to the frontend repo to scan (defaults to `.`)

**Examples:**
```bash
# Scan the current repo
bash /mnt/skills/user/design-system-extractor/scripts/scan-tokens.sh

# Scan a specific package in a monorepo
bash /mnt/skills/user/design-system-extractor/scripts/scan-tokens.sh ./packages/ui
bash /mnt/skills/user/design-system-extractor/scripts/extract-values.sh ./packages/ui
```

## Output

`scan-tokens.sh` emits JSON listing source files per category:

```json
{
  "root": ".",
  "tailwind_config": ["tailwind.config.js"],
  "css_variables": ["src/styles/globals.css"],
  "preprocessor_variables": [],
  "css_in_js": ["src/theme.ts"],
  "token_json": [],
  "global_stylesheets": ["src/styles/globals.css"],
  "font_definitions": ["src/styles/globals.css"]
}
```

`extract-values.sh` emits frequency-ranked value maps:

```json
{
  "root": ".",
  "colors": { "#3b82f6": 5, "#ffffff": 3 },
  "font_families": { "Inter, sans-serif": 4 },
  "spacing": { "1rem": 7, "0.5rem": 4 },
  "transitions": { "all 0.2s ease": 3 }
}
```

## Present Results to User

After running both scripts and reading the authoritative sources, present:

```
Design System Audit — <repo>

Sources detected:
- Tailwind config: tailwind.config.js
- CSS variables:   src/styles/globals.css (12 vars)
- CSS-in-JS theme: src/theme.ts

Tokens extracted:
- Typography: 2 families, 6 sizes
- Color:      9 named tokens (+3 near-duplicates flagged)
- Spacing:    8-step scale
- Motion:     3 transitions

Next: write DESIGN-SYSTEM.md to <path>? (y/n)
```

Then generate `DESIGN-SYSTEM.md` following the Step 6 section order.

## Troubleshooting

- **Empty results everywhere** — likely scanning a build output or wrong root.
  Re-run pointing at the source package (e.g. `./packages/ui`).
- **Permission denied running the script** — run via `bash <script>` rather than
  executing directly, or `chmod +x` the script first.
- **`find` is slow on large monorepos** — the script already prunes
  `node_modules`/`.git`/build dirs; narrow the scope by passing a subdirectory.
- **Values look duplicated (#3b82f6 vs #3a82f5)** — this is drift, not an error;
  document the canonical one and list the rest under Drift & Inconsistencies.
```
