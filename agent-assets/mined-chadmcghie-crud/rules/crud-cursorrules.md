# Multi-Platform CRUD Application - Clean Architecture

## Project Overview
This is a comprehensive multi-platform application built with .NET 8 and Angular, following Clean Architecture principles. The solution includes multiple UI frontends (Angular web, .NET MAUI cross-platform) and comprehensive testing strategies.

## Architecture Principles
- **Clean Architecture**: Domain-centric design with clear layer separation
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Domain-Driven Design**: Rich domain models with business logic encapsulation
- **CQRS**: Command Query Responsibility Segregation using MediatR
- **Dependency Injection**: Constructor injection throughout all layers

## Solution Structure
```
src/
├── Domain/           # Core business logic and entities (no external dependencies)
├── App/             # Application layer with use cases and business workflows
├── Infrastructure/   # Data access, external services, cross-cutting concerns
├── Api/             # ASP.NET Core Web API (full-featured)
├── Api.Min/         # ASP.NET Core Minimal API (lightweight alternative)
├── Angular/         # Angular web frontend
├── Maui/            # .NET MAUI cross-platform mobile/desktop app
└── Shared/          # Shared utilities and components

test/
├── Tests.Unit.Backend/      # Backend unit tests (Domain, Application)
├── Tests.Integration.*/     # Integration tests for each layer
└── Tests.E2E.*/            # End-to-end tests for complete workflows
```

## Technology Stack
- **Backend**: .NET 8, Entity Framework Core, MediatR, AutoMapper
- **Frontend**: Angular 20+, TypeScript, RxJS, Angular Material
- **Mobile**: .NET MAUI with MVVM pattern
- **Testing**: xUnit, Moq, Playwright
- **Database**: In-memory (development), SQL Server/PostgreSQL (production)

## Development Guidelines

### Code Quality
- Follow established coding standards and conventions
- Use meaningful names that express business intent
- Implement proper error handling and logging
- Write comprehensive tests for all business logic
- Use async/await for all I/O operations
- Follow SOLID principles and avoid code smells

### Layer Dependencies
- **Domain**: No external dependencies (pure business logic)
- **Application**: Depends only on Domain abstractions
- **Infrastructure**: Implements Application and Domain interfaces
- **API/UI**: Depends on Application and Infrastructure through DI

### Testing Strategy
- **Unit Tests**: Fast, isolated tests for business logic (70% of tests)
- **Integration Tests**: Test component interactions and data access (20% of tests)
- **E2E Tests**: Test complete user workflows and critical paths (10% of tests)

### Security
- Implement proper input validation at all boundaries
- Use HTTPS for all communications
- Follow OWASP security guidelines
- Implement proper authentication and authorization
- Validate and sanitize all user inputs

### Performance
- Use appropriate caching strategies
- Implement proper database indexing
- Use async patterns to avoid blocking
- Optimize frontend bundle sizes
- Monitor and profile application performance

## Project-Specific Guidelines
Each project has its own `.cursorrules` file with specific guidelines:
- `src/Domain/.cursorrules` - Domain layer patterns and DDD guidelines
- `src/App/.cursorrules` - Application services and CQRS patterns
- `src/Infrastructure/.cursorrules` - Repository pattern and data access
- `src/Api/.cursorrules` - Web API controllers and HTTP concerns
- `src/Angular/.cursorrules` - Angular components, services, and reactive patterns
- `src/Maui/.cursorrules` - MVVM pattern and cross-platform considerations
- `test/Tests.*.cursorrules` - Testing strategies and patterns

## Getting Started
1. Clone the repository and open `Crud.sln`
2. Restore NuGet packages and npm dependencies
3. Review the documentation in the `docs/` directory
4. Follow the project-specific guidelines in each `.cursorrules` file
5. Run tests to ensure everything is working correctly

## Documentation
- [Big Picture](docs/01-overview/1-big-picture.md) - High-level overview
- [Architecture Guidelines](docs/02-architecture/1-architecture-guidelines.md) - Design principles
- [Testing Strategy](docs/04-quality-control/1-testing-strategy/1-testing-strategy.md) - Testing approach

## Contributing
1. Follow the established architecture patterns
2. Write tests for new features and bug fixes
3. Update documentation when making significant changes
4. Follow the coding standards defined in each layer
5. Ensure all tests pass before submitting changes

## Build and Deployment
- Use `dotnet build` for backend projects
- Use `ng build` for Angular frontend
- Use `dotnet publish` for production deployments
- Run `dotnet test` for all test projects
- Use the provided PowerShell scripts for automation
