---
name: check_license
version: 1.0.0
license: MIT
---

# check_license

Consulta el estado de un token de licencia de creador: plan, listados
restantes (`uses_left`), vencimiento. **Gratis** — sin aprobación humana.

## Cuándo usarla

- Antes de `create_product`, para verificar que el token del humano está
  activo y tiene usos disponibles.
- Para decirle al humano cuántos listados le quedan.
- Si `create_product` falló con 401/403, para distinguir token inválido de
  licencia agotada.