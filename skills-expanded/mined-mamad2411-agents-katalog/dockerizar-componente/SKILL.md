---
name: dockerizar-componente
description: Dockeriza un componente FaaST (micro .NET, gateway, frontend React, servicio Node/Python) siguiendo el estándar de Confirming 2.0 y micro-api-back — analiza el repo, elige la familia de Dockerfile, genera Dockerfile + .dockerignore + docker-compose.yml + workflow, y deja el checklist de cutover. Usala cuando haya que contenerizar un componente legado, revisar un Dockerfile existente, o preparar el pase de un componente de PM2 a Docker.
---

# Dockerizar un componente FaaST

> **ESTADO: ACTIVA (estándar de Plataforma FAAST, 2026-09-22).** Validada con los pilotos reales de apiback y micro-backoffice. Acompaña a ADR-016.

## Alcance y relación con `deployment-standard`

Las dos skills son del plugin dev-team y **no se contradicen: se reparten el trabajo.**

| Skill | Responde | Quién la carga |
|---|---|---|
| **`deployment-standard`** | **Las reglas** (R1–R9, familias, compose, red, config, versionado, carpeta ADR-002) y **la operación segura** del servidor (inventario en solo lectura, deploy, cutover, BD local vs remota) | `infra`, `/dev-team:deploy`, `/dev-team:deploy-check`, `cloudsec` |
| **`dockerizar-componente`** (esta) | **El procedimiento para producir los artefactos de UN componente** (análisis del repo, elección de familia, Dockerfile/.dockerignore/compose/workflow desde plantilla, mapeo de appsettings, health con versión, verificación local, plan de cutover y checklist) | `infra` (y `backend` cuando prepara su servicio para contenedor) |

Equivalencias, para no duplicar: regla 1 = R4 · regla 2 = R1 + R2 · regla 3 = R8 · regla 4 = §3 del estándar · regla 9 = §5 · regla 10 = §6 · regla 11 = §7 (ADR-002) · regla 12 = R9. Las reglas de esta skill que el estándar no detalla (stub de Visual Studio, Hangfire de una réplica, `pm2 save` en el cutover, `HOME=/tmp` para UID arbitrario) **se suman**, no lo reemplazan. **Si alguna vez encontrás una diferencia real entre las dos, no elijas en silencio:** se para, se reporta al Lead y manda lo desplegado en las implementaciones de referencia hasta que se corrija la skill.

Los **valores** (servidores, usuario de despliegue, puertos existentes, instancias) salen del inventario del proyecto y de `config.json` → `deploy`, nunca de esta skill. Plantillas en `${CLAUDE_PLUGIN_ROOT}/skills/dockerizar-componente/templates/`.

## Qué hace esta skill

Te lleva de "hay un repo que corre con PM2" a "hay una imagen en GHCR, un compose, un workflow y un plan de cutover reversible", sin inventar nada: el estándar ya existe y está desplegado en `micro-api-back` y `faast-confirming-2.0`.

## Qué NO hace

- **No despliega.** Genera artefactos y deja el checklist; el deploy lo ejecuta infra con el workflow.
- **No toca servidores.** Ni instala Docker, ni edita vhosts, ni reinicia procesos.
- **No inventa configuración.** Si no sabés el valor real de una variable, se pide — nunca se adivina ni se copia del `appsettings` versionado (que está desactualizado y además tiene credenciales).
- **No dockeriza bases de datos, Apache ni runners.**

---

## Reglas duras (si una se rompe, se para y se avisa)

