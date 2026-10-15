---
name: generational-handles
description: Generational handles for safe entity references without raw pointers. Use when implementing entity references, solving dangling pointer problems, building slot maps, or when the user asks about pointer stability, entity IDs, or safe cross-references.
---

# Generational Handles

You are an expert in generational handle systems for game engines. When helping with entity referencing, follow these principles strictly.

## The Problem

In a sparse entity array, slots get reused. If Entity A holds a raw pointer or index to Entity B, and B is deleted, A's reference becomes dangling. Worse: if the slot is reused for Entity C, A silently points to the wrong entity.

Example: A jar holds a pointer to the goblin carrying it. Goblin dies, slot reused for a chicken. The jar now thinks the chicken is carrying it.

## The Solution: Generational Handles

Replace raw pointers with a self-validating lookup mechanism.

### Handle Structure

A handle is a lightweight struct with two fields:

```
Handle :: struct {
    index:      u32,  // Slot in the entity array
    generation: u32,  // Must match the slot's current generation
}
```

### Slot Map

Each slot in the entity array also stores a generation number:

```
Entity_Slot :: struct {
    entity:     Entity,
    generation: u32,      // Incremented every time this slot is freed
    is_occupied: bool,
}
```

### Lifecycle

1. **Spawn**: Assign entity to a free slot. Create handle with `{index=slot, generation=slots[slot].generation}`
2. **Delete**: Mark slot as free. **Increment `slots[slot].generation`**. This single action instantly invalidates every handle in the codebase that pointed to the old entity
3. **Resolve**: To access an entity via handle:
   - Look up `slots[handle.index]`
   - Compare `handle.generation == slots[handle.index].generation`
   - **Match**: return pointer to entity (it's the same one)
   - **Mismatch**: handle is stale — return nil sentinel (index 0)

### Free List for Slot Reuse

Maintain a free list to recycle deleted slots efficiently:

- On delete: push the freed index onto the free list, increment generation
- On spawn: pop from free list if available, otherwise use `next_empty_slot`
- The generation number ensures old handles to this slot are automatically invalidated

## Integration with ZII

When resolution fails, return index 0 (the nil sentinel). The caller never gets a null pointer — it gets the zero-initialized stub, which safely returns zeroed values for all properties.

```
resolve_handle :: proc(handle: Handle) -> ^Entity {
    if handle.index > 0 &&
       handle.index < MAX_ENTITIES &&
       slots[handle.index].generation == handle.generation &&
       slots[handle.index].is_occupied {
        return &slots[handle.index].entity
    }
    return &slots[0].entity  // nil sentinel, never null
}
```

## Rules When Writing Handle Code

- Never store raw pointers between entities — always use `Handle`
- Never skip the generation check when resolving
- Always increment generation on deletion, never reset it
- Always return the nil sentinel on failed resolution — never return null
- Handles are trivially serializable (just two integers)

## Anti-Patterns (Never Do This)

- Never use raw pointers for entity cross-references
- Never reset generation numbers to zero (they only go up)
- Never assume a handle is valid without resolving it first
- Never store resolved pointers across frames — resolve fresh each time
