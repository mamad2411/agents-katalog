# Marker-OCR-API Project Rules

## Architecture Principles

### Core Principles
- **One Layer, One Responsibility**: Each layer has a single, well-defined responsibility
- **Separation of Concerns**: Business logic, API layer, and data handling are strictly separated
- **Dependency Injection**: Services are injected rather than imported directly
- **Clean Architecture**: Dependencies point inward toward the business logic

### Project Structure
```
backend/
├── app/
│   ├── core/           # Configuration, exceptions, logging
│   │   ├── config.py   # Pydantic Settings with environment variables
│   │   ├── exceptions.py  # Custom exception classes
│   │   └── logger.py   # Structured logging setup
│   ├── api/            # FastAPI routes and HTTP layer
│   │   ├── dependencies.py  # Dependency injection (singletons with LRU cache)
│   │   └── routes/     # Route modules (health, documents)
│   ├── services/       # Business logic layer
│   │   ├── document_parser.py  # Real Marker service
│   │   ├── document_parser_mock.py  # Mock for tests
│   │   ├── file_handler.py  # Real file operations
│   │   ├── file_handler_mock.py  # Mock for tests
│   │   ├── redis_service.py  # Redis cache/task queue
│   │   └── marker_log_handler.py  # Marker-specific log handling
│   ├── models/         # Pydantic models for requests/responses
│   │   ├── request_models.py  # Request validation models
│   │   ├── response_models.py  # Response models
│   │   └── enums.py    # Enumeration types
│   └── utils/          # Pure utility functions
│       └── validators.py  # Input validation utilities
├── Dockerfile          # Production/dev image (with all ML dependencies)
├── Dockerfile.test-modelFree  # Lightweight test image (no ML models)
├── Dockerfile.test-FullStack  # Full test image (with ML models)
├── requirements-base.txt  # Core dependencies (NIVEAU 2)
├── requirements-minimal.txt  # Minimal test dependencies (NIVEAU 1)
└── requirements-models.txt  # ML model dependencies (NIVEAU 3)

frontend/
├── src/
│   ├── components/     # Reusable UI components
│   ├── services/       # API communication layer
│   ├── utils/          # Pure utility functions
│   └── pages/          # Page components
├── Dockerfile          # Production image
├── Dockerfile.dev      # Development image with hot reloading
└── tests/              # Frontend tests

tests/
├── backend/
│   ├── modelFree/      # Tests without ML dependencies (< 1s)
│   │   ├── conftest.py  # Fixtures with mock services
│   │   └── test_services/  # Service unit tests
│   └── FullStack/      # Integration tests with ML models
│       └── test_api_url_upload_integration.py
├── frontend/           # Component tests
└── local/              # Manual/development test scripts

docker-compose.dev.yml  # Development with hot reloading
docker-compose.test-modelFree.yml  # Fast tests (modelFree)
docker-compose.test-FullStack.yml  # Full integration tests
```

### Repository Separation
- **This repository (Marker-OCR-API)**: Development and testing only
  - Contains: dev/test docker-compose files, source code, test infrastructure
  - Does NOT contain: Production configuration, Traefik, SSL/TLS setup
- **Production repository (Marker-OCR-API-prod)**: Production deployment
  - Contains: Traefik reverse proxy, SSL/TLS, production docker-compose
  - Managed separately with different deployment workflow

## Code Standards

### Language Rules
- **Comments and Code**: Always in English
- **Chat Communication**: In French
- **Variable/Function Names**: English, descriptive, following conventions

### Python Backend
- Use FastAPI for API layer with async/await
- Pydantic Settings for configuration management (environment variables)
- Dependency injection pattern with singleton services (LRU cache)
- Lifespan management: Model initialization at startup, cleanup at shutdown
- Hot reload support: Handle CancelledError gracefully during development
- Type hints mandatory
- Max function length: 20 lines
- Max class length: 100 lines
- Follow PEP 8
- Structured logging with context (request IDs, operation tracking)
- Custom exception hierarchy (BaseAPIException) with proper HTTP status codes

### Frontend
- Modern JavaScript/TypeScript
- Component-based architecture
- Separation of concerns between UI and business logic
- Error boundaries for robust error handling

### Testing Architecture

#### Two-Tier Testing Strategy
1. **modelFree Tests** (Fast, < 1s):
   - Use `Dockerfile.test-modelFree` with `requirements-minimal.txt`
   - Mock services (`*_mock.py`) replace heavy dependencies
   - No ML model loading required
   - Located in `tests/backend/modelFree/`
   - Use `docker-compose.test-modelFree.yml`

