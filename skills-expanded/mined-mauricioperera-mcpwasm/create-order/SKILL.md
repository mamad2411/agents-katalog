---
name: create_order
version: 1.0.0
license: MIT
---

# create_order

Crea una orden por un producto, decrementando el stock **atómicamente** en
una transacción D1. Devuelve `{ok: true, order_id, sku, qty, total,
remaining_stock, payment_url}` o `{ok: false, status: 409, error}` si el sku
no existe o el stock no alcanzó.

## El flujo de compra que el agente debe seguir

1. `search_catalog` (o `get_product`) para elegir el producto y su `sku`.
2. **Confirma con el humano** antes de comprar: producto, cantidad, precio y
   el email al que va la orden. Comprar es un efecto en el mundo real — nunca
   invoques esta tool sin un OK explícito del humano.
3. Llama `create_order` con `{sku, qty, email, client_order_id}`.
4. **Genera un `client_order_id` único por intención de compra** (p.ej. un
   UUID). Si un reintento o error de red te deja dudoso, repite la llamada con
   el MISMO `client_order_id`: la API devuelve la orden original
   (`idempotent: true`) en vez de duplicarla.
5. **Entrega al humano el `payment_url`** que devuelve la tool: es el paylink
   (página de pago simulada en este demo) que marca la orden como `paid`.
   El pago es del HUMANO — no lo ejecutes por tu cuenta salvo petición
   explícita. El estado pasa de `confirmed` a `paid`.
6. Reporta al humano: `order_id`, `total`, `remaining_stock` y el paylink.

## Idempotencia

- `client_order_id` es una clave de deduplicación del CLIENTE.
- Misma clave → misma orden, siempre (200, `idempotent: true`, mismo
  `payment_url`).
- Clave distinta → orden nueva (aunque sea el mismo producto).
- Sin clave → cada llamada crea una orden nueva. Para agentes: SIEMPRE mandar
  la clave.

## Errores

| status | significado |
|---|---|
| 400 | validación (email inválido, qty no entera, sku vacío) |
| 409 | sku desconocido o `insufficient stock` (trae `requested`/`available`) |