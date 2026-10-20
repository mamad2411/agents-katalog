---
description: Symfony 7.4 / PHP 8.4 coding conventions for this project
alwaysApply: true
---

# Symfony 7.4 / PHP 8.4 conventions

- Every PHP file starts with `<?php` + `declare(strict_types=1);`. Namespaces follow PSR-4 from `App\`.
- Classes are `final` unless designed for extension; services are `final readonly class` with constructor
  promotion and no setters. Doctrine-mapped entities are `final` too (attribute mapping, no proxies needed
  thanks to native lazy objects).
- Prefer native enums (backed, `string`) over class constants; enums may carry small behaviour methods.
- Dependency injection: autowire by constructor type. Use `#[Autowire('%param%')]`, `#[AutowireIterator]`,
  `#[AsTaggedItem]`, `#[Target]` instead of YAML service definitions. `config/services.yaml` stays minimal.
- Routing via `#[Route]` attributes. Request bodies via `#[MapRequestPayload]` DTOs (`final readonly class`
  with Validator constraints on promoted properties). Responses are `JsonResponse` built from explicit arrays.
- Time comes from `Psr\Clock\ClockInterface`, ids from `Symfony\Component\Uid\Uuid::v7()`. Never `new \DateTimeImmutable()`
  or `time()` inside domain or application code.
- Configuration lives in `config/packages/*.yaml`; secrets and environment-specific values only via `%env()%`.
- Logging through `Psr\Log\LoggerInterface`, structured context arrays, no string interpolation of payloads.
- Exceptions are specific classes extending a per-layer base; no `\Exception` / `\RuntimeException` thrown directly.
- No `static` helpers, no service locators, no `ContainerInterface` injection, no traits for shared behaviour.
- Comments explain intent or trade-offs only; never narrate what the code does.

```php
// Good
final readonly class TwilioSmsProvider implements NotificationProvider
{
    public function __construct(
        private HttpClientInterface $httpClient,
        #[Autowire('%env(TWILIO_ACCOUNT_SID)%')] private string $accountSid,
        private ClockInterface $clock,
    ) {}
}
```

Formatting is owned by php-cs-fixer (`@Symfony`, `@PER-CS2.0`); do not hand-format against it.
