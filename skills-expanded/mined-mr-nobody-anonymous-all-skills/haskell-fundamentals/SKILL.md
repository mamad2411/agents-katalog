---
name: haskell-fundamentals
description: "Write idiomatic Haskell: algebraic data types, type classes, monadic effects, laziness pitfalls, cabal projects and property-based testing."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - haskell type class design
  - haskell monad transformer
  - haskell space leak
  - cabal project setup
  - quickcheck property
keywords:
  - haskell
  - ghc
  - cabal
  - typeclass
  - monad
  - quickcheck
source: custom
enabled: true
---

# Haskell Fundamentals

## Purpose

Write idiomatic Haskell: algebraic data types, type classes, monadic effects, laziness pitfalls, cabal projects and property-based testing.

## When to Use

- You are implementing Haskell data modelling or effectful logic.
- A program leaks memory or stalls due to lazy evaluation.
- You need a cabal project with reproducible dependency bounds and tests.

## When NOT to Use

- The system is in another language and Haskell would be adopted only for a small script.
- The task needs a mature ecosystem library that does not exist for the target domain.
- You need operational debugging of a running JVM/Node service.

## Capabilities

- Model domains with algebraic data types and exhaustive pattern matches.
- Use type classes and newtypes for abstraction without ad-hoc branching.
- Spot and fix space leaks from lazy accumulation.
- Verify invariants with QuickCheck and keep the build reproducible with cabal freeze.

## Inputs

- GHC version and the resolver/package set in use.
- The module being changed and its exported API.
- Observed behaviour: failing property, memory profile, or type error.

## Workflow

1. Check the GHC/cabal versions and the package set before writing code.
2. Model the domain with data types so illegal states cannot be constructed.
3. Keep pure logic separate from IO; push effects to the program edge.
4. Watch for lazy accumulation: use strict fields or explicit folds where needed.
5. Run `cabal build all && cabal test all` and add properties for the new invariants.

## Tools

- ghc / cabal
- ghci
- QuickCheck / hedgehog
- profiling with -prof

## Examples

- `cabal build all && cabal test all`
- `cabal repl lib:myapp`
- `cabal freeze`

## Safety

- String/ByteString conversion at scale causes leaks; choose the text type deliberately.
- Avoid `head`, `fromJust` and partial patterns in library code.
- Dependency bounds without a freeze file make builds drift.

## Source

All-Skills canonical library (`skills/programming/haskell-fundamentals`). First-party skill, maintained in this repository.

## Notes

- `-Wall -Werror=incomplete-patterns` catches the most common class of bug early.
- Strictness annotations are the fix for foldl-style leaks.
- Pairs with: `programming/rust-fundamentals`, `programming/scala-fundamentals`.
