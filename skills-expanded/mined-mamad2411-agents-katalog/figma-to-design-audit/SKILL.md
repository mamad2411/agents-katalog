---
name: figma-to-design-audit
description: Audit your codebase for design token drift. Finds hardcoded colors, spacing, and font values that should use design tokens. Reports unused tokens and components not following the design system. Run periodically to keep your codebase consistent.
allowed-tools: Read, Bash, Glob, Grep
---

# Design Token Drift Audit

You are auditing this project's codebase to find violations of the design system. Your job is to detect hardcoded values that should use design tokens, find unused tokens, and report components that bypass the design system.

---

## Pre-flight Check

1. Check that `.claude/design-tokens/design-tokens.json` exists. If it doesn't, tell the user to run `/figma-to-design-init` first and stop.
2. Read `.claude/design-tokens/design-tokens.json` fully into context.

---

## Audit 1: Hardcoded Values That Should Be Tokens

Scan all React/Next.js source files (`.tsx`, `.jsx`, `.ts`, `.js`) and style files (`.css`, `.scss`, `.module.css`, `.module.scss`) for hardcoded values that exist in the design tokens or should be using them.

### Colors
- Search for raw hex colors (`#[0-9a-fA-F]{3,8}`), `rgb(`, `rgba(`, `hsl(`, `hsla(` in component files and style files.
- Exclude: SVG files, image assets, config files (`tailwind.config.*`, `postcss.config.*`), `node_modules`, `.next`, test files.
- **Color comparison rule (exact match only):** Convert all found colors to lowercase 6-digit hex before comparison. Convert `rgb()` and `hsl()` values to hex. A match is exact hex equality only — no fuzzy matching, no "near-equivalent" matching.
- For each hardcoded color found, check if it exactly matches any value in `design-tokens.json` → `colors`. If yes, label it `definite` — this value should use the token.
- Also flag colors that do NOT exactly match any token value — label these `undocumented`.

### Spacing
- Search for hardcoded pixel values in padding, margin, gap, width, height properties: `padding: 16px`, `margin: 24px`, `gap: 8px`, `p-[16px]`, `m-[24px]`, etc.
- In Tailwind projects, look for arbitrary value brackets: `p-[...]`, `m-[...]`, `gap-[...]`, `w-[...]`, `h-[...]` with pixel values that match the spacing scale.
- Flag values that match the spacing scale but use raw numbers instead of tokens.

### Typography
- Search for hardcoded font sizes: `font-size: 14px`, `text-[14px]`, etc.
- Search for hardcoded font weights: `font-weight: 600`, `font-[600]`, etc.
- Search for hardcoded line heights in style declarations.
- Flag values that match the typography scale but use raw numbers instead of tokens.

### Shadows & Borders
- Search for hardcoded `box-shadow` values and `border-radius` values.
- Flag values that match tokens but are hardcoded.

---

## Audit 2: Unused Tokens

Check each token defined in `design-tokens.json` to see if it's actually used in the codebase.

**Search patterns by styling approach (deterministic):**

- **For Tailwind projects — color tokens:** Search for each color token name prefixed with `bg-`, `text-`, `border-`, `ring-`, `fill-`, `stroke-`, `decoration-`, `accent-`, `outline-`, `shadow-`. A color token is "used" if ANY of these prefixed forms appear in source files.
- **For Tailwind projects — spacing tokens:** Search for each spacing token name prefixed with `p-`, `px-`, `py-`, `pt-`, `pr-`, `pb-`, `pl-`, `m-`, `mx-`, `my-`, `mt-`, `mr-`, `mb-`, `ml-`, `gap-`, `gap-x-`, `gap-y-`, `w-`, `h-`, `space-x-`, `space-y-`, `inset-`, `top-`, `right-`, `bottom-`, `left-`. A spacing token is "used" if ANY of these prefixed forms appear.
- **For Tailwind projects — typography tokens:** Search for font family with `font-`, font size with `text-`, font weight with `font-`, line height with `leading-`.
- **For Tailwind projects — shadow tokens:** Search with `shadow-` prefix.
- **For Tailwind projects — border tokens:** Search with `rounded-` and `border-` prefixes.
- **For CSS variable projects:** Search for `var(--token-name)` usage. Exact string match.
- **For CSS-in-JS projects:** Search for `theme.colors.tokenName`, `theme.spacing.tokenName`, etc. Exact property path match.

Report tokens that exist in the token file but have zero references in the codebase. Label each as:
- `unused` — zero matches found across all search patterns
- `build-only` — if the token appears only in files under `.next/`, `dist/`, or `build/` (false positive — note this)

