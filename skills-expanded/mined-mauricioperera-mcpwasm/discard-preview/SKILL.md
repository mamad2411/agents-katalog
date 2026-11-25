---
name: discard_preview
version: 1.0.0
license: MIT
---

# discard_preview

Borra un preview AHORA en vez de esperar el TTL de 60 minutos: elimina el
worker desplegado de la cuenta temporal y descarta la sesión.

## Uso

```json
{ "sid": "el-sid-de-create_preview" }
```

Devuelve `{ ok: true, deleted: true, scriptName }`.

Cuándo usarla: el humano decide no conservar el preview, o el agente termina
de iterar y quiere dejar la cuenta limpia. Si nadie llama y nadie reclama, el
preview muere solo al cumplirse el TTL — esta tool solo lo adelanta.