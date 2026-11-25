# UI project structure for Rasterra

Use this reference when splitting `src/app.rs`, adding an editor panel, or
deciding whether UI code belongs in a shared widget module. It records an audit
performed on 2026-07-12; verify upstream layouts again before treating file
names as current APIs.

## Evidence from existing applications

### Jackdaw

The local Jackdaw checkout at `48c9891aa7be` targets Bevy 0.19. Its root
editor plugin is a composition point for feature plugins. The application shell
is in `layout.rs`; coherent features such as `inspector/`, `prefab/`, `remote/`,
and `terrain/` own their UI, state adapters, observers, and systems together.
Only broadly reusable editor machinery is separated into packages such as
`jackdaw_widgets`, `jackdaw_feathers`, and `jackdaw_panels`.

The useful pattern is feature ownership plus plugin composition. Do not copy
Jackdaw's current number of top-level files or workspace crates: those reflect
an extensible general-purpose editor, multiplayer/runtime boundaries, and years
of feature growth that Rasterra does not yet have.

### Bevy Feathers and headless widgets

Bevy's reusable UI libraries organize by technical role because they are design
systems, not application features:

```text
bevy_feathers: containers / controls / display / theme / tokens
bevy_ui_widgets: one behavior module and plugin per headless control
```

This is the right model for `app/ui/widgets/` only after Rasterra has genuinely
reusable controls. It is not the right top-level organization for brush
browsing, canvas interaction, layers, or document workflows.

### Zed, Lapce, and Rerun

- Zed separates its reusable `ui` crate (`components`, `styles`, `traits`, and
  utilities) from its `workspace` feature, which owns panes, docks, modal
  layers, status bars, toolbars, persistence, and workspace behavior.
- Lapce keeps its application UI in `lapce-app`, organized into feature modules
  such as editor, file explorer, palette, panel, settings, source control,
  terminal, window, and workspace. It extracts core editing, proxy, and RPC
  packages where dependency or process boundaries are real.
- Rerun keeps the viewer composition in `re_viewer` (`app`, `app_state`, `ui`,
  loading, saving, navigation) and gives large panels and view types their own
  packages. Its architecture explicitly distinguishes UI features, UI support,
  viewer context, rendering, and the application data store.

These are much larger products, but they reinforce two rules: organize product
behavior by feature, and extract a package only for demonstrated reuse,
dependency isolation, compilation isolation, or a separate runtime boundary.

Primary upstream references:

- [Jackdaw repository](https://github.com/jbuehler23/jackdaw)
- [Zed UI primitives](https://github.com/zed-industries/zed/tree/main/crates/ui/src)
- [Zed workspace feature](https://github.com/zed-industries/zed/tree/main/crates/workspace/src)
- [Lapce application package](https://github.com/lapce/lapce/tree/master/lapce-app)
- [Rerun architecture](https://github.com/rerun-io/rerun/blob/main/ARCHITECTURE.md)
- [Rerun viewer composition](https://github.com/rerun-io/rerun/tree/main/crates/viewer/re_viewer/src)

## Rasterra target

Keep one Cargo package. As the proof of concept grows, move toward:

```text
src/app/
├── mod.rs             # run(), app/plugin composition, bootstrap only
├── actions.rs         # project-owned user intents shared by UI/keys/tablet
├── shell.rs           # top-level editor scene and panel placement
├── canvas.rs          # canvas scene, capture/router, image upload
├── brush_browser.rs   # catalog UI, selection adapter, preview loading
├── tablet.rs          # octotablet host adapter and diagnostics
├── screenshot.rs      # visual harness and capture lifecycle
└── ui/
    ├── mod.rs         # shared UI plugin, if registration is needed
    ├── theme.rs       # Feathers theme extensions and layout metrics
    └── widgets/       # only controls reused by multiple features
```

This is a direction, not a request to create empty files. Keep a feature in one
file until it has two or more distinct internal responsibilities. Turn
`brush_browser.rs` into `brush_browser/` only when, for example, catalog
adaptation, scenes, and interaction systems are independently substantial.

## Ownership rules

1. Keep scene functions, marker components, observers, synchronization systems,
   and UI-only adapter state with the feature that owns the workflow.
2. Keep `shell.rs` declarative: compose feature scenes and define major panel
   placement; do not put brush selection or canvas painting behavior there.
3. Put only cross-feature visual foundations in `app/ui`: theme construction,
   restrained layout metrics, and genuinely reused project widgets.
4. Translate `Activate`, `ValueChange<T>`, shortcuts, and tablet controls into
   project-owned actions. Do not let domain systems query Feathers markers.
5. Let each substantial feature expose a small `Plugin` or `fn plugin(&mut App)`
   that registers its resources, observers, and systems. Keep the root app
   module as the readable inventory and ordering point.
6. Keep Bevy-independent state and algorithms in the existing library modules.
   Application feature modules adapt that state; they do not become a second
   domain model.
7. Avoid a broad application prelude. Explicit imports make cross-feature
   dependencies and accidental cycles visible.
8. Extract a crate only when independent dependencies, reuse, compilation, or a
   process/release boundary pays for the extra workspace complexity.

## Review questions

- Can the feature be found by the user-facing concept that owns it?
- Does the module own both its scene and the systems that keep it synchronized?
- Is shared UI code reused by at least two features, or is it speculative?
- Does the root app module explain plugin order without implementing features?
- Can feature behavior be tested through actions and state without rendering?
- Would a proposed crate have a dependency boundary that a Rust module cannot
  express adequately?
