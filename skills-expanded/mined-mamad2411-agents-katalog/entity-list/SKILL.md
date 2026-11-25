---
name: entity-list
description: Enumerate game entity objects. Trigger: entity list, player list, actor list, object enumeration.
tool: Cheat Engine + ReClass
x-alice-class: game
---# entity-list

## Trigger
`entity list, player list, actor list, object enumeration`

## Flow
```
find local player -> trace to container -> output entity struct + iteration code
```

## Script
`scripts/entity_list.py`
