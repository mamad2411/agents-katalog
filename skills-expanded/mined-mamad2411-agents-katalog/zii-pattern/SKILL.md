---
name: zii-pattern
description: Zero Is Initialization pattern with nil sentinels for lookup safety and Odin multi-return values for fallible operations. Use when designing struct defaults, error handling strategy, initialization patterns, or when the user asks about avoiding null checks, default values, or safe fallbacks.
---

# Zero Is Initialization (ZII) & Nil Sentinels

You are an expert in ZII-based design for game engines. When helping with initialization, error handling, or struct design, follow these principles strictly.

## Core Philosophy

**Design every struct so that all-zero memory is a valid, safe default state.**

Operating systems zero out freshly allocated pages. By making `0`, `false`, and `nil` represent "empty" or "inactive", your memory is fully initialized the moment you allocate it.

## ZII Design Rules

When defining any struct:

- `0` for numeric fields = "none" or "inactive"
- `false` for booleans = "disabled"
- `0` for index fields = "no reference" (index 0 is nil sentinel)
- Zero-valued enum = "none" or "default"

This means:

- **No constructors needed**: memory is valid the instant it's allocated
- **No destructors needed**: flip `is_active = false` or `memset` to zero
- **Resetting state is trivial**: zero the memory block, done
- **Hot-reload safe**: zeroed memory is always a valid starting state

## The Nil Sentinel (Index 0)

Reserve index 0 of your entity array as a permanent, zero-initialized stub:

- Start entity allocation at index 1
- Index 0 is always zero-filled and never used for real entities
- Any failed lookup returns index 0 instead of null
- The caller can safely read properties from the nil entity without crashing:
  - `nil_entity.health` → `0.0`
  - `nil_entity.is_active` → `false`
  - `nil_entity.first_child_idx` → `0` (no children, terminates traversal)

## Error Handling via Stubs

**No try/catch. No null checks. No error codes polluting every function.**

If something fails (entity pool full, bad index, stale handle), return the nil sentinel. The calling code continues naturally:

```
entity := get_entity(some_id)
// NO NULL CHECK REQUIRED
// If get_entity failed, entity points to the zero-stub
// entity.health safely evaluates to 0.0
// entity.is_active safely evaluates to false
if entity.health > 0 {
    // Only runs if entity is real and alive
    entity.position.x += 1.0
}
```

This eliminates entire categories of crashes and removes error-checking boilerplate from the game loop.

## Odin Note: Prefer Multi-Return for Fallible Ops

In Odin, prefer explicit multi-return results for operations that can fail due to external state (allocation, file I/O, Vulkan calls, init/setup paths):

```odin
create_buffer :: proc(...) -> (Buffer, bool)
load_asset   :: proc(...) -> (^Asset, Load_Error)
```

Use nil/index-0 sentinels for lookups and hot-path gameplay access where "missing" is a normal state.
Use multi-return for true failure paths where caller must branch.

## Arena Allocator Stubs

If a bump allocator runs out of space, it can return a pointer to a global zero-stub rather than null. The caller writes to the stub harmlessly (the data is lost, but the game doesn't crash). This is appropriate for non-critical allocations like particle effects.

## Rules When Writing Code

- Design every new struct so all-zero is a valid state
- Never use index 0 for real entities — it's the nil sentinel
- Never return null from entity/resource lookups — return the nil sentinel
- In Odin, prefer `(value, ok)` or `(value, error)` returns for fallible setup/resource operations
- Never write explicit null checks in game logic — rely on ZII defaults
- When resetting state, prefer `mem.zero` or `mem.set` over field-by-field clearing
- Enum values should have their zero value be "none" or "invalid"

## Anti-Patterns (Never Do This)

- Never design a struct where zero means something active or important
- Never return null/nil pointers from lookup functions
- Never use try/catch or error codes for entity operations
- Never force sentinel-only handling for true external/runtime failures in Odin
- Never write `if entity != nil` before accessing entity properties
- Never require an init() call before a struct is usable
