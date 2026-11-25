---
name: ui-init
description: One-time setup for the UI/UX skill set. Detects what's already in place, installs missing dependencies (Playwright, axe-core), identifies the token home, checks for a design brief, and writes a ## UI skills section to CLAUDE.md/AGENTS.md so every skill knows the project's setup. Run this before using /uiux, /animate, /copy, /a11y, /tokens, /landing, or /design-grill for the first time on a new project.
disable-model-invocation: true
---

# /ui-init — UI Skill Set Setup

Scaffolds everything the UI/UX skills assume is in place. Explore first, present findings, confirm with the user, then write. Never guess — always check before installing or creating.

---

## Process

### 1. Explore

Read the current state of the repo. Don't assume anything — check each one:

```bash
# Framework detection
cat package.json | grep -E '"next"|"vite"|"nuxt"|"astro"|"svelte"' 2>/dev/null | head -5

# Playwright installed?
node -e "require('@playwright/test')" 2>/dev/null && echo "playwright: yes" || echo "playwright: no"
find . -name "playwright.config.*" -not -path "*/node_modules/*" 2>/dev/null | head -3
# If a playwright.config exists, check for custom outputDir or use option that might conflict with /tmp writes
grep -h "outputDir\|use:" playwright.config.* 2>/dev/null | head -5

# axe-core installed?
find . -path "*/axe-core/package.json" -not -path "*/node_modules/.cache/*" 2>/dev/null | head -1 \
  && echo "axe-core: yes" || echo "axe-core: no"

# i18n library detection (affects /copy — edits go to message files, not components)
grep -r "i18next\|next-intl\|react-i18next\|@lingui\|formatjs\|next-translate" \
  package.json packages/*/package.json apps/*/package.json 2>/dev/null | head -3

# Token home — where design values live
find . \( -name "globals.css" -o -name "variables.css" -o -name "tokens.css" \) \
  -not -path "*/node_modules/*" 2>/dev/null
find . -name "tailwind.config.*" -not -path "*/node_modules/*" 2>/dev/null
find . -name "tokens.json" -o -name "design-tokens.json" 2>/dev/null | grep -v node_modules

# Design brief
ls DESIGN-BRIEF.md 2>/dev/null && echo "brief: yes" || echo "brief: no"

# CLAUDE.md / AGENTS.md
ls CLAUDE.md AGENTS.md 2>/dev/null
grep -n "UI skills\|ui skills\|design-grill\|/uiux" CLAUDE.md AGENTS.md 2>/dev/null | head -5

# prefers-reduced-motion in global CSS (needed by /animate and /a11y)
grep -rn "prefers-reduced-motion" . --include="*.css" -l 2>/dev/null | grep -v node_modules

# Skip link in root layout (needed by /a11y)
grep -rn "skip.*main\|Skip.*content\|#main-content" . --include="*.tsx" --include="*.html" 2>/dev/null \
  | grep -v node_modules | head -3

# Source root
find . -type d -name "src" -not -path "*/node_modules/*" -not -path "*/.next/*" \
  -not -path "*/dist/*" -not -path "*/.turbo/*" 2>/dev/null | head -1
```

### 2. Present findings

Summarise exactly what's present and what's missing. Use this table format:

```
Playwright             ✓ installed / ✗ missing
Chromium browser       ✓ installed / ✗ missing / ? unknown
Playwright baseURL     ✓ localhost:3000 / ⚠ custom port [n] — note for skills
axe-core               ✓ installed / ✗ missing
Token home             ✓ globals.css :root / ✓ tailwind.config / ✗ none
i18n library           ✓ [library name] — /copy edits message files / ✗ none
Design brief           ✓ DESIGN-BRIEF.md found / ✗ none
CLAUDE.md/AGENTS.md    ✓ exists / ✗ neither exists
UI skills section      ✓ already set up / ✗ missing
prefers-reduced-motion ✓ in globals.css / ✗ missing
Skip link              ✓ found / ✗ missing
```

Tell the user: "I'll walk you through setting up each missing piece. For already-present items I'll verify they're correct and skip anything that doesn't need changing."

