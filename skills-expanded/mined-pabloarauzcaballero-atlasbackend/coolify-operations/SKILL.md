---
name: coolify-operations
description: Operación diaria de Coolify self-hosted — logs y terminal, límites de CPU/memoria, limpieza de Docker y disco, notificaciones, actualización de Coolify, roles y API tokens con permiso mínimo, deploys disparados desde GitHub Actions por API/webhook, varios servers y runbook para deploys colgados, 502/503/504 y proxy que no enruta. Usar al operar o diagnosticar la plataforma, automatizar deploys, dar acceso a alguien, o cuando un dominio deja de responder.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Operar Coolify

Configuración inicial y build packs en `coolify-deployment`; bases y backups en
`coolify-databases-backups`; hardening del VPS en `server-hardening`. Verificado contra
coolify.io/docs; si tu instancia difiere, manda la doc de tu versión.

## 1. Arquitectura que conviene conocer

Coolify corre como Docker Compose con cuatro contenedores: `coolify` (app), `coolify-db`
(Postgres propio), `coolify-redis` (colas/caché) y `coolify-realtime` (Soketi + terminal web,
puertos internos 6001/6002). En cada upgrade los compose base se **sobrescriben**: no edites
`docker-compose.yml`/`docker-compose.prod.yml`; los cambios van en el override soportado
(`docker-compose.custom.yml`) y su `.env` en `/data/coolify/source/.env`. Las apps que
desplegás NO viven en esos compose, así que un upgrade de Coolify no las reinicia.

## 2. Logs, terminal y estado

- **Logs** del recurso desde el panel; para builds, el log de la operación en **Deployments**.
- **Terminal** dentro del contenedor para verificar desde adentro (`curl localhost:$PORT/health`).
- Lo que el panel no muestra: en el server, `docker ps`, `docker logs <container>`,
  `docker inspect <container> --format '{{json .State.Health}}'`.
- Antes de "reiniciar a ver si anda": leé el log completo del deploy y el del contenedor.
  Ver `root-cause-debugging`.

## 3. Recursos por contenedor

Cada application/database acepta límites: `limits_memory`, `limits_memory_swap`,
`limits_memory_reservation`, `limits_cpus`, `limits_cpuset`, `limits_cpu_shares`. Reglas:
- Ponéle límite de memoria a TODO lo que corre en un server compartido; un proceso Node sin
  límite puede tumbar el panel y la base.
- Reservá memoria para la propia instancia de Coolify (override: `cpus`, `mem_limit`,
  `mem_reservation` sobre el servicio `coolify`).
- Medí antes de ajustar: consumo real bajo tráfico, no adivinar.

## 4. Disco y limpieza automática

Imágenes y capas de build llenan el disco y hacen fallar deploys. Coolify limpia por cron o por
umbral de uso (**Automated Docker cleanup** por server: frecuencia, umbral, si borra redes y
volúmenes sin usar, imágenes a conservar). La limpieza consume CPU: programala en horario de
poco tráfico. Activá la notificación **Server Disk Usage**. Nunca "limpies" volúmenes a mano
en un server con bases sin backup verificado.

## 5. Notificaciones

Canales (email, Discord, Telegram, Slack, webhook...) y eventos por categoría. Mínimo para
producción: deploy fallido, contenedor detenido/unhealthy, backup fallido, disco, server
unreachable, Traefik desactualizado. El webhook de notificación trae un payload con
`pull_request_id`/`preview_fqdn` cuando aplica a previews. Ruteá alertas a un canal que alguien
mire (ver `backend-observability`).

## 6. Actualizar Coolify

- Antes: backup de la instancia (`coolify-databases-backups` §6) y leer las release notes.
- Actualización desde el panel (auto-update opcional) o script oficial. Los cuatro contenedores
  de infraestructura se recrean; las apps no.
- Después: panel accesible, proxy sano, un deploy de prueba en staging.
- No actualices un viernes a la tarde ni con un deploy en curso.

## 7. Equipos, roles y tokens

- Roles: **Owner**, **Admin**, **Member**. Un Member puede crear tokens `read`, pero no otorgar
  `read:sensitive`, `write`, `deploy` ni `root`.
