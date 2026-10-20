---
name: backup-restore-dr
description: Gate de backups, restore y recuperación ante desastres para PostgreSQL y el stack completo — RPO/RTO acordados, backups lógicos (pg_dump) vs físicos con archivado de WAL y recuperación a un punto en el tiempo (PITR), cifrado, copia fuera del sitio, restore PROBADO periódicamente, reconstrucción del stack desde cero como ejercicio y runbook. Usar al diseñar o revisar la estrategia de backup de un servicio, antes de una operación destructiva o un cambio de esquema riesgoso, al preparar un simulacro, o al afirmar que "hay backups". La base gestionada en Coolify: `coolify-databases-backups`.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Backup, restore y recuperación ante desastres

Un backup que nunca se restauró no es un backup: es un archivo con esperanza. Esta skill no
acepta "hay backups configurados" como estado; acepta "restauramos el de tal fecha en tanto
tiempo y los datos verificaron". En un sistema con datos clínicos y contables, perderlos o no
poder recuperarlos a tiempo es un incidente mayor.

## 1. RPO y RTO: primero el número, después la herramienta

| Término | Pregunta | Lo decide |
|---|---|---|
| **RPO** (punto de recuperación) | ¿Cuántos minutos de datos podemos perder? | Negocio + responsable del dominio |
| **RTO** (tiempo de recuperación) | ¿Cuánto podemos estar caídos? | Negocio |

- Se acuerdan **por escrito, por sistema**, antes de elegir tecnología. Un dump nocturno implica
  un RPO de hasta 24 h: si el negocio tolera 15 minutos, esa estrategia no sirve por más que
  "funcione".
- El RTO incluye **todo**: detectar, decidir, conseguir infraestructura, bajar el backup,
  restaurar, verificar, reapuntar la aplicación. No solo el tiempo de `pg_restore`.
- Los valores viven en el runbook del proyecto y se revisan cuando cambia el volumen de datos.

## 2. Lógico vs físico

| | Lógico (`pg_dump`) | Físico (base backup + WAL) |
|---|---|---|
| Qué copia | Una base, como objetos y datos | El cluster entero, a nivel de archivos |
| Consistencia | Consistente aun con la base en uso; no bloquea lectores ni escritores | Consistente al reproducir el WAL |
| Granularidad de recuperación | El instante del dump | Cualquier punto en el tiempo (PITR) |
| Portabilidad | Entre versiones mayores y arquitecturas | Misma versión mayor |
| Restore selectivo | Sí (una tabla, un schema) | No: todo el cluster |
| Sirve para | Migrar, clonar a staging, RPO holgado, copia de resguardo portable | RPO de minutos, bases grandes |

Regla: producción con RPO exigente ⇒ **físico + archivado de WAL**, y además un lógico
periódico como segunda vía portable. No son alternativas excluyentes.

### Lógico — lo que hay que saber

- `pg_dump` exporta **una sola base** y **no** incluye objetos globales (roles, tablespaces):
  esos salen con `pg_dumpall --globals-only`. Un restore sin roles falla o queda con dueños rotos.
- Formato custom (`-Fc`) o directorio (`-Fd`), nunca texto plano para producción: permiten
  restore selectivo y paralelo. Solo el formato directorio admite dump paralelo (`-j`).
- `pg_restore -j N` paraleliza carga de datos, índices y constraints (formatos custom y
  directorio). **No se combina con `--single-transaction`**: elegí velocidad o atomicidad.
- `--clean --if-exists` para pisar una base existente; `--create` para que cree la base;
  `--exit-on-error` para no seguir tras el primer fallo (por defecto continúa y cuenta errores
  al final: un restore "terminado" puede estar incompleto — leé la salida).
- `pg_restore --list` + `--use-list` para restaurar solo parte del archivo.
- Tras restaurar, correr `ANALYZE`: sin estadísticas el planificador elige mal.

### Físico y PITR — lo que hay que saber

1. Archivado de WAL: `wal_level = replica` (o superior), `archive_mode = on`, y un
   `archive_command` (o `archive_library`) que **devuelva distinto de cero si falla** y no pise
   archivos existentes.
2. Base backup con `pg_basebackup`.
3. Recuperación: restaurar el base backup, definir `restore_command`, opcionalmente un objetivo
   (`recovery_target_time`, `recovery_target_name`, `recovery_target_xid`), crear el archivo
   `recovery.signal` en el directorio de datos e iniciar el servidor.
4. Monitoreá el archivado: si el `archive_command` falla en silencio, el WAL se acumula en el
   servidor y el RPO real se degrada sin que nadie lo vea. Alerta por atraso de archivado.
5. Tras crear o eliminar un tablespace, tomá un base backup nuevo.

Procedimiento completo y advertencias: capítulo *Continuous Archiving and Point-in-Time
Recovery* de la doc oficial de PostgreSQL de **tu versión**. En plataformas gestionadas o
self-hosted con backups integrados, verificá qué hacen de verdad: `coolify-databases-backups`.

## 3. Protección de los backups

