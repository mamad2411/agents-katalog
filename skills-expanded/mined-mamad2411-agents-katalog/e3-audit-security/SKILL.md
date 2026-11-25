---
name: e3-audit-security
description: Use this skill for EOS Entrega 3 Módulo 4 — auditoría (emisor y lectura) y checklist de seguridad transversal (RBAC, cifrado en tránsito, exposición de errores).
---

# e3-audit-security

Use this skill only for Módulo 4 — Auditoría & Seguridad Transversal (E3-RF-06 + RNF-Seguridad).

## Scope

Implemented so far:

1. Emisor `recordAuditLog` (best-effort, ya existía antes de esta skill).
2. Lectura filtrable `GET /api/admin/audit-log`, con búsqueda por nombre de actor (`actorName`, `ilike` sobre `profiles.full_name`).
3. Panel de lectura `app/(tabs-admin)/audit-log.tsx`.
4. Tests unitarios del service/controller de `audit`.
5. Emisores de `user_profile`/`specialist_profile` agregados en `auth.service.ts` (registro), `profile.service.ts` (edición), `specialists.registration.service.ts` (alta de especialista) y `admin.service.ts` (aprobar/rechazar especialista) — ver sección "M2 - Identidad y Perfil" en `docs/e3-contracts.md` para el detalle de cada call-site.
6. **Consolidación de auditoría de rutinas**: crear una rutina (nombre + horario + pasos, todo en el wizard) o editarla ya no genera una fila por cada llamada al backend — `recordRoutineAudit` en `routines.service.ts` fusiona todo en un solo registro de `audit_logs` mientras ocurra dentro de una ventana de 3 minutos (`ROUTINE_BATCH_WINDOW_MS`). Sin límite de cantidad de pasos. Ver sección "M1 - Rutinas Avanzadas" en `docs/e3-contracts.md` para el mecanismo completo.
7. Emisores agregados para cobertura de eventos reportados por QA manual: reintento de test de piel (`quiz.controller.ts`, `entity: 'skin_profile'`), creación/edición/baja de rutina (`routines.service.ts`, ahora vía el mecanismo del punto 6), asignación de rutina por especialista (mismo mecanismo, `metadata.assignedBy`), vínculo/desvínculo con especialista (`specialists.directory.service.ts`, `entity: 'specialist_relation'`), creación/edición/baja de centro (`centers.service.ts`), baja de producto (`products.service.ts`, sus 3 flujos: `remove`/`forceRemove`/`replaceInRoutines`).

Not implemented yet (ver "Pendiente" abajo):

- T4.6 auditoría de **login** exitoso/fallido y **cambio de rol** explícito (creación/edición de perfil ya está cubierta, ver punto 5 arriba).
- T4.7 revisión de RBAC estricto en las rutas nuevas de M1/M2/M3/M5 (se verificó puntualmente `admin`/`profile`/`specialists`/`auth`, no una auditoría formal de las 5 áreas).
- T4.8 revisión de cifrado en tránsito / headers de seguridad — confirmado que no hay `helmet` ni equivalente en `backend/src/app.ts`.
- T4.9 revisión de exposición de errores en módulos nuevos.
- RLS de `audit_logs` (ver `docs/e3-supabase-security.md`, sección "audit_logs - estado real").
- Suscripciones de centro y baja (deactivate) de cuenta de usuario/especialista: no existe el flujo de negocio, fuera de alcance hasta que se construya (confirmado con la usuaria).

Do not implement (fuera de M4):

- M1 wizard/performance de rutinas.
- M2 auth federada.
- M3 CRUD de centros (ya completo).
- M5 planes/reportes.

## Branch

Use or suggest:

```text
feature/e3-m4-audit-log-read
```

## Backend

Módulo: `backend/src/modules/audit/`

```text
audit.types.ts        — AuditAction, AuditEntity (incluye skin_profile, specialist_relation), RecordAuditLogParams, AuditLogRow, AuditLogEntry (+ actorName/actorProfile/entityLabel/routineStepDetails[]/routineChange), AuditLogFilters, AuditLogPage
audit.repository.ts    — auditRepository.findAuditLogs(filters) + lookups batched (findProfileNamesByIds, findCenterNamesByIds, findRoutineNamesByIds, findProductNamesByIds, findSpecialistProfileRows, findSpecialtyByUserIds, findSubscriptionRows, findSubscriptionPlanNamesByIds, findStepsWithProducts, findProfileIdsByRole, findProfileIdsByNameSearch) + findRecentRoutineBatch/updateRoutineBatch (usadas solo por routines.service.ts para consolidar auditoría de rutinas)
audit.service.ts       — recordAuditLog (emisor, no tocar su contrato) + getAuditLogs (lector, normaliza filtros y pagina) + enrichAuditLogEntries (resuelve actor/entidad/pasos de rutina + cambios de la rutina/owner de suscripción) + isIsoDate
audit.controller.ts    — GET / -> getAuditLogs, parsea query params como strings
audit.routes.ts        — authenticate + requireRole('center_admin') + GET /
tests/audit.service.test.ts
tests/audit.controller.test.ts
```

