---
name: release-and-rollback
description: Estrategia de releases y rollback entre entornos — dev/staging/prod, estrategia de despliegue (recreate, rolling, blue-green, canary), feature flags para separar deploy de release, cambios de esquema y datos compatibles hacia atrás (expand/contract), verificación post-deploy y la mecánica de un rollback inmediato. Usar al planificar cómo sale una versión a producción, al meter un cambio de base junto con código, o al decidir entre rollback y fix-forward.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Releases y rollback

Un release no termina cuando el deploy queda verde: termina cuando verificaste que el flujo real
funciona y sabés cómo volver atrás en un minuto si no. El corte y numerado de versión está en
`github-releases-versioning`; el orden de etapas en `ci-cd-pipeline`; acá, la estrategia de salida
y de vuelta.

## 1. Entornos

| Entorno | Para qué | Datos |
|---|---|---|
| dev | Integración continua, pruebas del equipo | Sintéticos |
| staging | Ensayo del release igual que prod | Sintéticos o anonimizados — nunca datos personales reales (ver `data-privacy-sensitive`) |
| prod | Usuarios reales | Reales; todo cambio pasó por staging |

El mismo artefacto recorre los tres (construir una vez, promover; ver `ci-cd-pipeline`).

## 2. Estrategias de despliegue

| Estrategia | Cómo | Cuándo |
|---|---|---|
| Recreate | Apaga la vieja, levanta la nueva | Hay downtime; solo si se tolera |
| Rolling | Reemplaza instancias de a poco, detrás del healthcheck | Default para servicios sin estado |
| Blue-green | Dos entornos; se conmuta el tráfico de golpe | Rollback = volver a conmutar; necesita doble capacidad |
| Canary | La nueva recibe un % del tráfico, se sube si va bien | Cambios de alto riesgo, con métricas que decidan |

En un rolling, la app **vieja y la nueva conviven** unos segundos: por eso el cambio tiene que
ser compatible hacia atrás (§4).

## 3. Separar deploy de release: feature flags

- **Deploy** = el código está en producción. **Release** = los usuarios lo ven.
- Meté lo nuevo detrás de un **flag apagado**, desplegá, activá cuando quieras (o de a poco).
  Desactivar el flag apaga la feature **sin redesplegar** — el rollback más rápido que existe.
- Limpiá el flag cuando la feature está consolidada; un flag viejo es deuda (ver
  `technical-debt-management`).

## 4. Cambios de esquema y datos — compatibles hacia atrás

Nunca despliegues un cambio de base que rompa a la versión que todavía está corriendo. Patrón
**expand / contract**:

1. **Expand**: agregá lo nuevo sin quitar lo viejo (columna nueva nullable, tabla nueva). La app
   vieja lo ignora; la nueva lo usa.
2. **Migrar**: backfill de datos en background.
3. **Contract**: recién cuando ninguna versión viva usa lo viejo, lo quitás (otro release).

- Un `NOT NULL` sobre una columna nueva, un rename o un drop **en el mismo deploy que el código**
  rompe el rolling. Se parten en dos releases.
- En un modelo dirigido por diagrama, el cambio sale del generador (ver `model-driven-schema`);
  igual aplica la disciplina expand/contract sobre el orden de aplicación.
- Antes de un cambio de datos riesgoso: backup verificado (ver `backup-restore-dr`).

## 5. Verificación post-deploy

No declares el release hecho sin observarlo (ver `evidence-and-verification`):
- Healthcheck/readiness en verde y el **SHA desplegado** visible = el que esperabas.
- Smoke de los flujos críticos contra la URL real.
- Cambios de esquema/datos aplicados; sin errores nuevos en logs/trazas.

El protocolo y la evidencia mínima están en `deployment-verification-smoke`.

## 6. Rollback

- **Definí el criterio ANTES de desplegar**: qué señal (error rate, smoke rojo, flujo crítico
  caído) dispara el rollback, y quién decide.
- **Mecánica**: redeploy del artefacto anterior (por eso los tags son inmutables), conmutar en
  blue-green, o apagar el flag. Que sea **un paso**, ensayado, no una improvisación.
- **Rollback vs fix-forward**: si el rollback es seguro y rápido, revertí y diagnosticá con calma.
  Fix-forward solo si volver atrás es más riesgoso (p. ej. un cambio de datos ya aplicado que no
  es reversible) — razón de más para el expand/contract del §4.
- Un cambio de base **irreversible** ya desplegado no se "rollbackea" con redeploy: por eso se
  evita acoplar drop/rename al deploy del código.

## 7. Comunicación y registro

Antes: qué sale, cuándo, quién despliega, criterio de rollback. Después: qué se desplegó (SHA,
versión), resultado de la verificación, y si hubo rollback, por qué. Un incidente de release se
cierra con post-mortem (ver `incident-response-postmortem`).

## Checklist

- [ ] Estrategia elegida a conciencia; en rolling, el cambio es compatible hacia atrás.
- [ ] Cambios de esquema/datos en expand/contract, con backup verificado antes de lo riesgoso.
- [ ] Lo nuevo detrás de feature flag cuando conviene separar deploy de release.
- [ ] Verificación post-deploy hecha (SHA correcto, smoke verde) — ver `deployment-verification-smoke`.
- [ ] Criterio y mecánica de rollback definidos ANTES y ensayados (un paso).
- [ ] Release comunicado y registrado; incidente → post-mortem.
