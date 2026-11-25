---
name: domino-ui-bootstrap
description: Bootstrap or retrofit a Vite + React 18 + TypeScript project so it uses the Domino design system (`@dominodatalab/extensions-tools`). Scoped to a **fully standalone SPA frontend for a Domino application or extension**, not snippets, library additions, or work inside an existing Domino monorepo package. Use whenever the user wants to create, scaffold, refactor, retrofit, or set up such an SPA (a React app, web app, frontend, UI, or extension) that should "look like Domino", use Domino components, follow the Domino design system, or integrate with the Domino platform, including when they mention DominoThemeProviderDecorator, extensions-tools, or base-components without saying "Domino". Also use to make an existing standalone React/Vite project "Domino-styled" or add Domino theming. Handles React 18 / react-router 5 pinning, Storybook MCP registration, theme provider wiring, and build verification.
compatibility: Domino 6.3 and Domino Cloud. Needs Node that satisfies the Vite scaffold's engines range (^20.19.0 or >=22.12.0) or the Vite 5 fallback in SETUP-STEPS.md, and access to the npm registry that hosts @dominodatalab/extensions-tools. No Domino API calls.
---

# Domino UI Bootstrap

Applies to Domino 6.3 and Domino Cloud.

This skill makes a project use the Domino design system correctly. It works in three contexts:

- **Empty or non-existent directory** — scaffold a Vite + React 18 + TS project from scratch, then apply the Domino setup.
- **Existing Vite + React project** — leave the project alone, retrofit just the Domino bits (deps, theme provider, MCP, agent instructions file).
- **Existing React project on a different bundler/setup** — flag the mismatch to the user, then proceed only with their direction.

In all three cases, the skill executes the work end-to-end (runs commands, edits files), but it adapts to what's already there instead of overwriting blindly.

## Why this exists

A handful of choices look arbitrary but aren't — they match the rest of the Domino ecosystem and are easy to get wrong:

- **React 18, not 19.** `@dominodatalab/extensions-tools` peer-depends on React 18. React 19 fails at install.
- **react-router 5, not 6.** The library uses v5 APIs (`HashRouter` from `react-router-dom@5`).
- **HashRouter, not BrowserRouter.** This is what the library expects internally, and what the `domino-apps` skill recommends for every React app on Domino. Client-side routes live entirely after the `#`, so they never collide with backend paths or the Domino proxy prefix, relative asset URLs resolve from the app root on every route, and inner navigation works without server-side rewrite rules.
- **The npm package name is `@dominodatalab/extensions-tools`.** Storybook code snippets show imports from `@domino/base-components` — that's a Storybook-internal alias. Rewrite every such import to `@dominodatalab/extensions-tools` before pasting into a Domino project.
- **`DominoThemeProviderDecorator` wraps the whole React tree.** Without it, Domino components render unstyled or crash.
- **URLs must survive the proxy path.** Domino serves the app under a prefix (e.g. `/preview/<appId>/`), so asset and API URLs must be document-relative — not root-absolute. Vite's default `base: '/'` emits `/assets/…` and bypasses the proxy; user-written `fetch('/api/…')` does the same. Set `base: './'`, build API URLs against `document.baseURI`, and add the trailing slash when the App is opened without it (Domino serves `<prefix>` and `<prefix>/` alike, and relative URLs then resolve one level up). See Step 8. Invisible in local dev (`pathname` is `/`), surfaces only after deployment.

Treat these as invariants the project must satisfy by the end. How you get there depends on what's already in the target directory.

## Host-specific files

Steps 2, 6, 10, 11, and 13 write files that depend on which coding assistant is running this skill. Use the column for the current host. If you can't tell which host you are, or it isn't listed, ask the user which files their assistant reads.

| Purpose | Claude Code | Codex |
|---|---|---|
| Agent instructions file | `CLAUDE.md` | `AGENTS.md` |
| MCP server registration | `.mcp.json` | `.codex/config.toml` |
| Per-user MCP enablement | `.claude/settings.local.json` | None needed; Codex loads `.codex/config.toml` once the user trusts the project |
| Reload after MCP changes | Restart Claude Code | Restart Codex |

The rest of this skill calls these the **instructions file**, the **MCP config**, and the **MCP enablement file**.

---

## Workflow

Work Steps 1–13 in order; each reference file holds the full procedure for its steps. Retrofits skip Step 3 (scaffold) and Step 9 (starter screen); a project already on `@dominodatalab/extensions-tools` is a verification/repair job (Step 2 table). "Done" is gated by Step 12.

## Reference files

- [SETUP-STEPS.md](./SETUP-STEPS.md) — Steps 1–7: elicit paths and names, survey and classify the directory, scaffold, align `package.json` to the pins (incl. the Node < 20.19 toolchain branch), install, register the Storybook MCP, wire the entry point.
- [APP-SOURCE.md](./APP-SOURCE.md) — Steps 8–9: proxy-aware URLs (`base: './'`, `apiBase` from `document.baseURI`), starter screen, CSS reset, components safe to use without an MCP query.
- [PROJECT-FILES.md](./PROJECT-FILES.md) — Steps 10–11: instructions file (write or merge) and `.gitignore`.
- [VERIFY.md](./VERIFY.md) — Steps 12–13: `npm run build` gate, `dist/index.html` URL check, build-failure causes, hand-off checklist.

---

## Guiding principles when in doubt

- **Describe the goal, change the minimum.** The invariants in this skill are about Domino integration. Everything else in the user's project is their business — don't touch what isn't broken.
- **Read before you write.** On any retrofit, view a file before modifying it. The user's structure matters; preserve it where the Domino constraints don't override it.
- **Surface, don't silently fix.** If the user's existing code conflicts with a Domino invariant (router v6 routes, React 19 hooks), tell them what needs to change. Don't rewrite their app under the hood.
- **Test cases over conviction.** When unsure whether a component or prop exists, query the Storybook MCP. Don't ship invented props.

---

## What this skill is not for

- Editing `@dominodatalab/extensions-tools` source. Only the published npm package is consumed; upstream changes need a release from the library repo.
- Setting up test runners, CI, Tailwind, or other tooling on top. If the user wants those, finish the Domino bootstrap first (Step 12 green), then handle them separately — too many things can fail at once otherwise.
- Authenticating to private npm registries. If install fails on auth, ask the user; don't guess at credentials or workarounds.
- Building anything beyond a minimal app *before* the Storybook MCP is running. If the user asks for more than a minimal application while the MCP is not yet available, only scaffold the boilerplate plus a minimal app, then instruct the user to restart their assistant after finishing the app configuration so the MCP loads and the rest can be built against real component APIs.
