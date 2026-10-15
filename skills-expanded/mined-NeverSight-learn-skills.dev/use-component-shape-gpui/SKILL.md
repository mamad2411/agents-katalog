---
name: use-component-shape-gpui
description: "Add, review, refactor, or document GPUI component shape declarations and runtime contracts. Use for component_shape_gpui::GpuiComponentShape, component_shape_gpui::component_shape!, declared-shape markers, render contracts, configured builders, value compatibility, value binding, inferred or explicit McpInput metadata, and GPUI macro syntax."
---

# Use component shape GPUI

## Route the task

Use this skill for the `component-shape-gpui` public surface. Use
`use-component-shape` for framework-neutral metadata and
`use-component-shape-mcp` for typed schemas, decoding, tools, servers, and
stdio. Use a downstream integration skill when a form or table framework is
consuming an existing shape.

Inside this repository, read `AGENTS.md` first. Keep public runtime contracts
in `crates/component-shape-gpui`, macro implementation in
`crates/component-shape-gpui-macros`, compile contracts in
`crates/component-shape-gpui/tests/ui`, and user guidance in
`book/src/gpui-shapes.md`.

## Choose a declaration form

- Derive `GpuiComponentShape` when the crate owns the rendered component and
  backing state.
- Use `component_shape!` when wrapping state or components owned by another
  crate.
- Reuse an existing shape instead of declaring another wrapper when its public
  contracts already fit.

For an owned component:

```rust
#[derive(component_shape_gpui::GpuiComponentShape)]
#[gpui_component_shape(value = String, field_suffix = "input")]
pub struct TextInput;

pub struct TextInputState;
```

The derive infers `TextInputState`. Set `state = path::State` for another
name, and set `new = ...` when construction should not call
`State::new(window, cx)`. The rendered component must provide the constructor
selected by the render contract.

For external types:

```rust
component_shape_gpui::component_shape! {
    pub struct EmailInputShape {
        state = gpui_component::input::InputState;
        component = gpui_component::input::Input;
        value = String;
        field_suffix = "input";
    }
}
```

Omit `component = ...` for metadata-only shapes.

## Publish value behavior

- Add `value = T` or `values(...)` for explicit compatibility.
- Add `value_binding` to delegate through
  `GpuiComponentStateValueBinding<T>`.
- Put `GpuiComponentValueBinding<T>` inside `component_shape!` when the
  wrapper owns binding behavior.
- Implement both `ComponentShapeFor<T>` and `GpuiComponentShapeFor<T>` for a
  hand-written compatibility pair.
- Keep storage policy in the consuming framework.

The macros emit `DeclaredGpuiComponentShape` and `DeclaredComponentShape`.
Require those markers only when a consumer intentionally accepts macro-declared
shapes.

## Handle construction and metadata

Use `GpuiComponentShapeBuilder<Shape>` for field-site configuration and
`DefaultGpuiComponentShapeBuilder<Shape>` for the normal constructor. Dispatch
both through `build_component_shape`.

Use `field_suffix = "..."` for stable generated identifiers. Prefer semantic
ASCII suffixes such as `"input"`, `"select"`, or `"picker"`.

Let common Rust values infer coarse `McpInput` metadata. Set
`mcp_input = ...` for a known custom coarse form. Use typed MCP contracts for
richer wire schemas.

## Coordinate changes

Update public rustdoc and focused trybuild fixtures when macro syntax,
generated implementations, trait requirements, or diagnostics change. Update
`.stderr` fixtures only for intentional diagnostics. Keep the GPUI book
chapter and this skill aligned with public behavior; do not duplicate downstream
form or table rules here.
