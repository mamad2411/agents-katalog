---
name: php-saloon
description: Use this skill when building or debugging PHP API integrations and SDKs with Saloon, including connectors, requests, authentication, request bodies, testing, pagination, Laravel integration, and Saloon plugin workflows.
version: 1.0.0
source: https://docs.saloon.dev/
license: MIT
---

# php-saloon

Use this skill when you need to:
- build or refactor Saloon connectors, requests, or SDK-style clients
- add authentication, request bodies, retries, middleware, DTOs, pools, or pagination
- test Saloon integrations with `MockClient`, fixtures, or Laravel helpers
- work with Saloon plugins such as Laravel, caching, rate limiting, pagination, XML Wrangler, or Lawman
- upgrade Saloon between major versions, especially `v3` to `v4`

## Start Here

1. Read `references/getting-started.md` for install and first-request setup.
2. Read `references/core-patterns.md` for connectors, requests, auth, bodies, and sending flow.
3. Read `references/api-reference.md` for the most-used `Response`, failure-handling, and debugging APIs.
4. Read `references/advanced-patterns.md` for DTOs, middleware, OAuth2, pools, retries, solo requests, PSR hooks, and SDK patterns.

## Key Patterns

- Model each API integration with a `Connector` and each endpoint with a `Request`.
- Put shared behavior like base URL, default headers, auth, retries, and middleware on the connector.
- For request bodies, add `HasBody` and the matching trait like `HasJsonBody`, `HasMultipartBody`, `HasXmlBody`, `HasFormBody`, `HasStringBody`, or `HasStreamBody`.
- Use `Response` helpers like `json()`, `dto()`, `dtoOrFail()`, `status()`, `failed()`, `throw()`, `getPsrRequest()`, and `getPsrResponse()`.
- Prefer Saloon's built-in testing tools over real API calls in tests.

## Quick Examples

```php
use Saloon\Http\Connector;

class ForgeConnector extends Connector
{
    public function resolveBaseUrl(): string
    {
        return 'https://forge.laravel.com/api/v1';
    }
}
```

```php
use Saloon\Enums\Method;
use Saloon\Http\Request;

class GetServersRequest extends Request
{
    protected Method $method = Method::GET;

    public function resolveEndpoint(): string
    {
        return '/servers';
    }
}
```

```php
$response = $connector->send(new GetServersRequest);

$servers = $response->json();
```

## Reference Files

- `references/getting-started.md`: installation, first connector, first request, sending basics
- `references/core-patterns.md`: connectors, requests, auth, request bodies, and sending flow
- `references/api-reference.md`: response helpers, response customization, failure handling, and debug APIs
- `references/advanced-patterns.md`: SDKs, DTOs, middleware, OAuth2, pools, retries, solo requests, PSR hooks
- `references/testing-debugging.md`: `MockClient`, fixtures, assertions, debug helpers, known testing pitfalls
- `references/integrations-plugins.md`: pagination, Laravel plugin, caching, rate limits, XML Wrangler, Lawman, plugin authoring
- `references/upgrades.md`: supported versions, `v2` to `v3`, `v3` to `v4`, and security-sensitive upgrade notes

## Retrieval Notes

- Open `references/core-patterns.md` before writing new Saloon code from scratch.
- Open `references/api-reference.md` when you need the exact response and error-handling helpers to call.
- Open `references/testing-debugging.md` before changing fixtures, mocks, or request inspection.
- Open `references/upgrades.md` before touching legacy Saloon code or serializer, endpoint, and fixture-path behavior.
