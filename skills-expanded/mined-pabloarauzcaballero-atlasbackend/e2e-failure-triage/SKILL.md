---
name: e2e-failure-triage
description: Protocolo para clasificar y resolver cada fallo de un test E2E o de integración en una de cinco clases — PRODUCT_BUG, TEST_BUG, ENVIRONMENT, DATA, EXTERNAL — con señales para distinguirlas, acción obligatoria por clase y lista de arreglos prohibidos (skip, timeouts a ciegas, retries, borrar aserciones). Usar apenas un test se pone rojo, cuando un test pasa "a veces", antes de tocar un spec que falla, o cuando alguien propone reintentar hasta que pase.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Triage de fallos E2E

Un test rojo es **información**, no un obstáculo. La pregunta no es "cómo lo pongo verde" sino
"qué me está diciendo". Esta skill decide la clase del fallo; la causa profunda se persigue con
`root-cause-debugging`. Regla de la casa: **no se avanza con QA rojo** — ni al próximo criterio,
ni al próximo slice, ni al cierre.

## 1. Primero: reportar y congelar

1. Reportá el fallo de inmediato (nombre del test, step, esperado vs. obtenido). No lo guardes
   para el final.
2. Reproducilo con el test mínimo: un spec, un navegador, `--workers=1 --retries=0 --max-failures=1`.
3. Juntá la evidencia **antes** de editar nada:

| Evidencia | De dónde |
|---|---|
| Step que falló, esperado/obtenido | Salida del runner |
| Qué había en pantalla | Screenshot + snapshot del DOM en el trace |
| Qué pidió el front y qué respondió la API | Pestaña network del trace |
| Errores de JS | Consola del trace / vigía de `e2e-playwright` |
| Qué pasó en el servidor | Log de la API por correlation id (`backend-observability`) |
| Con qué datos y qué rol | Fixture/factory usada, `storageState` |

Leé el trace (`npx playwright show-trace <zip>`). Diagnosticar desde el mensaje de error sin abrir
el trace es adivinar.

## 2. Clasificar

| Clase | Qué es | Señales típicas |
|---|---|---|
| `PRODUCT_BUG` | El producto no cumple el requisito | Reproducible a mano; la API devuelve error o dato incorrecto; el dato no persiste tras reload; excepción en consola/servidor; falla igual en otro navegador |
| `TEST_BUG` | El test afirma mal o interactúa mal | A mano funciona; el locator matchea otro elemento o ninguno; la aserción compara contra un valor que el requisito no exige; falta un `await`; depende del orden de otros tests |
| `ENVIRONMENT` | El entorno no está en condiciones | Servicio caído, puerto ocupado, build viejo, variable faltante, navegador sin instalar; falla **todo**, no solo este test |
| `DATA` | El estado de datos no es el supuesto | Registro que "siempre existe" y no está; colisión de unicidad por corrida previa sin limpiar; seed desactualizado; fecha real que cruzó un límite |
| `EXTERNAL` | Depende de un tercero fuera de control | Proveedor de mapas/correo/pagos caído o con rate limit; respuesta externa cambió |

Preguntas de descarte, en orden:
1. ¿Falla todo o solo esto? Todo → `ENVIRONMENT`.
2. ¿Se reproduce a mano con los mismos datos y rol? Sí → `PRODUCT_BUG`. No → seguí.
3. ¿Pasa con datos recién creados? Sí → `DATA`.
4. ¿La red del trace muestra un dominio ajeno fallando? → `EXTERNAL`.
5. Lo que queda es `TEST_BUG`, y hay que **demostrarlo**, no asumirlo.

Sesgo a vigilar: clasificar `TEST_BUG` porque es lo más barato de arreglar. Por defecto un test
que antes pasaba y ahora falla tras tu cambio es `PRODUCT_BUG` hasta probar lo contrario
(ver `rationalization-guard`).

## 3. Acción por clase

