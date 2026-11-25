---
name: maple-make
description: Use when working with MapleStory assets — how to look up, compose, and render characters, mobs, maps, skills, items, or sprites via maple-lookup MCP.
---

# maple-make Skill

Loads the MapleStory data reference library under `references/` to provide complete knowledge on how MapleStory assets are structured and composed — sprite rendering, socket assembly, mob/NPC/skill/map data structures.

## Entry Point

Always start with `references/maple-data-reference.md`. It is the index that maps every domain to the correct resource file. Do not load resource files directly without consulting the entry point first.

## Resource Map

| File | Description |
|------|-------------|
| [maple-data-reference.md](references/maple-data-reference.md) | **ENTRY POINT** — Quick Rules, ID formulas, reference map |
| [maple-core-rendering.md](references/maple-core-rendering.md) | CDN, flip rules, draw formula, Phaser integration |
| [maple-core-folder-guide.md](references/maple-core-folder-guide.md) | data/ directory structure, file naming conventions |
| [maple-core-id-system.md](references/maple-core-id-system.md) | ID-to-file resolution rules |
| [maple-core-id-reference.md](references/maple-core-id-reference.md) | Weapon types, job tree, body part slots, skill grades |
| [maple-core-items.md](references/maple-core-items.md) | Item overview |
| [maple-core-items-reference.md](references/maple-core-items-reference.md) | Item ID reference |
| [maple-character-rendering.md](references/maple-character-rendering.md) | Character socket assembly (multi-part equip) |
| [maple-character-skill-system.md](references/maple-character-skill-system.md) | Skill definitions, damage formulas |
| [maple-character-skill-reference.md](references/maple-character-skill-reference.md) | Skill ID reference |
| [maple-character-morph-structure.md](references/maple-character-morph-structure.md) | Morph sprite structure |
| [maple-character-tamingmob-structure.md](references/maple-character-tamingmob-structure.md) | TamingMob (mount) structure |
| [maple-character-install-structure.md](references/maple-character-install-structure.md) | Install item structure |
| [maple-field-map.md](references/maple-field-map.md) | Map background & platform structure |
| [maple-field-reactor-structure.md](references/maple-field-reactor-structure.md) | Reactor sprite structure |
| [maple-npc-structure.md](references/maple-npc-structure.md) | NPC sprite structure |
| [maple-pet-structure.md](references/maple-pet-structure.md) | Pet sprite structure |
| [maple-mob-structure.md](references/maple-mob-structure.md) | Mob sprite & stat structure |
| [maple-mob-boss-{name}-structure.md](references/) | Per-boss sprite & attack structure (19 bosses) |

## Workflow

### 1. Read the entry point

```
references/maple-data-reference.md
```

This gives you the Quick Rules table (ID formulas, draw formulas, socket formulas) and the Reference Map that tells you which resource file to load for each domain.

### 2. Load on demand

Only load the resource files relevant to the current task. Use the Reference Map in `maple-data-reference.md` as the selector:

| Task | Load |
|------|------|
| Any sprite rendering | [maple-core-rendering.md](references/maple-core-rendering.md) — always, for all entity types |
| Character with equipment | [maple-character-rendering.md](references/maple-character-rendering.md) |
| Map / background | [maple-field-map.md](references/maple-field-map.md), [maple-core-folder-guide.md](references/maple-core-folder-guide.md) |
| Mob | [maple-mob-structure.md](references/maple-mob-structure.md) |
| NPC | [maple-npc-structure.md](references/maple-npc-structure.md) |
| Skill | [maple-character-skill-system.md](references/maple-character-skill-system.md) |
| Boss | [maple-mob-boss-{name}-structure.md](references/) |
| ID resolution | [maple-core-id-system.md](references/maple-core-id-system.md), [maple-core-id-reference.md](references/maple-core-id-reference.md) |

When a task clearly spans multiple domains, scan all resource file frontmatter descriptions first, then select files to full-load.

### 3. Apply the knowledge

Use the loaded references to:
- Resolve asset file paths from IDs
- Apply origin-based draw positioning and flip rules
- Assemble character socket chains
- Parse mob/skill/map JSON structure
- Integrate with Phaser 3 (via [maple-core-rendering.md](references/maple-core-rendering.md))

## Key Rules (from entry point)

| Rule | Formula |
|------|---------|
| Draw position | `draw_x = world_x - origin.x` / `draw_y = world_y - origin.y` |
| Flip anchor | `anchorX = flip ? (width - origin.x) : origin.x` |
| Socket (no flip) | `childOriginWorld = parentOriginWorld + parentSocket - childSocket` |
| Socket (flip) | `childOriginWorld.x = parentOriginWorld.x - parentSocket.x + childSocket.x` |
| Sprite direction | All sprites face **LEFT** by default — flip explicitly to face right |
| CDN base | `https://resource-static.msu.io/data/` |

## Constraints

- Never hardcode asset paths — always derive from resource files and ID formulas
- Never skip [maple-core-rendering.md](references/maple-core-rendering.md) when writing any draw/flip/socket code
- Never reference files outside `references/` for data structure knowledge
- Do not load all resource files at once — load on demand based on the task
