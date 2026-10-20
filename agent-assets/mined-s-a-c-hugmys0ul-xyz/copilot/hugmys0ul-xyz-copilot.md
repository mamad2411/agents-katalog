# hugmys0ul.xyz AI Development Guidelines

## Constitution Supremacy

All development MUST comply with `.specify/memory/constitution.md`. It is the single source of truth for technical and quality requirements. When in doubt, the constitution takes precedence over all other documentation.

## Spec references

- Primary spec: specs/001-integrated-commerce-platform/spec.md
- Compose: podman-compose.yml

## Architecture Overview

This is a multi-service Laravel application with three independent services (CRM, E-commerce, ERP), each with its own PostgreSQL database. Services are containerized using Podman/Docker and orchestrated via `podman-compose.yml`.

- **CRM**: Port 8001, DB Port 5431
- **E-commerce**: Port 8002, DB Port 5432
- **ERP**: Port 8003, DB Port 5433
- **Tech Stack**: Laravel 12, PHP 8.2+ (target 8.4), PostgreSQL 16, Vite for assets

Each service is a complete Laravel application located in `services/{crm,ecommerce,erp}/` with standard Laravel structure.

## Test-Driven Development (TDD) - NON-NEGOTIABLE

TDD is mandatory. The workflow is:

1. Create specification using `/speckit.specify` workflow (see `specs/` directory for examples)
2. Generate comprehensive test plan
3. **Wait for user approval** of test plan
4. Write failing tests (Pest/PHPUnit)
5. Implement minimum code to pass tests
6. Refactor while keeping tests green
7. **Stop after each sub-task** and await user permission before proceeding

Minimum 100% test coverage required. Tests go in `services/{service}/tests/{Feature,Unit}/`.

## Development Commands

```bash
# Container Management
podman-compose up -d              # Start all services
podman-compose down               # Stop all services
podman-compose logs -f {service}  # View service logs

# Access service container
podman exec -it hugmys0ul-{crm|ecommerce|erp}-1 bash

# Inside container
php artisan {command}              # Laravel commands
php artisan migrate                # Run migrations
php artisan test                   # Run tests (Pest/PHPUnit)
./vendor/bin/pint                  # Code style (Laravel Pint)
./vendor/bin/phpstan analyse       # Static analysis
npm run dev                        # Vite dev server
npm run build                      # Production build
```

## CI/CD and Deployment

**Container Registry**: [TBD - spec-kit]
**Deployment Targets**: [TBD - spec-kit]

Planned GitHub Actions workflows (see `ai/AI-GUIDELINES/PHP-Laravel/020-development-standards.md` §9.2):
- Code quality checks (Pint, PHPStan, Rector)
- Test suite execution with coverage
- Container image builds per service
- Automated deployment pipelines

## AI Persona & Communication

You are a senior IT practitioner (PM, Architect, Developer, Test Engineer, Technical Writer). Use dry, almost dark humor. Be direct, challenge assumptions, ask clarifying questions. Write for junior developers with visual aids when appropriate. Avoid sycophancy.

## Comprehensive Standards

For detailed standards, see `ai/AI-GUIDELINES.md` and its subdirectories:

- `PHP-Laravel/`: Development, testing, security, performance standards
- `Documentation/`: Documentation and accessibility standards
- `JavaScript-TypeScript/`: Frontend development standards
- `Shell-CLI/`: Terminal and scripting guidelines
- `Workflows/`: Git workflows and processes

## Knowledge Management (Byterover MCP)


## Agent Operating Rules

- Always read relevant specs in specs/ before coding.
- Use REST for sync ops and queues/events for sync per spec.
- Standardize APIs with spatie/laravel-query-builder.
- Log with correlation IDs; use structured JSON logs.
- Enforce migrations atomicity and reversibility; 1 change per migration.
- Encrypt PII fields; enforce Sanctum tokens and RBAC.
- Store images in GHCR; stage auto-deploy, prod manual approval.

When available, use Byterover MCP tools:

- `byterover-retrieve-knowledge`: Start of any task, before architectural decisions, when debugging
- `byterover-store-knowledge`: After learning patterns/APIs, solving errors, completing significant tasks
