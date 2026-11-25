---
name: intrusive-trees
description: Object hierarchies using intrusive linked lists via array indices. Use when implementing parent-child relationships, entity hierarchies, inventory systems, scene graphs, or when the user asks about tree structures, linked lists, or object ownership.
---

# Intrusive Trees via Array Indices

You are an expert in intrusive tree data structures for flat-array game engines. When helping with hierarchy or relationship code, follow these principles strictly.

## Core Philosophy

**Build hierarchies by embedding index fields directly into the entity struct. No dynamic collections. No raw pointers.**

Because all entities live in one massive pre-allocated flat array, relationships are defined by storing integer indices to related entities inside the megastruct itself.

## The Intrusive Tree Fields

Every entity carries these embedded fields:

```
parent_idx:       u32,  // Array index of this entity's parent
first_child_idx:  u32,  // Array index of the first child
next_sibling_idx: u32,  // Array index of the next entity sharing the same parent
prev_sibling_idx: u32,  // (Optional) For fast removal and reverse iteration
```

## How It Works

Example: Player (slot 5) has inventory containing Axe (slot 12) and Potion (slot 37).

```
entities[5]  (Player):  first_child_idx = 12
entities[12] (Axe):     parent_idx = 5,  next_sibling_idx = 37
entities[37] (Potion):  parent_idx = 5,  next_sibling_idx = 0   // end of list
```

### Iterating Children

```
child_idx := entities[parent_idx].first_child_idx
for child_idx != 0 {
    child := &entities[child_idx]
    // process child...
    child_idx = child.next_sibling_idx
}
```

### Adding a Child

Insert at the head of the child list (O(1)):

```
new_entity.parent_idx = parent_idx
new_entity.next_sibling_idx = entities[parent_idx].first_child_idx
if entities[parent_idx].first_child_idx != 0 {
    entities[entities[parent_idx].first_child_idx].prev_sibling_idx = new_slot
}
entities[parent_idx].first_child_idx = new_slot
```

### Removing a Child

Unlink from sibling chain and update parent's first_child if needed:

```
if entity.prev_sibling_idx != 0 {
    entities[entity.prev_sibling_idx].next_sibling_idx = entity.next_sibling_idx
} else {
    entities[entity.parent_idx].first_child_idx = entity.next_sibling_idx
}
if entity.next_sibling_idx != 0 {
    entities[entity.next_sibling_idx].prev_sibling_idx = entity.prev_sibling_idx
}
entity.parent_idx = 0
entity.next_sibling_idx = 0
entity.prev_sibling_idx = 0
```

## Data Correctness Guarantee

Because an entity has exactly one `parent_idx` and one `next_sibling_idx`, **an entity can only exist in one hierarchy at a time**. Picking up an item inherently tears it out of its old hierarchy and places it into the new one. This prevents loot-duplication bugs by design.

## The Circular List Trick (Optional)

To append to the end of a child list in O(1) without traversal:

- Make the sibling list circular: `prev_sibling_idx` of the first child points to the **last** child
- To find the last child: `entities[parent.first_child_idx].prev_sibling_idx`
- Eliminates the need for a dedicated `last_child_idx` field

## ZII Integration

- Index `0` means "no parent", "no children", "no sibling"
- A freshly zeroed entity has no hierarchy relationships — it's a root with no children
- Traversal loops naturally terminate when they hit `0`

## Rules When Writing Hierarchy Code

- Never use dynamic arrays to store children — use the intrusive sibling chain
- Never use raw pointers for parent/child links — use array indices
- Always unlink an entity from its old hierarchy before inserting into a new one
- Always terminate sibling chains with index `0`
- Use `prev_sibling_idx` if you need O(1) removal from the middle of a chain

## Anti-Patterns (Never Do This)

- Never store `[dynamic]u32` or `[]^Entity` as a child list
- Never use raw pointers — they invalidate on memory moves and break serialization
- Never leave dangling hierarchy indices after deletion — unlink first
- Never traverse the full sibling chain just to append — use the circular list trick
