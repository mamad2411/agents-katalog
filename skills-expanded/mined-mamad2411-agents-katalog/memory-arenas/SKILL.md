---
name: memory-arenas
description: Predictable memory management patterns for game engines. Use when implementing arena allocators, bulk memory allocation, bump allocators, or when the user asks about memory management strategy, avoiding malloc/free, or frame-scoped allocations.
---

# Predictable Memory Management

You are an expert in handmade-style game engine memory management. When helping with memory-related code, follow these principles strictly.

## Core Philosophy

**Bulk allocation with tuned sizes. Individual per-object malloc/free is forbidden.**

Dynamic runtime allocations (malloc, new, per-entity allocations) create unpredictable performance, fragment memory, and introduce failure points. Instead:

- Define **harsh limits** at compile time (e.g., `MAX_ENTITIES :: 10_000`)
- Profile peak usage and set arena initial sizes to comfortably cover that peak
- If the game loads successfully once, it will reliably run on that hardware forever — no late-game OOM crashes
- Memory fragmentation is impossible because there is no fragmentation to create

## Arena Allocator (Bump Allocator)

For dynamic-sized data (rendering commands, level loading, temporary work), use a bump/arena allocator:

1. Allocate a profiled/tuned initial block at startup
2. Advance a pointer forward through it sequentially
3. When the scope ends (frame ends, level ends), reset the offset to zero
4. No per-object free, no garbage collection, no reference counting

### Growable Arenas

Arenas are **tuned-size with a growth fallback**, not rigidly fixed:

- **Profile first:** run the game, measure peak usage per arena, set initial size to cover that peak
- **Growth is a bug signal:** if an arena grows at runtime, that means your tuned size is wrong — fix the size, don't rely on growth as normal operation
- **Growth mechanism:** when the arena exhausts its block, allocate a new chained block (same default size or larger if the single allocation demands it). On arena clear, reset all blocks' offsets to zero
- **Graceful OOM via ZII stub:** if the OS refuses memory, return a pointer to a global zero-initialized stub instead of NULL. Because all structs use Zero Is Initialization, the code safely reads/writes the stub without crashing — the game may glitch visually for a frame but keeps running. No null checks polluting the codebase

### Arena Lifetimes

Three distinct lifetime scopes:

| Allocator | Lifetime | Use for |
|---|---|---|
| App/permanent arena | Process lifetime | Data that must outlive a frame (entity arrays, loaded assets) |
| Frame/temp arena | Reset every frame | Per-frame scratch work (render commands, string formatting) |
| Swapchain arena | Reset on swapchain recreation | Vulkan resources tied to swapchain dimensions |

### Odin-Specific Guidance

Odin has built-in arena support in `core:mem`:

- Use `context.allocator` for permanent allocations (app arena)
- Use `context.temp_allocator` for per-frame scratch (frame arena)
- Arenas can be created with `mem.Arena` and initialized with a backing buffer
- Use `mem.arena_allocator(&arena)` to get an `Allocator` from an arena
- Reset with `mem.arena_free_all(&arena)` or `free_all(temp_allocator)` at frame start
- Size arenas via `#config` at compile time for initial sizing

For growable arenas in Odin, prefer `virtual.Arena` (`core:mem/virtual`) — it reserves a large virtual address range upfront and commits physical pages on demand. The OS only backs pages you actually touch, so you get growability without chained blocks or wasted physical memory.

## Vulkan Memory

Vulkan's explicit memory management follows the same pattern:

- Make a **few large allocations at startup** based on memory type (upload buffer, static buffer, staging buffer)
- Use a bump allocator to sub-allocate within each large block
- When a level ends, reset the bump offset — no per-object vkFreeMemory
- Persistently map host-visible buffers at startup; never map/unmap per frame

## Anti-Patterns (Never Do This)

- Never `malloc`/`free` or `new`/`delete` per entity or per frame
- Never use dynamic containers (std::vector, dynamic arrays) for core entity storage
- Never implement reference counting or garbage collection
- Never call `vkAllocateMemory` per object — batch into large blocks
- Never map/unmap Vulkan buffers per frame — keep them persistently mapped

## When Reviewing or Writing Code

- If you see per-object allocation, refactor to use a pre-allocated pool or arena
- If you see dynamic arrays growing unbounded, suggest a fixed-capacity array with a harsh limit
- Always ask: "What is the lifetime of this allocation?" and match it to the correct arena
- Prefer stack allocation or arena allocation over heap allocation in all cases
