---
name: conventions-code-rust
description: Load when coding in Rust.
---

# Rust Code Conventions

### Linting

- Use `cargo clippy` to check files.
- Avoid adding lint allows (`#[allow(dead_code)]`) to ignore warnings. Favor using `#[expect(dead_code)]` instead.

### Module Organization

- Prefer private modules (`mod foo;`) with explicitly re-exported public API via `pub use` in `mod.rs`.

### Module Size

- Target modules under 500 LoC (excluding tests).
- If a file exceeds roughly 800 LoC, add new functionality in a new module instead of extending the existing file. Make an exception only when there is a strong documented reason not to.
- When extracting code from a large module,
  - Move the related tests and module/type docs toward the new implementation so the invariants stay close to the code that owns them.
  - Do not extract just tests from a large module into a new file. Keep the tests with the code they are testing.
- Do not create logic/structs in `mod.rs` files. Favor creating a new file within the same module to keep `mod.rs` clean.

### Error Handling

- Use `thiserror` for domain-specific error enums. Use `anyhow` for propagation in application code.
- Derive `Error` and `Debug` on error enums. Use `#[from]` for automatic conversions where appropriate.

### Match Statements

- Make match statements exhaustive. Avoid wildcard (`_`) arms unless the set of variants is genuinely open-ended.

### Comments

- Add short doc comments (`///`) to public `fn` and `struct` declarations. Keep the comments concise and developer optimized.
- Do not add doc comments to private internals unless the logic is non-obvious.
- Inline comments are only for non-obvious reasoning (e.g. `// SAFETY:` blocks).

### Visibility

Treat each module as a unit of encapsulation with a graduated visibility model:

- `pub` for items that are part of a module's interface. The parent `mod.rs`
  decides whether they escape the directory via selective `pub use`. `pub` in a
  leaf does NOT mean "crate public API." It means "available for the parent to
  re-export or for siblings within the crate to use."
- `pub(crate)` for items that must cross module boundaries within the crate
  but are not part of the crate's external API (e.g., constructors like `fn new`
  called by a parent module).
- private for implementation internals: struct fields, helpers used only within
  the defining module and its descendant modules.

Treat `mod.rs` (and ultimately `lib.rs`) as a router: it declares child modules
as private `mod` and selectively re-exports items with `pub use foo::SpecificItem` (not glob `pub use foo::*`). This routes selected symbols through the parent
namespace, abstracting the nesting details of the module and naturally filtering
what is visible outside it. Do not make leaf items private as a substitute for
this filtering. That prevents the parent from re-exporting them and forces a
binary jump to fully `pub` when a boundary is crossed. Think about where a symbol is actually needed within the codebase and choose the narrowest level that
reaches there.

- Use `#[cfg(test)]` visibility (e.g. `pub` on test-only constructors like `open_in_memory`) rather than making internals permanently public.

### Types & Derives

- Derive only what is needed. Common set: `Debug`, `Clone`, `PartialEq`, `Eq`.
- Use builder-style methods (`with_*` returning `Self`) for optional configuration on structs.
- Use `clap` derive macros for CLI argument parsing.

### Imports

- Do not separate `use` groups with a blank line. All `use` statements should be in a single block. Let the formatter sort the groups automatically.

### Tests

- Place unit tests in a `#[cfg(test)] mod tests` block at the bottom of the same file.
- Prefer comparing whole-object equality (`assert_eq!`) over asserting individual fields one by one.
- Use `assert_matches!` (from `assert_matches` crate) for enum variant matching.
- Use `assert_fs` and `assert_cmd` for filesystem and CLI integration tests.
