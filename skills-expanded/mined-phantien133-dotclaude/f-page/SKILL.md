# f-page — Integrate Figma Pages into Project

Integrates generated page components from a Figma manifest into the project,
substituting UI kit components for any ad-hoc inline equivalents.

Called by `f-import` after `f-ui-kit` completes. Can also be invoked directly.

**Prerequisite:** `f-ui-kit` must have run on this manifest (components need
`installed_path` values set). Verified in Step 0.

---

## Input

```
Manifest path (from f-import):
  f-page <manifest-path>

Direct export-only shorthand:
  /f-page src/exports/auth-pages
  /f-page auth:src/exports/auth-pages
```

Parse `$ARGUMENTS`:
- If contains `:` before a path → extract module scope from prefix
- If arg ends with `.yaml` → manifest mode
- Otherwise → export folder mode (build ad-hoc manifest inline from folder)

---

## Step 0 — Validate

Read `.claude/figma.yaml` (error if missing → "Run /f-setup first").

Resolve:
- `module` = parsed scope or null
- `ui_kit_path` = `<cfg.output.component_base>/<module>/ui-kit/` or `<cfg.output.component_base>/ui-kit/`

Verify UI kit exists: check that `ui_kit_path` contains at least one `.tsx` or `.jsx` file.

If empty or missing:
```
No UI kit found at <ui_kit_path>.
Run /f-ui-kit first (or /f-import to run both together).
```

Build **component catalogue** from UI kit: read each installed component file,
extract component name, props signature, and what it renders (first JSX element type).

---

## Step 1 — Load manifest (or scan folder)

**Manifest mode:** Read `manifest.yaml`. Select components with `role: page`.

**Export folder mode:** Read all files in folder. Classify each:
- Apply same heuristics as f-ui-kit Step 1 but keep only `role: page` items
- Anything that looks like a shared component → skip (note in report)

If multiple page files found: ask which to build before continuing.

```
Multiple pages found. Which would you like to integrate?
  [1] SignIn.tsx
  [2] SignUp.tsx
  [3] ForgotPassword.tsx
  [4] All
```

Wait for selection.

---

## Step 2 — Detect page target paths

For each selected page, resolve target path using framework from config:

| Framework | Pattern |
|-----------|---------|
| Next.js App Router | `app/<module>/<slug>/page.tsx` where slug = kebab-case(page name) |
| Next.js Pages Router | `pages/<module>/<slug>.tsx` |
| Vite / CRA | `src/pages/<Module>/<PageName>.tsx` |

---

## Step 3 — Show integration plan + confirm

```
## f-page integration plan

Source:      src/exports/auth-pages
Module:      auth
UI kit path: src/components/auth/ui-kit/

Pages to integrate:
  SignIn.tsx   → app/auth/sign-in/page.tsx
  SignUp.tsx   → app/auth/sign-up/page.tsx

Component mapping:
  Source          UI kit        Action
  PrimaryButton   Button        replace (3 occurrences)
  TextInput       Input         replace (2 occurrences)
  CustomCard      —             keep inline
  ErrorMessage    —             keep inline

Transformations:
  - HTML → React conversions
  - Import rewrites to @/ alias
  - Substitute PrimaryButton → Button, TextInput → Input

Proceed? [y/n]
```

Mapping logic: for each inline component defined in the page source, fuzzy-match
against UI kit catalogue names. Match if:
- Exact name match (case-insensitive)
- Or name is a common synonym: PrimaryButton↔Button, TextInput↔Input,
  TextArea↔Textarea, SelectBox↔Select, CheckBox↔Checkbox

Wait for confirmation.

---

## Step 4 — Transform + write each page

For each page file:

1. Read source.
2. For each mapped component: replace all JSX usages. Adapt props if needed
   (e.g. `value=` → `defaultValue=` if the UI kit component uses that name;
   note mismatches for manual review rather than silently dropping props).
3. Remove inline component definitions that were replaced (the function bodies).
4. Update all imports:
   - Remove imports for replaced components.
   - Add imports from UI kit path (`@/components/<module>/ui-kit/<Name>`).
   - Rewrite remaining relative imports to use project alias.
5. Apply HTML→React conversions:
   - `class=` → `className=`
   - `for=` → `htmlFor=`
   - Void elements self-close
   - Inline style strings → object syntax
6. For Next.js App Router: ensure `"use client"` at top if component uses hooks or event handlers.
7. Write to target path.
   - If target already exists: write as `<name>-new.<ext>` and notify.

---

## Step 5 — Handle styles

| File type | Action |
|-----------|--------|
| `*.module.css` matching a page | Place next to the page file in its target directory |
| Global stylesheet | Append non-duplicate rules to project global stylesheet |
| Tailwind-only project | Skip all `.css` files |

---

## Step 6 — Report

```
## f-page complete

Pages written (2):
  app/auth/sign-in/page.tsx (created)
  app/auth/sign-up/page.tsx (created)

Component substitutions:
  PrimaryButton → Button  (3 occurrences in sign-in, 2 in sign-up)
  TextInput → Input       (2 occurrences in sign-in, 3 in sign-up)

Kept inline (potential future UI kit additions):
  CustomCard  — appears in sign-in
  ErrorMessage — appears in both pages

Manual follow-up:
  - sign-in: prop "inputMode" on TextInput has no match in Input — kept as-is, verify
  - sign-up: "use client" added (uses useState)
```

---

## allowed-tools

Read, Write, Bash
