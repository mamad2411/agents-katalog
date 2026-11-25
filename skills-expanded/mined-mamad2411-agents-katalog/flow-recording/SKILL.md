---
name: flow-recording
description: Anatomia y metodologia para registrar y re-ejecutar flujos de negocio en dev-team - una carpeta por flujo (flujos/{dominio}/{flujo}/) con un coordinador delgado (FLUJO.md), referencias sin secretos (usuarios por paso, datos, SQL de verificacion), runbook con pasos numerados (rol, acciones, resultado esperado con endpoint+codigo, mensaje de UI y estado de BD), opcional steps.yaml para re-ejecucion, precondiciones y switches, puntos de parada obligatorios ante escrituras y cambios de parametros, cambios de BD guardados con rollback, verificacion final y evidencia numerada. Cargala al crear, grabar o ejecutar un flujo de negocio paso a paso.
---

# Registrar y re-ejecutar flujos de negocio — metodologia (dev-team)

Un "flujo" es un proceso de negocio de punta a punta que el equipo quiere poder REPRODUCIR de
forma ordenada y con evidencia: crear una operacion, aprobar y desembolsar, dar de alta un
cliente, un proceso de cierre. En vez de que viva en la cabeza de una persona, se registra en
una carpeta versionable, con pasos exactos, verificaciones y puntos de control. Despues se
puede re-ejecutar (con las mismas garantias) o consultar como runbook.

Patron: un **coordinador delgado** que no ejecuta, sino que delega a los agentes del equipo y
consolida; todo lo especifico del flujo vive en archivos aparte. Esto lo hace generico: cualquier
dominio (factoring, confirming, cobranza, ...) usa la misma estructura.

## Donde viven los flujos
```
.coordination/flows/{dominio}/{flujo}/          # ej. factoring/creacion-operacion/
├── FLUJO.md            # coordinador: argumentos, precondiciones, fases, puntos de parada, seguridad
├── referencias/
│   ├── datos.md        # usuarios por paso (sin secretos), datos de prueba, como distinguir variantes/modos
│   └── verificacion.md # SQL de solo lectura / cambios guardados / estado posterior — cada query con "-- Esperado:"
├── runbook.md          # (o runbook-{variante}.md) pasos numerados de ejecucion
└── steps.yaml          # OPCIONAL: spec re-ejecutable (paso → selector/accion/assert)
```
La evidencia de cada corrida NO va aqui: va a `.coordination/evidence/FLOW-{dominio}-{flujo}-{fecha}/`
(gitignored), como la de QA. Los flujos SI se versionan (son conocimiento del equipo); la evidencia no.

## FLUJO.md — el coordinador (estructura fija)
```markdown
---
name: {dominio}-{flujo}
descripcion: {que hace el flujo, en una linea de negocio}
argument-hint: "variante={a|b} [monto=...] [ambiente=...] [otros=...]"
---
# Flujo: {titulo de negocio}

## Rol
Coordinador. NO ejecuta el flujo: delega a los agentes del equipo (qa-frontend para UI,
qa-backend/dba para SQL), pregunta al usuario en los puntos de parada y consolida.

## Argumentos
| Argumento | Valores | Default | Nota |
|-----------|---------|---------|------|
| variante  | a \| b  | (preguntar) | que camino del flujo |
| ambiente  | ...     | qa      | si falta credencial/runbook para otro, detener y preguntar |

## Precondiciones y switches (los que apliquen)
| Parametro | Donde | Que gobierna | valor esperado por variante |
|-----------|-------|--------------|-----------------------------|
Regla: si un flujo depende de parametros/switches, se VERIFICAN primero (solo lectura) y se
registra el valor INICIAL; se cambian solo con parada obligatoria y se restauran al final.

## Fases
### 0. Confirmar con el usuario (texto plano)
Enunciar riesgos reales (crea datos reales, cambia parametros que afectan a usuarios) y pedir OK.
### 1. Verificar precondiciones (solo lectura) y registrar valores iniciales
### 2. (si aplica) Cambiar parametros: PARADA OBLIGATORIA (cambio guardado por DBA)
### 3. Ejecutar el flujo (delegado) — pasos del runbook, captura por paso
### 4. Puntos de parada — en ambiente productivo, OK escrito del usuario EN EL MOMENTO (en pruebas, sin parada)
### 5. Verificar resultado (solo lectura + UI) contra lo esperado
### 6. Cierre — informe + restaurar parametros a los valores del paso 1 (misma parada del paso 2)

## Errores conocidos (reportar; no re-diagnosticar)
## Seguridad (sin passwords/tokens aqui; se leen de los archivos de acceso por nombre)
## No confirmado (marcar lo que aun no se verifico en el ambiente real)
```

