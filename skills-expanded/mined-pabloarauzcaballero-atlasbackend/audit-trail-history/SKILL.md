---
name: audit-trail-history
description: Diseño de rastro de auditoría e historial de registros — quién, qué, cuándo, desde dónde y por qué; almacenamiento append-only e inalterable; qué eventos auditar (incluidas las LECTURAS de datos sensibles); historial de versiones de un registro; triggers vs aplicación; qué no guardar en el log; retención y consulta eficiente. Usar al diseñar una tabla de auditoría, al agregar un endpoint que lee o muta datos clínicos, financieros o de permisos, al implementar "ver historial de cambios", o al revisar si una acción sensible deja rastro.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Rastro de auditoría e historial

Dos necesidades distintas que se suelen mezclar:

- **Auditoría**: registro de *acciones* para rendir cuentas (quién accedió a qué). Lo lee
  seguridad, compliance, un perito.
- **Historial**: versiones anteriores de un *registro* para el negocio (cómo estaba esta ficha
  el martes). Lo lee el usuario.

Se diseñan por separado. Los logs técnicos de operación son otra cosa más: `backend-observability`.

## 1. Las cinco preguntas

Cada evento de auditoría responde, sin joins frágiles:

| Pregunta | Campos |
|---|---|
| **Quién** | `actor_id`, `actor_type` (usuario, sistema, job, integración), rol efectivo, `tenant_id`; si actúa en nombre de otro, `on_behalf_of_id` |
| **Qué** | `action` (verbo de vocabulario cerrado), `resource_type`, `resource_id`, resultado (`success` / `denied` / `error`) |
| **Cuándo** | `occurred_at timestamptz` puesto por el servidor o la base, nunca por el cliente |
| **Desde dónde** | IP, user agent o cliente, `request_id` / trace id para cruzar con logs |
| **Por qué** | motivo declarado cuando el dominio lo exige: acceso de emergencia, corrección, base de consentimiento |

- El actor se **desnormaliza** (ID + etiqueta del momento): si el usuario se renombra o se da
  de baja, el evento tiene que seguir siendo legible.
- `action` es vocabulario cerrado y documentado (`record.read`, `record.export`,
  `permission.grant`), no texto libre.
- Los **intentos denegados** se auditan: son la señal más valiosa de abuso.

## 2. Qué auditar

1. **Lecturas de datos sensibles**, no solo escrituras: abrir un expediente, ver un
   documento, buscar a una persona, exportar o imprimir. En salud, "quién vio" importa tanto
   como "quién cambió".
2. Toda mutación de datos clínicos, financieros, de identidad y de consentimiento.
3. Autenticación y sesión: login, fallo, cierre, cambio de credenciales, MFA (`authn-identity`).
4. Cambios de autorización: roles, permisos, membresías, accesos delegados (`authz-access-control`).
5. Acciones administrativas y de soporte, incluida la suplantación ("ver como").
6. Accesos excepcionales (*break-glass*) con motivo obligatorio (`data-privacy-sensitive`).
7. Operaciones masivas y exportes: quién, cuántas filas, con qué filtro.
8. Cambios de configuración que alteran el comportamiento de seguridad.

No audites ruido (cada health check, cada listado de catálogo público): encarece y tapa la señal.

## 3. Append-only e inalterable

- La tabla de auditoría acepta **solo `INSERT`**. Se garantiza en la base, no por convención:

```sql
CREATE FUNCTION audit.forbid_mutation() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
  RAISE EXCEPTION 'audit log es append-only' USING ERRCODE = 'restrict_violation';
END $$;

CREATE TRIGGER events_no_mutation
  BEFORE UPDATE OR DELETE ON audit.events
  FOR EACH ROW EXECUTE FUNCTION audit.forbid_mutation();

REVOKE UPDATE, DELETE, TRUNCATE ON audit.events FROM app_role;
```

- El rol de la aplicación tiene `INSERT` y, a lo sumo, `SELECT` acotado. `TRUNCATE` no dispara
  triggers de fila: por eso el `REVOKE` además del trigger.
- Un evento equivocado no se corrige: se agrega otro que lo rectifica y lo referencia.
- Para evidencia de manipulación ante quien tiene acceso de superusuario: encadenar cada fila
  con el hash de la anterior y/o replicar a un almacenamiento externo de escritura única. El
  nivel exigido lo define el responsable de compliance: `regulatory-compliance-mapping`.
- En el modelo, la tabla lleva su estereotipo de solo-inserción (`data-modeling-plantuml`) y el
  ORM no expone `update`/`delete` para esa entidad.

## 4. Qué NO guardar

- **No copies PII completa al log de auditoría**: convierte al log en el blanco más jugoso
  del sistema y multiplica el alcance de cualquier filtración. Guardá `resource_type` +
  `resource_id` + nombres de los campos tocados; el contenido vive en la tabla de origen o en el
  historial, bajo sus propios controles de acceso.
