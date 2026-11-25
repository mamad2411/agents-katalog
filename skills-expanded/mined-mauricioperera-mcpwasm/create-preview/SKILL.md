---
name: create_preview
version: 1.0.0
license: MIT
---

# create_preview

Despliega una app web pequeña en una **cuenta temporal de Cloudflare** que vive
60 minutos. Devuelve una URL pública inmediata y una URL de reclamo para el
humano. Sin credenciales, sin signup, sin cuenta propia: la plataforma crea y
administra la cuenta desechable.

## El flujo completo (lo que el agente debe hacer)

1. **Construye la app** como un módulo ES de Cloudflare Worker (ver abajo).
2. Llama `create_preview` con `{ files, main }`.
3. **Muéstrale al humano AMBAS URLs**:
   - `previewUrl` — para usar la app YA (pública, funciona de inmediato).
   - `claimUrl` — para conservarla: el humano la abre, inicia sesión en
     Cloudflare y la app migra a su cuenta real. Si nadie la reclama antes de
     `claimExpiresAt`, todo se autodestruye en `expiresAt` (60 minutos).
4. Guarda el `sid` de la respuesta: para **re-desplegar sobre la misma cuenta**
   (iteraciones rápidas), pásalo como `sid` en la siguiente llamada.
5. Si el humano no quiere conservarla, llama `discard_preview` para borrarla
   antes del TTL.

## Formato de la app (Cloudflare Worker module)

`main` debe exportar `default { fetch }`. Para una página web, sirve HTML
desde el handler (HTML/CSS/JS inline en un template string):

```js
const page = `<!doctype html><html><body><h1>Hola</h1></body></html>`;
export default {
  async fetch(request) {
    return new Response(page, { headers: { "content-type": "text/html; charset=utf-8" } });
  }
};
```

Puedes responder JSON para APIs, servir rutas distintas con `new URL(request.url)`,
etc. Es un Worker completo, no un hosting de archivos estáticos.

## Límites (duros, del sandbox del agente)

- **Payload total ≤ 16 KB**: `fetchOrigin` del sandbox rechaza bodies mayores.
  Una app de una página con CSS/JS inline entra de sobra. Sin binarios, sin
  assets de build, sin node_modules.
- 1 a 20 archivos.
- Sin secretos: el código es legible por quien tenga la URL y la cuenta muere
  en 60 minutos, pero la URL del preview es **pública**.

## Errores comunes

| Síntoma | Causa | Qué hacer |
|---|---|---|
| `payload exceeds the 16KB limit` | app demasiado grande | un solo módulo, inline, sin assets |
| `main no esta en files` | `main` no coincide con ningún `files[].name` | usa exactamente el mismo nombre |
| `deploy fallo: HTTP 400 ... No such module` | un `import "./x.js"` apunta a un archivo que no enviaste | envía TODOS los archivos importados |
| `sin sesion de preview` al iterar | el sid expiró (>60 min) | llama `create_preview` sin `sid` (cuenta nueva) |
## Requisito del runtime

Esta skill necesita que el runtime haya arrancado con `--previews`:

```
npx -y @rckflr/mcpwasm https://llmstxt-studio.rckflr.workers.dev --previews
```

Sin el flag, la tool devuelve
`{ ok: false, error: "this runtime was not started with --previews..." }`.
El provisioning corre en el host del runtime (Node): el token de la cuenta
temporal nunca entra al sandbox ni al contexto del agente — la tool solo ve
`{sid, previewUrl, claimUrl, expiresAt}`.
