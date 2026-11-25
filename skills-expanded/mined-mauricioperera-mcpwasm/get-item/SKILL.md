---
name: get_item
version: 1.0.0
license: MIT
---

# get_item

Detalle de un item por id numérico: name, description, price, stock.
Devuelve `{found: false}` si el id no existe. **Lectura pública** — sin
aprobación humana.

## Cuándo usarla

- Antes de una escritura, para verificar precios/stock del item elegido.
- Después de un error de red durante `create_item`, para confirmar si la
  escritura aterrizó realmente antes de reintentar.