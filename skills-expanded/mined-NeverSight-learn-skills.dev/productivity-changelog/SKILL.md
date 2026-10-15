---
name: productivity-changelog
description: Genera CHANGELOG.md a partir de conventional commits en git log. Agrupa cambios por tipo (feat, fix, breaking, chore, docs), infiere versión semántica, y linkea issues/PRs cuando están referenciados en los commits. Úsala antes de un release, al cierre de sprint, o cuando el usuario diga "genera changelog", "release notes", "qué cambió", "changelog desde la última versión".
requires-devkits: auto-detect
---

# Productivity Changelog — Commits a Release Notes

Genera `CHANGELOG.md` desde conventional commits. Respeta [Keep a Changelog](https://keepachangelog.com/) y [Semantic Versioning](https://semver.org/).

---

## Workflow

### Paso 1: Determinar el rango

Preguntar en un solo mensaje si no es obvio:

1. **Desde dónde**: último tag (`git describe --tags --abbrev=0`), fecha, o commit hash
2. **Hasta dónde**: HEAD (default), tag específico, o commit hash
3. **Formato**: ¿Keep a Changelog? ¿Conventional Commits? ¿Custom?

Si el proyecto ya usa `semantic-release` o tiene `CHANGELOG.md`, respetar el formato existente.

### Paso 2: Recolectar commits

```bash
# Commits desde el último tag
git log --oneline --no-merges $(git describe --tags --abbrev=0)..HEAD

# O desde fecha específica
git log --oneline --no-merges --since="2026-06-01" --until="2026-06-23"

# Con cuerpo para extraer breaking changes y references
git log --format="%H %s %b" $(git describe --tags --abbrev=0)..HEAD
```

### Paso 3: Clasificar commits

| Prefijo | Categoría | Ejemplo |
|---------|----------|---------|
| `feat:` / `feat(scope):` | **Added** | `feat(orders): add cancellation endpoint` |
| `fix:` / `fix(scope):` | **Fixed** | `fix(payments): handle Stripe timeout` |
| `BREAKING CHANGE:` o `!:` en tipo | **Changed** (Breaking) | `feat(orders)!: change API response format` |
| `perf:` | **Improved** (Performance) | `perf(orders): add covering index` |
| `docs:` | **Documentation** | `docs(api): update endpoint descriptions` |
| `chore:` / `ci:` / `build:` / `refactor:` / `test:` / `style:` | **Maintenance** | `chore(deps): bump typescript to 7.0` |
| `revert:` | **Reverted** | `revert: feat(orders): add cancellation` |

Commits sin formato conventional → categoría **Other** o agrupar por autor.

### Paso 4: Inferir versión

| Cambios | Bump | Ejemplo |
|---------|------|---------|
| Solo `fix:` | **PATCH** | 1.3.0 → 1.3.1 |
| Al menos un `feat:` | **MINOR** | 1.3.0 → 1.4.0 |
| Al menos un breaking (`!:` o `BREAKING CHANGE`) | **MAJOR** | 1.3.0 → 2.0.0 |

Si el proyecto ya tiene versión en `package.json`, `pyproject.toml`, o `.csproj`, partir de ahí.

### Paso 5: Generar CHANGELOG.md

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.4.0] — 2026-06-23

### Added
- Order cancellation endpoint with email notification (`a1b2c3d`)
- Customer search by partial name match (`e4f5g6h`, closes #1234)

### Changed
- **Breaking:** Cancellation now requires a reason parameter. Update your API calls to include `{ "reason": "string" }`. (`i7j8k9l`)

### Fixed
- Stripe timeout gracefully handled with retry logic (`m0n1o2p`, closes #1289)
- Pagination returning duplicate results on last page (`q3r4s5t`)

### Maintenance
- TypeScript 7.0 (`u6v7w8x`)
- Migrated ESLint config to flat config (`y9z0a1b`)
- Updated CI to use Ubuntu 26.04 runner images (`c2d3e4f`)

---

## [1.3.0] — 2026-06-09
...
```

### Reglas de formato

- **Commits agrupados por tipo**, no por orden cronológico.
- **Cada ítem incluye el short hash** del commit para trazabilidad.
- **Issues/PRs linkeados** si el commit los menciona (`closes #X`, `fixes #X`, `ref #X`).
- **Breaking changes con explicación** de qué cambió y cómo migrar.
- **Sin commits de merge** (`--no-merges`).
- **Sin commits de `chore(release)`** generados por semantic-release (son ruido).

### Paso 6: Manejar CHANGELOG existente

Si ya existe `CHANGELOG.md`:
1. Insertar la nueva versión **debajo del header**, antes de la versión anterior.
2. No duplicar entradas si el rango de commits ya está cubierto.

### Paso 7: Actualizar versión en archivos de proyecto

Preguntar antes de modificar:

```json
// package.json
"version": "1.4.0"

// pyproject.toml
version = "1.4.0"

// .csproj
<Version>1.4.0</Version>
```

---

## Modo "desde cero"

Si el proyecto no tiene `CHANGELOG.md` ni tags:

```bash
# Generar changelog completo desde el primer commit
git log --oneline --no-merges --reverse
```

Organizar por versión inferida o por mes si no hay versiones claras.

---

## Lo que NO debe hacer

- No incluir commits de `chore(release)` o `[skip ci]`.
- No modificar `package.json` sin preguntar.
- No usar `git tag` sin preguntar (el usuario puede tener convenciones de tagging).
- No agrupar features y fixes en la misma categoría.
- No omitir breaking changes — deben ser lo más visible del changelog.
