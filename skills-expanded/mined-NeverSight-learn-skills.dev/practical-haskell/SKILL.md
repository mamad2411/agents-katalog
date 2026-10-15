---
name: practical-haskell
description: Guides efficient Haskell aligned with GHC practice -- laziness and strictness, purity, fusion, newtypes, pragmas, Core reading, and space-leak avoidance. Use when writing or reviewing Haskell, optimizing or profiling, debugging strictness or memory, or when the user mentions GHC, thunks, foldl vs foldl', list fusion, SPECIALIZE, or UNPACK.
---

# Practical Haskell (GHC)

Use this skill when the task is Haskell code quality, performance, or reasoning about evaluation. Assume GHC with optimizations (`-O` / `-O2`) unless the user says otherwise.

## Core ideas

- **Purity** lets the compiler rewrite code safely; prefer explicit effects in `IO` or appropriate abstraction.
- **Lazy by default**: values are evaluated when needed. That enables composition but can hide space leaks.
- **Types** catch many bugs early; use them to encode intent (including `newtype` for domain distinctions).
- **Know what GHC emits**: when performance matters, treat Core (`-ddump-simpl`) as ground truth after optimization.

## Always

- Be explicit about **strict vs lazy** data and bindings when modeling accumulators, parsers, or long-lived state.
- Prefer **`foldl'`** from `Data.List` (or strict folds from the right library) for numeric accumulation over plain `foldl` on strict values.
- **Profile** (`profiling`, eventlog, `ghc-debug`, etc.) before micro-optimizing.
- Write **small composable** functions; rely on inlining and specialization rather than giant monoliths.
- Use **fusion-friendly** pipelines (`map`, `filter`, `foldr`-based idioms) where appropriate; validate hot paths in Core if allocation matters.

## Never

- Accidentally build **large chains of thunks** (classic `foldl (+) 0` on large strict sums).
- Ignore **space leaks** from unevaluated structure holding onto memory.
- **Micro-optimize** without evidence from profiling or Core.
- Treat laziness as universally good or bad; decide per use case.

## Prefer

- **Strict fields** (`!`) on accumulator-like constructor fields; **`UNPACK`** for small unboxed numeric fields when profiling supports it.
- **Newtypes** for zero-runtime-cost distinctions vs `data` with a single field.
- **`INLINE` / `INLINABLE` / `SPECIALIZE`** on hot polymorphic glue when dictionaries or lack of specialization shows up in Core.
- **Worker/wrapper** style: a strict internal worker and a small external API.
- **Monomorphic** hot loops when polymorphism still costs after specialization attempts.

## Laziness and strictness

```haskell
import Data.List (foldl')

-- Infinite lists are fine when consumption is bounded.
naturals :: [Integer]
naturals = [1..]

firstTen :: [Integer]
firstTen = take 10 naturals

-- foldl on strict arithmetic often leaks thunks; foldl' forces as it goes.
badSum :: [Int] -> Int
badSum = foldl (+) 0

goodSum :: [Int] -> Int
goodSum = foldl' (+) 0
```

**Bang patterns** (`{-# LANGUAGE BangPatterns #-}`) force evaluation of a binding; use at strategic places (accumulators, fields that must not retain thunks).

**Strict fields** on `data` constructors evaluate to WHNF when the constructor is entered; combine with profiling to avoid over-forcing.

## Fusion and lists

List pipelines like `sum . map f . filter p` often fuse under `-O2` into a single loop. If allocation persists, inspect Core. Avoid forcing materialization unnecessarily (e.g. redundant `length` or indexing on huge intermediates in hot code).

GHC applies rewrite rules internally; custom `{-# RULES #-}` is advanced and must be validated (correctness and phase interactions).

## Newtypes

```haskell
newtype UserId = UserId Int
  deriving (Eq, Ord, Show)

newtype Email = Email String
  deriving (Eq, Show)
```

Use `newtype` for distinct types with identical representation. `GeneralizedNewtypeDeriving` can derive classes when appropriate and policy allows.

## Specialization and inlining

Polymorphic hot code may pass type-class dictionaries. Mitigations:

- Give a **monomorphic** variant for the hot path.
- Use **`{-# SPECIALIZE #-}`** for concrete instantiations.
- Use **`{-# INLINABLE #-}`** on small polymorphic helpers so call sites can specialize.

Verify with Core, not assumptions.

## Reading Core (quick guide)

Compile with something like `ghc -O2 -ddump-simpl -dsuppress-all -dno-suppress-type-signatures YourModule.hs` (flags vary by need).

- **`case`** usually forces evaluation; extra **`let`** bindings can mean allocation.
- Look for **fusion**: one tight recursive loop vs multiple passes.
- Check whether **dictionary calls** remain in hot loops.

## Mental checklist

1. **When** does each subexpression get forced?
2. **Where** might thunks retain memory (closures, lazy fields, `foldl`-style accumulation)?
3. **Will** this pipeline fuse or allocate intermediates?
4. **What** does simplified Core show for the hot path?
5. **Is** the hot code monomorphic and specialized?

## Signature moves (when profiling says so)

- Strict accumulators: `foldl'`, bang patterns, strict fields.
- `UNPACK` small strict numeric fields to reduce indirection.
- `INLINE` / `INLINABLE` / `SPECIALIZE` to recover specialization.
- Fusion-friendly combinators; avoid accidental intermediate lists in inner loops.
- Worker/wrapper refactor for clearer strict internals.
- Re-check Core after each change.

## Additional resources

For extended examples and GHC flag recipes, see [reference.md](reference.md).
