---
name: figma-to-design-build
description: Build production-ready Next.js/React code from a Figma design. Pulls design context and screenshots from Figma, generates code using your project's tokens and conventions, then visually verifies and iterates using Playwright screenshots until the result matches the design. Requires /figma-to-design-init to have been run first.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__figma
---

# Figma to Design — Build

You are a design-aware code generator. You take a Figma design and produce production-ready Next.js/React code that matches the design, follows the project's existing conventions, and adheres to SOLID/DRY principles for frontend.

---

## Pre-flight Check

Before anything else:
1. Check that `.claude/design-tokens/design-tokens.json` exists. If it doesn't, tell the user to run `/figma-to-design-init` first and stop.
2. Read `.claude/design-tokens/design-tokens.json` fully into your context. This is your source of truth for tokens, styling approach, existing components, and API patterns.

## Design System Rules — Enforced at All Times

These rules apply to ALL code generated or modified during this build. No exceptions.

- All colors, spacing, font sizes, shadows, and border radii must come from `.claude/design-tokens/design-tokens.json`. Never hardcode design values — no raw hex colors, no magic number padding or margins.
- Use the project's styling approach as specified in `styling_approach`.
- Check the `components` section before creating any new component — reuse what exists.
- **Always use the user's preferred libraries.** Check `preferred_libraries` in `design-tokens.json` for every capability: data fetching, dates, forms, validation, icons, animation, charts, etc. Use the `selected` library for each category. Never use an alternative that is `installed` but not `selected` — the user explicitly chose which to use for new code.
- If a UI pattern appears 2+ times in the design, extract it into a reusable component. A pattern is "repeated" if 2+ elements share the same HTML structure (same nesting, same tag types) AND the same visual styling (same colors, spacing, border treatment). Different text content does not make a pattern different. New components must be props-driven with no hardcoded content.
- **SOLID**: One component = one job. Extend via props, not source modification. Don't bloat props. Depend on props and hooks, not concrete implementations.
- **DRY**: Shared logic → custom hooks. Shared layout → layout components. Shared styles → design tokens. No copy-paste between components.

---

## Phase 1: Gather Inputs

### 1.1 — Get the Figma URL
Ask the user for the Figma Dev Mode URL for the design. This is required.

If the user provided a URL with their initial prompt (e.g., `/figma-to-design:build https://www.figma.com/design/...`), use that — captured in $ARGUMENTS.

### 1.1b — Dry Run Check
If the user includes "dry run" in their prompt or $ARGUMENTS, complete Phases 1 and 2 but do NOT write any files. Instead, present the plan: which files would be created/modified, which existing components would be reused, and the code structure. Ask the user to confirm before proceeding to write files and run the verification loop.

### 1.2 — Standard Intake Questions

Always ask the following questions in a single message. If the user already answered any of these in their prompt or $ARGUMENTS, pre-fill those and only ask the remaining ones.

**Intake history:** Before asking, check if `.claude/design-tokens/intake-history.json` exists. If it does, read it. For each question below, if there is a previous answer on record, show it as a selectable option labeled **"Last used: [previous answer]"** alongside the standard choices. The user must explicitly select it — never auto-apply previous answers. Always also show the standard options so the user can pick something different.

**Ask all of these every time:**

1. **What is this?** — Page, section, or component?
2. **Where should it live?** — File path (e.g., `app/dashboard/page.tsx`) or general area (e.g., "dashboard route")
3. **Functional or visual-only?**
   - **Fully functional**: Real interactivity, state management, working forms, navigation, etc.
   - **Visual only**: Placeholder data, no real logic, just matches the design visually
4. **Viewports?** — Desktop only, or multiple (desktop/tablet/mobile)? If multiple, share the Figma URL for each.
5. **Components to reuse?** — Name specific existing components, or say "use what makes sense"
6. **Does this design connect to any APIs?**
   - **No** — Static content, no API calls needed
   - **Yes** — If yes, ask the follow-up questions:
     - **How many API calls does this page/component need?** (e.g., 1, 2, 3+)
     - **For each API call**, ask the user to provide:
       - A name/description (e.g., "fetch user profile", "get notifications list", "load activity feed")
       - A sample response JSON or endpoint schema (optional but strongly recommended)
     - Present this as a numbered list the user can fill in. Example:
       > "Please describe each API call this design needs:
       > 1. **Call 1**: Name/description + sample response JSON
       > 2. **Call 2**: Name/description + sample response JSON
       > 3. *(add more as needed)*"

