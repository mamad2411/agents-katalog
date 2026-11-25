---
name: git-branching
description: "Estrategias de branching y versionado. Cubre GitFlow, GitHub Flow, Trunk-Based Development, Conventional Commits, semantic-release, y cuándo usar cada estrategia según el equipo y frecuencia de deploy. Actívala al definir la estrategia de branching del equipo, configurar semantic-release, o migrar entre flujos de trabajo."
disable-model-invocation: true
---

# Git Branching Strategies

Guía de estrategias de branching y versionado semántico (2026).

---

## Tabla de decisión

| Estrategia | Mejor para | Deploy frequency | Complejidad |
|------------|-----------|------------------|-------------|
| **GitHub Flow** | Web apps, equipos CI/CD | Continuous | Baja |
| **Trunk-Based** | Alta madurez, deploys diarios | Horaria/diaria | Media |
| **GitFlow** | Software versionado, releases programadas | Semanal/mensual | Alta |

---

## GitHub Flow (recomendado para la mayoría)

```
main ──────────────────────────────────────────────
  │           │                    │
  └── feature/orders ──┘          └── fix/email ──┘
        PR + squash                    PR + squash
```

```bash
# Flujo
git checkout -b feature/order-creation
# ... commits ...
git push origin feature/order-creation

# Crear PR en GitHub → review → merge squash
# La rama se elimina automáticamente al mergear

# Reglas:
# - main siempre deployable
# - Ramas cortas (<2 días de vida)
# - Squash merge: un commit por feature
# - Feature flags para features incompletas
```

---

## Trunk-Based Development

```
main ───────○──────○──────○────── (releases continuas)
  │ │ │ │ │ │ │ │ │ │ │ │
  └─ small branches (horas, no días)

# Reglas:
# - Ramas de máximo 1 día
# - Todo CI/CD sobre main
# - Feature flags para features largas
# - Commits pequeños y frecuentes
```

---

## GitFlow (legacy, solo versionado tradicional)

```
main    ──○────────────────────○────────── (releases)
           │                    │
develop ───┼──○──○──○──○───────┼──○────── (integración)
           │  │       │         │
feature/   ┘  │       │         │
release/      ┘       │         │
hotfix/               ┘         │
```

⚠️ GitFlow agrega fricción para equipos que deployan frecuentemente. Solo para software con releases programadas (ej: app de escritorio, SDK).

---

## Conventional Commits

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Tipos

| Type | Uso |
|------|-----|
| `feat` | Nueva feature |
| `fix` | Bug fix |
| `docs` | Documentación |
| `style` | Formato (no lógica) |
| `refactor` | Cambio de código sin feature ni fix |
| `perf` | Mejora de rendimiento |
| `test` | Tests |
| `chore` | Tareas de build, CI, deps |
| `ci` | CI/CD changes |
| `build` | Sistema de build |

```bash
feat(orders): add order cancellation endpoint
fix(payments): handle Stripe timeout gracefully
refactor(orders): extract validation to shared module
perf(orders): add covering index for customer queries
chore(deps): bump typescript to 7.0.0
```

### Configurar commitlint

```bash
npm install -D @commitlint/cli @commitlint/config-conventional
```

```javascript
// commitlint.config.js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor', 'perf',
      'test', 'chore', 'ci', 'build', 'revert',
    ]],
    'scope-case': [2, 'always', 'kebab-case'],
  },
};
```

### Husky 9 + commitlint

```bash
npm install -D husky
npx husky init
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
chmod +x .husky/commit-msg
```

---

## Semantic-release

```bash
npm install -D semantic-release @semantic-release/git @semantic-release/changelog
```

```javascript
// release.config.js
export default {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',    // Analiza commits → bump versión
    '@semantic-release/release-notes-generator',  // Genera changelog
    '@semantic-release/changelog',          // Escribe CHANGELOG.md
    '@semantic-release/npm',               // Publica en npm (opcional)
    ['@semantic-release/git', {
      assets: ['package.json', 'CHANGELOG.md'],
      message: 'chore(release): ${nextRelease.version}\n\n${nextRelease.notes}',
    }],
  ],
};
```

```bash
# CI: ejecutar en main después de que pasa CI
npx semantic-release

# Resultado:
# feat commit → bump MINOR (1.2.0 → 1.3.0)
# fix commit  → bump PATCH (1.2.0 → 1.2.1)
# feat! o BREAKING CHANGE → bump MAJOR (1.2.0 → 2.0.0)
```

---

## Naming de ramas

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `feature/` | Nueva funcionalidad | `feature/order-cancellation` |
| `fix/` | Corrección de bug | `fix/duplicate-email` |
| `hotfix/` | Fix urgente en producción | `hotfix/payment-timeout` |
| `refactor/` | Refactor sin feature/fix | `refactor/order-validation` |
| `chore/` | Tareas de mantenimiento | `chore/update-deps` |
| `docs/` | Documentación | `docs/api-reference` |

---

## Checklist branching

- [ ] Estrategia elegida según frecuencia de deploy
- [ ] Conventional commits con commitlint (Husky 9 o config hooks Git 2.54)
- [ ] Semantic-release para versionado automático
- [ ] Nombres de rama consistentes (prefijo tipo/descripcion)
- [ ] Ramas cortas (<2 días en GitHub Flow, <1 día en Trunk-Based)
- [ ] Squash merge en PRs (un commit lógico = un commit en main)
- [ ] Feature flags para features incompletas (no ramas long-lived)
- [ ] main siempre deployable (no romper main)
