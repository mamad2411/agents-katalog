# AGENTS.md — CL-01 (trios-claude)

> AAIF-compliant | MCP-compatible

## Identity

- Ring: CL-01
- Package: trios-claude-cl01
- Role: tools (scaffold — logic migration: TODO)

## What this ring does (target)

Owns tools logic for trios-claude after migration.
Currently a stub with a marker type and metadata constants.

## Rules (ABSOLUTE)

- R1: Sibling rings may not be imported without Cargo.toml declaration
- R9: Ring isolation
- L6: Pure Rust only

## You MAY

- ✅ Add types/methods within this ring's scope (tools)
- ✅ Add unit tests
- ✅ Migrate code from `crates/trios-claude/src/` matching this ring's scope

## You MAY NOT

- ❌ Import sibling rings without Cargo.toml dep
- ❌ Add I/O or async without explicit approval (check parent crate's policy)

## Build

```bash
cargo check -p trios-claude-cl01
cargo test  -p trios-claude-cl01
```
