---
alwaysApply: true
---

# Emarsys SDK PHP - Development Instructions

## Project Overview

This is a PHP 8.3+ SDK for the Emarsys API v3 with OAuth 2.0 authentication. The SDK follows modern PHP best practices with strict typing, immutability, and comprehensive testing.

**Key Technologies:**
- PHP 8.3+
- GuzzleHTTP 7.0 for HTTP requests
- PHPUnit 12 for testing
- PHPStan level 8 for static analysis
- Laravel Pint for code formatting

**Architecture:**
```
Client (facade)
  └─> Domain\Client (HTTP + OAuth)
       └─> Domain Clients (e.g., ContactListsClient)
            └─> DTOs (input) & Value Objects (output)
```

## Docker Development Workflow

**IMPORTANT:** Always use Docker for development, testing, and analysis to ensure environment consistency.

### Common Commands

```bash
# Start container
make up

# Install/update dependencies
make install

# Run tests
make test

# Run static analysis
make analyse

# Format code
make format

# Run all checks (format + analyse + test)
make check

# Open shell in container
make shell

# Stop container
make down
```

### Running Commands in Docker

**DO:** Use make commands or docker-compose exec
```bash
make test
make analyse
docker-compose exec php composer test
```

**DON'T:** Run composer/php commands directly on host
```bash
# ❌ WRONG - may have version/extension mismatches
composer test
php vendor/bin/phpunit

# ✅ CORRECT - runs in consistent Docker environment
make test
```

### When to Rebuild

Rebuild the Docker image if:
- Dockerfile changes
- PHP extensions are added
- System dependencies change

```bash
make rebuild
```

## PHP Best Practices

### 1. Type Safety

**ALWAYS use strict typing:**
```php
<?php

declare(strict_types=1);

namespace Hobbii\Emarsys\Domain;

// All parameters and return types MUST be typed
public function get(string $endpoint, array $query = []): Response
{
    // ...
}
```

**Rules:**
- Every file starts with `declare(strict_types=1);`
- All public method parameters have types
- All public method return types are declared
- Use union types when appropriate (e.g., `int|string|array|null`)
- Use `readonly` for immutable properties in PHP 8.3+

### 2. Immutability

**Value Objects and DTOs are immutable:**
```php
readonly class ContactList
{
    public function __construct(
        public int $id,
        public string $name,
        public ?string $description,
        public string $created,
    ) {}
}
```

**Rules:**
- Use `readonly` keyword for immutable classes
- No setters on Value Objects
- DTOs are input-only, Value Objects are output-only
- Collections should be immutable after construction

### 3. Exception Handling

**Exception hierarchy:**
```
EmarsysException (base)
├─> AuthenticationException (OAuth failures)
├─> RateLimitException (429 responses)
└─> ApiException (other API errors)
```

**Rules:**
- Always chain previous exceptions: `throw new ApiException('message', previous: $e)`
- Provide helpful error messages for users
- Include relevant context in exception properties
- Don't expose sensitive data (credentials, tokens) in exceptions

### 4. Naming Conventions

**Classes:**
- `PascalCase` for class names
- Suffix DTOs with purpose: `CreateContactList`, `UpdateContact`
- Value Objects named after domain concept: `ContactList`, `OauthData`
- Clients suffixed with `Client`: `ContactListsClient`

**Methods:**
- `camelCase` for method names
- Descriptive verbs: `create()`, `list()`, `delete()`, `get()`
- Private methods prefixed with purpose: `extractRetryAfter()`, `ensureValidOauthData()`

**Variables:**
- `camelCase` for variables
- Descriptive names, avoid abbreviations
- Boolean variables prefixed with `is`, `has`, `should`: `isRetry`, `hasErrors`

### 5. Documentation

**PHPDoc is required for:**
- All public methods
- Complex private methods
- Properties that need explanation
- Type hints for arrays: `@var ErrorObject[]`
- Parameter descriptions: `@param array<string,mixed> $options`

