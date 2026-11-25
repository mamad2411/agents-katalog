# UCarpool Development Structure and Rules

## Project Architecture

- **Full-stack carpooling app** for University of Utah students
- **Backend**: FastAPI with PostgreSQL, Poetry dependency management
**Frontend**: Native Swift iOS app (primary), Expo/React Native (deprecated - reference only)- 
**Infrastructure**: Docker Compose for development environment

## Backend Structure (FastAPI + PostgreSQL)

- **Main entry**: `Backend/main.py` with FastAPI app, WebSocket support, CORS middleware
- **Database**: SQLAlchemy ORM with Alembic migrations in `Backend/database/`
- **API Routes**: Modular routers in `Backend/routers/` (login, signup, routes, request, user, ride, strikes, message, pickup, drop_off)
- **Database Queries**: Separate query modules in `Backend/queries/` for data access layer
- **Dependencies**: Poetry for package management (`pyproject.toml`)
- **Testing**: Pytest with async support, comprehensive test coverage in `Backend/__tests__/`
- **Authentication**: Firebase integration with utah.edu email verification
- **External APIs**: Google Maps, Stripe payments, WebSocket real-time features

## Frontend Structure

- **Native iOS Frontend**: Swift iOS app in `UCarpool_iOS/` (PRIMARY - all new development)
  - **Framework**: Native Swift with SwiftUI
  - **Architecture**: MVVM pattern with Services layer
  - **Caching**: Multi-layer caching with Keychain, FileManager, NSCache
  - **Storage**: Keychain for tokens, FileManager for API responses, UserDefaults for preferences
  - **Build**: Xcode project for iOS deployment
  - **Glass Features**: Actively developing glass morphism UI features (visionOS/glass design)
    - Glass features are a priority and should be added wherever possible
    - Glass versions of features will likely replace non-glass versions
    - When implementing new features, prefer glass morphism design patterns
    - Glass features take precedence over traditional iOS UI when both are possible

- **Expo/React Native Frontend**: `Frontend/` (DEPRECATED - reference only)
  - **Status**: Deprecated - no new development
  - **Purpose**: Reference implementation for API contracts, data structures, and business logic
  - **Use Case**: Consult when building native iOS features to understand API endpoints and data models
  - **DO NOT**: Create new features or fix bugs in Expo app unless explicitly requested for reference purposes

- **Web Frontend**: React web app in `FrontendWeb/` (only work on when explicitly specified)


## Development Tools and Patterns

- **Package Management**: Poetry (Backend), npm (Frontend - deprecated), Xcode (iOS)
- **Testing**: Pytest (Backend), Jest (Frontend - deprecated), Xcode tests (iOS)
- **Database**: PostgreSQL with async SQLAlchemy, Alembic migrations
- **Containerization**: Docker Compose for local development
- **Code Quality**: TypeScript (deprecated), Swift (iOS), async/await patterns, proper error handling
- **Real-time**: WebSocket connections for live tracking
- **Security**: JWT tokens, Firebase auth, CORS middleware

## Key Development Rules

0. **Development Focus and Backward Compatibility**:
   - **PRIMARY FOCUS**: We are actively developing the **Backend API (FastAPI)** and **Native iOS app (Swift)**
   - **NO BACKWARD COMPATIBILITY REQUIRED**: The project has no users yet, so agents should NOT worry about maintaining backward compatibility
   - **Breaking Changes**: Breaking API changes, schema migrations, and iOS app updates are acceptable and expected during active development
   - **Migration Strategy**: When making breaking changes, focus on clean, modern implementations rather than maintaining legacy support
   - **Versioning**: API versioning and deprecation warnings are not necessary at this stage
   - **Data Loss**: Database migrations that require data loss or restructuring are acceptable if they improve the architecture
   - **Client Updates**: iOS app updates that require API changes are fine - assume the app and API can be updated together

