---
name: create_product
version: 1.0.0
license: MIT
---

# create_product

**Tool de pago**: publica un producto nuevo en el catálogo del marketplace.
Requiere un token de licencia de creador ($19 → 25 listados, 30 días).
Devuelve `{ok: true, sku, name, price, stock, uses_left}` o
`{ok: false, needs_payment: true}` si falta el token.

## El flujo de venta que el agente debe seguir

1. El humano dice que quiere vender algo en la tienda.
2. Llama `buy_creator_access` con el **email del humano** → obtiene un
   `payment_url` (paylink de licencia).
3. **Entrega el paylink al humano**: es SU compra, no la tuya. La página
   muestra el `license_token` tras el pago.
4. El humano te pasa el token. Verifícalo con `check_license` (gratis).
5. Llama `create_product` con `{name, price, access_token, ...}` — y como
   siempre: **confirma nombre, precio y stock con el humano antes**.
6. Reporta el `sku` creado y los `uses_left` restantes.

## Sin token

- Sin `access_token` la tool responde `{ok:false, needs_payment:true}` — no
  insistas: el acceso se compra, no se salta.
- Token inválido/expirado/agotado → el worker responde 401/403 con la causa.

## Errores

| status | significado |
|---|---|
| 400 | validación (name vacío, price negativo) |
| 401 | falta o es inválido el license token (needs_payment) |
| 403 | licencia expirada o sin listados restantes |