Wait for answers before proceeding. Do not assume defaults for any unanswered question.

**After receiving answers:** Save the answers to `.claude/design-tokens/intake-history.json` for future reference. Structure:

```json
{
  "last_build": {
    "timestamp": "<ISO 8601>",
    "what": "<page | section | component>",
    "where": "<file path>",
    "mode": "<functional | visual-only>",
    "viewports": "<desktop-only | multiple>",
    "components_to_reuse": "<user's answer>",
    "has_api_calls": "<yes | no>"
  }
}
```

### 1.4 — Load Design Context
1. **Figma design context** — Use Figma MCP to pull design context and implementation details from the provided URL(s). Get layout, spacing, colors, typography, and component structure.
2. **Figma screenshot(s)** — Use Figma MCP to get a screenshot of each viewport. **CRITICAL: Hold these screenshots in context for the entire session. You need them for every comparison round. Do not discard them.**
3. **Target file context** — If slotting into an existing file, read it first. If it's a new file, read neighboring files to understand patterns (imports, layout conventions, naming).

### 1.4b — Auto-Suggest Reusable Components

After loading the Figma design context, match the design against the `components` section of `design-tokens.json` using **keyword-based matching only** (no visual similarity matching):

1. Scan the Figma design context text for these exact element keywords: `button`, `input`, `select`, `textarea`, `card`, `avatar`, `badge`, `table`, `nav`, `tab`, `modal`, `dialog`, `tooltip`, `popover`, `alert`, `toast`, `sidebar`, `header`, `footer`, `breadcrumb`, `pagination`, `toggle`, `checkbox`, `radio`, `dropdown`, `menu`, `list`, `grid`, `form`, `search`, `icon`.
2. For each keyword found in the Figma context, check if a component with that word (case-insensitive) in its `name` exists in the `components` array of `design-tokens.json`.
3. If a match is found, add it to the suggestions list.
4. Sort suggestions alphabetically by component name.

**Present suggestions to the user before proceeding:**

> "Based on the Figma design, I recommend reusing these existing components:
> - **Button** (`src/components/ui/Button.tsx`) — matched keyword: `button`
> - **Card** (`src/components/ui/Card.tsx`) — matched keyword: `card`
> - **Avatar** (`src/components/ui/Avatar.tsx`) — matched keyword: `avatar`
>
> Does this look right? Any additions or changes?"

Wait for confirmation. If the user already specified components in question 5, merge your suggestions with their list (deduplicate by component name) and confirm the combined set.

### 1.5 — Library Check

After loading the Figma design context, identify what the design requires (e.g., charts, maps, date pickers, carousels, rich text editors, drag-and-drop, animations, icons, etc.).

**Step 1: Check installed packages.**
Read `package.json` dependencies and devDependencies. For each capability the design needs, check if a relevant library is already installed.

Examples:
- Charts → `recharts`, `chart.js`, `@nivo/*`, `victory`, `d3`
- Maps → `react-map-gl`, `@react-google-maps/api`, `leaflet`
- Date pickers → `react-datepicker`, `@mui/x-date-pickers`, `react-day-picker`
- Carousels → `swiper`, `embla-carousel-react`, `keen-slider`
- Animations → `framer-motion`, `react-spring`, `@react-spring/web`
- Icons → `lucide-react`, `react-icons`, `@heroicons/react`
- Tables → `@tanstack/react-table`, `ag-grid-react`

**Step 2: Check `preferred_libraries` first.** If the capability category exists in `preferred_libraries`, use the `selected` library. No question needed — the user already chose during init.

**Step 3: If the category does NOT exist in `preferred_libraries`** (the design needs something that was not detected during init), check `package.json` to see if any relevant library is already installed.

