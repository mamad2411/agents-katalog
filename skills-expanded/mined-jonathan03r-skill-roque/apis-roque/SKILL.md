---
name: apis-roque
description: Arquitectura, formato y buenas prácticas para backends y APIs REST en Node.js/TypeScript (Express) estilo Roque. Úsala siempre que vayas a crear, modificar, revisar o depurar código backend Node.js: endpoints, rutas, controllers, schemas de validación, services, middlewares de auth/autorización, manejo de errores, respuestas HTTP, integraciones externas o clientes de API del frontend.
---

# APIs Roque

Reglas para escribir backends Node.js/TypeScript con Express como los genera [Roque-stack](https://github.com/Jonathan03R/Roque-stack). Las instrucciones del usuario, `AGENTS.md`/`CLAUDE.md` y el patrón vigente del repositorio prevalecen sobre esta guía. Para carpetas y helpers compartidos ver también `estructura-backend-roque`; para SQL/RLS, `esquema-roque`.

## Antes de tocar código

1. Lee `AGENTS.md`/`CLAUDE.md` y `docs/REUTILIZABLES.md` si existen.
2. Busca un módulo parecido y copia su forma. No inventes rutas, carpetas ni helpers si ya hay uno equivalente.
3. Define: recurso, actor que puede usarlo, entrada, salida, efectos y errores posibles.
4. No cambies rutas, payloads ni permisos existentes si el pedido no lo pide; el frontend depende de ellos.

## Pipeline de la app

Orden en `app.ts`:

```ts
app.use(requestContextMiddleware);   // requestId + header X-Request-Id
app.use(cors(...));
app.use(express.json());
app.use(httpAccessLogger);           // logs sin payloads sensibles
app.get("/health", ...);
app.use("/api", apiRouter);          // routes/index.ts monta cada módulo
app.use(apiNotFoundMiddleware);      // 404 ROUTE_NOT_FOUND
app.use(apiErrorMiddleware);         // último: todo error termina en apiErrorResponse
```

## Módulo por funcionalidad

```text
src/modules/<modulo>/
├── <modulo>.route.ts        # Router: método, path, middlewares, controller
├── controller/              # entrada HTTP
├── schemas/                 # parse/validación y tipos
└── services/                # DB, APIs externas, archivos
src/middlewares/             # auth, autorización por recurso, errores, request context
src/shared/http/             # apiErrorResponse, PublicApiError, actor context
src/config/                  # env, clientes (supabase, etc.)
```

Nombres de archivo en `kebab-case` por negocio: `agencias-home.controller.ts`, `agencias-home.schema.ts`, `agencias-home.service.ts`.

## Responsabilidad por capa

| Capa | Hace | No hace |
| --- | --- | --- |
| Route | Declara path, encadena `authMiddleware`, identidad y autorización, llama al controller con `.bind` | Lógica de negocio |
| Controller | Parsea `params`/`query`/`body` con el schema, llama al service, arma la respuesta | Consultas a DB, llamadas HTTP externas |
| Schema | Funciones `parseX(value: unknown): Tipo` que validan y normalizan; lanzan error 400 | IO, secretos |
| Service | Consulta DB/APIs, aplica reglas, devuelve datos o `null` | Conocer `req`/`res` |
| Middleware | Autenticación, pertenencia al recurso, request context | Formar respuestas de éxito |

Controller como clase con una instancia exportada:

```ts
class ReservasController {
  async list(request: Request, response: Response): Promise<void> {
    try {
      const query = parseReservasQuery(request.query);
      const data = await reservasService.list(request.authUser!.id, query);
      response.json({ ok: true, data });
    } catch (error) {
      apiErrorResponse({
        req: request,
        res: response,
        error,
        fallbackCode: "RESERVAS_LIST_FAILED",
        fallbackUserMessage: "No se pudieron cargar las reservas.",
      });
    }
  }
}

export const reservasController = new ReservasController();
```

No importes un controller desde otro. Si dos módulos comparten lógica, muévela a un service o a `src/shared`.

## Formato de respuesta

Éxito:

```json
{ "ok": true, "data": { } }
```

- Usa `200` para lecturas y actualizaciones, `201` al crear, `202` para trabajo asíncrono aceptado, `204` sin cuerpo.
- Colecciones grandes: paginación (`limit`, `cursor` u `offset`) y orden estable explícito (`order by fecha_creacion desc, id desc`). Nunca dependas del orden por defecto de la base.
- Devuelve solo los campos que el consumidor necesita. No expongas columnas internas ni secretos.

Error (siempre vía `apiErrorResponse`):

```json
{
  "success": false,
  "status": 404,
  "code": "RESERVA_NOT_FOUND",
  "message": "La reserva no existe.",
  "requestId": "uuid",
  "reportable": false,
  "errors": { }
}
```

- `message`: único texto que ve el usuario. Corto, en español, sin HTML ni detalles técnicos.
- `code`: estable, `MAYUSCULAS_CON_GUION_BAJO`, prefijado por el módulo (`RESERVAS_*`, `AUTH_*`).
- `requestId`: lo pone `requestContextMiddleware`; sirve para rastrear el error en logs.
- `reportable`: `false` para errores esperados del usuario (validación, 404, permisos); `true` para fallos del sistema.
- `errors`: diagnóstico estructurado (campos inválidos, status externo). El frontend no lo renderiza.

Código nuevo no usa `{ ok: false, message }` armado a mano ni decide el status buscando texto en `error.message`. Si tocas un controller antiguo con ese patrón, migra solo lo que cambias.

## Errores

Lanza `PublicApiError` cuando conoces la causa:

```ts
throw new PublicApiError(404, "RESERVA_NOT_FOUND", "La reserva no existe.", false);
throw new PublicApiError(400, "RESERVAS_VALIDATION_ERROR", "fecha debe tener formato YYYY-MM-DD.", false, undefined, { field: "fecha" });
```

| Caso | HTTP | `code` |
| --- | ---: | --- |
| Entrada inválida | 400 | `<MODULO>_VALIDATION_ERROR` |
| Sin sesión o token inválido | 401 | `SESSION_INVALID` |
| Sin permiso sobre el recurso | 403 | `<MODULO>_FORBIDDEN` |
| Recurso no existe | 404 | `<RECURSO>_NOT_FOUND` |
| Conflicto o duplicado | 409 | `<RECURSO>_CONFLICT` |
| Regla de negocio incumplida | 422 | `<MODULO>_<REGLA>` |
| Proveedor externo falló | 502 | `<MODULO>_<PROVEEDOR>_FAILED` |
| Dependencia no disponible | 503 | `<MODULO>_UNAVAILABLE` |
| Error no previsto | 500 | `fallbackCode` del controller |

- Un error se crea una vez, en la capa que conoce la causa. Las demás lo dejan pasar.
- No cambies `api-error-response.ts` para arreglar un solo módulo; corrige el módulo.

## Validación

- Valida `params`, `query` y `body` en el schema antes de cualquier efecto.
- Convierte tipos explícitamente (`Number`, `trim`, fechas) y rechaza valores fuera de rango.
- Campos opcionales vacíos (`""`, `null`) se normalizan a `undefined`.
- No confíes en IDs, roles ni scopes enviados por el cliente.

## Seguridad y autorización

- Toda ruta privada pasa por `authMiddleware`; la identidad se lee de `request.authUser`, nunca del body.
- Comprueba pertenencia al recurso en servidor (middleware `require*` o en el service) antes de leer o escribir datos de otro usuario u organización.
- El cliente admin de Supabase (`service_role`) solo vive en el backend y se usa en services.
- Secretos solo desde `src/config/env.ts`; nunca hardcodeados ni en respuestas.

## Integraciones externas

1. El service hace la llamada y conserva `status` y body originales antes de parsear.
2. Si falla, lanza `PublicApiError` 502 con mensaje humano y los datos originales en `details`.
3. Si el proveedor devuelve HTML, el `message` lleva solo texto visible; el HTML completo queda en `details`.
4. Define timeout y decide si el reintento es seguro (idempotencia) antes de reintentar.

## Logs

- Loguea `requestId`, método, endpoint, status, `code` y usuario; no payloads completos.
- Nunca loguees `authorization`, cookies, contraseñas, tokens, `service_role` ni códigos de invitación.

## Frontend

El cliente muestra solo `error.response.data.message` (o el campo equivalente en Dart/Flutter) y puede guardar `requestId` para soporte. No renderiza `errors`, `details` ni stacks.

## Pruebas

- Tests junto a la unidad: `<archivo>.test.ts`, ejecutados con `tsx --test`.
- Cubre como mínimo: validación inválida (400), sin sesión (401), sin permiso (403) y caso feliz.

## Checklist

- [ ] Ruta con auth y autorización correctas.
- [ ] Schema valida toda la entrada.
- [ ] Controller sin lógica de DB y con `apiErrorResponse` en el `catch`.
- [ ] Errores conocidos como `PublicApiError` con `code` estable.
- [ ] Éxito con `{ ok: true, ... }` y status correcto.
- [ ] Colecciones paginadas y con orden explícito.
- [ ] Sin secretos en respuestas ni logs.
- [ ] Tests nuevos o actualizados; `tsc` y `git diff --check` limpios.
