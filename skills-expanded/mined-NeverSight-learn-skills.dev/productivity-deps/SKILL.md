---
name: productivity-deps
description: "Mantenimiento de dependencias. Escanea paquetes outdated en Node.js (npm outdated), Python (pip list --outdated), .NET (dotnet list package --outdated) y Flutter (flutter pub outdated). Clasifica updates por riesgo (patch = seguro, minor = revisar, major = planificar), genera changelog de cada update desde GitHub releases, y sugiere agrupar en PRs separados. Úsala al inicio de cada sprint, el lunes por la mañana, o cuando el usuario diga 'actualizar dependencias', 'dependency check', 'qué paquetes están desactualizados', 'npm outdated'."
---

# Productivity Deps — Mantenimiento de Dependencias

Escanea dependencias outdated en todos los stacks, clasifica por riesgo y sugiere PRs.

---

## Workflow

### Paso 1: Detectar stack(s) del proyecto

Si es monorepo, escanear cada paquete/proyecto por separado:

| Stack | Comando | Formato |
|-------|---------|---------|
| **Node.js** | `npm outdated --json` | JSON |
| **Python** | `uv pip list --outdated --format json` o `pip list --outdated --format json` | JSON |
| **.NET** | `dotnet list package --outdated` | Texto parseable |
| **Flutter** | `flutter pub outdated` | Texto parseable |

### Paso 2: Clasificar por riesgo

| Bump | Riesgo | Acción sugerida |
|------|--------|-----------------|
| **PATCH** (1.2.3 → 1.2.4) | 🟢 Bajo | Auto-merge. Bug fixes, no breaking. |
| **MINOR** (1.2.3 → 1.3.0) | 🟡 Medio | PR separado. Nuevas features, sin breaking. Revisar release notes. |
| **MAJOR** (1.2.3 → 2.0.0) | 🔴 Alto | Planificar. Breaking changes. Revisar migration guide. No mergear sin equipo. |
| **PRE-RELEASE** (1.2.3 → 2.0.0-beta) | ⚪ Info | Solo informativo. No instalar en producción. |
| **Security advisory** | 🔴 Crítico | PR inmediato. Vulnerabilidad conocida. Mergear hoy. |

### Paso 3: Buscar changelogs y release notes

Para cada update MINOR o MAJOR, buscar release notes desde GitHub/GitLab:

```bash
# Obtener releases de GitHub
gh release view --repo owner/package v2.0.0 --json body,name,publishedAt
```

Si `gh` no está disponible, inferir desde el changelog del paquete o el repo.

### Paso 4: Detectar security advisories

```bash
npm audit --json                    # Node.js
uv run pip-audit --format json       # Python
dotnet list package --vulnerable     # .NET
flutter pub outdated --dependency-overview  # Flutter
```

Las vulnerabilidades CRITICAL/HIGH se reportan en la cima, con prioridad absoluta.

### Paso 5: Generar tabla de updates

```markdown
# 📦 Dependency Updates — Sprint 13 (2026-06-23)

## 🔴 Security (merge hoy)

| Paquete | Actual | Nueva | CVE | Acción |
|---------|--------|-------|-----|--------|
| `semver` | 7.5.4 | 7.7.2 | CVE-2026-1234 | `npm install semver@7.7.2` |
| `cryptography` | 43.0.0 | 44.0.1 | CVE-2026-5678 | `uv add cryptography==44.0.1` |

## 🟢 Patch (auto-merge — seguro)

| Paquete | Actual | Nueva |
|---------|--------|-------|
| `typescript` | 7.0.0 | 7.0.2 |
| `eslint` | 9.15.0 | 9.15.1 |
| `ruff` | 0.10.0 | 0.10.2 |

## 🟡 Minor (revisar release notes)

| Paquete | Actual | Nueva | Release Notes |
|---------|--------|-------|---------------|
| `antd` | 5.28.0 | 5.29.2 | [CHANGELOG](https://github.com/ant-design/ant-design/releases/tag/5.29.2) |
| `@tanstack/react-query` | 5.62.0 | 5.65.0 | [CHANGELOG](https://github.com/TanStack/query/releases) |
| `pydantic` | 2.10.0 | 2.11.0 | [CHANGELOG](https://github.com/pydantic/pydantic/releases) |

## 🔴 Major (planificar — breaking changes)

| Paquete | Actual | Nueva | Migration Guide |
|---------|--------|-------|-----------------|
| `drizzle-orm` | 0.36.0 | 1.0.0 | [Migrate to v1](https://orm.drizzle.team/docs/migrate-to-v1) |
| `zod` | 3.23.0 | 4.0.0 | [Migration guide](https://zod.dev/v4) |

---

## 📋 PRs sugeridos

1. **PR #1 — Security + Patch** (merge inmediato)
   - `semver` 7.5.4 → 7.7.2 (critical CVE)
   - `typescript` 7.0.0 → 7.0.2
   - `eslint` 9.15.0 → 9.15.1
   - CI: lint + typecheck + test

2. **PR #2 — Minor updates** (revisar release notes primero)
   - `antd` 5.28.0 → 5.29.2 (nuevo Statistic.Timer, fixes)
   - `@tanstack/react-query` 5.62.0 → 5.65.0

3. **PR #3 — Major: drizzle-orm v1** (planificar con equipo)
   - Breaking: nueva API de columnas
   - Migración requiere cambios en 12 archivos
```

### Paso 6: Ofrecer ejecución

```
¿Quieres que...?
1. Cree un PR con los updates de Security + Patch (seguro, merge inmediato)
2. Cree un PR con los updates Minor (revisar release notes)
3. Solo muestre el reporte, yo actualizo manualmente
```

---

## Manejo de monorepo

Escanear cada `package.json`/`pyproject.toml`/`.csproj` por separado y consolidar:

```markdown
## packages/shared
- `zod` 3.23.0 → 3.23.1 (patch)

## apps/api
- `express` 5.0.0 → 5.0.1 (patch)
- `prisma` 7.0.0 → 7.1.0 (minor)

## apps/web
- `antd` 5.28.0 → 5.29.2 (minor)
- `zod` 3.23.0 → 3.23.1 (patch)  ← mismo update que shared
```

### Consolidar updates compartidos

Si `zod` aparece en 3 `package.json`, crear un solo PR que lo actualice en los 3, no 3 PRs separados.

---

## Lo que NO debe hacer

- No ejecutar `npm update` o `pip install --upgrade` sin preguntar.
- No mergear PR de Major sin que el equipo revise breaking changes.
- No ignorar security advisories con severity CRITICAL.
- No asumir que un Minor no tiene breaking (leer release notes siempre).
- No actualizar deps en archivos generados (`package-lock.json`, `uv.lock`) sin usar el comando apropiado (`npm install`, `uv lock --upgrade-package`).
