# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Settings 
.claude/settings.local.json


## Architecture

This is a multi-platform CRUD application using Clean Architecture with:
- **Backend**: .NET 8 API with Entity Framework Core, MediatR (CQRS), SQLite database
- **Frontend**: Angular 20 with TypeScript, RxJS
- **Layers**: Domain → App → Infrastructure → Api → UI (Angular/MAUI)
- **Ports**: API runs on 5172 (HTTP) and 7268 (HTTPS), Angular on 4200

## Branch and Deployment Strategy

This project uses a 3-stage pipeline:
- **Feature branches** (`feature/*`, `bugfix/*`, `hotfix/*`) → Development work, no deployment
- **dev branch** → Deploys to dev environment (dev.your-app.com)
- **main branch** → Deploys to production (your-app.com)

### Deployment Triggers
- Merge to `dev` → Triggers `deploy-dev.yml` → Deploys to dev environment → Runs full E2E suite
- Merge to `main` → Triggers `deploy-production.yml` → Deploys to production → Runs smoke tests

### Testing Strategy

Test distribution across the pipeline:
- **Feature branches**: Unit tests only (~3-5 min)
- **PR to dev**: Integration + smoke E2E tests (~5-10 min)
- **Dev deployment**: Full E2E test suite (~15-20 min)
- **PR to main**: Production readiness validation (~10-15 min)
- **Production deployment**: Smoke tests + health checks (~2-5 min)

See @docs/03-Development/specs/2025-09-29-branch-deployment-strategy/ for complete specification.

## Key Commands

### Development
```bash
# Start both API and Angular (use PowerShell)
scripts/LaunchApps.ps1

# Kill running servers before builds
scripts/kill-servers.ps1

# Start API only
dotnet run --project src/Api/Api.csproj --launch-profile http

# Start Angular only
cd src/Angular && npm start
```

### Build
```bash
# Build entire solution
dotnet build solutions/Crud.sln

# Build backend only
dotnet build solutions/Crud.Backend.sln

# Build Angular
cd src/Angular && npm run build
```

### Testing
```bash
# Backend unit tests
dotnet test test/Tests.Unit.Backend/Tests.Unit.Backend.csproj

# Backend integration tests
dotnet test test/Tests.Integration.Backend/Tests.Integration.Backend.csproj

# E2E tests (using Playwright webServer - see ADR-003)
cd test/Tests.E2E.NG
npm run test:smoke       # 2-minute smoke tests only
npm run test:critical    # 5-minute critical tests
npm run test             # Run ALL E2E tests (~15-20 min)

# Angular tests
cd src/Angular && npm test
```

### Code Quality & Formatting
```bash
# IMPORTANT: Always run before committing!

# .NET formatting - check for issues
dotnet format solutions/Crud.sln --verify-no-changes

# .NET formatting - auto-fix issues
dotnet format solutions/Crud.sln

# Angular linting
cd src/Angular && npm run lint
```

## E2E Testing Strategy

### Test Levels

E2E tests use Playwright's built-in webServer configuration (see `playwright.config.ts`). Tests are organized into three levels:

```bash
# Local development and CI/CD
npm run test:smoke       # @smoke tagged tests (~2-3 min) - Critical user flows
npm run test:critical    # @critical tagged tests (~5-10 min) - Production readiness validation
npm run test             # ALL tests (~15-20 min) - Comprehensive validation
```

### Manual Workflow Trigger

```bash
# Manually trigger full E2E tests on any branch
gh workflow run "Manual E2E Tests" --ref branch-name -f branch=branch-name
```

### Pipeline Usage

- **PR to dev**: Runs `test:smoke` (2-3 min quick validation)
- **PR to main**: Runs `test:critical` (5-10 min production readiness)
- **Deploy to dev**: Runs `test` (15-20 min full suite)
- **Deploy to production**: Runs `test:smoke` (2-3 min deployment validation)

### Technical Details

- **Playwright webServer**: Automatic server management, unique database per test run
- **Database isolation**: Unique filenames prevent locking issues
- **Serial execution**: `workers: 1` for SQLite/EF Core compatibility
- **CI/CD**: Same webServer configuration as local development

