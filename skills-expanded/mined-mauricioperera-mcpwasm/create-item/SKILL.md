---
name: create_item
version: 2.0.0
license: MIT
---

# create_item

**Tool de pago** (licencia de creador): crea un item nuevo en el catálogo vivo
(D1). Devuelve `{ok: true, id, name, price, stock}` con `uses_left`, o
`{ok: false, needs_payment: true}` si falta el token de licencia.

## El flujo que el agente debe seguir

1. El humano dice que quiere crear items en la plataforma.
2. Si aún no tiene licencia: llama `buy_creator_access` con el **email del
   humano** → paylink. **El pago es del HUMANO** — entrégale el link y espera.
3. La página del paylink muestra el `license_token` tras pagar; el humano te
   lo pasa. Verifícalo gratis con `check_license`.
4. Confirma nombre, precio y stock con el humano. Recién entonces llama
   `create_item` con `{name, price, access_token}`.
5. Reporta el `id` creado y los `uses_left` restantes.

## Sin token

- Sin `access_token` la tool responde `{ok:false, needs_payment:true}` con el
  `next_step` — no insistas: el acceso se compra, no se salta.
- Token inválido → el worker responde 401 (`needs_payment`).
- Licencia expirada o agotada → 403 con la causa.

## Errores

| status | significado |
|---|---|
| 400 | validación (name vacío, price negativo) |
| 401 | falta o es inválido el license token (needs_payment) |
| 403 | licencia expirada o sin creaciones restantes |