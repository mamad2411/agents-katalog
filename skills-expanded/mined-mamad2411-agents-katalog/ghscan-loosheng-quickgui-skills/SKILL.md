# Task: maintain the `quickgui` agent skill

You maintain `skills/quickgui/` in this repository: an agent skill that teaches coding agents how to build desktop applications with QuickGUI (Go, TypeScript, Rust). The runtime header above this prompt gives you:

- `UPSTREAM_DIR`: a checkout of `egoist/quickgui` at `TAG` (read-only source of truth).
- `MODE`: `full` (write the skill from scratch) or `incremental` (update it from `PREV_TAG` to `TAG`).
- `CONTEXT_FILE`: release notes, changed-file list, and CHANGELOG excerpt for this sync.
- `DIFF_FILE` (incremental only): the upstream diff of user-facing sources between `PREV_TAG` and `TAG`.

## Hard rules

- Only create, edit, or delete files under `skills/`. Do not touch anything else in this repository.
- Do not run `git`, `gh`, or any command that commits, pushes, or talks to GitHub. A later CI step handles publishing.
- Do not modify `UPSTREAM_DIR`.
- Every API, function, component, prop, option, CLI flag, and code example must exist in upstream at `TAG`. Verify names against the source (`UPSTREAM_DIR/go/ui`, `UPSTREAM_DIR/go/native`, `UPSTREAM_DIR/packages/solid`, `UPSTREAM_DIR/packages/native`, `UPSTREAM_DIR/packages/cli`, `UPSTREAM_DIR/src`, `UPSTREAM_DIR/examples`). Never invent APIs. If unsure, omit it.
- Document only the current API surface. Do not describe removed APIs, migrations, or history.
- Write in English. Be concise and concrete: rules, idioms, and short runnable snippets beat prose.

## Sources of truth (in priority order)

1. `UPSTREAM_DIR/AGENTS.md`: architecture constraints that applications must respect.
2. `UPSTREAM_DIR/website/src/content/docs/{go,typescript,rust}/en/*.mdx`: user guides (ignore `ja/` and `zh/`).
3. `UPSTREAM_DIR/website/src/content/docs/{go,typescript,rust}/components/**`: component reference (ignore `ja/` and `zh/`).
4. `UPSTREAM_DIR/examples/`: working applications; prefer snippets that mirror these.
5. `UPSTREAM_DIR/docs/*.md`: feature notes (skip `docs/architecture/`, `docs/releasing.md`, and roadmap/status pages unless they state user-facing constraints).
6. `UPSTREAM_DIR/packages/cli`: `@quickgui/cli` commands and project templates.

## Skill layout

```text
skills/quickgui/
  SKILL.md
  references/
    getting-started.md      # prerequisites, `bunx @quickgui/cli init`, CLI commands, project structure, run/build
    go.md                   # Go idioms: ui/native/reactive packages, element construction, returning *ui.Element, formatting
    typescript.md           # TypeScript idioms: Bun + Solid 2 JSX, worker model, style prop rules
    rust.md                 # Rust idioms: quickgui crate, builders, parts, cargo workflow
    components.md           # component catalog with per-language names, compound parts, key props/events
    styling.md              # style builders, layout (flex/grid), typography, paint, container queries
    reactivity.md           # signals/state/effects per language, retained bindings, async data
    routing.md
    forms-and-input.md      # inputs, fields, selection controls, keyboard/mouse/gesture input, focus
    overlays-and-dialogs.md # popovers, menus, tooltips, dialogs, toasts, context menus
    animations.md
    rendering.md            # images, SVG, shaders, graphics, performance guidance for apps
    native-services.md      # windows, menubar, tray, clipboard, file dialogs, notifications, system APIs
    resources.md            # app icon, bundled resources, assets and fonts
    extensions.md           # native extensions and first-party extensions (editor, markdown, terminal, updater)
    swift-ui.md             # SwiftUI components and hosting (macOS)
    updater.md
    testing.md              # testing QuickGUI apps
```

This is the starting module list. Add, merge, split, or remove reference files when upstream structure changes, but keep `SKILL.md`'s index in sync and keep every file focused on one module.

### `SKILL.md` requirements

- YAML frontmatter exactly in this shape:

  ```yaml
  ---
  name: quickgui
  description: <one or two sentences: what QuickGUI is and when to use this skill; mention Go, TypeScript, Rust, native desktop GUI, GPU-rendered, no webview>
  metadata:
    upstream-version: <TAG>
  ---
  ```

- Under 500 lines. Sections:
  1. What QuickGUI is and its current status (experimental; platform support).
  2. When to use this skill.
  3. Choosing a language, with a minimal "hello window" example for each of Go, TypeScript, and Rust.
  4. Core rules every agent must follow (distilled from `AGENTS.md` and the guides): e.g. no CGO or IPC bridges in Go, containers start empty and use `.Child(...)`/`.Children(...)`, Go components return `*ui.Element`, TypeScript styles only through the `style` prop with camelCase keys, and so on.
  5. Common workflows: create a project, run in development, build, format/check.
  6. Reference index: a table or list linking every file in `references/` with a one-line "read when..." hint. Use relative links such as `[components](references/components.md)`.

### Reference file requirements

- Start each file with a `#` title and a one-paragraph scope statement.
- When an API differs by language, show all three languages side by side (Go, TypeScript, Rust subsections or tabbed code blocks). Mark features that are unavailable or macOS-only.
- Include a "Pitfalls" section when upstream docs or `AGENTS.md` call out constraints.
- Keep each file under roughly 400 lines; split if it grows beyond that.
- Only link to files that exist. Link to upstream pages with absolute URLs of the form `https://github.com/egoist/quickgui/blob/<TAG>/<path>`.

## Procedure

### `MODE=full`

1. Read `CONTEXT_FILE`, `AGENTS.md`, the `en` guides for all three languages, and the component reference.
2. Skim `examples/` to confirm idioms (e.g. `examples/counter`, `examples/counter-typescript`, `examples/*.rs`).
3. Write every reference file, then `SKILL.md`.
4. Re-verify each code snippet's identifiers against upstream source.

### `MODE=incremental`

1. Read `CONTEXT_FILE` and `DIFF_FILE` to identify user-facing changes (new, renamed, or removed APIs, components, CLI flags, behavior).
2. Map each change to the affected reference files and update them. Remove documentation for anything that was deleted or renamed.
3. Add new reference files for genuinely new modules and index them in `SKILL.md`.
4. Update `metadata.upstream-version` in `SKILL.md` to `TAG`.
5. If nothing user-facing changed, only bump `metadata.upstream-version`.

## Final self-check

Before finishing, confirm:

- `skills/quickgui/SKILL.md` has valid frontmatter with `name: quickgui` and the correct `upstream-version`.
- Every relative link in `SKILL.md` and `references/` resolves to an existing file.
- No file outside `skills/` was changed.

End with a short summary of what you changed and why.