Montado en `backend/src/app.ts` como `app.use('/api/admin/audit-log', auditRouter)`.

### Enriquecimiento en `enrichAuditLogEntries`

- **Actor**: `actorName` (nombre real) + `actorProfile` ("Usuario" / "Especialista - {specialty}" / "Administrador de Centro"), resuelto contra `profiles`/`specialist_profiles`.
- **Entidad afectada**: `entityLabel` se resuelve primero contra la tabla en vivo; si el registro ya no existe (`delete`), cae a `deriveFallbackEntityLabel`, que deriva el nombre desde el `before`/`after` guardado en el propio evento.
- **Rutina consolidada** (M1): si `metadata.changeType === 'routine_batch'` (o los shapes legacy `routine_step_batch`/`routine_step`, ver retrocompatibilidad en `docs/e3-contracts.md`), arma `routineStepDetails` (array, uno por paso — categoría, nombre, `hasProducts` resuelto contra `routine_step_products`, proxy del estado *actual* del paso porque `attachProductToStep`/`detachProductFromStep` no emiten `recordAuditLog`) y `routineChange` (`before`/`after` de la rutina en sí, si el batch incluye un cambio de la rutina y no solo de pasos).
- **Suscripciones**: `owner_id`/`ownerId` se reemplaza por `owner` (nombre resuelto vía `profiles` o `centers` según `owner_type`) antes de devolver `before`/`after` — no se expone el id crudo del titular.
- **Filtro `entity=user_profile`**: antes de consultar `audit_logs`, resuelve los ids de `profiles` con `role='user'` (`findProfileIdsByRole`) y los pasa como `entityIdIn`, para no traer eventos de perfiles de especialista/admin bajo ese filtro.
- **Filtro `actorName`**: resuelve `profiles.full_name ilike '%query%'` (`findProfileIdsByNameSearch`) y pasa los ids como `actorIdIn`. Reemplaza a los filtros `entityId`/`actorId` (match exacto por uuid) en la pantalla — esos dos quedaron rotos para uso real porque el usuario intentaba escribir un nombre ahí y Postgres tiraba `invalid input syntax for type uuid`.

### Contrato de lectura

```text
GET /api/admin/audit-log?entity=&entityId=&actorId=&actorName=&from=&to=&page=&limit=
```

Ver `docs/e3-contracts.md`, sección "M4 - Auditoria y Seguridad Transversal", para el contrato completo (query params, shape de respuesta, reglas de validación). No hay rol `admin`/`platform_admin` en el sistema — el endpoint usa `requireRole('center_admin')` igual que `/api/admin/*` y `/api/centers`.

### Reglas al extender el service

- `recordAuditLog` es best-effort (nunca lanza). No cambiar ese comportamiento al tocar el archivo.
- `getAuditLogs` sí valida y lanza `ApiError(400, ...)` en español ante filtros inválidos — es un endpoint de lectura protegido, no un emisor best-effort.
- El repository devuelve filas snake_case (`AuditLogRow`); el service las mapea a camelCase (`AuditLogEntry`) antes de responder, igual que `centersService.toCenterSummary`. No exponer snake_case en la respuesta HTTP.
- `normalizePositiveInt(value, fallback, max)` recorta el valor parseado a `Math.min(parsed, max)`. **Cuidado con el `max` de `page`**: hubo un bug donde se pasaba `1` como `max` (`normalizePositiveInt(rawFilters.page, 1, 1)`), lo que forzaba cualquier página pedida a quedar en `1` — "Siguiente" nunca avanzaba. `page` no tiene un tope real, solo `limit` lo tiene (`MAX_PAGE_SIZE`); usar `Number.MAX_SAFE_INTEGER` como `max` de `page`.
- `recordRoutineAudit` (en `routines.service.ts`, no en el módulo `audit`) es la única excepción al patrón "un `recordAuditLog` = una fila nueva": busca/actualiza filas recientes vía `auditRepository.findRecentRoutineBatch`/`updateRoutineBatch` antes de decidir si inserta. Si se agrega un caso nuevo de mutación de rutina, pasarlo por esta función (no llamar a `recordAuditLog` directo para `entity: 'routine'`), o se vuelve a romper la consolidación.

## Frontend

```text
types/audit.ts          — AuditAction, AuditEntity, AuditLogEntry (espejo del tipo backend, incluye routineStepDetails[] y routineChange), AuditLogFilters, AuditLogPage
services/audit.ts        — getAuditLogs(filters), getAuditLogErrorMessage(error)
app/(tabs-admin)/audit-log.tsx — pantalla de lectura con filtros (entity, nombre del actor, rango de fechas) y paginación anterior/siguiente
```

