---
name: qa-orchestration
description: Orquesta QA de punta a punta — plan, diseño, entornos, datos, ejecución, reporte y gate go/no-go — incluyendo el pipeline de CI (estático → unitario → integración → contrato → E2E → performance → seguridad) y un patrón de orquestación multi-agente con roles (planificador, investigador, ejecutor, revisor independiente). Usar al diseñar cómo se prueba un release completo, al armar o depurar un pipeline de CI, o al coordinar varios agentes/personas que hacen QA sobre el mismo cambio.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Orquestación de QA de punta a punta

Esta skill coordina el **proceso**: quién hace qué, en qué orden, con qué entrada y qué salida.
Para decidir qué probar y en qué nivel, ver `qa-strategy`; para el contenido técnico de cada
tipo de prueba, ver `unit-testing` e `integrity-testing`.

## 1. Flujo end-to-end

```
Plan → Diseño de casos → Entornos → Datos → Ejecución → Reporte → Gate go/no-go → Regresión
```

1. **Plan**: alcance del cambio, riesgos (`qa-strategy` §2), niveles de test involucrados,
   quién es dueño de cada nivel, fecha/checkpoint del gate.
2. **Diseño de casos**: casos de aceptación derivados de los criterios, casos borde, casos
   negativos (qué debe fallar y cómo). Cada caso referencia el requisito que verifica.
3. **Entornos**: efímeros y reproducibles (contenedor, no "el servidor de staging de siempre"
   con estado acumulado). Mismo build artefacto que se promueve, nunca una recompilación distinta
   por ambiente.
4. **Datos**: fixtures versionadas, generadas por el propio pipeline, aisladas por run
   (ver `qa-strategy` §6 e `integrity-testing` §5 para dependencias reales vía contenedores).
5. **Ejecución**: pipeline de CI en capas (ver §2), paralelizado donde no hay dependencia de orden.
6. **Reporte**: plantilla fija (ver §4), no prosa libre — facilita comparar runs.
7. **Gate go/no-go**: criterio objetivo y pre-acordado, no una decisión ad hoc post-hoc (ver §3).
8. **Regresión/retest**: todo bug arreglado agrega un caso permanente a la suite del nivel que
   lo debería haber atrapado; el retest confirma el fix Y corre la suite completa, no solo el caso.

## 2. Pipeline de CI en capas

Cada capa corre solo si la anterior pasó (fail-fast), salvo que se declare explícitamente
independiente para paralelizar:

| Orden | Capa | Objetivo | Paraleliza con |
|---|---|---|---|
| 1 | Estático (lint, tipos, formato) | Errores de forma antes de gastar cómputo en tests | — (gate de entrada) |
| 2 | Unitario | Lógica de negocio aislada, feedback en segundos | Sharding por paquete/módulo |
| 3 | Integración | Colaboración con dependencias reales (DB, cola) | Sharding por dominio/módulo |
| 4 | Contrato | Productor/consumidor de una API siguen de acuerdo | Independiente de integración |
| 5 | E2E | Flujos críticos de negocio en entorno real | Sharding por flujo/spec, ejecución en paralelo con locks de datos |
| 6 | Performance | Regresión de latencia/throughput en rutas críticas | Después de E2E (necesita entorno estable) |
| 7 | Seguridad | Escaneo estático + dinámico, revisión de `security-guardrails` | Puede correr en paralelo desde la capa 1 (no bloquea, pero bloquea el gate final) |

- **Sharding**: dividí la suite por módulo o por tiempo histórico de ejecución (no alfabético),
  balanceando shards para que todos terminen en tiempo similar.
- **Fail-fast vs fail-safe**: en PRs, fail-fast (cancelá el resto ante el primer rojo) para dar
  feedback rápido. En el pipeline de release, fail-safe (corré todas las capas igual) para tener
  el cuadro completo antes de decidir el gate.

## 3. Quality gates y checklist de release

- Un gate es una condición binaria y automatizable, nunca "se ve bien": ejemplos válidos —
  "0 tests rojos en capas 1-5", "sin hallazgos críticos/altos de seguridad sin mitigar",
  "presupuesto de performance no excedido en rutas marcadas críticas", "cobertura no bajó
  respecto al baseline" (como piso de alarma, no como objetivo — ver `qa-strategy` §8).
