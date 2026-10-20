# GitHub Copilot Instructions

Welcome to the PDF Viewer POC repository! This file provides guidance for GitHub Copilot coding agent when working on this project.

## Quick Start

**Essential Commands:**
```bash
make install          # First-time setup (installs all dependencies)
make qa              # Validate code before committing (format, lint, type, test)
make dev-backend     # Start backend server at http://localhost:8000
make dev-frontend    # Start frontend server at http://localhost:5173
```

**Before Every Commit:**
1. `make qa` - Run full quality assurance suite
2. `pre-commit run --all-files` - Check for secrets and style issues

## Project Overview

Modern PDF viewer proof-of-concept with React 19.1 frontend and FastAPI backend. Key features include full-text search with highlighting, URL loading, form field extraction, and ground truth comparison UI.

**Tech Stack:**
- **Frontend**: React 19.1, TypeScript, Material UI v7, PDF.js 5.3+, Vite, Zustand
- **Backend**: FastAPI, Python 3.11+, UV package manager, Pydantic v2
- **Testing**: Vitest (frontend), pytest (backend), Playwright (E2E)
- **Code Quality**: Ruff, Black, ESLint, Prettier, mypy, TypeScript

## Repository Structure

```
pdfviewer/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI route handlers
│   │   ├── models/       # Pydantic v2 models
│   │   ├── services/     # Business logic
│   │   ├── middleware/   # CORS, logging, error handling
│   │   ├── utils/        # Helpers, decorators
│   │   └── main.py       # FastAPI application
│   └── uploads/          # PDF storage (gitignored)
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API clients
│   │   └── store/        # Zustand state management
│   └── public/           # Static assets
├── tests/
│   ├── test_*.py         # Backend unit tests
│   ├── integration/      # API integration tests
│   └── e2e/             # Playwright E2E tests
├── docs/                 # Project documentation
├── configs/              # Configuration files
└── scripts/              # Build and utility scripts
```

## Development Workflow

### Setup Commands
```bash
make install          # Install all dependencies (auto-detects uv/pip)
make dev-backend      # Start backend server (http://localhost:8000)
make dev-frontend     # Start frontend server (http://localhost:5173)
```

### Quality Assurance
```bash
make qa              # Run full QA suite (format, lint, type, test)
make lint            # Run all linters
make format          # Format all code
make type            # Type check (mypy + tsc)
make test            # Run unit and integration tests
make test-smoke      # Quick smoke tests only
make test-e2e        # End-to-end tests (requires servers running)
```

### Before Committing
1. Run `make qa` to ensure code quality
2. Verify tests pass: `make test`
3. Check for secrets: `pre-commit run --all-files`

## Dependency Management

### Adding Dependencies

**Python (Backend):**
- Preferred: Use `uv` for faster dependency management: `uv pip install <package>`
- Fallback: Use `pip` if `uv` is not available: `pip install <package>`
- Update `configs/pyproject.toml` with the new dependency
- Run `make install` to ensure consistency across environments
- **Security**: ALWAYS check dependencies for known vulnerabilities before adding

**JavaScript/TypeScript (Frontend):**
- Use `npm install <package>` from the `frontend/` directory
- Prefer exact versions for stability: `npm install <package>@<version> --save-exact`
- Update `frontend/package.json` automatically via npm
- Run `npm audit` to check for security vulnerabilities

### Updating Dependencies

**Backend:**
```bash
# Update a specific package
uv pip install --upgrade <package>  # or pip install --upgrade <package>

# Update all packages (careful!)
uv pip install --upgrade -r configs/pyproject.toml
```

**Frontend:**
```bash
cd frontend
npm update <package>        # Update specific package
npm outdated               # Check for outdated packages
npm audit fix              # Fix security vulnerabilities
```

**Best Practices:**
- Test thoroughly after updating dependencies
- Update one dependency at a time when possible
- Check breaking changes in CHANGELOG files
- Run full test suite: `make test`

## Coding Standards

### Python (Backend)
- **Python Version**: 3.11+ with modern syntax
  - Use `X | Y` for unions (not `Union[X, Y]`)
  - Use `datetime.UTC` (not `datetime.utc` or `timezone.utc`)
  - Use `isinstance(x, int | float)` patterns