Dependencia agregada: `@react-native-community/datetimepicker` (instalada vía `npx expo install`, no `npm install`, para mantener compatibilidad con Expo SDK 54).

Navegación: tarjeta "Auditoría" en `app/(tabs-admin)/index.tsx`, ruta `routes.adminAuditLog` (`constants/routes.ts`). `app/(tabs-admin)/_layout.tsx` es un `Stack`, no un tab bar — no hace falta declarar la pantalla en una lista de tabs, solo el archivo y el link de navegación.

Reusa `components/Card.tsx`, `constants/colors.ts`, sin introducir estilos nuevos. Sigue el patrón de `app/(tabs-admin)/plans.tsx` (loadData con `useCallback` + `useFocusEffect`, estados de loading/error/vacío explícitos).

### Tarjeta de cada evento

- Meta grid con 4 items: `Actor`, `Perfil`, `Registro` (= `entityLabel`), `Fecha` — todo lo que antes vivía repetido en distintos recuadros del detalle ahora se muestra una sola vez, acá.
- El detalle expandible (`AuditLogCard`) se arma distinto según `entry.action`, usando `entry.routineChange` en vez de `entry.before`/`entry.after` cuando está presente (filas consolidadas de rutina no tienen `before`/`after` a nivel de fila):
  - `delete` → `DeleteSummaryBlock`: una sola línea, "Elemento eliminado" (actor y fecha ya están en el meta grid, no se repiten).
  - `create` → `CreateBlock`: campos de `routineChange.after` (o `after`) vía `FieldValue`.
  - resto con diff → `UpdateDiffBlocks`: dos recuadros, "Antes" y "Después", solo con los campos que cambiaron (`buildDiffRows`).
  - `entry.routineStepDetails` (si no es `null`/vacío) → `RoutineStepBlock`, con **todos** los pasos del array (sin límite), independientemente de `action` — puede aparecer junto con `CreateBlock`/`UpdateDiffBlocks` en la misma tarjeta cuando la rutina y sus pasos se consolidaron en el mismo registro.
- `FieldValue` es recursivo: valores anidados (ej. el plan de una suscripción, y dentro sus `features`) se muestran como bullets indentados por nivel, no como una línea aplanada.
- `HIDDEN_FIELD_KEYS` (en el mismo archivo) filtra campos que no deben mostrarse crudos: `id`, `created_at`/`updated_at`, `plan_id`, `owner_id`, `routine_id` (y sus variantes camelCase) — se ocultan en cualquier nivel de anidación porque son ruido o datos sensibles (UUIDs sin nombre resuelto), o porque ya se muestran en otro lado (ej. `entityLabel` arriba).

### Paginación

- Cambiar de página no navega con `router` — es estado local (`page`/`limit`/`total` en `AuditLogScreen`) más `getAuditLogs({ page })`.
- `goToPage(targetPage)` centraliza el cambio: hace `listRef.current?.scrollToOffset({ offset: 0 })` **antes** de lanzar `loadData`, para que el scroll sea instantáneo al tocar el botón y no recién cuando la respuesta llega (si se scrollea reactivamente en un `useEffect` atado a `page`, el usuario queda 1-2s viendo la página vieja porque `page` solo cambia después del `await`).
- Mientras `isLoading` es `true` y ya había datos (`entries.length > 0`), el `ListFooterComponent` reemplaza los botones de paginación por un spinner ("Cargando página...") en vez de desaparecer — si no, el usuario pierde el feedback de carga al estar scrolleado cerca del pie.

## Tests

Tests en español, estilo `centers.service.test.ts` / `centers.controller` (mock del repository/service con `jest.mock`, `jest.mocked`, factories `makeAuditLog(overrides = {})`).

Casos cubiertos en `backend/src/modules/audit/tests/`:

- Filtros vacíos usan defaults de paginación (`page=1`, `limit=10`).
- Filtros de `entity`/`entityId`/`actorId` se pasan al repository.
- `from` posterior a `to` → `ApiError`.
- Fecha con formato inválido → `ApiError`.
- `limit` se recorta al máximo permitido (100).
- `page` no numérico o no positivo → `ApiError`.
- **`page` solicitado se respeta** (`page: '3'` → el repository se llama con `page: 3`, no se recorta a 1 — regresión del bug de paginación).
- Resolución de `actorName`/`actorProfile` por rol (`user`/`specialist`/`center_admin`).
- Fallback de `entityLabel` desde `before`/`after` cuando el registro fue eliminado.
- `routineStepDetails` (array) con `hasProducts` true/false y `null` cuando el metadata no es de una rutina consolidada; retrocompatibilidad con filas legacy `routine_step_batch`/`routine_step`.
- `routineChange` con `before`/`after` de la rutina cuando el batch incluye datos de la rutina en sí, `null` cuando el batch es solo de pasos.
- Filtro `entity=user_profile` resuelve `entityIdIn` con ids de `role='user'` (y devuelve página vacía sin consultar `audit_logs` si no hay ninguno).
- Filtro `actorName` resuelve `actorIdIn` por nombre (con y sin coincidencias) y se ignora si queda vacío tras `trim()`.
- Suscripciones: `owner_id` se reemplaza por `owner` (nombre), tanto para `owner_type='user'` como `'center'`.
- Controller mapea query params `string | string[] | undefined` a `string | undefined` antes de llamar al service.

