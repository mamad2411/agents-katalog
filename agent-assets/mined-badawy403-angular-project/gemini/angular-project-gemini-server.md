# Express.js Backend Guidelines


## Key Principles
- Minimalist and unopinionated design
- Middleware-first architecture
- Fully asynchronous request handling
- Modular and feature-based structure
- Strong separation of concerns
- Production-ready robustness over simplicity

---

## Architecture
- Layered Architecture (Controller → Service → Repository)
- Feature-based modular structure (each domain is self-contained)
- Optional Use Case / Application Layer for complex business logic
- DTO layer for input/output data shaping
- Environment-based configuration management with validation (dotenv )


## Middleware
- Custom middleware for reusable logic
- Centralized error-handling middleware (4-parameter signature)
- Async middleware wrapper to avoid try/catch repetition
- Third-party middleware:
    - helmet (security headers)
    - cors (cross-origin control)
    - morgan or pino-http (logging)
    - express-rate-limit (rate limiting)
- Request validation middleware
- Authentication & authorization middleware (RBAC-ready)

---

## Routing
- express.Router() for modular routing
- RESTful conventions for endpoint design
- Route grouping by feature/domain
- API versioning (/api/)
- Clean separation between routes and controllers
- Standardized request/response flow

---

## API Design Standards
- Consistent response format:
    - success, data, error, meta , code
- Pagination, filtering, and sorting conventions
- Idempotent endpoints where required (especially payments)
- Proper HTTP status code usage
- Predictable error structure

---

## Security
- Helmet for HTTP headers protection
- Rate limiting per user/IP
- Input sanitization and validation (Zod/Joi)
- CORS strict configuration
- HTTP Parameter Pollution protection (HPP)
- JWT with refresh token rotation (if authentication exists)
- Role-Based Access Control (RBAC)
- Optional OAuth2/social login abstraction

---

## Observability
- Structured logging (prefer Pino over Winston)
- Request correlation / trace ID per request
- Centralized error tracking (e.g., Sentry)
- Metrics collection
- Health checks (/health, /ready endpoints)


---

## Developer Experience (DX)
- ESLint + Prettier configuration
- Pre-commit hooks (Husky + lint-staged)
- Absolute imports support
- Database migrations and seeders support
- Clean project structure with scalability in mind

---

## Best Practices
- Prefer async/await over callbacks
- Avoid business logic inside controllers
- Handle all errors centrally
- Validate input as early as possible
- Use meaningful HTTP status codes
- Keep services pure and testable
- Avoid tight coupling between layers