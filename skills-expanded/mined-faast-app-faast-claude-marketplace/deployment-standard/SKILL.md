---
name: deployment-standard
description: Estandar de dockerizacion y despliegue de FAAST para dev-team - las reglas duras de contenedor (un puerto interno, non-root por UID del host, healthcheck real, cero secretos en imagen, multi-stage, dockerignore, logs a stdout, provenance, init), las familias de Dockerfile (.NET, gateway, frontend/nginx, node, python, batch), convenciones de docker-compose y variables por instancia, exposicion de puertos y red, config por variables de entorno, registry y versionado por version.txt, la estructura de carpeta de despliegue en el servidor, el proceso de despliegue (CI self-hosted y manual), el cutover de PM2 a Docker, la prueba en local, la eleccion de BD local vs remota, y como descubrir de forma SEGURA que hay en un servidor sin romper nada. Cargala al dockerizar un componente, preparar un despliegue, revisar un Dockerfile o inventariar un servidor.
---

# Estandar de dockerizacion y despliegue — FAAST (dev-team)

Este es el estandar que sigue el equipo para contenerizar y desplegar un componente
(microservicio .NET, gateway, frontend, servicio Node/Python, batch). Los VALORES concretos
(IPs, hosts, puertos existentes, nombres de instancia) viven en el inventario del proyecto
(`config.json` → `deploy` y el archivo de inventario de servidores), NUNCA hardcodeados aqui.
Las REGLAS si son fijas. Un componente que rompe una regla dura no se despliega.

**Alcance frente a la skill `dockerizar-componente`:** esta skill es la NORMA (reglas,
convenciones y operacion segura de servidores). `dockerizar-componente` es el PROCEDIMIENTO
con plantillas para producir los artefactos de UN componente (Dockerfile por familia,
`.dockerignore`, compose, workflow, mapeo de appsettings, health con version, verificacion
local, plan de cutover y checklist). Usa las dos: las reglas salen de aqui, los archivos de
alla. Si encuentras una diferencia real entre ambas, no elijas en silencio: reportala al Lead.

## 0. Regla de oro de operacion — no romper nada
Antes de tocar un servidor, un contenedor o un pipeline: **descubre en solo lectura, y cambia
solo con plan y confirmacion**. Nunca borres, nunca `docker compose down` de algo compartido,
nunca reinicies el reverse proxy que sirve a varias apps, nunca edites un vhost sin backup.
Ver §10 (descubrimiento seguro) y §7 (proceso de despliegue).

## 1. Las 9 reglas duras del contenedor (R1–R9)
| # | Regla | Detalle |
|---|-------|---------|
| **R1** | **Un solo puerto interno** | La app escucha en `8080` dentro del contenedor. El puerto del host es `${HOST_PORT}` (variable). |
| **R2** | **Non-root por UID del host** | `user: "${RUN_UID:-1000}:${RUN_GID:-1000}"` en el compose. El Dockerfile NO crea usuario, NO hace `chown`, NO pone `USER`. Confirmar `id <usuario-deploy>` en cada servidor. Nunca root. |
| **R3** | **HEALTHCHECK real** | Que use herramientas que la imagen SI tiene (instalar `curl`, o one-liner sin binario externo). |
| **R4** | **Cero secretos en la imagen** | Credenciales de build solo por `--mount=type=secret`. Jamas `--build-arg` para secretos, jamas `.env`/claves copiadas a capas. |
| **R5** | **Multi-stage siempre** | La imagen final no trae SDK ni toolchain de compilacion. |
| **R6** | **`.dockerignore` obligatorio** | Minimo: `**/bin`, `**/obj`, `**/node_modules`, `.git`, `.env*`. Sin el, el `COPY` arrastra artefactos del host y rompe el build. |
| **R7** | **Logs a stdout/stderr** | Nada de archivos de log dentro del contenedor. |
| **R8** | **Provenance off + tag permanente** | `provenance: false` en el build; tag `sha-<sha>` permanente que nunca se borra. |
| **R9** | **`init: true` en cada compose** | Sin un init como PID 1, la app puede no morir ante SIGABRT y quedar unhealthy al 100% de CPU para siempre. |