- Permisos de API token: `read` (valores sensibles redactados), `read:sensitive` (secretos,
  logs, envs), `write`, `deploy` (deploys, restarts, stops, webhooks), `root` (salta chequeos,
  sigue atado al team). Elegir `root` en el panel quita los demás.
- Regla: **un token por integración, con el mínimo permiso** (CI de deploy = solo `deploy`),
  nombre que diga quién lo usa, y revocación en **Keys & Tokens > API Tokens** si se filtra.
- La API debe estar habilitada a nivel instancia; se puede restringir por allowlist de IPs.
- 2FA obligatorio para Owners/Admins (ver `server-hardening`).

## 8. Disparar deploys desde CI

Endpoint `POST /api/v1/deploy` (también `GET`) con `uuid` **o** `tag` (no ambos) y `force`
opcional. `Authorization: Bearer <token con deploy>`. Respuestas: 401 token inválido/ajeno,
403 sin permiso `deploy`, 429 rate limit o cola ocupada (respetá `Retry-After`).

```yaml
# Paso final de un job de GitHub Actions, SOLO después de tests e imagen publicada
- name: Trigger Coolify deployment
  run: |
    curl --fail --request POST "${{ secrets.COOLIFY_URL }}/api/v1/deploy" \
      --header "Authorization: Bearer ${{ secrets.COOLIFY_TOKEN }}" \
      --header "Content-Type: application/json" \
      --data '{"uuid":"${{ vars.COOLIFY_API_UUID }}","force":false}'
```

Tags: agrupá recursos (`api`, `worker`) y desplegalos juntos por `tag`. El webhook por recurso
(`/api/v1/deploy?uuid=...&force=false`) se copia desde el panel; la URL identifica, el token
autoriza. Ver `github-actions-ci`.

## 9. Varios servers

Server de build separado (**use_build_server**) evita que los builds compitan con producción.
Cada server tiene su proxy, su firewall (`server-hardening`) y su limpieza. Los recursos de
distintos servers no comparten red: bases y apps del mismo entorno, en el mismo server/destination.

## 10. Runbook de diagnóstico

| Síntoma | Causa típica | Qué hacer |
|---|---|---|
| Deploy "en cola" sin avanzar | Otro deploy del mismo recurso en curso; cola ocupada; server sin recursos | Ver Deployments, cancelar el colgado, revisar CPU/disco del server |
| Build falla | Falta de disco, versión de Node, comando de build/instalación, secreto solo runtime | Leer el log de build entero; probar el Dockerfile localmente |
| Build OK, **502 Bad Gateway** | Puerto mal (Ports Exposes ≠ puerto real) o app escuchando en `localhost` | Logs → confirmar `0.0.0.0` y puerto → corregir |
| **503 No available server** | Ningún contenedor healthy bajo esa URL | Healthcheck desde Terminal; `curl`/`wget` presente; certificado/dominio |
| **504 Gateway Timeout** | La app responde lento o streaming largo | Optimizar; si es legítimo, ajustar timeouts de Traefik en la config del proxy (`respondingTimeouts`) |
| Certificado no emitido | DNS no apunta, puerto 80 cerrado, rate limit de Let's Encrypt | Verificar DNS y firewall; staging CA para probar |
| Contenedor reinicia en loop | Crash al arrancar (env faltante, migración) | `docker logs`; corregir causa; no subir retries |
| Panel lento/caído | Server saturado, disco lleno | Límites de memoria, limpieza, mover builds a build server |

Cada intervención en producción deja registro: qué se tocó, por qué, resultado. Ver
`incident-response-postmortem`.

## Checklist

- [ ] Límites de memoria/CPU en todos los recursos; reserva para Coolify.
- [ ] Limpieza automática de Docker programada; alerta de disco activa.
- [ ] Notificaciones de deploy fallido, unhealthy, backup y server unreachable a un canal vigilado.
- [ ] Tokens con permiso mínimo, uno por integración, con dueño y fecha.
- [ ] 2FA en Owners/Admins; Members sin tokens de escritura.
- [ ] Backup de instancia antes de cada upgrade; upgrade probado en staging.
- [ ] Runbook anterior a mano; ninguna intervención sin registro.
