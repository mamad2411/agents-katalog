---
name: coolify-databases-backups
description: Gate para PostgreSQL gestionado en Coolify — base nunca pública, conexión por red interna, volúmenes, backups programados a S3-compatible con retención, restore PROBADO, upgrades de versión mayor, staging separado, prohibición de restaurar producción con datos de salud en entornos de prueba sin anonimizar, y backup de la propia instancia (APP_KEY). Usar al crear o tocar una base en Coolify, al programar o auditar backups, antes de un upgrade y en cada simulacro de restore. La estrategia genérica de RPO/RTO, PITR y simulacros es `backup-restore-dr`.
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Bases de datos y backups en Coolify

Complementa a `backup-restore-dr` (RPO/RTO, estrategia general) y `data-privacy-sensitive` (qué datos
pueden salir de producción). Verificado contra coolify.io/docs; ante diferencias, manda la doc
de tu versión.

## 1. Crear la base bien

- Recurso **Database > PostgreSQL** en el mismo server/destination que la API que la usa.
- Imagen fijada por versión mayor (`postgres:16-alpine`, no `latest`); un upgrade mayor es un
  procedimiento, no un cambio de tag (§5).
- Límites de memoria (`limits_memory`) y reserva: Postgres sin límite en un server compartido
  se come el panel.
- Credenciales generadas por Coolify o propias, largas, y **solo** visibles en el panel para
  roles con `read:sensitive`.
- `postgres_conf` para ajustes (`shared_buffers`, `work_mem`, `log_min_duration_statement`)
  versionados en el repo de infraestructura, no editados a mano en el contenedor.

## 2. Red: nunca pública

- **Accessible over the internet / `is_public` = off.** Sin `public_port`.
- La API se conecta por la **URL interna** (nombre del contenedor en la red Docker de Coolify);
  la URL pública solo existe si activaste exposición, y no deberías.
- Si un build necesita la base (migración en build): repensalo — las migraciones/patches corren
  como paso de deploy o job, no en el build. Ver `release-and-rollback`.
- Acceso humano puntual: túnel SSH al server (`ssh -L 5432:<container-ip>:5432`) con registro
  de quién, cuándo y para qué; jamás abrir el puerto "un ratito".
- Un `DATABASE_URL` de producción no viaja por chat, PR ni preview deployment.

## 3. Persistencia

- Los datos viven en un **volumen** gestionado por Coolify; borrar el recurso puede borrar el
  volumen: confirmá el comportamiento de tu versión antes de eliminar cualquier base.
- La limpieza automática de Docker con "borrar volúmenes sin usar" activo es un riesgo si una
  base está detenida: mantené las bases corriendo o desactivá esa opción en ese server.
- Un restore nunca se hace "sobre" el volumen a mano: usá el procedimiento de §4.

## 4. Backups programados

Configurá en el recurso (o por CLI `coolify database backup create`): frecuencia cron, retención
local y **copia a S3-compatible** (`--save-s3 --s3-storage-uuid`). Reglas:
- **Producción: mínimo diario**, más frecuente si el RPO lo exige. Retención local corta
  (disco) + retención larga en S3 con versionado del bucket.
- S3 en **otro proveedor o cuenta** que el server; credenciales con permiso solo de escritura
  al bucket de backups.
- Notificación **backup fallido** a un canal vigilado. Un backup que falla en silencio
  durante semanas es la falla más común.
- Cifrado: el dump contiene datos sensibles. Bucket cifrado en reposo, acceso mínimo, registro de acceso.
- Backup lógico (`pg_dump`) es lo que Coolify hace; para PITR o réplicas necesitás una
  solución aparte (ver `backup-restore-dr`).

## 5. Restore

Un backup no restaurado no es un backup. **Simulacro trimestral mínimo**, y siempre antes de un
upgrade mayor.

Desde el panel: base corriendo → **Configuration > Import Backup** → revisá **Custom Import
Command** y **Backup includes all databases** → **Restore from S3** (o subir archivo) → **Check
File** → confirmar → leer **Database Restore Output** hasta el final antes de reconectar apps.

Reglas:
- Restaurá en una base **nueva de staging**, no sobre producción, salvo incidente declarado.
- Después del restore, corré las consultas de `data-quality-validation` (conteos, huérfanos)
  y una prueba funcional real.
- Medí el tiempo total (RTO real) y registralo.

### Datos sensibles y entornos de prueba

Restaurar producción en staging/dev/preview **está prohibido sin anonimizar**: nombres,
documentos, contactos, notas clínicas, adjuntos. Opciones en orden de preferencia: seeds
sintéticos (`seed-data-catalogs`, `test-data-management`); dump anonimizado por script
versionado y revisado; subconjunto sin tablas clínicas. Ver `data-privacy-sensitive`.

## 6. Upgrade de versión mayor

`pg_upgrade` no ocurre por cambiar el tag: el volumen de una versión no arranca con la otra.
Procedimiento: backup verificado → base nueva con la versión destino → restore → validar →
apuntar la API → conservar la vieja unos días → borrar. Para la base **interna de Coolify**
existe el script oficial `/data/coolify/source/upgrade-postgres.sh <versión>` (detiene el
contenedor `coolify` momentáneamente); verificá con
`docker exec coolify-db sh -lc 'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Atc "SHOW server_version;"'`.

## 7. Backup de la instancia de Coolify

Perder Coolify sin backup = perder secretos, claves SSH y configuración de todos los recursos.
- Guardá el **`APP_KEY`** de `/data/coolify/source/.env` en un gestor de secretos: cifra los
  secretos de la base de Coolify; sin él, el restore no puede leerlos.
- Dump manual: `docker exec coolify-db pg_dump --format=custom --no-acl --no-owner --username=coolify coolify > /data/backups/coolify-db-<fecha>.dmp`,
  copiado fuera del server (o backup de instancia a S3 desde el panel).
- Guardá también `/data/coolify/ssh/keys/` y la versión de Coolify vigente.
- Restore en server nuevo: instalar Coolify, reemplazar SOLO `APP_KEY` en el `.env` nuevo,
  `pg_restore --clean --if-exists --exit-on-error --no-acl --no-owner` dentro de `coolify-db`.

## 8. Staging separado

Base de staging propia (server o al menos recurso y credenciales distintos), tamaño acotado,
datos sintéticos, mismos backups pero retención corta. Ningún proceso de staging tiene
credenciales de producción.

## Evidencia / Definition of Done

Para afirmar "los backups funcionan" pegá, literal:
1. Configuración del backup (frecuencia, S3, retención) y el último **backup exitoso con fecha**.
2. Salida del **Database Restore Output** del último simulacro, con fecha y duración.
3. Consultas de verificación post-restore con sus conteos.
4. Confirmación de que la base **no** es pública (`is_public: false`, sin `public_port`).
5. Dónde está guardado el `APP_KEY` y la fecha del último backup de instancia.

Sin (2) el veredicto es BLOCKED, no PASS. Ver `evidence-and-verification`.

## Checklist

- [ ] Imagen con versión mayor fijada; límites de memoria; conf versionada.
- [ ] Base no pública; API por URL interna; acceso humano solo por túnel con registro.
- [ ] Backups diarios a S3-compatible externo, cifrados, con alerta de fallo.
- [ ] Simulacro de restore en los últimos 90 días con RTO medido.
- [ ] Nunca producción con datos sensibles en staging/dev/preview sin anonimizar.
- [ ] `APP_KEY` y claves SSH de Coolify resguardados fuera del server.
- [ ] Procedimiento de upgrade mayor ensayado en staging antes que en producción.