## 2. Familias de Dockerfile
Elige la familia por lo que ES el componente. Las imagenes base van PINNEADAS por version (nunca `latest`).

| Familia | Componente | Base |
|---|---|---|
| **D1** | .NET 8/9/10 (API/servicio) | `sdk` → `aspnet` |
| **D2** | .NET 6/7 | mismo patron, base mas vieja |
| **D3** | Gateway Ocelot/YARP | D1 + `ocelot.json` montado `:ro` |
| **D4** | .NET con Chromium/Skia/PDF/fuentes | Debian (NUNCA alpine) |
| **D6** | Host Hangfire | 1 sola replica, `TZ` explicito, dashboard con auth |
| **D7** | Consola / batch | `dotnet/runtime`, sin puerto |
| **F1** | Frontend Vite | node:20 → nginx:alpine |
| **F2** | Frontend webpack 5 | node:20 → nginx:alpine |
| **F3** | Frontend webpack 4 | node 16/20 con openssl-legacy |
| **F4** | Frontend CRA | node 18 |
| **N1** | Node (API/servicio) | node:20-alpine |
| **P1** | Python | python:3.12-slim |
| **X** | Librerias / movil | NO se dockeriza |

Notas por familia:
- **.NET**: instalar `curl` para el healthcheck; copiar el `.sln` conservando su carpeta (aplanarlo rompe el build con MSB3202).
- **Frontend/nginx**: preparar nginx para UID arbitrario — quitar la directiva `user`, mover `pid` y temporales a `/tmp`, generar `env.js`/`health.json` en runtime en `/tmp` y servirlos con `alias`.

## 3. docker-compose (convenciones C1–C8)
- **Un compose por repo**, byte-identico entre ambientes. Toda diferencia vive en `.env.<instancia>`.
- Nombre de proyecto y contenedor: `<repo>-${AMBIENTE}`. Imagen: `<registry>/<org>/<repo>:${IMAGE_TAG}`.
- `env_file: ${ENV_FILE_PATH}` con ruta ABSOLUTA (compose resuelve `env_file` contra el checkout del runner, no contra `--env-file`).
- `AMBIENTE`, `IMAGE_TAG` y `ASPNETCORE_ENVIRONMENT` los exporta CI; nunca viven en el `.env`.
- Defaults: `restart: unless-stopped`, `mem_limit: ${MEM_LIMIT:-512m}`, logging json-file (10m × 3), healthcheck cada 30s, `init: true`, `user:` presente.
- `.env` con permisos `600`, NUNCA versionado. Hangfire nunca se escala (1 replica).
- Confirming 2.0 usa `profiles: public/private` en un solo compose.

## 4. Puertos, red y exposicion
- **Capa publica**: bind `127.0.0.1:${HOST_PORT}:8080`, nunca `0.0.0.0`. El reverse proxy del host (Apache/Nginx) termina TLS y hace `ProxyPass`.
- **Capa privada**: bind `${MS_BIND:-0.0.0.0}`; el perimetro es el Security Group / la red privada.
- Servidores publico y privado son hosts SEPARADOS: no hay red docker compartida entre ellos; el gateway alcanza los micro por `http://${MS_HOST}:<puerto>`.
- **Redes docker compartidas en un host**: la crea UN compose; el resto la referencia `external: true` (nunca `driver: bridge` para una red ajena). Verifica quien la creo antes de tocarla: `docker network inspect <red> --format '{{.Labels}}'`.
- **El reverse proxy compartido va en su PROPIO compose**, jamas dentro del compose de una app (un `down` de la app tumbaria todos los sitios).
- Regla de vhost: cada `:443` que proxya a un contenedor pone `RequestHeader set X-Forwarded-Proto "https"` y `X-Forwarded-Port "443"`.
- Se respetan los puertos existentes del proyecto (del inventario). Apache, bases de datos y runners NO se contenerizan.

