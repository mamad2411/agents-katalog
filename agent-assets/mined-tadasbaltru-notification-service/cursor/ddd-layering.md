---
description: DDD layering and dependency rule for the NotificationPublisher bounded context
globs: src/NotificationPublisher/**
alwaysApply: false
---

# NotificationPublisher layering

Dependency rule (arrows = "may import"): `Domain <- Application <- Infrastructure, UserInterface`.

## Domain (`Domain/`)
- No `Symfony\` imports. Doctrine allowed only as `Doctrine\Common\Collections` and `Doctrine\ORM\Mapping`
  (aggregates are entities). `EntityManager`, repositories and DBAL types stay in Infrastructure. See DECISIONS §1.5.
- Aggregate root `Notification` owns `Delivery` children (which own `DeliveryAttempt`s) and guards invariants;
  state changes are named methods (`markSent()`, `startAttempt()`), never public setters. Domain expands one
  `Delivery` per *requested* channel; "enabled" is Application configuration (2.1), not a Domain concept.
- Value objects (`Recipient`, `IdempotencyKey`, `NotificationContent`) are `final readonly`, validate in the
  constructor, expose `equals()` when compared.
- Ports are interfaces here: `NotificationProvider`, `NotificationRepository`, `RecipientResolver`,
  `DeliveryThrottle`. Domain exceptions extend `Domain\Exception\DomainException`.

## Application (`Application/`)
- Commands/queries are `final readonly` DTOs; handlers are `#[AsMessageHandler]` services that orchestrate
  ports and aggregates. No business rules that belong in the aggregate; no HTTP or Doctrine types.
- Policies with branching (e.g. `FailoverDeliveryStrategy`) live here, unit-tested with fakes.

## Infrastructure (`Infrastructure/`)
- Adapters implementing ports: Doctrine repositories, custom DBAL types under `Persistence/Doctrine/Type/`,
  providers under `Provider/<Channel>/`, framework glue (rate limiter, mailer, http client).
- Aggregates are mapped with `#[ORM\Entity]` on the Domain class (`doctrine.yaml` `type: attribute`).

## UserInterface (`UserInterface/Http/`)
- Controllers translate HTTP <-> Application commands only. Validation via DTO constraints; errors mapped to
  JSON problem responses. No repository access from controllers.
- OpenAPI attributes (`OpenApi\`, `Nelmio\`) are a UserInterface concern; Domain and Application never import them.

```php
// Bad: Domain depending on persistence runtime
namespace App\NotificationPublisher\Domain\Model;
use Doctrine\ORM\EntityManagerInterface;   // forbidden in Domain

// Good: mapping attributes on the aggregate; port in Domain, adapter in Infrastructure
namespace App\NotificationPublisher\Domain\Port;
interface NotificationProvider { public function send(Delivery $delivery): ProviderResult; }
```