Tests de la consolidación de auditoría de rutinas (`backend/src/modules/routines/tests/routines.service.test.ts`, mockeando `auditRepository.findRecentRoutineBatch`/`updateRoutineBatch`):

- Dos altas de pasos de la misma rutina dentro de la ventana → un solo `recordAuditLog`, el segundo paso se agrega vía `updateRoutineBatch`.
- Crear rutina + actualizar horario + agregar N pasos (probado con 5, sin límite) → **un solo registro** `action: 'create'` con `metadata.routine.after` reflejando el estado final y `metadata.steps` con los N pasos en orden.
- `createRoutine`/`updateRoutine`/`deleteRoutine` auditan con el `before`/`after` (o `routineChange`) correcto.

Tests de los demás emisores agregados (cada uno mockea `recordAuditLog` con el mismo patrón):

- `backend/src/modules/admin/tests/admin.service.test.ts` — aprobar/rechazar especialista emite con `before` resuelto y `action` correcta; no emite si no hay `adminUserId`.
- `backend/src/modules/specialists/tests/specialists.registration.service.test.ts` — alta de especialista emite con `entityId = profile.id`.
- `backend/src/modules/specialists/tests/specialists.directory.service.test.ts` — `linkSpecialist`/`unlinkSpecialist`/`assignRoutineToPatient` emiten correctamente (o no emiten cuando no corresponde, ej. reutilizar relación ya activa).
- `backend/src/modules/profile/tests/profile.service.test.ts` — edición de perfil emite con `before`/`after`; no emite en los casos de error (403/404/400).
- `backend/src/modules/auth/tests/auth.service.test.ts` — registro emite `action: 'create'` con el `actorRole` correcto; no emite si falla la creación del usuario.
- `backend/src/modules/quiz/tests/quiz.controller.test.ts` (nuevo, primer test de este módulo) — reintento del test de piel emite con `metadata.changeType: 'skin_quiz_retake'` cuando había un perfil previo.
- `backend/src/modules/centers/tests/centers.service.test.ts` — create/update/delete de centro emiten con `before`/`after` correctos.
- `backend/src/modules/products/tests/products.service.test.ts` — `remove`/`forceRemove`/`replaceInRoutines` emiten `action: 'delete'` con `before` y `metadata.changeType` distintivo.

## Pendiente (no resuelto por esta skill todavía)

Ver la tabla de verificación completa contra el checklist §7 de `docs/plan_entrega3.md` en `docs/e3-contracts.md` (sección "Verificación de seguridad", dentro de "M4 - Auditoria y Seguridad Transversal"). Resumen:

1. **RLS de `audit_logs`**: falta una migración nueva que habilite RLS (deny-all por defecto). No se creó en esta iteración porque toca una migración de base de datos — comunicar antes de escribirla. Detalle en `docs/e3-supabase-security.md`.
2. **T4.6 incompleto**: creación/edición de `user_profile`/`specialist_profile` ya emiten (ver Scope arriba); falta login exitoso/fallido y cambio explícito de rol.
3. **T4.7**: solo se verificó puntualmente RBAC de las rutas tocadas en esta sesión, no una auditoría formal de M1/M2/M3/M5 completa.
4. **T4.8**: confirmado que falta `helmet` (o equivalente) en `backend/src/app.ts` — no se agregó, queda como hallazgo.
5. **T4.9**: exposición de errores revisada de forma genérica vía `error.middleware.ts` (comportamiento compartido por toda la API, no específico de auditoría) — sin hallazgos.
6. **Suscripciones de centro y baja de cuenta de usuario/especialista**: no existe el flujo de negocio, fuera de alcance hasta que se construya (confirmado con la usuaria).

## Verification

```bash
cd backend && npm run typecheck && npx jest --testPathPatterns=audit
npm run lint
```

Manual: generar un evento (crear/editar un centro o rutina, que ya llaman a `recordAuditLog`) y confirmar que aparece en `GET /api/admin/audit-log` y en la pantalla `app/(tabs-admin)/audit-log.tsx` con los filtros correctos.
