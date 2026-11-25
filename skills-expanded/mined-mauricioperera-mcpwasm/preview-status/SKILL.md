---
name: preview_status
version: 1.0.0
license: MIT
---

# preview_status

Consulta el estado de una sesión de preview creada con `create_preview`.

## Uso

```json
{ "sid": "el-sid-de-create_preview" }
```

Devuelve `{ ok: true, sid, previewUrl, claimUrl, expiresAt, claimExpiresAt,
msToExpiry, accountName, scriptName }`.

`msToExpiry` es el tiempo restante de vida de la cuenta temporal en
milisegundos. Útil para avisarle al humano cuánto le queda antes de que la
app muera si no la reclama. Si la sesión ya expiró o no existe, devuelve
`{ ok: false, error: "session not found (it may have expired)" }` — en ese
caso crea un preview nuevo con `create_preview`.