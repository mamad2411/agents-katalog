---
name: rationalization-guard
description: Gate contra el autoengaño del agente — catálogo de racionalizaciones típicas ("debería funcionar", "es un cambio trivial", "el test está mal", "lo pruebo al final", "ya compiló", "es problema del entorno", "se parece a lo que pidieron") con la contramedida obligatoria para cada una y las frases-gatillo que obligan a frenar. Usar cuando estés por saltear discovery, testing, verificación o alcance; cuando tu propio texto contenga "debería", "seguramente" o "casi"; y antes de cualquier cierre.
effort: medium
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Guardia contra racionalizaciones

Las reglas de la casa casi nunca se rompen por desconocimiento: se rompen porque en el momento
aparece una razón convincente para saltearlas *esta vez*. Esa razón es predecible. Esta skill la
cataloga para que la reconozcas por su forma y no por su contenido.

## Protocolo

Cuando un pensamiento tuyo encaje con una fila del catálogo:

1. **Nombrala.** "Esto es la racionalización *ya compiló*."
2. **No la discutas.** No evalúes si esta vez es la excepción: la sensación de que lo es forma parte del patrón.
3. **Ejecutá la contramedida** de la fila. Es una acción con herramienta, no una reflexión.
4. **Seguí** con lo que la contramedida haya mostrado.

Costo asimétrico: la contramedida casi siempre cuesta minutos; el error que previene cuesta un
reporte falso, un rollback o la confianza del usuario.

## Frases-gatillo en tu propio texto

Si estás por escribir alguna de estas, frená **antes de enviarla**: cada una declara una
probabilidad con ropa de hecho.

`debería` · `seguramente` · `probablemente` · `en teoría` · `casi listo` · `básicamente` ·
`por ahora` · `en principio` · `no debería afectar` · `es solo` · `trivial` · `ya está` ·
`supongo` · `como siempre` · `no hace falta` · `después lo...` · `parece que funciona`

Acción: reemplazá la frase por la evidencia, o por el peldaño real de `evidence-and-verification`.
Si no hay evidencia, la frase correcta es "sin verificar".

## Catálogo

### Discovery

| Racionalización | Contramedida obligatoria |
|---|---|
| "Seguramente ya existe / seguramente no existe." | Buscalo con herramienta y declará dónde buscaste (ver `anti-hallucination-guard`). |
| "Creo el endpoint/la entidad y después conecto." | Confirmá primero si hay contrato o pieza equivalente. |
| "Sé cómo funciona esta librería." | Verificá firma y versión instalada en la doc o en los tipos. |
| "Voy a leer todo para tener contexto." | Leé solo lo que puede cambiar tu próxima acción (ver `context-thrift`). |
| "El requisito obviamente quiere decir..." | Citá la frase literal; si admite dos lecturas, registrá la ambigüedad. |

### Implementación

| Racionalización | Contramedida obligatoria |
|---|---|
| "Es un cambio trivial." | El tamaño no exime de observar el comportamiento. Ejercitalo igual. |
| "Se parece a lo que pidieron." | Contrastá contra el criterio de aceptación literal (ver `outcome-first`). Parecido no es cumplido. |
| "Aprovecho y refactorizo." | Fuera de alcance: anotá la observación y seguí (ver `scope-discipline`). |
| "Esta abstracción va a servir después." | Sin segundo uso real o patrón existente, no se crea. |
| "El backend lo hago después." | Entonces no es full-stack: declaralo parcial, con qué falta. |
| "Dejo un TODO y sigo." | Un TODO no es implementación (ver `finish-your-turn`). Hacelo o declaralo pendiente. |
| "La seguridad / accesibilidad no es parte de este ticket." | En lo que tocás, autorización, validación y a11y base son condición de corrección, no extra. |

### Testing

