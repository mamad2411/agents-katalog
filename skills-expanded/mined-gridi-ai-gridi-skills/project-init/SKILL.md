---
name: project-init
description: >
  Project initialization and configuration skill. Auto-detects tech stack and conventions from existing projects,
  or collects preferences interactively for new projects to generate crew-config.json.
  Must be invoked before the workflow orchestrator's first run.
user-invocable: true
argument-hint: "[project-path]"
---

# Project Init

Analyzes project environment and generates `crew-config.json` before starting the workflow.

## Language Detection

> **The output language for all Crew skills is determined by `crew-config.json → preferences.language`.**
>
> **Auto-detection rule**: If the user invokes a Crew skill with additional text in a specific language,
> that language is automatically set as the preference. No explicit question is needed.
>
> | User input | Detected language |
> |------------|-------------------|
> | `/crew:workflow-orchestrator Build a shopping mall` | `en` |
> | `/crew:workflow-orchestrator 쇼핑몰 만들어줘` | `ko` |
> | `/crew:workflow-orchestrator ECサイトを作って` | `ja` |
> | `/crew:workflow-orchestrator Créer une boutique en ligne` | `fr` |
>
> If no accompanying text is provided (bare `/crew:workflow-orchestrator`), ask the user:
>
> ```
> What language would you like Crew to use for documents and communication?
> - (1) English (default)
> - (2) 한국어
> - (3) 日本語
> - (4) Other (specify)
> ```
>
> The detected or selected language is saved to `crew-config.json → preferences.language`.
> **All subsequent skills read this field and produce outputs in that language.**

## Operation Modes

### Mode A: Existing Project Detection (Auto-analysis)

If source code exists at the project root, analyze automatically.

```
Project root scan
     │
     ├── package.json found? → Node.js ecosystem analysis
     ├── requirements.txt / pyproject.toml? → Python ecosystem analysis
     ├── go.mod? → Go ecosystem analysis
     ├── pom.xml / build.gradle? → Java ecosystem analysis
     └── None found → Mode B (Interactive setup)
```

#### Detection Targets

| Category | Detection Target | Detection Method |
|----------|-----------------|------------------|
| **Framework** | Next.js, NestJS, Express, FastAPI, Django, Spring Boot, Gin, etc. | package.json dependencies, import patterns |
| **Language** | TypeScript, JavaScript, Python, Go, Java | File extensions, tsconfig.json existence |
| **Package Manager** | npm, yarn, pnpm, pip, poetry | Lock file existence |
| **Test Framework** | Jest, Vitest, Mocha, pytest, JUnit | devDependencies, test config files |
| **Linter/Formatter** | ESLint, Prettier, Ruff, Black | Config file existence |
| **Database** | PostgreSQL, MySQL, SQLite, MongoDB | ORM config, env vars, docker-compose |
| **ORM** | Prisma, TypeORM, Sequelize, SQLAlchemy, GORM | Dependencies, config files |
| **CSS** | Tailwind, styled-components, CSS Modules, SCSS | Config files, dependencies |
| **State Management** | Redux, Zustand, Recoil, Pinia | Dependencies |
| **Authentication** | NextAuth, Passport, direct JWT | Dependencies, auth-related files |
| **API Style** | REST, GraphQL | Route patterns, dependencies |
| **Monorepo** | Turborepo, Nx, Lerna | Config files, workspaces |
| **Container** | Docker, docker-compose | Dockerfile existence |
| **CI/CD** | GitHub Actions, GitLab CI | .github/workflows, .gitlab-ci.yml |
| **ID Strategy** | UUID, Auto-increment, ULID, nanoid | Entity/migration analysis |
| **i18n** | next-intl, react-i18next, vue-i18n | Dependencies, translation files |
| **Commit Convention** | Conventional Commits, freeform | commitlint config, recent commit analysis |

#### Analysis Process

