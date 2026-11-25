---
name: code-review-standard
description: Estándar de la casa para revisar un pull request — rúbrica por dimensión (correctitud, seguridad, tests, claridad, alcance), severidades (bloqueante, mayor, menor, nit), qué bloquea el merge y qué es sugerencia, revisar el diff y no a la persona, límites de tamaño, y checklist del autor y del revisor. Usar al revisar cualquier PR, al preparar un PR para pedir review, al decidir si un comentario debe frenar el merge, o al definir la política de revisión de un repo.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Estándar de revisión de código

Revisar es un gate de calidad, no un ritual. El objetivo es que entre a la rama solo código
correcto, seguro y mantenible — y que el autor aprenda algo, no que se sienta juzgado. Se revisa
el **diff**, nunca a la persona.

## 1. Antes de pedir review (autor)

Un PR listo para revisar cumple `github-pull-requests`:
- Chico y de un solo propósito (ver §5). Si mezcla refactor y feature, partilo (`refactoring-safely`).
- Descripción con qué / por qué / cómo probar / evidencia / riesgo.
- CI en verde: format, lint, typecheck, tests. No se revisa un PR rojo.
- Auto-revisado: el autor leyó su propio diff completo antes de asignarlo.

No hagas perder el tiempo del revisor con cosas que la máquina detecta sola.

## 2. Rúbrica — las dimensiones, en orden de prioridad

Revisá en este orden; no te pierdas en estilo antes de mirar si funciona.

1. **Correctitud** — ¿hace lo que dice? ¿casos límite, errores, concurrencia, nulos? ¿la lógica
   es correcta o solo parece? ¿los tests prueban el comportamiento o la implementación?
2. **Seguridad** — autorización a nivel de objeto y de función, validación en servidor, PII
   fuera de logs y respuestas, secretos, inputs. Ante la duda, invocá `security-guardrails`.
3. **Tests** — ¿existe test del cambio? ¿cubre el camino feliz y al menos un error/edge? ¿falla
   si rompés el código a propósito? Sin test de lo nuevo, es bloqueante salvo excepción declarada.
4. **Claridad y mantenibilidad** — nombres, funciones cortas, sin duplicación, sigue el patrón
   vecino (`clean-code`, `native-code-patterns`). ¿lo entenderá quien lo lea en seis meses?
5. **Alcance** — ¿el diff está dentro de lo que el PR dice hacer? Refactors o renombres colados
   son ruido: pedí separarlos (`scope-discipline`).

## 3. Severidades — etiquetá cada comentario

Prefijá cada comentario con su severidad para que el autor sepa qué frena y qué no:

| Severidad | Significado | ¿Bloquea merge? |
|---|---|---|
| **[bloqueante]** | Bug, agujero de seguridad, falta test crítico, rompe contrato | Sí |
| **[mayor]** | Problema real de diseño/mantenibilidad que conviene arreglar ahora | Sí, salvo acuerdo explícito de diferirlo con ticket |
| **[menor]** | Mejora recomendable, no urgente | No |
| **[nit]** | Preferencia de estilo, opinable | No — el autor decide |

Regla: si no marcaste severidad, es [nit]. No dejes que un [nit] frene un merge.

## 4. Qué bloquea vs qué es sugerencia

- **Bloquea**: correctitud rota, seguridad, falta de test de lo nuevo, ruptura de contrato de API,
  cambio fuera de alcance sin justificar.
- **No bloquea**: gustos de estilo (los resuelve el linter/formatter, no el revisor), micro
  optimizaciones sin dato de que importen, reescrituras "como lo haría yo".
- Si vas a bloquear, decí **por qué** y **qué destrabaría** el comentario. Un bloqueo sin salida
  clara es una pared, no una revisión.

## 5. Tamaño y forma

- PR grande = revisión mala. Apuntá a diffs revisables de una sentada; partí lo grande en PRs
  apilados (`github-pull-requests`). Un PR de 800 líneas recibe "LGTM" sin leer: eso no es revisar.
- Los cambios generados/masivos (lockfiles, migraciones generadas, formateo) van en commits o PRs
  separados y se declaran, para que el revisor sepa qué mirar y qué escanear.

## 6. Tono

- Comentá el código, no a la persona: "esta función maneja mal el caso vacío", no "no pensaste el caso vacío".
- Preguntá cuando no entendés en vez de asumir error: "¿qué pasa si `items` viene vacío acá?".
- Elogiá lo que está bien; una revisión no es solo una lista de defectos.
- El autor: no te defiendas del feedback, respondé cada comentario (arreglado / discrepo porque X /
  lo difiero con ticket). No resuelvas una conversación sin responderla.

## Anti-patrones

- Aprobar sin leer porque el PR es grande o el autor es senior.
- Ahogar en [nits] un PR que tiene un bug de correctitud sin ver.
- Rebotar por estilo lo que el formatter ya normaliza.
- Bloquear con "no me gusta" sin alternativa concreta.
- Revisar solo el archivo cambiado sin mirar a quién afecta (usos, contrato, tenant).

## Checklist del revisor

- [ ] Leí el diff completo, no solo los archivos que esperaba.
- [ ] Correctitud: casos límite, errores, concurrencia, nulos.
- [ ] Seguridad: autz por objeto y función, validación servidor, PII fuera de logs/respuesta.
- [ ] Hay test de lo nuevo y falla si rompo el código.
- [ ] Claridad: nombres, duplicación, sigue el patrón vecino.
- [ ] El diff está dentro del alcance declarado.
- [ ] Cada comentario tiene severidad; los bloqueos dicen cómo destrabarse.

## Checklist del autor

- [ ] PR chico, un propósito, descripción completa con evidencia.
- [ ] CI verde antes de asignar; me auto-revisé el diff.
- [ ] Respondí cada comentario; no cerré conversaciones sin responder.

## Evidencia / DoD

Un PR está listo para mergear cuando: CI en verde (pegá el estado de checks), cero comentarios
[bloqueante]/[mayor] abiertos (o diferidos con ticket enlazado), y al menos una aprobación de
alguien que no es el autor. Registralo en el PR, no de palabra. Ver `github-pull-requests` para el
mecanismo y `github-branch-protection-rulesets` para forzarlo.
