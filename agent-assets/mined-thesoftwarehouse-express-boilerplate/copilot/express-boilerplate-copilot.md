# Coding Guidelines for Node.js/TypeScript Boilerplate

## Project Overview

This repository is a boilerplate for building Node.js applications using TypeScript, following best practices and architectural patterns. It is designed to be a starting point for new projects, providing a solid foundation with modern development tools and methodologies.

## Code Architecture

### Key Patterns
- **CQRS (Command Query Responsibility Segregation)**: Separates read and write operations for better scalability and maintainability.
- **Dependency Injection**: Uses Awilix for managing dependencies, promoting loose coupling and easier testing.
- **Event-driven architecture**: Utilizes an event dispatcher for handling domain events, enabling asynchronous processing and decoupling of components.
- **Feature-based structure**: Organizes code into features, each encapsulating related functionality, making it easier to navigate and maintain.
- **RESTful API**: Exposes a RESTful API for client interactions, following standard HTTP methods and status codes.
- **GraphQL API**: Apollo Server integration for GraphQL queries and mutations alongside REST endpoints.

### Project Structure
```src/
├── app/
│   ├── features/          # Feature-based organization
│   │   ├── [feature-name]/ # Each feature has its own directory
│   │   │   ├── actions/          # REST endpoint handlers
│   │   │   ├── commands/         # State-changing DTOs
│   │   │   ├── queries/          # Data-retrieval DTOs
│   │   │   ├── handlers/         # Command/query business logic
│   │   │   ├── query-handlers/   # Query business logic
│   │   │   ├── events/           # Domain events
│   │   │   ├── subscribers/      # Event listeners
│   │   │   ├── graphql/          # GraphQL resolvers
│   │   │   ├── models/           # TypeORM entities
│   │   │   └── routing.ts        # Route definitions
│   ├── infrastructure/    # Infrastructure code (e.g., repositories implementations)
│   ├── config/            # Configuration files
│   ├── container/         # Dependency injection container setup
│   ├── errors/            # Custom error classes
│   ├── shared/            # Shared utilities and helpers
│   ├── tests/             # Integration tests files
│   │   └── bootstrap.ts   # Test bootstrap file
│   ├── migrations/      # TypeORM migrations
│   ├── router.ts        # Registering all feature routes
│   └── app.ts           # Express app setup and initialization, application routing setup
├── index.ts           # Application entry point
└── container.ts       # Dependency injection container setup
```

### Key Libraries and Functionalities
- **TypeScript**: For static typing and modern JavaScript features.
- **Express**: Web framework for building REST APIs.
- **Apollo Server**: GraphQL server implementation for building GraphQL APIs.
- **TypeORM**: ORM for database interactions with PostgreSQL.
- **Awilix**: Dependency injection container for managing dependencies.
- **@tshio/command-bus**: Command bus for handling commands in CQRS pattern.
- **@tshio/query-bus**: Query bus for handling queries in CQRS pattern.
- **@tshio/event-dispatcher**: Event dispatcher for handling domain events.
- **Celebrate**: Request validation middleware using Joi schemas.
- **Helmet**: Security middleware for setting HTTP headers.
- **CORS**: Cross-origin resource sharing middleware.
- `src/shared/pagination-utils`: Utility functions for request parameters to TypeORM options conversion and list endpoint responses.
- `src/shared/cache-decorator`: Caching utilities for query optimization.
- `src/shared/utils`: Common utility functions for various operations.
- **UUID v4**: For unique identifiers in database entities.
- **Docker**: For containerization and consistent development environment.
- **Mocha + Chai + Supertest**: Testing framework stack for unit and integration tests.
- **SWC**: Fast TypeScript/JavaScript transpiler (alternative to tsc).
- **ESLint + Prettier**: Code quality and formatting tools.
- **Husky**: Git hooks for pre-commit quality checks.

### Key Development Guidelines

#### Important Commands
- **Development Environment**: Use `npm run watch` to start TypeScript compilation in watch mode and `npm start` to run the API server
- **Building**: Use `npm run build` (tsc) or `npm run build-swc` (SWC transpiler) to compile TypeScript
- **Linting**: Use `npm run lint` to check code style and `npm run lint-fix` to automatically fix issues
- **Formatting**: Use `npm run format` to format code using Prettier
- **Testing**: Use `npm run integration` for integration tests and `npm run units` for unit tests
- **Test Coverage**: Use `npm run integration-tests-coverage` and `npm run services-units-coverage` for coverage reports
- **Database Migrations**: Use `npm run generate-migration` to create new migrations
- **Running Migrations**: Use `npm run run-migrations` to execute pending migrations
- **GraphQL Schema**: Use `npm run generate-schema` to generate GraphQL type definitions
- **Docker Management**: Use `npm run down` to stop all containers and volumes

