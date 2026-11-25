---
name: server_time
version: 1.0.0
license: MIT
---

# server_time

Devuelve la hora actual del servidor consultando `/api/time` vía
`host.fetchOrigin`. Es una skill ejecutable async: el handler es `async` y
parsea el JSON devuelto por el origin.

## Respuesta

```json
{ "now": "2026-07-02T12:00:00.000Z", "epoch": 1788254400000 }
```