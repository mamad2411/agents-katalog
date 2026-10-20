---
name: state-machines-workflows
description: Estados como máquina explícita para solicitudes, citas, cotizaciones, reclamos y toda entidad con ciclo de vida — tabla de transiciones, guardas por rol y por dato, transición atómica con precondición en el `UPDATE`, historial, efectos después del commit, estados terminales y tests por transición válida e inválida. Usar al agregar un estado o acción a una entidad, al exponer un endpoint que cambia estado, al revisar un `PATCH` que acepta `status`, o ante un registro en estado imposible.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Máquinas de estado y flujos

Si una entidad tiene una columna `status`, **ya tenés** una máquina de estados; la única
pregunta es si está escrita en un lugar o desparramada en `if` por todo el código. Esta
skill la hace explícita. Carreras en `concurrency-and-locking`; status HTTP en
`error-handling-contract`; efectos asíncronos en `async-messaging-events`.

## 1. Cuándo aplica

- La entidad pasa por etapas con reglas sobre qué sigue a qué (solicitud de consulta,
  cita, cotización, reclamo/preautorización de seguro, publicación moderada, asiento
  contable borrador→contabilizado).
- No aplica a un booleano independiente (`isFeatured`). Sí aplica si hay **varios
  booleanos que se excluyen** (`isApproved`, `isRejected`, `isCancelled`): eso es un
  estado mal modelado — colapsalo en uno.

## 2. La máquina es una tabla, en un solo lugar

Primero se escribe la tabla (y se valida con negocio); después el código.

| Desde | Acción | Hacia | Quién | Guarda de datos | Efecto |
|---|---|---|---|---|---|
| `requested` | `accept` | `accepted` | profesional asignado | horario libre | notificar paciente |
| `requested` | `reject` | `rejected` ⛔ | profesional asignado | motivo obligatorio | notificar paciente |
| `requested` | `cancel` | `cancelled` ⛔ | paciente dueño | — | liberar hueco |
| `accepted` | `cancel` | `cancelled` ⛔ | paciente o profesional | dentro de la ventana permitida | liberar hueco, notificar |
| `accepted` | `complete` | `completed` ⛔ | profesional | fecha ya ocurrida | habilitar nota clínica |

⛔ = terminal. **Lo que no está en la tabla está prohibido** (deny by default).

```typescript
const TRANSITIONS = {
  requested: { accept: 'accepted', reject: 'rejected', cancel: 'cancelled' },
  accepted:  { cancel: 'cancelled', complete: 'completed' },
  rejected:  {}, cancelled: {}, completed: {},          // terminales: sin salidas
} as const satisfies Record<Status, Partial<Record<Action, Status>>>;

export function next(from: Status, action: Action): Status {
  const to = (TRANSITIONS[from] as Partial<Record<Action, Status>>)[action];
  if (!to) throw new InvalidTransitionError(from, action);   // → 409
  return to;
}
```

- `satisfies` hace que agregar un estado sin declarar sus salidas **no compile**
  (ver `typescript-standards`).
- Si los estados son un catálogo de la base (value set), la tabla de transiciones
  referencia los **códigos de concepto**, no labels (ver `terminology-value-sets`).
- Una librería de statecharts solo se justifica con estados jerárquicos/paralelos
  reales. Para un ciclo de vida lineal, la tabla alcanza.

## 3. La API expone acciones, no estados

```typescript
// ❌ el cliente elige el estado destino: puede saltarse etapas y guardas
PATCH /appointments/:id   { "status": "completed" }

// ✅ el cliente pide una acción; el servidor decide el destino
POST /appointments/:id/accept
POST /appointments/:id/cancel   { "reason": "..." }
```

- `status` **nunca** es escribible en un DTO de creación ni de actualización (mass
  assignment — ver `authz-access-control`). El estado inicial lo fija el servidor.
- La respuesta incluye el estado nuevo y, si ayuda a la UI, las **acciones disponibles
  para este actor** (`availableActions`): el front no replica las reglas, solo las pinta.
  Ocultar un botón no es autorización.

## 4. Guardas: tres capas, en orden

1. **Estructura**: ¿la acción existe desde este estado? (tabla) → si no, **409**
   `INVALID_TRANSITION`.
2. **Actor**: ¿este rol, con esta relación con el recurso (dueño, profesional asignado,
   mismo tenant), puede ejecutarla? → si no, **403/404** (ver `authz-access-control`).
3. **Datos**: ¿se cumplen las precondiciones de negocio (motivo presente, dentro de
   ventana, montos cuadran)? → si no, **422**.

Las guardas viven en el dominio (entidad o servicio de dominio), no en el controller ni
en el front. Un método por acción (`appointment.accept(actor, clock)`), no un
`setStatus()` público.

## 5. Transición atómica

Leer el estado, validarlo en memoria y guardar es una carrera: dos operadores
aprueban y rechazan a la vez y ambos "pasan". La precondición viaja **en la escritura**:

