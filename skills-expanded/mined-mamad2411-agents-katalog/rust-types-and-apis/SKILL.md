---
name: rust-types-and-apis
description: Use for trait bounds, generics, trait objects, newtypes, typestate, conversion boundaries, public API design, and crate-facing Rust interfaces.
globs: ["**/Cargo.toml", "**/*.rs"]
---

# Rust Types and APIs

Use this when the real question is how much of the design should be expressed
in types, traits, and public signatures.

## Working stance

- Make invalid states hard to represent before adding runtime checks.
- Keep public APIs narrower than internal helper code.
- Prefer concrete types until abstraction pressure is real.
- Use trait objects for extension seams and heterogeneity, not by reflex.
- Prefer typed domains and borrowed read-only inputs over stringly or
  collection-specific signatures.
- Accept broad inputs; return precise outputs.

## Decision surface

- Generics: the caller should stay generic and one concrete type flows through
  each call site.
- `dyn Trait`: runtime heterogeneity, plugin seams, or monomorphization costs
  matter more than static dispatch.
- Newtype: domain distinction matters and misuse should not compile.
- Typestate: operation order is finite and important enough to encode.
- Sealed trait: downstream implementations would weaken invariants.
- `AsRef` or `Into` inputs: caller flexibility helps without hiding semantics.
- `&str` or `&[T]` inputs: prefer them over `&String` or `&Vec<T>` when the
  callee only reads.

## Red flags

- public APIs expose internal helper traits or incidental generic parameters,
- public APIs accept `&String` or `&Vec<T>` where `&str` or `&[T]` would do,
- strings represent closed sets, validated IDs, or states that should be
  enums or newtypes,
- a trait object appears only to avoid naming a concrete type,
- boxed trait objects appear even though one concrete type or `impl Trait`
  would work,
- one implementation spawned a deep generic or trait abstraction anyway,
- newtypes exist but immediately expose raw fields everywhere,
- invariant-carrying types expose public fields directly,
- typestate multiplies boilerplate without enforcing a real rule,
- crate features change core semantics rather than optional integration.

Read [generics-vs-dyn.md](references/generics-vs-dyn.md),
[newtypes-and-typestate.md](references/newtypes-and-typestate.md), and
[public-api-boundaries.md](references/public-api-boundaries.md) when one of
those forks becomes the main design pressure.
