---
name: work-report-md
description: Cómo se escribe el REPORTE.md que cierra un trabajo — qué gana el derecho a entrar en COMPLETADO, cómo redactar A MEDIAS con sus cuatro respuestas obligatorias (qué anda, qué no anda, qué falta exactamente, dónde quedó), cómo pegar evidencia recortada sin parafrasear y enmascarando datos sensibles, y por qué "No cubierto" no es lo mismo que "Pendiente". Usar al cerrar cualquier trabajo, al terminar una sesión con algo incompleto, o al retomar trabajo ajeno.
effort: high
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Reporte de trabajo en `.md`

La regla `40-reporte-obligatorio` fija que **ningún trabajo se cierra sin `REPORTE.md` en disco**.
Esta skill enseña a escribirlo para lo único que importa: que alguien que no estuvo pueda retomar
el trabajo sin preguntarte nada. No es un resumen de lo que hiciste, es el **estado verificado del
sistema** más el mapa exacto de lo que quedó sin terminar.

## Cuándo aplica

- Al cerrar el trabajo.
- Al cerrar la sesión aunque falte mucho — el caso más importante y el que más se saltea.
- Al devolver el control por un bloqueo externo.

La evidencia específica de QA (casos, veredictos, capturas por viewport) se redacta con
`qa-evidence-reporting` y se referencia desde acá. Los checkpoints **durante** el trabajo son
`progress-reporting`; esto es el artefacto **al cerrar**.

## 1. La barra de entrada de cada sección

Ubicá cada microtarea del plan en una sola sección. La pregunta que decide es siempre la misma:
**¿corriste el DoD y tenés la salida?**

| Situación | Sección |
|---|---|
| DoD ejecutado, salida pegada, CA cumplido | COMPLETADO |
| Código escrito sin correr el DoD, DoD en rojo, o parte anda y parte no | A MEDIAS |
| No se empezó, está trabado por algo externo, o se decidió no hacerlo | PENDIENTE (`TODO` / `BLOQUEADO` / `DESCARTADO`) |

"Está escrito pero no lo probé" **nunca** es COMPLETADO. Es la trampa más común y la que destruye
la confianza en el reporte entero: basta un ítem falso para que nadie crea en los otros.

## 2. COMPLETADO

Una fila por microtarea, con el comando y su resultado. Si no podés pegar la salida, no va acá.

```markdown
| ID | Qué se logró | Comando | Resultado |
|---|---|---|---|
| H1.S1.M1 | La base rechaza turnos solapados del mismo profesional | inserción solapada manual | PASS — `evidencia/m1-constraint.txt` |
| H1.S2.M1 | El conflicto devuelve 409 `APPOINTMENT_OVERLAP` | test de API del conflicto | PASS — `evidencia/m4-api.txt` |
```

Escribí el "qué se logró" en términos **observables**: "la base rechaza turnos solapados", no
"agregué el constraint".

## 3. A MEDIAS: las cuatro respuestas

La sección que más importa. Falta una de las cuatro y el ítem no está reportado.

❌ Inútil — no permite retomar nada:
```markdown
### H1.S3.M1 — Mostrar el conflicto
Casi listo, falta pulir el front.
```

✅ Accionable — otra persona lo retoma sin preguntar:
```markdown
### H1.S3.M1 — Mapear el conflicto al mensaje de la UI
- Qué anda: el front recibe el 409 y el interceptor lo captura; el test de API
  del backend está en verde (`evidencia/m4-api.txt`).
- Qué no anda: la pantalla muestra el mensaje genérico "Ocurrió un error" en vez
  del texto de conflicto de horario.
- Qué falta exactamente: agregar la entrada `APPOINTMENT_OVERLAP` al mapa de códigos
  del interceptor de errores y su texto; el mapa ya existe y tiene tres entradas.
- Dónde quedó: rama `feature/agenda-conflictos`, compila y typecheck en verde;
  E2E `reserva-conflicto` en rojo únicamente por esta aserción.
```

- **Qué anda** — solo lo demostrado, con su evidencia. Si no lo corriste, no va acá.
- **Qué no anda** — el comportamiento observado, no la causa supuesta; si no la investigaste,
  decilo (ver `root-cause-debugging`).
- **Qué falta exactamente** — pasos nombrables. "Terminarlo", "pulirlo" y "ajustar detalles" no
  son pasos. Si no sabés qué falta, escribí "falta diagnosticar por qué X" y qué intentaste.
- **Dónde quedó** — rama, archivos tocados, y **si compila o no**: eso decide si quien retoma
  puede correr algo o tiene que arreglar primero.

## 4. PENDIENTE

Lo que no se empezó, con su estado. En los bloqueados, qué los destraba y de quién depende — un
bloqueo sin dueño no se resuelve nunca.

```markdown
| ID | Estado | Qué lo destraba |
|---|---|---|
| H2.S1.M1 | TODO | — |
| H2.S2.M1 | BLOQUEADO | La extensión de índices por rango no está habilitada en pruebas; depende de infraestructura |
| H1.S3.M3 | DESCARTADO | Producto confirmó que los turnos contiguos no son conflicto |
```