- Nunca secretos, tokens, contraseñas ni cuerpos de request crudos.
- Si el negocio necesita el valor anterior y el nuevo, eso es **historial** (§5), no auditoría.
- Ver `data-privacy-sensitive` para clasificación y enmascarado.

## 5. Historial de versiones de un registro

| Estrategia | Cómo | Cuándo |
|---|---|---|
| **Tabla de historia** | Cada cambio copia la fila vieja a `<tabla>_history` con `valid_from`/`valid_to` y quién | Necesitás reconstruir el registro en una fecha; caso general |
| **Inmutable + nueva versión** | El registro no se edita; una enmienda es una fila nueva que referencia a la anterior | Documentos firmados, asientos contables, decisiones de riesgo (`accounting-double-entry`) |
| **Eventos como fuente** | El estado se deriva de la secuencia de eventos | Flujos donde la secuencia *es* el dominio (`state-machines-workflows`) |

- La versión vigente se obtiene sin escanear la historia (`valid_to IS NULL` con índice parcial,
  o tabla actual separada).
- La columna de versión del locking optimista (`concurrency-and-locking`) **no** es un
  historial: dice que cambió, no qué había antes.
- El historial con datos sensibles hereda los mismos permisos que el registro actual. Ocultar un
  campo en la ficha y mostrarlo en "ver cambios" es una fuga.

## 6. Triggers vs aplicación

| | Trigger de base | Capa de aplicación |
|---|---|---|
| Captura | Toda escritura, incluidos scripts y accesos directos | Solo lo que pasa por el código instrumentado |
| Conoce al actor | No, salvo que la app lo propague a la sesión | Sí: usuario, rol, tenant, motivo, request |
| Audita lecturas | No (no hay trigger de `SELECT`) | Sí |
| Riesgo | Actor "desconocido"; costo por fila | Olvidarse de instrumentar un camino |

Regla de la casa: **historial de datos por trigger** (no se puede saltear) y **auditoría de
acciones en la aplicación** (conoce intención y lecturas), en un punto único — interceptor o
servicio de dominio — no dispersa por los controllers. Para que el trigger conozca al actor, la
aplicación fija una variable de sesión **local a la transacción** (`set_config(..., true)`) y el
trigger la lee con `current_setting`. Con pool de conexiones, un valor no local se filtra entre
requests.

- El evento de auditoría de una mutación se escribe **en la misma transacción** que la mutación:
  si una se revierte, la otra también.
- El evento de una **lectura** o de un acceso **denegado** se escribe aunque la operación
  principal no tenga transacción o falle; no puede depender de su commit.

## 7. Retención y consulta

- Plazo de retención definido por tipo de evento y documentado; lo fija el responsable
  legal/compliance, no el desarrollador. Pasado el plazo se **archiva o purga por un proceso
  privilegiado y auditado**, no con el rol de la aplicación.
- Particioná por tiempo (`PARTITION BY RANGE (occurred_at)`): retención = desprender una
  partición, no un `DELETE` masivo.
- Índices para las tres preguntas reales: por recurso (`resource_type, resource_id, occurred_at`),
  por actor (`actor_id, occurred_at`), por tenant y tiempo. Considerá BRIN sobre `occurred_at` en
  tablas muy grandes insertadas en orden temporal; medí con `EXPLAIN ANALYZE`.
- Consultar el log de auditoría **también se audita**, y requiere un permiso propio.
- Paginación por cursor sobre `(occurred_at, event_id)`; nunca `OFFSET` en una tabla que solo crece.

## Anti-patrones

- "Auditoría" como columnas `updated_by`/`updated_at` en la fila: solo recuerda al último.
- Log de auditoría mutable "para corregir errores".
- Volcar el JSON completo del paciente en cada evento.
- Auditar solo escrituras en un sistema donde el riesgo principal es la curiosidad indebida.
- Timestamp o actor tomados del payload del cliente.
- Auditoría escrita en un `catch` que se traga su propio fallo: si no se pudo auditar una acción
  sensible, la acción falla.

## Checklist

- [ ] Cada evento responde quién, qué, cuándo, desde dónde y, si aplica, por qué.
- [ ] Lecturas, exportes y accesos denegados de datos sensibles quedan registrados.
- [ ] Tabla append-only garantizada por trigger **y** por privilegios; ORM sin update/delete.
- [ ] Sin PII completa, secretos ni cuerpos crudos en el log.
- [ ] Historial con estrategia elegida a propósito y mismos permisos que el dato vigente.
- [ ] Actor propagado a la base con alcance de transacción.
- [ ] Mutación y su evento en la misma transacción.
- [ ] Retención documentada, particionado por tiempo, índices por recurso y por actor.
- [ ] Test que intenta `UPDATE`/`DELETE` sobre el log y espera el rechazo (`integrity-testing`).