0.5. **Glass Features Priority**:
   - **Glass Morphism UI**: Actively add glass morphism design features wherever possible in the iOS frontend
   - **Replacement Strategy**: Glass versions of features will likely replace non-glass versions - this is expected and acceptable
   - **Design Preference**: When implementing new UI features, prefer glass morphism design patterns over traditional iOS UI
   - **No Duplication Needed**: Don't maintain both glass and non-glass versions - glass features can replace existing implementations
   - **Modern UI**: Focus on creating beautiful, modern glass morphism interfaces that enhance the user experience

1. **Modular Architecture**:
   - Separate routers, queries, and components
   - Routers handle HTTP logic, queries handle database logic
   - NEVER call ORM directly from routers - always use query functions

2. **Async Patterns**:
   - Use async/await throughout backend
   - ALL router endpoints MUST be async functions
   - ALL database operations MUST use async SQLAlchemy
   - ALL I/O operations (API calls, file operations) MUST be async

3. **Type Safety**:
   - Swift strict typing for iOS frontend   
   - Complete type hints for all Python functions
   - Pydantic models for all request/response validation
   - NO `any` types in TypeScript (deprecated frontend)

4. **Testing**:
   - Minimum 80% test coverage for backend
   - ALL new endpoints must have integration tests
   - ALL new query functions must have unit tests
   - Tests must use async/await patterns matching production code

5. **Database**:
   - Use query modules for data access, not direct ORM calls
   - ALL database operations MUST be in `Backend/queries/` modules
   - Routers MUST call query functions, never access database directly

6. **Authentication**:
   - Firebase + utah.edu email verification required
   - ALL protected endpoints MUST use `Depends(get_current_user)` or `Depends(get_current_user_id)`
   - NEVER skip authentication checks

7. **Real-time Features**:
   - WebSocket for location tracking and messaging
   - Use `websocket_manager` for managing connections

8. **Mobile-First Development**:
   - **DEFAULT FOCUS**: Always prioritize native iOS frontend (`UCarpool_iOS/`) unless explicitly told otherwise
   - Native Swift iOS app is the primary development target
   - **Expo/React Native**: The `Frontend/` directory is deprecated and should only be used as a reference for API contracts and data structures when building native iOS features
   - **Web Frontend**: Only work on web frontend (`FrontendWeb/`) when explicitly specified by the user
   - When user requests frontend work without specifying "web", assume native iOS frontend is intended

9. **Frontend Styling**:
   - **ALWAYS use the UCarpool theme** for all styling in frontend files
   - **React Native (Frontend/)**: Import theme from `../constants/theme` or appropriate relative path
     - Use `theme.colors.*` for all colors (NEVER hardcode hex colors or color names)
     - Use `theme.spacing.*` for all spacing/padding/margin values
     - Use `theme.borderRadius.*` for all border radius values
     - Use `theme.typography.*` for all font sizes and weights
     - Use `theme.shadows.*` for all shadow styles
     - Example: `backgroundColor: theme.colors.primary`, `padding: theme.spacing.md`, `borderRadius: theme.borderRadius.lg`
   - **Web Frontend (FrontendWeb/)**: Use Tailwind classes that reference the theme (theme is integrated into Tailwind config)
     - Prefer theme-based Tailwind classes: `bg-primary`, `text-primary`, `border-primary`, etc.
     - Use theme spacing: `p-md`, `m-lg`, etc. (as configured in Tailwind)
     - Use theme border radius: `rounded-md`, `rounded-lg`, etc.
     - If custom styles are needed, import theme from `src/constants/theme` and use theme values
   - **NEVER use hardcoded colors, spacing, or other style values** - always reference the theme
   - **Exception**: Only use hardcoded values for truly dynamic/calculated styles (e.g., `width: .infinity`, `frame(maxWidth: .infinity)`)

10. **Code Readability**:
    - **ALWAYS favor readability over brevity** when there's a trade-off
    - Use descriptive variable names over short abbreviations
    - Break complex expressions into multiple lines with intermediate variables
    - Add comments for non-obvious logic, especially business rules
    - Prefer explicit code over clever one-liners
    - Use early returns to reduce nesting and improve readability
    - Format code with proper spacing and line breaks for clarity

