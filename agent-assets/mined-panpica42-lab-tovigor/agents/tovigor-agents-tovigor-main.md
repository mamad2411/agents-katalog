# Repository Guidelines

## Project Structure & Module Organization
This repository is a `uni-app` application built on Vue 3 and maintained primarily in HBuilderX. Core entry files live at the root: `main.js`, `App.vue`, `pages.json`, `manifest.json`, and `uni.scss`.

- `pages/`: page-level views grouped by feature, such as `freeTraining/`, `partTraining/`, `smartAssess/`, `games/`, and `serial-test/`.
- `components/`: shared UI, including modal and layout primitives.
- `utils/`: reusable logic and service modules, including serial-device integration in `serialService.js`.
- `static/`: bundled static assets.
- `docs/`: product and development notes.
- `_deprecated/`: legacy code kept for reference only; avoid new work here.

Register new routes in `pages.json` and keep feature-specific components close to the page that uses them when reuse is limited.

## Development Workflow
- Use HBuilderX as the primary development and build environment.
- Main target platform is Android App.
- H5 should be treated as a preview/debug surface, not the source of truth for hardware behavior.
- Do not treat `npm` scripts as the standard workflow for this repository.
- Do not proactively use `node`, `npm`, or Node-based tooling unless the user explicitly asks for it or the current task clearly depends on it.
- Do not start subagents.
- Do not perform full-project searches unless the user explicitly asks for one.

## Coding Style & Naming Conventions
Follow the existing style: tab indentation in `.js`, `.vue`, and JSON-like config files. Use single quotes in JavaScript unless the file already differs. Prefer `camelCase` for variables and functions, `PascalCase` for globally registered components, and kebab-case file names for page and component `.vue` files such as `free-training-intro.vue`.

Keep page logic feature-local when possible. Shared device or business logic belongs in `utils/` or a reusable component.

## Vue Conventions
- Treat this repository as a Vue 3 uni-app project.
- Prefer Composition API and `<script setup>` in `.vue` pages and components.
- Keep the app entry aligned with Vue 3 `createSSRApp`.
- Do not introduce new Vue 2 patterns such as `new Vue(...)` in active code.

## Encoding Rules
Treat all Chinese text in this repository as UTF-8. When editing `.vue`, `.nvue`, `.js`, or `.md` files that contain Chinese comments, UI copy, or logs, preserve readable Chinese and do not introduce mojibake or replacement text.

When reading files that may contain Chinese text, always use an explicit UTF-8 decoding path. Do not rely on terminal, shell, or operating-system default encodings when inspecting repository contents.

On Windows PowerShell, treat the default decoding behavior as unsafe for UTF-8 files without BOM. When using commands such as `Get-Content`, explicitly specify `-Encoding UTF8`, or read bytes and decode them as UTF-8 before trusting the displayed text.

If a file already contains garbled Chinese, do not continue editing those broken strings blindly. First confirm the intended text, then repair or replace it in valid UTF-8 before making further content changes.

## Patch Application Reliability
Before applying a patch, re-read the exact target block from disk and confirm the current context still matches. Do not rely on stale output from an earlier read when the file may have changed.

Keep patches as small as practical. Change one logical block at a time, and do not mix behavior edits with unrelated whitespace, line-ending, indentation, quote-style, or comment churn.

When editing UTF-8 files that contain Chinese text, keep the read path explicitly UTF-8 before preparing the patch, and avoid incidental encoding or line-ending normalization as part of the same edit.

If a target file already has uncommitted changes, treat the on-disk content as the source of truth and patch around it instead of assuming the previous state.

If a patch fails to apply, re-read the file, compare the live text with the expected context, and retry with a narrower patch. After repeated failure, stop blind retrying and explain the mismatch before continuing.

## nvue / Android Rules
Treat `nvue` pages on Android as a separate rendering environment from standard `.vue` pages. Do not assume WebView behavior applies to native rendering, especially for `video`, overlays, `z-index`, fixed/absolute positioning, and gesture handling.

For floating controls on `nvue` pages, prefer page-local implementations over reusing generic `.vue` UI components unless the component has already been verified on real Android devices. SVG or `image` rendering inside fixed `nvue` overlays can fail even when the same asset works in `.vue` pages.

When adjusting `nvue` fullscreen interactions, preserve the event-receiving structure and layer order whenever possible. Seemingly harmless layout or `z-index` refactors can change gesture hit-testing and break double-tap behavior. Verify `nvue` interaction changes on a real Android device before considering the task complete.

## Testing Guidelines
There is no automated test suite configured in this repository. Do not run full test suites. Validate UI and navigation changes in HBuilderX. For hardware-related work, use the serial test pages under `pages/serial-test/` and document manual verification steps.

## Commit & Pull Request Guidelines
Recent history favors concise, purpose-first commits, commonly with prefixes like `feat:`, `refactor:`, and `docs:`. Keep commits scoped to one change set and use imperative summaries, for example `feat: add action selection dialog`.

PRs should include:
- a short description of the user-facing or technical change
- linked issue or task ID when available
- screenshots or recordings for UI changes
- manual verification notes, especially for serial/device flows
