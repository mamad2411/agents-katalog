---
name: list_items
version: 1.0.0
license: MIT
---

# list_items

Lista items del catálogo con filtro opcional de texto. **Lectura pública** —
el agente puede usarla libremente, sin aprobación humana.

## Uso

- `list_items` → hasta 10 items (id, name, description, price, stock).
- `list_items {q: "widget"}` → filtra por texto en name/description.
- `list_items {limit: 3}` → límite explícito (máx 50).

## Cuándo usarla

Para descubrir qué existe antes de proponer cualquier escritura. Es el paso
seguro: no tiene efectos en el mundo real.