**If a library is installed → use it.** Never rebuild from scratch what a project dependency already provides. If multiple are installed, ask the user which to prefer (same format as init Step 5e).

**Step 4: If no matching library is installed**, present the user with 2-3 options and a recommendation:

> "The design includes [charts/maps/etc.] but no library is installed for this. Here are the options:
> 1. **[Library A]** — [one-line why]. **(Recommended)**
> 2. **[Library B]** — [one-line why].
> 3. **Build from scratch** — Only if the requirement is simple enough.
>
> Which would you like?"

Always recommend the option that best fits the project's existing stack and complexity. Wait for the user's choice before proceeding. Install the chosen library before generating code. **After the user chooses, update `preferred_libraries` in `.claude/design-tokens/design-tokens.json`** with the new category and selection so future builds don't ask again.

---

## Phase 2: Generate Code

### Code Principles — Follow All of These

**Reusability:**
- Before creating ANY new component, check `design-tokens.json` → `components`. If an existing component can do the job, USE IT.
- If a pattern appears 2+ times in the design (same HTML structure + same visual styling = repeated pattern; different text content does not make it different), extract it into a new reusable component.
- New components must be props-driven and composable. No hardcoded content — pass it through props.
- Place new reusable components in the project's existing component directory structure.

**SOLID for Frontend:**
- **Single Responsibility**: One component = one job. A `PricingCard` renders a pricing card. It does not fetch data.
- **Open/Closed**: Components are extendable via props (`variant`, `size`, `className`) without modifying source.
- **Liskov Substitution**: Specialized versions of components are drop-in replacements for the base.
- **Interface Segregation**: Don't bloat props. If a component needs wildly different data for different uses, split it.
- **Dependency Inversion**: Components depend on props and hooks, not direct imports of API clients or stores.

**DRY for Frontend:**
- All colors, spacing, font sizes, shadows, radii come from `design-tokens.json`. NEVER hardcode values like `#3B82F6` or `padding: 24px`.
- Use the project's styling approach (from `design-tokens.json` → `styling_approach`). If Tailwind, use Tailwind classes. If CSS modules, use CSS modules. Match what exists.
- Shared logic goes in hooks. Shared layout goes in layout components. No copy-paste.
- One source of truth for all design tokens.

**File Structure:**
- **File placement rules (deterministic):**
  - **New reusable components:** Place in the same directory as the existing component most similar in type (matched by keyword from the auto-suggest list). If no similar component exists, use the first directory that exists from this priority list: `src/components/ui/`, `src/components/shared/`, `src/components/common/`, `src/components/`, `components/ui/`, `components/`.
  - **Page-specific components:** Place in the route directory's `components/` subfolder (e.g., `app/dashboard/components/`). If no such subfolder exists, create it.
  - **New hooks:** Place in the same directory as existing hooks. If no hooks directory exists, use `src/hooks/` or `hooks/`.
  - **API functions/services:** Place in the same directory as existing API files (from `api.config_path` in tokens). If none exists, use `src/services/` or `src/lib/api/`.
- **Strict one-component-per-file rule**: Each component gets its own file. The only exception is a sub-component that is 15 lines or fewer — it may stay in the parent file. Anything over 15 lines must be extracted to a separate file, imported, and used.
- Export with proper TypeScript types for all props.

### Generation Rules

1. Write code for the primary viewport first (typically desktop).
2. Add responsive behavior for other viewports using the project's breakpoint system from `design-tokens.json`.
3. Use semantic HTML (`nav`, `main`, `section`, `article`, `aside`, `header`, `footer`, `button`) — not div soup.
4. Include accessibility: proper heading hierarchy, alt text, button labels, focus management, aria attributes where needed.
5. For images, use placeholder `src` values with a comment noting which Figma asset it corresponds to.
6. **`"use client"` rule:** Add `"use client"` if and only if the component uses any of: `useState`, `useEffect`, `useReducer`, `useRef` with DOM interaction, `useContext`, event handlers (`onClick`, `onChange`, `onSubmit`, `onKeyDown`, etc.), browser APIs (`window`, `document`, `localStorage`, `sessionStorage`), or third-party hooks that require client context. If none of these are present, do NOT add it.
7. Focus on the default/resting visual state. Do not implement hover, focus, active, or animation states unless the user explicitly requests them or the Figma design includes them as separate frames.
8. **Tailwind class selection rule (if Tailwind):** Always use the shortest Tailwind class that achieves the exact value. Prefer scale classes (`p-4`) over arbitrary values (`p-[16px]`). For values not in the Tailwind scale, use arbitrary values. Never use longhand (`px-4 py-4`) when shorthand (`p-4`) achieves the same result. For colors, always use the semantic token class (`bg-primary`) over the raw color class (`bg-blue-500`) if a semantic token exists.

