# Artify

Laravel 12+/13+, PHP 8.4+, MySQL
Platform to display independent artists and they work.

## Structure

```
app/
├── Exceptions/          # Custom domain and application exceptions
├── Livewire/            # Reactive UI components (server-driven frontend)
├── Http/
│   ├── Controllers/     # HTTP entry points; orchestrate requests and responses
│   ├── Middleware/      # Request/response pipeline and cross-cutting concerns
│   └── Requests/        # Form requests and input validation rules
├── Mail/                # Email classes, templates, and notifications
├── Models/              # Eloquent models and domain entities
├── Providers/           # Service container bindings and application bootstrapping
├── Repositories/        # Data access layer (database persistence and queries)
└── Services/            # Business logic and application use cases

database/
├── migrations/          # Database schema definitions and versioning
├── seeders/             # Development and test data population
└── factories/           # Model factories for generating test data

routes/
└── web.php              # Web route definitions and endpoint mappings

tests/
├── Feature/             # End-to-end and integration tests (HTTP, database, services)
└── Unit/                # Isolated tests for individual classes and methods
```

### Execution Flow

```
User
  ↓
/acc:plan
  ↓
tech-lead-architect
  ↓
Creates date-plan-title.md
  ↓
User approval
  ↓
/acc:implement
  ↓
code-executor
  ↓
Implements plan
  ↓
Runs tests & static analysis
  ↓
/acc:review
  ↓
code-reviewer
  ↓
Reviews architecture, security, performance and maintainability
  ↓
Generates date-plan-title-review.md
  ↓
User approval
  ↓
Merge
```

## Architecture
This application follows a layered MVC architecture:

Controllers handle HTTP requests and responses.
Services contain business logic and application use cases.
Repositories encapsulate data access and persistence concerns.
Models represent domain entities and database records.
Livewire Components implement interactive UI behavior.

## Request Flow
Request
→ Middleware
→ Request Validation
→ Controller
→ Service
→ Repository
→ Model / Database
→ Response

## Layer Responsibilities
Controllers should be thin and contain no business logic.
Services coordinate business rules and workflows.
Repositories are the only layer that communicates directly with the database.
Models should represent data and relationships, not application workflows.
Business logic should live in Services, not Controllers, Models, or Repositories.

See the app/ directory for the complete project structure.

## Tests
Run the full test suite:
```bash
php artisan test
```

## Conventions
# Design Principles
- Follow SOLID principles.
- Depend on abstractions, not concrete implementations.
- Keep business logic independent from framework, database, and infrastructure concerns.
- Favor explicit code over magic and hidden behavior.

# Class Design
- Keep classes small and focused on a single responsibility.
- Keep methods short and expressive.
- Use constructor dependency injection.
- Prefer immutable value objects when appropriate.
- Avoid static state and hidden side effects.

# Error Handling
- Use named domain exceptions for business rule violations.
- Never throw generic \Exception for domain logic.
- Fail fast and provide meaningful exception messages.

# Code Quality
- Write code for readability first.
- Favor clarity over cleverness.
- Follow DRY, but avoid premature abstraction.
- Optimize for maintainability rather than brevity.
- Leave the codebase simpler than you found it.

# Database Access
- Access the database through Repositories.
- Keep query logic out of Controllers and Services.
- Encapsulate persistence details behind repository interfaces.
