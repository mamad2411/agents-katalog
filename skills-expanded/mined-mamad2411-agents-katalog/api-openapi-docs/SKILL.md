---
name: api-openapi-docs
description: Documentación profesional de APIs con OpenAPI 3.1 — contract-first vs code-first, operationId, tags, reutilización con $ref, ejemplos, respuestas de error con problem+json, esquemas de seguridad, paginación, versionado/deprecación, linting con Spectral y detección de breaking changes. Usar al escribir o revisar un spec OpenAPI, documentar un endpoint nuevo, o antes de publicar/versionar una API pública o interna.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Documentación de API con OpenAPI

Cómo mantener un contrato OpenAPI 3.1 profesional, legible por humanos y por
herramientas. Para el modelo de errores y versionado a nivel de arquitectura, ver
`backend-development`. Para NestJS específicamente, ver `nestjs-development` §8
(`@nestjs/swagger`). Para auditar la **seguridad** de un spec ya escrito (SQG,
autenticación, exposición de datos), usá las skills `42crunch-audit`/`42crunch-scan` —
no dupliques ese trabajo acá.

## 1. Contract-first vs code-first

| Enfoque | Cuándo | Riesgo si no se cuida |
|---|---|---|
| Contract-first: el `.yaml` es la fuente de verdad, el código se genera/valida contra él | APIs públicas, múltiples equipos consumiendo, contratos que se negocian antes de codear | el código puede desviarse del contrato si no hay validación automática |
| Code-first: el spec se genera desde decoradores/anotaciones en el código (`@nestjs/swagger`) | equipo único, iteración rápida, API interna | el spec documenta lo que el código hace, no necesariamente lo que debería — fácil arrastrar un mal diseño a la doc |

- Sea cual sea el enfoque, el spec generado/escrito se **valida en CI** contra el
  código real (o el código contra el spec) — un contrato desincronizado es peor que
  no tener contrato, porque miente con autoridad.

## 2. Estructura del contrato

- Un `operationId` único y estable por operación (`getOrderById`, no `get1`) — lo usan
  generadores de clientes y SDKs; renombrarlo es un breaking change para esos consumidores.
- `tags` agrupan operaciones por recurso/dominio (`Orders`, `Users`), no por verbo HTTP.
- `summary` corto + `description` con el detalle (reglas de negocio relevantes, quién
  puede llamarlo) — no dupliques el nombre de la operación como resumen.
- Reutilizá con `$ref` (`#/components/schemas/...`) en vez de repetir el mismo objeto
  en cada respuesta: un DTO cambia una vez, no en N lugares del spec.
- **Examples** (`examples` o `example` en cada schema/response) para cada caso relevante:
  éxito, y al menos un error típico. Un spec sin ejemplos es una referencia incompleta.

## 3. Errores

- Respuestas de error con `Content-Type: application/problem+json` (RFC 9457), un
  schema compartido (`ProblemDetails`) referenciado desde cada operación — no un shape
  de error distinto por endpoint.
- Documentá **todos** los códigos de error posibles de la operación, no solo `200`/`201`:
  `400` (validación), `401`/`403` (auth), `404`, `409` (conflicto), `422`, `429`
  (rate limit), `500` — cada uno con su `$ref` al schema de error y un ejemplo.

```yaml
responses:
  '404':
    description: Order not found
    content:
      application/problem+json:
        schema:
          $ref: '#/components/schemas/ProblemDetails'
        example:
          type: https://api.example.com/errors/not-found
          title: Order not found
          status: 404
          instance: /orders/8f14e
```

## 4. Seguridad, paginación, versionado

- Declará `securitySchemes` (`bearerAuth`, `apiKey`, `oauth2`) en `components` y
  aplicalos por operación con `security` — no dejes implícito qué requiere autenticación.
- Documentá parámetros de paginación (`cursor`/`page`, `limit`) y el shape de la
  respuesta paginada como un schema reutilizable (ver `backend-development` §5).
- Versioná el `info.version` del documento junto con la API; marcá operaciones
  obsoletas con `deprecated: true` y explicá el reemplazo en la `description` —
  no borres una operación deprecada del spec sin el período de aviso acordado.

## 5. Linting y breaking changes

- Corré un linter de OpenAPI (Spectral u equivalente) en CI con un ruleset que exija:
  `operationId` presente, todas las responses de error documentadas, `$ref` en vez de
  esquemas inline duplicados, ausencia de esquemas sin `description`.
- Detectá breaking changes automáticamente comparando el spec del branch contra el de
  `main`/la versión publicada (herramienta de diff de OpenAPI) antes de mergear: quitar
  un campo, volver requerido un campo opcional, angostar un enum, o cambiar un tipo son
  breaking aunque el código "funcione".
- Un campo nuevo opcional, una operación nueva, o un enum que se amplía no son breaking
  — no bloquees esos cambios con el mismo criterio.

## Anti-patrones

- Spec generado una vez y nunca vuelto a sincronizar con el código.
- Mismo shape de error definido inline en cada operación en vez de un `$ref` compartido.
- `operationId` autogenerado y cambiante entre builds (rompe SDKs generados).
- Eliminar un campo o angostar un enum sin pasar por deprecación ni bump de versión.
- Publicar un spec sin ejemplos, dejando que el consumidor adivine el shape real.

## Checklist

- [ ] El spec se valida contra el código real en CI (no confiar en que "quedó igual").
- [ ] Todo schema repetido está en `components` y referenciado con `$ref`.
- [ ] Toda operación documenta sus respuestas de error relevantes con `application/problem+json`.
- [ ] `securitySchemes` declarados y aplicados por operación.
- [ ] Paginación documentada con un schema reutilizable.
- [ ] Deprecaciones marcadas con `deprecated: true` y explicadas, con período de aviso.
- [ ] Linter de OpenAPI corriendo en CI.
- [ ] Diff de breaking changes corriendo en CI antes de mergear un cambio de contrato.
- [ ] Para exposición pública, pasar además por `42crunch-audit`/`42crunch-scan`.
