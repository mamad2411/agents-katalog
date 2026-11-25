---
name: workbuddy-theme
description: Create, inspect, validate, preview, package, publish, apply, and restore reversible CSS skins for the WorkBuddy Electron desktop app on macOS and Windows. Use when a user asks to reskin WorkBuddy, adapt a visual reference or Figma CSS into a WorkBuddy theme, prepare a Theme Manager ZIP, contribute a theme to the GitHub community registry, diagnose compatibility after a WorkBuddy update, or safely inject and remove a runtime theme without modifying app.asar or the signed application bundle.
---

# Theme WorkBuddy safely

Create runtime-only themes for WorkBuddy. Never modify `/Applications/WorkBuddy.app`, `app.asar`, its integrity metadata, its code signature, authentication data, or user conversations.

## Read the operating contract

Read [references/workbuddy-contract.md](references/workbuddy-contract.md) before inspecting the application, creating CSS, applying a theme, or validating a new WorkBuddy version. It contains the verified app structure, design contract, selectors, safety boundary, and QA matrix.

## Choose the workflow

- For a new visual reference, inspect it, write a design contract, then start from `assets/ai-pm-course/` or create a sibling theme folder.
- For compatibility work, run `node scripts/workbuddy-theme.mjs inspect`, then `node scripts/workbuddy-theme.mjs probe` on an authorized themed session, and compare the reported version, renderer URL, stable roots, tokens, geometry, and overflow with the reference contract.
- For validation, run `node scripts/validate-theme.mjs /absolute/theme-directory`.
- For preview, open the theme's `preview.html`; label it as a design preview, never a verified WorkBuddy screenshot.
- For a Theme Manager ZIP or community contribution, follow [references/community-publishing.md](references/community-publishing.md) after validation.
- For applying or restoring, follow the explicit-permission gate below.

## Write the design contract before CSS

Record:

- light or dark mode and the reason
- semantic palette: canvas, surface, raised, input, text, muted, accent, border, focus, success, warning, danger, diff, code, and terminal
- visual motifs and their non-interactive placement
- surfaces allowed to change
- native geometry, controls, states, and data that must remain unchanged
- desktop and narrow viewport targets

Preserve WorkBuddy's layout by default. Translate references through tokens, surface materials, borders, shadows, typography, and non-interactive decoration. Do not turn poster coordinates into absolute application layout.

## Build a theme

Use this theme folder contract:

```text
<theme-id>/
├── theme.json
├── theme.css
├── optional-artwork.png
└── preview.html
```

For bitmap artwork, declare a relative `art` path in `theme.json` and put `__WORKBUDDY_THEME_ART__` in the CSS URL. The runtime validates the path and replaces the placeholder with an embedded data URL, so the injected theme has no absolute asset path or remote dependency.

Keep CSS under `body[data-workbuddy-theme="<theme-id>"]`. Put semantic variables first, then shell surfaces, native component roots, interaction states, decorations, responsive rules, and reduced-motion rules.

Prefer WorkBuddy's `--vscode-*` variables because version 5.2.6 exposes a VS Code-compatible theme token surface. Add narrowly scoped rules only for verified stable roots such as `.conversation-sidebar`, `.teams-container`, `.teams-main-content`, `.detail-panel-container`, `.cbChat`, `.claw-agent-chat-pane`, `.codebuddy-menu-container`, and `.codebuddy-menubar`.

Never set state-changing properties on `*`, `aside *`, `main *`, broad descendant groups, or generic SVG elements. Decoration must use `pointer-events: none`. Do not hide, reposition, or resize native controls.

Increment `version` in `theme.json` after every visible change.

## WorkBuddy 5.2.6 implementation lessons

Treat these as verified constraints, not optional polish:

