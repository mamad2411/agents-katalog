---
name: type-safe-enum-generation-per-language
description: "Generate per-language enums from a single content_types JSON: Rust enum, Python StrEnum, TypeScript union literal, Go const iota — with from_string, to_string, and SIZE constants."
category: codegen
version: 1.0.0
version_origin: extracted
confidence: high
tags: [magika, codegen]
source_type: extracted-from-git
source_url: https://github.com/google/magika.git
source_ref: main
source_commit: 0a8cb9626bbf76c2194117d9830b23e9052a1548
source_project: magika
imported_at: 2026-04-18T00:00:00Z
---

# Type Safe Enum Generation Per Language

**Trigger:** You support 300+ string-keyed types and want compile-time validation in every language without hand-maintaining four enum lists.

## Steps

- Parse content_types_kb.min.json once; produce a deterministically sorted list of labels.
- Generate per language: Rust pub enum (with non_exhaustive), Python StrEnum, TS string literal union, Go const iota with String().
- Apply consistent name normalization (3gp → _3gp in Rust due to no leading-digit identifiers).
- Generate from_string / to_string + a SIZE/COUNT constant.
- At codegen time, validate every label is present in the target model — fail the build on drift.
- Add a 'DO NOT EDIT' header to every generated file and check generated files into git.

## Counter / Caveats

- Label normalization rules differ per language; keep them in one place.
- Rust enums with 300+ variants slow compile time noticeably; non_exhaustive helps downstream evolution.
- Index stability matters if downstream uses int indices for array lookups; renumbering breaks model output mappings.
- Tooling (rust-analyzer, pyright) needs the generated files to exist before it can resolve symbols — generate before checkout-time tasks.

## Source

Extracted from `magika` (https://github.com/google/magika.git @ main).

Files of interest:
- `rust/gen/src/main.rs:40-100`
- `python/src/magika/types/content_type_label.py:19-50`
- `js/src/content-type-label.ts`
