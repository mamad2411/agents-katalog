---
name: authz-access-control
description: Gate de autorización para la API — deny by default, RBAC + ownership + relación (quién atiende a quién), chequeo a nivel de objeto en cada endpoint (BOLA/IDOR), de función (BFLA) y de campo (mass assignment y respuesta mínima), roles cerrados en un único mapa, guards y policies en NestJS, y matriz rol × recurso × acción como artefacto. Usar al crear o revisar cualquier endpoint, query de listado, export, job o acción por link que lea o mute datos de alguien, y antes de cerrar un cambio que toque roles o permisos.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Autorización y control de acceso — gate

`authn-identity` establece **quién** es el actor. Esta skill decide **qué puede hacer sobre qué
objeto**. `security-guardrails` enuncia el principio; acá está el método para que se cumpla
endpoint por endpoint. El aislamiento entre organizaciones es de `multi-tenancy`.

Marco: OWASP API Security Top 10 2023 — **API1** Broken Object Level Authorization (BOLA/IDOR),
**API3** Broken Object Property Level Authorization, **API5** Broken Function Level
Authorization (BFLA). Son tres chequeos distintos y los tres son obligatorios.

## 1. Las cuatro preguntas de toda operación

| # | Pregunta | Falla si se omite |
|---|---|---|
| 1 | ¿El actor está autenticado? | acceso anónimo |
| 2 | ¿Su rol puede ejecutar **esta función**? | BFLA — un paciente invoca un endpoint de admin |
| 3 | ¿Puede operar sobre **este objeto**? | BOLA/IDOR — cambia el `:id` y ve lo ajeno |
| 4 | ¿Puede leer/escribir **estos campos**? | mass assignment / fuga de propiedades |

Un guard de rol responde solo la 2. **La 3 casi nunca se resuelve con un decorador**: necesita
cargar el objeto (o filtrar la query) con el actor como parte de la condición.

## 2. Deny by default

- Guard global de autenticación y de roles por `APP_GUARD`; lo público se declara (`@Public()`).
- **Trampa del ejemplo oficial de NestJS**: su `RolesGuard` devuelve `true` cuando la ruta no
  declara roles. Eso es *allow by default*. En la casa, una ruta sin metadatos de autorización
  **se rechaza**; quien la quiera abierta a cualquier autenticado lo declara.

```ts
// ❌ sin @Roles() la ruta queda abierta a cualquier autenticado
if (!requiredRoles) return true;

// ✅ sin política declarada, se niega
const policy = this.reflector.getAllAndOverride(POLICY_KEY, [ctx.getHandler(), ctx.getClass()]);
if (!policy) throw new ForbiddenException();
```

- `Reflector.createDecorator<T>()` o `SetMetadata` para declarar; `getAllAndOverride` con
  `[getHandler(), getClass()]` para que el handler pise al controller.
- Los guards corren **antes** de pipes e interceptors: en el guard todavía no hay DTO validado
  ni entidad cargada. Por eso el chequeo de objeto vive en el caso de uso, no en el guard.

## 3. Modelo: rol + ownership + relación

- **Rol** (RBAC): qué funciones existen para ese tipo de actor. Conjunto **cerrado**, definido
  en **un único mapa** del código (rol → permisos). Prohibido comparar strings de rol sueltos
  por la base de código o derivar permisos del nombre del rol.
- **Ownership**: el recurso es del actor (su perfil, sus citas, sus publicaciones).
- **Relación** (ReBAC): el actor tiene un vínculo vigente con el dueño — el profesional que
  **atiende** a ese paciente, el miembro de esa organización, el titular del seguro. La
  relación tiene vigencia y alcance: se verifica contra datos, no contra el rol.
- **Atributos/contexto**: estado del recurso, consentimiento vigente, horario, tenant.
- En salud la regla típica combina todo: *rol profesional* **y** *relación de atención vigente*
  **y** *base legal que cubre ese dato* (ver `data-privacy-sensitive`). El rol solo no alcanza:
  ser médico no da acceso a todos los pacientes.

## 4. Chequeo a nivel de objeto (BOLA/IDOR)

1. Todo endpoint con un identificador en ruta, query o body lo verifica. También los anidados:
   `/patients/:pid/records/:rid` exige que `rid` **pertenezca** a `pid`, además del acceso a `pid`.
2. **Preferí filtrar a verificar**: meté el actor en la condición de la query. Así no existe
   una ventana donde el objeto ajeno ya está cargado.
3. Los **listados y búsquedas** también son acceso a objetos: el filtro por actor/relación va en
   la query, no en un `.filter()` posterior (rompe la paginación y filtra de más al log).
4. Recurso ajeno ⇒ **404**, no 403, cuando la sola existencia es información (¿este paciente
   tiene historia en esta clínica?). 403 cuando el actor ya sabe legítimamente que existe.
5. IDs no adivinables (UUID) **no son autorización**: reducen enumeración, no reemplazan el chequeo.
6. El identificador del actor sale del token/sesión; **nunca** de un campo del body o un header
   que el cliente controla (`userId`, `doctorId`, `X-User`).

```ts
// ❌ autenticado ≠ autorizado sobre ESTA cita
const appt = await em.findOneOrFail(Appointment, id);

// ✅ el actor es parte de la condición; si no es suya, no existe
const appt = await em.findOne(Appointment, {
  id,
  $or: [{ patient: actor.personId }, { professional: actor.personId }],
});
if (!appt) throw new NotFoundException();
```

## 5. Chequeo a nivel de función (BFLA)

- Rutas administrativas o de otro rol no se protegen por estar "escondidas" ni por prefijo de URL.
- Cuidado con verbos: que `GET /x/:id` esté permitido no implica `PATCH` ni `DELETE`.
- Acciones de transición de estado (aprobar, anular, cerrar) son funciones con su propio permiso,
  no un `PATCH { status }` genérico que cualquiera con escritura puede mandar
  (`state-machines-workflows`).