11. **DRY Principles (Don't Repeat Yourself)**:
    - **Extract repeated code** when the same logic appears **more than twice** (3+ occurrences)
    - **Only extract if there's a sensible, descriptive name** that clearly communicates the function's purpose
    - **DO NOT abstract** if the extracted function name would be vague or generic (e.g., `doStuff()`, `processData()`, `handleThing()`)
    - **Balance DRY with readability**: If extracting makes the code harder to understand, prefer slight repetition
    - **Good extraction examples**: `validateUtahEmail()`, `formatRouteDate()`, `calculateAvailableSeats()`, `sendRideNotification()`
    - **Bad extraction examples**: `process()`, `handle()`, `doWork()`, `helper()` - these names don't explain what the function does
    - **When in doubt, favor readability over DRY** - clear, slightly repetitive code is better than abstract, hard-to-understand code
    - **Exception**: Always extract validation logic, error handling patterns, and data transformations that appear multiple times, even if only twice

12. **Git Commit Reminders**:
    - **ALWAYS suggest a git commit** when it seems like an appropriate time to commit changes
    - **Appropriate times to suggest commits**:
      - After completing a feature or significant functionality
      - After fixing a bug or resolving an issue
      - After completing a refactoring or code improvement
      - After making multiple related changes that form a logical unit
      - Before switching to a different task or feature
      - After passing tests or completing validation
    - **How to suggest commits**:
      - Propose the git commit command with a meaningful commit message
      - Use `git add` to stage relevant files (or `git add .` if all changes are related)
      - Use `git commit -m "descriptive message"` with a clear, concise message
      - **NEVER commit without user approval** - always propose the command and wait for user confirmation
      - The user will approve the command before it runs
    - **Commit message guidelines**:
      - Use clear, descriptive messages that explain what was changed and why
      - Follow conventional commit format when appropriate (e.g., "feat:", "fix:", "refactor:")
      - Keep messages concise but informative
      - Examples: "feat: add glass morphism UI to login screen", "fix: resolve authentication token refresh issue", "refactor: extract route validation logic into separate function"
    - **DO NOT suggest commits**:
      - For trivial changes like fixing typos or formatting (unless explicitly requested)
      - When work is clearly incomplete or broken
      - When the user explicitly says not to commit

## File Organization Patterns

- **Backend**: `routers/` for API endpoints, `queries/` for database operations, `__tests__/` for tests
- **Frontend**: `app/` for screens, `components/` for UI, `services/` for API calls
- **Shared**: Environment variables, Docker configuration, comprehensive testing setup

## Development Workflow

- **Backend Development**: Use Poetry for dependencies, pytest for testing, async/await patterns
- **Frontend Development**: Use Xcode for native iOS, Expo CLI for reference (deprecated)
- **Database**: Use Alembic for migrations, query modules for data access
- **Real-time**: WebSocket connections for live location tracking
- **Testing**: Comprehensive coverage with both unit and integration tests
- **Deployment**: Docker Compose for local development, Xcode for iOS deployment

### Frontend Linting and Type Checking

- **Native iOS (UCarpool_iOS/)**:
  - Use Xcode's built-in Swift compiler for type checking
  - Build the project in Xcode to verify compilation
  - Follow Swift style guidelines and best practices
  - Ensure all code compiles without warnings or errors
  - **AUTOMATIC LINT CHECK**: When modifying any Swift file in `UCarpool_iOS/`, ALWAYS run the iOS build check to verify compilation:
    - Command: `cd UCarpool_iOS && xcodebuild -project UCarpool.xcodeproj -scheme UCarpool -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' build 2>&1 | grep -E "(error:|warning:|BUILD SUCCEEDED|BUILD FAILED)"`
    - **When to run**: After creating, modifying, or deleting any `.swift` file in `UCarpool_iOS/`
    - **NEVER skip the iOS build check** - always verify compilation before considering the task complete
    - **Fix all compilation errors** before considering the task complete
    - If the build fails, fix the errors and rebuild until `BUILD SUCCEEDED` is shown
    - **Note**: This uses a generic iOS Simulator destination for lint checking only. Physical device builds should be done through Xcode when needed.
- **Expo/React Native (Frontend/)**: DEPRECATED - no longer maintained
- **Web Frontend (FrontendWeb/)**:
  - Lint: `npm run lint` (from `FrontendWeb/` directory)
  - Type check: `npm run build` includes type checking, or use `tsc --noEmit` directly
  - When checking a file, run BOTH lint and type-check: `npm run lint && tsc --noEmit`
  - **When to run lint/type-check**:
    - After creating or modifying any frontend TypeScript/TSX file
    - Before committing frontend changes
    - When the agent wants to verify code quality
  - **NEVER skip linting or type checking** - always run both commands together
  - **Fix all linting errors** before considering the task complete
  - **Fix all type errors** before considering the task complete
  
## Code Quality Standards

### Documentation Requirements

- **Router Endpoints**: ALL router endpoints MUST have docstrings with:
  - Description of what the endpoint does
  - Args section listing all parameters with types
  - Returns section describing response structure
  - Raises section listing possible HTTP exceptions
  - Example:
    ```python
    """
    Create a new route for the authenticated driver.

    Args:
        request: FastAPI request object
        pickup_str: Pickup location name/address
        db: Database session
        current_user: Authenticated user from Firebase token

    Returns:
        CreateRouteResponse: The created route with ID and status

    Raises:
        HTTPException: 400 if validation fails, 500 if route creation fails
    """
    ```

- **Query Functions**: ALL query functions MUST have docstrings explaining:
  - What the function does
  - Parameters and their types
  - Return value and type
  - Any exceptions that may be raised

- **Complex Logic**: ALL complex logic MUST have inline comments explaining the "why", not just the "what"

- **Type Hints**: ALL public functions/classes MUST have complete type hints

### Security Requirements (CRITICAL)

- **NEVER hardcode API keys, tokens, passwords, or secrets in source code**
  - Use environment variables only (e.g., `process.env.EXPO_PUBLIC_GOOGLE_MAPS_KEY`)
  - If a fallback is needed, it MUST be a placeholder like `"your_api_key_here"` that will fail in production
  - Example of BAD code: `const API_KEY = "AIzaSy..."` ❌
  - Example of GOOD code: `const API_KEY = process.env.API_KEY || ""` ✅

- **ALL API endpoints MUST be authenticated** using `Depends(get_current_user)` or `Depends(get_current_user_id)`

- **Sensitive data MUST be encrypted** at rest and in transit

- **Input validation**: ALWAYS validate all user inputs using Pydantic models

- **Error messages**: NEVER expose internal error details in production responses (use `config.BACKEND_DEBUG_LOGGING` to control detail level)

### Error Handling Standards

- **ALWAYS use `handle_router_error()` utility** from `utils.error_handling` for non-HTTP exceptions:
  ```python
  try:
      # ... code ...
  except HTTPException:
      raise  # Re-raise HTTPExceptions as-is
  except Exception as e:
      raise handle_router_error(e, 'function_name', 500)
  ```

- **ALWAYS return appropriate HTTP status codes**:
  - 400: Bad Request (validation errors, invalid input)
  - 401: Unauthorized (missing or invalid authentication)
  - 403: Forbidden (authenticated but not authorized)
  - 404: Not Found (resource doesn't exist)
  - 500: Internal Server Error (unexpected server errors)

- **ALWAYS log errors with context** before returning to client:
  ```python
  logger.error(f"Error in {context}: {error}", exc_info=True)
  ```

### Testing Requirements

- **ALL new router endpoints MUST have integration tests** in `Backend/__tests__/routers/`
- **ALL new query functions MUST have unit tests** in `Backend/__tests__/queries/`
- **Test coverage MUST be maintained at minimum 80%** for backend code
- **ALL tests MUST use async/await patterns** matching production code
- **Test files MUST follow naming convention**: `test_<module_name>.py`

### Backend Testing Design Patterns

When writing backend tests, **ALWAYS follow the established testing architecture and patterns** already incorporated in the codebase:

#### Test Organization Structure

- **Unit Tests** (`Backend/__tests__/unit/`): Test individual functions and components in isolation
- **Integration Tests** (`Backend/__tests__/integration/`): Test component interactions and database operations
- **Router Tests** (`Backend/__tests__/routers/`): Test API endpoints with mocked dependencies
- **Query Tests** (`Backend/__tests__/queries/`): Test database query functions with real database operations
- **Acceptance Tests** (`Backend/__tests__/acceptance/`): Test complete user workflows and end-to-end scenarios

#### Fixtures and Test Setup

- **ALWAYS use existing fixtures** from `Backend/__tests__/conftest.py`:
  - `test_engine`: Async database engine with table creation/cleanup
  - `db_session`: Async SQLAlchemy session with automatic cleanup (TRUNCATE CASCADE)
  - `client`: TestClient with database dependency override
  - `simple_client`: TestClient with mocked auth (use for router tests)
  - `mocked_db_client`: Fully mocked client (use when database not needed)
  - `sample_user_data`, `sample_route_data`, `sample_vehicle_data`: Test data factories
  - `mock_user`: Standard mock user for authentication
  - `isolate_dependency_overrides`: Auto-isolation fixture (runs automatically)

- **For acceptance tests**, use fixtures from `Backend/__tests__/acceptance/conftest.py`:
  - `postgres_container`: PostgreSQL Docker container for real database testing
  - `test_engine`: PostgreSQL-based engine for acceptance tests
  - `db_session`: Session with PostgreSQL connection
  - `client`: TestClient with PostgreSQL database

- **For router tests**, use `Backend/__tests__/routers/conftest.py` for path setup

#### Test Data and Factories

- **Use test data factories** from `Backend/__tests__/utils/factories.py` when creating complex test data:
  - `UserFactory`, `VehicleFactory`, `RouteFactory`, etc.
  - Factories use factory_boy for realistic test data generation

- **Generate unique test data** to avoid conflicts:
  - Use `uuid.uuid4()` for unique emails: `f"test_{uuid.uuid4().hex[:8]}@gcloud.utah.edu"`
  - Use `get_test_email()` helper function when available
  - Use `factory.Faker()` in factories for realistic data

#### Async Testing Patterns

- **ALL tests MUST be async** and use `@pytest.mark.asyncio` or `pytest_asyncio`:
  ```python
  @pytest.mark.asyncio
  async def test_example(db_session: AsyncSession):
      # Test code here
  ```

- **Use `AsyncMock`** for mocking async functions:
  ```python
  from unittest.mock import AsyncMock
  mock_function = AsyncMock(return_value=result)
  ```

- **Use `pytest_asyncio.fixture`** for async fixtures:
  ```python
  @pytest_asyncio.fixture(scope="function")
  async def my_fixture():
      # Setup
      yield value
      # Teardown
  ```

#### Mocking Patterns

- **Firebase is automatically mocked** via `conftest.py` - no need to manually mock Firebase auth
- **Use `@patch` decorators** for mocking external dependencies:
  ```python
  @patch("routers.routes.get_user_id_by_email", new_callable=AsyncMock, return_value=1)
  @patch("routers.routes.is_driver", new_callable=AsyncMock, return_value=True)
  def test_example(self, mock_is_driver, mock_get_user_id, simple_client):
      # Test code
  ```

- **Use dependency overrides** for FastAPI dependencies:
  ```python
  from dependencies import get_current_user
  from main import app
  
  def mock_get_current_user():
      return {"uid": "test-user-id", "email": "test@gcloud.utah.edu", "email_verified": True}
  
  app.dependency_overrides[get_current_user] = mock_get_current_user
  ```

- **ALWAYS clean up dependency overrides** - the `isolate_dependency_overrides` fixture handles this automatically

#### Test Isolation and Cleanup

- **Tests MUST be isolated** - each test should run independently without side effects
- **Database cleanup is automatic** via `db_session` fixture (TRUNCATE CASCADE after each test)
- **Dependency overrides are isolated** via `isolate_dependency_overrides` fixture (runs automatically)
- **Use `scope="function"`** for all fixtures to ensure fresh state per test
- **Tests can run in any order** - no test should depend on another test's state

#### Test Structure and Organization

- **Use class-based organization** for related tests:
  ```python
  class TestRoutesRouter:
      """Test routes router endpoints."""
      
      @pytest.mark.asyncio
      async def test_create_route_success(self, simple_client):
          """Test creating a route successfully."""
          # Test code
  ```

- **Use descriptive test names**: `test_<action>_<scenario>` (e.g., `test_create_route_success`, `test_create_route_not_driver`)

- **Include docstrings** explaining what each test validates:
  ```python
  def test_example(self, client):
      """Test that creating a route returns 201 status code."""
      # Test code
  ```

#### Test Assertions and Validation

- **Assert HTTP status codes** explicitly:
  ```python
  assert response.status_code == status.HTTP_201_CREATED
  ```

- **Validate response structure** and content:
  ```python
  response_data = response.json()
  assert "id" in response_data
  assert response_data["status"] == "ACTIVE"
  ```

- **Test error cases** with appropriate status codes:
  ```python
  assert response.status_code == status.HTTP_403_FORBIDDEN
  assert response.json()["detail"] == "User is not authorized to access this route."
  ```

#### Acceptance Test Patterns

- **Acceptance tests** should test complete user workflows:
  - Use real PostgreSQL database (via `postgres_container` fixture)
  - Test end-to-end scenarios (e.g., create route → receive request → accept → complete)
  - Use `@pytest.mark.acceptance` marker
  - Test multi-user scenarios and complex interactions

- **Example acceptance test structure**:
  ```python
  @pytest.mark.acceptance
  @pytest.mark.route_lifecycle
  async def test_complete_route_lifecycle(self, client, db_session, sample_route_data):
      """Test complete route lifecycle: create -> publish -> receive requests -> modify -> cancel."""
      # Step-by-step workflow testing
  ```

#### Query Test Patterns

- **Query tests** should use real database operations:
  - Use `db_session` fixture for database access
  - Test actual SQLAlchemy operations, not mocks
  - Verify database state changes
  - Test edge cases and error conditions

- **Example query test structure**:
  ```python
  @pytest.mark.asyncio
  async def test_create_route_by_id(self, db_session):
      """Test creating a route with driver ID."""
      driver = User(email="driver@gcloud.utah.edu", name="Driver", role=RoleEnum.DRIVER)
      db_session.add(driver)
      await db_session.commit()
      
      route = await create_route_by_id(db_session, driver.id, route_data)
      assert route.driver_id == driver.id
  ```

#### Router Test Patterns

- **Router tests** should focus on HTTP layer:
  - Use `simple_client` or `mocked_db_client` fixtures
  - Mock query functions and business logic
  - Test authentication, authorization, validation
  - Test error handling and status codes

- **Example router test structure**:
  ```python
  @patch("routers.routes.create_route_by_id", new_callable=AsyncMock)
  def test_create_route_success(self, mock_create_route, simple_client):
      """Test creating a route successfully."""
      mock_route = MagicMock()
      mock_route.id = 1
      mock_create_route.return_value = mock_route
      
      response = simple_client.post("/routes", data=route_data)
      assert response.status_code == status.HTTP_201_CREATED
  ```

#### Best Practices

- **Reference existing tests** in `Backend/__tests__/` when writing new tests to maintain consistency
- **Use existing fixtures** rather than creating new ones unless absolutely necessary
- **Follow the established patterns** for test organization, naming, and structure
- **Test both success and failure cases** for all endpoints and functions
- **Use appropriate test markers** (`@pytest.mark.acceptance`, `@pytest.mark.integration`, etc.)
- **Keep tests focused** - each test should validate one specific behavior
- **Use meaningful assertions** that clearly indicate what is being tested

### Code Quality Patterns

- **User ID Lookup**: ALWAYS use `Depends(get_current_user_id)` instead of manually looking up user_id:
  ```python
  # BAD: Manual lookup
  user_id = await get_user_id_by_email(db, current_user["email"])

  # GOOD: Use dependency
  async def endpoint(user_id: int = Depends(get_current_user_id)):
      # user_id is already available
  ```

- **Rate Limiting**: ALWAYS use rate limiting decorators on public endpoints:
  ```python
  @user_limiter.limit("20/minute")
  async def endpoint(...):
      ...
  ```

- **Request Validation**: ALWAYS validate request data with Pydantic models (FastAPI does this automatically)

- **TODO Comments**: NEVER commit TODO comments without creating an issue/ticket. If a TODO is necessary, format it as:
  ```python
  # TODO(#123): Description of what needs to be done
  ```

### Terminal Commands

- **PowerShell Usage**: ALWAYS use PowerShell commands when running terminal commands on Windows
  - Use PowerShell syntax (e.g., `Get-ChildItem` instead of `ls`, `Set-Location` instead of `cd` when appropriate)
  - Use PowerShell operators (e.g., `-and`, `-or`, `-not` instead of `&&`, `||`, `!`)
  - Use PowerShell environment variable syntax: `$env:VARIABLE_NAME` instead of `$VARIABLE_NAME` or `%VARIABLE_NAME%`
  - Use PowerShell path separators: `/` or `\` (PowerShell handles both, but prefer `/` for cross-platform compatibility)
  - For multi-line commands, use PowerShell line continuation with backtick `` ` `` or semicolons `;`
  - When chaining commands, use PowerShell operators: `;` for sequential execution, `|` for piping, `&&` and `||` are available in PowerShell 7+
  - Use PowerShell-native commands when available (e.g., `Test-Path` instead of `test -f`)

### General Standards

- **Code Reviews**: All changes must be reviewed by team
- **Version Control**: Proper Git workflow with meaningful commit messages
- **Line Endings**: ALL files written by agents MUST use LF (Line Feed) line endings, never CRLF (Carriage Return + Line Feed). This ensures consistency across platforms and prevents Git diff issues.

## File Creation Rules

- **NEVER create .md files or scripts unless absolutely necessary**:
  - **Markdown files (`.md`)**: DO NOT create unless explicitly requested by the user or required for project setup (e.g., existing README.md)
  - **Shell scripts (`.sh`, `.ps1`, `.bat`)**: DO NOT create unless explicitly requested by the user
  - **Documentation files**: DO NOT create unless explicitly requested
  - **Setup scripts**: DO NOT create unless explicitly requested
  - **Configuration templates**: DO NOT create unless explicitly requested

- **When are .md files or scripts "absolutely necessary"?**
  - User explicitly requests them
  - Required for project setup (e.g., existing README.md that needs updating)
  - Part of a critical workflow that cannot be done without them
  - Required by a framework or tool (e.g., package.json scripts)

- **Code Files**: Can be created directly when implementing features
- **Test Files**: Can be created when adding new functionality
- **Configuration Files**: Only create if required for functionality (e.g., package.json, tsconfig.json)

- **Temporary Scripts and Analysis Files**:
  - **ALWAYS delete temporary scripts** created for one-time analysis, debugging, or testing after completing the task
  - **ALWAYS delete unrequested .md files** created during analysis or investigation (unless explicitly requested by user)
  - Examples of files to delete:
    - Scripts created to analyze code (e.g., `check_circular_imports.py`, `analyze_dependencies.py`)
    - Temporary analysis markdown files (e.g., `API_CONSISTENCY_ANALYSIS.md`, `DEPENDENCY_REPORT.md`)
    - One-time utility scripts that were only needed for a specific task
  - **Exception**: Keep scripts/files if the user explicitly asks to keep them or if they're part of the permanent project structure
