---
name: port-component
description: Ports a UI component from the gaia mono repo (theexperiencecompany/gaia) into the gaia-ui registry. Use when asked to port, copy, migrate, or bring over a component from gaia, the mono repo, or the main repo into gaia-ui. The user may give a component name ("port weather-card"), a file path in the gaia repo, or a screenshot of UI from heygaia.io to identify the component. Pulls from the master branch by default unless a specific branch or ref is given.
---

# Port Component from Gaia Mono Repo

Copies a component from the gaia mono repo into this repo (gaia-ui), makes it a reusable open-source component, and wires up registry, preview, and docs.

- Source repo: `~/work/gaia` (override with `GAIA_REPO` env var). Remote: `https://github.com/theexperiencecompany/gaia`
- Default ref: `origin/master`. Use another branch or ref only if the user asks.
- Destination: `registry/new-york/ui/` in this repo.

Never check out branches in the gaia repo. Read files with `git show <ref>:<path>` so the user's working tree there stays untouched.

## Accepting the request

The user identifies the component in one of three ways:

1. **Component name** ("port the footer"). Run the finder script (step 1 below).
2. **File path** ("apps/web/src/components/navigation/Footer.tsx"). Read it directly with `git show`.
3. **Screenshot** of UI from heygaia.io. Look at the image, identify what the component is (footer, navbar, pricing section, chat bubble, etc.), then search for it by that name and by distinctive strings visible in the screenshot (`git grep -i "Request a Feature" origin/master -- apps/web`).

If it is still ambiguous after searching, show the user the candidate paths and ask.

## Where to look in the gaia repo

Only search frontend code. Never search backend, infra, or tooling.

Search these paths, in this order:

| Path | What lives there |
|---|---|
| `apps/web/src/components/` | Shared web components (`ui/`, `navigation/`, `layout/`, `shared/`, `seo/`) |
| `apps/web/src/features/<feature>/components/` | Feature components (chat, landing, pricing, mail, calendar, settings, onboarding, ...) |
| `apps/web/src/config/` | App config the components import (`appConfig.tsx` has `footerSections`, `connect`, nav links) |
| `apps/web/src/lib/`, `apps/web/src/hooks/` | Helpers and hooks components may depend on |
| `apps/web/src/stores/` | Zustand stores (strip these when porting, replace with props) |

Do NOT look in: `apps/api` (Python backend), `apps/bots`, `apps/bridge`, `apps/voice-agent`, `infra`, `tools`, `scripts`, `packages/cli`, `docs`, `openspec`. `apps/mobile` and `apps/desktop` only if the user explicitly asks for a mobile or desktop component.

## Workflow

### 1. Locate the source

```bash
.agents/skills/port-component/scripts/find-component.sh <component-name> [ref]
```

The script fetches origin, searches file names and exported symbols on the ref, and prints matching paths. Read files without checkout:

```bash
git -C ~/work/gaia show 'origin/master:apps/web/src/components/navigation/Footer.tsx'
```

Also read every local import of the component (relative imports, config, hooks, feature utils). Each one must be ported, inlined, or replaced with a prop.

### 2. Check for an existing version

Look in `registry/new-york/ui/` and `registry.json`. If the component already exists, ask before overwriting.

### 3. Make it reusable

Most mono repo components are coupled to the app. They must ship as clean open-source components anyone can drop into their project. Apply these rules:

- **Config imports become props.** `footerSections` from `appConfig` becomes a `sections` prop. Never hardcode GAIA links, URLs, or copy in the component; demo data belongs in the preview.
- **App-specific chunks become slots.** A status iframe, company logo, or analytics widget becomes a `ReactNode` prop (`startSlot`, `brandSlot`) or is dropped.
- **Strip mono repo concerns.** SEO/JsonLd, analytics (PostHog), i18n hooks, feature flags, Zustand stores. Replace with props or sensible defaults.
- **Drop hard asset dependencies.** If the source loads a wallpaper or logo from `/public`, make it an optional prop with a CSS fallback so the component works with zero assets.
- **Minimize npm deps.** Prefer `matchMedia` over pulling in `motion` just for `useReducedMotion`. Every dependency listed in `registry.json` gets installed in the consumer's project.
- **HeroUI never survives the port.** Map to shadcn primitives (`@/components/ui/*`) or Radix patterns.
- **Rewrite import paths.** `cn` from `@/lib/utils`, icons from `@/components/icons` (Hugeicons), sibling registry components from `@/registry/new-york/ui/<name>`.

### 4. Follow gaia-ui conventions

- **One component per file.** Never stack multiple components in one file. Multi-part components split into sibling files (`footer.tsx`, `footer-wordmark.tsx`) that all get listed in the `registry.json` files array. Look at `weather-card` for the pattern.
- File names are kebab-case. Normalize whatever casing the user gives.
- Tabs for indentation (biome). Match the existing code style exactly.
- Exported, documented props interface per component. `className` pass-through merged with `cn()`.
- A11y: keyboard focus styles, ARIA labels, `aria-hidden` on decorative elements, `prefers-reduced-motion`, semantic elements (`nav`, `footer`, `button`).
- Theme-aware CSS variables where the design allows; a deliberately dark component (glow footer) may keep its palette but must say so in its docs.
- No em dashes anywhere: not in code comments, not in docs, not in descriptions. Use commas, colons, or parentheses.

### 5. Register and build

