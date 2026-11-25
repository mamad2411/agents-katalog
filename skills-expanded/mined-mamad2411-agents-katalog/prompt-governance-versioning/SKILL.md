---
name: prompt-governance-versioning
description: Gobernanza del repositorio de prompts/skills de la empresa — versionar una skill, registrar cambios de comportamiento en un changelog, revisar antes de mergear, asignar dueños por área, deprecar sin romper, y no quebrar las skills que otras enlazan. Usar al crear, editar, renombrar, deprecar o borrar una skill; al cambiar una `description`; al mover una skill entre áreas; y antes de publicar cualquier cambio que altere cómo se comporta una skill existente.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Gobernanza y versionado de skills

Este repositorio es el producto de la empresa: su valor es que las skills sean confiables y
predecibles. Un cambio no revisado que rompe el disparo de una skill degrada a todos los
proyectos que la usan. Tratá cada skill como una API pública: tiene contrato, versión y dueño.

## 1. La skill como contrato

- El **contrato** de una skill son tres cosas: su `name` (dirección para enlaces), su
  `description` (cuándo dispara) y el comportamiento que promete su cuerpo.
- Cambiar cualquiera de las tres es un cambio de contrato: pasa por revisión y por `prompt-evals`.
- Corregir un typo o afilar una frase sin alterar el disparo ni el comportamiento no es cambio
  de contrato: igual se commitea con mensaje claro, pero no exige evals completas.

## 2. Versionado (SemVer adaptado a skills)

Cada skill lleva versión en su changelog (no en el frontmatter, para no ensuciar el contrato):

| Cambio | Nivel | Ejemplo |
|---|---|---|
| Rompe disparo o comportamiento esperado | **MAJOR** | cambiar el foco de la `description`, quitar una regla en la que otros confían |
| Agrega capacidad sin romper lo previo | **MINOR** | nueva sección, nuevo caso cubierto, ejemplo nuevo |
| Corrección que no cambia el contrato | **PATCH** | typo, redacción, link roto, dato verificado |

Renombrar una skill es MAJOR y se maneja como deprecación (§5), nunca como edición silenciosa.

## 3. Changelog de comportamiento

Registrá los cambios que alteran comportamiento en `CHANGELOG.md` del repo (o en `references/`
de la skill si preferís por-skill). Una línea por cambio:

```
## 2026-09-19
- solid-principles v1.2.0 (MINOR): agregada sección composición > herencia. @dueño-backend
- e2e-playwright v2.0.0 (MAJOR): description ahora excluye tests de API. Migrar refs. @dueño-qa
```

El changelog existe para responder "¿por qué esta skill cambió de comportamiento y desde
cuándo?" sin leer el historial de git entero. No dupliques ahí el `git log`; registrá el **qué
cambió para el usuario**, no el diff.

## 4. Revisión antes de mergear

Ninguna skill nueva ni editada entra sin:

1. Auto-chequeo de `skill-authoring` (frontmatter, description que dispara, ≤~180 líneas, un trabajo).
2. `prompt-evals`: casos de disparo (activa cuando debe, no cuando no debe) y de no-regresión.
3. Revisión de un segundo par (el dueño del área o un par), no del propio autor.
4. Verificación de que **no rompe enlaces**: si otras skills la enlazan por `name`, el name sigue
   existiendo (§6).

## 5. Deprecación (nunca borrado silencioso)

Una skill que deja de valer no se borra de golpe: rompe los `[[enlaces]]` y la memoria muscular.

1. Marcala deprecada en la primera línea del cuerpo: `> DEPRECADA desde 2026-09-19 — usar \`nueva-skill\`.`
2. Dejá la redirección al menos un ciclo (definí cuántas semanas en el CLAUDE.md del repo).
3. Actualizá toda skill que la enlazaba para que apunte a la nueva.
4. Recién entonces borrá el directorio, en un commit propio que diga qué la reemplaza.

Renombrar = crear la nueva + deprecar la vieja apuntando a ella.

## 6. No romper enlaces entre skills

- Antes de renombrar/borrar una skill, buscá quién la enlaza:
  `grep -rl "nombre-skill" .claude/skills` — y actualizá cada referencia en el mismo cambio.
- Un enlace a una skill que todavía no existe es válido (marca trabajo futuro), pero un enlace a
  una que **existió y se borró** es deuda: no dejes referencias colgadas.

## 7. Dueños por área

Cada área (backend, frontend, QA, seguridad, datos, salud, oficio del repo) tiene un dueño
responsable de su coherencia. El dueño aprueba cambios de contrato de sus skills y evita
duplicación dentro del área. Registrá el mapa área → dueño en el CLAUDE.md del repo o en
`CODEOWNERS` si el repo usa `code-review-standard`.

## 8. Cómo probar un cambio antes de publicarlo

1. Editá en una rama, nunca sobre la de integración (ver `git-workflow-multirepo`).
2. Corré las evals de la skill tocada (`prompt-evals`).
3. Probala en una sesión real: pedí una tarea que **debería** dispararla y otra que **no**, y
   observá si se activa como corresponde.
4. Revisión de par + dueño.
5. Merge con mensaje que cite el nivel de cambio (MAJOR/MINOR/PATCH) y actualizá el changelog.

## Anti-patrones

- Editar la `description` "para que dispare más" sin evals → termina disparando en todo.
- Borrar una skill dejando enlaces colgados en otras.
- Renombrar en silencio confiando en que "nadie la usaba".
- Un changelog que copia el diff en vez de decir qué cambió para el usuario.
- Cambiar comportamiento y versión en el mismo commit que un refactor de forma (ver `refactoring-safely`).

## Checklist

- [ ] Clasifiqué el cambio: MAJOR / MINOR / PATCH.
- [ ] Frontmatter y forma pasan el auto-chequeo de `skill-authoring`.
- [ ] `prompt-evals` corrió: disparo correcto y sin regresión.
- [ ] Revisó un par o el dueño del área, no solo yo.
- [ ] Ningún `name` enlazado quedó roto (`grep` de referencias hecho).
- [ ] Changelog actualizado con el qué-cambió-para-el-usuario y el dueño.
- [ ] Si deprecé/renombré: redirección puesta y referencias migradas.

## Evidencia / DoD

Para dar por publicado un cambio de skill, pegá:
- salida de `prompt-evals` (casos de disparo y regresión) con veredicto;
- salida del `grep` de referencias mostrando que no hay enlaces rotos;
- la línea agregada al changelog;
- quién revisó (par/dueño).
Sin esas cuatro, el cambio queda en `WRITTEN`, no en publicado. Ver `evidence-and-verification`.
