---
name: ki-stack-file-surgery
description: |
  Perform offline, structural KiCad file edits with kiutils-rs. Use when the task
  is better expressed as a deterministic file transformation, when no live KiCad
  session is needed, or when preserving KiCad syntax and formatting matters.
license: MIT
compatibility: opencode
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
---

# ki-stack-file-surgery

## Purpose

This skill teaches the agent how to use `kiutils-rs` for structural KiCad file edits.

It is the canonical `ki-stack` skill for:

- offline KiCad file mutation
- lossless read/modify/write flows
- project, library table, design rule, and board metadata edits
- structural transforms where preserving unknown syntax matters

## When to use it

Use this skill when:

- no live KiCad session is needed
- the edit is inherently file-structural
- preserving formatting and unknown tokens matters
- the task is deterministic enough to justify a small Rust transform

Do not use this skill when:

- the task is naturally a live board automation workflow
- the task is just rendering or verification
- the agent only needs a tiny text patch that is not semantically structural

## Shared assumptions

- Prefer `kiutils-rs` for offline structural changes.
- Default to lossless output.
- Inspect before writing custom Rust when possible.
- Use typed setter/upsert/remove APIs for writeable edits.

## Phase 1: Orient

1. Find the relevant KiCad files:

   ```bash
   skills/ki-stack/bin/kicad-project-find <root>
   ```

2. Identify the file type before writing code:

- `.kicad_pcb`
- `.kicad_mod`
- `.kicad_dru`
- `.kicad_pro`
- `fp-lib-table`
- `sym-lib-table`

3. If the file type is supported by the stable public `kiutils-rs` API, continue.

4. If the task actually wants live state or selection-aware behavior, route to `ki-stack-live` instead.

## Phase 2: Inspect

Before writing custom Rust, inspect the file shape.

Preferred command:

```bash
skills/ki-stack/bin/kiutils-inspect path/to/file.kicad_pcb --show-unknown --show-diagnostics --show-canonical
```

Useful flags:

- `--json`
- `--show-cst`
- `--show-canonical`
- `--show-unknown`
- `--show-diagnostics`

Inspection should tell you whether:

- the file parses cleanly
- unknown tokens exist and should be preserved
- the change should target typed APIs rather than low-level internals

## Phase 3: Execute

Write the smallest Rust program that performs the structural edit.

Canonical safe pattern:

```rust
use kiutils_rs::{PcbFile, WriteMode};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut doc = PcbFile::read("input.kicad_pcb")?;
    doc.upsert_property("EditedBy", "ki-stack");
    doc.write_mode("output.kicad_pcb", WriteMode::Lossless)?;
    Ok(())
}
```

Preferred edit style:

- `set_*`
- `upsert_*`
- `remove_*`

Avoid this pattern for writeable mutations:

- mutate through `ast_mut()` and then call `write()`

That is explicitly a guardrail in the library docs.

## Phase 4: Verify

Structural file surgery is not done when the program compiles. It is done when the output is checked.

Preferred verification loop:

1. inspect the output file again
2. render the relevant artifact with `ki-stack-render` if visual output matters
3. run DRC/ERC if the file type and change warrant it
4. report lossless vs canonical write mode explicitly

For boards, it is often reasonable to follow with:

```bash
skills/ki-stack/bin/kicad-drc-json output.kicad_pcb drc.json
```

## Phase 5: Report

Always report:

- input file
- output file
- file type
- whether lossless or canonical write mode was used
- the exact Rust program or command used
- any render or check artifacts produced

## Good transform shape

Write short single-purpose transforms.

Preferred shape:

1. read one document type explicitly
2. apply a small number of typed mutations
3. write in lossless mode unless normalization is requested
4. exit with a clear error if parsing or writing fails

## Helper assets

References:

- `skills/ki-stack/references/kiutils-recipes.md`

Helpers:

- `skills/ki-stack/bin/kicad-project-find`
- `skills/ki-stack/bin/kiutils-inspect`

Templates:

- `skills/ki-stack/templates/rust-kiutils-main.rs`

## Guardrails

- If the task wants live editor context, do not force a file-surgery path.
- If the file type is unsupported by the stable public API, say so clearly.
- Default to lossless output.
- Do not mutate through `ast_mut()` and then write.
- If the change is electrically meaningful, follow with CLI checks instead of trusting the transform alone.

## Completion states

- `DONE`: transform completed and output verified
- `DONE_WITH_CONCERNS`: transform completed but verification is partial or a file-type caveat exists
- `BLOCKED`: parse, write, or toolchain setup failed irrecoverably
- `NEEDS_CONTEXT`: target files, desired mutation, or input/output paths are unclear