## 5. Evidencia: recortar sin parafrasear

Recortar está bien. **Reescribir no.** Lo pegado tiene que ser texto que salió de la máquina, no
tu resumen. Importa la línea del veredicto, el conteo, y el error **completo** cuando falla.
❌ "Los tests pasaron correctamente." ✅ `Tests: 12 passed, 12 total`.

**Datos sensibles.** Ninguna salida puede llevar datos reales de pacientes, secretos ni tokens.
Enmascaralos y **declará que enmascaraste**: si no lo aclarás, quien lee no sabe si el sistema no
los emitió o si vos los sacaste. Los archivos completos van en `evidencia/`, referenciados por ruta.

```text
409 APPOINTMENT_OVERLAP profesional=<ID-ENMASCARADO> franja=10:00-10:30
(paciente y documento enmascarados manualmente para este reporte)
```

## 6. "No cubierto" no es "Pendiente"

| | Qué es | Ejemplo |
|---|---|---|
| **Pendiente** | No se hizo | "No se implementó el bloqueo de franjas" |
| **No cubierto** | Se hizo, **no se verificó** | "Se probó con dos escrituras simultáneas, no con diez; no se ejercitó en móvil" |

"No cubierto" declara los límites de tu propia verificación: caminos no ejercitados, dispositivos
no probados, volúmenes no alcanzados. Omitirlo convierte un PASS parcial en PASS total a ojos del
que lee — un overclaim aunque cada frase sea cierta por separado.

## 7. Cuando todo salió mal

Sin maquillaje y sin dramatismo. Si QA está en rojo va en la **primera línea**:

```markdown
# Reporte — Impedir doble reserva de turno
**Estado: no entregable.** El E2E de conflicto está en rojo; la invariante de base funciona
pero el flujo completo todavía deja pasar la segunda reserva desde la UI.
- Avance: 3 / 7 microtareas HECHO (43 %)
```

Un fallo bien reportado vale **más** que un éxito reportado vago: uno se retoma, el otro se audita.

## 8. Escribir para quien no vio la sesión

Nada de "como hablamos" ni "ese archivo". Nombrá los artefactos completos (ruta, rama, ID de
microtarea), sin pronombres sin antecedente. Test rápido: leelo como alguien que se sumó hoy — si
tenés que preguntar algo, falta información.

## 9. Retomar un trabajo ajeno

El orden de lectura de un reporte previo (estado → A MEDIAS → dónde quedó → No cubierto) está en
[references/retomar-trabajo.md](references/retomar-trabajo.md). Si no te alcanza para arrancar,
eso es un defecto del reporte: anotalo.

## Anti-patrones

| Anti-patrón | Por qué falla | Arreglo |
|---|---|---|
| "Casi listo", "falta pulir" | No es accionable | Las cuatro respuestas |
| Escrito pero no probado en COMPLETADO | Overclaim | Va a A MEDIAS |
| Porcentaje inventado | Oculta el estado | `HECHO / total` |
| Borrar lo que falló | Miente por omisión | Se declara con su estado |
| Resumen optimista con QA en rojo | Engaña al que decide | El rojo va primero |
| Salida parafraseada o secciones vacías borradas | No es evidencia / se lee como "no había nada" | Pegar literal; escribir "ninguna" |
| Sin "No cubierto" | PASS parcial leído como total | Declarar los límites |

## Evidencia / DoD

El reporte está terminado cuando podés mostrar todo esto:

- [ ] `REPORTE.md` existe en disco junto al `PLAN.md` — pegá la salida del listado que lo muestra.
- [ ] Toda microtarea del plan está en exactamente una sección y los conteos cuadran:
      `COMPLETADO + A MEDIAS + PENDIENTE == total del plan`.
- [ ] Cada ítem de COMPLETADO tiene comando y salida literal referenciada en `evidencia/`.
- [ ] Cada ítem de A MEDIAS tiene las cuatro respuestas, con "dónde quedó" indicando si compila.
- [ ] El porcentaje coincide con `HECHO / total` calculado, y el peldaño declarado no es más
      fuerte que lo demostrado (ver `evidence-and-verification`).
- [ ] Ninguna salida pegada tiene datos de pacientes, secretos ni tokens; lo enmascarado, declarado.
- [ ] Existen "No cubierto", "Desvíos del plan", "Riesgos residuales" y "Decisiones y
      ambigüedades", con contenido o con "ninguna".

## Checklist

- [ ] Se escribió aunque el trabajo no haya terminado.
- [ ] Si algo está en rojo, se dice en la primera línea.
- [ ] Los bloqueos nombran qué los destraba y de quién dependen; se lee sin contexto de la sesión.
- [ ] El estado coincide con el del `PLAN.md` (ver `milestone-planning`).
- [ ] Antes de cerrar el turno se pasó por `finish-your-turn`.
