---
name: go-backend-init
description: Initialize a new Go backend repository with production-grade engineering setup. Use when creating new Go microservice projects, setting up Go repos from scratch, or when the user asks to scaffold a Go backend with best practices (Uber FX, Ent ORM, gRPC, CI/CD, linting, Docker).
metadata:
  author: luoling8192
  version: "2026.03.12"
---

# Go Backend Repository Initialization Skill

Initialize a production-grade Go backend repository following battle-tested patterns from real microservice projects.

## When to Use

- User asks to create a new Go backend project
- User wants to scaffold a Go microservice repo
- User needs a Go project template with CI/CD, linting, Docker, etc.

## Initialization Checklist

When invoked, walk through these steps **in order**. Ask the user for project-specific details first:

1. **Project name** (Go module path, e.g., `github.com/org/my-service`)
2. **Service names** (e.g., `platform`, `api`, `worker` — at least one)
3. **Go version** (default: latest stable, currently 1.25)
4. **Database** (PostgreSQL with Ent ORM is default; ask if needed)
5. **Proto/gRPC** (yes/no — if yes, set up buf + generated code structure)
6. **System dependencies** (any C libraries like libsoxr, etc.)

## Directory Structure

Create this structure, adapting service names to the user's input:

```
.
├── cmd/
│   └── <service>/
│       └── main.go              # Uber FX app entry point
├── internal/
│   ├── configs/                 # Config loading (.env + optional config center)
│   ├── datastore/               # Database client initialization (Ent)
│   ├── grpc/
│   │   ├── servers/             # gRPC + HTTP server lifecycle
│   │   ├── services/            # gRPC service implementations (business logic)
│   │   └── registers/           # Service registration with gRPC server
│   └── models/                  # Data access layer (Ent ORM CRUD)
├── pkg/                         # Reusable packages (errors, utils)
│   └── apierrors/               # Standardized error handling
├── libs/                        # Shared test/logging utilities
├── schema/                      # Ent ORM schema definitions
│   └── generate.go              # go:generate directive for Ent
├── ent/                         # (generated) Ent ORM code — DO NOT EDIT
├── api/
│   └── generated/               # (generated) Proto/gRPC code — DO NOT EDIT
├── hack/                        # Dev scripts
├── .github/
│   ├── actions/
│   │   └── setup-go-env/
│   │       └── action.yml       # Composite action: Go + system deps
│   └── workflows/
│       └── ci.yml               # Lint + Test + Build + Autofix
├── .vscode/
│   ├── settings.json
│   └── extensions.json
├── .editorconfig
├── .gitignore
├── .golangci.yml
├── .tool-versions
├── .env.example
├── cspell.config.yaml
├── renovate.json
├── Dockerfile
├── go.mod
└── CLAUDE.md                    # AI assistant context
```

## File Templates

### 1. `go.mod`

```go
module {{MODULE_PATH}}

go {{GO_VERSION}}

require (
	go.uber.org/fx v1.23.0
	// Add Ent ORM if using database
	entgo.io/ent v0.14.4
	// Add gRPC if using proto
	google.golang.org/grpc v1.72.0
	google.golang.org/protobuf v1.36.6
	// Add Echo if using HTTP
	github.com/labstack/echo/v4 v4.13.4
)
```

After creating, run `go mod tidy` to resolve dependencies.

### 2. `.editorconfig`

```ini
root = true

[*.toml]
indent_size = 4
indent_style = space
max_line_length = 100
trim_trailing_whitespace = true

[*.rs]
indent_size = 2
indent_style = space
max_line_length = 100
trim_trailing_whitespace = true

[*.md]
# double whitespace at end of line
# denotes a line break in Markdown
trim_trailing_whitespace = false

[*.{js,ts,vue,tsx,jsx,html,css,json,yaml,yml}]
indent_size = 2
indent_style = space
trim_trailing_whitespace = true

[*.go]
indent_size = 2
indent_style = tab
trim_trailing_whitespace = true

[*.proto]
indent_size = 2
indent_style = space

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
```

### 3. `.golangci.yml`

See [references/golangci.yml](references/golangci.yml) for the full config.

