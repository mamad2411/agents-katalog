---
name: claim_preview
version: 1.0.0
license: MIT
---

# claim_preview

Conserva un deploy más allá del TTL de la cuenta temporal (60 min): inicia el
**claim hosted** — $19 por 30 días (simulado por ahora). La tool es gratis; el
pago es del humano.

## El flujo que el agente debe seguir

1. El humano dice que quiere quedarse el deploy que su agente construyó.
2. Llama `claim_preview` con `{sid, email}` (el sid viene de `create_preview`)
   → obtiene un `payment_url` (paylink de claim).
3. **Entrega el paylink al humano**: es SU compra — nunca la ejecutes por tu
   cuenta salvo petición explícita.
4. Tras pagar, el deploy queda **reclamado**: TTL extendido a 30 días y el
   estado (`preview_status`) refleja `claimed` con el email del dueño.
5. Reporta al humano: confirmación y nueva fecha de expiración.

## Claim nativo de Cloudflare (gratis)

Además de este claim hosted, la sesión siempre trae la `claimUrl` nativa de
Cloudflare: transferir la cuenta temporal a la cuenta propia del humano. Es
GRATIS y el agente puede compartirla — el claim de pago conserva el deploy
EN la plataforma (hosted); el nativo lo exporta.

## Errores

| status | significado |
|---|---|
| 400 | email del humano faltante o inválido |
| 404 | la sesión no existe (TTL vencido o sid incorrecto) |