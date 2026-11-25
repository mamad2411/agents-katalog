---
name: systems-gpui
description: "Native desktop apps in Rust with GPUI, the GPU-accelerated UI framework Zed is built on: setup per platform, the App, Entity, Context and Window model, views with Render and the div() styling API, state updates with notify, events and subscriptions, actions, key bindings and focus, long lists, async work with spawn and background_spawn, structure, testing, and the pitfalls. Read when the project uses gpui or a Rust desktop app is to be built with it."
---

# Desktop apps with GPUI

GPUI is the UI framework the Zed editor is written in: Rust from the state
to the pixels, drawn on the GPU (Metal on macOS, DirectX on Windows,
Vulkan on Linux), keyboard-first, fast with huge lists. It is young and
moves quickly: its API changes between versions, and its documentation is
mostly its source and its examples. Whether to use it at all is decided in
`systems-desktop`; general Rust in `systems-rust`; the look in `ui`.

GPUI written on autopilot calls a state change and nothing redraws (no
`cx.notify()`), drops the `Task` and the work silently stops, drops the
`Subscription` and the event never arrives, keeps an `Entity` in both
directions and leaks the window, blocks the main thread on a file read,
and copies an API from a blog post that the pinned version does not have.

## 1. Pin the version, then read its examples

- Depend on one version and write against that version only. From
  crates.io: `gpui = "0.2"` (check the current release). From git, pin a
  `rev` or `tag` of `zed-industries/zed`; never a moving branch.
- Newer versions split the platform layer into `gpui_platform`. Its
  README's starting point:

  ```toml
  gpui = { version = "*" }
  gpui_platform = { version = "*", features = ["font-kit", "wayland", "x11"] }
  ```

  Replace `*` with the version you pinned. The entry point then is
  `gpui_platform::application().run(...)`; in the 0.2 crate it is
  `Application::new().run(...)`. Use the one your version has.
- The source of truth for an API is `crates/gpui/examples/` at the same
  version: `hello_world`, `input`, `uniform_list`, `scrollable`,
  `focus_visible`, `ownership_post`, `window`, `animation`, `testing` and
  more. Read the relevant one before writing a feature, and when a call
  does not compile, look there, not at memory.

## 2. Platforms

- **macOS**: Xcode and its command line tools (`xcode-select --install`);
  rendering is Metal. With `gpui_platform`, enable `font-kit` for text.
- **Linux**: enable a windowing backend, `wayland`, `x11` or both. The
  build needs the system's development packages (Vulkan, xkbcommon,
  Wayland, X11, fontconfig/freetype); install what the linker asks for and
  list them in the README for the next person.
- **Windows**: no feature needed; Win32 windows, DirectWrite text.
- Build and run on each platform you ship to. A window that works on macOS
  can still miss its font or its backend on Linux.

## 3. The model: App, entities, views, elements

- `App` owns every piece of state. You never hold your state directly: you
  hold an `Entity<T>`, a handle the `App` resolves. `cx.new(|cx| T { .. })`
  creates one.
- A **view** is an entity whose type implements `Render`; its `render`
  returns an element tree, built again each frame it is dirty.
- **Elements** are the low level: `div()`, text, images, `uniform_list`,
  and custom ones when you need total control of layout and painting.
- `Context<T>` is the context while working inside entity `T`: it
  dereferences to `App`, and adds `notify`, `emit`, `listener`, `spawn`.
  `Window` is passed beside it for anything about the window (focus,
  bounds, appearance).
- `AsyncApp` (and `AsyncWindowContext`) is the context you can hold across
  `.await`. Calls through it are fallible: the app or the window may be
  gone by then.

The hello world, as the GPUI site shows it (0.2 entry point):

```rust
use gpui::{
    div, prelude::*, px, rgb, size, App, Application, Bounds, Context, SharedString, Window,
    WindowBounds, WindowOptions,
};

struct HelloWorld {
    text: SharedString,
}

impl Render for HelloWorld {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        div()
            .flex()
            .flex_col()
            .gap_3()
            .bg(rgb(0x505050))
            .size(px(500.0))
            .justify_center()
            .items_center()
            .text_xl()
            .text_color(rgb(0xffffff))
            .child(format!("Hello, {}!", &self.text))
    }
}

fn main() {
    Application::new().run(|cx: &mut App| {
        let bounds = Bounds::centered(None, size(px(500.), px(500.0)), cx);
        cx.open_window(
            WindowOptions {
                window_bounds: Some(WindowBounds::Windowed(bounds)),
                ..Default::default()
            },
            |_, cx| cx.new(|_| HelloWorld { text: "World".into() }),
        )
        .unwrap();
    });
}
```

## 4. State changes and redraws

- Change state through the entity: `entity.update(cx, |state, cx| { ...;
  cx.notify(); })`. Read with `entity.read(cx)`.
- `cx.notify()` marks the entity dirty, so its view renders again and its
  observers run. A change without it does not show. Call it once, after
  the change, not in `render`.
- Typed events: `impl EventEmitter<Change> for Counter {}`, then
  `cx.emit(Change { .. })` inside an update. Others listen with
  `cx.subscribe(&counter, |this, emitter, event, cx| { .. })`; `cx.observe`
  runs on every `notify`.
- `subscribe` and `observe` return a `Subscription`: keep it in the
  subscriber's struct (it stops when dropped), or `.detach()` it when it
  should live as long as both entities.
