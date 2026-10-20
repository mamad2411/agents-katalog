---
applyTo: "**/*.{ts,js}"
---

# Code Quality Guidelines

## Core Quality Commands
- **`npm run lint`** - Check for linting errors using ESLint with Airbnb TypeScript configuration
- **`npm run lint-fix`** - Automatically fix linting errors where possible
- **`npm run format`** - Format code using Prettier (printWidth: 120, trailingComma: all)
- **`npm run integration`** - Execute integration tests using Mocha, Chai, and Supertest
- **`npm run units`** - Execute unit tests for services and utilities
- **`npm run integration-tests-coverage`** - Run integration tests with nyc coverage reporting
- **`npm run services-units-coverage`** - Run unit tests with nyc coverage reporting

## Pre-commit Quality Gates
- **Husky pre-push hook** automatically runs linting and unit tests before pushing
- **Commitlint** enforces conventional commit message format
- All quality checks must pass before code can be merged

## Code Style Standards
- **ESLint Configuration**: Extends Airbnb TypeScript base, Prettier recommended
- **File Naming**: Use kebab-case for all files (enforced by unicorn/filename-case rule)
- **Interface Naming**: PascalCase without "I" prefix (enforced by @typescript-eslint/naming-convention)
- **String Quotes**: Double quotes only (enforced by @typescript-eslint/quotes)
- **Console Usage**: No console.log statements allowed in production code (use Logger instead)
- **Test Files**: Use .spec.ts suffix, excluded from unused-expressions rule

## TypeScript Quality
- **Strict Mode**: All TypeScript strict checks enabled
- **No Unused Variables**: Error on unused variables (argsIgnorePattern: "^_" for intentionally unused)
- **Decorator Support**: Experimental decorators enabled for dependency injection
- **Source Maps**: Inline source maps for better debugging

## Testing Quality Requirements
- **Coverage Reporting**: nyc configured for both unit and integration test coverage
- **Test Environment**: Mocha with TypeScript support, Chai assertions, Supertest for API testing
- **Test Structure**: Separate unit tests for services, integration tests for endpoints
- **No Test-Only**: Prevent .only() in test files (no-only-tests plugin)

## Documentation Standards
- **TSDoc Comments**: Use JSDoc-style comments for all public methods and classes
- **API Documentation**: Swagger/OpenAPI documentation in swagger/ directory
- **Feature Documentation**: Each feature should have clear purpose and usage documentation
- **Error Documentation**: Document all custom error types and their usage

## Health Monitoring
- **Health Endpoint**: `/health` endpoint returns 200 OK when application is healthy
- **Database Health**: Health checks should validate database connectivity
- **Service Dependencies**: Monitor external service availability in health checks

## Performance Standards
- **Build Performance**: Use SWC for faster TypeScript compilation in development
- **Bundle Analysis**: Regular analysis of build output size and dependencies
- **Memory Usage**: Monitor memory consumption in long-running processes
- **Response Times**: API endpoints should respond within acceptable time limits

## Security Quality
- **Dependency Scanning**: Regular security audits of npm packages
- **Input Validation**: All inputs validated using Celebrate/Joi schemas
- **Security Headers**: Helmet middleware for security headers
- **CORS Configuration**: Proper CORS setup for allowed origins

## Git Quality Standards
- **Conventional Commits**: Follow conventional commit format (enforced by commitlint)
- **Branch Naming**: Use descriptive branch names with feature/ or fix/ prefixes
- **Pull Request Quality**: Comprehensive PR descriptions with testing notes
- **Code Review**: All changes require code review before merging

## CI/CD Quality
- **Docker Containerization**: All services containerized for consistent environments
- **Pipeline Validation**: Automated quality checks in CI/CD pipelines
- **Environment Parity**: Development, staging, and production environment consistency
- **Deployment Verification**: Post-deployment health checks and smoke tests

## Quality Metrics
- **Code Coverage**: Maintain minimum coverage thresholds for unit and integration tests
- **Cyclomatic Complexity**: Monitor and reduce complex functions
- **Technical Debt**: Regular refactoring to address code smells and technical debt
- **Performance Metrics**: Track and optimize key performance indicators

## Development Workflow
1. **Before Coding**: Ensure local environment is up to date
2. **During Development**: Run tests frequently, use watch mode for immediate feedback
3. **Before Committing**: Run full quality suite (lint, format, tests)
4. **Before Pushing**: Verify all quality gates pass
5. **After Merging**: Monitor deployment and quality metrics

## Quality Tools Integration
- **SonarQube**: Static code analysis and quality metrics
- **nyc**: Test coverage reporting with LCOV format
- **Prettier**: Consistent code formatting
- **ESLint**: Code quality and style enforcement
- **TypeScript Compiler**: Type checking and compilation
- **Husky**: Git hooks for quality enforcement