Add an entry to `registry.json` items. Edit the file directly and match the existing tab formatting exactly (never round-trip the whole file through a formatter or script). Include `dependencies` only for npm packages the component actually imports, `registryDependencies` for gaia-ui components it uses, and every file in `files`.

Then build the registry artifact and commit it with the rest:

```bash
pnpm registry:build     # shadcn build, generates public/r/<name>.json
```

Only commit the `public/r/<name>.json` you added plus the footer entry in `public/r/registry.json`. If the local shadcn version reformats every other `public/r/*.json`, revert those unrelated files and match the existing format in yours (for example the top-level `"type": "registry:ui"` field).

### 6. Preview

Create `components/previews/<name>/default.tsx` with realistic demo data (this is where GAIA-branded content is fine). Add variant previews only if the component has real variants. Previews auto-register by path; no index to update.

**Port the brand assets too, not just the code.** The preview must look like the component does on the GAIA landing page, and the code alone rarely gets you there. Before writing the preview, hunt down every asset the original render depends on and bring the real one over:

- **Images and wallpapers.** If the original references anything under `apps/web/public` (wallpapers, logos, textures), copy the exact file into gaia-ui's `public/` at a matching path (`git show origin/master:apps/web/public/<path> > public/<path>`) and use it in the preview (for example `backgroundSrc`). Never substitute a CSS-gradient approximation when the original uses an image; a hand-tuned gradient will not match.
- **Fonts.** Resolve what the original's font utility actually maps to (check `--font-*` variables in `apps/web/src/app/styles/globals.css` and `apps/web/src/app/fonts/`); gaia's `font-serif` is Aeonik, not a serif. If gaia-ui does not load that face, copy the woff2 into `app/fonts/`, register it with `next/font/local` (see `app/fonts/aeonik.ts`), and pass it to the preview. The component itself stays font-agnostic via a `fontClassName`-style prop.
- **Colors.** Trace hardcoded colors back to what actually paints on screen (a wallpaper's pixels, a brand token), and expose them as props with the real value as the default.

Then compare your rendered preview against the live landing page (or a recording of it) side by side before calling the port done. If it does not read as the same thing, an asset is still missing.

### 7. Docs

Create `content/docs/components/<name>.mdx`. Copy the structure of an existing doc (`pricing-card.mdx` is the reference) and keep it tight:

- Frontmatter: `category`, `title`, `description`. The `category` places it in the sidebar; pick from the list in `lib/navigation.ts` (`CATEGORY_ORDER`).
- Sections in order: intro line, `<ComponentPreview name="<name>/default" />`, "Usage in Gaia" (one or two lines), Installation (`package-install` block with the `https://ui.heygaia.io/r/<name>` URL), Usage (one minimal example), Examples (only meaningfully different ones), Props table per exported component, short Notes if there are real caveats.
- No filler prose, no marketing fluff, no walls of examples.

The sidebar is generated from docs frontmatter, so a correct `category` is all that is needed; only touch `lib/navigation.ts` for a brand new category.

### 8. Verify, then it is done

Run all of these and fix failures:

```bash
pnpm type                 # tsc --noEmit
pnpm lint                 # biome check
```

Then confirm:

- `public/r/<name>.json` exists after the registry build and contains all files.
- The component appears in the docs sidebar: start `pnpm dev`, or verify the mdx frontmatter category matches `CATEGORY_ORDER` in `lib/navigation.ts`.
- The preview renders: hit `/docs/components/<name>` in the dev server and check the browser for runtime errors, or at minimum confirm the preview imports resolve in `pnpm type`.
- Take a screenshot of the rendered component (used in the PR, step 9). With the dev server on a port, capture the demo element with playwright and the system chromium:

```js
// run from a repo that has playwright installed (~/work/gaia works)
import { chromium } from "playwright";
const b = await chromium.launch({ executablePath: "/usr/bin/chromium" });
const page = await b.newPage({ viewport: { width: 1440, height: 1000 }, colorScheme: "dark" });
await page.goto("http://localhost:<port>/docs/components/<name>", { waitUntil: "networkidle" });
await page.waitForTimeout(3000); // let canvases/animations draw
await page.locator("main <demo-selector>").first().screenshot({ path: "/tmp/<name>.png" });
await b.close();
```

  Eyeball the screenshot before using it: wrong logo, broken layout, or empty canvas means something is off.
- Run through the AGENTS.md checklist (dark mode, keyboard, ARIA, reduced motion, exported types).

### 9. Ship

Unless the user says otherwise: branch (`sanku/<name>-component`), commit, push, and open a PR on gaia-ui with `gh pr create`, summarizing what was ported, from where (source path and ref), and what was changed to make it reusable.

Include the screenshot in the PR description. Push it to the `pr-assets` branch and reference the raw URL:

```bash
git checkout pr-assets 2>/dev/null || git checkout --orphan pr-assets
# copy image in, commit only the image, push, then switch back
```

Then embed: `![<name> component](https://raw.githubusercontent.com/theexperiencecompany/gaia-ui/pr-assets/<name>.png)`

If `gh` hangs through the mise shim, call the real binary at `~/.local/share/mise/installs/gh/<version>/gh_*/bin/gh`.

## Notes

- If the component pulls in a large dependency tree, summarize what is needed and confirm scope before porting everything.
- Screenshots may show composed sections (navbar + hero + footer). Port only the component the user asked about; ask if unclear.
