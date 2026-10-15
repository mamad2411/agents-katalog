---
name: figma-to-design-init
description: Initialize the design-to-code workflow. Scans your codebase for styling patterns, extracts design tokens, discovers reusable components, detects API call patterns, and generates design token files under .claude/design-tokens/. Run this once per project before using /figma-to-design-build.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__figma
---

# Initialize Design System

You are initializing the design-to-code workflow for this project. Your job is to deeply understand the existing codebase's design patterns and produce a `design-tokens.json` file at `.claude/design-tokens/design-tokens.json`.

## Pre-check: Incremental Update

Before scanning, check if `.claude/design-tokens/design-tokens.json` exists.

- If it **does not exist**: create the `.claude/design-tokens/` directory and proceed with a full scan (Steps 1-8).
- If it **does exist**: read it into context. Then run a targeted scan:
  1. Check if the styling approach or config file has changed. If yes, re-extract tokens (Step 2).
  2. Scan only for new, modified, or deleted components and hooks since the file was last generated (compare file paths in the existing JSON against what's on disk).
  3. Check if `package.json` dependencies have changed — compare installed packages against the `preferred_libraries` section. If new libraries were added to an existing category, or a new category now has libraries, re-run Step 5 for those categories only. Ask the user to re-choose if a new competing library was added to a category that previously had only one.
  4. Merge changes into the existing `design-tokens.json` — add new entries, update changed entries, remove entries for deleted files.
  5. Skip Steps 7-8's Playwright/pixelmatch install if already installed.

This avoids re-reading the entire codebase when only a few components have changed.

## Step 1: Identify the Styling Approach

Scan the project for how styles are written. Look for:

- `tailwind.config.ts` or `tailwind.config.js` → Tailwind CSS
- `*.module.css` or `*.module.scss` files → CSS/SCSS Modules
- `styled-components`, `@emotion/styled`, or `@emotion/css` in `package.json` → CSS-in-JS
- `.css` files imported directly into components → Vanilla CSS
- A combination of the above

Record the primary styling approach. If mixed: count the number of component files (`.tsx`, `.jsx`) using each approach. The approach used by >50% of component files is `primary`. Others are `secondary`. If no approach exceeds 50%, record as `mixed` and list all approaches in descending order of file count.

## Step 2: Extract Design Tokens

Based on the styling approach, extract tokens from the appropriate source:

**If Tailwind:** Read `tailwind.config.ts/js` and extract the `theme` / `extend` values — colors, spacing, fontFamily, fontSize, borderRadius, boxShadow, screens (breakpoints).

**If CSS Variables:** Search for `:root` or `[data-theme]` blocks in CSS files. Extract all custom properties.

**If CSS-in-JS / Theme file:** Look for theme objects (commonly in `theme.ts`, `styles/theme.ts`, `lib/theme.ts`, or similar). Extract the token values.

**If Vanilla CSS:** Scan all `.css` files in `src/` and `app/`. A value is a token if it appears in 3+ separate files. Record the exact value and assign a generated name based on context (e.g., `color-1`, `color-2`, `spacing-1`). Sort tokens by frequency descending.

For all approaches, extract:
- **Colors**: primary, secondary, background, surface, text, border, error, success, warning, info — and any other semantic color names used
- **Spacing**: the scale or common spacing values used
- **Typography**: font families, size scale, weight scale, line heights
- **Breakpoints**: responsive breakpoints
- **Shadows**: box-shadow values
- **Borders**: border-radius values, border widths

## Step 3: Discover Reusable Components

Scan the project for existing UI components. Common locations:
- `src/components/`, `src/components/ui/`, `components/`, `app/components/`
- Any barrel export files (`index.ts`) that re-export components

For each component found, record:
- **name**: The component name
- **path**: File path relative to project root
- **description**: Must follow this exact format: `[Component type] that [primary function]. Supports [key prop categories].` Example: `Button component that triggers actions. Supports variant, size, and loading state.` Do not use free-form descriptions — stick to this template.
- **props**: The props it accepts (read from TypeScript types, PropTypes, or the JSX usage). List all prop names alphabetically.

**Inclusion criteria (deterministic):**
- **Include** any component that is imported by 2+ files (check with grep for import statements referencing the component file).
- **Include** any component that is imported by only 1 file IF it lives in a directory named `ui/`, `shared/`, `common/`, or `primitives/`.
- **Skip** everything else — these are page-specific components.

A component is page-specific if it lives inside a route directory (e.g., `app/dashboard/components/`) AND is imported by only 1 file.

## Step 4: Discover Shared Hooks and Utilities

Look for custom hooks relevant to UI development:
- `useMediaQuery`, `useBreakpoint` → responsive behavior
- `useDebounce`, `useThrottle` → input handling
- `useClickOutside` → dropdowns, modals
- `useForm`, `useFormField` → form state
- Any data fetching hooks

Record these in a `hooks` section with name, path, and description.

## Step 5: Detect Libraries and Resolve Competing Choices

This step scans `package.json` to find all installed libraries, groups them by capability category, and asks the user to choose a preferred library when multiple options exist in the same category. This ensures the build skill always uses the right library for new code.

### Step 5a: Scan package.json

Read `package.json` → `dependencies` and `devDependencies`. For every installed package, check if it belongs to a known capability category. A library belongs to a category if its package name matches.

**Known categories and their members (this is a starting reference, NOT an exhaustive list):**

| Category | Known libraries |
|----------|----------------|
| data_fetching | `@tanstack/react-query`, `@tanstack/query`, `swr`, `axios`, `@apollo/client`, `urql`, `graphql-request` |
| realtime | `ably`, `socket.io-client`, `pusher-js`, `@supabase/realtime-js`, `firebase`, `@firebase/messaging` |
| state_management | `zustand`, `@reduxjs/toolkit`, `redux`, `jotai`, `recoil`, `mobx`, `mobx-react`, `valtio`, `xstate` |
| forms | `react-hook-form`, `formik`, `@tanstack/react-form`, `final-form`, `react-final-form` |
| validation | `zod`, `yup`, `joi`, `superstruct`, `valibot`, `@sinclair/typebox` |
| dates | `date-fns`, `dayjs`, `moment`, `luxon`, `@date-io/date-fns`, `@date-io/dayjs`, `@date-io/moment` |
| animation | `framer-motion`, `react-spring`, `@react-spring/web`, `gsap`, `motion`, `auto-animate`, `@formkit/auto-animate` |
| icons | `lucide-react`, `react-icons`, `@heroicons/react`, `@phosphor-icons/react`, `@tabler/icons-react`, `@iconify/react` |
| charts | `recharts`, `chart.js`, `react-chartjs-2`, `@nivo/core`, `victory`, `@visx/visx`, `d3`, `apexcharts`, `react-apexcharts`, `tremor` |
| tables | `@tanstack/react-table`, `ag-grid-react`, `@ag-grid-community/react`, `react-data-grid` |
| date_picker | `react-datepicker`, `react-day-picker`, `@mui/x-date-pickers`, `@mantine/dates` |
| carousel | `swiper`, `embla-carousel-react`, `keen-slider`, `react-slick`, `splide`, `@splidejs/react-splide` |
| toast_notification | `react-hot-toast`, `react-toastify`, `sonner`, `@radix-ui/react-toast`, `notistack` |
| modal_dialog | `@radix-ui/react-dialog`, `@headlessui/react`, `react-modal`, `@mui/material` |
| maps | `react-map-gl`, `@react-google-maps/api`, `leaflet`, `react-leaflet`, `mapbox-gl`, `@vis.gl/react-google-maps` |
| rich_text | `tiptap`, `@tiptap/react`, `slate`, `slate-react`, `draft-js`, `react-quill`, `@lexical/react` |
| drag_and_drop | `@dnd-kit/core`, `react-beautiful-dnd`, `@hello-pangea/dnd`, `react-dnd` |
| testing | `vitest`, `jest`, `@testing-library/react`, `cypress`, `playwright` |
| css_in_js | `styled-components`, `@emotion/styled`, `@emotion/css`, `@stitches/react`, `vanilla-extract` |
| component_library | `@mui/material`, `@mantine/core`, `@chakra-ui/react`, `@radix-ui/themes`, `@nextui-org/react`, `antd`, `@shadcn/ui` |
| internationalization | `next-intl`, `react-i18next`, `i18next`, `react-intl`, `@formatjs/intl` |
| auth | `next-auth`, `@auth/core`, `@clerk/nextjs`, `@supabase/auth-helpers-nextjs`, `firebase/auth` |

**IMPORTANT: This list is a starting reference.** If you encounter an installed package that is NOT in this list but clearly belongs to a capability category (e.g., a new charting library, a new form library), create a new category or add it to the appropriate existing one. The goal is to catch ALL competing libraries, not just the ones listed above. Use the package name and its npm description to determine its category.

### Step 5b: Also detect `fetch` usage

`fetch` is not a package — it's a built-in. Scan source files for `fetch(` usage. If found, add `fetch (built-in)` to the `data_fetching` category.

Similarly, scan for:
- `"use server"` → add `next-server-actions (built-in)` to `data_fetching`
- CSS `@import` / `.css` file imports → add `vanilla-css (built-in)` to `css_in_js` if relevant

### Step 5c: Count usage per library

For each detected library, count how many source files (`.ts`, `.tsx`, `.js`, `.jsx`) import or use it. This is used for the recommendation.

### Step 5d: Identify categories with competing libraries

For each category:
- **If 0 libraries detected** → skip the category entirely, do not record it.
- **If exactly 1 library detected** → auto-select it. No question needed. Record it silently.
- **If 2+ libraries detected** → this is a conflict. Ask the user to choose (Step 5e).

### Step 5e: Ask the user to choose preferred libraries

For each category with 2+ libraries, present the options to the user with a recommendation. Ask all conflicting categories in a **single message**.

**Recommendation logic (deterministic):**
1. The library used in the most source files is the default recommendation.
2. Exception: if a library is widely known to be deprecated or unmaintained (e.g., `moment` is deprecated, `react-beautiful-dnd` is unmaintained), recommend the next most-used alternative instead and note the deprecation.

**Format:**

> I found multiple libraries for the same purpose in these categories:
>
> **Data fetching**: `@tanstack/react-query` (8 files), `swr` (5 files), `fetch` (12 files)
> → Recommended: **@tanstack/react-query** (most structured usage, best loading/error state support)
>
> **Dates**: `date-fns` (14 files), `moment` (6 files)
> → Recommended: **date-fns** (moment is deprecated, date-fns is actively maintained)
>
> **Forms**: `react-hook-form` (4 files), `formik` (7 files)
> → Recommended: **formik** (used in more files)
>
> For each category, which library should I use when generating new code?

Wait for the user to respond. If the user says "go with recommendations" or similar, use all recommended options.

### Step 5f: Detect API-specific configuration

After the user selects a preferred data fetching library, scan for its configuration:

- **API base URL**: look for `axios.create({ baseURL })`, environment variables like `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_BASE_URL`, or similar.
- **Query client setup**: if React Query or SWR, look for `QueryClientProvider`, `SWRConfig`, default options.
- **API utility files**: look in `lib/api.ts`, `utils/api.ts`, `services/api.ts`, `api/index.ts`.
- **Auth header injection**: interceptors, middleware, fetch wrappers.

Record API-specific patterns using these exact enum values:
- **`error_handling`** — must be one of: `toast`, `error-boundary`, `inline-message`, `console-only`, `none-detected`. If multiple patterns coexist, use the one that appears in >50% of API call sites. If no pattern exceeds 50%, use `mixed` and note the top two.
- **`loading_pattern`** — must be one of: `react-query-isLoading`, `swr-isLoading`, `suspense`, `useState-loading`, `skeleton-component`, `none-detected`. Same >50% rule applies.
- **`response_envelope`** — search for a consistent wrapper object shape across 3+ API responses. Record the exact key names (e.g., `{ data, error, meta }`). If no consistent shape across 3+ responses, record `none-detected`.
- **Shared types** — check for API response types in `types/`, `interfaces/`, or co-located with API calls. Record the path to the types directory if one exists.

## Step 5d: Import Figma Variables (Optional)

If Figma MCP is available and the user provides a Figma file URL (or one was used in a previous build), attempt to import Figma Variables to enrich the design tokens.

1. Use the Figma MCP `get_variable_defs` tool with the Figma file's node ID and file key to pull the file's variable definitions.
2. Figma Variables typically include:
   - **Color variables**: semantic colors like `primary`, `secondary`, `background`, `text`, organized by collection/mode (e.g., light/dark)
   - **Spacing variables**: spacing scale values
   - **Typography variables**: font sizes, line heights, font weights
   - **Border radius variables**: radius values

3. **Merge strategy — Figma Variables supplement, they do not override. Match by exact key name only:**
   - If a Figma Variable's key name exactly matches a codebase token key name, keep the codebase version as the source of truth. Do NOT match by value similarity or fuzzy name matching — exact key name match only.
   - If a Figma Variable has no codebase equivalent (no exact key name match), add it to the tokens with a `"source": "figma"` annotation.
   - If a Figma Variable and codebase token have the same exact key name but different values, flag the mismatch to the user in the verification step (Step 8).

4. Record any imported Figma Variables in a `figma_variables` section for reference:

```json
"figma_variables": {
  "imported_from": "<figma file URL or key>",
  "mismatches": [
    {
      "name": "primary",
      "figma_value": "#2563EB",
      "code_value": "#3B82F6",
      "status": "flagged"
    }
  ]
}
```

If Figma MCP is not available or no Figma file URL is known, skip this step entirely. Do not ask the user for a Figma URL during init — this is an optional enrichment, not a requirement.

## Step 6: Generate design-tokens.json

Write the file to `.claude/design-tokens/design-tokens.json`. Create the `.claude/design-tokens/` directory if it does not exist. Structure:

```json
{
  "styling_approach": "<tailwind | css-modules | css-in-js | vanilla-css | mixed>",
  "styling_config_path": "<path to tailwind config, theme file, or primary CSS file>",
  "colors": { },
  "spacing": { },
  "typography": { },
  "breakpoints": { },
  "shadows": { },
  "borders": { },
  "components": [
    {
      "name": "ComponentName",
      "path": "src/components/ui/ComponentName.tsx",
      "description": "What it does in plain English",
      "props": ["variant", "size", "children"]
    }
  ],
  "hooks": [
    {
      "name": "useHookName",
      "path": "src/hooks/useHookName.ts",
      "description": "What it does"
    }
  ],
  "preferred_libraries": {
    "<category_name>": {
      "selected": "<package name the user chose>",
      "installed": ["<all installed packages in this category>"],
      "file_count": { "<package>": "<number of files using it>" }
    }
  },
  "api": {
    "config_path": "<path to API config/setup file, e.g., lib/api.ts>",
    "query_client_path": "<path to QueryClient setup if using React Query/SWR>",
    "base_url_env": "<environment variable name for API base URL, e.g., NEXT_PUBLIC_API_URL>",
    "response_envelope": "<exact key names if consistent across 3+ responses, e.g., { data, error, meta } | none-detected>",
    "auth_pattern": "<axios-interceptor | fetch-wrapper | next-auth-session | auth-header-manual | none-detected>",
    "error_handling": "<toast | error-boundary | inline-message | console-only | mixed | none-detected>",
    "loading_pattern": "<react-query-isLoading | swr-isLoading | suspense | useState-loading | skeleton-component | mixed | none-detected>"
  }
}
```

**`preferred_libraries` rules:**
- Include ALL categories where at least 1 library was detected.
- For categories with only 1 library, `selected` and `installed` will both contain just that one library.
- For categories where the user chose, `selected` is the user's choice, `installed` lists everything found.
- The build skill reads `preferred_libraries.<category>.selected` to decide which library to use.
- The old `api.client` field is removed — the data fetching library is now at `preferred_libraries.data_fetching.selected`.

**Example:**

```json
"preferred_libraries": {
  "data_fetching": {
    "selected": "@tanstack/react-query",
    "installed": ["@tanstack/react-query", "swr", "fetch (built-in)"],
    "file_count": { "@tanstack/react-query": 8, "swr": 5, "fetch (built-in)": 12 }
  },
  "dates": {
    "selected": "date-fns",
    "installed": ["date-fns", "moment"],
    "file_count": { "date-fns": 14, "moment": 6 }
  },
  "icons": {
    "selected": "lucide-react",
    "installed": ["lucide-react"],
    "file_count": { "lucide-react": 22 }
  },
  "realtime": {
    "selected": "ably",
    "installed": ["ably"],
    "file_count": { "ably": 3 }
  },
  "forms": {
    "selected": "react-hook-form",
    "installed": ["react-hook-form"],
    "file_count": { "react-hook-form": 9 }
  }
}
```

If no libraries are detected in any category (e.g., a brand new project with no dependencies), omit the `preferred_libraries` section entirely.

The `api` section is now only for API-specific configuration (base URL, auth, error handling, loading patterns). It is only included if a `data_fetching` library exists in `preferred_libraries`. Omit it entirely for projects with no data fetching.

## Step 7: Check Playwright and Pixelmatch

Ensure Playwright and pixelmatch are installed globally and ready for the visual verification workflow.

**Playwright:**
1. Run `npx playwright --version` to check if Playwright is available.
2. If not installed, run `npm install -g playwright` and then `npx playwright install chromium`.
3. If already installed, skip.

**Pixelmatch (for objective visual scoring):**
1. Run `npx pixelmatch 2>&1` to check if pixelmatch CLI is available.
2. If not available, run `npm install -g pixelmatch`.
3. Verify with `npx pixelmatch --help` or `pixelmatch 2>&1`.
4. If already installed, skip.

## Step 8: Verify and Confirm

After generating the file:
1. Show the user a summary:
   - Styling approach detected
   - Number of colors/tokens extracted
   - Components discovered (count and names)
   - Hooks found (count and names)
   - **Preferred libraries** — list each category and the selected library. For categories where the user made a choice, note it. For auto-selected (single library) categories, note they were auto-selected.
   - API configuration detected (if any)
   - Figma variable mismatches (if any)
2. Ask if anything looks wrong or missing
3. If they correct something, update the file
4. Confirm initialization is complete and they can now use `/figma-to-design-build`

## Important Rules

- Do NOT invent tokens that don't exist in the codebase. Only record what's actually there.
- If the project is new with almost no tokens or components, say so. A sparse file is fine.
- If you find inconsistencies (e.g., 5 different grays with no naming convention), note them but record as-is. Don't "clean up" the design system — that's the user's job.