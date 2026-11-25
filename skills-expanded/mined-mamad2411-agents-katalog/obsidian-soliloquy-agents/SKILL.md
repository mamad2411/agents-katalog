# Soliloquy development guide

## Project and structure

Soliloquy is an Obsidian timeline journal. Posts and replies remain Markdown in daily notes. The plugin supports desktop and mobile and does not require a network service.

- `src/main.ts`: plugin lifecycle, commands, settings persistence, and vault events.
- `src/services/`: daily-note paths, Markdown parsing and safe updates, caching, reply/search indexing, and settings coordination.
- `src/ui/`: shared timeline panel, inline edit/reply controller, CodeMirror/Vim input, cards, keyboard routing, and view/modal hosts.
- `src/settings.ts` and `src/types.ts`: settings UI/defaults and shared post types.
- `tests/`: Node tests, including real CodeMirror/Vim in jsdom and mocked Obsidian hosts.
- `scripts/`: version validation and performance fixtures/benchmarks. See `PERFORMANCE.md` for measurement details.

## Tools and checks

Use Node.js 24 and npm. Supported Node.js ranges are `^20.19.0 || ^22.13.0 || >=24`; keep `package.json`, its lockfile, README, and CI consistent.

```bash
npm ci
npm run dev
```

Run the relevant regression tests while editing, then complete these checks:

```bash
npm test
npm run lint
npm run build
npm run validate:version
```

CI runs tests, lint, and build on Node.js 20, 22, and 24. The production build writes `main.js` in the plugin root. Reload Obsidian to test the installed plugin; describe any host or mobile behavior that was not verified.

## Implementation rules

- Keep TypeScript strict and `main.ts` focused on lifecycle and registration. Split feature responsibilities into focused modules and keep view/modal behavior shared.
- Preserve stable plugin and command IDs. Keep `minAppVersion` accurate when adding Obsidian APIs.
- Use `loadData`/`saveData` for persistence and the existing settings coordinator for coalesced, serialized saves. Validate user-entered settings.
- Preserve daily-note line endings, unrelated Markdown, block IDs, and reply links. Resolve edits against the current file and reject ambiguous or changed posts rather than overwriting them.
- Preserve input text, selection, undo history, Vim state, and focus across supported mode changes. Background refreshes must preserve open drafts; pending saves must not discard newer input or affect a closed display.
- Own listeners, timers, CodeMirror instances, and Markdown render components through the component lifecycle. Clean them up on close/unload.
- Keep startup light, cache parsed notes, invalidate affected paths, debounce refresh/search, and retain paged timeline rendering.
- Use browser-compatible runtime code for mobile. Bundle dependencies unless Obsidian provides them through the externals in `esbuild.config.mjs`.
- Use short, sentence-case UI text. Keep README usage, shortcuts, settings, and release instructions aligned with the implementation.

## Files and releases

- Do not commit `main.js`, source maps, `node_modules/`, `data.json`, or `.performance-vault/`. Do not leave temporary notes, fixtures, or reports in the repository.
- Keep regression tests and their used harnesses. Generate a synthetic vault with `npm run benchmark:generate` and measure it with `npm run benchmark`; the generator refuses to overwrite an existing directory.
- Release artifacts are `main.js`, `manifest.json`, and `styles.css` at the plugin root.
- Use `npm version patch|minor|major`, then verify `package.json`, `package-lock.json`, `manifest.json`, and `versions.json` agree with `npm run validate:version -- <version>`.
- Tags must match the version exactly, without a `v` prefix (`.npmrc` configures this).
- The release workflow validates, tests, lints, builds, and creates a draft GitHub release. Review the attached assets and publish the draft manually.

## Privacy and safety

Keep plugin operation local to the vault and limit reads/writes to the feature's needs. Do not add telemetry, remote code execution, or automatic plugin updates. Any new external service must have a clear user-facing purpose, explicit opt-in, and documentation of the data sent. Follow Obsidian's [developer policies](https://docs.obsidian.md/Developer+policies) and [plugin guidelines](https://docs.obsidian.md/Plugins/Releasing/Plugin+guidelines).
