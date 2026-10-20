---
name: core-standards
description: Universal standards for all SmartWorkz code (applies to all files)
alwaysApply: true
---

# SmartWorkz Core Standards

You are an expert AI assistant embedded in SmartWorkz Technologies.

## Stack

- **Backend**: .NET 8, ASP.NET Core, C# 12, Dapper, FluentValidation
- **Frontend**: Angular 17+, TypeScript strict mode, DevExtreme, RxJS
- **Database**: SQL Server 2022, T-SQL, stored procedures
- **Infrastructure**: Azure DevOps, AWS, Docker
- **Testing**: xUnit, Moq, FluentAssertions, Playwright

## Language Requirements

### C#

**ALWAYS**:
- Use C# 12 features (primary constructors, collection expressions)
- Prefer `async`/`await` with `CancellationToken` parameters
- Use `ILogger<T>`, never `Console.Write`
- Enable `#nullable enable` at top of every file

**NEVER**:
- `Thread.Sleep()` — always `await Task.Delay()`
- Leave TODO comments in generated code
- Expose raw exceptions to API consumers
- Hardcode secrets or connection strings
- Use `var` for ambiguous types (be explicit)

### TypeScript

**ALWAYS**:
- Use `strict: true` in `tsconfig.json`
- Type all function parameters and return values
- Use `const` over `let`, never `var`
- Use modern async/await, not `.then()` chains

**NEVER**:
- Use `any` type (use `unknown` then narrow)
- Leave unused imports
- Skip null checks (`obj?.property` before `.property`)

## API Design

### Controllers / Endpoints

**ALWAYS**:
- Return `ProblemDetails` (RFC 7807) on error
- Use versioning: `api/v1/[controller]`
- Include `[ApiController]` attribute
- Document all public endpoints with XML docs

**NEVER**:
- Return raw exceptions
- Use 200 OK for errors
- Skip `Content-Type` headers

### DTOs

**ALWAYS**:
- Separate DTOs from domain models
- Validate at boundary (FluentValidation)
- Include all `[Required]`, `[StringLength]` attributes
- Use `record` for immutable DTOs (C# 12)

**NEVER**:
- Return domain entities directly
- Mix DB models with API contracts
- Skip field validation

## Error Handling

**ALWAYS**:
- Catch specific exceptions, not `catch (Exception)`
- Log exception details before rethrowing
- Return structured error responses
- Include correlation IDs in logs

**NEVER**:
- Expose stack traces to clients
- Swallow exceptions silently
- Log sensitive data (passwords, tokens, PII)

## Logging

**ALWAYS**:
- Use `ILogger<T>` injected via DI
- Use semantic logging (structured properties):
  ```csharp
  logger.LogError("User {UserId} failed login attempt {AttemptCount}", userId, count);
  ```
- Log at appropriate levels: Error, Warning, Information, Debug

**NEVER**:
- Log passwords, API keys, tokens, PII
- Use string concatenation in log messages
- Log inside loops without sampling

## Security

**ALWAYS**:
- Parameterize all SQL queries
- Validate and sanitize all user input
- Use `[Authorize]` on protected endpoints
- Store secrets in configuration (not in code)
- Use HTTPS for all external calls

**NEVER**:
- Hardcode secrets
- Trust user input
- Skip authentication/authorization
- Build SQL strings via concatenation

## Testing

**ALWAYS**:
- Write tests for new features
- Use test naming: `MethodName_Scenario_ExpectedResult`
- Include happy path, edge cases, null inputs, exceptions
- Mock external dependencies (HTTP, DB, services)

**NEVER**:
- Test private methods (test behavior, not implementation)
- Use real databases in unit tests (use mocks)
- Create flaky tests (avoid `Thread.Sleep`)

## Naming Conventions

### C#

| What | Convention | Example |
|------|-----------|---------|
| Namespaces | PascalCase | `SmartWorkz.Services.Users` |
| Classes | PascalCase | `UserService` |
| Methods | PascalCase | `GetUserAsync` |
| Properties | PascalCase | `UserId` |
| Local vars | camelCase | `userId` |
| Constants | UPPER_SNAKE | `MAX_RETRIES` |
| Interfaces | IPascalCase | `IUserService` |
| Async methods | PascalCaseAsync | `GetUserAsync` |

### TypeScript / Angular

| What | Convention | Example |
|------|-----------|---------|
| Files | kebab-case | `user-list.component.ts` |
| Classes | PascalCase | `UserListComponent` |
| Interfaces | IPascalCase | `IUser` |
| Methods | camelCase | `getUser()` |
| Properties | camelCase | `userId` |
| CSS classes | sw-kebab-case | `.sw-user-card` |
| CSS (BEM) | `.sw-block__element--modifier` | `.sw-card__header--active` |

### SQL

| What | Convention | Example |
|------|-----------|---------|
| Procedures | usp_FeatureName | `usp_GetUserById` |
| Views | vw_FeatureName | `vw_ActiveUsers` |
| Tables | PascalCase | `Users`, `Roles` |
| Columns | PascalCase | `UserId`, `CreatedDate` |
| Indexes | ix_TableColumn | `ix_Users_Email` |

## Documentation

**ALWAYS**:
- Add XML docs to all public types, methods, properties
- Include `<summary>`, `<param>`, `<returns>`, `<exception>`
- Add `<example>` for utility methods
- Keep docs up-to-date when code changes

**NEVER**:
- Leave docs as placeholders
- Document trivial methods
- Commit code without class-level docs

## Code Style

**ALWAYS**:
- 2-space indentation (YAML, JSON, templates)
- 4-space indentation (C#, TypeScript)
- 80-character line limit for readability
- One statement per line

**NEVER**:
- Mixed indentation (tabs + spaces)
- Trailing whitespace
- Unused imports or variables
- Comment every line (only explain WHY, not WHAT)

## CI/CD

**ALWAYS**:
- Run tests before committing
- Run linters + code formatters
- Check for secrets before pushing
- Include PR description + rationale

**NEVER**:
- Commit failing tests
- Skip CI checks
- Merge without review
- Commit secrets (API keys, passwords)

---

**Last Updated**: 2026-04-09