- **Type Hints**: Mandatory for all functions and methods
- **Pydantic**: Use Pydantic v2 models for data validation
  - Use `computed_field` decorator for computed properties
  - Use `field_validator` for custom validation
- **Formatting**: Black (88 chars), Ruff for linting
- **Import Order**: Standard library, third-party, local imports
- **Error Handling**: Use structured logging (structlog)
- **API Decorators**: 
  ```python
  @log_api_call("operation_name", log_params=True, log_response=True)
  @log_file_operation("upload", file_param="file")
  ```

### TypeScript/React (Frontend)
- **React Version**: 19.1 with Strict Mode compatibility
  - Avoid legacy lifecycle methods
  - Use hooks (useState, useEffect, custom hooks)
  - Prefer functional components
- **Type Safety**: Strict TypeScript, no `any` types
- **State Management**: Zustand for global state
- **Styling**: Material UI v7 + Tailwind CSS
- **PDF.js**: 
  - Virtual page rendering (render visible pages only)
  - Use Web Workers (exact version matching pdf.js/pdf.worker.js)
  - Implement page.cleanup() for non-visible pages
  - Limit 3-5 concurrent page renders
- **Testing**: Vitest with Testing Library
  - Test user interactions, not implementation details
  - Use proper accessibility queries (getByRole, getByLabelText)

### General Principles
- **KISS**: Keep it simple, avoid over-engineering
- **DRY**: Don't repeat yourself, extract reusable logic
- **YAGNI**: Don't add features until needed
- **Test Coverage**: Maintain high test coverage for new code
- **Documentation**: Update docs when changing behavior

## Testing Requirements

### Test Organization
- **Unit Tests**: `tests/test_*.py` (backend), `src/**/__tests__/*.test.tsx` (frontend)
- **Integration Tests**: `tests/integration/api/`
- **E2E Tests**: `tests/e2e/`

### Writing Tests
- Follow existing test patterns in the repository
- Use descriptive test names: `test_should_reject_invalid_pdf_format()`
- Arrange-Act-Assert pattern
- Mock external dependencies appropriately
- Test edge cases and error conditions

### Coverage Expectations
- New features should have corresponding tests
- Aim for >80% coverage on new code
- Critical paths require 100% coverage

## Important Files & Patterns

### Key Backend Files
- `backend/app/main.py` - FastAPI app configuration
- `backend/app/api/` - API endpoints (upload, load_url, metadata, etc.)
- `backend/app/models/` - Pydantic models
- `backend/app/services/` - Business logic
- `backend/app/utils/decorators.py` - Logging decorators

### Key Frontend Files
- `frontend/src/components/PDFViewer/` - Main PDF viewer components
- `frontend/src/hooks/usePDFSearch.ts` - Search functionality
- `frontend/src/components/TestPDFLoader.tsx` - Test PDF loader
- `frontend/src/components/PDFViewer/PDFExtractedFields.tsx` - Form extraction UI

### Configuration Files
- `configs/pyproject.toml` - Python dependencies and tools
- `frontend/package.json` - Node dependencies
- `configs/Makefile` - Development commands
- `.pre-commit-config.yaml` - Pre-commit hooks
- `configs/mypy.ini` - Type checking config (symlinked to root)

## Security Guidelines

### Critical Rules
- **NO SECRETS**: Never commit API keys, tokens, passwords, or credentials
- **Environment Variables**: Use `.env` files (see `.env.example`)
- **Pre-commit Hooks**: Always run before committing
  ```bash
  pre-commit install
  pre-commit run --all-files
  ```
- **Secret Scanning**: `gitleaks detect` and `detect-secrets scan`
- **Input Validation**: Validate all user inputs with Pydantic
- **File Upload**: 50MB limit, validate PDF format with python-magic
- **CORS**: Configured for ports 5173-5176 (development only)

### What NOT to Commit
- `.env` files (use `.env.example` template)
- API keys, tokens, passwords
- Private keys or certificates
- Uploaded PDFs (`backend/uploads/`)
- Node modules, Python cache (`__pycache__`)
- Build artifacts (`dist/`, `artifacts/`)
- IDE-specific files (except `.vscode` if widely useful)

