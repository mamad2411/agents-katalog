---
name: admin-page-fix-workflow
description: "Use when fixing Admin page UI, responsive layout issues, and React hook/lint problems in qr-presensi-frontend (Admin.jsx/Admin.css)."
---

# Admin Page Fix Workflow

## Outcome

Deliver a clean, responsive Admin page with stable React hooks, no lint errors in the touched files, and consistent styling without heavy inline CSS.

## Steps

1. Read `src/pages/Admin.jsx` and `src/pages/Admin.css` first.
2. Check for React hook issues:

- Callback used before declaration
- Missing hook dependencies
- Unused state/variables

3. Move repeated async loaders to `useCallback` when referenced by effects.
4. Replace inline style blocks with semantic class names.
5. Ensure layout is responsive:

- Desktop: two-panel card layout
- Mobile: one-column stack

6. Normalize data used by map markers:

- Parse `lat`/`lng` as numbers
- Filter invalid coordinates
- Provide empty-state message when no points

7. Improve safety/accessibility quickly:

- Add `rel="noreferrer"` for external links opened in new tab
- Use button `type="button"` for non-submit actions

8. Validate with diagnostics (`get_errors`) for edited files.

## Decision Points

- If API returns GPS logs separately, prefer GPS logs for map points; otherwise fallback to presence records.
- If global CSS (e.g. Vite default `index.css`) distorts the page, either override in page scope or clean globals only when safe across routes.
- If table overflows on small screens, keep horizontal scrolling in a dedicated wrapper.

## Completion Checks

- `Admin.jsx` and `Admin.css` show no lint/compile issues.
- Admin page stays readable on desktop and mobile widths.
- QR controls, presence table, and modal map all remain usable.
- No critical inline style blocks remain except unavoidable third-party props.

## Example Prompts

- "Apply the admin-page-fix-workflow skill to improve Admin.jsx and Admin.css."
- "Use admin-page-fix-workflow to fix hook dependency warnings and mobile layout in Admin page."
