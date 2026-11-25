---
name: convert-web-pages-to-browser-extensions
version: 0.1.1
description: Convert any frontend webpage into a browser extension entry page with an HTML entry. Supports popup, options, sidepanel, devtools, newtab, bookmarks override, history override, and custom entries. Use when the user asks to migrate or adapt an existing web page into extension UI.
---

# Convert Web Pages to Browser Extensions

Use this skill to transform an existing frontend page into an extension entry with minimal behavior changes.

## When to Use

- User asks to convert a webpage/project into an extension page
- User wants one UI reused for `popup`, `options`, `sidepanel`, `devtools`, or `newtab`
- User asks for browser override pages such as bookmarks/history/newtab
- User has an existing `index.html` and wants it to become an extension entry
- User needs custom extension entries with explicit HTML files

## Scope

This skill focuses on **entry conversion and wiring**:

1. Keep UI behavior as-is where possible
2. Move or wrap page code into extension entry structure
3. Ensure an HTML entry exists for page-like entries
4. Update extension config/manifest mappings
5. Validate build and runtime constraints for extension contexts

## Mandatory Classification (Do First)

Before writing conversion code, classify the source page by:

1. **Frontend runtime**
   - Native HTML + JS
   - React / Vue / Svelte / Solid
2. **Style system**
   - Plain CSS
   - Tailwind CSS / UnoCSS
   - Less / Sass
3. **Third-party libraries**
   - Browser-safe client libraries (can run in extension UI/runtime)
   - Node-only libraries (require Node core APIs or server runtime)

This classification determines Addfox plugin wiring, dependency placement, and feasibility.

## Fast Workflow

Copy this checklist and update progress:

```md
Conversion Progress
- [ ] Identify source page dependencies and runtime assumptions
- [ ] Classify framework/style/library compatibility
- [ ] Choose target extension entry type
- [ ] Create/adjust HTML entry and bootstrap script
- [ ] Replace web-only APIs with extension-safe equivalents
- [ ] Wire manifest/config entry mapping
- [ ] Build and verify in extension runtime
```

## Entry Mapping Guide

| Target | Typical HTML entry | Notes |
|---|---|---|
| popup | `app/popup/index.html` | Small viewport, no long blocking tasks |
| options | `app/options/index.html` | Full settings UI, persistent controls |
| sidepanel | `app/sidepanel/index.html` | Chrome side panel UX constraints apply |
| devtools | `app/devtools/index.html` | Runs in DevTools context, API limits differ |
| newtab | `app/newtab/index.html` | Needs new tab override wiring |
| bookmarks override | `app/bookmarks/index.html` | Browser-specific override support |
| history override | `app/history/index.html` | Browser-specific override support |
| custom | `app/<custom>/index.html` | Add explicit entry mapping in config/manifest |

## Conversion Rules

1. Preserve user-visible behavior first, refactor later.
2. Keep HTML entry explicit for page-based entries.
3. Avoid direct assumptions about `window.location` origin and backend cookies.
4. Replace unsupported APIs (`alert`-style or blocked browser APIs) with extension-compatible alternatives.
5. Move privileged logic out of UI into background/content messaging when needed.
6. Keep permissions minimal and host matches explicit.

## Addfox Framework Required Work

When the target project uses Addfox, always complete these tasks:

1. **Entry layout**
   - Create or map entry files under `app/` (reserved or custom entry names).
   - Ensure page-like entries have `index.html` plus bootstrap script (`index.tsx`/`index.ts`/`index.js`).
2. **`addfox.config` wiring**
   - Configure `manifest` and entry mapping so Addfox can resolve output files.
   - Keep framework plugin list aligned with source stack (React/Vue/Preact/Svelte/Solid or vanilla).
3. **Manifest alignment**
   - Add entry-related keys (`action`, `options_ui`, `side_panel`, `devtools_page`, `chrome_url_overrides`, etc.).
   - Keep browser-specific sections explicit when Chromium and Firefox differ.
4. **Context adaptation**
   - Move privileged operations to background where required.
   - Add explicit messaging between page entry and background/content contexts.
5. **Build and runtime checks**
   - Run Addfox dev/build flows and verify extension loading.
   - Validate that assets, routing, and permissions work in real extension contexts.

## Framework and Style Mapping Rules

Use these rules during conversion:

- **Native HTML + JS**
  - Keep minimal Addfox config; no framework plugin needed.
- **React**
  - Add React plugin and React/ReactDOM runtime dependencies.
- **Vue**
  - Add Vue plugin and Vue runtime dependency.
- **Svelte**
  - Add Svelte plugin and Svelte runtime dependency.
- **Solid**
  - Add Solid plugin and Solid runtime dependency.

For styles:

- **Tailwind CSS / UnoCSS / Less / Sass**
  - Add corresponding build plugin/tooling and required style dependencies.
  - Ensure entry imports style files in the extension entry bootstrap path.

## Third-Party Library Compatibility Rules

Classify each third-party dependency before migration:

1. **Browser-compatible client library**
   - Can be bundled into extension entry/background/content as needed.
2. **Node-only library**
   - If it relies on Node built-ins (for example `fs`, `net`, `tls`, `child_process`) or server-only runtime, it is not directly runnable in extension UI contexts.
   - Mark as incompatible for direct client use and move to an alternative design (background with web APIs, remote service, or library replacement).

Do not silently keep Node-only dependencies in converted page entries.

## Required Checks

- Entry loads without blank screen
- Static assets resolve under extension URL
- Routing works with extension base path
- No CSP violations from inline scripts/eval
- Messaging works across UI/background/content boundaries
- Manifest keys match target entry type

## Common Fix Patterns

- **Asset path issues**: use root-relative or bundler-managed asset imports
- **Router base issues**: set hash/history base for extension origin
- **Storage migration**: switch from localStorage-only assumptions to extension storage as needed
- **Cross-origin calls**: move network calls requiring elevated permissions to background
- **Context mismatch**: gate code paths by runtime context (popup/options/devtools/etc.)

## Output Expectations

When applying this skill, provide:

1. Selected entry type and why
2. File mapping (source page -> extension entry files)
3. Manifest/config changes
4. Any runtime/API substitutions
5. Verification steps and known limitations

## Additional Reference

- Detailed conversion playbook: [reference.md](./reference.md)
- Practical conversion samples: [examples.md](./examples.md)