```bash
# 1. Framework & language detection
cat package.json 2>/dev/null  # Analyze dependencies
ls tsconfig.json 2>/dev/null  # TypeScript check
cat requirements.txt 2>/dev/null || cat pyproject.toml 2>/dev/null

# 2. Project structure analysis
ls -la src/ app/ pages/ components/ 2>/dev/null  # Directory patterns
find . -name "*.test.*" -o -name "*.spec.*" | head -5  # Test patterns

# 3. Config file scan
ls .eslintrc* eslint.config* .prettierrc* tailwind.config* 2>/dev/null
ls docker-compose* Dockerfile 2>/dev/null
ls .github/workflows/*.yml 2>/dev/null

# 4. DB & ORM detection
cat prisma/schema.prisma 2>/dev/null  # Prisma
grep -r "TypeORM\|createConnection" src/ 2>/dev/null | head -3

# 5. ID strategy detection
grep -r "uuid\|UUID\|randomUUID\|SERIAL\|AUTO_INCREMENT\|autoIncrement" \
  --include="*.ts" --include="*.py" --include="*.java" -l 2>/dev/null | head -5

# 6. i18n detection
cat package.json 2>/dev/null | grep -o '"next-intl"\|"react-i18next"\|"vue-i18n"'
ls locales/ messages/ i18n/ 2>/dev/null

# 7. Commit convention detection
cat commitlint.config* 2>/dev/null
git log --oneline -20 2>/dev/null
```

### Mode B: Interactive Setup (New Project)

If the project is empty or no source code is found, ask the user interactively.

#### Question Flow

```markdown
## 🚀 Crew Project Initialization

No existing code detected in this project. Let's set things up with a few questions.

### 1. Project Type
What kind of project is this?
- (1) Full-stack web application
- (2) Backend API only
- (3) Frontend only
- (4) Monorepo (frontend + backend)

### 2. Backend Framework (if backend included)
- (1) NestJS (TypeScript) — recommended
- (2) Express (TypeScript)
- (3) FastAPI (Python)
- (4) Django (Python)
- (5) Spring Boot (Java)
- (6) Gin (Go)

### 3. Frontend Framework (if frontend included)
- (1) Next.js (React) — recommended
- (2) React + Vite
- (3) Vue 3 + Vite
- (4) Svelte
- (5) Angular

### 4. Database
- (1) PostgreSQL — recommended
- (2) MySQL
- (3) SQLite (dev/prototype)
- (4) MongoDB

### 5. CSS/Styling (if frontend included)
- (1) Tailwind CSS — recommended
- (2) styled-components
- (3) CSS Modules
- (4) SCSS

### 6. ID Strategy
- (1) UUID (application-level generation) — recommended
- (2) Auto-increment (DB-generated)
- (3) ULID
- (4) nanoid

### 7. Internationalization (i18n)
- (1) Enabled (next-intl / react-i18next)
- (2) Disabled

### 8. Package Manager
- (1) npm
- (2) yarn
- (3) pnpm — recommended

> Reply with numbers (e.g., "1, 1, 1, 1, 1, 1, 1, 3")
> Or answer each question individually.
```

#### Quick Presets

If the user types "default", "recommended", or similar, apply the recommended preset:

```json
{
  "projectType": "fullstack",
  "backend": { "framework": "nestjs", "language": "typescript" },
  "frontend": { "framework": "nextjs", "language": "typescript" },
  "database": { "type": "postgresql" },
  "styling": "tailwindcss",
  "idStrategy": "uuid",
  "i18n": true,
  "packageManager": "pnpm"
}
```

## Recommended Defaults

When the user doesn't specify preferences or selects "recommended", apply these defaults:

### Stack
| Component | Default | Why |
|-----------|---------|-----|
| Backend | NestJS (TypeScript) | Mature DI, decorators, excellent TS support |
| Frontend | Next.js (React) | SSR/SSG, App Router, large ecosystem |
| Database | PostgreSQL | ACID, JSON support, widely deployed |
| ORM | Prisma | Type-safe, excellent DX, auto migrations |
| Styling | Tailwind CSS | Utility-first, fast iteration, no CSS-in-JS runtime |
| State | Zustand | Minimal boilerplate, TS-native |
| Package Manager | pnpm | Fast, disk-efficient, strict |
| ID Strategy | UUID | Distributed-safe, no DB dependency |

### Convention Defaults
| Convention | Default | Why |
|-----------|---------|-----|
| Contract Driven Development | **Enabled** | Type-safe API integration, catches contract mismatches at compile time |
| i18n | Enabled | Ready for localization from day one |
| Commit Convention | Conventional Commits | Enables auto-changelog and semantic versioning |
| Branch Strategy | Feature Branch | Clean PR-based workflow |