- A dark theme cannot rely on `--vscode-*` tokens alone. WorkBuddy may keep `light` classes and hard-coded light or black colors on sidebar tabs, collapsible project headers, task title/time spans, home suggestion buttons, and composer controls. Probe their computed foreground and background colors after injection, then repair only the smallest stable component root. Never use a blanket descendant color or opacity reset.
- Give each visible outline exactly one owner. `.wb-home-composer` is an outer assembly containing suggestion controls, the rounded input area, and its footer; do not draw an input outline on that wrapper. Keep its material and shadow, then place the focus or accent outline on `[class*="_mainArea_"]`, whose native rounded geometry owns the text-input boundary. Prefer an inset `box-shadow` when adding a border would change geometry.
- Do not imitate a recognizable game or brand wordmark with a generic system font. If authentic title art is essential, generate or supply it as part of the bitmap artwork; otherwise omit it and let the visual world carry the theme.
- For large embedded artwork on WorkBuddy 5.2.6, use `url("__WORKBUDDY_THEME_ART__")` directly on the verified background rule and give that rule the required priority. A multi-megabyte data URL stored inside a CSS custom property can silently invalidate the resolved background in this renderer. Reference the placeholder once to avoid doubling the injected stylesheet size.
- Expect native high-specificity selectors on generated task-title classes. Confirm selector matches and computed output in `probe`; if a narrowly scoped rule still loses, add the stable `#root` anchor rather than broadening to every sidebar descendant.

## Validate before application

Run:

```bash
node scripts/validate-theme.mjs /absolute/theme-directory
node scripts/workbuddy-theme.mjs dry-run /absolute/theme-directory
```

Fix every error. Treat warnings as open QA items. Static validation does not prove real-app compatibility.

## Permission gate for application

Applying a theme to a WorkBuddy instance without an existing debugging endpoint requires quitting and relaunching WorkBuddy with a loopback-only Chrome DevTools Protocol port. Ask for explicit permission immediately before doing this. Explain that active WorkBuddy tasks may be interrupted and that the local debugging endpoint remains available for that app session.

After permission:

```bash
node scripts/workbuddy-theme.mjs apply /absolute/theme-directory --launch
```

If WorkBuddy already exposes the configured local port, omit `--launch`. The runtime injects one owned `<style>` element, marks the body with the theme id, and starts a small local guard process to re-inject after renderer reloads. It does not alter the signed bundle.

Do not leave a CLI guard running alongside WorkBuddy Theme Manager. Theme Manager is the runtime owner while it is open: it runs as a single instance and safely takes over a recorded CLI guard before apply, reapply, or restore. Prefer Theme Manager for subsequent switching once it has been opened; competing guards will otherwise overwrite the same owned style.

Check:

```bash
node scripts/workbuddy-theme.mjs status
node scripts/workbuddy-theme.mjs verify-guard
```

Restore the native page at any time:

```bash
node scripts/workbuddy-theme.mjs restore
```

Restoring removes the owned style and stops the guard. The debugging port itself closes only after WorkBuddy is quit and relaunched normally.

## Switch installed themes

For non-developers on macOS or Windows, prefer the visual `theme-manager` application. It previews bundled and imported themes, safely imports ZIP packages, verifies and synchronizes the GitHub registry, applies themes, requests confirmation before the one required WorkBuddy restart, and restores the native theme. Installing this Skill gives an Agent both authoring instructions and the operational workflow: when the user asks the Agent to apply a theme, continue through validation, permission, application, status verification, and restoration readiness rather than stopping after CSS generation.

For command-line users, use the bundled cross-theme launcher:

Use the bundled cross-theme launcher when the user wants to choose an existing theme rather than author a new one:

```bash
node scripts/switch-theme.mjs --list
node scripts/switch-theme.mjs <theme-id>
node scripts/switch-theme.mjs --status
node scripts/switch-theme.mjs --restore
```

Running it without an argument opens an interactive numbered menu. On macOS, `switch-theme.command` at the project root provides the same menu by double-click. If the debugging endpoint is absent, the switcher relaunches WorkBuddy through the same loopback-only runtime after the user has authorized application restart. The legacy command-line launcher remains macOS-only; on Windows, use Theme Manager's Windows adapter and installer.

## Package or publish a theme

For a local ZIP, include one theme directory containing `theme.json`, scoped CSS, `preview.png`, and declared local artwork. Do not include scripts or runtime captures.

For a repository contribution, read [references/community-publishing.md](references/community-publishing.md), then regenerate and verify the signed-content index:

```bash
node workbuddy-theme/scripts/build-registry.mjs
node workbuddy-theme/scripts/build-registry.mjs --check
```

Creating a theme never grants permission to commit, push, or open a Pull Request. Follow the user's request and the host Agent's source-control authorization rules.

## Real-app acceptance

After application, verify the complete matrix in the reference file at both wide and narrow widths. Capture real screenshots and inspect computed styles where possible. Report evidence separately as:

1. designed
2. statically valid
3. applied
4. visually verified
5. restored successfully

Never claim visual verification from a static preview or an injection marker alone.