Key principles:
- Use `version: "2"` format
- Start with `default: all`, then disable noisy/opinionated linters
- Enable `gofmt` + `goimports` formatters
- Exclude generated code paths (`api/`, `ent/`) with `generated: lax`
- Set sane thresholds: `dupl: 600`, `nestif: min-complexity: 9`

### 4. `.gitignore`

```gitignore
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib
bin/*
dist/*
out/*

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool
*.out

# Go workspace file
go.work

# Editor and IDE
.idea
*.swp
*.swo
*~
.DS_Store

# Config files (keep example)
config/*
!config/config.yaml

__debug*
.env
.env.local

# Binary outputs (add your service names)
./main
```

### 5. CI Workflow (`.github/workflows/ci.yml`)

See [references/ci.yml](references/ci.yml) for the full workflow.

Key jobs:
- **Lint** (push only): golangci-lint with 7m timeout
- **Unit Test**: `go test ./...`
- **Nilaway** (null safety): static analysis excluding generated code
- **Build Test** (PR only): `go build ./...`
- **Autofix** (PR only): auto-fix lint and commit with `[autofix]` tag, with conflict guard

### 6. Composite Action (`.github/actions/setup-go-env/action.yml`)

```yaml
name: setup-go-env
description: Setup Go environment with required dependencies
runs:
  using: composite
  steps:
    - uses: actions/setup-go@v6
      with:
        go-version: "^{{GO_VERSION}}"
        cache: true
    # Add system dependencies if needed:
    # - run: |
    #     sudo apt-get update -qq
    #     sudo apt-get install --no-install-recommends -y \
    #       libsoxr-dev \
    #       pkg-config
    #   shell: bash
```

### 7. `.vscode/settings.json`

```jsonc
{
  "go.useLanguageServer": true,
  "go.lintOnSave": "package",
  "go.vetOnSave": "workspace",
  "go.coverOnSave": false,
  "go.lintTool": "golangci-lint-v2",
  "go.lintFlags": [
    "--fast-only",
    "--config=${workspaceFolder}/.golangci.yml"
  ],
  "go.formatTool": "gofmt",
  "go.inferGopath": true,
  "go.coverOnSingleTest": true,
  "go.testTimeout": "900s",
  "go.testFlags": ["-v", "-count=1"],
  "go.toolsManagement.autoUpdate": true,
  "gopls": {
    "build.buildFlags": [],
    "ui.completion.usePlaceholders": true,
    "ui.semanticTokens": true
  },
  "[go]": {
    "editor.insertSpaces": false,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": "always"
    }
  },
  "go.testEnvVars": {
    "LOG_LEVEL": "debug"
  }
}
```

### 8. `.vscode/extensions.json`

```json
{
  "recommendations": [
    "streetsidesoftware.code-spell-checker",
    "mikestead.dotenv",
    "EditorConfig.EditorConfig",
    "yzhang.markdown-all-in-one",
    "redhat.vscode-yaml",
    "golang.go",
    "bufbuild.vscode-buf"
  ]
}
```

### 9. `renovate.json`

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:recommended",
    ":dependencyDashboard",
    ":semanticPrefixFixDepsChoreOthers",
    ":prHourlyLimitNone",
    ":prConcurrentLimitNone",
    ":ignoreModulesAndTests",
    "group:monorepos",
    "group:recommended",
    "group:allNonMajor",
    "replacements:all",
    "workarounds:all"
  ],
  "rangeStrategy": "bump",
  "labels": ["dependencies"],
  "minimumReleaseAge": "3 days"
}
```

### 10. `.tool-versions`

```
golang {{GO_VERSION}}
```

### 11. `cspell.config.yaml`

```yaml
version: "0.2"
ignorePaths: []
dictionaryDefinitions: []
dictionaries: []
words:
  - entgo
  - Ents
  - entsql
  - enttest
  - fxevent
  - nolint
  - stretchr
  - structpb
  - timestamppb
  # Add project-specific words as they arise
