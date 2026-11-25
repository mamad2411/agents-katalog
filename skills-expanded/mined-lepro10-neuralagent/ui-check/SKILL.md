---
name: ui-check
description: Screenshot NeuralAgent screens at phone and desktop sizes in light and dark mode against a throwaway test daemon, then review them against the design system. Use after any UI change, when the user says "ui check", "screenshots", "wie sieht das aus", or before a release.
---

# UI check

Tools: `scripts/dev/README.md`. Design rules: `docs/notes/design-system.md` (read sections 1–7
once per session). Never point these tools at the owner's real daemon; they refuse it anyway.

## 1. Start (own home and port if another agent may be running one)
```
node scripts/dev/env.mjs status                       # something already up on /tmp/na-ui?
node scripts/dev/env.mjs up --seed [--llm] [--home /tmp/na-ui-<you> --port 1452]
```
`--seed` gives four workspaces, Claude/Codex/Gemini stand-ins in all states, a swarm and MCP
servers; `--llm` adds a fake Neural model. Pass the same `--home/--port` to every command below.

## 2. Shoot
```
node scripts/dev/shot.mjs pages --devices phone,small,kb,desk --schemes light,dark --montage --tag <topic>
node scripts/dev/shot.mjs pages agents settings --devices phone --schemes dark   # only what changed
```
- Sizes: `phone` 390×844, `small` 360×780, `kb` 390×450 (keyboard open), `desk` 1440×900;
  `tablet`/`laptop` when layout breakpoints changed.
- A screen without a scene (a sheet, a dialog, a new page): add `scripts/dev/scenes/<name>.mjs`
  (see `scenes/pages.mjs`) instead of a one-off script. Fake update states: `--hash "&update=0.3.0"`.
- Web remote screens: `node scripts/dev/web-remote.mjs --montage` (needs the web build).
- Output in `research-local/shots/` (git-ignored). Default DPR 1 keeps images small.

## 3. Review (montage first, single shots only where something looks off)
Per screen and size, in both schemes:
- Nothing under the status bar or tab bar (safe areas), nothing cut off at 360 px, no horizontal scroll.
- Touch targets ≥ 44 px on phones; text readable; contrast fine in **light** mode too.
- Standard parts: `Page`, `List`/`Row`, `Empty`, `SkeletonList`, `Menu` for choices, `Sheet` for
  tasks; no custom overlays; sheets usable with the keyboard open (`kb`).
- Activity marks and status colours as in design-system section 5; motion not janky.
- Errors: `shot.mjs` prints redacted console errors and exits 1 on a failed device/scheme.
Then `pnpm typecheck && pnpm lint:tokens`.

## 4. Stop and report
```
node scripts/dev/env.mjs down [--home …]              # stops exactly what `up` started
```
Report in short, simple German: what was checked (screens × sizes × schemes), what looks off
(file + screenshot path), what you fixed. Known gaps are listed at the end of
`docs/notes/design-system.md`; do not report those again.
