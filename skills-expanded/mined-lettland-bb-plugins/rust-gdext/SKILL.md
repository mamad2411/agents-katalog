---
name: rust-gdext
description: Use when binding Rust to Godot via gdext (godot-rust v4) — GodotClass derive, signals, exports, init/process/physics, build pipeline.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: language
  languages: [rust]
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [rust-essentials, rust-testing, godot, gdscript]
---

# Rust + Godot via `gdext`

**Iron Law: `Gd<T>` is the ownership boundary. Never store a raw `&Node`/`&T` across an `await`, frame, or callback — Godot owns the lifecycle, not Rust. Panics across the FFI boundary become Godot errors; don't rely on `unwrap` for control flow.**

**Versions:** Current `gdext 0.4.x` against Godot `4.5` / `4.6` — _No LTS series; `godot` crate tracks Godot minor releases. Each `gdext` release pins a `compatibility_minimum` Godot version; mismatched `.gdextension` manifests refuse to load silently. MSRV currently Rust `1.87`._

## Cargo project shape

```
mygame-rust/
├── Cargo.toml
├── src/lib.rs
└── ../godot-project/
    ├── mygame.gdextension     # manifest pointing at target/{debug,release}/
    └── ...
```

`Cargo.toml`:

```toml
[package]
name    = "mygame_rust"
edition = "2024"

[lib]
crate-type = ["cdylib"]        # required — Godot dlopens the shared library

[dependencies]
godot = { version = "0.4", features = ["api-4-5"] }
```

`crate-type = ["cdylib"]` is non-negotiable. Add `"rlib"` only if you also want to consume the crate from integration tests.

`src/lib.rs` entry:

```rust
use godot::prelude::*;

struct MyExtension;

#[gdextension]
unsafe impl ExtensionLibrary for MyExtension {}
```

`#[gdextension]` is the **single** entry point. Multiple `ExtensionLibrary` impls per cdylib will not compile.

## Defining a class

```rust
use godot::classes::{INode3D, Node3D};
use godot::prelude::*;

#[derive(GodotClass)]
#[class(base = Node3D, init)]      // `init` synthesises a default `init()`
pub struct Player {
    #[export] speed: f32,
    #[export] max_hp: i32,

    #[var(get)] current_hp: i32,    // exposed read-only to GDScript

    base: Base<Node3D>,             // mandatory if you derive INode3D below
}
```

- `#[class(base = X)]` chooses the Godot parent. `Node`, `Node2D`, `Node3D`, `Control`, `Resource`, `RefCounted` are the common ones.
- `#[class(init)]` generates a `Default`-like constructor — drop it if your fields can't be defaulted; then implement `INodeXXX::init` yourself.
- `#[export]` puts the field in the inspector. `#[var]` exposes it to GDScript without inspector UI.
- The `base: Base<T>` field is how you call into the parent. Don't store a `Gd<T>` of self — that creates a cycle.

## Lifecycle hooks

```rust
#[godot_api]
impl INode3D for Player {
    fn init(base: Base<Node3D>) -> Self {
        Self { speed: 5.0, max_hp: 100, current_hp: 100, base }
    }

    fn ready(&mut self) {
        // Tree is now wired; children exist; safe to query them.
    }

    fn process(&mut self, delta: f64) {
        // Per-frame, variable timestep. Visuals, input polling.
    }

    fn physics_process(&mut self, delta: f64) {
        // Fixed step (60 Hz default). All movement + collision queries go here.
    }
}
```

Don't compute physics in `process` — it ties simulation speed to frame rate. Don't poll the scene tree in `init` — siblings aren't there yet.

## Methods exposed to GDScript

```rust
#[godot_api]
impl Player {
    #[func]
    fn take_damage(&mut self, amount: i32, source: Gd<Node>) {
        self.current_hp = (self.current_hp - amount).max(0);
        self.signals().damaged().emit(amount, &source);
        if self.current_hp == 0 {
            self.signals().died().emit();
        }
    }

    #[signal]
    fn damaged(amount: i32, source: Gd<Node>);

    #[signal]
    fn died();
}
```

- `#[func]` exports to GDScript / editor. Accept owned `GString`, `Gd<T>`, primitives — not `&str`.
- `#[signal]` declarations get typed emit/connect on `signals()` (gdext 0.4 named signals — type-checked at compile time, the killer feature versus raw `emit_signal`).
- Past-tense names (`damaged`, `died`); pass context as params — mirrors GDScript discipline.