#### Development Workflow
1. **Initial Setup**: Run `./init.sh` or manual Docker setup for first-time environment preparation
2. **Development**: Start `npm run watch` for TypeScript compilation and `npm start` for the API server (in separate terminals)
3. **Code Quality**: Run `npm run lint-fix` and `npm run format` before committing changes
4. **Testing**: Execute `npm run integration` and `npm run units` to ensure all tests pass
5. **Database Changes**: Generate migrations with `npm run generate-migration` after model updates
6. **Pre-commit**: Husky hooks automatically run linting and unit tests before git push

#### General Guidelines
- Always use TypeScript for type safety and modern JavaScript features
- Follow the project's coding conventions and architectural patterns
- Use dependency injection for managing dependencies, avoiding direct instantiation of classes
- All environment variables must be extracted and validated using `dotenv` and `joi` packages in `src/config/app.ts`
- Store environment configuration in `.env` (local) and `.env.test` (testing), use `.env.dist` as template
- Never use `npm run plop` to generate code, create files manually following the established patterns
- Use Docker containers for all development operations - avoid running commands directly on host machine
- All database migrations are auto-executed at application start, do not run them manually
- Follow the detailed instruction files for specific development patterns:
  - Actions: REST endpoint implementation patterns
  - Handlers: Command/Query handler implementation
  - Models: Entity and repository patterns
  - Routing: Route registration and middleware
  - Tests: Testing requirements and patterns
  - Quality: Code quality standards and tools
  - Security: Security best practices and implementation

#### Naming Guidelines
- Always think in terms of features, not technical layers
- Feature names should be descriptive and reflect the bounded context (e.g., `user-management`, `order-processing`, `notification-service`)
- Avoid naming features by connected entities alone (e.g., avoid just `user`, prefer `user-management`)
- Use **kebab-case** for directories, filenames and imports (e.g., `user-controller.ts`, `create-user.command.ts`)
- Use **camelCase** for variables and function names (e.g., `getUserById`, `processOrder`)
- Use **PascalCase** for class names and interfaces (e.g., `UserService`, `OrderRepository`, `CreateUserCommand`)
- Use **snake_case** for database columns and TypeORM entity properties (e.g., `first_name`, `created_at`)
- Use descriptive suffixes for file types:
  - `.action.ts` for REST endpoint handlers
  - `.handler.ts` for command/query handlers
  - `.command.ts` for command DTOs
  - `.query.ts` for query DTOs
  - `.event.ts` for domain events
  - `.subscriber.ts` for event subscribers
  - `.resolver.ts` for GraphQL resolvers
  - `.entity.ts` for TypeORM entities
  - `.repository.ts` for repository implementations
- Use descriptive suffixes for class names (e.g., `UserService`, `OrderRepository`, `CreateUserHandler`)

#### Database Guidelines
- Use **TypeORM** for database interactions
- Use **UUID v4** for unique identifiers, avoid auto-increment IDs
- Use repositories for data access in handlers, not direct TypeORM queries
- Always generate migrations using the provided npm script (`npm run generate-migration`), do not create them manually
- Never add parameters to the `npm run generate-migration` command, as it will fail
- All migrations are auto-executed at application start, do not run them manually
- Migrations are stored in `src/migrations/`

#### Testing Guidelines
- Every endpoint must have a corresponding integration test
- Every utility function must have a corresponding unit test

#### Security Guidelines
- Never expose sensitive information in error messages or responses
- Use HTTPS for secure communication, especially in production environments

## When Adding Features

1. Define domain model in appropriate bounded context
2. Create commands/queries with handlers
3. Add repository interfaces and implementations  
4. Wire up event subscribers for cross-context communication
5. Register all components in DI container
6. Add validation and error handling
7. Write integration tests following existing patterns

Focus on maintaining clean boundaries between domain, application, and infrastructure layers while leveraging the established CQRS and event-driven patterns.
