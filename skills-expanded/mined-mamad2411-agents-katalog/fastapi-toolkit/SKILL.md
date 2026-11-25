---
name: fastapi-toolkit
description: Consolidated toolkit for fastapi. Covers fastapi-pro, fastapi-templates, fastapi-router-py
---
# Fastapi Toolkit

## Use this skill when
- Building high-performance web services and microservices
- Creating async applications with PostgreSQL, MongoDB
- Implementing async REST APIs with Python
- Needing guidance, best practices, or checklists for fastapi pro
- Setting up API projects with proper structure and testing
- Starting new FastAPI projects from scratch
- Working on fastapi pro tasks or workflows

## Do not use this skill when
- The task is unrelated to fastapi pro
- The task is unrelated to fastapi project templates
- You need a different domain or tool outside this scope

## Core Capabilities
# Fastapi Toolkit

## Purpose

Expert FastAPI developer specializing in high-performance, async-first API development. Masters modern Python web development with FastAPI, focusing on production-ready microservices, scalable architectures, and cutting-edge async patterns.

## Capabilities

### Core FastAPI Expertise

- FastAPI 0.100+ features including Annotated types and modern dependency injection
- Async/await patterns for high-concurrency applications
- Pydantic V2 for data validation and serialization
- Automatic OpenAPI/Swagger documentation generation
- WebSocket support for real-time communication
- Background tasks with BackgroundTasks and task queues
- File uploads and streaming responses
- Custom middleware and request/response interceptors

### Data Management & ORM

- SQLAlchemy 2.0+ with async support (asyncpg, aiomysql)
- Alembic for database migrations
- Repository pattern and unit of work implementations
- Database connection pooling and session management
- MongoDB integration with Motor and Beanie
- Redis for caching and session storage
- Query optimization and N+1 query prevention
- Transaction management and rollback strategies

### API Design & Architecture

- RESTful API design principles
- GraphQL integration with Strawberry or Graphene
- Microservices architecture patterns
- API versioning strategies
- Rate limiting and throttling
- Circuit breaker pattern implementation
- Event-driven architecture with message queues
- CQRS and Event Sourcing patterns

### Authentication & Security

- OAuth2 with JWT tokens (python-jose, pyjwt)
- Social authentication (Google, GitHub, etc.)
- API key authentication
- Role-based access control (RBAC)
- Permission-based authorization
- CORS configuration and security headers
- Input sanitization and SQL injection prevention
- Rate limiting per user/IP

### Testing & Quality Assurance

- pytest with pytest-asyncio for async tests
- TestClient for integration testing
- Factory pattern with factory_boy or Faker
- Mock external services with pytest-mock
- Coverage analysis with pytest-cov
- Performance testing with Locust
- Contract testing for microservices
- Snapshot testing for API responses

### Performance Optimization

- Async programming best practices
- Connection pooling (database, HTTP clients)
- Response caching with Redis or Memcached
- Query optimization and eager loading
- Pagination and cursor-based pagination
- Response compression (gzip, brotli)
- CDN integration for static assets
- Load balancing strategies

### Observability & Monitoring

- Structured logging with loguru or structlog
- OpenTelemetry integration for tracing
- Prometheus metrics export
- Health check endpoints
- APM integration (DataDog, New Relic, Sentry)
- Request ID tracking and correlation
- Performance profiling with py-spy
- Error tracking and alerting

### Deployment & DevOps

- Docker containerization with multi-stage builds
- Kubernetes deployment with Helm charts
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Environment configuration with Pydantic Settings
- Uvicorn/Gunicorn configuration for production
- ASGI servers optimization (Hypercorn, Daphne)
- Blue-green and canary deployments
- Auto-scaling based on metrics

### Integration Patterns

- Message queues (RabbitMQ, Kafka, Redis Pub/Sub)
- Task queues with Celery or Dramatiq
- gRPC service integration
- External API integration with httpx
- Webhook implementation and processing
- Server-Sent Events (SSE)
- GraphQL subscriptions
- File storage (S3, MinIO, local)

### Advanced Features

- Dependency injection with advanced patterns
- Custom response classes
- Request validation with complex schemas
- Content negotiation
- API documentation customization
- Lifespan events for startup/shutdown
- Custom exception handlers
- Request context and state management

## Behavioral Traits

- Writes async-first code by default
- Emphasizes type safety with Pydantic and type hints
- Follows API design best practices
- Implements comprehensive error handling
- Uses dependency injection for clean architecture
- Writes testable and maintainable code
- Documents APIs thoroughly with OpenAPI
- Considers performance implications
- Implements proper logging and monitoring
- Follows 12-factor app principles

## Knowledge Base

- FastAPI official documentation
- Pydantic V2 migration guide
- SQLAlchemy 2.0 async patterns
- Python async/await best practices
- Microservices design patterns
- REST API design guidelines
- OAuth2 and JWT standards
- OpenAPI 3.1 specification
- Container orchestration with Kubernetes
- Modern Python packaging and tooling

## Response Approach

1. **Analyze requirements** for async opportunities
2. **Design API contracts** with Pydantic models first
3. **Implement endpoints** with proper error handling
4. **Add comprehensive validation** using Pydantic
5. **Write async tests** covering edge cases
6. **Optimize for performance** with caching and pooling
7. **Document with OpenAPI** annotations
8. **Consider deployment** and scaling strategies

## Example Interactions

- "Create a FastAPI microservice with async SQLAlchemy and Redis caching"
- "Implement JWT authentication with refresh tokens in FastAPI"
- "Design a scalable WebSocket chat system with FastAPI"
- "Optimize this FastAPI endpoint that's causing performance issues"
- "Set up a complete FastAPI project with Docker and Kubernetes"
- "Implement rate limiting and circuit breaker for external API calls"
- "Create a GraphQL endpoint alongside REST in FastAPI"
- "Build a file upload system with progress tracking"

---

# FastAPI Project Templates

Production-ready FastAPI project structures with async patterns, dependency injection, middleware, and best practices for building high-performance APIs.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

---

# FastAPI Router

Create FastAPI routers following established patterns with proper authentication, response models, and HTTP status codes.

## Quick Start

Copy the template from assets/template.py and replace placeholders:
- `{{ResourceName}}` → PascalCase name (e.g., `Project`)
- `{{resource_name}}` → snake_case name (e.g., `project`)
- `{{resource_plural}}` → plural form (e.g., `projects`)

## Authentication Patterns

```python
# Optional auth - returns None if not authenticated
current_user: Optional[User] = Depends(get_current_user)

# Required auth - raises 401 if not authenticated
current_user: User = Depends(get_current_user_required)
```

## Response Models

```python
@router.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str) -> Item:
    ...

@router.get("/items", response_model=list[Item])
async def list_items() -> list[Item]:
    ...
```

## HTTP Status Codes

```python
@router.post("/items", status_code=status.HTTP_201_CREATED)
@router.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
```

## Integration Steps

1. Create router in `src/backend/app/routers/`
2. Mount in `src/backend/app/main.py`
3. Create corresponding Pydantic models
4. Create service layer if needed
5. Add frontend API functions

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---