- **Cifrado** en tránsito y en reposo. Un backup contiene toda la PII del sistema sin los
  controles de acceso de la aplicación: es el activo más sensible que tenés (`data-privacy-sensitive`).
- La **clave de cifrado se guarda separada** del backup y también tiene resguardo. Backup cifrado
  con la clave perdida = sin backup.
- **Copia fuera del sitio**: al menos una copia en otra cuenta/proveedor/región que el servidor
  de producción **no pueda borrar** con sus credenciales. El ransomware y el error humano borran
  lo que alcanzan. Regla de orientación 3-2-1: tres copias, dos medios, una fuera del sitio.
- Retención por niveles (diarios, semanales, mensuales) acorde a obligaciones legales del
  dominio: los plazos los fija el responsable legal (`regulatory-compliance-mapping`).
- Inmutabilidad u *object lock* en el almacenamiento si está disponible.
- Acceso a backups restringido, con registro (`audit-trail-history`).
- Un dump de producción **no** se restaura en una máquina de desarrollo: `test-data-management`.

## 4. El alcance no es solo la base

Inventario de lo que hace falta para volver a operar, cada ítem con su backup y su dueño:

- Base(s) de datos y objetos globales (roles).
- Almacenamiento de archivos y adjuntos (`file-uploads-media`).
- Secretos, claves de cifrado, certificados (`environment-secrets-config`).
- Configuración de infraestructura, DNS, variables de entorno.
- Stores derivados (índices de búsqueda, caches): ¿se respaldan o se **reconstruyen** desde la
  base? Si se reconstruyen, ese tiempo cuenta para el RTO.
- Código y modelo están en git: verificá que el remoto no sea la única copia.

## 5. Restore probado

1. **Simulacro calendarizado** (la frecuencia la define el proyecto; que exista y se cumpla).
   Restore completo en entorno aislado, cronometrado.
2. Verificación de los datos restaurados con `data-quality-validation`: conteos contra la
   fuente, huérfanos, invariantes, y el dato más reciente presente (mide el RPO real).
3. Levantar la aplicación contra la base restaurada y correr el smoke test
   (`deployment-verification-smoke`).
4. Registrar: backup usado, tiempos por etapa, problemas, RPO y RTO **medidos** vs acordados.
5. Si el RTO medido supera al acordado, la estrategia **no cumple**, aunque los datos estén sanos.

Además, automatizá una verificación barata en cada backup: que el archivo existe, pesa lo
esperable (una caída brusca de tamaño es una alarma) y `pg_restore --list` lo lee.

## 6. Reconstrucción desde cero

Ejercicio distinto del restore: levantar el stack completo en una máquina limpia siguiendo solo
el repo y el runbook — esquema generado desde el modelo (`model-driven-schema`), catálogos
recargados (`seed-data-catalogs`), servicios arriba (`docker-local-stack`). Detecta dependencias
no documentadas, pasos manuales que "todos saben" y secretos que viven en una sola laptop. Todo
lo que haya que preguntarle a una persona es un defecto del runbook.

## 7. Runbook

Un documento por sistema, ejecutable por alguien que no lo escribió, a las 3 AM:

- RPO/RTO acordados y últimos medidos.
- Dónde están los backups, cómo se accede, dónde está la clave.
- Comandos exactos de restore, con placeholders claros, en orden.
- Cómo decidir el objetivo de recuperación ante corrupción lógica (un `DELETE` erróneo): PITR a
  *justo antes* del evento.
- Cómo verificar y cómo reapuntar la aplicación.
- A quién avisar y qué comunicar (`incident-response-postmortem`).

## Anti-patrones

- "El proveedor hace backups" sin haber restaurado nunca uno.
- Única copia en el mismo servidor o disco que la base.
- Dump en texto plano sin cifrar en un bucket accesible.
- `archive_command` que siempre devuelve 0.
- Antes de una operación destructiva, "sacar un backup" sin verificar que se puede leer.
- Medir el RTO como el tiempo del comando de restore.

## Checklist

- [ ] RPO y RTO acordados por escrito para este sistema.
- [ ] Estrategia coherente con el RPO (PITR si es de minutos).
- [ ] Objetos globales y todo el inventario del §4 cubiertos.
- [ ] Backups cifrados; clave resguardada aparte.
- [ ] Copia fuera del sitio que producción no puede borrar; retención definida.
- [ ] Alerta por fallo o atraso de backup y de archivado de WAL.
- [ ] Último simulacro de restore dentro del período definido, con tiempos registrados.
- [ ] Runbook actualizado y ejecutado por alguien distinto de su autor.

## Evidencia / Definition of Done

Para afirmar "los backups sirven" pegá **literal**: (1) salida del comando de restore con su
resumen de errores, (2) tiempos por etapa y total vs RTO, (3) timestamp del dato más reciente
restaurado vs momento del backup (RPO medido), (4) tabla de `data-quality-validation` sobre la
base restaurada, (5) smoke test de la aplicación contra ella, (6) lo no cubierto. Ver
`evidence-and-verification`.
