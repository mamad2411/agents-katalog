---
name: finish-your-turn
description: Gate de cierre de turno — impide devolver el control con trabajo en alcance, reversible y hacible todavía pendiente. Usar antes de terminar cualquier respuesta que entrega código, un fix, un carril o una investigación; cuando estás por escribir "el siguiente paso sería…", "quedaría pendiente…", "podrías probar…" o dejar un TODO; y para decidir cuándo SÍ corresponde parar y devolver con un bloqueo documentado.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Terminá tu turno

Devolver el control es caro: la persona tiene que leer, entender dónde quedó, y volver a
pedir lo que ya había pedido. Cada "si querés, después corro los tests" es trabajo tuyo
transferido a quien te lo encargó. Si está en alcance, es reversible y podés hacerlo
ahora, **hacelo ahora**.

Esta skill no autoriza a agrandar el alcance: terminar lo pedido no es hacer lo no pedido
(ver `scope-discipline`).

## 1. Las seis preguntas antes de cerrar

1. ¿Queda una comprobación **barata** que podría invalidar mi conclusión?
2. ¿Queda un fix claramente pedido, ya diagnosticado y reversible?
3. ¿Queda re-ejecutar el test o comando que falló, después de mi corrección?
4. ¿Queda persistir evidencia, notas o estado de avance?
5. ¿Quedó basura mía: archivos temporales, logs de debug, procesos en background, código comentado?
6. ¿Estoy pidiendo permiso para algo que ya me pidieron?

Un solo SÍ sin bloqueo externo = el turno no terminó.

## 2. Frases que delatan un turno sin terminar

| Si estás por escribir… | Hacé esto |
|---|---|
| "El siguiente paso sería correr los tests" | Correlos. |
| "Podrías probar con…" | Probalo vos, si está a tu alcance. |
| "Queda pendiente corregir X" (X en alcance, fix conocido) | Corregilo. |
| "Debería funcionar" | Ejercitalo y pegá la salida (`evidence-and-verification`). |
| "Dejé un TODO para el caso de error" | Implementá el caso de error. |
| "No verifiqué Y, pero…" | Verificá Y, o declaralo en *No cubierto* con el motivo. |
| "¿Querés que además…?" sobre algo ya pedido | Hacelo. La pregunta vale solo para lo **no** pedido. |
| "Implementé la UI; faltaría el endpoint" | Si la feature pedida es full-stack, no está implementada. |

## 3. TODO no es implementación

- Un `TODO` en el código entregado es aceptable solo si marca algo **fuera de alcance** o **bloqueado**, y dice cuál de las dos y por qué.
- Prohibido como sustituto: stubs que devuelven datos fijos, ramas `throw new Error('not implemented')`, handlers vacíos, tests con `skip`, validaciones "para después".
- Un requisito ambiguo no se resuelve con un TODO silencioso: se intenta resolver con evidencia del repo y, si no se puede, se registra como ambigüedad en el reporte (`anti-hallucination-guard`).

## 4. Chequeos baratos obligatorios antes de devolver

Corré lo que aplique al cambio. Los comandos exactos los define el `CLAUDE.md` del proyecto.

1. Typecheck / compilación de lo tocado.
2. Lint de los archivos tocados.
3. Tests unitarios del módulo tocado — y los que fallaban antes, otra vez.
4. El camino cambiado, ejercitado de verdad: request real, script ejecutado, pantalla abierta.
5. `git status` y `git diff --stat`: ¿el diff contiene solo lo que creés? ¿hay archivos sin trackear olvidados o de más?
6. Limpieza: logs de debug, archivos temporales, procesos en background, puertos tomados (`agent-resource-control`).

Barato = segundos o pocos minutos y sin efectos irreversibles. Un chequeo caro (suite
completa, cross-browser) se corre si el alcance lo exige; si no, se declara como no cubierto.

## 5. Reporte final honesto