---

## Audit 3: Component Reuse Violations

Check if page-level files use raw HTML elements instead of existing reusable components.

**Detection method (deterministic):**
1. Search for raw HTML elements (`<button`, `<input`, `<select`, `<textarea`, `<dialog`, `<table`) in files under `app/` and `src/pages/` (page-level files only, NOT files inside component directories).
2. For each raw HTML element found, check if a corresponding component exists in the `components` array of `design-tokens.json`. Match by element type to component name:
   - `<button` → any component with `button` (case-insensitive) in its name
   - `<input` → any component with `input` or `textfield` in its name
   - `<select` → any component with `select` or `dropdown` in its name
   - `<textarea` → any component with `textarea` in its name
   - `<dialog` → any component with `dialog` or `modal` in its name
   - `<table` → any component with `table` in its name
3. If a raw element is found AND a matching component exists, flag it as a violation.
4. Do NOT flag raw elements in component files themselves (they are the implementation).

---

## Audit 4: Preferred Library Violations (if applicable)

If `preferred_libraries` exists in `design-tokens.json`:

**4a: Data fetching violations.**
If `preferred_libraries.data_fetching` exists, check that components use the `selected` data fetching library, not alternatives:
- If selected is `@tanstack/react-query` but a component uses raw `fetch` or `useEffect` + `useState` for data fetching, flag it.
- If selected is `@tanstack/react-query` but a component imports `swr`, flag it.
- If selected is `axios` but a component uses raw `fetch`, flag it.
- Check for missing error handling on API calls (no `onError`, no `.catch()`, no error state).
- Check for missing loading states on API calls.

**4b: Other library category violations.**
For each category in `preferred_libraries` where `installed` has more than 1 entry, check that source files use the `selected` library and not a non-selected alternative:
- If `dates.selected` is `date-fns` but a file imports `moment`, flag it.
- If `forms.selected` is `react-hook-form` but a file imports `formik`, flag it.
- Apply the same check for all categories with competing libraries.

**Detection method:** For each non-selected library in a category, grep for its import statement (`import ... from '<package>'` or `require('<package>')`). Any match in source files (excluding `node_modules`, config files, and lock files) is a violation.

---

## Report Format

Present the audit results as a structured report:

```
## Design Token Drift Audit Report

### Hardcoded Values Found
| File | Line | Value | Should Be | Token Name |
|------|------|-------|-----------|------------|
| src/components/Header.tsx | 42 | #3B82F6 | Token | primary |
| src/app/dashboard/page.tsx | 87 | padding: 24px | Token | spacing-6 |

**Total: X hardcoded values across Y files**

### Unused Tokens
| Token | Category | Defined Value |
|-------|----------|---------------|
| warning | colors | #F59E0B |

**Total: X unused tokens**

### Component Reuse Violations
| File | Line | Issue | Suggested Component |
|------|------|-------|-------------------|
| src/app/settings/page.tsx | 23 | Inline button styling | Use Button component |

**Total: X potential violations**

### Preferred Library Violations (if applicable)
| File | Line | Issue | Category | Selected | Used Instead |
|------|------|-------|----------|----------|-------------|
| src/app/users/page.tsx | 15 | Uses raw fetch | data_fetching | @tanstack/react-query | fetch |
| src/utils/format.ts | 8 | Imports moment | dates | date-fns | moment |

**Total: X library violations**

### Summary
- Hardcoded values: X (Y are direct token matches, Z are new/undocumented)
- Unused tokens: X
- Component reuse violations: X
- Preferred library violations: X
- **Design system adherence score: X/100**
```

Calculate the adherence score as: `100 - (total_violations * penalty)` where each hardcoded value = -1 point, each unused token = -0.5 points, each component violation = -2 points, each library violation = -2 points. Floor at 0, cap at 100.

---

## Important Rules

- Only scan source files. Skip `node_modules`, `.next`, `dist`, `build`, `coverage`, test files (`*.test.*`, `*.spec.*`, `__tests__/`), and config files (`*.config.*`, `postcss.*`).
- **Flag ALL matches from regex scans.** Label each as either `definite` (the hardcoded value exactly matches a token value) or `undocumented` (the hardcoded value has no matching token). Do not skip any regex match. Do not use subjective confidence — every match is either exact-match or not.
- Do not modify any files. This is a read-only audit.
- If the project is small (< 10 source files), say so and note that the audit may be less meaningful.
