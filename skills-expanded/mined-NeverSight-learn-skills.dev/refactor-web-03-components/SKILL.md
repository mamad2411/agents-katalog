---
name: refactor-web-03-components
description: Frontend UI component-standard checking and code generation tool (version-adaptive). Use this skill when the user asks for a "UI component standard" review, "color check", "font/typography standard", "button standard", "table standard", "input standard", "component samples", or to "generate a component" (table, form, query panel) on a Vue 3 + TypeScript frontend. It selects the matching versioned ruleset from the project `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`). This is step 3 of 5 of the frontend governance lane in the refactor-chain bundle.
---

# Frontend UI Component Standard Check & Code Generation — refactor-chain · Web lane · step 03/05

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** Frontend project governance (versioned) · **Position:** step 03 of 05 · **Prerequisite:** refactor-web-02-modules · **Next:** refactor-web-04-layout.
**Adaptivity:** Selects the versioned ruleset from the project `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`).

## Purpose
This skill checks UI component standards and generates compliant component code for a Vue 3 + TypeScript frontend. Based on the *Integrated System Interface Standard*, it enforces constraints on color, typography, buttons, input controls, and tables, and also ships component-level code templates and standard samples for rapidly producing compliant components. The skill detects the version declared in `package.json` and loads the corresponding ruleset before executing. It offers three functions: component standard checking (scanning code for conformance), standard-sample display (canonical example code per component type), and template generation (producing compliant component code from reusable templates).

## When to use
- The user wants to verify that components meet the UI standard. Trigger phrases: "UI component standard", "color check", "font/typography standard", "button standard", "table standard", "input standard".
- The user wants to view standard component samples. Trigger phrases: "component samples", "button sample", "table sample", "input-box sample".
- The user wants to generate compliant component code from templates. Trigger phrases: "generate component", "generate table", "generate form", "generate query panel".
- The user wants a full-suite standard audit. Trigger phrases: "UI full check", "frontend standard review".

## Rules enforced
Five rule categories are applied. Generated components must use CSS variables rather than hard-coded color values, must expose `aria` attributes or accessible labels on buttons and form controls, and must follow the Alibaba frontend development standard.

**`S01` Color (5 rules):** `S01-01` brand-color correctness (ERROR), `S01-02` neutral-color consistency (WARNING), `S01-03` functional-color correctness (ERROR), `S01-04` color-count control (WARNING), `S01-05` CSS-variable usage (SUGGESTION). Core palette: brand `#1890FF`; label text `#595959`, body text `#434343`, placeholder `#BFBFBF`; error / required asterisk `#FF4D4F`, success `#52C41A`, warning `#FAAD14`; disabled background `#FAFAFA`, disabled text `#BFBFBF`; hover background `#F5F5F5`, selected background `#E6F7FF`; editable-area background `#FEFFE6`; divider `#F0F0F0`; non-current breadcrumb `#8C8C8C`; link / selected text `#1890FF`.

**`S02` Typography (5 rules):** `S02-01` font-size correctness (ERROR), `S02-02` font-weight convention (WARNING), `S02-03` label-width limit (WARNING), `S02-04` text-alignment rules (WARNING), `S02-05` numeric formatting (WARNING). Core sizes: `16px` card title, `14px` control label / button / body, `12px` hints / auxiliary content.

**`S03` Buttons (8 rules):** `S03-01` primary-button count ≤ 1 (ERROR), `S03-02` danger-button count ≤ 1 (WARNING), `S03-03` total-button control (WARNING), `S03-04` more-panel width ≤ 200px (WARNING), `S03-05` button text size 14px (ERROR), `S03-06` loading state (WARNING), `S03-07` secondary-page button direction (WARNING), `S03-08` back-button position (WARNING). At most one primary button (blue background) per page; ordinary buttons use a grey border; use danger buttons sparingly; when action buttons exceed 4, collapse into a "More" button whose panel is ≤ 200px.

**`S04` Input controls (8 rules):** `S04-01` required mark (red `*`, ERROR), `S04-02` placeholder text (WARNING), `S04-03` disabled-state style (WARNING), `S04-04` dropdown convention (WARNING), `S04-05` clear function (SUGGESTION), `S04-06` label layout (WARNING), `S04-07` editable area (WARNING), `S04-08` query-panel convention (WARNING). Required labels get a leading red asterisk; label and control are stacked top-to-bottom; label max width is 8 Chinese characters (truncate beyond); a query panel places three controls per row; quick-query conditions ≤ 3.

**`S05` Tables (11 rules):** `S05-01` row-number column (ERROR), `S05-02` checkbox column (WARNING), `S05-03` action column (WARNING), `S05-04` frozen-column count ≤ 3 (WARNING), `S05-05` zebra striping (WARNING), `S05-06` header-row style (WARNING), `S05-07` content-alignment rules (WARNING), `S05-08` total row (WARNING), `S05-09` hyperlink style (WARNING), `S05-10` column-width setting (SUGGESTION), `S05-11` filter/sort (SUGGESTION). First column is the row-number column (frozen left); last column is the action column (frozen right); zebra striping is white on odd rows, light grey on even; header row is bold and centered; content rows left-align text, right-align numbers, center status; numeric columns use thousands separators and amounts default to two decimals; the total row sits below the table with the selected-total row above it; each side freezes ≤ 3 columns.

## Procedure
1. **Step 0 — detect version (never skip).** Read `package.json` at the project root, extract `version`. If it cannot be extracted, default to `3.6.0-SNAPSHOT`. Match against the version map: exact match wins; otherwise match the `major.minor` series and take the newest directory in that series; otherwise fall back to the `3.6.0-SNAPSHOT` baseline and emit a warning.
2. **Step 1 — load rules.** Read the `REFERENCE.md` in the resolved version directory under `references/original/versions/<version>/`.
3. **Step 2 — check.** Scope the target files and rule categories (color / typography / button / input / table / all), then apply the per-category rules in `scripts/` (`color-rules.md`, `typography-rules.md`, `button-rules.md`, `input-rules.md`, `table-rules.md`) and report compliant items, violations, and fix suggestions.
4. **Step 2 — samples.** Display canonical examples from `examples/` (`E01`–`E07`: buttons, inputs, tables, pagination, tree, tabs, breadcrumb).
5. **Step 2 — generate.** From `templates/` (`T05`–`T10`: query panel, data table, form card, detail card, audit log, progress bar), read the code skeleton for the requested component, adjust details against the matching sample, and self-check the output against the matching rules.

## Guardrails
- Do not change business logic/behavior; structural + standards refactoring only.
- The ~57 bundled component code samples and templates under `references/original/` are the verbatim source of truth — do not translate or rewrite their code; copy and reuse them as-is. Preserve exact color values, font sizes, and pixel limits when generating or fixing components.

## Verify
- Version was detected from `package.json` (or the documented fallback applied) and the correct version directory was loaded.
- For a check: the selected `S01`–`S05` rules were all evaluated and reported.
- Generated components use CSS variables (no hard-coded colors), carry `aria`/accessible labels, and match the canonical palette, font sizes, button/input/table conventions above.

## References
The exhaustive original rules, versioned rule sets, and component/page templates are bundled verbatim under `references/original/` (source of truth). Consult them for per-version detail and code samples.

## Chain position
Runs after refactor-web-02-modules. On success the orchestrator advances to refactor-web-04-layout. `refactor-code-solid` runs by default as the final step of the lane.