## runbook.md — pasos numerados (formato)
Cada paso nombra el rol/usuario, las acciones exactas y el RESULTADO ESPERADO verificable:
```markdown
### Paso 3 (o "Estacion 3"): {rol} ({usuario})
**Login:** {como entrar, con que cuenta — la credencial se lee del archivo de acceso, no se escribe aqui}
1. Menu {Modulo → Pantalla}.
2. {accion: llenar campo, presionar boton...}
3. Grabar.
**Resultado esperado:**
- {VERBO} {endpoint} → **200** (o el codigo correcto)
- Mensaje en pantalla: "{texto exacto}"
- Estado de BD: {tabla/objeto} queda en {estado}
```
Cierra el runbook con: una tabla de conteos antes/despues (`Objeto | Antes | Despues`), una
tabla de tiempos/gotchas (`Momento | Accion | Tiempo tipico | Notas`), y las fuentes.

## referencias/verificacion.md — SQL con esperado
Tres bloques, cada query con su comentario `-- Esperado:`:
1. **Solo lectura** (estado antes/durante) — SELECTs.
2. **Cambio guardado** (lo ejecuta el DBA, no el flujo): preflight SELECT, before-image, UPDATE
   por clave primaria guardado sobre el valor previo, dry-run con rollback, `@ROWCOUNT=1`, conteo.
3. **Estado posterior** (tras la accion clave) y **objetos que deben existir**.
Placeholders para nombres que cambian entre ambientes; nunca hosts/credenciales reales en el archivo.

## steps.yaml — opcional, para re-ejecucion asistida
Cuando el flujo se estabiliza, se puede describir de forma re-ejecutable (el `grabar` lo genera
capturando locators con `browser_generate_locator`):
```yaml
flujo: {dominio}-{flujo}
variante: a
pasos:
  - id: "03"
    actor: "{rol}"
    accion: "click"        # navigate|fill|click|select|verify|sql
    objetivo: "getByRole('button', { name: 'Grabar' })"
    espera: "status 200 en {endpoint}"
    evidencia: "03-{rol}-grabar-200.png"
  - id: "04"
    accion: "verify"
    objetivo: "browser_verify_text_visible('La operacion se realizo con exito')"
```
El `steps.yaml` es una AYUDA, no reemplaza el criterio: un paso que falla se detiene y se reporta,
nunca se reintenta a ciegas.

## Reglas duras de ejecucion (iguales para todo flujo)
- **Un solo browser compartido** (Playwright MCP); captura en CADA paso (`00-`, `01-`...).
- **A la primera falla, detener** (login falla, servicio caido, dato que no existe): capturar el
  primer intento, marcar bloqueante, reportar. Sin reintentos, sin workarounds, sin debug.
  Cada reintento de un flujo que ESCRIBE crea datos reales — por eso no se reintenta a la ligera.
- **Puntos de parada segun el ambiente** (`config.json` → `ambientes`): en un ambiente
  **productivo**, antes de cualquier ESCRITURA sensible (grabar, aprobar, confirmar
  giro/desembolso, elegir banco, cualquier write) se pide OK del usuario EN EL MOMENTO, por texto,
  y ese OK vale solo ahi. En un ambiente de **pruebas** (desarrollo, QA, certificacion, puente,
  demo, o el que el proyecto declare asi) esas acciones de negocio son normales y se ejecutan sin
  parada: el usuario ya pidio correr el flujo. **Siempre** hay parada (en cualquier ambiente) antes
  de cambiar un parametro o escribir en BD, porque eso afecta a otros que usan el mismo ambiente.
- **Cambios de parametros/BD**: los ejecuta el DBA con el patron guardado (§verificacion), nunca
  el flujo por su cuenta; se cambian y se restauran JUNTOS si son varios que deben coincidir.
- **Documentar el estado planeado ANTES** de crear nada (`00-ANTES-*.md`): que datos, con que
  cuentas, en que ambiente.
- **Secretos**: passwords/tokens se leen de los archivos de acceso del proyecto por NOMBRE de
  variable, nunca se escriben en el flujo, la evidencia ni el chat.
- **Ambiente**: preferente de pruebas; si el flujo toca un ambiente productivo, es una decision
  explicita del usuario con sus riesgos enunciados. Un ambiente no declarado se pregunta una vez.

## Evidencia de una corrida (skill `visual-evidence`)
La captura y el analisis siguen la skill `visual-evidence` (traza navegable + video con acciones
y capitulos + capturas ancladas a una verificacion + snapshot de accesibilidad + sidecars de
consola/red + `INDEX.md` de analisis). En `.coordination/evidence/FLOW-{dominio}-{flujo}-{fecha}/`:
- `00-ANTES-datos-planeados.md` — el estado planeado antes de ejecutar
- `NN-{actor}-{accion}.png` — captura por paso, numerada; fallas con prefijo en mayuscula
  (`NN-BLOQUEANTE-*.png`)
- `red-*.txt` / `consola-*.txt` — red y consola del flujo
- `payload-*-request.json` / `-response.json` — payloads relevantes (redactados)
- `informe-flujo.md` — resultado por paso (`Paso | Resultado | Evidencia`), verificaciones,
  y el veredicto global (COMPLETADO / DETENIDO EN PASO N / BLOQUEADO), mas los valores iniciales
  y finales de los parametros tocados (para probar que se restauraron)