## 6. Chequeo a nivel de campo (API3)

- **Entrada**: DTO con allowlist + `ValidationPipe({ whitelist: true, forbidNonWhitelisted: true })`
  (`nestjs-development`). Campos sensibles (`role`, `status`, `ownerId`, `tenantId`, `verifiedAt`,
  montos) **nunca** en un DTO de edición general; cambian por su caso de uso dedicado.
- **Salida**: DTO de respuesta **por vista y por rol**, nunca la entidad del ORM serializada.
  Devolvé lo mínimo que esa pantalla necesita (`data-privacy-sensitive`). Un mismo recurso puede tener
  tres proyecciones: pública, del titular, del profesional tratante.
- Filtros, ordenamientos e `include/expand` controlados por el cliente también filtran datos:
  allowlist de campos filtrables y de relaciones expandibles.

## 7. La UI nunca es barrera

Ocultar un botón, deshabilitar un campo o no enlazar una ruta es UX. Toda regla de permiso
existe en el backend y se prueba contra el backend, con un cliente HTTP, salteando la UI.

## 8. Superficies que se olvidan

- **Jobs y consumidores de eventos**: corren sin request ⇒ sin actor implícito. Llevan el actor
  o la autorización ya resuelta en el payload, y no amplían privilegios (`background-jobs-scheduling`).
- **Exportes, reportes y descargas de archivos**: misma regla que el listado que los origina;
  URLs firmadas de corta vida, no rutas estáticas adivinables (`file-uploads-media`).
- **Links de email/chat**: el token identifica la acción; la acción sensible exige sesión del
  actor correcto (`authn-identity`).
- **Caché**: una respuesta autorizada para un actor nunca se sirve a otro (`caching-strategy`).
- **Websockets / suscripciones**: autorizar la suscripción **y** cada mensaje emitido.
- **Búsqueda**: el índice no debe revelar lo que el listado oculta (`search-and-filtering`).
- **Acceso de emergencia / soporte**: si existe, es explícito, acotado en el tiempo, con motivo
  obligatorio y auditado (`audit-trail-history`). Nunca un flag silencioso.

## 9. La matriz como artefacto

Por módulo, mantené versionada una tabla **rol × recurso × acción** con la condición:

| Recurso · acción | Anónimo | Paciente | Profesional | Admin org. |
|---|---|---|---|---|
| Cita · leer | ✗ | propia | donde es tratante | de su organización |
| Cita · cancelar | ✗ | propia, si estado lo permite | propia agenda | ✗ |

- Cada celda no vacía es un test positivo; **cada ✗ y cada condición es un test negativo**.
- La matriz se revisa en el PR junto con el código. Endpoint sin fila en la matriz = no mergea.

## 10. Tests negativos obligatorios

Por endpoint que toca datos de alguien, como mínimo:
1. Sin credencial → 401.
2. Rol sin permiso de función → 403.
3. **Mismo rol, otro dueño** (usuario B pide el recurso de A) → 404/403. Es el test de IDOR.
4. Relación inexistente o vencida (profesional que no atiende a ese paciente) → 404/403.
5. Body con campos prohibidos (`role`, `ownerId`, `tenantId`) → 400, y verificar que **no** persistió.
6. Listado: el usuario B no ve ningún registro de A, ni en `total`/contadores.
7. Hijo de otro padre: `/a/:idA/b/:idDeOtroPadre` → 404.

Van en la suite de API con base real (`api-testing`, `integrity-testing`); un guard mockeado no prueba nada.

## Anti-patrones

- `@UseGuards(AuthGuard)` y nada más. "El front no muestra ese botón".
- `findOne(id)` seguido de un `if` que alguien olvidará en el próximo endpoint.
- `if (user.role === 'admin')` disperso; roles nuevos creados ad hoc desde un carril.
- Devolver la entidad completa y "que el front muestre lo que necesite".
- Aceptar `userId`/`tenantId` del body. 403 que confirma la existencia de un registro clínico.

## Evidencia / Definition of Done

Para afirmar que un endpoint está autorizado, pegá **salida literal**:
- Fila(s) de la matriz rol × recurso × acción que cubren el cambio.
- Ejecución de los tests negativos 1–7 aplicables, con el código HTTP observado en cada uno.
- El request real del caso IDOR (usuario B → recurso de A) y su respuesta, no una descripción.
- Para mass assignment: request con el campo prohibido + consulta que muestre que no cambió.
- Resultado de `grep` de comparaciones de rol fuera del mapa único (debe dar vacío o justificado).
- Riesgo residual declarado. Sin esto, el estado es "escrito", no "verificado"
  (`evidence-and-verification`).

## Checklist

- [ ] Guards globales; ruta sin política declarada ⇒ denegada.
- [ ] Roles cerrados en un único mapa; sin strings de rol sueltos.
- [ ] Chequeo de objeto en **cada** identificador, incluidos recursos anidados.
- [ ] Listados y búsquedas filtran por actor/relación dentro de la query.
- [ ] Relación y consentimiento verificados contra datos, con vigencia.
- [ ] Actor tomado de la sesión, nunca del body/headers del cliente.
- [ ] DTO de entrada con allowlist; campos sensibles solo por caso de uso dedicado.
- [ ] DTO de salida por vista/rol; nunca la entidad cruda.
- [ ] 404 vs 403 decidido a conciencia.
- [ ] Jobs, exportes, links, caché, websockets y búsqueda revisados.
- [ ] Matriz actualizada en el PR; tests negativos 1–7 en verde con salida pegada.
