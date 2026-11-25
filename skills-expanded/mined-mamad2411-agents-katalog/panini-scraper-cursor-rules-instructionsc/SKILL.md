# Panini Scraper - Cursor Rules

## Project Overview

This is a TypeScript library for scraping Panini Brasil product information. It follows Clean Architecture principles and is designed as a reusable npm package.

**Project Type**: TypeScript Library (not an API or CLI)
**Version**: 1.1.0
**Architecture**: Clean Architecture with SOLID principles
**Test Coverage Requirement**: Minimum 80% (currently 95%+)

## Core Principles

### 1. Clean Architecture

**Layer Structure** (dependencies flow inward):
```
domain/ → usecases/ → infrastructure/
```

- **Domain Layer** (`src/domain/`): 
  - Core business entities and interfaces
  - NO external dependencies
  - Pure TypeScript only
  - Define interfaces, not implementations

- **Use Cases Layer** (`src/usecases/`):
  - Application business logic
  - Depend ONLY on domain layer
  - Orchestrate data flow

- **Infrastructure Layer** (`src/infrastructure/`):
  - External concerns (HTTP, parsing)
  - Implement domain interfaces
  - May depend on external libraries (Axios, Cheerio)

### 2. SOLID Principles

- **Single Responsibility**: Each class has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Derived classes must be substitutable
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depend on abstractions, not concretions

## Code Style and Conventions

### TypeScript

- Use **strict mode** (already enabled in tsconfig.json)
- Prefer `readonly` for immutable properties
- Use `interface` for data structures, `class` for entities with behavior
- Avoid `any` type - use proper typing
- Use `const` for constants, avoid `var`

### Naming Conventions

