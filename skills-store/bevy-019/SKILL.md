---
name: bevy-019
description: Implement, review, or migrate Rasterra code against Bevy 0.19 specifically. Use for Bevy APIs, feature flags, plugins, ECS, rendering, text, input, scenes, UI, or examples where later or older Bevy syntax could be mistaken for 0.19 behavior.
---

# Work with Bevy 0.19

1. Read `CONTRIBUTING.md` and `docs/plan.md` before changing code.
2. Confirm uncertain APIs in versioned Bevy 0.19 docs or the `v0.19.0` source tag. Do not copy `main` blindly.
3. Prefer the 0.19 scene system for hierarchical construction and `bsn!` for new UI.
4. Keep Bevy types at Rasterra's application, rendering, input, and UI boundaries.
5. Run the narrowest relevant check or example in debug mode.

## Project defaults

- Target `bevy = "0.19"`.
- Enable `bevy_feathers` while Rasterra uses Feathers.
- Add `FeathersPlugins` when using the complete Feathers widget set. Do not confuse it with the lower-level `FeathersCorePlugin`.
- Use the non-experimental 0.19 feature names `bevy_feathers` and `bevy_ui_widgets`.
- Remember that the `ui` feature no longer follows automatically from `2d` or `3d` when selecting features manually.
- Use `EditableText` as the text-entry primitive, but account for its documented missing conveniences before promising editor-grade behavior.
- Consider Bevy's `SettingsPlugin` for persisted panel layout and tool preferences, but keep document state and transient interaction state out of application settings.
- Prefer semantic font sources such as `FontSource::SystemUi` where an editor should follow the host. Enable `system_font_discovery` before relying on installed font families.

## Editor-facing 0.19 APIs

- Feathers 0.19 adds text and number input, dropdown menus, disclosure toggles, icon/label primitives, pane containers, list views, and scrollbars. Check the gallery before creating an equivalent control.
- `EditableText` supports Unicode, IME, selection, clipboard integration, multiline text, filtering, and character limits. It does not yet provide placeholder text, undo/redo, or password masking by itself.
- `FontSize` is an enum in 0.19. Use `FontSize::Px` for fixed editor chrome or `Rem` with a deliberate `RemSize` policy; do not pass a bare `f32` copied from older examples.
- BSN scenes, Feathers widgets, and headless widget events are the preferred construction layers; domain actions and state remain project-owned.
- Keep the root Bevy app module as a thin plugin/composition inventory. Let a
  substantial editor feature register its own resources, observers, and
  systems through a small plugin while keeping its scenes beside that feature.
- Prefer feature modules inside the existing package. Do not derive a Cargo
  workspace layout from large editors until reuse or dependency isolation is
  concrete.

## Guard against adjacent-version examples

- Replace deprecated Feathers bundle constructors with BSN scene components.
- Use the 0.19 names without the former `Core` prefix for UI widget components.
- Check the 0.18-to-0.19 migration guide when adapting older code.
- Treat `.bsn` files as future-facing: 0.19 ships code-driven BSN but no first-party `.bsn` asset loader.
- Treat BSN, Feathers, and headless widgets as evolving APIs. Hide repeated framework details behind project-owned scene functions or components.

## Remote debugging

- Use Bevy 0.19's `RemotePlugin` together with `RemoteHttpPlugin` for the
  standard Bevy Remote Protocol (BRP) transport.
- Keep Rasterra's remote-debug module transport-only. Exercise the same ECS
  components, events, and systems as local UI and input instead of duplicating
  application behavior behind RPC commands.
- Make the server an explicit runtime option, default it to loopback, and warn
  when it is bound to a non-loopback address. BRP can inspect and mutate the
  world and is not an authentication boundary.
- Keep Winit updating while remote debugging is enabled. A desktop application
  parked on an unfocused compositor workspace may otherwise stop advancing the
  ECS world that services requests arriving through BRP's server thread.
- Prefer BRP's built-in discovery, query, mutation, event observation, input,
  and screenshot paths before registering project-specific methods.
- For screenshot automation, begin a global `ScreenshotCaptured` watch before
  spawning the temporary `Screenshot` entity. The capture entity despawns after
  use, so attaching a late entity-specific watch can race its lifetime.
- Follow Bevy's versioned remote integration example when building automation;
  it demonstrates UI discovery, input injection, and screenshot capture through
  BRP without an application-specific test API.

## Headless editor rendering

- Keep headless operation as a second host for the same editor plugins and
  schedules. It is not a second application implementation.
- Remove the primary window, disable [`WinitPlugin`], and install
  [`ScheduleRunnerPlugin`] at a deliberate update rate. `WinitSettings` can
  keep a windowed app updating while unfocused, but it cannot prevent a Wayland
  compositor from throttling or withholding window-surface presentation.
- Render the editor camera to `RenderTarget::Image`. Mark that camera with
  `IsDefaultUiCamera`, or put `UiTargetCamera(camera_entity)` on every root UI
  layout; otherwise the scene can render while the offscreen UI remains absent.
- Capture occasional automation frames with `Screenshot::image(handle)`.
  Do not copy the render target back to the CPU every frame unless the product
  actually needs a continuous image stream.
- Keep mouse, keyboard, and tablet hosts interactive-only. Headless automation
  should inject project actions and normalized pointer samples at the same
  boundaries those adapters use.
- A windowless renderer still needs a GPU adapter. Software adapters are valid
  for correctness and CI but can make visual captures substantially slower.

## Primary references

- [Bevy 0.19 release notes](https://bevy.org/news/bevy-0-19/)
- [Bevy 0.18 to 0.19 migration guide](https://bevy.org/learn/migration-guides/0-18-to-0-19/)
- [Bevy 0.19 API documentation](https://docs.rs/bevy/0.19.0/bevy/)
- [Bevy source at v0.19.0](https://github.com/bevyengine/bevy/tree/v0.19.0)
- [Bevy 0.19 remote integration example](https://github.com/bevyengine/bevy/blob/v0.19.0/examples/remote/integration_test.rs)
