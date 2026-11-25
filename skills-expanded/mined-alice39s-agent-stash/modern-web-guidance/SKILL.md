---
name: "modern-web-guidance"
description: "Offline copy of GoogleChrome/modern-web-guidance: 208 guides on modern HTML, CSS, and client-side JavaScript (dialogs, popovers, anchor positioning, container queries, view transitions, scroll-driven animations, forms, autofill, validation, accessibility, dark mode, Core Web Vitals, image loading, security, passkeys, sanitization, web components, built-in AI, WebMCP). Use before writing or changing web UI, CSS layout or animation, or browser-side JS, including HTML/CSS/DOM inside React, Vue, or other frameworks. Not for backend code, build tooling, CI, or tests."
license: "CC-BY-4.0"
metadata:
  updated: "2026-11-10"
  sources: "GoogleChrome/modern-web-guidance, npm modern-web-guidance@1.0.0"
  generator: "scripts/sync-modern-web-guidance.ts"
---

# Modern Web Guidance

Guides from [GoogleChrome/modern-web-guidance](https://github.com/GoogleChrome/modern-web-guidance), copied from npm `modern-web-guidance@1.0.0` (skill version `2026_11_09-5bcc021b`, published 2026-11-10). Each guide is `references/<category>/<id>.md`; each category's `index.md` lists its guides with a one-line description, a token count, and feature gates.

## Workflow

1. Find guides. Open the index of each category that fits the task, or search all indexes at once: `rg -i "<keyword>" references/*/index.md`. Search by the user-visible capability or the UI primitive it implies (`confirm dialog`, `date picker`), not by framework or app names, and search once per feature when a task touches several.
2. Read the matching guides in full, plus the discipline guide of the same category when the table below lists one. Guides cite other guides as `npx -y modern-web-guidance@latest retrieve "<id>"`; read `references/*/<id>.md` for those instead of running the command.
3. Write the code with the guide's patterns and fallbacks, then check the result against the guide and the user's request before finishing.
4. When no guide matches after a second search, continue without one.

## Feature gates

A guide with an Origin Trial or Volatile entry in the Gate column relies on an experimental Origin Trial API or on a feature that ships in one engine only or is still changing. Use such a guide only when the user agrees, or when `.mwgrc` in the project root (or `~/.mwgrc`) sets `"allowOriginTrials": true` or `"allowVolatileFeatures": true` respectively.

## Browser support

- Baseline Widely available features need no fallback. For any other feature, follow the fallback the guide gives.
- When the user or the project states a support policy (for example `Safari 17.4+` or `Baseline 2024`), use the compatibility data in the guide to decide which fallbacks to keep. A feature meets a `Baseline YYYY` target when its Baseline year is YYYY or earlier.

## Frameworks

The guides use plain HTML, CSS, and JavaScript. Keep the platform feature when porting to a framework:

- Pass new HTML attributes that the framework types do not know yet (`popover`, `commandfor`, `interestfor`) through a spread or cast instead of dropping them.
- Guard `window` and DOM globals during server rendering, and load polyfills with a dynamic `import()` on the client.
- Call `showModal()` and similar methods through refs, generate per-instance IDs and `anchor-name` values, and keep `:root` and `@starting-style` rules unscoped.

## Categories

| Category | Guides | Discipline guide | Index |
| --- | --- | --- | --- |
| accessibility | 4 | [accessibility](references/accessibility/accessibility.md) | [index](references/accessibility/index.md) |
| built-in-ai | 4 | - | [index](references/built-in-ai/index.md) |
| css | 18 | [css](references/css/css.md) | [index](references/css/index.md) |
| forms | 19 | [forms](references/forms/forms.md) | [index](references/forms/index.md) |
| html | 8 | [html](references/html/html.md) | [index](references/html/index.md) |
| js | 5 | - | [index](references/js/index.md) |
| performance | 26 | [performance](references/performance/performance.md) | [index](references/performance/index.md) |
| privacy | 1 | [privacy](references/privacy/privacy.md) | [index](references/privacy/index.md) |
| pwa | 2 | - | [index](references/pwa/index.md) |
| security | 17 | [security](references/security/security.md) | [index](references/security/index.md) |
| ui-atoms | 13 | - | [index](references/ui-atoms/index.md) |
| ui-behaviors | 40 | - | [index](references/ui-behaviors/index.md) |
| ui-components | 22 | - | [index](references/ui-components/index.md) |
| user-experience | 3 | - | [index](references/user-experience/index.md) |
| visual-design | 22 | - | [index](references/visual-design/index.md) |
| wasm | 1 | - | [index](references/wasm/index.md) |
| webmcp | 3 | [webmcp](references/webmcp/webmcp.md) | [index](references/webmcp/index.md) |

## Source and license

The guide text is from GoogleChrome/modern-web-guidance and is licensed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/); parts of it derive from MDN Web Docs and from W3C, WHATWG, and IETF specifications. `sources.json` records the package version, tarball, and the upstream index entry of every guide. `scripts/sync-modern-web-guidance.ts` in Alice39s/agent-stash copies the guides and writes this file and the category indexes.
