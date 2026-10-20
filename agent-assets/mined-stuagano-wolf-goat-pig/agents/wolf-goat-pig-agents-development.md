# Wolf Goat Pig Contributor Guidelines

Welcome to the project! Please follow these conventions whenever you modify files in this repository.

## Coding Conventions
- **Python (backend/scripts/tests)**
  - Target Python 3.11 syntax.
  - Prefer explicit imports and type annotations in new or heavily modified modules.
  - Keep functions small and focused; extract helpers when logic exceeds ~40 lines.
  - Use f-strings for string formatting and favour pathlib over os.path for new filesystem work.
- **TypeScript/JavaScript (frontend/src)**
  - Target modern ES modules with TypeScript where available.
  - Use functional React components and hooks; avoid legacy class components.
  - Keep state colocated; lift only when shared across siblings.
  - Prefer `const` over `let`, and ensure all asynchronous code handles error states.
- **Testing Artifacts**
  - Place new automated tests alongside the code they cover (e.g., `backend/tests`, `frontend/src/__tests__`).
  - Provide fixtures or mocks under `tests/` or `frontend/src/test-utils` instead of duplicating setup logic.

## Testing Expectations
Before requesting review, validate your work locally:
1. For full regression coverage run `./scripts/diagnostics/run_simulation_tests.sh`. This orchestrates backend pytest suites, frontend unit coverage, and simulation functional checks.
2. For backend-only iterations, at minimum run:
   - `cd backend && python -c "from app.main import app"` to confirm dependencies and import checks still succeed.
   - `cd backend && pytest` (targeted modules are fine, e.g., `pytest tests/test_simulation_unit.py`).
3. For frontend changes limited to `frontend/src`, run `cd frontend && npm test -- --watchAll=false` and, when visuals are affected, `npm run build` to ensure the bundle compiles cleanly.
4. Document any skipped checks (with justification) in your PR summary.

## Deployment Testing
Before deploying to production on GCP:
1. **Run deployment checklist**: `.husky/deployment-checklist` - comprehensive pre-deployment validation
2. **Test production builds locally**:
   - Backend container: `./scripts/deployment/test-prod-backend.sh`
   - Frontend static build: `./scripts/deployment/test-prod-frontend.sh`
   - Full stack: `./scripts/deployment/test-prod-all.sh` (interactive menu)
3. **Verify deployment health**: `./scripts/deployment/verify-deployment.sh`
4. **Docker production simulation**: `docker-compose -f docker-compose.prod.yml up`

Git hooks are configured to run automatic checks:
- **Pre-push**: Runs tests and build verification before pushing to remote
- **Pre-commit**: Basic syntax and security checks (if configured)

Additional tooling documentation is available in `docs/guides/local-development.md`, `docs/guides/local-deployment-testing.md`, `docs/guides/project-structure.md`, Reference these when in doubt.

## Area-Specific Notes
- **Backend (`backend/app`)**
  - Follow FastAPI best practices: define routers under `backend/app/api`, schemas in `backend/app/schemas`, and business logic under `backend/app/services`.
  - Ensure database migrations or schema updates are mirrored in `backend/app/database` helpers and accompanied by fixture updates.
  - When touching simulation flows, cross-check expectations in `scripts/diagnostics/simulation_startup_check.py` and `tests/functional/test_simulation_functional.py`.
- **Frontend (`frontend/src`)**
  - Keep shared UI primitives under `frontend/src/components` and avoid deep relative imports; prefer alias paths defined in `tsconfig.json`.
  - Update Storybook or MDX docs (under `frontend/src/docs`) when user-facing behavior changes.
  - Coordinate state changes with backend contract updates by syncing TypeScript types with the FastAPI schemas.

## Pull Request Summary Requirements
Every PR description must include:
1. **Summary** – bullet list of meaningful changes, referencing impacted domains (backend/frontend/tests).
2. **Validation** – commands or scripts executed (e.g., `./scripts/diagnostics/run_simulation_tests.sh`, `cd backend && pytest`). Note any failures and rationale.
3. **Screenshots** – include when frontend visuals change. Use local tooling or CI artifacts to capture them.

Thank you for contributing! Keeping these guidelines consistent helps us ship reliable features quickly.