```sql
UPDATE consultation_request
   SET status = 'accepted', decided_by = $2, decided_at = now(), version = version + 1
 WHERE id = $1 AND status = 'requested';     -- 0 filas afectadas = perdiste → 409
```

- Con ORM: versión de fila (locking optimista) **o** `FOR UPDATE` de la fila dentro de la
  transacción; nunca ninguno de los dos.
- Transición + fila de historial + mensaje de outbox = **una sola transacción**.
- La acción es **idempotente** ante reintentos: repetir `accept` sobre algo ya `accepted`
  por el mismo actor devuelve el estado actual (200), no un error ni un segundo efecto.
  Repetirla desde un estado incompatible sí es 409.

## 6. Historial de transiciones

Tabla append-only `<entidad>_transition`: `entity_id`, `from_status`, `to_status`,
`action`, `actor_id`, `actor_role`, `reason`, `occurred_at`, `metadata`.

- El `status` de la entidad es una **proyección** del último evento; el historial es la
  verdad de cómo se llegó. Sirve a auditoría, soporte y métricas de tiempos por etapa
  (ver `audit-trail-history`).
- Nunca se edita ni se borra. `reason` obligatorio en rechazos, cancelaciones y reversas.
- Sin datos sensibles en `reason`/`metadata` salvo que el acceso al historial esté tan restringido
  como el dato clínico (ver `data-privacy-sensitive`).

## 7. Efectos secundarios: después del commit

- Notificar, liberar un hueco en otro agregado, emitir un asiento, llamar a un tercero:
  **nunca dentro** de la transacción de la transición. Si el efecto falla, la transición
  ya ocurrió y es correcta; si la transición hace rollback, el email ya salió.
- Patrón: la transición escribe un mensaje en **outbox** en la misma transacción; un
  relay lo publica; el handler es idempotente (ver `async-messaging-events`,
  `notifications-delivery`).
- Un efecto fallido se reintenta y se alerta; **no** revierte el estado.

## 8. Terminales, reversas y tiempo

- Un estado terminal no tiene salidas. "Reabrir" no es editar el estado: es una acción
  nueva y explícita en la tabla (`reopen`), con su guarda y su rastro, o una **entidad
  nueva** que referencia a la anterior (nueva cotización que reemplaza a la vencida).
- En lo contable y lo clínico no hay "deshacer": hay **reversa/enmienda** como registro
  nuevo (ver `accounting-double-entry`, `audit-trail-history`).
- Transiciones por tiempo (`expire`, `no_show`): las ejecuta un job con el **mismo**
  camino de código que las manuales — misma tabla, mismo `UPDATE` condicional, actor
  `system` en el historial (ver `background-jobs-scheduling`). No calcules "vencido" al
  vuelo en unas queries y guardado en otras.
- Inyectá el reloj: las guardas de ventana temporal deben ser testeables.

## 9. Tests: la matriz completa

- Generá los casos **desde la tabla**: para cada par (estado, acción) → si está permitido,
  afirmá destino, fila de historial y mensaje de outbox; si no, afirmá
  `InvalidTransitionError` y que **nada cambió**.
- Por cada transición permitida: un test por guarda de actor negada y uno por guarda de
  datos negada (ver `unit-testing` para parametrizados).
- Un test de API por acción: status + `code` del error (ver `api-testing`).
- Un test de concurrencia por transición disputable: N intentos en paralelo → 1 gana,
  el resto 409, un solo registro de historial (ver `integrity-testing`).
- Invariante en datos: query que cuente entidades cuyo `status` no coincide con su
  última transición; debe dar 0 (ver `data-quality-validation`).

## Anti-patrones

- `status` aceptado en el body; `setStatus()` público; reglas duplicadas en el front.
- `if (status === 'x' || status === 'y')` repetido en servicios distintos.
- Varios booleanos excluyentes en lugar de un estado.
- Leer-validar-guardar sin precondición en el `UPDATE` ni versión.
- Enviar la notificación dentro de la transacción.
- "Reabrir" con un `UPDATE` manual a la base.
- Testear solo el camino feliz de la máquina.

## Checklist

- [ ] Tabla de transiciones escrita, validada con negocio y codificada en un único módulo.
- [ ] La API expone acciones; `status` no es escribible en ningún DTO.
- [ ] Guardas en tres capas (estructura → actor → datos) con 409 / 403-404 / 422.
- [ ] Transición con precondición en la escritura (o versión/lock) y dentro de una transacción.
- [ ] Historial append-only con actor, acción, motivo y fecha, en la misma transacción.
- [ ] Efectos vía outbox, después del commit, con handlers idempotentes.
- [ ] Estados terminales sin salidas; reaperturas y reversas como acciones/entidades explícitas.
- [ ] Transiciones por tiempo por el mismo camino de código, con actor `system` y reloj inyectado.
- [ ] Matriz completa de tests generada desde la tabla, incluidas las transiciones inválidas.