- Checklist mínima antes de dar go a un release:
  - [ ] Todas las capas de CI en verde para el artefacto exacto que se va a desplegar.
  - [ ] Sin flakies sin cuarentena en el run de referencia.
  - [ ] Hallazgos de seguridad críticos/altos resueltos o con mitigación aprobada.
  - [ ] Plan de rollback probado (no solo documentado) para el cambio de mayor riesgo.
  - [ ] Migraciones de datos verificadas con `integrity-testing` (rollback incluido).
  - [ ] Reporte de evidencia (§4) firmado por el revisor independiente.
- Un no-go documenta la causa raíz y la condición exacta para reintentar el gate — no "arreglar
  y reintentar" sin especificar qué cambió.

## 4. Plantilla de reporte de evidencia

```
## Reporte QA — <cambio/release>
Alcance: <qué se probó, qué quedó explícitamente fuera y por qué>
Resultado por capa: estático=✅ unitario=✅ integración=✅ contrato=✅ e2e=✅ perf=✅ seguridad=✅
Evidencia: <link al run de CI, no texto pegado a mano>
Hallazgos abiertos: <lista con severidad/prioridad, ver qa-strategy §4>
Flakies en cuarentena: <lista o "ninguno">
Veredicto: GO / NO-GO — <condición objetiva que lo determina>
```

## 5. Patrón de orquestación multi-agente

Cuando varios agentes hacen QA sobre el mismo cambio, cada rol tiene un contrato de
entrada/salida explícito — nunca un agente "revisa todo" sin límite de responsabilidad:

| Rol | Entrada | Responsabilidad | Salida |
|---|---|---|---|
| **Planificador** | Descripción del cambio + criterios de aceptación | Deriva riesgos (`qa-strategy` §2) y arma el plan de capas a ejecutar | Plan de pruebas con niveles, prioridad y dueño por área |
| **Investigador** | Plan de pruebas + código/diff | Explora el código, identifica casos borde no obvios, dependencias externas, contratos afectados | Lista de casos de prueba concretos, uno por riesgo identificado |
| **Ejecutor** | Casos de prueba | Escribe/corre los tests de cada capa, captura salida literal | Resultado por capa + evidencia cruda (no resumida) |
| **Revisor independiente** | Evidencia cruda del ejecutor | Verifica que la evidencia respalde el veredicto — nunca confía en el resumen del ejecutor sin ver la salida real | Veredicto GO/NO-GO firmado, con hallazgos que el ejecutor pudo pasar por alto |

- El revisor independiente **no es la misma sesión/contexto que el ejecutor**: si el mismo
  agente que corrió los tests también los certifica, se pierde la verificación cruzada — el
  sesgo de confirmación hace que se acepte la propia salida sin escrutinio.
- Cada handoff entre roles pasa un artefacto verificable (plan, lista de casos, salida literal,
  veredicto), nunca una descripción en prosa de "ya lo revisé".
- Si un rol no puede cumplir su contrato (el investigador no encuentra el contrato de la API,
  el ejecutor no puede levantar el entorno), reporta el bloqueo explícitamente — no rellena con
  una suposición para poder avanzar (ver anti-alucinación en evidencia mínima de decisiones).

## Checklist

- [ ] El pipeline tiene las 7 capas o una razón explícita para omitir alguna.
- [ ] Cada quality gate es una condición binaria y automatizable, no una impresión subjetiva.
- [ ] El reporte usa la plantilla fija, con link al run real, no texto narrado a mano.
- [ ] Si hay orquestación multi-agente, el revisor independiente no es el mismo contexto que el ejecutor.
- [ ] Todo bug arreglado agregó un caso de regresión permanente a la suite.

## Evidencia / Definition of Done

- Link al run de CI completo (todas las capas), no captura parcial ni resumen narrado.
- Reporte con la plantilla de §4 completa, veredicto GO/NO-GO con su condición objetiva.
- Si hubo orquestación multi-agente: los cuatro artefactos de handoff (plan, casos, evidencia
  cruda, veredicto firmado), no solo el veredicto final.