## Output: crew-config.json

After analysis or interactive setup, generate `crew-config.json` at the project root.

```json
{
  "$schema": "https://raw.githubusercontent.com/gridi-ai/gridi-skills/main/schemas/crew-config.schema.json",
  "version": "1.0.0",
  "preferences": {
    "language": "en"
  },
  "project": {
    "name": "my-project",
    "type": "fullstack",
    "monorepo": false
  },
  "backend": {
    "framework": "nestjs",
    "language": "typescript",
    "orm": "prisma",
    "testFramework": "jest",
    "apiStyle": "rest"
  },
  "frontend": {
    "framework": "nextjs",
    "language": "typescript",
    "styling": "tailwindcss",
    "stateManagement": "zustand",
    "testFramework": "vitest"
  },
  "database": {
    "type": "postgresql",
    "orm": "prisma"
  },
  "conventions": {
    "idStrategy": "uuid",
    "i18n": true,
    "commitConvention": "conventional",
    "contractDriven": true,
    "branchStrategy": "feature-branch",
    "cssNaming": "tailwind-utility"
  },
  "tools": {
    "packageManager": "pnpm",
    "linter": "eslint",
    "formatter": "prettier",
    "containerization": "docker-compose",
    "ci": "github-actions"
  },
  "integrations": {
    "figma": false,
    "playwright": true
  },
  "detectedAt": "2026-03-24T00:00:00Z",
  "detectionMode": "auto"
}
```

## Contract Driven Development (Default)

When `conventions.contractDriven` is `true` (the default), all skills follow this pattern:

1. **be-spec** writes the OpenAPI spec first
2. **be-main** generates backend types from the spec and implements to satisfy the contract
3. **fe-main** generates API client from the spec — no manual fetch/axios calls

This ensures type-safe integration between backend and frontend.

To disable: set `conventions.contractDriven: false` in crew-config.json.

See: `be-spec/references/contract-driven-development.md` for details.

## How Skills Use crew-config.json

All skills read `crew-config.json` and adapt their behavior accordingly:

| Skill | Referenced Settings | Impact |
|-------|-------------------|--------|
| All skills | preferences.language | Output language for documents and communication |
| tech-lead | idStrategy, backend, database | ID strategy for data modeling |
| be-main | backend.framework, idStrategy | Framework-specific code patterns |
| be-test | backend.testFramework | Jest vs pytest vs JUnit selection |
| be-spec | backend.apiStyle | REST vs GraphQL spec generation |
| fe-main | frontend.framework, styling, i18n | UI code generation patterns |
| qa-e2e | integrations.playwright | Test runner setup |
| ci | tools.ci, conventions.commitConvention | CI pipeline and commit rules |
| devops | tools.containerization | Docker vs direct execution |
| product-designer | integrations.figma | Figma MCP availability |
| be-spec, be-main, fe-main | conventions.contractDriven | Enable/disable OpenAPI-based type and client generation |

## Reconfiguration

If `crew-config.json` already exists:

```markdown
## Existing Configuration Detected

`crew-config.json` already exists.

- **Project**: {project.name}
- **Language**: {preferences.language}
- **Backend**: {backend.framework} ({backend.language})
- **Frontend**: {frontend.framework} ({frontend.language})
- **Database**: {database.type}
- **ID Strategy**: {conventions.idStrategy}

Would you like to:
- (1) Use as-is
- (2) Re-analyze (reflect project changes)
- (3) Manually modify specific settings
```

## MCP Connection Detection

Also detect Figma and Playwright MCP connection status:

```bash
# Check MCP server list
# If TalkToFigma MCP is available → integrations.figma = true
# If Playwright MCP is available → integrations.playwright = true
```

## Validation

Verify that the generated `crew-config.json` is valid:

- [ ] Required fields exist (project.type, at least one of backend or frontend)
- [ ] Framework-language combination is valid (e.g., nestjs + typescript ✅, nestjs + python ❌)
- [ ] ID strategy is specified
- [ ] Test framework is specified
- [ ] preferences.language is set
