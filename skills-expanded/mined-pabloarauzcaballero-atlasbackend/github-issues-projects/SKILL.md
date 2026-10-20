---
name: github-issues-projects
description: Gestión del trabajo en GitHub con Issues y Projects — issue forms en YAML, labels como taxonomía, milestones, sub-issues, campos y vistas de Projects, automatizaciones integradas, triage y la cadena de trazabilidad carril ↔ issue ↔ PR ↔ evidencia. Usar al crear plantillas de issues, al definir o limpiar labels, al armar el tablero de un equipo o de un carril, al hacer triage del backlog, o al partir un carril grande en issues rastreables entre varios repos.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Issues y Projects

El issue es la unidad de **intención** (qué y por qué); el PR, la de **cambio**; la evidencia,
la de **prueba**. Si no se puede ir del requisito al commit y del commit a la prueba, el
trabajo no es auditable. Cómo se redacta un bug: `bug-reporting-standard`. Cómo se define un
carril: `lane-authoring`.

## 1. Cadena de trazabilidad

```text
Carril (lane)  →  Issue padre  →  Sub-issues (por repo / por slice)  →  PR(s)  →  Evidencia
  REQ-<n>          "epic"           uno por cambio mergeable             Closes #   reporte + CI
```

1. Cada carril tiene **un issue padre** con sus criterios de aceptación numerados.
2. Cada slice mergeable es un **sub-issue**, en el repo donde vive el cambio.
3. Cada PR cierra exactamente los sub-issues que completa (`github-pull-requests` §5).
4. La evidencia de cierre se enlaza en el issue padre antes de cerrarlo
   (`evidence-and-verification`). Cerrar sin evidencia = reabrir después.

## 2. Issue forms

Viven en `.github/ISSUE_TEMPLATE/*.yml`. Claves de primer nivel: obligatorias `name`
(único entre plantillas), `description`, `body`; opcionales `title`, `labels`, `assignees`,
`projects`, `type`.

```yaml
name: Bug
description: Algo no funciona como debería
title: "[bug]: "
labels: ["tipo:bug", "estado:triage"]
body:
  - type: markdown
    attributes:
      value: "No pegues datos reales de pacientes ni credenciales."
  - type: textarea
    id: repro
    attributes:
      label: Pasos para reproducir
      placeholder: "1. …  2. …"
    validations:
      required: true
  - type: input
    id: version
    attributes:
      label: Versión / commit
  - type: dropdown
    id: severidad
    attributes:
      label: Severidad
      options: [Crítica, Alta, Media, Baja]
    validations:
      required: true
  - type: checkboxes
    id: checks
    attributes:
      label: Antes de enviar
      options:
        - label: Busqué duplicados
          required: true
```

- Tipos de elemento: `markdown`, `input`, `textarea` (admite `render` y `value`), `dropdown`
  (`options`, `default`), `checkboxes`, `upload`. Cada uno con `attributes` y `validations`.
- `config.yml` en la misma carpeta controla el selector de plantillas (issues en blanco,
  enlaces de contacto): claves exactas, verificar en la doc oficial.
- Si un repo define sus propias plantillas, **no** hereda ninguna de las de la organización
  (`github-repo-standards`).
- Plantillas mínimas de la casa: bug, feature/requisito, tarea técnica, carril.
- Aviso de privacidad arriba de todo form: nunca datos clínicos ni personales reales
  (`data-privacy-sensitive`).

## 3. Labels como taxonomía

Un label sin prefijo es una opinión; con prefijo es una dimensión. Una sola etiqueta por dimensión.

| Dimensión | Ejemplos | Uso |
|---|---|---|
| `tipo:` | bug, feature, tarea, deuda, docs | Qué es |
| `area:` | agenda, clinico, contable, auth, infra | Dónde pega; alinea con CODEOWNERS |
| `prioridad:` | p0, p1, p2, p3 | Cuándo se atiende |
| `severidad:` | critica, alta, media, baja | Cuánto daña (solo bugs) |
| `estado:` | triage, bloqueado, necesita-info | Excepciones al flujo; el flujo normal vive en Projects |
| `riesgo:` | seguridad, datos, breaking | Dispara gates extra |

- **Mismos labels, mismo color, en los 5 repos.** Sincronizalos por script
  (`gh label clone <repo-origen>` o `gh label create` en bucle): `github-cli-automation`.
- Severidad ≠ prioridad (`qa-strategy`): un typo en la home es baja severidad y puede ser p1.
- Labels de categoría alimentan las release notes (`github-releases-versioning`).
- Podá: label sin uso en 6 meses, se borra.

