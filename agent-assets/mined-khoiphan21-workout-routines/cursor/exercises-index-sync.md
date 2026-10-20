---
description: Keep exercises/index.md and equipment/index.md in sync when exercises or equipment change
globs: ["exercises/**/*.md", "equipment/**/*.md"]
alwaysApply: false
---

# Exercise and equipment index sync

When you **add**, **remove**, or **rename** an exercise file in `exercises/` or an equipment file in `equipment/`, you **must** update the relevant index files.

## What to update

1. **exercises/index.md** — When exercises or equipment change:
   - **By muscle group** — Add or remove the exercise from the appropriate muscle group(s): Back, Chest, Shoulders, Triceps, Core, Legs, Skill/holds, Conditioning.
   - **By equipment** — Add or remove the exercise from the appropriate equipment section(s). Equipment sections match the files in `equipment/`.
   - **Reference** — The "General Notes and Warm-up" stays in Reference; other reference-style pages go there.
2. **equipment/index.md** — When equipment is added or removed, add or remove the item from the "All equipment" list.

## Format

- Use the exercise title from the `#` heading in the exercise file.
- Link format: `[Exercise Title](slug)` where slug is the filename without `.md`.
- Equipment links: `[Equipment name](../equipment/slug)`.