## Git Workflow

### Branch Strategy
- **Primary Branch**: `main` (NOT `master`)
- **Feature Branches**: Create from `main`, use descriptive names
  - Examples: `feature/pdf-search`, `fix/memory-leak`, `docs/api-update`
- **Short-lived**: Keep branches focused, merge quickly, delete after merge
- **Clean History**: Delete merged branches immediately

### Commit Messages
- Use conventional format: `type: description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- Examples:
  - `feat: add PDF full-text search with highlighting`
  - `fix: resolve memory leak in PDF renderer`
  - `docs: update API documentation for load-url endpoint`
  - `test: add integration tests for PDF upload`

## Common Tasks & Patterns

### Adding a New API Endpoint
1. Create route handler in `backend/app/api/`
2. Define Pydantic models in `backend/app/models/`
3. Add business logic in `backend/app/services/`
4. Add unit tests in `tests/`
5. Add integration tests in `tests/integration/api/`
6. Update API documentation in `docs/API.md`

### Adding a React Component
1. Create component in `frontend/src/components/`
2. Add tests in same directory: `ComponentName.test.tsx`
3. Export from component directory
4. Update parent components to use it
5. Test with Vitest: `npm test`

### Running Specific Tests
```bash
# Backend
pytest tests/test_health.py -v
pytest tests/integration/api/test_upload.py::test_upload_valid_pdf -v

# Frontend
npm test -- ComponentName
npm test -- --run src/components/__tests__/FileUpload.test.tsx
```

## System Dependencies

### Required: libmagic
File type detection requires `libmagic`:
```bash
# macOS
brew install libmagic

# Ubuntu/Debian
sudo apt-get install libmagic1

# RHEL/CentOS/Fedora
sudo yum install file-devel

# Windows - python-magic-bin auto-installed
```

## Performance Considerations

### PDF.js Optimization
- Render only visible pages (virtual scrolling)
- Use Web Workers to avoid blocking UI
- Call `page.cleanup()` on non-visible pages
- Limit concurrent renders to 3-5 pages
- Use HTTP Range Requests for large files

### Backend
- Use async operations for I/O
- Implement request timeouts
- Stream large responses when possible

### Frontend
- Lazy load components
- Virtualize long lists
- Memoize expensive computations
- Debounce search inputs

## Documentation

Before making changes, review:
- `README.md` - Project overview and quick start
- `CLAUDE.md` - AI assistant development guide
- `docs/TECHNICAL.md` - Technical details and setup
- `docs/API.md` - API endpoint documentation
- `docs/CONTRIBUTING.md` - Contribution guidelines
- `tests/README.md` - Testing guide

## Troubleshooting

### Backend Issues
- **libmagic errors**: Reinstall libmagic for your OS
- **Import errors**: Check virtual environment, reinstall dependencies
- **Type errors**: Run `mypy backend` to diagnose

### Frontend Issues
- **Module not found**: Run `npm install` in frontend/
- **Type errors**: Run `npm run type-check`
- **Build errors**: Check node version (need 18+)

### Test Failures
- **Fixture missing**: Run `make test-integration-fixtures`
- **Server not running**: Start with `make dev-backend` and `make dev-frontend`
- **Timeout**: Increase timeout or check server logs

## Task Selection Guidance

### Good Tasks for Copilot
- Bug fixes with clear reproduction steps
- Adding tests for existing functionality
- Documentation updates
- UI improvements and accessibility fixes
- Code refactoring with clear scope
- Adding validation or error handling

### Tasks Requiring Human Review
- Security-critical changes
- Database schema migrations
- Authentication/authorization logic
- Production deployment changes
- Major architectural decisions
- Breaking API changes

## Additional Resources

- **API Docs**: http://localhost:8000/docs (when backend running)
- **Frontend**: http://localhost:5173 (when frontend running)
- **Test Reports**: `artifacts/htmlcov/` (backend), `frontend/coverage/` (frontend)

---

**Author**: Dominic Fahey (domfahey@gmail.com)  
**License**: MIT  
**Last Updated**: 2025-10-30
