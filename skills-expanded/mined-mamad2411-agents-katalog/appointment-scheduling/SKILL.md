---
name: appointment-scheduling
description: Gate de diseño para agenda y citas — horarios de atención, bloqueos, disponibilidad calculada, prevención de doble reserva con exclusion constraint por rango más locking, zonas horarias, duración y buffers, estados de la cita, recordatorios y reglas de reprogramación y cancelación. Usar al modelar o tocar horarios, disponibilidad, reserva de turnos, bloqueos de agenda, la vista de "hoy" o cualquier endpoint que cree, mueva o cancele una cita. La mecánica genérica de carreras y locking es `concurrency-and-locking`.
allowed-tools: Read Grep Glob Bash
effort: high
---

# Agenda y citas — reglas de diseño

La corrección de una agenda se juega en dos frentes: **no reservar dos veces el mismo hueco** y
**no equivocarse con la hora** (zonas horarias). Todo lo demás es consecuencia.

## 1. Zonas horarias: guardá en UTC, mostrá en local

- Persistí instantes en **UTC** (`timestamptz`). La zona del profesional/paciente es un dato
  aparte para presentar y para interpretar reglas ("atiende de 9 a 17 hora local").
- Los horarios de atención son **reglas en hora local** (ej. "lunes 09:00–13:00 America/…").
  La disponibilidad concreta de un día se **calcula** aplicando la regla a la fecha y resolviendo
  la zona (incluido horario de verano). No guardes slots materializados como única verdad.
- Nunca hagas aritmética de fechas con offsets fijos ("resto 4 horas"): usá una librería de zonas
  y la fecha real (verificá la API de la librería que uses; ver `typescript-standards`).

## 2. Disponibilidad = reglas − ocupado − bloqueos

La disponibilidad de un profesional en un rango se deriva de:
1. **horarios de atención** (plantilla semanal + excepciones por fecha);
2. menos **citas existentes** (con su duración y buffers);
3. menos **bloqueos** (vacaciones, ausencias, mantenimiento).

Calculala en el servidor. El front pinta huecos; no decide disponibilidad.

## 3. Doble reserva: la carrera central

Dos clientes piden el último hueco a la vez. Chequear "¿está libre?" y luego insertar **no
alcanza**: entre el check y el insert entra el otro (ver `concurrency-and-locking`).

- Defensa en la **base**, no solo en la app. En PostgreSQL, la herramienta correcta es un
  **exclusion constraint** sobre un rango temporal (`tstzrange`) con `EXCLUDE USING gist`,
  particionado por recurso (profesional/sala), de modo que dos citas solapadas del mismo recurso
  sean imposibles (ver `postgresql-advanced`). Requiere la extensión `btree_gist` para combinar
  el id del recurso con el rango.

```sql
-- una cita nunca puede solaparse con otra del mismo profesional
ALTER TABLE appointment ADD CONSTRAINT no_overlap
  EXCLUDE USING gist (professional_id WITH =, during WITH &&)
  WHERE (status <> 'cancelled');
```

- El `WHERE` excluye las canceladas para que un hueco liberado vuelva a estar disponible.
- La app traduce la violación del constraint a un 409 claro (ver `error-handling-contract`),
  no a un 500.

## 4. Duración y buffers

- Una cita ocupa `[inicio, inicio+duración)`; los **buffers** (limpieza, preparación) se suman al
  rango que bloquea la agenda, aunque no sean tiempo "de atención".
- Modelá el rango efectivo que participa del exclusion constraint incluyendo el buffer, o
  registralo aparte con criterio consistente.

## 5. Estados de la cita

Máquina explícita (ver `state-machines-workflows`):

`requested` → `confirmed` → (`completed` | `cancelled` | `no_show`) ; y `rescheduled`.

- Cada transición valida rol y reglas (quién puede cancelar, con cuánta anticipación).
- Reprogramar = liberar el rango viejo y reservar el nuevo **atómicamente**; el rango viejo vuelve
  a estar disponible solo cuando la nueva reserva tiene éxito.
- Guardá el historial de cambios de la cita (ver `audit-trail-history`).

## 6. Reglas de reprogramación y cancelación

- Ventanas ("cancelar hasta 24 h antes"), cupos, penalidades: son reglas de negocio en el
  servidor, no botones ocultos en la UI (la UI nunca es la barrera).
- Solapamientos permitidos por overbooking (si el negocio lo pide) son una **excepción explícita
  y declarada**, no un descuido del constraint.

## 7. Recordatorios

- Los recordatorios se disparan por job programado, idempotente y con la zona horaria correcta
  (ver `background-jobs-scheduling`); un recordatorio no se envía dos veces.
- Cancelar/reprogramar una cita cancela o reprograma su recordatorio.

## Anti-patrones

- Guardar horas "locales" en columnas sin zona y hacer aritmética con offsets fijos.
- Prevenir el solape solo con un `if` en la aplicación.
- Materializar todos los slots como filas y tratarlos como única verdad.
- Marcar la cita cancelada pero dejar el hueco ocupado por el constraint.
- Reprogramar liberando el hueco viejo antes de asegurar el nuevo.

## Checklist

- [ ] Instantes en UTC (`timestamptz`); zona local como dato aparte; sin aritmética de offsets fijos.
- [ ] Disponibilidad calculada en el servidor (reglas − citas − bloqueos), con DST resuelto.
- [ ] Exclusion constraint por recurso + rango en la base, excluyendo canceladas.
- [ ] Buffers incluidos en el rango que bloquea la agenda.
- [ ] Estados y transiciones explícitos; reprogramación atómica; historial guardado.
- [ ] Reglas de cancelación/anticipación validadas en el servidor.
- [ ] Recordatorios por job idempotente con la zona correcta.

## Evidencia / DoD

Pegá la **salida literal** de:
- una prueba de concurrencia: dos reservas simultáneas del mismo hueco → una 201 y una 409
  (no dos 201);
- una prueba de zona horaria: una cita creada en una zona se lee correctamente desde otra;
- una prueba de que cancelar libera el hueco (una nueva reserva del mismo rango ahora tiene éxito);
- una reprogramación que falla al reservar el nuevo rango y **no** perdió el viejo.