```

### 12. `Dockerfile` (multi-stage)

See [references/Dockerfile](references/Dockerfile) for the full template.

Key patterns:
- Build stage: `golang:<version>-bookworm` with system deps
- Go mod download first (layer caching)
- Build all services under `./cmd/*` dynamically
- Runtime stage: `debian:bookworm-slim` (minimal image)
- Use `--mount=type=cache` for Go build cache

### 13. Uber FX Entry Point (`cmd/<service>/main.go`)

```go
package main

import (
	"log/slog"
	"os"

	"go.uber.org/fx"
	"go.uber.org/fx/fxevent"

	"{{MODULE_PATH}}/internal/configs"
	"{{MODULE_PATH}}/internal/datastore"
	"{{MODULE_PATH}}/internal/models"
)

func main() {
	app := fx.New(
		fx.WithLogger(func(logger *slog.Logger) fxevent.Logger {
			return &fxevent.SlogLogger{Logger: logger}
		}),
		fx.Provide(func() *slog.Logger {
			return slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
				Level: slog.LevelDebug,
			}))
		}),
		configs.Module(),
		datastore.Module(),
		models.Modules(),
		// Add service-specific modules here
	)
	app.Run()
}
```

### 14. Uber FX Constructor Pattern

All services and models MUST follow this pattern:

```go
type NewXXXModelParams struct {
	fx.In
	Client *ent.Client
	Logger *slog.Logger
	Config *configs.Config
}

func NewXXXModel() func(NewXXXModelParams) *XXXModel {
	return func(params NewXXXModelParams) *XXXModel {
		return &XXXModel{
			client: params.Client,
			logger: params.Logger,
			config: params.Config,
		}
	}
}
```

Register in module files:

```go
// internal/models/models.go
func Modules() fx.Option {
	return fx.Options(
		fx.Provide(xxx.NewXXXModel()),
		// ... other models
	)
}
```

### 15. Ent ORM Schema (`schema/generate.go`)

```go
package schema

//go:generate go run -mod=mod entgo.io/ent/cmd/ent generate ./ --target ../ent --feature=sql/execquery,sql/schemaconfig,sql/lock,sql/upsert
```

Schema conventions:
- UUID primary keys: `field.UUID("id", uuid.UUID{}).Default(uuid.New).Unique().Immutable()`
- Soft delete: `field.Time("deleted_at").Optional().Nillable()`
- Enum status fields: `field.Enum("status").Values("ACTIVE", "INACTIVE")`
- Timestamps: `field.Time("created_at").Default(time.Now).Immutable()`

### 16. `.env.example`

```bash
# =============================================================================
# Application Configuration
# =============================================================================

# Log level: debug, info, warn, error
LOG_LEVEL=info

# =============================================================================
# Database
# =============================================================================
DATABASE_DSN=postgres://user:pass@localhost:5432/dbname?sslmode=disable

# =============================================================================
# Service Ports
# =============================================================================
HTTP_PORT=8080
GRPC_PORT=9090

# =============================================================================
# Authentication
# =============================================================================
# JWT_SECRET=your-secret-here

# =============================================================================
# External Services
# =============================================================================
# REDIS_URL=redis://localhost:6379/0
```

### 17. `CLAUDE.md` Template

Generate a CLAUDE.md that documents:
- Project overview (what it does, key capabilities)
- Technology stack
- Essential commands (run, test, lint, generate)
- Architecture (services, layers, communication)
- Directory structure
- Development workflow (schema changes, API changes, service implementation)
- DI patterns (Uber FX constructors)
- Code style and best practices

Use the reference project's CLAUDE.md as a structural template, but tailor content to the new project.

## Post-Initialization Steps

After scaffolding, run these commands:

```bash
# Initialize Go module
go mod init {{MODULE_PATH}}
go mod tidy

# Initialize git
git init

# Generate Ent code (if using database)
go generate ./...

# Verify lint config
golangci-lint run

# Verify build
go build ./...

# Create initial commit
git add .
git commit -m "feat: initial project scaffold"
```

## Key Principles

1. **Config via .env** — no YAML config files; use environment variables with `.env` for local dev
2. **Uber FX everywhere** — all DI through FX constructors, never manual instantiation
3. **Generated code is sacred** — never edit `ent/` or `api/generated/`, always regenerate
4. **Soft delete by default** — `deleted_at` field on user-facing entities
5. **Structured logging** — `*slog.Logger` injected via FX, never `fmt.Println`
6. **Factory pattern for providers** — when supporting multiple backends (TTS, storage, etc.)
7. **Layered architecture** — Model (CRUD) → Service (business logic) → Registration → Server
