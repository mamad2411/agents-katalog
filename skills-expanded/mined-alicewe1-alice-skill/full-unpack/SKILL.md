---
name: full-unpack
description: Complete unpacking chain. Trigger: full unpack, complete unpack, unpack workflow, 完整脱壳.
type: chain
x-alice-class: reverse
---# full-unpack

## Chain
1. `esp-law` — ESP law OEP location
2. `memory-breakpoint` — Memory BP fallback
3. `iat-rebuild` — IAT rebuild
4. `patch-apply` — Verify + save

## Execution
Execute each step sequentially. Output combined results.
