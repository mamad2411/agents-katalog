# GitHub Copilot Instructions for Go-Admin

This is a comprehensive enterprise-grade admin management system based on Go + Gin framework with a Vue.js frontend. The project follows a layered architecture with modular design and Chinese localization.

## Project Architecture

**Core Structure:**

- `go-admin/` - Main backend application (Go + Gin + GORM + Casbin)
- `docs/` - Comprehensive Chinese documentation and guides
- Frontend is separate: [go-admin-ui](https://github.com/go-admin-team/go-admin-ui)

**Backend Architecture:**

```
cmd/           # CLI commands (server, migrate, gen, config)
app/admin/     # Admin module (APIs, Services, Models)
common/        # Shared components (middleware, database, actions)
config/        # Configuration files and settings
```

## Key Development Patterns

### 1. Multi-Command Architecture

Use Cobra CLI for different operation modes:

```bash
./go-admin server    # Start API server
./go-admin migrate   # Database migration
./go-admin gen       # Code generation
```

### 2. Service Layer Pattern

All business logic follows the Service pattern in `app/admin/service/`:

```go
type SysUser struct {
    service.Service
}
func (e *SysUser) GetPage(c *dto.SysUserGetPageReq, p *actions.DataPermission, list *[]models.SysUser, count *int64) error
```

### 3. Data Permission System

Every data operation includes permission scoping via `actions.DataPermission`:

```go
err := e.Orm.Scopes(
    actions.Permission(data.TableName(), p),
).Find(list).Error
```

### 4. JWT Authentication

Development vs Production token handling in `common/middleware/auth.go`:

- Dev mode: 876010 hours (never expire)
- Prod mode: Configurable timeout

### 5. Swagger Documentation

Auto-generated API docs with Chinese comments:

```go
//go:generate swag init --parseDependency --parseDepth=6 --instanceName admin -o ./docs/admin
```

## Development Workflow

### Environment Setup

```bash
# Clone and setup
git clone <this-repo>
cd go-admin

# Install dependencies
go mod tidy

# Setup config
cp config/settings.yml.example config/settings.yml
# Edit database settings in config/settings.yml

# Initialize database
./go-admin migrate -c config/settings.yml

# Start development server
./go-admin server -c config/settings.yml
```

### Testing Strategy

Following test pyramid in `docs/development/testing.md`:

- Unit tests: `go test ./...`
- Integration tests with testcontainers
- API tests via httptest
- Benchmarks: `go test -bench=.`

### Code Generation

Built-in code generator for CRUD operations:

```bash
./go-admin gen -c config/settings.yml -t tablename
```

## Chinese Localization Standards

- **All comments in Traditional Chinese** (繁體中文)
- **Documentation in `docs/`** follows Taiwan terminology
- **Swagger annotations** include Chinese descriptions
- **Error messages and logs** in Chinese where appropriate

## Configuration Management

Uses `github.com/spf13/viper` for config:

- `config/settings.yml` - Main config
- Environment-specific configs (dev, prod, test)
- Database drivers: MySQL, PostgreSQL, SQLite

## Security & Permissions

- **RBAC model** via Casbin integration
- **JWT tokens** with configurable expiration
- **Data permissions** enforced at ORM level
- **Route-level middleware** for authentication

## Build & Deployment

```bash
# Standard build
make build

# Docker build
make build-linux
docker-compose up -d

# SQLite build (for development)
make build-sqlite
```

## Documentation Structure

Comprehensive docs in `docs/`:

- `development/` - Development guides and architecture
- `docker/` - Container deployment guides
- `tests/` - Testing guides and strategies
- `changes/` - Change logs with timestamps

When working on this codebase, always check the extensive documentation in `docs/` for detailed implementation patterns and maintain consistency with the established Chinese localization standards.
