# API TB40 Project Rules

## Architecture Patterns
- **Data-Driven Logic**: Assessment logic, trait definitions, and questions MUST be stored in `api/:version/:type/calculation.json`.
- **Service Layer**: Business logic belongs in `services/`.
- **Middleware**: Validation and security logic belongs in `middleware/`.
- **Utilities**: Reusable helpers belong in `utils/`.

## Coding Standards
- **ES6+**: Use modern JavaScript features.
- **Async/Await**: Prefer async/await over callbacks or raw promises.
- **RESTful Principles**: Endpoints should follow `/api/:version/:type/...` structure.
- **Error Handling**: Use a centralized middleware for returning consistent JSON error responses.

## Testing Standards
- **Framework**: Use **Jest** and **Supertest**.
- **Coverage**: Maintain at least 80% coverage for services and utils.
- **Placement**: All tests belong in the `__tests__/` directory.

## Documentation
- **Markdown**: Use `devlog/` to track major changes and architectural decisions.
- **API Spec**: Prefer OpenAPI/Swagger for documenting endpoints.
- **Templates**: Handlebars is preferred for dynamic JSON/SVG generation.

## Performance
- **Compression**: Use compression for large SVG/JSON responses.
- **Rate Limiting**: Always apply rate limiting to public API endpoints.
