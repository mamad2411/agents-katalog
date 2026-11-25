---
name: bevy-bsn-ui
description: Author or refactor Rasterra's Bevy 0.19 scenes and UI with `bsn!`, `bsn_list!`, scene functions, patches, relationships, observers, and `SceneComponent` props. Use whenever creating UI hierarchies, reusable UI composition, or replacing imperative entity spawning.
---

# Author UI with BSN

Read `CONTRIBUTING.md` and use the versioned Bevy 0.19 scene documentation.

## Workflow

1. Express one conceptual entity as `fn name(...) -> impl Scene` using `bsn!`.
2. Express sibling roots as `impl SceneList` using `bsn_list!`.
3. Compose hierarchy inline with `Children [...]`; use parentheses when an entity has multiple entries and boundaries would otherwise be unclear.
4. Parameterize ordinary scene functions first. Derive `SceneComponent` when the reusable scene is a project-owned conceptual widget or needs named props.
5. Attach behavior declaratively with `on(...)` observers and keep domain state outside the scene.
6. Spawn startup roots with `scene.spawn()` or use `spawn_scene` / `queue_spawn_scene` as appropriate.

## Syntax and composition rules

- Omit fields that should retain defaults. BSN entries are ordered patches, not full struct replacement.
- Use `{expression}` where arbitrary Rust or a dynamic scene/list must be embedded.
- Use `#Name` only for scoped entity naming and references inside one macro invocation.
- Use `@Widget` to instantiate a `SceneComponent`; use `@prop` for its immediate, non-patchable props.
- Apply call-site component patches after a composed scene to customize layout or appearance without cloning the template.
- Use `Children [{children}]` to accept an `impl SceneList` slot in a reusable container.
- Keep conditionals in Rust before the macro when possible. BSN 0.19 has no native `if` or `match` syntax.
- Build runtime-length homogeneous children as a `Vec<S>` where `S: Scene`, or heterogeneous children as `Vec<Box<dyn SceneList>>`, then interpolate the list. Do not generate a giant macro for brush catalogs or other data-driven collections.
- Remember that `Scene` and `SceneList` are `Send + Sync + 'static`. Pass owned strings, handles, IDs, or copied values into returned scenes instead of capturing borrowed catalog entries.
- Keep each `#Name` reference inside the `bsn!` invocation that declares it. Composed scene functions and `SceneComponent`s introduce their own name scopes.
- Avoid scene caching until profiling identifies repeated resolution cost and its semantics are understood.

## UI pattern

```rust
fn tool_button(label: &str) -> impl Scene {
    bsn! {
        @FeathersButton {
            @caption: bsn! { Text(label) ThemedText }
        }
        AccessibleLabel(label)
        on(|_activate: On<Activate>| {
            // Send a domain action or update authoritative state.
        })
    }
}
```

Prefer small scene functions like this over one giant screen macro. Let the caller patch `Node`, marker components, observers, or visual variants.

Keep a scene function with the application feature that owns its state and
behavior. Let the editor shell compose `brush_browser`, `canvas`, and future
feature scenes; do not move every scene into a technical `scenes` or `ui`
module. Reserve `app/ui/widgets` for project controls reused across features.

For a data-driven list, convert domain entries into owned scene values at the UI boundary:

```rust
fn brush_tiles(brushes: impl IntoIterator<Item = BrushTileProps>) -> impl SceneList {
    brushes
        .into_iter()
        .map(brush_tile)
        .collect::<Vec<_>>()
}
```

Keep catalog parsing and selection state outside this function; its job is only scene composition.

## Review checklist

- Verify every interactive control has an accessible label.
- Verify emitted events update authoritative state rather than relying on incidental visuals.
- Verify scene functions do not capture short-lived references that violate their returned type's lifetime.
- Verify examples use 0.19 `@SceneComponent` syntax, not unreleased or older preview syntax.
- Run formatting and a targeted compile/test.

## Primary references

- [Bevy 0.19 BSN overview](https://bevy.org/news/bevy-0-19/#next-generation-scenes)
- [Bevy Scene 0.19 syntax and concepts](https://docs.rs/bevy_scene/0.19.0/bevy_scene/)
- [Bevy 0.19 BSN example](https://github.com/bevyengine/bevy/blob/v0.19.0/examples/scene/bsn.rs)
- [Bevy 0.19 Feathers gallery](https://bevy.org/examples/ui-user-interface/feathers-gallery/)
