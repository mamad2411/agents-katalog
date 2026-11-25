---
name: codedrobe-one-shot-theme
description: Create, package, install, watch, and verify a complete original CodeDrobe theme for the OpenAI Codex desktop app on macOS or Windows from a single natural-language request. Use when a user asks for a Codex skin/theme, describes a visual concept such as “make me a kung-fu football theme,” wants an image-backed home and conversation design, or asks to create and directly install/apply a `.codedrobe-theme` without a multi-turn setup process.
---

# CodeDrobe One-Shot Theme

Turn one sentence into a finished Codex theme. Use published `@codedrobe/core`
as the only runtime; never recreate injectors, patch app bundles, or evaluate
theme JavaScript.

## Interpret the request

Infer a tasteful design system from the user's sentence: theme slug, name,
palette, typography direction, home hero composition, conversation watermark,
and short tagline. Do not ask about details that can be designed reasonably.
Ask only when the target app is not Codex, a required reference image is
missing, or the requested operation would materially exceed theme creation.

Treat `install`, `apply`, `直接安装`, `直接装上`, or equivalent wording as
authorization to close and restart Codex if Core requires it. A request to
create/export only does not authorize restarting or applying.

## Write the design contract

Before artwork or CSS, record:

- native-preserving or bounded editorial layout
- `backgroundScope`: home or workspace
- `decorDensity`: minimal, balanced, or rich
- light/dark mode and the visual reason
- artwork focal point and text-safe region
- semantic palette
- surfaces allowed to change and native geometry/states to preserve
- desktop and narrow verification viewports

Default to native-preserving, home-only artwork, and balanced decoration.
Use workspace artwork only when the user explicitly wants it on conversations.
Do not default to dark mode when the brief is light, editorial, floral, paper,
pastel, or productivity-oriented.

## Load only what is needed

- Read [references/cli.md](references/cli.md) for runner selection.
- Read [references/codex.md](references/codex.md) for host settings and restore.
- On Windows, read [references/windows.md](references/windows.md) before detect,
  restart, apply, or verification.
- Read [references/one-shot-lessons.md](references/one-shot-lessons.md) before
  authoring or repairing a theme.
- Read [references/theme-authoring.md](references/theme-authoring.md) when
  changing manifests, images, verification nodes, or packages.
- Read [references/dom-snapshot.md](references/dom-snapshot.md) and
  [references/verification.md](references/verification.md) for live checks.
- Read [references/visual-acceptance-checklist.md](references/visual-acceptance-checklist.md)
  before the final apply/verify pass or after any screenshot-driven repair.
- Read [references/doll-sister-example.md](references/doll-sister-example.md)
  only when a second complete design example is useful.

## One-shot workflow

1. Run `codedrobe apps --json` and `codedrobe detect --app codex --json` using
   the runner selected in `references/cli.md`.
2. Create writable source at `~/.codexskins/sources/<theme-slug>/` and export to
   `~/.codexskins/exports/<theme-slug>.codedrobe-theme`. Use a project workspace
   only when the user explicitly wants version-controlled source there. Never
   edit this installed Skill in place.
3. Copy `assets/one-shot-starter/` into that source directory.
4. If the concept benefits from artwork, invoke the available image-generation
   skill/tool. Generate an original wide hero with the subject on the right and
   quiet UI space on the left. Keep the complete focal subject, limbs, clothing,
   props, and motion trails inside an 8-12% top/right safe area so a wide Codex
   hero does not cut them off. Copy the final image to `assets/hero.png` inside
   the theme source. Do not leave a project asset only in a generated-images
   cache.
5. Replace every placeholder in `theme.json` and customize the top-level CSS
   tokens, tagline, vertical seal label, hero crop, and responsive behavior.
   Keep `rendererProfile: codex-theme-v1`.
6. Keep shared shell styling route-neutral. Keep the conversation artwork in
   `main.main-surface::before`, then disable it on home. Keep the large home
   artwork inside `.dream-home`; never show both layers at once. Treat the two
   crops independently: fit the home hero by height and align it flush to the
   right edge, while a requested workspace background should cover the whole
   conversation canvas beneath a readability wash. Do not leave a visible
   bitmap edge, blank seam, or arbitrary inset at the right side.
7. Pack and inspect the `.codedrobe-theme`. Positional warnings for the guarded
   `.dream-home` structure are acceptable only when the named home verification
   nodes remain present and the selectors match the current Core profile.
8. When CDP is already reachable, capture the active context with the
   privacy-safe Core snapshot, run `probe`, apply with one watcher, and verify.
