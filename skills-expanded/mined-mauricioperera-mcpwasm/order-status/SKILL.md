---
name: order_status
version: 1.0.0
license: MIT
---

# order_status

Consulta una orden por su id numérico. Devuelve
`{found: true, order: {order_id, sku, qty, email, total, status, created_at}}`
o `{found: false}`.

## Argumentos

- `order_id` (number, requerido): el id que devolvió `create_order`.

## Cuándo usarla

Después de una compra con respuesta dudosa (timeout, error de red): confirma
si la orden existe antes de reintentar `create_order`. Y para darle al humano
el estado actualizado de una compra previa.