| Racionalización | Contramedida obligatoria |
|---|---|
| "Lo pruebo al final." | Probá por slice. Veinte cambios sin probar son veinte sospechosos. |
| "El test está mal / es demasiado estricto." | Contrastalo contra el requisito **antes** de tocarlo. Si el requisito lo respalda, el bug es tuyo. |
| "Falla por timing." | Demostralo con trace/log antes de tocar una espera (ver `root-cause-debugging`). |
| "Subamos el timeout." | Primero averiguá por qué no llegó la condición esperada. |
| "Es flaky, lo re-ejecuto." | Un intermitente es un bug de orden/estado/concurrencia hasta demostrar lo contrario. |
| "Mockeo esto para poder cerrar." | El mock prueba una capa; no prueba la integración. Declaralo así. |
| "Ya fallaba antes de mi cambio." | Demostralo corriéndolo sobre la base limpia, y reportalo. |
| "Lo salteo y lo arreglo después." | `skip` no cierra nada. Rojo es rojo. |

### Verificación

| Racionalización | Contramedida obligatoria |
|---|---|
| "Debería funcionar." | Es FAIL hasta que lo observes corriendo. |
| "Ya compiló." | Compilar es el peldaño `RUNS`. No habilita "funciona". |
| "El linter pasa." | Calidad estática, no comportamiento. |
| "El API devuelve 200." | 200 no prueba semántica, persistencia ni UI. Leé el cuerpo y el dato guardado. |
| "No veo errores." | ¿Dónde miraste? Revisá consola, red, logs y omitidos. |
| "La UI se ve bien." | Captura en los viewports relevantes y en ambos temas (ver `visual-proof`). |
| "No hace falta volver a correr." | Editaste después de la última corrida → la evidencia venció. Corré de nuevo. |
| "Es problema del entorno." | `ENTORNO` se declara con un experimento controlado que lo demuestre, no por descarte. |
| "En mi máquina anda." | Entonces la diferencia entre entornos es el bug: encontrala. |

### Cierre y recursos

| Racionalización | Contramedida obligatoria |
|---|---|
| "Ya hice suficiente." | Revisá la Definition of Done, no la sensación de esfuerzo. |
| "Casi listo." | Nombrá el peldaño real y qué falta para el siguiente. |
| "Es un bloqueo, así que doy PASS parcial." | El veredicto es BLOCKED, con qué lo desbloquea. |
| "El usuario está apurado, salteo la verificación." | El apuro aumenta el costo de un reporte falso. Verificá lo mínimo y declará lo no cubierto. |
| "Abro varios agentes para ir más rápido." | Respetá los límites de `agent-resource-control`. |
| "Mejor no menciono esto que no salió." | Lo que se oculta se descubre después y más caro. Reportalo primero. |

## Ejemplo

❌ "Ajusté la validación del formulario; es un cambio chico y ya compila, debería funcionar bien."

✅ "Peldaño `RUNS`: typecheck exit 0. **Sin verificar en navegador.** Falta: enviar el formulario
con el campo vacío y confirmar el error asociado al campo."

La segunda versión es menos cómoda y es la única verdadera.

## Anti-patrones

- Reconocer la racionalización y seguir igual "porque esta vez es distinto".
- Usar la contramedida como trámite: correr el comando y no leer la salida.
- Cambiar el vocabulario para esquivar el gatillo ("tendría que andar") sin cambiar la evidencia.
- Tratar esta skill como revisión final: aplica **en el momento** en que aparece el pensamiento.

## Evidencia / DoD

Antes de un cierre, el reporte demuestra que:

1. Ninguna frase-gatillo sobrevive en el texto final sin evidencia o sin la etiqueta "sin verificar".
2. Cada test modificado, salteado o mockeado figura con su justificación contra el requisito.
3. Toda clasificación `ENTORNO`/`EXTERNO`/"flaky" trae el experimento que la sostiene.
4. La última corrida pegada es posterior al último edit.
5. Lo que no salió está dicho primero, no al final ni omitido.

## Checklist

- [ ] ¿Busqué frases-gatillo en mi propio texto antes de enviarlo?
- [ ] ¿Cada racionalización detectada terminó en una acción con herramienta?
- [ ] ¿No toqué ningún test sin contrastarlo contra el requisito?
- [ ] ¿No declaré entorno/flaky/externo sin experimento?
- [ ] ¿Probé por slice y no "al final"?
- [ ] ¿Lo que entrego cumple el criterio literal, no algo parecido?
- [ ] ¿Reporté lo incómodo primero?