## 4. Milestones, sub-issues y tipos

- **Milestone** = entrega con fecha (release, hito). No lo uses como "carpeta temática": para eso
  están los labels `area:`. Un issue, un milestone.
- **Sub-issues**: parten un issue grande en tareas rastreables; el padre muestra el avance, y
  ese progreso es filtrable y agrupable en Projects. Límites documentados: hasta 100 sub-issues
  por padre y hasta 8 niveles de anidación. Un sub-issue puede vivir en **otro repo**: es el
  mecanismo natural para carriles que cruzan API + web + mobile.
- Usá 2 niveles (carril → slice). Más profundidad es burocracia.
- **Issue types** y **dependencias** entre issues (bloquea / bloqueado por): disponibilidad y
  configuración, verificar en la doc oficial. Si no están disponibles, escribí
  `Bloqueado por org/repo#N` en el cuerpo y usá el label `estado:bloqueado`.

## 5. Projects

Un Project es una vista sobre issues y PRs de **varios repos**: es el tablero del equipo, no del repo.

**Layouts**: tabla (densa, para triage y planificación), tablero (flujo por estado), roadmap
(fechas e iteraciones).

**Campos personalizados**: texto, número, fecha, selección única, iteración. Hay un máximo de
campos por proyecto: pocos y usados.

Campos de la casa:

| Campo | Tipo | Para qué |
|---|---|---|
| Estado | Selección única | Por hacer / En curso / En review / En QA / Hecho |
| Carril | Selección única o texto | Agrupar por lane |
| Iteración | Iteración | Sprint |
| Estimación | Número | Capacidad |
| Evidencia | Texto (URL) | Link al reporte de cierre |

**Automatizaciones integradas** (sin código): asignar estado al agregar o cerrar un item,
**auto-add** de items de un repo que cumplan un filtro, **auto-archive** por criterio.
Para lo demás: API GraphQL o Actions.

**Vistas mínimas**: Triage (`estado:triage`, tabla) · Sprint actual (tablero, filtro por
iteración) · Por carril (tabla agrupada, con progreso de sub-issues) · Bloqueados · Roadmap.

**Insights** para gráficos de flujo y **status updates** para el estado del proyecto: usalos en
vez de un documento aparte que nadie actualiza.

## 6. Triage

Cadencia fija (diaria o por sprint). Para cada issue en `estado:triage`:

1. ¿Duplicado? → cerrar como duplicado, enlazando el original.
2. ¿Reproducible / entendible? No → `estado:necesita-info` + pregunta concreta + fecha límite.
3. Clasificar: `tipo`, `area`, `severidad` (bugs), `prioridad`.
4. ¿Toca seguridad o datos sensibles? → `riesgo:*`, y **no** se discute el detalle en un issue
   público: canal privado (`github-security-features`).
5. Asignar milestone o dejar en backlog explícitamente. "Sin decidir" no es un estado.
6. Sacar `estado:triage`.

Issue sin actividad ni decisión tras N semanas (definilo en el CLAUDE.md del proyecto): se
cierra como "no planificado" con explicación. Un backlog infinito no es un backlog.

## 7. Agentes e issues

- Un agente **puede**: crear issues con la plantilla, comentar hallazgos con evidencia, enlazar
  PRs, proponer labels.
- Un agente **no** cierra issues ajenos, no cambia prioridad ni milestone, no borra ni
  transfiere issues sin confirmación humana.
- Nunca pegues en un issue logs con datos personales, tokens o dumps: recortá y anonimizá.
- Antes de crear, buscá duplicados: `gh issue list --search "<términos>" --state all`.

## Anti-patrones

- Issue "Arreglar agenda" sin criterio de aceptación.
- Labels libres, distintos en cada repo.
- Project usado como lista de deseos sin estados ni dueño.
- PRs sin issue ("era un cambio chiquito").
- Cerrar el issue al mergear aunque falte verificar en el entorno.
- Discutir una vulnerabilidad en un issue público.

## Checklist

- [ ] Issue forms en `.github/ISSUE_TEMPLATE/` con aviso de privacidad.
- [ ] Taxonomía de labels con prefijos, idéntica en todos los repos.
- [ ] Un issue padre por carril; sub-issues por slice, en el repo que corresponde.
- [ ] Cada PR vinculado a su issue; cada cierre con evidencia enlazada.
- [ ] Project con campos mínimos, vistas de triage/sprint/carril/bloqueados.
- [ ] Auto-add y auto-archive configurados.
- [ ] Triage con cadencia y reglas de cierre por inactividad.
- [ ] Permisos de agentes sobre issues acotados y escritos.
