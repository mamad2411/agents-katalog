---
name: git-workflow-multirepo
description: Flujo de git puro para trabajo que cruza varios repos hermanos (API, web, mobile, modelo) — rama nueva antes del primer commit y nunca sobre la rama de integración, el mismo nombre de rama en todos los repos afectados, commits atómicos con Conventional Commits, rebase vs merge y orden de merge por dependencia de contrato. Usar antes del primer commit de un carril, al coordinar cambios que tocan más de un repo, o al decidir cómo integrar una rama sin romper a los demás repos.
---

<!-- ESPEJO GENERADO por AtlasPromptManager/tools/install_skills.py - NO EDITAR A MANO -->
<!-- La fuente es AtlasPromptManager/.claude/skills/. Lo que edites aca se pierde. -->

# Git multi-repo

La empresa trabaja en repos hermanos y un carril suele tocar dos o tres a la vez. Esto es la
mecánica de git; la parte de plataforma (PRs, protección de ramas, disparos cruzados) vive en
`github-pull-requests` y `github-multirepo-coordination`.

## Cuándo aplica

- Antes del primer commit de cualquier carril.
- Cuando un cambio toca más de un repo.
- Al decidir rebase vs merge y en qué orden integrar.

## 1. Rama antes del primer commit — nunca sobre integración

- **Nunca** commitees directo sobre la rama de integración/producción (definí su nombre en el
  CLAUDE.md del proyecto). Creá la rama de trabajo **antes** del primer commit.
- Partí siempre de la integración actualizada: `git switch <integración> && git pull` y recién
  después `git switch -c <rama>`.

## 2. Mismo nombre de rama en todos los repos afectados

- Usá el **mismo nombre de rama** en cada repo que el carril toca (p. ej. `carril-42-bloqueo-agenda`).
  Facilita encontrar las piezas del cambio y automatizar disparos cruzados.
- Declará al abrir el carril qué repos toca (ver `lane-authoring`), así sabés dónde crear ramas.

## 3. Commits atómicos + Conventional Commits

- Un commit = un cambio coherente que deja el repo compilando. Nada de "wip" ni "varios arreglos".
- Formato: `tipo(scope): descripción` — `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`.
  Ejemplo: `feat(agenda): bloqueo de franja horaria`.
- El body explica el porqué cuando no es obvio; referenciá el issue/carril.
- Conventional Commits alimenta el changelog y el versionado — ver `github-releases-versioning`.

```
❌ git commit -m "cambios"
✅ git commit -m "fix(auth): rechazar refresh token ya rotado"
```

## 4. Rebase vs merge

- **Rebase** tu rama de trabajo sobre la integración para mantener historia lineal y resolver
  conflictos de a poco: `git fetch && git rebase origin/<integración>`.
- **No** reescribas historia ya compartida/pusheada que otros usan (evitá `--force` sobre ramas
  compartidas; si hace falta, `--force-with-lease` y avisá).
- La estrategia de integración del PR (squash/merge/rebase) la fija el repo — ver `github-pull-requests`.

## 5. Orden de merge por dependencia de contrato

Cuando un carril cambia un contrato compartido (p. ej. la API expone un campo nuevo que la web
consume), integrá en orden de dependencia y con compatibilidad hacia atrás:

1. Primero el productor del contrato (API/modelo), de forma **retrocompatible**.
2. Después el consumidor (web/mobile).
3. Recién al final remové lo viejo, cuando ya nadie lo usa (expand → migrate → contract).

Esto evita romper un repo mientras el otro todavía no mergeó. El detalle de la ventana de
despliegue está en `github-multirepo-coordination`.

## Anti-patrones

- Commitear sobre la rama de integración.
- Nombres de rama distintos en cada repo para el mismo carril.
- Commits gigantes que mezclan feature, refactor y formateo.
- `git push --force` sobre una rama que otros comparten.
- Mergear el consumidor antes que el productor y romper el build ajeno.

## Checklist

- [ ] Rama creada desde la integración actualizada, antes del primer commit.
- [ ] Mismo nombre de rama en todos los repos del carril.
- [ ] Commits atómicos con Conventional Commits y repo compilando en cada uno.
- [ ] Rama rebaseada sobre la integración; sin `--force` sobre ramas compartidas.
- [ ] Orden de merge por dependencia de contrato, con retrocompatibilidad.