**Example:**
```php
/**
 * Extract retry-after value from rate limit response.
 *
 * Checks both Retry-After header (standard) and X-RateLimit-Reset header (common in APIs).
 * The Retry-After header can contain either:
 * - An integer representing seconds to wait
 * - An HTTP date string representing when to retry
 *
 * @return int Number of seconds to wait before retrying (defaults to 60 if not found)
 */
private function extractRetryAfter(ResponseInterface $response): int
{
    // ...
}
```

### 6. Testing

**Test file organization matches source:**
```
src/Domain/ContactLists/ContactListsClient.php
tests/Unit/Domain/ContactLists/ContactListsClientTest.php
```

**Testing rules:**
- Every public method has at least one test
- Test edge cases and error conditions
- Use descriptive test names: `test_rate_limit_exception_thrown_on_429_response()`
- Mock external dependencies (Guzzle)
- Integration tests are separate and require credentials

**Test structure:**
```php
public function test_descriptive_name_of_what_is_being_tested(): void
{
    // Arrange - set up test data
    $responses = [/* mock responses */];
    $client = $this->createClientWithMockHandler($responses);

    // Act - perform the action
    $result = $client->someMethod();

    // Assert - verify expectations
    $this->assertInstanceOf(ExpectedType::class, $result);
    $this->assertSame('expected', $result->property);
}
```

### 7. HTTP Client Patterns

**When adding new domain clients:**

1. **Create domain client:** `src/Domain/NewFeature/NewFeatureClient.php`
2. **Add DTOs:** `src/Domain/NewFeature/DTOs/CreateNewFeature.php`
3. **Add Value Objects:** `src/Domain/NewFeature/ValueObjects/NewFeature.php`
4. **Register in main client:**
```php
// src/Client.php
private ?NewFeatureClient $newFeature = null;

public function newFeature(): NewFeatureClient
{
    return $this->newFeature ??= new NewFeatureClient($this->client);
}
```

**HTTP method patterns:**
```php
// GET request
$response = $this->client->get('endpoint', ['param' => 'value']);

// POST request
$response = $this->client->post('endpoint', ['key' => 'value']);

// Response handling
$data = $response->dataAsArray();
return NewValueObject::fromArray($data);
```

## Code Quality Standards

### Static Analysis (PHPStan Level 8)

**Before committing, always run:**
```bash
make analyse
```

**Common issues to avoid:**
- Missing return type declarations
- Untyped parameters
- Potentially undefined array keys (use `??` or `isset()`)
- Mixed types without explicit handling

**Fix patterns:**
```php
// ❌ BAD - PHPStan error: possibly undefined
$value = $array['key'];

// ✅ GOOD - null coalescing
$value = $array['key'] ?? null;

// ❌ BAD - missing array type
/** @var array */

// ✅ GOOD - specific array type
/** @var array<string,mixed> */
```

### Code Formatting (Laravel Pint - PSR-12)

**Auto-format before committing:**
```bash
make format
```

**Key rules:**
- 4 spaces for indentation (no tabs)
- Opening braces on same line for methods/classes
- One blank line between methods
- No trailing whitespace
- Single blank line at end of file

### Pre-commit Hook

The repository includes a pre-commit hook that automatically:
1. Formats code with Pint
2. Stages formatted files
3. Allows commit to proceed

**Setup (automatic via composer):**
```bash
composer install  # Sets up git hooks automatically
```

## Common Patterns

### 1. Value Object Factory Pattern

```php
readonly class ContactList
{
    private function __construct(/* properties */) {}

    public static function fromArray(array $data): self
    {
        return new self(
            id: $data['id'],
            name: $data['name'],
            description: $data['description'] ?? null,
            created: $data['created'],
        );
    }
}
```

### 2. Collection Pattern

```php
use Hobbii\Emarsys\Domain\ValueObjects\DataCollection;

/**
 * ContactList collection
 *
 * @extends DataCollection<int,ContactList>
 */
final class ContactListCollection extends DataCollection
{
    protected static function getItemClass(): string
    {
        return ContactList::class;
    }
}
```

