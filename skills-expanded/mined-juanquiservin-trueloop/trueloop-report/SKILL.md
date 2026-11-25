---
name: trueloop-report
description: Produce el handoff final de un proyecto TRUELOOP - qué se construyó, arquitectura, decisiones, pruebas, hallazgos de QA, limitaciones conocidas, seguridad, costos, cómo correrlo y cómo modificarlo. Úsalo cuando el usuario escriba /trueloop-report o pida el resumen, el reporte, el entregable o el cierre del proyecto.
---

# TRUELOOP · Reporte de entrega

El examen final de TRUELOOP no es que el código compile. Es que el humano **siga
entendiendo su propio sistema** después de la automatización.

Un reporte que esconde 300 commits detrás de un "listo" es un fracaso, aunque el
software funcione.

## Fuentes (léelas todas antes de escribir)

`.trueloop/PROJECT.md` · `SPEC.md` · `STATE.json` · `TASKS.md` · `DECISIONS.md` ·
`ASSUMPTIONS.md` · `QA.md` · `ISSUES.md` · `LEARNINGS.md` · `RUN_LOG.md`
más `git log --oneline` y `git diff --stat <base>..HEAD` de la rama del loop.

## Estructura del reporte

```markdown
# <Proyecto> · Entrega TRUELOOP
<fecha> · rama <branch> · último commit verificado <hash>

## 1. Qué se construyó
Dos párrafos en lenguaje llano. Qué hace y para quién.
Sin jerga. Si el usuario no lo entiende, el reporte no sirve.

## 2. Contra el objetivo original
| Lo que pediste (PROJECT.md) | Lo que se entregó | Estado |
|---|---|---|
Esta tabla va primero a propósito. Los loops largos derivan, y esta es la única
sección que lo detecta.

## 3. Arquitectura
Componentes, cómo se hablan, dónde vive cada cosa. Un diagrama ASCII vale más
que tres párrafos.

## 4. Decisiones importantes
Las que un futuro tú va a cuestionar. Qué se decidió, qué se descartó y por qué.
Con fecha.

## 5. Archivos y componentes
Agrupados por área, no una lista plana de 200 rutas.

## 6. Verificación
Qué se probó, con qué comando, qué salió.
| Criterio | Verificación | Resultado |

## 7. Hallazgos de QA
Los que se cerraron y **los que siguen abiertos**. No escondas los abiertos.

## 8. Limitaciones conocidas
Lo que NO hace, lo que hace a medias, lo que solo funciona bajo cierto supuesto.
Esta sección es la que hace confiable todo el reporte.

## 9. Seguridad
Superficie de ataque, qué se validó, qué falta, dónde viven los secretos.

## 10. Costo e infraestructura
Qué cuesta correrlo. Qué escala con uso. Qué se contrató.
Y aparte: qué costó ESTE loop (iteraciones y gasto de STATE.json).

## 11. Cómo se corre
Comandos exactos desde un clon limpio. Probados, no supuestos.

## 12. Cómo se modifica
Dónde tocar para los tres cambios más probables.

## 13. Siguiente acción sugerida
UNA cosa. La que más mueve la aguja.
```

## Reglas de escritura

- **Los abiertos van visibles.** Un reporte que solo cuenta lo bueno no es un reporte,
  es marketing interno.
- **Nada de "se implementó exitosamente".** Di qué se implementó y qué comando lo prueba.
- **Un supuesto sin validar es una limitación conocida.** Trátalo como tal.
- **Si el loop terminó en STALLED o BLOCKED**, la sección 1 empieza diciendo eso, no
  la escondas hasta la 8.
- Sin adjetivos de venta. El humano ya sabe que trabajó; quiere saber qué tiene.

## Entrega

1. Escribe `.trueloop/REPORT.md` en el proyecto.
2. Muestra en el chat las secciones 1, 2, 8 y 13 - lo demás lo lee en el archivo.
3. Si hay lecciones generalizables en `LEARNINGS.md` (que aplicarían a otros proyectos,
   no solo a este), ofrece promoverlas al skill `trueloop`.
   **Solo las generalizables.** Un skill que engorda con detalles de cada proyecto deja
   de servir para todos.