### API Integration Rules

If the user selected "Yes" for API connections in question 6 and `preferred_libraries.data_fetching` exists in `design-tokens.json`, follow these rules:

1. **Use the selected data fetching library.** Check `preferred_libraries.data_fetching.selected`. If it's `@tanstack/react-query`, generate `useQuery`/`useMutation` hooks. If `swr`, use `useSWR`. If `axios`, use the project's axios instance. If `fetch (built-in)`, use fetch with the project's wrapper if one exists. Never use a different fetching library than what's selected.

2. **Match the project's API file structure.** If the project has API calls in `services/`, `api/`, or `lib/`, put new API calls in the same location following the same naming convention.

3. **Generate typed API functions for each call the user described.**
   - If the user provided a sample response JSON, generate TypeScript interfaces/types from it.
   - If no sample was provided, generate reasonable types based on the design's data needs with `// TODO: Replace with actual API response type` comments.
   - Name the types descriptively (e.g., `UserProfileResponse`, `NotificationItem`, `ActivityFeedEntry`).

4. **Wire up components to API calls.**
   - Components should consume data from the API hooks/functions, not hardcoded values.
   - Use the project's established loading state pattern (from `api.loading_pattern` in tokens).
   - Use the project's established error handling pattern (from `api.error_handling` in tokens).
   - The generated code should work end-to-end — when the user plugs in a real API endpoint, the component renders real data without structural changes.