### 3. API Response Parsing

```php
// In domain client
$response = $this->client->get('contact-lists');
$data = $response->dataAsArray();

// Parse collection
$items = array_map(
    fn(array $item) => ContactList::fromArray($item),
    $data
);

return new ContactListCollection($items);
```

### 4. Error Handling

```php
try {
    $response = $this->client->request($method, $endpoint, $options);
    return Response::fromPsrResponse($response);
} catch (ClientException $e) {
    $statusCode = $e->getResponse()->getStatusCode();

    if ($statusCode === 429) {
        throw new RateLimitException(/* ... */, previous: $e);
    }

    throw new ApiException('Error message', previous: $e);
}
```

## Integration Tests

**DO NOT run integration tests casually** - they create real API resources.

**Setup:**
```bash
# 1. Copy environment file
cp .env.example .env

# 2. Add real credentials to .env
EMARSYS_CLIENT_ID=your-client-id
EMARSYS_CLIENT_SECRET=your-client-secret

# 3. Run quick test (read-only)
make integration-test
```

**Integration test rules:**
- Tests use real Emarsys API
- Tests may create resources (contact lists)
- Tests attempt cleanup but may leave data
- Add warning comments for destructive operations
- Document required credentials in test docblocks

## Pull Request Checklist

Before submitting a PR, ensure:

1. **All checks pass:**
```bash
make check  # Runs format + analyse + test
```

2. **Code is documented:**
- [ ] Public methods have PHPDoc
- [ ] Complex logic has explanatory comments
- [ ] README updated if adding features

3. **Tests are comprehensive:**
- [ ] Unit tests for new functionality
- [ ] Edge cases covered
- [ ] Mocks used for external dependencies

4. **Types are strict:**
- [ ] All parameters typed
- [ ] All return types declared
- [ ] PHPStan level 8 passes

5. **No technical debt:**
- [ ] No TODO comments without issue reference
- [ ] No commented-out code
- [ ] No debug statements (var_dump, dd, etc.)

## Troubleshooting

### Issue: "Class not found"
**Solution:** Rebuild autoloader
```bash
docker-compose exec php composer dump-autoload
```

### Issue: "Tests fail in Docker but pass locally"
**Solution:** This means your local environment differs. Trust Docker results and fix the code.

### Issue: "PHPStan errors that seem wrong"
**Solution:** PHPStan level 8 is strict. Either:
1. Fix the type issue (preferred)
2. Add specific `@phpstan-ignore-next-line` with explanation
3. Update `phpstan.neon` if it's a false positive

### Issue: "Docker is slow on macOS"
**Solution:** This is expected. Consider:
- Using vendor volume (already configured)
- Excluding heavy directories from sync
- Running tests in Docker but developing locally

## Context7 MCP - Emarsys API Documentation

This project is configured with Context7 MCP server for instant access to Emarsys API documentation.

**How to use:**
- Ask questions about Emarsys API: "What endpoints are available for contact lists?"
- Reference documentation: "According to the Emarsys API docs, what's the rate limit?"
- Get accurate implementation guidance based on official docs

The AI can now fetch real-time information from the official Emarsys API reference to help you code correctly.

## Resources

- [PSR-12 Coding Style](https://www.php-fig.org/psr/psr-12/)
- [PHPStan Documentation](https://phpstan.org/user-guide/getting-started)
- [PHPUnit Documentation](https://phpunit.de/documentation.html)
- [Emarsys API Documentation](https://dev.emarsys.com/docs/emarsys-core-api-guides/)
- [Emarsys Core API Reference](https://dev.emarsys.com/docs/core-api-reference/) (via Context7 MCP)
- [Guzzle Documentation](https://docs.guzzlephp.org/)

## Questions or Issues?

- Check `RATE_LIMITING_SPEC.md` for future feature plans
- Review `tests/Integration/README.md` for integration testing details
- See `README.md` for usage examples and API documentation
- See `.cursor/README.md` for Cursor IDE configuration and MCP server setup
