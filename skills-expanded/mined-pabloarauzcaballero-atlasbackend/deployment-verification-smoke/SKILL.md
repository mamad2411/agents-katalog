---
name: deployment-verification-smoke
description: Gate de verificación post-deploy — healthcheck y readiness, versión desplegada (commit SHA), smoke de los flujos críticos contra la URL real, patch de base aplicado, logs sin errores nuevos, señales estables y criterio de rollback inmediato, con salida literal pegada. Usar después de cualquier deploy a staging o producción, antes de anunciar "está en producción", tras un rollback, y al cerrar un carril cuyo criterio es "desplegado".
allowed-tools: Read Grep Glob Bash
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Verificación post-deploy (smoke)

"Deploy verde en Coolify" significa que el contenedor arrancó, nada más. Esta skill define
qué hay que observar en el entorno real para poder decir "desplegado y funcionando". Aplica
la escalera de `evidence-and-verification`; el rollback en sí está en `release-and-rollback`;
cómo se configura Coolify en `coolify-deployment`.

## 1. Cuándo corre

- Después de **todo** deploy: manual, auto-deploy por push, disparado desde CI, rollback.
- En staging antes que en producción; en producción dentro de los primeros minutos.
- Automatizado en CI cuando el deploy lo dispara CI (job `smoke` después del webhook);
  manual con el mismo guion cuando el deploy fue por push.

## 2. Los siete chequeos

| # | Chequeo | Cómo | Pasa cuando |
|---|---|---|---|
| 1 | **Deploy terminó** | Log de la operación en Deployments | Última línea de éxito; con rolling update: `Rolling update completed` |
| 2 | **Health/readiness** | `curl -fsS https://<dominio>/health` | 200 y el body indica dependencias OK (base, cola) |
| 3 | **Versión correcta** | Endpoint o header de versión con el commit SHA (`SOURCE_COMMIT`) | SHA == el que se quiso desplegar |
| 4 | **Esquema de base** | Query de versión de patch/migración o conteo de la tabla nueva | Coincide con lo que el release exige |
| 5 | **Flujos críticos** | Smoke E2E o `curl` autenticado contra 3–5 rutas clave | Respuestas esperadas, sin 5xx |
| 6 | **Logs** | Logs del contenedor desde el arranque | Sin errores nuevos, sin stack traces, sin reinicios |
| 7 | **Señales** | Tasa de error, latencia p95, contenedor `healthy` | Estables respecto al deploy anterior |

Si (3) falla, lo demás no importa: estás verificando otra versión.

## 3. Guion de smoke

Definí en el CLAUDE.md del proyecto la lista de rutas críticas. Ejemplo de forma:

```bash
BASE="https://api.staging.ejemplo.com"
curl -fsS "$BASE/health" | tee /dev/stderr | grep -q '"status":"ok"'
curl -fsS "$BASE/version" | grep -q "$EXPECTED_SHA"
curl -fsS -o /dev/null -w '%{http_code}\n' "$BASE/v1/public/directory?limit=1"   # espera 200
curl -fsS -o /dev/null -w '%{http_code}\n' "$BASE/v1/me"                          # sin token: espera 401
curl -fsS -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $SMOKE_TOKEN" "$BASE/v1/me"  # espera 200
```

Reglas del smoke:
- Usuario de smoke **dedicado**, con permisos mínimos, en datos de prueba; nunca un paciente real.
- Solo lecturas o escrituras idempotentes y reversibles en un tenant de prueba.
- Incluir un caso negativo (401/403) para confirmar que la autorización sigue activa.
- Web SSR: `curl` del HTML de la home y de una ruta pública debe traer contenido renderizado,
  no un shell vacío; después, Playwright smoke serial (`e2e-playwright`).
- Tiempo total < 2 minutos; si necesita más, no es smoke.

## 4. Criterio de rollback inmediato

Rollback **sin discusión** si en los primeros minutos:
- health en rojo o contenedor reiniciando;
- versión distinta a la esperada;
- cualquier flujo crítico devuelve 5xx;
- tasa de error o p95 sube de forma clara respecto a antes;
- logs con errores repetidos que no existían.

Primero rollback, después diagnóstico (`root-cause-debugging`). Si el release incluyó un cambio
de esquema no compatible hacia atrás, el rollback de la app NO alcanza: seguí el plan de
`release-and-rollback` y avisá antes de tocar la base.

## 5. Automatización en CI

Job separado que corre después del webhook de deploy: espera el estado del deployment por API
(o `gh run`/polling con timeout), luego ejecuta el guion. Falla el job si falla cualquier
chequeo, y notifica al canal de deploys. Ver `github-actions-ci`, `coolify-operations`.

## 6. Anti-patrones

- "Deployment successful" en el panel como única evidencia.
- Verificar en `localhost` o en staging y anunciar producción.
- Smoke con usuario admin real o sobre datos de pacientes.
- Mirar solo la home; no confirmar la versión; no leer logs.
- Dejar el smoke para "cuando alguien entre a probar".

## Evidencia / Definition of Done

Pegá, literal y recortado (ver `evidence-and-verification`):

```text
VEREDICTO:  PASS | FAIL | BLOCKED
Entorno:    production | staging     Recurso: <nombre>     Fecha/hora: <UTC>
Deploy:     <última línea del log de deployment>
Health:     <comando + body>
Versión:    esperada <sha> · desplegada <sha>
Esquema:    <query + resultado>
Smoke:      <ruta → código> × N (incluye un 401/403 esperado)
Logs:       <"sin errores nuevos" + rango revisado, o las líneas encontradas>
Señales:    <error rate / p95 antes → después>
No cubierto: <qué flujo no se ejercitó y por qué>
```

Sin versión confirmada ni smoke ejecutado, el veredicto máximo es BLOCKED. "Debería estar
bien" es FAIL.

## Checklist

- [ ] Lista de rutas críticas y usuario de smoke definidos en el proyecto.
- [ ] Siete chequeos ejecutados en orden; versión confirmada antes que el resto.
- [ ] Caso negativo de autorización incluido.
- [ ] Logs leídos desde el arranque del contenedor nuevo.
- [ ] Criterio de rollback aplicado sin negociar.
- [ ] Reporte con formato de Evidencia pegado en el carril/PR/canal.