## Calling into the base (`self.base()`)

```rust
fn move_forward(&mut self, delta: f64) {
    let forward = -self.base().get_transform().basis.col_c(); // -Z forward
    self.base_mut().translate(forward * self.speed * delta as f32);
}
```

`base()` / `base_mut()` return access to the parent node. Acquire late, drop early — never hold across an `await` or callback or you'll deadlock the borrow checker.

## `Gd<T>` — the smart pointer for Godot objects

```rust
let enemy: Gd<Enemy> = self.base().get_node_as::<Enemy>("Enemy");
enemy.bind().some_read_only_query();                        // shared borrow
enemy.bind_mut().take_damage(5, self.to_gd().upcast());     // exclusive borrow
```

| Operation                    | Cost / risk                                                                            |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| Clone `Gd<T>`                | Cheap ref-count bump; use freely                                                       |
| `bind()` / `bind_mut()`      | Runtime borrow check; reentry panics. `try_bind*()` for fallible variants in hot paths |
| `instance_id()`              | Stable handle; safe across frames. Resolve via `Gd::from_instance_id`                  |
| Storing `Gd<Node>` long-term | `Node` is NOT ref-counted — dangles on free. `is_instance_valid()` first               |

`RefCounted`-derived types are ref-counted; `Node`-derived are not. Prefer storing `instance_id` for long-lived scene-tree references.

## Error handling across the FFI

Panics inside `#[func]` are caught by gdext and surface as Godot errors — _but they unwind and leave half-mutated state_. Prefer `Result` + `godot_error!` + a sentinel return. GDScript can't pattern-match a `Result`; return `Variant::nil()` on failure, or model success/error as separate signals. Reserve `expect("invariant: ...")` for truly impossible branches.

```rust
#[func]
fn load_config(&self, path: GString) -> Variant {
    match std::fs::read_to_string(path.to_string()) {
        Ok(s)  => s.to_variant(),
        Err(e) => { godot_error!("load_config: {}", e); Variant::nil() }
    }
}
```

## When to write Rust vs GDScript

| Reach for Rust                                       | Stay in GDScript              |
| ---------------------------------------------------- | ----------------------------- |
| Pathfinding, procgen, physics queries in tight loops | Editor tooling, UI glue       |
| Heavy math (mesh ops, ECS, AI)                       | Signal wiring, state machines |
| Reusing a Rust crate (serde, image, RNG)             | Designer-tweaked behaviour    |
| Determinism — fixed-seed simulation                  | Prototyping a mechanic        |

Typing across the boundary is friction. Don't port 50-line gameplay scripts because "it's faster" — measure first. The win shows up in 10k-particle simulations and pathfinding grids, not in `if hp <= 0: die()`.

## Build & workflow

`cargo build` (debug → `target/debug/lib…`) / `cargo build --release` (`target/release/`). The `.gdextension` manifest references both — Godot picks based on editor vs export build. Hot-reload: rebuild → Godot detects mtime change → reloads. Lifecycle and manifest details: `Skill(godot)`.

Typical flow: sketch in GDScript → move the hot loop to Rust once it's measurable (Godot profiler, then `cargo flamegraph`) → keep the `#[func]`/`#[signal]` surface small → `cargo clippy -- -D warnings` + `cargo fmt` before commit.

## Anti-patterns

- Holding `&mut self` across `base().call_deferred(...)` — borrow checker says no for good reason.
- `.bind_mut()` on a `Gd` whose access pattern you don't own — panic on reentry.
- `unwrap()` on `try_get_node_as::<T>` — node names are stringly typed; fail loudly with `expect("…")`.
- Storing `Gd<Node>` long-term without `is_instance_valid()` — silent dangling-reference crashes.
- Multiple `#[gdextension]` impls in one crate, mixing `gdnative` (v3) with `gdext`, `Box<dyn Trait>` as a `#[func]` parameter, re-exporting `godot::prelude::*` from your modules — all break in different ways.

## Hand-off

For the Rust language baseline (ownership, errors, Cargo): `Skill(rust-essentials)`. For unit + integration tests in the Rust crate (gdext code is hard to test in-engine; pure Rust modules are not): `Skill(rust-testing)`. For Godot scene/signal architecture the Rust code plugs into: `Skill(godot)`. For packaging, cross-compiling, and the `.gdextension` manifest: `Skill(godot)`. For the GDScript side of the boundary: `Skill(gdscript)`.
