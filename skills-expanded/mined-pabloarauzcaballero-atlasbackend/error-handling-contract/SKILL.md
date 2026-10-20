---
name: error-handling-contract
description: Contrato de errores de la API — errores de dominio y su mapeo a HTTP (400, 401, 403, 404, 409, 412, 422, 428, 429, 5xx) con criterio, problem details (RFC 9457), códigos estables para el cliente, traducción de errores de base y ORM, exception filter único en NestJS, y nada de stack, SQL ni datos de pacientes en la respuesta. Usar al crear una excepción de dominio, decidir qué status devuelve un caso, escribir o revisar un exception filter, documentar errores en OpenAPI, o cuando el front no distingue dos fallos.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Contrato de errores

Un error es parte del **contrato público**: el cliente programa contra él. `backend-development`
fija el formato (problem details); esta skill fija **qué** error, **qué** status y **qué**
código, y dónde se traduce. El filtro de Nest en sí está en `nestjs-development`.

## 1. Dos clases de fallo, dos tratamientos

| | Error **esperado** (de dominio) | **Bug / fallo de infraestructura** |
|---|---|---|
| Ejemplo | turno ocupado, versión vieja, sin permiso | `TypeError`, base caída, timeout de un tercero |
| Tipo | excepción de dominio tipada | cualquier otra cosa |
| Status | 4xx específico | 500 / 502 / 503 / 504 |
| Log | `info`/`warn`, sin stack | `error` con stack + alerta |
| `detail` al cliente | específico y accionable | genérico |

- El dominio lanza excepciones **propias** (`AppointmentOverlapError`), sin conocer HTTP.
  La traducción a HTTP ocurre en **un solo lugar** (filtro global). Un `throw new
  HttpException(...)` dentro de un servicio de dominio acopla la regla al transporte.
- No uses excepciones para el flujo normal: "no hay resultados" es `200` con lista vacía.

## 2. Qué status, con criterio

| Status | Cuándo | No lo uses para |
|---|---|---|
| **400** | Request mal formada: JSON inválido, tipo incorrecto, falta un campo, formato de fecha | reglas de negocio |
| **401** | No hay credencial válida (ausente, vencida, firma inválida). Lleva `WWW-Authenticate` | "autenticado pero sin permiso" |
| **403** | Autenticado, pero la acción no le está permitida a su rol | ocultar existencia (ver 404) |
| **404** | No existe **o** existe pero no es de su tenant/no puede saber que existe | errores de ruta interna |
| **409** | Conflicto con el **estado actual** del recurso: duplicado, solapamiento, transición inválida desde el estado actual, idempotency key en curso | validación de campos |
| **412** | Precondición del request falló: `If-Match`/versión no coincide | conflictos sin precondición explícita |
| **422** | Sintaxis correcta, **semántica** inválida: regla de negocio sobre el contenido (fin antes que inicio, monto fuera de rango, key reutilizada con otro payload) | JSON roto |
| **428** | La mutación exige precondición (`If-Match`/versión) y no vino | — |
| **429** | Límite de tasa. Lleva `Retry-After` | sobrecarga del servidor (503) |
| **500** | Bug. Siempre genérico | errores esperados |
| **502/504** | Un upstream respondió mal / no respondió | bugs propios |
| **503** | No disponible temporalmente (mantenimiento, dependencia crítica caída). `Retry-After` | — |

Reglas de desempate:

- **403 vs 404 sobre recurso ajeno**: si revelar que existe es una fuga (historia clínica
  de otro paciente, recurso de otro tenant), respondé **404**. Decidilo por tipo de
  recurso y sé consistente (ver `authz-access-control`).
- **400 vs 422**: ¿un validador de esquema lo detecta sin conocer el negocio? → 400. ¿Hace
  falta estado o una regla del dominio? → 422. Elegí la convención de validación de DTO
  (400 **o** 422) una vez por API y no la mezcles.
- **409 vs 412**: si el cliente mandó una precondición explícita y falló → 412. Si el
  conflicto surge del estado sin que el cliente lo haya condicionado → 409.
- Nunca `200` con `{ "success": false }`. Nunca `500` para un error esperado.

## 3. Forma: problem details + código estable

`Content-Type: application/problem+json` (RFC 9457, reemplaza a la 7807). Miembros
estándar: `type`, `title`, `status`, `detail`, `instance`. Extensiones de la casa:

```json
{
  "type": "https://errors.example.com/appointment-overlap",
  "title": "El horario ya no está disponible",
  "status": 409,
  "code": "APPOINTMENT_OVERLAP",
  "detail": "El profesional tiene otra cita entre 10:00 y 10:30.",
  "instance": "/appointments",
  "traceId": "c1f0…",
  "errors": [{ "field": "startsAt", "code": "SLOT_TAKEN", "message": "Horario ocupado" }]
}
```

- **`code`** es el contrato: `SCREAMING_SNAKE`, estable, único, **nunca se renombra** (eso
  es breaking). El front decide por `code`, jamás parseando `title`/`detail`.