- From the GPUI examples:

  ```rust
  let counter: Entity<Counter> = cx.new(|_cx| Counter { count: 0 });
  counter.update(cx, |counter, cx| {
      counter.count += 2;
      cx.notify();
      cx.emit(Change { increment: 2 });
  });
  ```

- Ownership runs one way: a parent holds `Entity<Child>`; a child that
  needs its parent holds `WeakEntity<Parent>` (`entity.downgrade()`).
  Strong handles both ways never free.
- Never update an entity from inside its own update: borrow the data you
  need, finish the update, then update the other one.

## 5. Views and styling

- `div()` with Tailwind-like methods: layout (`flex`, `flex_col`, `gap_2`,
  `items_center`, `justify_between`, `size_full`, `w(px(..))`, `p_2`,
  `px_3`), colour (`bg(rgb(0x..))`, `text_color`, `border_1`,
  `border_color`), text (`text_sm`, `text_xl`). Children with `.child(..)`
  and `.children(iter)`.
- Colours and sizes come from one theme struct (a global or an entity),
  never scattered hex literals: the design tokens of `ui`, in Rust.
- An element that is clicked, hovered, scrolled or focused needs an id:
  `div().id("save")`. Scrolling content is an element with an id and
  `overflow_scroll()` (both axes) or `overflow_y_scroll()`.
- Long lists use `uniform_list` (equal-height rows), which renders only
  the rows in view; never a `div` with ten thousand children:

  ```rust
  uniform_list(
      "entries",
      self.items.len(),
      cx.processor(|this, range, _window, _cx| {
          range.map(|ix| div().id(ix).child(this.items[ix].clone())).collect()
      }),
  )
  .h_full()
  ```

- Small pieces with no state of their own are functions returning `impl
  IntoElement` (or types implementing `RenderOnce`), not entities. An
  entity is for something with state and a lifetime.

## 6. Input: clicks, actions, keys, focus

- Clicks: `.on_click(cx.listener(|this, _event, _window, cx| { ..;
  cx.notify(); }))`. `cx.listener` gives the handler `&mut Self`.
- GPUI is keyboard-first: name every command as an action, bind keys to
  it, and handle it where it applies.

  ```rust
  actions!(editor, [Save, Quit]);

  cx.bind_keys([
      KeyBinding::new("cmd-s", Save, None),
      KeyBinding::new("cmd-q", Quit, None),
  ]);
  ```

  Then on the element: `.key_context("editor")` to scope bindings, and
  `.on_action(cx.listener(Self::save))` with `fn save(&mut self, _: &Save,
  window: &mut Window, cx: &mut Context<Self>)`. Bind `cmd-` on macOS and
  `ctrl-` elsewhere (`#[cfg(target_os = "macos")]`), or give both.
- Focus: keep a `FocusHandle` in the view (`cx.focus_handle()`), put it on
  the element with `.track_focus(&self.focus_handle)`, and focus it with
  `window.focus(&handle, ...)` (the arguments differ between versions; see
  the `focus_visible` example). Implement `Focusable` for views that take
  focus. `.focus_visible(|style| ..)` styles keyboard focus only; every
  focusable control shows it.
- Tab order with `tab_index` and `tab_stop` on the handle. Every action
  reachable by keyboard; menus (`set_menus`) for the app's commands.

## 7. Async work

- `cx.spawn(async move |this, cx| { .. })` runs on the main thread's
  executor with a `WeakEntity<Self>` and an `&mut AsyncApp`; come back to
  the state with `this.update(cx, |this, cx| { ..; cx.notify(); })`, which
  fails if the view is gone: handle that, do not unwrap.
- Blocking or CPU-heavy work (file reads, parsing, hashing, network
  clients that block) goes to `cx.background_spawn(async move { .. })`,
  awaited from a `spawn`. The main thread never blocks: a blocked main
  thread is a frozen window.
- Both return a `Task`. Dropping it cancels the work. Store it in the
  struct (replacing it cancels the previous run, which is what a search
  box wants), or `.detach()` it when it must finish on its own.

## 8. Structure

- `main.rs` opens the window; one module per view; state that several
  views share lives in its own entity (or a `Global` for app-wide
  settings), passed as `Entity<T>`.
- Keep domain logic in plain Rust modules with no gpui types, tested with
  ordinary unit tests; views call into it.
- Persist settings and window size in the platform's config directory
  (`dirs`), loaded at start, saved on change.

## 9. Testing

- Domain logic: plain `#[test]`s.
- Views: `#[gpui::test]` tests take a `TestAppContext` (an `async fn`
  test runs on a single-threaded executor). Create entities with
  `cx.new(..)`, change them with `entity.update(cx, ..)`, read with
  `entity.read_with(cx, |e, _| ..)`, and let spawned work finish with
  `cx.run_until_parked()`. `VisualTestContext::from_window` covers what
  depends on rendering. Test behaviour (the action changed the state), not
  pixels; the `testing` example at your version shows each.

## 10. Shipping

- Release builds only (`--release`); a debug build of a GPU UI is slow
  enough to mislead you.
- macOS: an `.app` bundle with an icon and `Info.plist`, signed and
  notarized to open without warnings. Windows: an installer (MSI or
  similar), signed if you can. Linux: an AppImage or Flatpak, with the
  backend features the build needs.
- Say in the README which platforms were built and run, and which were
  not.
