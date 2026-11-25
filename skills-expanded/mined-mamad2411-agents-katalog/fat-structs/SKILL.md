---
name: fat-structs
description: Entity design using tagged unions with shared fields instead of ECS. Use when designing entity systems, game object architecture, adding new entity properties, or when the user asks about entity storage, component systems, or game object patterns.
---

# Tagged-Union Entity Design

You are an expert in handmade-style entity architecture using Odin's tagged unions. When helping with entity/game-object code, follow these principles strictly.

## Core Philosophy

**Discard ECS. Use a single struct with shared fields and a tagged union for type-specific data.**

Modern ECS fragments data into arrays of individual components to maximize cache lines. However, iterating over entities is rarely the actual bottleneck in indie games. The complexity of splitting and merging component streams introduces friction for small teams.

A pure megastruct (every possible field in one struct, toggled by boolean flags) works but wastes memory on irrelevant fields and relies on runtime flag discipline. Odin's tagged unions give you the same flat-array storage model with **compiler-enforced type safety** and **exhaustive switch checking**.

## The Pattern

Split entity data into two layers:

1. **Shared fields** — properties that nearly every entity needs (transform, hierarchy, rendering)
2. **Tagged union** — type-specific data, one variant per entity kind

```odin
Player_Data :: struct {
    health:        f32,
    stamina:       f32,
    input_dir:     vec2,
}

Enemy_Data :: struct {
    health:        f32,
    aggro_range:   f32,
    target_handle: Handle,
}

Projectile_Data :: struct {
    damage:   f32,
    lifetime: f32,
    owner:    Handle,
}

Item_Data :: struct {
    item_id:    u32,
    stack_size: u16,
}

Entity_Data :: union {
    Player_Data,
    Enemy_Data,
    Projectile_Data,
    Item_Data,
}

Entity :: struct {
    // Shared fields (common to all entity types)
    flags:        Entity_Flags,

    position:     vec3,
    rotation:     vec3,
    scale:        vec3,
    velocity:     vec3,

    // Hierarchy (intrusive tree via indices)
    parent_idx:       u32,
    first_child_idx:  u32,
    next_sibling_idx: u32,
    prev_sibling_idx: u32,

    // Rendering
    mesh_id:      u32,
    material_idx: u32,
    transform:    mat4,

    // Type-specific data
    data: Entity_Data,
}
```

### Why Not `#no_nil`

Do NOT use `#no_nil` on `Entity_Data`. The default nil union value means:

- A zeroed entity has `data = nil` → no type → inactive (ZII compatible)
- You can check `entity.data == nil` to skip empty slots during iteration
- Deleting an entity is just zeroing its memory — the union tag resets to nil naturally

### Exhaustive Switching

The compiler enforces that you handle every entity type:

```odin
switch d in &entity.data {
case ^Player_Data:
    d.stamina = min(d.stamina + regen * dt, max_stamina)
case ^Enemy_Data:
    if distance(entity.position, player_pos) < d.aggro_range {
        // chase
    }
case ^Projectile_Data:
    d.lifetime -= dt
    if d.lifetime <= 0 do destroy_entity(idx)
case ^Item_Data:
    // items don't tick
case nil:
    // empty slot — skip
}
```

If you add a new variant to `Entity_Data`, the compiler flags every switch that doesn't handle it. No forgotten flag checks, no silent fallthrough.

### Shared Fields for Cross-Cutting Logic

Logic that applies to all entity types uses the shared fields directly — no switch needed:

```odin
// Physics integration — runs on ALL active entities regardless of type
for &entity in entities {
    if entity.data == nil do continue
    entity.position += entity.velocity * dt
}
```

### Entity_Flags for Orthogonal State

Use a flags enum for state that cuts across types (any entity kind can be on fire, invisible, etc.):

```odin
Entity_Flags :: bit_set[Entity_Flag]

Entity_Flag :: enum {
    On_Fire,
    Invisible,
    Frozen,
    // ... orthogonal states, not entity types
}
```

Flags are for **temporary states**, not for distinguishing entity types. The union tag handles type identity.

## Storage

A single contiguous array, allocated once at startup:

- `entities: [MAX_ENTITIES]Entity` — one flat block, fixed size per entity = shared fields + largest union variant
- `next_empty_slot` starts at 1 (index 0 is the nil sentinel)
- Gaps are left when entities are deleted (sparse array) — never shift memory to compact

## Benefits

- **Serialization is trivial**: save/load the entire array as a flat binary blob — the union tag is an integer, variants are value types
- **Compiler-enforced completeness**: adding a new entity type forces you to handle it everywhere
- **No polymorphism**: no vtables, no dynamic dispatch, no inheritance hierarchies
- **ZII compatible**: zeroed memory = nil union = empty slot
- **Hot-reload friendly**: the struct layout is the entire game state — cast `rawptr` to `^Game_State`
- **Clearer data ownership**: each variant documents exactly which fields belong to which entity type

## Rules When Writing Entity Code

- Shared fields go in `Entity` directly — they are available to all entity types
- Type-specific fields go in a union variant struct — never add type-specific data to the shared fields
- Use `switch d in &entity.data` for type-specific logic — the compiler ensures exhaustive handling
- Use `Entity_Flags` (bit_set) only for orthogonal temporary states, not for type identity
- Iterate the flat array with simple `for` loops; skip `nil` union slots
- Never allocate entities individually — always use the pre-allocated pool
- Index 0 is reserved as the nil sentinel (see ZII pattern)
- Use generational handles for safe cross-references between entities
- Do NOT use `#no_nil` on the entity union — nil = empty slot is the ZII default

## Anti-Patterns (Never Do This)

- Never create separate component arrays and join them at runtime (ECS)
- Never use inheritance, vtables, or Odin interfaces for entity types
- Never dynamically resize the entity array
- Never compact/defragment the array — leave gaps, use sparse iteration
- Never store raw pointers between entities — use indices or generational handles
- Never use boolean flags to distinguish entity types — that's what the union tag is for
- Never use `#partial switch` on entity data — always handle every variant explicitly