5. **For multiple API calls in a single page/component:**
   - Each API call gets its own hook/function.
   - Handle loading and error states independently per call (unless the project uses a coordinated pattern like React Query's `useQueries`).
   - If calls have dependencies (e.g., call 2 needs data from call 1), chain them appropriately using the project's pattern (e.g., `enabled` option in React Query).

6. **Placeholder endpoints.**
   - Use descriptive placeholder URLs: `/api/user/profile`, `/api/notifications`, etc.
   - Add a comment above each endpoint: `// TODO: Replace with actual endpoint`
   - If `base_url_env` exists in the API config, use it: `${process.env.NEXT_PUBLIC_API_URL}/user/profile`

---

## Phase 3: Visual Verification Loop

After generating the code, run this loop. **Maximum 4 rounds.**

### 3.1 — Take a Screenshot
Use the Playwright CLI (globally installed) via Bash to capture screenshots:

```bash
npx playwright screenshot --viewport-size="1280,800" <dev-server-url> /tmp/figma-to-design-screenshot.png
```

1. Run the command with the dev server URL and the primary viewport width.
2. If multiple viewports, run additional commands at each viewport width (e.g., `--viewport-size="768,1024"` for tablet, `--viewport-size="375,812"` for mobile).
3. Read the resulting screenshot file(s) to load them into context for comparison.

If the dev server isn't running or Playwright can't reach the page:
1. Tell the user to start their dev server and provide the local URL.
2. Wait for confirmation, then retry once.

If Figma MCP returns an error or empty response during Phase 1:
1. Retry the Figma MCP call once.
2. If it fails again, tell the user: "Figma MCP couldn't fetch the design. Check that the URL is a valid Figma Dev Mode link and that Figma MCP is connected." Stop.

Do NOT retry any failing tool more than once. If a tool fails twice, report the error and stop rather than burning tokens on repeated failures.

### 3.2 — Compare

**Step A: Objective pixel-diff score.**

Run a pixel-diff comparison between the Figma screenshot and the Playwright screenshot using the pixelmatch CLI (installed globally during `/figma-to-design-init`).

**Step A.1: Save the Figma screenshot to disk.**

Before running pixel-diff, the Figma screenshot must be saved as a PNG file. Use Figma MCP's `get_screenshot` to get the screenshot, then save it to `/tmp/figma-screenshot.png`. The Playwright screenshot is already at `/tmp/figma-to-design-screenshot.png`.

**Step A.2: Run the pixelmatch CLI.**

```bash
pixelmatch /tmp/figma-screenshot.png /tmp/figma-to-design-screenshot.png /tmp/figma-diff.png 0.1
```

Arguments:
- Image 1: `/tmp/figma-screenshot.png` (Figma)
- Image 2: `/tmp/figma-to-design-screenshot.png` (Playwright)
- Diff output: `/tmp/figma-diff.png` (red pixels = differences)
- Threshold: `0.1` (default sensitivity, range 0-1, lower = more sensitive)

**Step A.3: Read the CLI output.**

The CLI prints output in this format:
```
matched in: 15.123ms
different pixels: 143
error: 0.15%
```

Parse the output:
- `error` = the percentage of pixels that differ. **The match score is `100 - error`**. So `error: 0.15%` means a **99.85% match**.
- `different pixels` = the absolute count of differing pixels.
- The diff image at `/tmp/figma-diff.png` shows exactly which pixels differ (red = different). Read this image to show the user where differences are.

**Step A.4: If the command fails:**
1. If pixelmatch is not found, try installing: `npm install -g pixelmatch`
2. Retry the command once.
3. If it fails again (e.g., images have different dimensions, format issues), warn the user: "Pixel-diff scoring unavailable — falling back to visual-only comparison." Proceed with Step B only.

**Step B: Visual judgment comparison.**

Also compare the screenshots visually. The pixel-diff score is a baseline, but visual judgment catches structural issues that pixel-diff misses (e.g., correct layout with slightly different fonts still looks right).

Evaluate:

- **Layout**: Overall structure, columns, section ordering, alignment
- **Spacing**: Gaps, padding, margins between elements
- **Typography**: Font sizes, weights, line heights, hierarchy
- **Colors**: Backgrounds, text colors, borders, accents
- **Components**: Correct components used, correct appearance
- **Responsive**: Each viewport matches its respective Figma frame (if applicable)

**Step C: Scoring rules and reporting.**

- **If pixel-diff is available:** Use the pixel-diff `matchPercent` as the sole gating score for the decide step (3.3). Visual judgment is used ONLY to identify WHAT is wrong and prioritize fixes — it does NOT affect the score.
- **If pixel-diff is unavailable** (install failed): Use visual judgment as the gating score. Explicitly warn the user: "Pixel-diff is unavailable — scoring is approximate and based on visual judgment."

**Always display the score to the user after each comparison round:**

> **Round X comparison:**
> - Pixel-diff score: **99.85% match** (error: 0.15%, 143 different pixels)
> - Diff image: `/tmp/figma-diff.png`
> - Visual issues identified: [list specific issues from Step B]

If pixel-diff is unavailable, show:

> **Round X comparison (visual-only — pixelmatch not available):**
> - Visual score: **~85%** (approximate)
> - Issues identified: [list specific issues]

### 3.3 — Analyze Diff Image and Identify Fixes

**When pixel-diff is available**, read the diff image (`/tmp/figma-diff.png`) to pinpoint exactly where differences are. The diff image shows red/magenta pixels where the two screenshots differ and transparent/dark pixels where they match.

**Step 3.3a: Read the diff image and map red regions to components.**

1. Read `/tmp/figma-diff.png` to see which areas of the page have red pixels.
2. Divide the page into logical regions based on the component structure you generated:
   - **Top region** → header/navbar
   - **Upper-middle** → hero section or page title area
   - **Middle** → main content area (cards, forms, tables, etc.)
   - **Lower-middle** → secondary content
   - **Bottom** → footer
   - **Left/Right edges** → sidebars, margins
3. For each region with visible red pixels, identify which specific component/element in your generated code corresponds to that region.
4. Categorize each red region by issue type:
   - **Large red block** (solid rectangle of red) → wrong background color, missing section, or completely wrong layout
   - **Red outline/border around an element** → wrong spacing, padding, margin, or border
   - **Scattered red pixels in text areas** → wrong font size, weight, line-height, or font family
   - **Thin red lines/strips** → off-by-a-few-pixels alignment or spacing
   - **Red in image/icon areas** → missing or wrong-sized image placeholder

**Step 3.3b: Create a fix list ordered by red pixel density.**

For each identified issue, estimate how many red pixels it accounts for. Fix the issues with the most red pixels first — this maximizes the score improvement per fix.

Example fix list:
> 1. **Header background** (top 80px) — large red block → background color is `bg-white` but should be `bg-surface` → ~5,000 red pixels
> 2. **Card spacing** (middle section) — red outlines around cards → gap is `gap-4` but should be `gap-6` → ~2,000 red pixels
> 3. **Body text** (scattered red in paragraphs) → font size is `text-sm` but should be `text-base` → ~1,500 red pixels

### 3.4 — Decide and Fix

Use the gating score from Step C (pixel-diff `100 - error%` if available, otherwise visual judgment):

- **Below 95%**: Apply the fixes identified in Step 3.3b, starting with the highest red-pixel-density issues. Make targeted edits — do NOT rewrite entire components. After applying fixes, go back to 3.1 to take a new screenshot and re-run pixelmatch. Do not ask the user. Continue this loop automatically until either:
  - The pixel-diff score reaches **95% or above**, OR
  - **Round 4** is reached

- **95% or above**: Stop. Show the user:
  - The current Playwright screenshot(s)
  - The pixel-diff score (e.g., "Pixel-diff: **96.2% match** (error: 3.8%, 3,891 different pixels)")
  - The diff image path `/tmp/figma-diff.png`
  - Any remaining visible differences
  - Summary of all fixes applied across rounds

- **Round 4 reached regardless of score**: Stop. Show the user the current state, pixel-diff score, the diff image, and remaining issues. List the specific red regions that still differ and explain what would need manual adjustment.

### 3.5 — Fix Priority Order

When multiple issues have similar red pixel density, prioritize in this order:
1. Structural/layout issues (wrong grid, missing sections, incorrect ordering) — these cause the most red pixels
2. Color mismatches (wrong backgrounds, text colors) — large solid blocks of red
3. Spacing issues (wrong gaps, padding, margins) — red outlines and strips
4. Typography mismatches (font size, weight, line-height) — scattered red in text
5. Border radius, shadow, and decorative differences — small red areas
6. Fine-grained alignment and sub-pixel polish — minimal red pixels

---

## Phase 4: Finalize

After the loop ends:

1. Ensure all new components are properly exported and TypeScript types are correct.
2. Summarize what was built:
   - Files created or modified (with paths)
   - New reusable components introduced
   - Existing components reused from the project
   - **Score progression across rounds** (e.g., "Round 1: 72.3% → Round 2: 88.1% → Round 3: 95.4%")
   - **Fixes applied per round** (e.g., "Round 1: fixed header bg color, card spacing. Round 2: fixed font sizes, button padding.")
   - Final match score
   - Any remaining known differences from the Figma (with diff image reference)
3. **Auto-update design tokens if needed.** If new reusable components, hooks, or API patterns were created during this build:
   - Read the current `.claude/design-tokens/design-tokens.json`
   - Add new components to the `components` array (with name, path, description, props)
   - Add new hooks to the `hooks` array (with name, path, description)
   - Update the `api` section if new API patterns were introduced
   - Write the updated file back
   - Tell the user: **"Updated `.claude/design-tokens/design-tokens.json` with X new components / Y new hooks."** List what was added so they can verify.

---

## Critical Reminders

- **Never lose the Figma screenshots from context.** You need them for every comparison round.
- **Always read `.claude/design-tokens/design-tokens.json` before generating code.** Non-negotiable.
- **Reuse over recreate.** Check existing components first. Always.
- **Targeted fixes, not rewrites.** Each iteration changes as little as possible.
- **Match the project's conventions.** Styling approach, file structure, naming patterns — match what's already there.