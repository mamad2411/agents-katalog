# Structure Rules — Backend (Layered Java) Examples

**Framework basis:** Java 17+, Maven/Gradle, Spring Boot 3.x under
`src/main/java/<group>/<app>/`. The rules themselves are framework-agnostic —
these trees only show one concrete stack.
**Translation hints:** Gradle vs Maven only changes the build file and the
`src/main` root marginally; Quarkus/Micronaut keep the same package layering.
Feature-first and layer-first are both shown — pick ONE per tier (Rule 2).
**Version-sensitive:** Boot 3.x uses `jakarta.*`; the package *tree* is
unaffected by that. `module-info.java` (JPMS) is optional and, if present, is
the real public-surface boundary for Rule 5.

## Rule 1 — Location is derivable from role
Violation — a junk-drawer package:
```
com/acme/shop/
  util/                 # dumping ground: unrelated helpers pile up here
    OrderStuff.java
    Misc.java
    Helpers.java
```
Correct — every file's package names its role:
```
com/acme/shop/
  order/OrderService.java          # feature-scoped
  pricing/PriceCalculator.java     # named, cohesive shared logic
  time/ClockProvider.java
```

## Rule 2 — One organizing axis per tier
Violation — layer-first and feature-first mixed at the same level:
```
com/acme/shop/
  controllers/OrderController.java  # layer-first here...
  order/OrderService.java           # ...feature-first here — inconsistent
  repositories/OrderRepository.java
```
Correct (feature-first, applied uniformly):
```
com/acme/shop/
  order/    OrderController.java  OrderService.java  OrderRepository.java
  payment/  PaymentController.java PaymentService.java PaymentRepository.java
```
Correct (layer-first, applied uniformly):
```
com/acme/shop/
  controller/ OrderController.java  PaymentController.java
  service/    OrderService.java     PaymentService.java
  repository/ OrderRepository.java  PaymentRepository.java
```

## Rule 4 — The tree encodes dependency direction
Violation — domain imports an adapter:
```
domain/Order.java          ->  import com.acme.shop.web.OrderResponse;   // domain -> transport
domain/OrderService.java   ->  import com.acme.shop.persistence.OrderEntity; // domain -> ORM
```
Correct — adapters depend inward on a port the domain owns:
```
com/acme/shop/order/
  domain/        Order.java   OrderService.java   OrderRepositoryPort.java  # inner: no outward imports
  web/           OrderController.java  OrderResponse.java                   # depends on domain
  persistence/   OrderJpaRepository.java (implements OrderRepositoryPort)   # depends on domain
```

## Rule 5 — One public entry per module
Violation — reaching past a module's surface into its internals:
```java
import com.acme.shop.order.persistence.internal.OrderRowMapper; // deep import into internals
```
Correct — a package-facade (or JPMS `exports`) is the only entry:
```
com/acme/shop/order/
  OrderModule.java          # public facade — the one entry point
  internal/ ...             # package-private detail, not imported from outside
```

## Rule 6 — Co-locate by change cadence (test placement)
Two accepted conventions — detect which the repo uses, keep it uniform:
```
# Mirrored test root (Maven/Gradle default)
src/main/java/com/acme/shop/order/OrderService.java
src/test/java/com/acme/shop/order/OrderServiceTest.java   # same package path
```

## Rule 9 — Designated homes for non-source
```
project/
  src/main/resources/        # config + static resources, not under java/
  src/main/resources/db/migration/   # migration scripts (persistence-warden owns content)
  build/  target/            # generated — .gitignore'd, never hand-edited
```
