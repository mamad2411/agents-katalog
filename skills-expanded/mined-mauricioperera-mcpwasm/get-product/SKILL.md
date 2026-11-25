---
name: get_product
version: 1.0.0
license: MIT
---

# get_product

Detalle completo de un producto por su `sku`: name, description, category,
price y **stock en vivo**. Devuelve `{found: false}` si el sku no existe.

## Argumentos

- `sku` (string, requerido): p.ej. `wasm-mug`.

## Cuándo usarla

Antes de crear una orden grande: el `stock` que devuelve `search_catalog`
puede estar desactualizado (otro agente pudo comprar mientras tanto);
`get_product` da el valor vivo y `create_order` es quien decide al final con
su 409 si el stock ya no alcanzó.