## 5. Configuracion y secretos
- **Todo el `appsettings` pasa a variables de entorno**, mapeadas `Seccion__Clave`. El `appsettings.json` del repo conserva solo la estructura con placeholders `SET_VIA_ENV`.
- Verificacion: el diff entre las claves del appsettings desplegado y el `.env` debe ser vacio, y el contenedor arranca sin valores en el appsettings.
- Valores reales se toman del servidor y se guardan fuera de git (`.coordination/env-reales/`, gitignored).
- Certificados, `ocelot.json` y credenciales de terceros se montan `:ro`.
- Un componente con auth ABORTA el arranque si falta su clave de firma (sin fallback silencioso).
- Secretos al despliegue: por GitHub Environment de la instancia (`gh secret set --env`, `gh variable set --env`) o `.env` persistente en el servidor. Confirmar que el secret llega de punta a punta (definido en Environment Y renderizado en el workflow Y pasado en el compose).

## 6. Registry, versionado y health
- Registry: GHCR (o el del proyecto). Tags: `sha-<sha>` (permanente) + `<instancia>-v<version>`.
- **La version tiene UNA fuente: `version.txt`**, leida por la app en runtime; nunca inyectada por `--build-arg`.
- Tags de ambiente: `stage-v…`, `puente-v…`, `demo-v…`. Prod usa `vX.Y.Z`, creada por cut-by-digest SIN rebuild (imagenes inmutables).
- `/health/live` chequea solo el proceso (lo llama el HEALTHCHECK de Docker). `/health` devuelve JSON `{component, version, status, environment, commit, timestamp, checks}` con 200 o 503.
- Al resolver "el tag mas reciente de este commit": SIEMPRE `sort -V | tail -1`, nunca `head -1`/`tail -1` sin ordenar (un release sin cambio de codigo comparte commit y sin ordenar resuelve el tag viejo).

## 7. Proceso de despliegue
### Carpeta en el servidor (ADR-002) — convencion fija
```
$HOME/deploy/<repo>/<instancia>/
├── docker-compose.yml
├── .env.<instancia>        (permisos 600, NUNCA en git)
└── deploy-history.log      (una linea por despliegue: fecha | AMBIENTE | imagen:tag | usuario)
```
Sin segmento `prod/`, sin subcarpeta de version, sin segmento de capa. UN token de instancia se
usa para: la rama, el `.env`, la carpeta, el proyecto compose, el contenedor, el GitHub Environment y el runner.

### Flujo CI (GitHub Actions)
1. Leer `version.txt`. 2. Build + push en `ubuntu-latest` (`provenance: false`, tag `sha-<sha>`).
3. `resolve-auto-deploy` lee `.github/deploy-policy.yml` (`auto_deploy: true` para componentes nuevos).
4. Deploy en un self-hosted runner del servidor destino: `docker compose -p <proyecto> up -d --force-recreate`.
5. Esperar liveness, luego gate por `/health` (readiness). 6. Capturar el RepoDigest y anexar a `deploy-history.log`.
Las instancias son runners elegidos por matriz, no ramas. Ramas de ambiente: `release/faast/stage` → `puente` → `demo` (rebuild real en cada paso); el unico cut formal es demo → prod (PR aprobado por Plataforma).

### Despliegue manual seguro (cuando no hay CI o es puntual)
Plan primero, y en el servidor: `cd ~/deploy/<repo>/<instancia>` → verificar `.env` (permisos 600) →
`docker compose pull` (o cargar imagen) → `docker compose -p <proyecto> up -d --force-recreate` →
esperar health → anexar linea a `deploy-history.log`. Nunca borres la carpeta ni el `.env` previo.