1. **Cero secretos en la imagen.** Ni `appsettings` con valores, ni tokens, ni certificados, ni `.env`. Credenciales de build solo por `--mount=type=secret`.
2. **El contenedor corre con el UID/GID del usuario de despliegue del servidor destino** (en Amazon Linux, `ec2-user`; no un usuario técnico dedicado tipo `appuser`; regla fija de Plataforma FAAST, 2026-09-22, reemplaza la version anterior de esta regla). **Nunca root** (nunca UID 0). Puerto interno **8080**, siempre. El UID/GID va **por variable** (`RUN_UID`/`RUN_GID` en el `.env.<instancia>`, seteado en `docker-compose.yml` con `user: "${RUN_UID:-1000}:${RUN_GID:-1000}"`), nunca hardcodeado en el Dockerfile — `1000` es el default de fábrica de `ec2-user` en las AMI de Amazon Linux, pero **hay que confirmarlo en cada servidor nuevo** con `id <usuario-deploy>` antes de asumirlo (no todos los servidores tienen por que coincidir). El Dockerfile NO crea ni cambia a un usuario propio: la imagen se construye y queda con archivos legibles por defecto, y quien corre el proceso lo define `docker-compose.yml` en runtime.
   - **Por qué (dejarlo escrito para quien lo audite después):** correr como `ec2-user` le da al contenedor el mismo alcance de lectura que tiene el administrador del servidor — incluidos los `.env`/certificados de otros componentes y, en servidores donde `ec2-user` tiene `sudo` sin contraseña, una vía teórica de escalar a control total del host si el contenedor se ve comprometido. Es una decisión consciente de Plataforma FAAST para resolver de raíz el problema de permisos entre certificados/secretos (propiedad de `ec2-user`, `600`) y contenedores no-root (que antes no podían leerlos sin tocar permisos archivo por archivo). Sustituye al patrón anterior de `appuser`/UID dedicado (ej. UID 999), que sigue puesto en `apiback` y `micro-backoffice` y hay que migrar (pendiente registrado del proyecto de dockerización).
   - **nginx (F1-F4) NO se resuelve igual que .NET.** .NET arranca con cualquier UID porque solo lee `/app`; nginx **escribe** (pid, temp paths, `env.js`) y trae una directiva `user` que un master no-root no puede aplicar. La imagen se **prepara para UID arbitrario** sin crear usuario: se borra la directiva `user`, pid y temp paths van a `/tmp` (1777), los logs se dejan como están (ya son symlinks a `/dev/stdout`/`/dev/stderr`) y `env.js`/`health.json` se generan en `/tmp` y se sirven con `alias`. Todo esto ya viene aplicado en `templates/Dockerfile.frontend`, `templates/nginx.conf` y `templates/frontend-entrypoint.sh`. Detalle y porqué: skill `deployment-standard` §2 (nota Frontend/nginx).
   - **D4 / N1 / P1:** un UID arbitrario **no tiene home escribible**. Chromium, fontconfig, npm y Python escriben en `$HOME`: hay que redirigirlo con `ENV HOME=/tmp` (+ `XDG_CACHE_HOME`/`NPM_CONFIG_CACHE`). Ya viene en las plantillas.
3. **`provenance: false`** en todo `build-push` a GHCR, y tag `sha-<sha>` permanente que nunca se borra.
4. **Un `docker-compose.yml` por repo**, byte-idéntico entre ambientes; toda diferencia en `.env.<instancia>`.
5. **Nunca reutilizar un Dockerfile stub de Visual Studio.** 17 repos legado los tienen y están desalineados con el `TargetFramework`. Se reescriben desde plantilla.
6. **Hangfire: una sola réplica por base de storage y ambiente.** Sin excepciones.
7. **No se escribe nunca en el repo de código** desde la coordinación: los artefactos generados se proponen, se revisan, y se commitean por el flujo normal de ramas (ADR-039).
8. **Si el componente hace autenticación**, el contenedor debe **abortar el arranque** si falta la clave de firma. Prohibido el fallback silencioso. Requiere review de cybersec.
9. **Todo el `appsettings` a variables de entorno** (Plataforma FAAST, 2026-09-21). Ver Paso 4.
10. **Health obligatorio con versión interna y estado** (`/health/live` y `/health`, sin datos sensibles). Ver Paso 4.5.
11. **Misma estructura de carpetas de despliegue que apiback y Confirming 2.0 (ADR-002):** `$HOME/deploy/<repo>/<instancia>/` en el servidor, con `docker-compose.yml`, `.env.<instancia>` (600, fuera de git) y `deploy-history.log`, todo del usuario que corre el CD. Un solo token de instancia para rama, `.env`, carpeta, proyecto compose, Environment y contenedor. No inventar rutas distintas por componente.
12. **`init: true` en TODO `docker-compose.yml`, sin excepción (Plataforma FAAST, 2026-09-23 — hallazgo fleet-wide).** Dentro del contenedor la app es PID 1, y el kernel **ignora en PID 1** las señales sin handler cuya acción por defecto es terminar el proceso: una excepción .NET no atrapada termina siempre en `abort()`→`SIGABRT`, pero como PID 1 el proceso **nunca sale** — el contenedor queda `Up (unhealthy)` girando al 100% de un core **para siempre**, y `restart: unless-stopped` **no rescata nada** porque el proceso nunca termina (no hay salida que reinicie). Confirmado empíricamente en `gw-gestion-cobranza`: el mismo binario con `docker run --init` (tini como PID 1) sale con código **134** al instante. `init: true` es el fix estándar, universal y de infraestructura — ya viene puesto en `templates/docker-compose.yml`; no depende de que la app maneje excepciones ni reemplaza ningún mitigante app-level puntual que ya exista (ej. un `Environment.Exit` propio para un caso de config faltante), que se conserva como capa adicional.