### 3. Walk through each decision (one at a time)

---

#### Section A — Playwright

> **What it is:** Playwright is the browser automation tool all the visual skills use to take screenshots, record animations, and run accessibility scans. Every skill that verifies changes visually needs it.
> **Which skills need it:** /uiux, /animate, /copy, /a11y, /landing, /tokens

**If already installed:** verify Chromium browser is available:
```bash
npx playwright install chromium --dry-run 2>/dev/null && echo "chromium: ok" || echo "chromium: needs install"
```
If Chromium is missing, install it: `npx playwright install chromium`

Also check whether an existing `playwright.config.*` could conflict with how skill scripts write to `/tmp`:
- Skills write screenshots and videos directly to `/tmp/` using absolute paths — they bypass any `outputDir` in the config entirely.
- **Conflict to watch for:** if the config sets `use: { baseURL: ... }` pointing to a port other than 3000, note it — skill scripts all default to `http://localhost:3000`. Record the actual port in the CLAUDE.md block if it differs.
- If `playwright.config` restricts which browsers are installed (e.g. only `firefox`), Chromium may still need a separate install. The skills always use `chromium` — verify it's available regardless of the config.

**If not installed:**

> "Playwright isn't installed. It's a dev dependency used only during skill runs — it won't affect your production bundle. Should I install it?"

Default: yes. Install:
```bash
pnpm add -D @playwright/test 2>/dev/null || npm install -D @playwright/test
npx playwright install chromium
```

---

#### Section B — axe-core

> **What it is:** axe-core is the accessibility scanning engine /a11y uses to programmatically detect WCAG violations.
> **Which skills need it:** /a11y only

**If already installed:** skip.

**If not installed:**

> "axe-core isn't installed. It's a dev dependency used only by /a11y for programmatic accessibility scanning. Should I install it?"

Default: yes.
```bash
pnpm add -D axe-core 2>/dev/null || npm install -D axe-core
```

---

#### Section C — Token home

> **What it is:** The file where design tokens (colors, spacing, typography) live. /tokens reads and writes here. /uiux applies fixes here for global changes.
> **Which skills need it:** /tokens, /uiux

**If a token home exists** (globals.css with `:root`, tailwind.config, or tokens.json): note the location and confirm it with the user. No action needed.

**If no token home exists:**

> "No design token file was found. Tokens need a home — usually a `:root` block in globals.css or a `theme.extend` in tailwind.config.ts. Which do you prefer?"

Options:
- **CSS custom properties in globals.css** — works with any framework, most flexible (recommended for new projects)
- **Tailwind config** — works if you're already using Tailwind
- **I'll set it up myself** — skip, just note the location

If globals.css exists but has no `:root` block: offer to add a minimal starter block:
```css
/* Design tokens */
:root {
  /* Add your tokens here — /tokens will help you fill this in */
}
```

---

#### Section D — prefers-reduced-motion

> **What it is:** A CSS media query that suppresses animations for users who've requested reduced motion in their OS settings. Required for WCAG 2.1 AA compliance.
> **Which skills need it:** /animate (adds it), /a11y (checks for it)

**If already present:** skip.

**If missing:**

First, identify the correct global CSS file to write to. In a monorepo there may be multiple — pick the one that is imported by the root layout or `_app.tsx`, not a component-scoped one:

```bash
# Find all global CSS files
find . \( -name "globals.css" -o -name "global.css" -o -name "index.css" \) \
  -not -path "*/node_modules/*" -not -path "*/.next/*" 2>/dev/null

# Which one is imported in the root layout or app entry?
grep -rn "globals.css\|global.css\|index.css" . \
  --include="*.tsx" --include="*.ts" --include="*.js" \
  -not -path "*/node_modules/*" | grep "import\|require" | head -5
```

Use the file imported at the root — not the first globals.css found. If multiple root-level imports exist, show them to the user and ask which one is the true global entry.

> "The `prefers-reduced-motion` rule isn't in your global CSS. It's a WCAG requirement that makes all animations respect the user's OS motion preference. I'll add it to `[confirmed file path]`."