## 8. Cutover de PM2 a Docker (puente de vhost)
1. El contenedor llega a `healthy` en el mismo puerto. 2. Smoke test por el vhost real.
3. Cambiar el `ProxyPass` del loopback a la nueva IP/puerto y **`reload`** Apache (nunca `restart`;
antes `httpd -t` y backup `.bak-<timestamp>` del vhost). 4. `pm2 stop` SIN borrar la carpeta vieja,
y en el mismo paso `pm2 save` (con respaldo previo del dump): sin `pm2 save`, el `pm2 resurrect` del
proximo arranque del servidor vuelve a levantar el proceso viejo, choca con el puerto del contenedor
(`EADDRINUSE`) y entra en un bucle de reinicios que satura la CPU (incidente real; detalle y
verificacion del dump en `dockerizar-componente` Paso 6).
5. Probar el rollback en ese mismo momento. QA valida con capturas. Si algo falla, se revierte el ProxyPass.

## 9. Prueba en local
```bash
docker build -t local/<repo>:test .
docker history local/<repo>:test | grep -iE "secret|token|password|key" || echo "sin secretos en capas"
docker run --rm -u 1000:1000 -p 18080:8080 --env-file ./.env.local local/<repo>:test
curl -fsS localhost:18080/health/live && docker exec <cid> id   # confirmar non-root
```
Stack completo de dev: `docker-compose.dev.yml` (levanta todos los servicios). El ambiente
dev/desa es SIEMPRE local — sin GitHub Environment ni job de deploy en el pipeline.

## 9b. Base de datos: local (Docker) vs remota
Regla del proyecto (confirmar en `config.json` → `deploy.db`):
- **Servidores nunca corren un contenedor de BD.** En ambientes reales la BD es gestionada
  (RDS/instancia dedicada) y llega por `ConnectionStrings__X` como variable de entorno.
- **En dev local hay dos opciones** — elegir explicitamente y dejarla en `config.json`:
  1. **Remota** (BD de desarrollo compartida): sin contenedor local; el `.env.local` apunta al host remoto. Mas fiel, requiere acceso de red y no ensuciar datos compartidos.
  2. **Local en Docker** (`mysql:8.x`/`sqlserver` en el `docker-compose.dev.yml` con datos dummy): aislado, reproducible, ideal para probar migraciones sin afectar a nadie.
- Los tests usan Testcontainers (BD efimera por corrida), independiente de lo anterior.
- Si el proyecto no define cual, PREGUNTAR al usuario una vez y persistir en `config.json` (`deploy.db.devTarget: "remota" | "local-docker"` + el host o el servicio de compose).

## 10. Descubrimiento seguro: "que hay en este servidor" (SOLO LECTURA)
Antes de desplegar o cambiar algo en un servidor, inventaria en solo lectura y registra el
resultado en el inventario del proyecto. Nunca modifiques nada en esta fase.
```bash
ls -la ~/deploy/                       # que componentes/instancias hay desplegados
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker inspect <cid> --format '{{.Config.Image}} | {{.Config.User}} | {{.State.Health.Status}}'
tail -n 20 ~/deploy/<repo>/<instancia>/deploy-history.log   # que version corre y desde cuando
curl -fsS localhost:<HOST_PORT>/health | jq .               # version/commit/checks
docker network ls; docker network inspect <red> --format '{{.Labels}}'  # quien creo la red
```
Cada componente descubierto se agrega al inventario de servidores del proyecto (una fila por
componente/instancia: componente, repo, instancia, ambiente, DNS/IP, puerto, carpeta de deploy,
comando de logs, comando de health, notas). El inventario responde "que corre en esta maquina"
y evita el error de tocar o borrar algo que no era del despliegue en curso.

## Reglas de seguridad de operacion (resumen)
- Solo lectura para descubrir; cambios solo con plan + confirmacion (plan primero).
- Nunca borrar carpetas de deploy, `.env` previos, ni contenedores/imagenes de otros componentes.
- Nunca `docker compose down` de un servicio compartido; nunca `restart` del reverse proxy.
- Vhost: `httpd -t` + backup `.bak-<ts>` + `reload`, jamas `restart`.
- Secretos y `.env` reales: fuera de git, permisos 600; en la evidencia/inventario se cita que existen, no su valor.
- Todo despliegue deja su linea en `deploy-history.log` y actualiza el inventario.