2. **FullStack Tests** (Integration with ML):
   - Use `Dockerfile.test-FullStack` with all requirements
   - Real Marker library and ML models
   - For integration testing with actual PDF processing
   - Located in `tests/backend/FullStack/`
   - Use `docker-compose.test-FullStack.yml`

#### Testing Standards
- **Mandatory**: Unit tests for all business logic in services/
- **Mandatory**: Integration tests for API endpoints
- **Mandatory**: Component tests for frontend
- Test coverage minimum: 80%
- Use pytest for Python, Jest for JavaScript
- Mock services pattern: Environment-based switching (test vs production)
- Test fixtures: Use conftest.py for shared test setup
- Fast tests: Prefer modelFree for rapid development feedback

### Docker & DevOps

#### Docker Images Strategy
- **Dockerfile**: Production/dev image with all ML dependencies (requirements-base.txt + requirements-minimal.txt + requirements-models.txt)
- **Dockerfile.test-modelFree**: Lightweight test image (~30s build) with requirements-minimal.txt only
- **Dockerfile.test-FullStack**: Full test image with ML dependencies for integration tests
- **Dockerfile.dev** (frontend): Development image with hot module replacement

#### Docker Compose Files
- **docker-compose.dev.yml**: Development environment with hot reloading
  - Backend: uvicorn with --reload flag
  - Frontend: Vite dev server with HMR
  - Redis: Shared cache service
  - Volume mounts for live code editing
- **docker-compose.test-modelFree.yml**: Fast test execution (< 1s)
- **docker-compose.test-FullStack.yml**: Full integration tests with ML

#### Development Workflow
- Hot reloading: Backend (~1-2s), Frontend (~100ms)
- Volume mounting: Code changes reflected immediately
- Redis: Required service for caching/background tasks
- Network: Shared `marker-network` for service communication
- Health checks: All containers include health check endpoints

#### Requirements Management
- **requirements-base.txt** (NIVEAU 2): Core application dependencies
- **requirements-minimal.txt** (NIVEAU 1): Minimal dependencies for fast test builds
- **requirements-models.txt** (NIVEAU 3): ML model dependencies (heavy)
- Test images use minimal requirements for speed
- Production/dev images use all three levels

## File Organization

### Maximum File Sizes
- Python files: 200 lines maximum
- JavaScript files: 150 lines maximum
- Configuration files: 50 lines maximum

### Naming Conventions
- Files: snake_case for Python, kebab-case for frontend
- Classes: PascalCase
- Functions/Variables: camelCase (JS), snake_case (Python)
- Constants: UPPER_SNAKE_CASE

## Dependencies

### Core Dependencies
- **Backend**: FastAPI, Pydantic, Pydantic Settings, Marker library, Redis, pytest
- **Frontend**: React 18, Vite, Tailwind CSS, Jest, Testing Library
- **Infrastructure**: Docker, Docker Compose, Redis (for caching/background tasks)

### Service Architecture
- **Singleton Pattern**: Services use LRU cache for singleton instances
- **Dependency Injection**: FastAPI Depends() with get_* functions in dependencies.py
- **Service Cleanup**: Async cleanup functions called on application shutdown
- **Mock Services**: Parallel mock implementations (*_mock.py) for testing
  - Mock services mirror real service interfaces
  - Environment-based switching in test fixtures
  - In-memory storage for fast test execution

### Testing Optimizations
- **Lightweight test images**: Separate Docker images for testing without ML dependencies
- **Mock services**: Use mock implementations (document_parser_mock.py, file_handler_mock.py) for unit tests
- **Minimal requirements**: Test-specific requirements-minimal.txt for faster builds (~30s vs ~7min)
- **Two-tier testing**: modelFree for speed, FullStack for integration

### API Architecture
- **Route Organization**: Routes organized in `api/routes/` modules (health, documents)
- **API Versioning**: All routes prefixed with `/api/v1`
- **Middleware**: CORS, TrustedHost (production), request timing, request ID tracking
- **Lifespan Management**: Async context manager for startup/shutdown
  - Startup: Create directories, initialize Marker models
  - Shutdown: Cleanup services, handle CancelledError gracefully
- **Model Loading**: Pre-load Marker models at startup with progress tracking
- **Health Checks**: Comprehensive health endpoint with service status
- **OpenAPI**: Auto-generated docs at `/docs` (Swagger UI) and `/redoc`

### Prohibited Patterns
- God objects/classes
- Direct file system access from API layer
- Hardcoded configurations (use Pydantic Settings instead)
- Missing error handling
- Untested business logic
- Direct service instantiation in routes (use dependency injection)
- Synchronous I/O operations (use async/await)
- Missing type hints

