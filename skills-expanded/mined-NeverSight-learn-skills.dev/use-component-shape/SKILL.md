---
name: use-component-shape
description: "Add, review, refactor, or document framework-neutral component-shape metadata and generator contracts. Use for ComponentShapeMetadata, ComponentShapeFor, DeclaredComponentShape, ComponentShapeUse, capabilities, prototyping suffixes, Rust syntax wrappers, McpInput metadata, ValueChange, or shared code-generation behavior; route GPUI declarations and typed MCP integrations to their dedicated skills."
---

# Use component shape

## Route the task

Keep a contract in `component-shape` when it does not require a UI framework
or protocol runtime. Use `use-component-shape-gpui` for GPUI declarations,
rendering, builders, or value binding. Use `use-component-shape-mcp` for typed
JSON Schema, decoding, tools, servers, resources, prompts, or stdio.

Inside this repository, read `AGENTS.md` before editing. The owning surfaces
are:

- `crates/component-shape` for public framework-neutral contracts.
- `crates/component-shape-codegen` for shared token generation and path,
  suffix, syntax, or MCP metadata normalization.
- `book/src/framework-neutral-shapes.md` for user guidance.
- `crates/component-shape/src/lib.rs` and public rustdoc for the API contract.

## Choose the public contract

- Implement `ComponentShapeMetadata` for shape-owned `PROTOTYPING`,
  `CAPABILITIES`, and coarse `MCP_INPUT`.
- Implement `ComponentShapeFor<Value>` for each supported value. Override its
  `MCP_INPUT` only when the pair differs from the shape-level metadata.
- Require `DeclaredComponentShape` only for shapes emitted by a
  backend-approved declaration surface.
- Use `ComponentFieldName` and `ComponentShapeUse` to record a selected
  source field and shape path for generators.
- Use `ComponentSuffix` for stable, non-empty ASCII identifier suffixes.
- Use `RustPath`, `RustType`, and `RustExpr` to preserve validated Rust
  syntax.
- Normalize framework events into `ValueChange::Unchanged`,
  `ValueChange::Set`, or `ValueChange::Clear`.

Keep framework types out of this crate. Prefer generic capability metadata over
framework-specific branching.

## Handle coarse MCP metadata

Use `McpInput` for common scalar, collection, object, and range shapes. Leave
`McpInput::unsupported()` when a shape should not advertise model input. Use
`McpInput::any()` only for intentionally arbitrary JSON.

Keep precise schemas, strict JSON decoding, authorization, handler policy, and
transport in `component-shape-mcp` or the consuming application.

## Coordinate changes

When shared semantics change:

1. Update the framework-neutral definition and rustdoc.
2. Update `component-shape-codegen` only when token generation,
   normalization, imports, suffixes, or emitted metadata change.
3. Update framework macro fixtures only when their public syntax, generated
   contract, or diagnostics change.
4. Update the framework-neutral book chapter and affected downstream skills
   when the user workflow changes.

Keep parser internals and design rationale in focused code documentation or
tests rather than user-facing READMEs.
