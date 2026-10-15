---
name: rust-unused-code
description: Use for Rust `dead_code` and `unused_imports` findings, especially when conditional compilation, feature flags, target-specific code, or test-only code change what actually gets compiled. Prefer conditional compilation, narrowly scoped inline modules, and in-function imports so only needed code enters each compiled module. Use when deciding whether code should move behind `#[cfg(...)]`, into a tighter module, or into a narrower import scope instead of suppressing lints.
---

# Rust Unused Code

Treat `dead_code` and `unused_imports` as useful feedback about the compiled
shape of the program, not as noise to suppress.

## Working stance

- Start from the compiled configuration that raised the lint.
- Keep each module honest about what it actually depends on in that
  configuration.
- Bring code into scope only where that code is needed.
- Prefer changing compilation boundaries over adding lint suppressions.
- Treat `#[allow(dead_code)]` and `#[allow(unused_imports)]` as a last resort
  that normally signals the design still needs tightening.

## Core rule

If a symbol, import, or helper is only needed in some configurations, compile
it only in those configurations.

That usually means:

- put `#[cfg(...)]` on the item that is actually conditional,
- move related items into a narrowly scoped inline module guarded by `#[cfg(...)]`,
- move an import down into the function or test that uses it,
- split common API from conditional implementation details.

## Preferred fixes

### Gate the item, not the symptom

- Put `#[cfg(feature = "...")]`, `#[cfg(test)]`, or target guards on the
  function, type, impl block, const, or module that is genuinely optional.
- Avoid compiling a helper into a module where no compiled path can call it.

### Use narrowly scoped inline modules

- Group feature-specific or target-specific helpers into an inline module when
  they only make sense together.
- Keep the public surface outside the gated module as small as possible.
- Re-export only what the active configuration must expose.

### Use in-function imports when scope is genuinely local

- Import inside a function when a dependency is used in one function, one test,
  or one narrow cfg-controlled branch.
- Prefer this over a broad module-level `use` that becomes unused in other
  builds.

### Keep tests and support code inside test-only compilation

- Put test helpers under `#[cfg(test)]`.
- Import production items into tests from the test module or test function,
  rather than broadening production module imports for test convenience.

## Anti-patterns

- Adding `#[allow(dead_code)]` to keep an uncalled helper around "for later".
- Adding `#[allow(unused_imports)]` because different features use different
  imports from the same module.
- Using `cfg_attr(..., allow(...))` to silence lints instead of expressing the
  real compilation boundary.
- Keeping target-specific or feature-specific helpers in a common module when
  only one implementation can compile at a time.
- Pulling imports to module scope when only one function or test needs them.

## Decision guide

When a lint appears, ask these questions in order:

1. Is this code meant to exist in every compiled configuration?
2. If not, which exact `#[cfg(...)]` boundary matches the real usage?
3. Does the unused item belong in a smaller inline module with its peers?
4. Is the import only needed inside one function, test, or cfg branch?
5. If I remove or move this item, does the compiled dependency picture become
   more accurate?

If the honest answer is "this item should not compile here", change the
compilation scope. Do not suppress the lint.

## When suppression is reluctantly acceptable

Use suppression only when the code must exist in that compiled scope even
though direct usage is intentionally opaque to the compiler, for example:

- generated code that must preserve a stable emitted shape,
- external macro expansion contracts you cannot restructure,
- trait or ABI surfaces that must remain present for external consumers while
  local builds cannot exercise every symbol.

Even then:

- scope the suppression to the smallest possible item,
- explain why the compiler cannot see the usage,
- prefer a comment that describes the external contract,
- revisit the design before copying the pattern elsewhere.

## Worked examples

Read [worked-examples.md](references/worked-examples.md) when you need concrete
before-and-after patterns for:

- feature-gated imports,
- target-specific helper modules,
- test-only helpers and imports,
- in-function imports inside cfg-controlled code.