⚠️ **IMPORTANT**: The `test:smoke` and `test:critical` commands use environment variables for CI compatibility. Do not remove these variables from `package.json`.

## Health Checks

The application uses ASP.NET Core Health Checks middleware following Kubernetes liveness/readiness patterns:

- **`GET /health`** - Liveness probe (is app alive?)
  - Used by: Kubernetes, load balancers
  - Returns: Standard ASP.NET Core health check JSON

- **`GET /health/ready`** - Readiness probe (is app ready for traffic?)
  - Used by: Kubernetes, Playwright test startup
  - Includes EF Core warm-up (`CountAsync`) to prevent cold-start timeouts

- **`GET /health/detailed`** - Diagnostic endpoint
  - Used by: Operations, support teams
  - Returns: Detailed JSON with environment, database provider, app metadata

All endpoints use tag-based filtering (`"live"` and `"ready"` tags) on the `DatabaseHealthCheck` class.

## Project Structure

- `src/Domain/` - Business entities and logic (no external dependencies)
- `src/App/` - Application services, CQRS handlers, DTOs (depends only on Domain)
- `src/Infrastructure/` - EF Core, repositories, external services
- `src/Api/` - ASP.NET Core Web API controllers
- `src/Angular/` - Angular 20 frontend application
- `test/Tests.Unit.Backend/` - xUnit unit tests with Moq and FluentAssertions
- `test/Tests.Integration.Backend/` - API integration tests with WebApplicationFactory
- `test/Tests.E2E.NG/` - Playwright E2E tests
- `solutions/` - Solution files (Crud.sln, Crud.Backend.sln, Crud.Angular.sln)
- `docs/` - Architecture, development guides, quality control documentation
- `scripts/` - PowerShell automation scripts (LaunchApps.ps1, kill-servers.ps1)

## Database

- **Development**: SQLite with file-based storage
- **Database Files**: Multiple SQLite databases for different environments
  - `src/Api/CrudApp.db` - Main development database
  - `src/Api/CrudAppDev.db` - Development database
  - `src/Api/CrudAppDesignTime.db` - Design-time database
  - `CrudTest_local.db` - Local test database
- **Connection strings**: Configured in `appsettings.*.json` files
- **Migrations**: `dotnet ef migrations add <name> -p src/Infrastructure -s src/Api`
- **Update database**: `dotnet ef database update -p src/Infrastructure -s src/Api`

## Clean Architecture Rules

1. **Domain** has no external dependencies
2. **App** depends only on Domain
3. **Infrastructure** implements interfaces from App/Domain
4. **Api** orchestrates via dependency injection
5. Use MediatR for all business operations
6. Repository pattern for data access
7. DTOs for API contracts, separate from domain models

## Important Rules

- **NEVER commit or push without explicit permission**
- **NEVER create documentation files unless explicitly requested**
- **ALWAYS prefer editing existing files over creating new ones**
- **ALWAYS run code formatting before committing:**
  - `dotnet format solutions/Crud.sln` for .NET code
  - `npm run lint` in src/Angular for TypeScript code

## Known Issues & Workarounds

### Settings.local.json Not Auto-Loading
- **Issue**: `.claude/settings.local.json` permissions don't load automatically at startup
- **Workaround**: Run `/permissions` command once at session start to trigger settings loading
- **Fix Applied**: Removed conflicting `"Bash(echo:*)"` from "ask" section that was overriding specific echo commands in "allow" section

## Key References

- API ports: 5172 (HTTP), 7268 (HTTPS)
- Angular port: 4200
- Serial testing decision: @docs/02-Architecture/Decisions/0001-Serial-E2E-Testing.md
- Dev branch is the default branch
- No Failures Ever - We don't try and move past it.  We will troubleshoot and solve it.  Use additional tools if necessary.
- NEVER REBASE!!! NO EXCEPTIONS!!!
- Manual E2E Tests should be run from the branch that pushed the changes.  Do this by using --ref and -f params
- When I ask for e2e tests, run all e2e tests;  if i want smoke tests, i will ask for smoke tests;
- When I ask for e2e tests on CI, run them on using the existing branch name for both ref and f branch: parameters.