No further confirmation needed — add to the end of the identified file:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

---

#### Section E — Design brief

> **What it is:** DESIGN-BRIEF.md is a project-root file that captures visual direction — brand personality, color system, typography, animation level, component style. All UI skills read it before starting so they don't have to re-derive what's already been decided.
> **Which skills need it:** /uiux, /animate, /tokens, /landing (all read it if present)

**If already exists:** read it, summarise it in two sentences, confirm it's current.

**If missing:**

> "No DESIGN-BRIEF.md found. Without it, each skill run starts from scratch on visual direction. You have two options:
> 1. **Run /design-grill now** — 12-question interview that produces the brief (recommended before any UI work)
> 2. **Skip for now** — skills will ask about visual direction inline when needed"

If user chooses option 1: stop here and instruct them to invoke `/design-grill`. After the brief is written, re-run `/ui-init` to complete setup.
If user chooses option 2: note it in the CLAUDE.md section.

---

#### Section F — CLAUDE.md / AGENTS.md update

Pick the file to edit:
- If `CLAUDE.md` exists → edit it
- Else if `AGENTS.md` exists → edit it
- If neither exists → ask which to create. Don't pick for them.

If a `## UI skills` section already exists: update it in-place. Don't append a duplicate.

Add this block (adjust based on what was found/installed):

```markdown
## UI skills

### Visual verification
Playwright is installed for screenshot and animation verification. Chromium browser is available.
Dev server runs on `http://localhost:[PORT]` — all skill scripts default to this URL.
Run `npx playwright install chromium` if screenshots fail.

### Accessibility scanning
axe-core is installed. /a11y uses it for programmatic WCAG 2.1 AA scanning.

### Token home
Design tokens live in `[path to token file]`. /tokens reads and writes here.
[If none: "No token home configured — /tokens will ask at setup time."]

### Internationalisation
[If i18n detected: "/copy detected [library name]. All copy edits go into message files under `[path]`, not hardcoded into component files."]
[If none: "No i18n library detected. /copy edits strings directly in component files."]

### Design brief
[If DESIGN-BRIEF.md exists: "Visual direction is documented in `DESIGN-BRIEF.md`. All UI skills read this before starting."]
[If none: "No design brief yet. Run /design-grill before /uiux or /tokens to establish visual direction."]

### Skills available
| Skill | When to use |
|-------|------------|
| /design-grill | Before any UI work — establishes visual direction and writes DESIGN-BRIEF.md |
| /uiux | Redesign any screen — pixel-perfect, recursive |
| /uicolor | Color correction master — balance, temperature, shadows, hierarchy, 60-30-10 |
| /animate | Add or fix animations and micro-interactions |
| /copy | Audit and rewrite all user-facing strings |
| /a11y | Fix accessibility violations — WCAG 2.1 AA |
| /tokens | Find hardcoded design values and replace with tokens |
| /landing | Optimise a marketing or product landing page for conversion |
```

### 4. Done

Tell the user what was set up and what was skipped. Recommend the next step:

- If no design brief: "Run `/design-grill` next to establish visual direction before any skill touches the UI."
- If brief exists but no token system: "Run `/tokens` next to build the token system from the existing colors."
- If everything is in place: "Setup is complete. You can now run any UI skill. Recommended order for a new project: `/design-grill` → `/tokens` → `/uiux` → `/uicolor` → `/animate` → `/copy` → `/a11y`."

---

## Rules

1. **Explore before acting.** Never install or create files without checking first.
2. **Edit the existing file, don't create a duplicate.** If `CLAUDE.md` exists, edit it. If `## UI skills` already exists, update it in-place.
3. **Only install dev dependencies.** Playwright and axe-core are `devDependencies` — never `dependencies`.
4. **Skip what's already correct.** Don't reinstall a working Playwright setup.
5. **Never create `AGENTS.md` if `CLAUDE.md` exists** (or vice versa).
6. **The `prefers-reduced-motion` rule is always added** without asking — it's a WCAG requirement, not a preference.
7. **Don't run /design-grill yourself** — instruct the user to invoke it. It's a full interactive session that belongs in its own turn.
