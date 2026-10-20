---
name: flujos-mesa
description: Como la Mesa de Servicios registra y re-ejecuta sus PROPIOS flujos operativos paso a paso - buscar operaciones de un cliente, verificar el estado de una cesion, preparar un reporte, revisar una pantalla en produccion - en carpetas flujos/{dominio}/{flujo}/ con coordinador delgado (FLUJO.md), referencias sin secretos, runbook con pasos numerados (rol, acciones, resultado esperado), steps.yaml opcional, ejecucion por el QA de negocio (UI con Playwright MCP grabando todo) y el DBA de mesa (verificaciones SOLO SELECT), ambientes productivos con autorizacion explicita, puntos de parada obligatorios antes de cualquier accion que escriba, evidencia por corrida y validacion de precondiciones. Cargala al crear, grabar o ejecutar un flujo de la Mesa.
---

# Flujos de la Mesa — registrar y re-ejecutar lo que la Mesa hace a diario

La Mesa repite operaciones: "buscar las operaciones vencidas de un cliente", "verificar en que
estado quedo una cesion", "revisar la bandeja de un perfil en produccion", "preparar el reporte
semanal". En vez de que cada persona lo haga de memoria, se registra UNA vez como flujo y se
re-ejecuta con las mismas garantias: pasos exactos, verificaciones, evidencia y paradas antes
de cualquier accion sensible. Es el mismo patron que el `/flow` del dev-team, adaptado a la
operacion de la Mesa (si el plugin dev-team esta instalado, su skill `flow-recording` aplica
como referencia; esta es la version de la Mesa).

## Donde viven
```
.mesa/flujos/{dominio}/{flujo}/        ej. factoring/buscar-operaciones-cliente/
├── FLUJO.md            coordinador: para que sirve, argumentos, precondiciones, fases, paradas, seguridad
├── referencias/
│   ├── datos.md        perfiles por paso (por NOMBRE de variable, sin secretos), datos de ejemplo, variantes
│   └── verificacion.md SELECTs de solo lectura con "-- Esperado:" (los corre el dba-mesa)
├── runbook.md          pasos numerados: rol, pantalla, acciones, resultado esperado
└── steps.yaml          OPCIONAL: pasos re-ejecutables (selector/accion/verificacion) que graba el prototipador o el qa-negocio
```
La evidencia de cada corrida NO va aqui: va a `.mesa/evidencia/FLUJO-{dominio}-{flujo}-{fecha}/`
(gitignored). Los flujos se versionan (son conocimiento de la Mesa); la evidencia no.

## Dos clases de flujo (y lo que cambia)
| Clase | Ejemplos | Quien ejecuta los pasos | Paradas |
|---|---|---|---|
| **Consulta** (solo mira) | buscar operaciones, verificar estado, exportar un listado, revisar una bandeja | `qa-negocio` en UI (grabando) · `dba-mesa` en SELECT | ninguna obligatoria; se registra ambiente y perfil |
| **Accion** (algo cambia por la pantalla) | aprobar, reasignar, cerrar un caso, cargar un documento | `qa-negocio` en UI | en ambiente de **pruebas** (`.mesa/config.json` → `ambientes`): sin paradas, es una accion de prueba normal; en **produccion**: autorizacion registrada por corrida y parada antes de cada paso que escribe |
El DBA de mesa **nunca** escribe por SQL dentro de un flujo: solo verifica con `SELECT` antes y
despues. Si un flujo necesita un cambio en datos, eso es un paquete de scripts (`/mesa-servicios:sql`)
para que lo ejecute el autorizado, no un paso del flujo.

## Ambientes productivos
La Mesa a veces necesita operar en produccion (buscar, verificar, a veces actuar). Reglas:
- `FLUJO.md` declara `ambiente: produccion` y **que se permite** (solo consulta / acciones listadas).
- Cada corrida en produccion registra en `00-ANTES` quien autorizo, cuando y para que caso.
- Flujos de **consulta** en produccion: sin paradas, con evidencia (asi se demuestra que solo se miro).
- Flujos de **accion** en produccion: parada antes de CADA paso que escribe, OK escrito del
  usuario de mesa en el momento (no vale "ya autorizado para todo"), y un solo intento por paso.
- Cuentas por NOMBRE de variable (`.mesa/accesos.env`); nunca credenciales en el flujo ni en la evidencia.
- Datos personales que aparezcan en pantalla se redactan en las capturas antes de guardar/entregar.

## FLUJO.md (coordinador)
```markdown
---
name: {dominio}-{flujo}
descripcion: {que hace, en negocio}
clase: consulta | accion
ambiente: pruebas | produccion
argument-hint: "cliente=ACME [desde=YYYY-MM-DD] [estado=vencida]"
---
# Flujo: {titulo}
## Argumentos  (tabla: argumento · valores · default · "preguntar si falta")
## Precondiciones  (que debe existir; verificaciones SELECT de referencias/verificacion.md §1)
## Fases
0. Confirmar con el usuario de mesa (en produccion: registrar autorizacion)
1. Verificar precondiciones (solo lectura)
2. Ejecutar pasos del runbook (qa-negocio en UI grabando; paradas antes de cada escritura)
3. Verificar resultado (SELECT §2 + UI)
4. Cierre: informe-flujo.md + evidencia
## Paradas obligatorias  (lista de pasos que escriben)
## Errores conocidos  (sintoma → que hacer: reportar, no re-diagnosticar)
## Seguridad  (sin secretos; cuentas por nombre; ambiente)
## No confirmado  (lo que aun no se verifico en el ambiente real)
```

## runbook.md (pasos)
```markdown
### Paso 1: {rol} ({VAR_USUARIO})
1. Menu {Modulo → Pantalla}.
2. {accion: filtrar por cliente, elegir rango…}
**Resultado esperado:** {lo que se ve: "listado con las operaciones del cliente, columnas …"}
**Escribe algo:** no | si → PARADA (OK del usuario de mesa)
```
Cierra con una tabla de tiempos y trampas (`Momento · Accion · Tiempo tipico · Ojo con…`) y las fuentes.

## Ejecucion (lo que produce una corrida)
`.mesa/evidencia/FLUJO-{dominio}-{flujo}-{fecha}/`: `00-ANTES.md` (argumentos, ambiente, perfil
por nombre, autorizacion si es produccion) · capturas `NN-{paso}.png` resaltadas · traza · video
con capitulos · `NN-consola.txt`/`NN-red.txt` · `INDEX.md` · `informe-flujo.md` (resultado por
paso, verificaciones, veredicto: COMPLETADO / DETENIDO EN PASO N / BLOQUEADO). Misma disciplina
que `evidencia-reproduccion`: un intento por paso, a la primera falla se detiene y reporta, sin
reintentos a ciegas.

## Grabar un flujo (crearlo recorriendolo)
`/mesa-servicios:flujo grabar`: el usuario de mesa recorre el flujo por la UI con el equipo
(Playwright MCP: captura por paso, `browser_generate_locator` para `steps.yaml`,
`browser_network_requests` para el resultado esperado) y el runbook queda escrito con lo real,
no con lo que se cree. En produccion se graba solo la clase consulta, o la clase accion con
paradas y autorizacion.

## Reglas duras
- Flujos versionados en `.mesa/flujos/`; evidencia fuera de git.
- DBA solo `SELECT` dentro de un flujo; cambios en datos van por `/mesa-servicios:sql` al autorizado.
- Produccion: autorizacion registrada por corrida; acciones solo las listadas; parada por escritura.
- Secretos por nombre de variable; datos personales redactados.
- A la primera falla se detiene y reporta; nunca "probar de nuevo a ver".