---

## Procedimiento

### Paso 1 — Identificar el componente (5 min, solo lectura)

Recolectá, sin ejecutar nada:

| Dato | Dónde |
|---|---|
| Repo y rama de trabajo | `git ls-remote`, o el inventario del proyecto (`inventario/asis-repos-legado.md` en la coordinación, si existe) |
| `TargetFramework` real | El `.csproj`, **no** el `FROM` de un Dockerfile existente |
| Nombre del `.dll` de entrada | `AssemblyName` del `.csproj`, o el `pm2 jlist` del servidor |
| Ubicación del `.sln` | Afecta el `COPY` del stage de build |
| Puerto actual | El vhost de Apache y el `--urls` del proceso PM2 |
| Dependencias de SO | `grep` de `System.Drawing`, `SkiaSharp`, `PuppeteerSharp`, `Selenium`, `DirectoryServices`, `GemBox` |
| Archivos en disco | `cert/`, `Templates/`, `Assets/`, `TemplateEmail/`, `FileServer/`, `Logs/` |
| ¿Es host de Hangfire? | `Hangfire.*` en el `.csproj` + `RecurringJob` en el código |
| Quién lo consume | El inventario AS-IS (§4.2) — determina el orden de cutover |

**Bandera roja que hay que buscar siempre:** `UseUrls("http://localhost:...")` hardcodeado. Rompe el binding dentro del contenedor y se diagnostica mal. Si está, **el arreglo de código va primero**, antes del Dockerfile.

### Paso 2 — Elegir la familia

```
¿Frontend?        → Vite: F1 · webpack 5: F2 · webpack 4/React 16: F3 · CRA: F4
¿Node/TS?         → N1
¿Python?          → P1
¿Consola/batch?   → D7 (dotnet/runtime, sin puerto)
¿Chrome/Skia/gdiplus/fuentes? → D4 (Debian, NUNCA alpine)
¿Host de Hangfire?            → D6 (= D1/D2 + una réplica + TZ + dashboard con auth)
¿Gateway Ocelot/YARP?         → D3 (= D1 + ocelot.json montado)
net8/9/10 → D1 · net6/7 → D2 · netcoreapp3.x/net5 → D5 (EOL: decisión pendiente de Plataforma — migrar primero con `migrar-dotnet`)
```

Tabla de familias normativa: skill `deployment-standard` §2.

**Si la familia es D5 (EOL): pará acá.** No se dockeriza nada EOL hasta que la decisión (c) del ADR-016 esté respondida. Reportá y esperá.

### Paso 3 — Generar los artefactos

Copiá la plantilla que corresponda desde `templates/` y ajustá **solo** los parámetros:

| Archivo | Plantilla |
|---|---|
| `Dockerfile` | `templates/Dockerfile.dotnet` · `templates/Dockerfile.dotnet-native` · `templates/Dockerfile.frontend` |
| `.dockerignore` | `templates/dockerignore` |
| `docker-compose.yml` | `templates/docker-compose.yml` |
| Workflow | `templates/build-push.yml` |
| Front: nginx + entrypoint | `templates/nginx.conf`, `templates/frontend-entrypoint.sh` |