## Documentation Standards

### Project Documentation
- **README.md**: Main project overview and quickstart
- **MAKEFILE_GUIDE.md**: Comprehensive Makefile command reference
- **QUICK_START.md**: 30-second setup guide
- **API Documentation**: Auto-generated from FastAPI (available at /docs)

### Documentation Maintenance
- Keep documentation in sync with code changes
- Update guides when new commands or features are added
- Maintain examples with current command syntax
- Include performance metrics and optimization tips

### Documentation Constraints
- **NO intermediate/work-in-progress documentation files** (e.g., HOTFIX_*.md, FIX_*.md, SOLUTION_*.md)
- **NO summary or status report files** unless explicitly requested by the user
- **Focus on code and essential documentation only**: README, guides, code comments
- When fixing issues: **code changes only**, no extra documentation unless asked
- If documentation is needed: update existing files (README, guides) instead of creating new ones

## Test Organization

**CRITICAL RULE**: All test-related files MUST be in `tests/` directory.

### Required Structure

✅ **ALLOWED**:
- `tests/TESTING.md` - Complete test documentation (centralized)
- `tests/pytest.ini` - Pytest configuration
- `tests/.gitignore` - Test artifacts
- `tests/backend/modelFree/` - Backend unit tests (fast, no ML)
- `tests/backend/FullStack/` - Backend integration tests (with ML)
- `tests/frontend/` - Frontend component tests (Jest)

❌ **FORBIDDEN**:
- Root `pytest.ini` - Must be in `tests/`
- Root `*TEST*.md` or `*TESTING*.md` - Must be in `tests/`
- `backend/test_*.py` - Must be in `tests/backend/`
- `frontend/src/*.test.jsx` - Must be in `tests/frontend/`
- `tests/local/` - Removed (no manual/local tests)

### File Naming

- Backend: `test_*.py` (pytest convention)
- Frontend: `*.test.jsx` or `*.spec.jsx` (Jest convention)

### Configuration

- `tests/pytest.ini` - Pytest configuration with marks
- `frontend/jest.config.js` - Points to `tests/frontend/`

### Enforcement

1. **Before creating a test**: Verify it's in `tests/` directory
2. **Before creating test docs**: Add to `tests/TESTING.md`
3. **Before committing**: Verify no test files outside `tests/`
4. **CI/CD**: Only tests in `tests/` are executed

### Complete Documentation

See `tests/TESTING.md` for:
- Complete test guide
- Architecture (modelFree vs FullStack)
- Pytest marks usage
- All commands
- Examples and best practices

## Update Policy

**IMPORTANT**: This .cursorrules file MUST be updated whenever:
- New architectural decisions are made
- Global application rules change
- New technology is adopted
- Code standards are modified
- Project structure changes

**CRITICAL**: The following documentation files MUST be updated when relevant changes occur:

### MAKEFILE_GUIDE.md Updates Required When:
- New Makefile commands are added or modified
- Docker optimization strategies change
- Test architecture is modified (e.g., new test images, mock services)
- Performance improvements are implemented
- New development workflows are established
- CI/CD pipeline changes affect available commands
- Build processes are optimized or restructured

### Other Documentation Updates:
- **README.md**: When project scope, installation, or main features change
- **QUICK_START.md**: When setup process is simplified or modified
- **API Documentation**: Automatically updated via FastAPI, manual review for breaking changes

The coding agent is responsible for updating this file to maintain consistency across the project.

## Error Handling
- Use structured exceptions with proper HTTP status codes
- Custom exception hierarchy: BaseAPIException with status_code and details
- Exception handlers: Custom handlers for BaseAPIException, HTTPException, ValidationError
- Log all errors with appropriate context (request ID, URL, method)
- Handle CancelledError gracefully during hot reload (debug level, don't fail)
- Graceful degradation for non-critical features (e.g., model loading failures don't block startup)
- User-friendly error messages in the frontend
- Error responses: Consistent ErrorResponse model with error, status_code, details

## Performance
- Async/await for I/O operations
- Efficient file handling for large documents
- Progress tracking for long-running operations (model loading state, job status)
- Resource cleanup after processing (lifespan shutdown handlers)
- Docker image optimization for development speed
- Separate test and production build strategies
- Request timing: X-Process-Time header added to all responses
- Request tracing: X-Request-ID header for request correlation
- Model initialization: Pre-load Marker models at startup (lifespan startup)
- Singleton services: LRU cache prevents redundant service instantiation
- Test performance: modelFree tests < 1s, FullStack tests for integration only 