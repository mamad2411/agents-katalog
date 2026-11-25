---
name: search_catalog
version: 1.0.0
license: MIT
---

# search_catalog

Busca en el catálogo de la tienda. Empareja texto libre contra `name` y
`description`, con filtros opcionales por `category` (exacta) y `max_price`
(inclusivo). Devuelve hasta 10 productos con `sku`, `name`, `price`,
`category` y `stock`.

## Argumentos

- `q` (string, opcional): texto libre contra name y description.
- `category` (string, opcional): categoría exacta, p.ej. `merch` o `hardware`.
- `max_price` (number, opcional): precio máximo inclusivo.

## Ejemplo

```json
{ "q": "mug", "max_price": 20 }
```

El `sku` devuelto es el identificador para `get_product` y `create_order`.