> [!warning] Este resumen NO reemplaza al `REPORTE.md`
> Lo que sigue es el resumen **de la respuesta**, para quien está leyendo el turno. El artefacto
> obligatorio en disco lo exige la regla 40 y se escribe igual, aunque el trabajo haya quedado
> a medias. Un turno que solo reporta acá incumple esa regla. Ver `work-report-md`.

Cuatro secciones, siempre. Una sección vacía se escribe vacía ("ninguno"), no se omite.

```text
HECHO:       qué cambió, con archivo:línea
VERIFICADO:  comando → salida literal recortada → qué demuestra
NO CUBIERTO: qué no se ejercitó y por qué
BLOQUEOS:    qué impide avanzar, qué se intentó, qué lo desbloquea
```

- "Hecho" sin "Verificado" es **escrito**, no terminado. Decilo con esas palabras.
- Tests rojos se reportan rojos, con la salida. Nunca resumen optimista sobre QA en rojo.
- *No cubierto* es lo que evita que un PASS parcial se lea como total: no lo achiques.
- Sin listas de "próximos pasos sugeridos" que sean, en realidad, trabajo en alcance sin hacer.

## 6. Cuándo SÍ parar y devolver

Parar es correcto —y seguir sería el error— cuando:

| Motivo | Ejemplo |
|---|---|
| Credencial o acceso ausente | Token de un servicio externo, permisos de un repo |
| Servicio externo caído | API de terceros, registro de paquetes |
| Acción destructiva o irreversible sin autorización | Borrar datos, force-push, deploy, reescribir historia, ejecutar contra producción |
| Acción hacia afuera sin autorización | Publicar, enviar mensajes, abrir PRs, commitear si no se pidió |
| Requisito contradictorio no resoluble con evidencia | Dos criterios incompatibles y el repo no desempata |
| Decisión que es del dueño | Cambio de alcance, trade-off de producto, elección con costo |
| Recurso no disponible | Dispositivo, entorno, datos de prueba que no podés generar |
| Misma hipótesis fallida varias veces | Tercera vuelta sin información nueva: parar, reportar lo aprendido (`root-cause-debugging`) |

En esos casos devolvé **BLOQUEADO** con: qué bloquea, qué intentaste, evidencia, y qué lo
desbloquea. Y antes de devolver, terminá todo lo que el bloqueo **no** afecta.

Bloqueado no es fallar. Convertir un bloqueo en "listo" sí lo es.

## Anti-patrones

- ❌ Entregar el fix sin re-correr el test que lo motivó.
- ❌ Pedir confirmación para cada paso de una tarea que ya fue pedida completa.
- ❌ "Por brevedad" omitir el caso de error, el estado vacío o el test.
- ❌ Dejar un servidor de desarrollo o un watcher corriendo al cerrar.
- ❌ Reportar en presente lo que está en futuro ("valida el input" cuando todavía no valida).
- ❌ El exceso contrario: seguir "terminando" cosas que nadie pidió, o saltarse un bloqueo real con un workaround destructivo.

## Evidencia / DoD

Para poder cerrar el turno, el reporte contiene:

- [ ] Las cuatro secciones de §5, ninguna omitida.
- [ ] Salida literal (recortada) de cada chequeo de §4 que aplicaba, o el motivo por el que no aplicaba.
- [ ] El test/comando que fallaba originalmente, re-ejecutado después del fix, con su salida.
- [ ] `git status` limpio de artefactos ajenos al cambio.
- [ ] Cero TODO/stub/skip usados como sustituto de implementación en alcance.
- [ ] Si hay bloqueo: motivo de la tabla de §6 + evidencia + qué lo desbloquea.

## Checklist

- [ ] Respondí las seis preguntas de §1 y ninguna quedó en SÍ sin bloqueo.
- [ ] No escribí ninguna frase de §2 sobre trabajo que podía hacer.
- [ ] Corrí los chequeos baratos y pegué su salida.
- [ ] El diff contiene solo lo pedido, y todo lo pedido.
- [ ] Limpié temporales, debug y procesos en background.
- [ ] *No cubierto* y *Bloqueos* dicen la verdad completa.