Parámetros a completar: `DOTNET_VERSION`, `SOLUTION_DIR`, `PROJECT`, el `.dll` del `ENTRYPOINT`, `HOST_PORT` (= el puerto que ya usa el vhost) y el endpoint del `HEALTHCHECK`.

### Paso 4 — Configuración a variables

> **REGLA DURA (Plataforma FAAST, 2026-09-21): TODO el `appsettings` pasa a variables de entorno.** No se copia, monta ni hornea ningún `appsettings*.json` con valores en la imagen ni en el contenedor: cada clave (incluidas `ConnectionStrings`, URLs de otros servicios, llaves JWT/S3/Sentry, flags y `Logging`) se define como variable en el `.env.<instancia>`. Si una clave del `appsettings` desplegado no tiene su variable, **el componente no está dockerizado**. Ver criterio de verificación abajo.

1. Listá **todas** las claves del `appsettings.json` desplegado (el del servidor, no el del repo), incluidas las anidadas y las de arrays (`Seccion__Lista__0`, `Seccion__Lista__1`…).
2. Mapealas a `Seccion__Clave` (dos guiones bajos **solo** en la variable de entorno; en el código siempre `Seccion:Clave`). Definí también `ASPNETCORE_ENVIRONMENT` y `ASPNETCORE_URLS=http://+:8080`.
   - **Verificación de completitud (obligatoria):** generá la lista aplanada de claves del `appsettings` desplegado y compará contra las variables del `.env`; no debe faltar ninguna ni sobrar ninguna (diff vacío). Adjuntá el diff (solo nombres, nunca valores) al informe del componente.
   - Probá arrancar el contenedor **sin** ningún `appsettings*.json` con valores: si arranca sano y con la configuración correcta, la regla se cumple.
3. Dejá el `appsettings.json` del repo con **estructura y placeholders** (`SET_VIA_ENV`), sin un solo valor real.
4. Armá el `.env.<instancia>` de ejemplo **con los nombres y sin los valores**; el valor real lo pone quien corresponda en el servidor, permisos `600`.
5. Lo que no es texto (certificados de firma, credenciales de terceros, `ocelot.json`) va montado como volumen `:ro`, nunca en la imagen.

### Paso 4.5 — Health obligatorio con versión y estado

> **REGLA DURA (Plataforma FAAST, 2026-09-21): todo repo dockerizado expone un endpoint de health que devuelve la versión interna del componente y su estado.**

Contrato mínimo (JSON, sin autenticación, **sin datos sensibles**: nada de connection strings, hosts, tokens ni mensajes de excepción):

```json
{ "component": "<repo>", "version": "<versión interna>", "status": "Healthy|Degraded|Unhealthy",
  "environment": "<ambiente>", "commit": "<sha corto>", "timestamp": "<UTC ISO8601>",
  "checks": { "<dependencia>": "Healthy|Unhealthy" } }
```

- `GET /health/live`: solo el proceso, sin dependencias. Lo usa el `HEALTHCHECK` de Docker (una caída de la BD no debe reiniciar el contenedor).
- `GET /health` (readiness): con las dependencias (BD, servicios de los que depende). HTTP 200 si Healthy/Degraded, 503 si Unhealthy.
- La versión sale de **una sola fuente: `version.txt`** (el archivo del repo, el mismo que ya usa el CI para el tag/release de git), **leído por la app en runtime** — no de una inyección separada por `--build-arg`/`InformationalVersion`. Todo lo que muestre la versión (health, Scalar/Swagger, cualquier otra vista) lee ese mismo archivo, lo ideal vía un helper compartido cacheado (ej. `VersionInfo.Current`). En .NET, `version.txt` va copiado al output de publish y se lee con `File.ReadAllText`. En frontends con nginx, el entrypoint genera `health.json` a partir del mismo archivo. Un `ARG VERSION` en el Dockerfile, si existe, es solo para **taguear la imagen** en CI/el registro — nunca la fuente que lee la app en runtime, para que no se desincronicen dos mecanismos. Nunca hardcodeada.
- Frontends (nginx): `/health` sirve un `health.json` generado en el entrypoint con `component`, `version` y `status`.
- Verificación: con el contenedor levantado, `docker exec <contenedor> cat /app/version.txt` y `curl /health | jq -r .version` devuelven **la misma cadena**, y el estado es `Healthy`; con la BD caída, `/health/live` sigue 200 y `/health` da 503. Si el componente expone documentación de API, el `info.version` de su documento OpenAPI tiene que dar **esa misma cadena** — es la verificación de tres puntas de la skill `scalar-api-docs` (E-SC-05), automatizada en `templates/verificar-scalar.sh` de esa skill.
- Si `/health` devuelve `unknown`, `1.0.0` o vacío: `version.txt` no llegó a la imagen (falta el `CopyToOutputDirectory`) o la versión está hardcodeada. Las dos cosas bloquean.