- `title` es estable por tipo; `detail` es específico de la ocurrencia y puede cambiar.
- `errors[]` para validación por campo: `field` con la ruta del DTO (`items[2].amount`),
  así el formulario asocia el error al input (ver `frontend-forms-ux`).
- `traceId` siempre: es lo que el usuario le pasa a soporte (ver `backend-observability`).
- Textos para el usuario final: el front los resuelve por `code` (i18n del lado cliente);
  `title`/`detail` son fallback (ver `frontend-i18n-l10n`).

## 4. Lo que nunca sale en un error

- Stack trace, nombre de clase interna, ruta de archivo, versión de librería.
- SQL, nombre de tabla/constraint, mensaje crudo del driver (`duplicate key value
  violates unique constraint "uq_…"`).
- **PII**: documento, nombre de paciente, diagnóstico, email de un tercero. Ni en
  `detail` ni en el log del error (ver `data-privacy-sensitive`). Referí por id opaco.
- Pistas de enumeración: "el email existe pero la contraseña es incorrecta" → mensaje
  único para login y recuperación (ver `authn-identity`).
- En 5xx el cuerpo es genérico + `traceId`. El detalle completo va al log del servidor.

## 5. Traducir errores de infraestructura en el borde

Los errores de base y de ORM se convierten a excepciones de dominio en la capa de
persistencia/caso de uso, por **SQLSTATE + nombre de constraint**, nunca por texto.

| Origen | Dominio → HTTP |
|---|---|
| `23505` unique_violation (constraint conocida) | `…AlreadyExistsError` → 409 |
| `23P01` exclusion_violation | `…OverlapError` → 409 |
| `23503` foreign_key_violation (referencia del cliente) | `…ReferenceNotFoundError` → 422 |
| `23514` check_violation | regla de dominio → 422 (si llegó hasta acá, faltó validar antes) |
| `OptimisticLockError` del ORM | `StaleVersionError` → 412 / 409 |
| `NotFoundError` del ORM (`findOneOrFail`) | `…NotFoundError` → 404 |
| `40001` / `40P01` agotados los reintentos | 503 con `Retry-After` |
| constraint **desconocida** | 500 + alerta: es un caso no modelado |

```typescript
// ❌ filtra la constraint y acopla el cliente al esquema
throw new ConflictException(dbError.message);

// ✅ traducción por código, mensaje propio
if (isUniqueViolation(e, 'uq_appointment_request')) throw new DuplicateRequestError(requestId);
throw e; // lo no reconocido sigue siendo un bug
```

## 6. El filtro: un solo punto de traducción

- Un mapa `código de dominio → { status, type, title }` declarado con `satisfies` para que
  agregar un error sin mapearlo no compile (ver `typescript-standards`).
- Orden del filtro global (`@Catch()`): excepción de dominio → mapa; `HttpException` del
  framework (incluida la de validación) → normalizada al mismo formato; **todo lo
  demás** → 500 genérico, log `error` con stack y `traceId`.
- La respuesta de validación del `ValidationPipe` se reescribe a `errors[]`: que el
  cliente no tenga dos formatos.
- Guards, pipes e interceptors producen el **mismo** formato. Probalo: un 401, un 403, un
  400 de validación y un 404 de ruta inexistente deben ser `application/problem+json`.
- `catch` vacío prohibido. `catch` que loguea y sigue, solo si degradar es una decisión
  de producto documentada. No loguees **y** relances en cada capa: un error, un log.

## 7. Documentarlo en OpenAPI

- Un schema `Problem` reutilizable por `$ref`, y por operación las respuestas de error
  **que realmente puede dar**, cada una con ejemplo y su `code` (ver `api-openapi-docs`).
- El catálogo de `code` es un artefacto versionado (enum en el spec o tabla en la doc):
  agregar es compatible; renombrar, cambiar status o quitar es **breaking**.

## Anti-patrones

- `throw new Error('algo falló')` sin tipo; `HttpException` lanzada desde el dominio.
- El front hace `if (message.includes('ya existe'))`.
- Propagar `error.message` del driver al cliente.
- 500 por turno ocupado; 400 para todo; 200 con `success: false`.
- 403 que confirma que existe el expediente de otra persona.
- Dos formatos de error según pase o no por el `ValidationPipe`.

## Checklist

- [ ] Cada fallo esperado es una excepción de dominio tipada, sin dependencia de HTTP.
- [ ] Status elegido con la tabla §2; convención 400/422 y 409/412 única en toda la API.
- [ ] Respuesta `application/problem+json` con `code` estable y `traceId`.
- [ ] Validación por campo en `errors[]` con ruta de campo.
- [ ] Sin stack, SQL, nombres de constraint ni PII en el cuerpo ni en el mensaje logueado.
- [ ] Errores de base traducidos por SQLSTATE + constraint; lo desconocido → 500 con alerta.
- [ ] Un único filtro global; guards/pipes/404 de ruta devuelven el mismo formato.
- [ ] Cada operación documenta en OpenAPI sus errores reales con ejemplo.
- [ ] Test por cada error esperado: status + `code` (ver `api-testing`).
