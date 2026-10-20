# Agent instructions — intentumdiff-puppet-parser

The puppet parser plugin: a Wasm component emitting deterministic SemanticNode trees.

## Hard invariants
- Determinism: same input, byte-identical tree; 0-based positions; stable labels/hashes.
- No source text in facts; parse failures return the in-band error envelope, never a panic.
- `.claude/skills/` here are STAMPED from the SDK master — never edit them in this repo.
- CI is a thin caller of the SDK's reusable parser-ci.yml — CI fixes belong in the SDK.

## Build + test (Rust 1.93.0)
```bash
cargo build --release --target wasm32-wasip2
cargo test
```

Guide: https://github.com/buchochelliq-labs/intentumdiff-plugin-sdk/blob/main/docs/PLUGIN_GUIDE.md