### Paso 5 — Verificar la imagen localmente

```bash
docker build -t local/<repo>:test .
docker history local/<repo>:test          # ningún secreto, ningún appsettings con valores
docker run --rm -p 18080:8080 --env-file ./.env.local local/<repo>:test
docker ps                                  # debe llegar a (healthy), no quedarse en (starting)
curl -f http://localhost:18080/<endpoint del healthcheck>
```

Si queda `unhealthy` para siempre: casi siempre es que la imagen `aspnet` no trae `curl`. Instalalo en el stage final (el `apt-get` corre como root **en build**; eso no contradice la regla #2, que habla del usuario en **runtime**).

**Probá siempre con el UID real del servidor destino**, no con el default del motor:

```bash
ssh <servidor> id <usuario-deploy>         # evidencia para el checklist (ec2-user en Amazon Linux)
docker run --rm -u 1000:1000 -p 18080:8080 --env-file ./.env.local local/<repo>:test
docker exec <contenedor> id                # debe dar ese uid/gid, nunca uid=0
```

Si el contenedor arranca como root pero falla con `-u`, falta algo del patrón de UID arbitrario (típico en nginx: pid o temp paths sin mover a `/tmp`, o un `HOME` no escribible en D4/N1/P1).

### Paso 6 — Preparar el cutover (no ejecutarlo)

Redactá el plan con estos 6 puntos, que es lo que infra va a ejecutar:

1. Carpeta `$HOME/deploy/<repo>/<instancia>/` (home del usuario de despliegue) con `.env.<instancia>` (600), `docker-compose.yml` y `deploy-history.log`.
2. `docker compose up -d` en el servidor destino; esperar `healthy`.
3. Smoke **por el camino real** (a través del vhost), comparado contra el proceso PM2 actual.
4. Cambio del `ProxyPass` del vhost: `localhost:<puerto>` → `<IP del servidor nuevo>:<mismo puerto>`; `reload` de Apache.
5. `pm2 stop <proceso>` del proceso anterior — **sin borrar la carpeta** — y **en el mismo paso** `pm2 save` (con respaldo previo `cp -p ~/.pm2/dump.pm2 ~/.pm2/dump.pm2.pre-cutover-<componente>-<ts>`). Verificar que el dump quedó con ese proceso en `stopped`: `python3 -c "import json,os;[print(p['name'],p.get('status')) for p in json.load(open(os.path.expanduser('~/.pm2/dump.pm2')))]"`. **Sin `pm2 save`, el `pm2 resurrect` del arranque (hay servidores de pruebas que se apagan y encienden todos los días, p. ej. QA Total) vuelve a levantar el PM2 viejo**, que choca con el puerto del contenedor (`EADDRINUSE`) y entra en un bucle infinito de reinicios que satura la CPU (incidente real en un servidor de QA, 2026-09-24: ~42 000 reinicios en 10 h por proceso, CPU al 0 % libre). Al día siguiente del cutover, confirmar que `restart_time` del proceso detenido no crece.
6. **Prueba de rollback en el mismo momento**: revertir el `ProxyPass`, verificar que PM2 responde, y volver al contenedor.

### Paso 6.5 — CI/CD: `auto_deploy: true` desde el primer commit (Plataforma FAAST, 2026-09-22)

El patrón de despliegue automático ya está probado y en producción (`apiback`, `micro-backoffice`). Para todo componente **nuevo**, el `.github/deploy-policy.yml` se crea directamente con `auto_deploy: true` para la instancia — **no** arranca en `false` a la espera de un flip manual, salvo que haya una razón puntual para frenarlo (ej. el runner de ese servidor todavía no está confirmado).

Los secretos van por **GitHub Environment** (`secrets_source: github_secrets` si el workflow lo soporta como selector explícito), no por archivo `.env` persistente a mano en el servidor:
1. Crear el GitHub Environment con el nombre de la instancia (ej. `qa_total`), con `deployment_branch_policy` restringido a la rama de ese ambiente.
2. Cargar los secretos sensibles con `gh secret set NOMBRE --env <instancia>` y las variables no sensibles con `gh variable set NOMBRE --env <instancia>`, con los nombres que ya define el bloque `env:` del job de deploy en `cd-<instancia>.yml` (no inventar nombres nuevos).
3. El `.env` real extraído del servidor (`{coordinacion}/env-reales/<componente>-<instancia>.env.real`, gitignored) es la fuente de los valores, nunca se imprime ni se commitea.

### Paso 7 — Cerrar con el checklist

Completá `reference/checklist.md`. Cualquier "no" bloquea el cutover. QA valida con **capturas de pantalla**, no solo con JSON o trazas de red.

---

## Errores que ya costaron tiempo (verificalos siempre)

| Síntoma | Causa real |
|---|---|
| `MSB3202: project file not found` en el restore | El `.sln` se copió aplanado a la raíz; sus referencias a los `.csproj` son relativas a su propia carpeta |
| Contenedor siempre `unhealthy` con la app funcionando | La imagen `aspnet` (Debian slim) no trae `curl` |
| `Connection refused` desde Apache al contenedor | `UseUrls("http://localhost:…")` hardcodeado en el código |
| Compose no encuentra el `.env` | `env_file:` se resuelve contra el checkout del runner, no contra `--env-file`. Usar `ENV_FILE_PATH` absoluto |
| El job se ejecuta dos veces | Dos instancias de Hangfire contra la misma base (el proceso PM2 viejo sigue vivo, o hay una copia en otro servidor) |
| `PlatformNotSupportedException` con `System.Drawing` | .NET 7+ no lo soporta en Linux. Hay que confirmar si el uso es real antes de dockerizar |
| El primer arranque intenta bajar Chromium de internet | PuppeteerSharp sin `ExecutablePath` fijado |
| El front carga pero no llega a ningún gateway | `env.js` horneado en la imagen en vez de generado por el entrypoint |
| CPU del servidor al 100 % y un proceso PM2 con miles de reinicios tras el primer arranque posterior al cutover | Se hizo `pm2 stop` sin `pm2 save`: el dump seguía con el proceso `online`, `pm2 resurrect` lo levantó al bootear y choca en bucle con el puerto del contenedor (`EADDRINUSE`). Fix: `pm2 stop` + `pm2 save` y verificar el dump |

---

## Archivos de esta skill

```
dockerizar-componente/
├── SKILL.md                  (este archivo)
├── templates/
│   ├── Dockerfile.dotnet             D1/D2/D3/D6
│   ├── Dockerfile.dotnet-native      D4
│   ├── Dockerfile.frontend           F1-F4
│   ├── docker-compose.yml
│   ├── dockerignore
│   ├── nginx.conf
│   ├── frontend-entrypoint.sh
│   └── build-push.yml
└── reference/
    └── checklist.md
```

**Fuente de verdad de las reglas:** skill `deployment-standard` (y, si el proyecto lo tiene, su documento `estandares/estandar-dockerizacion-faast.md` en la coordinación).
**Implementaciones de referencia:** `micro-api-back` (ramas de ambiente) y `faast-confirming-2.0/infra/docker/`. Ante cualquier duda entre el documento y lo desplegado, **gana lo desplegado**.
