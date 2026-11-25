---
name: scala-fundamentals
description: "Write idiomatic Scala 3: given/using type classes, opaque types, immutable collections, sbt builds and property-based testing with ScalaCheck."
type: procedural
category: programming
domain: programming
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: advanced
triggers:
  - scala 3 given using
  - scala type class design
  - sbt build setup
  - scala future vs cats effect
  - scalacheck property test
keywords:
  - scala
  - scala3
  - sbt
  - cats-effect
  - scalacheck
  - type-class
source: custom
enabled: true
---

# Scala 3 Fundamentals

## Purpose

Write idiomatic Scala 3: given/using type classes, opaque types, immutable collections, sbt builds and property-based testing with ScalaCheck.

## When to Use

- You are writing or reviewing Scala 3 code and need idiomatic typing and effect handling.
- An sbt build, cross-build or dependency conflict needs a minimal fix.
- Concurrency and error handling must be expressed explicitly instead of thrown.

## When NOT to Use

- The codebase is Scala 2.12 and cannot move to Scala 3; given/using syntax will not compile.
- The task is Spark-only data code where the DataFrame API dominates the design.
- You need a JVM-wide performance investigation with no Scala-specific semantics.

## Capabilities

- Model domains with opaque types, enums and sealed hierarchies.
- Express effects with `Either`/`IO` instead of exceptions, keeping boundaries explicit.
- Structure sbt multi-module builds with reproducible dependency versions.
- Test invariants with ScalaCheck generators rather than examples only.

## Inputs

- Scala version(s) targeted and whether cross-building is required.
- The module boundaries and current error-handling convention.
- The failing test or type error, and the behaviour the caller expects.

## Workflow

1. Confirm the Scala version and effect library before choosing syntax.
2. Encode invariants in types first (opaque type + smart constructor).
3. Keep effects at the edge: pure core, explicit `IO`/`Either` at the boundary.
4. Pin dependencies in one place and verify with `sbt evicted`.
5. Run `sbt +test` when cross-building so every target compiles.

## Tools

- sbt
- scalafmt / scalafix
- ScalaCheck / munit

## Examples

- `sbt +test`
- `sbt evicted`
- `sbt "Test/runMain propertyCheck"`

## Safety

- Implicit/given resolution that is not obvious makes code hard to debug; keep instances close to types.
- Blocking inside an effect runtime starves the thread pool; use the blocking pool deliberately.
- Cross-build breakage often hides in macros and reflective serialization.

## Source

All-Skills canonical library (`skills/programming/scala-fundamentals`). First-party skill, maintained in this repository.

## Notes

- Opaque types give zero-cost wrappers without runtime allocation.
- `sbt evicted` surfaces version conflicts before runtime `NoSuchMethodError`.
- Pairs with: `programming/java-modern`, `data/apache-spark`.