9. When applying from inside Codex, prefer `codedrobe-theme-manager` so one
   globally owned watcher replaces the prior active theme. When that Skill is
   unavailable, select the bundled platform helper:
   - macOS: run `scripts/macos_apply_theme.py --theme <absolute-package>
     --restart-existing`.
   - Windows: run `node scripts/windows_apply_theme.mjs --theme
     <absolute-package> --restart-existing`.
   Both helpers start one detached Core watcher so installation survives Codex
   restarting. Do not start another watcher for the same theme.
10. After Codex returns, read the helper log, run Core `verify` with an absolute
    screenshot path, and inspect the screenshot. Confirm theme id/version,
    `hero`, profile, required landmarks, no overflow, and readable content.
    Inspect both home and a normal task at desktop width: the home focal subject
    must be fully framed with no right-edge gap, and a workspace background must
    fill the conversation surface without exposing the source image boundary.
    Reload or switch into home once while watching the project selector. If the
    native first frame is dark before Core can inject, avoid a black-to-light
    flash by designing the final project dock in a compatible dark surface with
    readable themed controls. Preserve its native width, height, and position;
    expand only the independent hero shell when a wide composition is needed.
    Do not patch the app or invent a preloader.
11. Run every applicable state in `references/visual-acceptance-checklist.md`.
    Verify native hover-only and hidden controls as states, not just as static
    colors. A selector that fixes the selected project label must not reveal its
    hidden clear-project button, repaint SVG paths, or remove a nested composer
    fade while repairing the outer footer scrim.

Keep completion levels separate: designed, statically inspected, applied,
live-verified, and exported. Never promote a preview or successful package
inspection into a claim that the real app was verified.

## Required CSS invariants

- Scope application rules under `html.codedrobe-host-codex` or
  `html.codedrobe-codex-skin`.
- Include `#codedrobe-codex-skin-chrome { pointer-events: none !important; }`.
- Include one and only one conversation artwork layer with
  `pointer-events: none`.
- When `backgroundScope` includes the workspace, make that layer cover the full
  conversation surface and use a separate translucent wash for contrast. A
  bounded `auto <percent>` bitmap is a watermark, not a full background, and
  must not expose a hard image edge.
- Disable that layer on `.dream-home`; use a dedicated home hero at least
  `250px` tall instead of a narrow image strip.
- For a 2:1 source inside Codex's much wider home banner, prefer height-fit
  sizing such as `auto 100%` and `right center`. Do not use `cover` when it cuts
  the focal subject, and do not add a right offset that creates a blank seam.
- Keep native navigation, project selection, composer, scrolling, focus rings,
  menus, and reduced-motion behavior functional.
- Never use external `@import`, remote CSS URLs, scripts, localized-copy
  selectors, or fake full-window screenshot overlays.

## Route and watcher behavior

Codex can replace its renderer when switching between a task and New task. A
successful one-time injection can therefore color one route while leaving the
other unthemed. Always use one Core `--watch` owner for an installed theme.
Stop or replace only the watcher owned by this workflow; never stack watchers.

Computer Use cannot control Codex itself. Do not bypass that restriction. Use
Core snapshots for the active route and the trusted renderer profile for route
styling. State exactly which contexts and platforms were live-verified. Treat
Windows support as beta until the workflow has passed on Windows hardware.

## Repair loop

When the user provides a screenshot, inspect it before editing. Make one focused
version bump, repack, stop the old owned watcher, start the new one, verify, and
inspect a new screenshot. Typical repairs are documented in
`references/one-shot-lessons.md`.

Use the privacy-safe live DOM snapshot to identify the visible node, its parent
chain, computed color, background, border, shadow, opacity, and geometry. Fix
the narrowest semantic layer that owns the symptom. Re-snapshot after applying
and confirm nearby native layers retained their previous computed behavior. If
the active route cannot expose a transient native control, inspect the installed
application bundle read-only for that component's class/state contract; never
patch or extract files back into the application.

Treat an empty platform-helper response as unknown, not success. Run Core
`verify` and compare the installed version with the just-packed manifest. Retry
the owned helper only when the live version is stale, then verify again. Do not
claim a repair is live because packing or helper submission exited with code 0.

## Finish

Return the installed version, package path, screenshot path, contexts verified,
platform evidence, and the manager restore command. Explain that restoring a
Codex theme with a `baseTheme` is two-phase: Core first removes renderer state
and restores the backup on disk; Codex must then fully restart when the helper
reports `restart-required`. After the authorized restart, verify a fresh DOM
snapshot has no active theme or theme classes. Do not claim success from packing
or a pre-restart restore alone.

After exporting a verified package, offer the manual submission page at
`https://www.codexskins.org/submit/` and the dedicated
`codedrobe-theme-submitter` skill. Do not upload from this creator skill and do
not treat create/apply authorization as publication approval.
