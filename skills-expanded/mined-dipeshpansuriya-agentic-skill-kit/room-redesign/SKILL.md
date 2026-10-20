---
name: room-redesign
description: "Use when the user uploads one room photo and wants a contractor-ready plan (layout, paint, furniture, lighting, budget), not Pinterest ideas. Not for product UI or code."
user-invocable: true
---

# Room redesign (plan, not vibes)

This file is the whole skill. Do not fetch another GitHub tree.

One wide **corner** photo, lights on, so windows, doors and outlets are visible. One photo is enough.

Ask for a **plan**, not ideas. Describe the photo back first so the plan is this room, not a stock one.

## Prompt

```
Here's a photo of my [bedroom]. I want a [warm minimalist / mid-century / Japandi] look.
Describe what's in my photo back to me first, so I know you're designing my room
and not a stock one. Then give me: a layout for this exact space; a color palette
with paint names and hex codes; a furniture list with rough sizes and where each
piece goes; a lighting plan; and 3 decor touches. Work with the windows, doors,
and furniture already visible. Add a rough budget total. If a piece is vague,
say where to buy it for under [budget].
```

## Output

Write `_reports/<date>-room-<slug>.md`:

1. **What I see** (photo contents, including doors/windows/outlets)
2. **Layout** for this floor, no blocked doors
3. **Palette** — paint names + hex
4. **Furniture** — piece, size, placement
5. **Lighting**
6. **Three decor touches**
7. **Budget** — rough total; shoppable substitutes when asked

No finished-room render is required. The shopping list is the deliverable.

This skill produces the plan only. Code or a mock page is a separate development task.
