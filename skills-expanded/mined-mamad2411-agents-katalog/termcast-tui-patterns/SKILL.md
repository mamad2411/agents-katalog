---
name: termcast-tui-patterns
description: "termcast (Raycast-API-shaped terminal UI, Bun) component and PTY e2e testing patterns. Explicit-only — loaded via bootstrap:init Step 1b for termcast projects."
user-invocable: false
allowed-tools: Read
---


# termcast TUI Patterns

Explicit-only skill for termcast (Raycast extension API, ported to the terminal via
`@opentui/react` + Bun) projects. Named caller: `/bootstrap:init` Step 1b (marker: `package.json`
declares a `termcast` dependency -> candidate skill `termcast`); also referenced from
`templates/workflow/tui-app.CLAUDE.md.tmpl`'s on-demand loading table. No natural end-user
trigger phrase exists yet — auto-trigger promotion is a future, evidence-driven change
(design.md D4 of `add-tui-app-stack`).

## Routing

| Working on | Load |
| --- | --- |
| `List`/`Detail`/`Form`/`ActionPanel` component usage | `references/component-api.md` |
| Accessory alignment (equal counts/order per `List.Item`) | `references/component-api.md` |
| `accessoryTagsLayout` column widths | `references/component-api.md` |
| `useCachedPromise` + `revalidate()` | `references/component-api.md` |
| Cache vs `LocalStorage` | `references/component-api.md` |
| Bun explicit-`react`-dep gotcha (`useSyncExternalStore` crash) | `references/component-api.md` |
| Writing a `*-demo.tsx` mock-data variant | `references/tui-e2e-testing.md` |
| `launchTerminal` / PTY driving (`press`, `type`) | `references/tui-e2e-testing.md` |
| `toMatchInlineSnapshot` golden frames, `pnpm e2e -u` | `references/tui-e2e-testing.md` |
| CI-skip when the extension folder is absent | `references/tui-e2e-testing.md` |

## Agent rules digest

`templates/workflow/tui-app.CLAUDE.md.tmpl` § Agent Rules lays down the same 9-item termcast
canon (`logger.log` not `console.log`; no `setTimeout` for React state; minimize `useState`;
`.tsx` for all JSX; `ctrl`/`alt`+letter shortcuts only; `showFailureToast` in actions;
`revalidate()` after mutations; equal accessory counts per `List.Item`; explicit `react` dep
under Bun) in every scaffolded project's CLAUDE.md. This skill is where to go for the worked
examples and *why* behind each rule — start with `references/component-api.md`.