**PRODUCT_BUG** — corregir ya.
1. No sigas con otro criterio.
2. Causa raíz, no síntoma (`root-cause-debugging`).
3. Fix mínimo dentro del alcance (`scope-discipline`).
4. Si el bug era atrapable más abajo, agregá el test unitario/integración que lo cubre.
5. Re-ejecutá **el mismo** E2E, sin modificarlo. Después la regresión del módulo.

**TEST_BUG** — arreglar el test sin debilitar el requisito.
1. Escribí por qué la aserción o el locator eran incorrectos, citando el requisito.
2. El test corregido tiene que seguir fallando si el producto se rompe: probalo rompiendo el
   producto a propósito (o razoná explícitamente por qué fallaría).
3. Re-ejecutá.

**ENVIRONMENT / DATA** — resolver si está bajo tu control.
1. Arreglá la causa (levantar el servicio, regenerar datos por el camino oficial del proyecto,
   nunca a mano en la base). Ver `test-data-management`, `docker-local-stack`.
2. Si el test dependía de estado compartido, ese es un `TEST_BUG` adicional: hacelo dueño de sus datos.
3. Re-ejecutá. Documentá qué estaba mal.

**EXTERNAL** — documentar, nunca maquillar.
1. Evidencia de que el tercero falla (status, respuesta, hora).
2. El resultado es **BLOCKED**, no PASS. Registrá qué lo desbloquea.
3. Evaluá si ese test debería usar un doble del tercero en la frontera (y dejar el contacto real
   para un smoke aparte).

## 4. Arreglos prohibidos

| Prohibido | Por qué |
|---|---|
| `test.skip` / `fixme` / comentar el test | Esconde el fallo; la cobertura desaparece en silencio |
| Subir timeouts sin causa identificada | Convierte un bug de rendimiento o de espera en lentitud permanente |
| Activar `retries` para que "pase al segundo intento" | Un pass en retry es un flaky no diagnosticado |
| Borrar o aflojar aserciones | El test deja de probar el requisito |
| `waitForTimeout` | Sincroniza por suerte |
| `force: true`, `dispatchEvent` para saltear un overlay | El usuario real tampoco puede |
| Mockear la respuesta que falla | Declara terminado algo que no funciona |
| Re-correr hasta verde y reportar PASS | Falsea la evidencia |

## 5. Intermitentes

- Corré el test N veces en serie (`--repeat-each=<N> --workers=1`) para medir la tasa de fallo.
- Causas a buscar: carrera entre UI y respuesta de red, animación en curso, reloj real, datos
  compartidos, orden de tests, `await` faltante.
- Si no se resuelve en el momento: cuarentena formal con dueño y fecha según
  `regression-suite-management`. Cuarentena ≠ skip silencioso.

## 6. Registro del fallo

```text
TEST:        <archivo> › <nombre>
STEP:        <acción o aserción que falló>
ESPERADO:    <...>      OBTENIDO: <...>
CLASE:       PRODUCT_BUG | TEST_BUG | ENVIRONMENT | DATA | EXTERNAL
CAUSA:       <una frase, con archivo:línea si aplica>
ACCIÓN:      <fix aplicado o bloqueo documentado>
RE-TEST:     <comando> → <resultado literal>
EVIDENCIA:   <ruta del trace / screenshot>
```

Si derivó en un defecto que no se corrige ahora, abrilo con `bug-reporting-standard`.

## Checklist

- [ ] Fallo reportado en el momento, no al cierre.
- [ ] Reproducido aislado, serial, sin retries.
- [ ] Trace abierto y leído antes de editar.
- [ ] Clase asignada con la señal que la justifica.
- [ ] `TEST_BUG` demostrado contra el requisito, no asumido.
- [ ] Ningún arreglo de la lista de prohibidos.
- [ ] Mismo test re-ejecutado en verde + regresión del módulo.
- [ ] `EXTERNAL`/`ENVIRONMENT` sin resolver reportados como BLOCKED, no PASS.

## Evidencia / DoD

Para cerrar un fallo pegá: el registro del §6 completo, la salida literal del runner **antes**
(rojo) y **después** (verde) con el mismo comando, y el diff que lo arregló. Un fallo sin clase
asignada o sin re-test pegado sigue abierto (ver `evidence-and-verification`).