- **Classes**: PascalCase (e.g., `ProductEntity`, `HttpClient`)
- **Interfaces**: PascalCase (e.g., `Product`, `ProductRepository`)
- **Functions/Methods**: camelCase (e.g., `scrapeProduct`, `normalizeUrl`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TIMEOUT`)
- **Files**: kebab-case or camelCase matching the main export

### Error Handling

- Create **specific error types** extending base error classes
- Always include context in errors (URL, status code, etc.)
- Throw errors from domain when business rules are violated
- Transform external errors to domain errors in infrastructure

Example:
```typescript
throw new InvalidUrlError(url);
throw new ProductNotFoundError(url);
throw new ProductScrapingError(message, url, statusCode);
```

### Function Guidelines

- Keep functions **small and focused** (ideally < 30 lines)
- Extract complex logic into private methods
- Use descriptive names that explain intent
- Avoid side effects where possible
- Return meaningful values, not void when possible

## Documentation Standards

### JSDoc Requirements

ALL public APIs MUST have comprehensive JSDoc:

```typescript
/**
 * Brief description of what the function does.
 * 
 * Detailed explanation if needed, including:
 * - How it works
 * - When to use it
 * - Important considerations
 * 
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws {ErrorType} When this error is thrown
 * 
 * @example
 * ```typescript
 * const result = await someFunction('example');
 * console.log(result);
 * ```
 */
```

### Documentation Files

- Update `README.md` for user-facing changes
- Update `ARCHITECTURE.md` for architectural decisions
- Update `CHANGELOG.md` for version changes
- Create examples in `examples/` for new features

## Testing Requirements

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete flows with mocked HTTP

### Coverage Requirements

- Minimum **80%** coverage on all metrics
- Aim for **95%+** on critical paths
- **100%** coverage on domain entities

### Test Naming

```typescript
describe('ClassName', () => {
    describe('methodName', () => {
        it('should do something when condition', () => {
            // Test implementation
        });
    });
});
```

### Testing Best Practices

- Test behavior, not implementation
- Use descriptive test names
- Arrange, Act, Assert pattern
- Mock external dependencies
- Test edge cases and error paths

## Project-Specific Rules

### Product Entity

The `Product` interface includes:
- `title`, `fullPrice`, `currentPrice`, `isPreOrder`, `inStock`
- `imageUrl`, `url`, `format`, `contributors`, `id`

When modifying `Product`:
1. Update `product.entity.ts` (interface AND class)
2. Update `paniniScraper.service.ts` (extraction logic)
3. Update tests to include new fields
4. Update README.md examples

### Scraping Logic

Located in `src/infrastructure/paniniScraper.service.ts`:

- Use **multiple selectors** as fallbacks for robustness
- Filter out **placeholder images** (check `isPlaceholderImage`)
- Normalize prices (handle comma/dot separators)
- Extract IDs from multiple sources (details, URL, etc.)
- Handle missing data gracefully

### HTTP Client

- Default timeout: 15 seconds
- Include browser-like headers to avoid detection
- Support proxy configuration
- Transform Axios errors to domain errors

## Common Tasks

### Adding a New Product Field

1. Update `Product` interface in `src/domain/product.entity.ts`
2. Update `ProductEntity` constructor and properties
3. Add extraction method in `paniniScraper.service.ts`
4. Call extraction in `scrapeProduct` method
5. Update tests to verify new field
6. Update documentation and examples

### Adding a New Scraping Feature

1. Define interface in **domain layer**
2. Implement in **infrastructure layer**
3. Add use case if needed in **usecases layer**
4. Export from `src/index.ts` if public API
5. Write tests (unit + integration)
6. Document in README.md

### Creating a New Error Type

1. Extend `ProductScrapingError` in `src/domain/product.repository.ts`
2. Add to exports in `src/domain/index.ts`
3. Export from main `src/index.ts`
4. Document in README.md error handling section

## Dependencies

### Production

- `axios`: HTTP client
- `cheerio`: HTML parsing

### Development

- `typescript`: Type system
- `jest`: Testing framework
- `eslint`: Linting

**DO NOT** add dependencies without strong justification. Keep the library lightweight.

## Scripts

```bash
npm run build          # Build the project
npm test              # Run all tests
npm run test:coverage # Run tests with coverage
npm run lint          # Check for linting errors
npm run lint:fix      # Fix linting errors
npm run clean         # Clean build directory
npm run example:basic # Run basic usage example
npm run example:advanced # Run advanced usage example
```

## Git Workflow

- Follow conventional commits
- Create feature branches
- Write meaningful commit messages
- Keep commits focused and atomic
- Update CHANGELOG.md for notable changes

## Anti-Patterns to Avoid

❌ **Don't** import infrastructure in domain layer
❌ **Don't** use `any` type
❌ **Don't** add API/server functionality (this is a library)
❌ **Don't** skip writing tests
❌ **Don't** commit without running tests
❌ **Don't** violate layer boundaries
❌ **Don't** add unnecessary dependencies
❌ **Don't** use console.log (use proper error handling)

## When Making Changes

### Before Coding

1. Understand which layer(s) are affected
2. Check if existing patterns can be reused
3. Plan the changes to minimize ripple effects

### While Coding

1. Follow existing code style and patterns
2. Write tests alongside code (TDD encouraged)
3. Keep functions small and focused
4. Add comprehensive JSDoc

### After Coding

1. Run `npm run lint` - fix all issues
2. Run `npm test` - all tests must pass
3. Run `npm run build` - build must succeed
4. Check coverage - must be ≥80%
5. Update documentation if needed
6. Review your own changes

## Example Patterns

### Creating a Use Case

```typescript
export class MyUseCase {
    constructor(
        private readonly repository: MyRepository
    ) {}

    async execute(input: Input): Promise<Output> {
        // Validate input
        // Call repository
        // Transform/return result
    }
}
```

### Implementing a Repository

```typescript
export class MyService implements MyRepository {
    constructor(config?: Config) {
        // Initialize dependencies
    }

    async myMethod(param: string): Promise<Result> {
        try {
            // Implementation
        } catch (error) {
            // Transform to domain error
        }
    }
}
```

### Writing Tests

```typescript
describe('MyClass', () => {
    let instance: MyClass;
    let mockDependency: jest.Mocked<Dependency>;

    beforeEach(() => {
        mockDependency = {
            method: jest.fn()
        } as any;
        instance = new MyClass(mockDependency);
    });

    it('should do something correctly', async () => {
        // Arrange
        const input = 'test';
        mockDependency.method.mockResolvedValue('result');

        // Act
        const result = await instance.execute(input);

        // Assert
        expect(result).toBe('expected');
        expect(mockDependency.method).toHaveBeenCalledWith('test');
    });
});
```

## IDE Configuration

### Recommended VSCode Extensions

- ESLint
- TypeScript and JavaScript Language Features
- Jest Runner
- Better Comments

### Editor Settings

- Tab size: 4 spaces (as per .editorconfig if present)
- Format on save: enabled
- Trim trailing whitespace: enabled

## Resources

- **Architecture**: See ARCHITECTURE.md
- **Examples**: See examples/ directory
- **Changelog**: See CHANGELOG.md
- **Tests**: See tests/ directory

## Questions?

When in doubt:
1. Check existing code for patterns
2. Read ARCHITECTURE.md for design decisions
3. Follow Clean Architecture principles
4. Maintain test coverage
5. Document everything public

Remember: **This is a library, not an application**. Focus on providing a clean, well-documented API for other developers to use.

