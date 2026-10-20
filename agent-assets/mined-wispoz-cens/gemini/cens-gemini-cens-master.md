# Development Guidelines for Go + Vue 3 + PostgreSQL Project

## Project Stack
- **Backend**: Go (Golang)
- **Frontend**: Vue 3 with Composition API
- **Styling**: Tailwind CSS v4
- **Database**: PostgreSQL
- **Documentation**: Context 7 format

---

## Core Development Principles

### 1. Backend Development (Go)

#### Follow Go Best Practices
- Use idiomatic Go code following the [Effective Go](https://go.dev/doc/effective_go) guidelines
- Organize code using standard Go project layout
- Use meaningful package names (lowercase, single word when possible)
- Prefer composition over inheritance
- Handle errors explicitly - never ignore errors
- Write clear, self-documenting code with appropriate comments for exported functions

#### Linters and Code Quality
- **Run linters BEFORE every build** - builds must not proceed with linting errors
- Use `golangci-lint` as the primary linter (combines multiple linters)
- Use `gofmt` for code formatting
- Use `goimports` for import organization
- Configure pre-commit hooks
- Run static analysis tools

**Required linters in `.golangci.yml`:**
```yaml
linters:
  enable:
    - errcheck      # Check for unchecked errors
    - gosimple      # Simplify code
    - govet         # Reports suspicious constructs
    - ineffassign   # Detect ineffectual assignments
    - staticcheck   # Advanced static analysis
    - unused        # Check for unused code
    - gocyclo       # Cyclomatic complexity
    - gofmt         # Format code
    - revive        # Fast linter
    - gosec         # Security issues
    - typecheck     # Type checking
```

**Build commands:**
```bash
# Run linters
golangci-lint run ./...

# Format code
gofmt -s -w .
goimports -w .

# Run tests
go test -v -race -cover ./...

# Build
go build -o app ./cmd/api
```

**Makefile example:**
```makefile
.PHONY: lint test build

lint:
	golangci-lint run ./...
	
format:
	gofmt -s -w .
	goimports -w .

test:
	go test -v -race -cover ./...

prebuild: lint test

build: prebuild
	go build -o app ./cmd/api
```

#### Scalability
The backend MUST be designed for horizontal scalability:

- **Stateless Design**
  - No session state stored in application memory
  - Use external session stores (Redis, PostgreSQL)
  - Enable running multiple instances behind a load balancer
  
- **Database Scalability**
  - Use connection pooling with appropriate limits
  - Implement read replicas for read-heavy operations
  - Use database migrations for schema changes
  - Design for eventual consistency where appropriate
  - Implement caching strategies (Redis, in-memory cache)
  
- **Concurrency**
  - Use goroutines and channels for concurrent operations
  - Implement worker pools for background jobs
  - Use context for cancellation and timeouts
  - Avoid shared mutable state
  
- **Performance**
  - Implement pagination for list endpoints
  - Use database indexes appropriately
  - Implement rate limiting
  - Use caching for frequently accessed data
  - Optimize database queries (avoid N+1 queries)
  
- **Observability**
  - Implement health check endpoints (`/health`, `/ready`)
  - Export metrics (Prometheus format)
  - Use distributed tracing (OpenTelemetry)
  - Implement structured logging with correlation IDs
  
**Example scalable service:**
```go
type Config struct {
    MaxDBConnections int
    CacheEnabled     bool
    WorkerPoolSize   int
}

type Service struct {
    db     *sql.DB
    cache  *redis.Client
    logger *zerolog.Logger
    pool   *WorkerPool
}

func (s *Service) ProcessInParallel(ctx context.Context, items []Item) error {
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()
    
    sem := make(chan struct{}, s.config.WorkerPoolSize)
    errCh := make(chan error, len(items))
    
    for _, item := range items {
        sem <- struct{}{}
        go func(item Item) {
            defer func() { <-sem }()
            if err := s.processItem(ctx, item); err != nil {
                errCh <- err
            }
        }(item)
    }
    
    // Wait for all goroutines
    for i := 0; i < cap(sem); i++ {
        sem <- struct{}{}
    }
    
    close(errCh)
    return <-errCh
}
```

#### Test-Driven Development (TDD)
- **ALWAYS write tests BEFORE implementation**
- Follow the Red-Green-Refactor cycle:
  1. Write a failing test (Red)
  2. Write minimal code to pass the test (Green)
  3. Refactor while keeping tests green (Refactor)
- Aim for high test coverage (minimum 80%)
- Use table-driven tests where appropriate
- Test files should be named `*_test.go`
- Write unit tests, integration tests, and end-to-end tests
- Mock external dependencies using interfaces

#### SOLID Principles
- **S - Single Responsibility**: Each struct/function should have one reason to change
- **O - Open/Closed**: Open for extension, closed for modification
- **L - Liskov Substitution**: Interfaces should be substitutable
- **I - Interface Segregation**: Keep interfaces small and focused
- **D - Dependency Inversion**: Depend on abstractions, not concretions

#### Domain-Driven Design (DDD)
Structure the project using DDD layers:

```
project/
├── cmd/                    # Application entry points
├── internal/
│   ├── domain/            # Domain layer (entities, value objects, domain services)
│   ├── application/       # Application layer (use cases, DTOs)
│   ├── infrastructure/    # Infrastructure layer (repositories, external services)
│   └── interfaces/        # Interface layer (HTTP handlers, gRPC, CLI)
├── pkg/                   # Reusable packages
└── tests/                 # Integration and E2E tests
```

- **Entities**: Core business objects with identity
- **Value Objects**: Immutable objects without identity
- **Aggregates**: Clusters of entities and value objects
- **Repositories**: Abstract data access
- **Services**: Domain logic that doesn't fit in entities
- **Use Cases**: Application-specific business rules

#### Clean Code & Clean Architecture
- Use meaningful variable and function names
- Keep functions small and focused (ideally < 20 lines)
- Avoid deep nesting (max 3 levels)
- Use early returns to reduce complexity
- Separate business logic from infrastructure concerns
- Dependencies point inward (domain has no external dependencies)
- Use dependency injection for better testability

#### Error Handling and Logging
- **Handle ALL errors explicitly**
- Never use `panic()` in production code except for truly unrecoverable errors
- Use custom error types for domain-specific errors
- Wrap errors with context using `fmt.Errorf("context: %w", err)`
- Implement structured logging using a logger like `zerolog` or `zap`
- Log at appropriate levels:
  - `DEBUG`: Detailed diagnostic information
  - `INFO`: General informational messages
  - `WARN`: Warning messages for potentially harmful situations
  - `ERROR`: Error events that might still allow the app to continue
  - `FATAL`: Severe errors that cause application termination
- Include relevant context in logs (user ID, request ID, trace ID)
- Log errors immediately when they occur
- Create centralized error handling middleware
- Store logs for analysis and monitoring

**Example error handling:**
```go
func (s *UserService) GetUser(ctx context.Context, id string) (*domain.User, error) {
    user, err := s.repo.FindByID(ctx, id)
    if err != nil {
        s.logger.Error().
            Err(err).
            Str("user_id", id).
            Msg("failed to retrieve user from repository")
        return nil, fmt.Errorf("get user: %w", err)
    }
    return user, nil
}
```

---

### 2. Frontend Development (Vue 3)

#### Vue 3 Best Practices
- Use Composition API with `<script setup>` syntax
- Organize components by feature, not by type
- Keep components small and focused (< 300 lines)
- Use composables for reusable logic
- Use Pinia for state management
- Follow Vue style guide (priority A and B rules)

#### TypeScript
- **ALWAYS use TypeScript** - no plain JavaScript
- Enable strict mode in `tsconfig.json`
- Define proper types and interfaces for all data structures
- Avoid using `any` type - use `unknown` if type is truly unknown
- Use type guards for runtime type checking
- Define props and emits with proper typing
- Use generic types where appropriate
- Create shared type definitions in `types/` directory

**Example TypeScript usage:**
```typescript
// types/user.ts
export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'user'
  createdAt: Date
}

// composables/useUser.ts
import type { Ref } from 'vue'
import type { User } from '@/types/user'

export function useUser() {
  const user: Ref<User | null> = ref(null)
  
  const fetchUser = async (id: string): Promise<User> => {
    // Implementation
  }
  
  return { user, fetchUser }
}
```

#### Linters and Code Quality
- **Run linters BEFORE every build** - builds must not proceed with linting errors
- Use ESLint for code quality
- Use Prettier for code formatting
- Configure pre-commit hooks with Husky
- Use Vue-specific ESLint plugins (`eslint-plugin-vue`)
- Configure TypeScript ESLint parser

**Required ESLint configuration:**
```json
{
  "extends": [
    "plugin:vue/vue3-recommended",
    "@vue/typescript/recommended",
    "prettier"
  ],
  "rules": {
    "vue/multi-word-component-names": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn"
  }
}
```

**Build script in package.json:**
```json
{
  "scripts": {
    "lint": "eslint . --ext .vue,.ts,.tsx --max-warnings 0",
    "format": "prettier --write \"src/**/*.{vue,ts,tsx,json}\"",
    "type-check": "vue-tsc --noEmit",
    "prebuild": "npm run lint && npm run type-check",
    "build": "vite build"
  }
}
```

#### Tailwind CSS v4
- Use Tailwind utility classes exclusively
- Avoid custom CSS unless absolutely necessary
- Use Tailwind's design tokens for consistency
- Leverage Tailwind's responsive modifiers (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`)
- Use Tailwind's color palette
- Extract repeated patterns into components, not custom CSS classes
- Configure Tailwind properly in `tailwind.config.js`

#### Design Principles
- **Clean and Minimalistic Design**
  - Use generous white space
  - Limit color palette (2-3 primary colors max)
  - Use consistent typography scale
  - Maintain visual hierarchy
  - Avoid clutter and unnecessary elements
  
- **Responsive Design**
  - Mobile-first approach
  - Test on multiple screen sizes (320px to 2560px)
  - Use responsive Tailwind utilities
  - Ensure touch targets are minimum 44x44px
  - Optimize images for different screen sizes
  - Implement responsive navigation patterns

**Example responsive component:**
```vue
<template>
  <div class="container mx-auto px-4 sm:px-6 lg:px-8">
    <h1 class="text-2xl sm:text-3xl lg:text-4xl font-bold">
      Responsive Title
    </h1>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <!-- Content -->
    </div>
  </div>
</template>
```

---

### 3. Documentation

#### Context 7 Format
Use Context 7 format for all documentation and code generation:

```markdown
# Context
[Describe the current situation, problem, or feature]

# Goals
[List specific, measurable objectives]

# Technical Details
[Relevant technical information, constraints, dependencies]

# Implementation Plan
[Step-by-step approach]

# Testing Strategy
[How to verify the implementation]

# Acceptance Criteria
[Conditions that must be met]

# Open Questions
[Unresolved issues or clarifications needed]
```

---

### 4. Communication and Clarification

#### Always Ask Before Implementing
Before implementing ANY feature, ask 3-4 clarifying questions:

**Example questions:**
1. What is the expected behavior when [edge case scenario]?
2. Should this feature be available to all users or specific roles?
3. What are the performance requirements (response time, concurrent users)?
4. Are there any specific validation rules or business constraints?
5. What should happen if the operation fails?
6. Do we need to maintain backward compatibility?
7. Are there any security considerations for this feature?

#### When Uncertain
- **ALWAYS ask for clarification rather than making assumptions**
- Request examples or mockups for UI features
- Ask about edge cases and error scenarios
- Clarify acceptance criteria
- Confirm technical constraints (performance, scalability, security)

---

### 5. Database (PostgreSQL)

#### Best Practices
- Use migrations for schema changes (e.g., `golang-migrate`)
- Index frequently queried columns
- Use transactions for multi-step operations
- Use prepared statements to prevent SQL injection
- Implement connection pooling
- Use JSONB for flexible schema needs
- Follow naming conventions (snake_case for tables and columns)
- Add appropriate constraints (NOT NULL, UNIQUE, CHECK)

#### Repository Pattern
```go
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*domain.User, error)
    Save(ctx context.Context, user *domain.User) error
    Update(ctx context.Context, user *domain.User) error
    Delete(ctx context.Context, id string) error
}
```

---

### 6. Docker & Container Orchestration

#### Docker Requirements
**EVERYTHING must run in Docker containers** - no local installations required.

#### Docker Compose Structure
All services must be defined in `docker-compose.yml`:

```yaml
version: '3.8'

services:
  # Backend API
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: app-api
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/appdb
      - REDIS_URL=redis://cache:6379
      - ENV=development
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - ./backend:/app
      - /app/vendor  # Exclude vendor directory
    command: go run cmd/api/main.go
    networks:
      - app-network
    restart: unless-stopped

  # Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: app-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules  # Exclude node_modules
    command: npm run dev
    networks:
      - app-network
    restart: unless-stopped

  # PostgreSQL Database
  db:
    image: postgres:16-alpine
    container_name: app-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=appdb
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./database/migrations:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d appdb"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network
    restart: unless-stopped

  # Redis Cache
  cache:
    image: redis:7-alpine
    container_name: app-cache
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - app-network
    restart: unless-stopped

  # Nginx (Production)
  nginx:
    image: nginx:alpine
    container_name: app-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - api
      - frontend
    networks:
      - app-network
    restart: unless-stopped
    profiles:
      - production

volumes:
  postgres-data:
  redis-data:

networks:
  app-network:
    driver: bridge
```

#### Dockerfile Best Practices

**Backend Dockerfile (Multi-stage build):**
```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install dependencies
RUN apk add --no-cache git make

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Run linters
RUN go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
RUN golangci-lint run ./...

# Run tests
RUN go test -v -race ./...

# Build binary
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main ./cmd/api

# Runtime stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

# Copy binary from builder
COPY --from=builder /app/main .

# Expose port
EXPOSE 8080

# Run
CMD ["./main"]
```

**Frontend Dockerfile (Multi-stage build):**
```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Run linters and type checking
RUN npm run lint
RUN npm run type-check

# Build for production
RUN npm run build

# Runtime stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose Commands
**ALL commands MUST be executed through docker compose:**

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d api

# View logs
docker compose logs -f api
docker compose logs -f frontend

# Execute commands in containers
docker compose exec api go test ./...
docker compose exec api golangci-lint run ./...
docker compose exec api go run cmd/migrate/main.go up

docker compose exec frontend npm run lint
docker compose exec frontend npm run type-check
docker compose exec frontend npm test

# Access database
docker compose exec db psql -U user -d appdb

# Access Redis
docker compose exec cache redis-cli

# Rebuild specific service
docker compose build api
docker compose up -d --build api

# Stop all services
docker compose down

# Stop and remove volumes
docker compose down -v

# Scale services (for load testing)
docker compose up -d --scale api=3

# View running containers
docker compose ps

# Execute migration
docker compose exec api ./migrate -path /migrations -database "$DATABASE_URL" up

# Run database backup
docker compose exec db pg_dump -U user appdb > backup.sql

# Restore database
docker compose exec -T db psql -U user appdb < backup.sql
```

#### Development Workflow with Docker

**Daily development commands:**
```bash
# Morning startup
docker compose up -d

# Check logs during development
docker compose logs -f api frontend

# Run tests
docker compose exec api go test -v ./...
docker compose exec frontend npm test

# Run linters before committing
docker compose exec api golangci-lint run ./...
docker compose exec frontend npm run lint

# Database migrations
docker compose exec api make migrate-up
docker compose exec api make migrate-down

# Access database for debugging
docker compose exec db psql -U user -d appdb

# Restart service after config changes
docker compose restart api

# Rebuild after dependency changes
docker compose build api
docker compose up -d api

# End of day cleanup
docker compose down
```

#### Production Deployment
```bash
# Build production images
docker compose -f docker-compose.prod.yml build

# Start production stack
docker compose -f docker-compose.prod.yml up -d

# Run health checks
docker compose exec api curl http://localhost:8080/health

# View production logs
docker compose -f docker-compose.prod.yml logs -f

# Scale API instances
docker compose -f docker-compose.prod.yml up -d --scale api=5
```

#### Docker Best Practices
- Use multi-stage builds to reduce image size
- Run linters and tests in build stage (fail fast)
- Use `.dockerignore` to exclude unnecessary files
- Never run containers as root in production
- Use specific image versions, not `latest` tag
- Implement health checks for all services
- Use volumes for persistent data only
- Use named volumes for better management
- Keep containers stateless and ephemeral
- Use environment variables for configuration
- Implement proper logging to stdout/stderr
- Use Docker secrets for sensitive data in production

**.dockerignore example:**
```
.git
.gitignore
.env
.env.local
node_modules
dist
coverage
*.log
tmp
vendor
.vscode
.idea
```

#### Required Makefile Commands
Create a `Makefile` in the project root:

```makefile
.PHONY: help up down restart logs build test lint clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services
	docker compose up -d

down: ## Stop all services
	docker compose down

restart: ## Restart all services
	docker compose restart

logs: ## Show logs (use service=<name> for specific service)
	docker compose logs -f $(service)

build: ## Build all services
	docker compose build

test-api: ## Run backend tests
	docker compose exec api go test -v -race -cover ./...

test-frontend: ## Run frontend tests
	docker compose exec frontend npm test

lint-api: ## Run backend linters
	docker compose exec api golangci-lint run ./...

lint-frontend: ## Run frontend linters
	docker compose exec frontend npm run lint
	docker compose exec frontend npm run type-check

lint: lint-api lint-frontend ## Run all linters

test: test-api test-frontend ## Run all tests

migrate-up: ## Run database migrations
	docker compose exec api make migrate-up

migrate-down: ## Rollback database migrations
	docker compose exec api make migrate-down

db-shell: ## Access database shell
	docker compose exec db psql -U user -d appdb

redis-shell: ## Access Redis shell
	docker compose exec cache redis-cli

clean: ## Remove all containers, volumes, and images
	docker compose down -v --rmi all

reset: clean up ## Clean and restart everything
```

---

### 7. Git Workflow

#### Commit Messages
Follow conventional commits format:
```
type(scope): subject

body

footer
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example:**
```
feat(auth): implement JWT token refresh mechanism

- Add refresh token generation
- Implement token rotation
- Add tests for token expiration

Closes #123
```

#### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Urgent production fixes

---

### 8. Code Review Checklist

Before submitting code for review:
- [ ] All tests pass (unit, integration, E2E)
- [ ] Test coverage meets minimum threshold (80%)
- [ ] Code follows SOLID principles
- [ ] Error handling is comprehensive
- [ ] Logging is implemented appropriately
- [ ] Documentation is updated
- [ ] Code is formatted (`gofmt`, Prettier)
- [ ] No hard-coded values (use configuration)
- [ ] Security vulnerabilities checked
- [ ] Performance optimized
- [ ] Mobile responsiveness verified
- [ ] **All linters pass without errors** (golangci-lint, ESLint)
- [ ] **TypeScript compilation successful** (no type errors)
- [ ] **Docker build completes successfully**
- [ ] **All services start correctly with docker compose**
- [ ] **Environment variables documented** in `.env.example`
- [ ] **Multi-stage Docker builds used** (optimized image size)
- [ ] **.dockerignore configured properly**

---

### 9. Development Workflow Example

**TDD Workflow for a new feature:**

1. **Understand Requirements**: Ask clarifying questions
2. **Start Docker Environment**: 
   ```bash
   docker compose up -d
   ```
3. **Write Test**: Create failing test
   ```bash
   # For backend
   docker compose exec api go test ./internal/domain/user -v
   
   # For frontend
   docker compose exec frontend npm test -- user.spec.ts
   ```
4. **Implement**: Write minimal code to pass test
5. **Run Linters**:
   ```bash
   docker compose exec api golangci-lint run ./...
   docker compose exec frontend npm run lint
   docker compose exec frontend npm run type-check
   ```
6. **Refactor**: Improve code while keeping tests green
7. **Verify Tests Still Pass**:
   ```bash
   docker compose exec api go test -v -race -cover ./...
   docker compose exec frontend npm test
   ```
8. **Document**: Add Context 7 documentation
9. **Review**: Self-review using checklist
10. **Commit**: Use conventional commit format
11. **Cleanup**:
    ```bash
    docker compose down
    ```

---

## Quick Reference

### Backend Structure
```
internal/
├── domain/
│   ├── user/
│   │   ├── user.go          # Entity
│   │   ├── user_test.go     # Tests first!
│   │   └── repository.go    # Interface
│   └── ...
├── application/
│   ├── user/
│   │   ├── create_user.go   # Use case
│   │   └── create_user_test.go
│   └── ...
└── infrastructure/
    ├── persistence/
    │   └── postgres/
    │       ├── user_repository.go
    │       └── user_repository_test.go
    └── ...
```

### Frontend Structure
```
src/
├── components/
│   ├── common/
│   └── features/
├── composables/
├── views/
├── stores/
├── router/
└── utils/
```

---

## Remember

1. **Tests first, always** - No production code without tests
2. **Ask questions** - Better to clarify than assume (3-4 questions before implementing)
3. **Handle errors** - Every error must be handled and logged
4. **Keep it clean** - Simple, readable, maintainable code
5. **Mobile matters** - Always responsive, always tested
6. **Document** - Use Context 7 format
7. **SOLID & DDD** - Architecture matters
8. **TypeScript only** - No plain JavaScript in frontend
9. **Linters must pass** - No builds without clean linter output
10. **Everything in Docker** - All commands via `docker compose exec`
11. **Design for scale** - Stateless, horizontally scalable backend
12. **Pre-commit checks** - Run linters and tests before every commit

---

## Resources

- [Effective Go](https://go.dev/doc/effective_go)
- [Vue 3 Style Guide](https://vuejs.org/style-guide/)
- [Tailwind CSS v4 Documentation](https://tailwindcss.com)
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [golangci-lint](https://golangci-lint.run/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [The Twelve-Factor App](https://12factor.net/) - Scalable app methodology