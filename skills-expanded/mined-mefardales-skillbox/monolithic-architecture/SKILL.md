---
name: monolithic-architecture
description: >
  Modular monolith architecture best practices covering project structure, module
  boundaries, dependency management, and migration strategies. Use this skill when
  building new applications or restructuring existing monoliths for maintainability.
license: MIT
metadata:
  author: skillbox
  version: "1.0"
  category: backend
  tags: monolith, architecture, modular, design, structure
---

# Monolithic Architecture Best Practices

## Why Monolith-First

Start with a monolith. A monolith is simpler to develop, deploy, debug, and reason about. You avoid the operational complexity of distributed systems: no service discovery, no distributed tracing, no eventual consistency, no saga patterns.

Extract to microservices only when you have a proven need:
- A specific module needs to scale independently
- Different teams need to deploy independently on different schedules
- A module requires a fundamentally different technology stack

Most applications never reach that point. A well-structured monolith handles millions of users.

## Modular Monolith Structure

Organize code into vertical modules, each representing a bounded context. Do not organize by technical layer (controllers/, models/, services/) at the top level.

```
myapp/
  modules/
    orders/
      api/
        routes.py
        schemas.py
      domain/
        models.py
        services.py
        events.py
      repository/
        order_repo.py
      tests/
        test_order_service.py
        test_order_api.py
      __init__.py          # public module API
    payments/
      api/
        routes.py
        schemas.py
      domain/
        models.py
        services.py
      repository/
        payment_repo.py
      tests/
      __init__.py
    inventory/
      ...
    users/
      ...
  shared/
    auth/
      middleware.py
    database/
      session.py
    events/
      bus.py
  main.py
  config.py
```

Each module has its own api, domain, and repository layers. The module's `__init__.py` exports only the public interface.

## Module Boundaries and Dependency Rules

Modules communicate through explicit public interfaces. Do not import internal module code from another module.

```python
# modules/orders/__init__.py -- this is the public API
from modules.orders.domain.services import OrderService
from modules.orders.domain.models import OrderStatus

__all__ = ["OrderService", "OrderStatus"]
```

```python
# modules/payments/domain/services.py -- CORRECT
from modules.orders import OrderService  # uses the public API

class PaymentService:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    def process_payment(self, order_id: int):
        order = self.order_service.get_order(order_id)
        # process payment...
```

```python
# modules/payments/domain/services.py -- WRONG
from modules.orders.repository.order_repo import OrderRepository  # bypasses module boundary
from modules.orders.domain.models import Order  # internal model, not exported
```

Enforce these rules with an architectural linter. In Python, use `import-linter`:

```ini
# .importlinter
[importlinter]
root_package = myapp

[importlinter:contract:module-boundaries]
name = Module boundaries
type = independence
modules =
    myapp.modules.orders
    myapp.modules.payments
    myapp.modules.inventory
    myapp.modules.users
```

## Inter-Module Communication

Use an in-process event bus for cross-module communication. This decouples modules without network overhead.

```python
# shared/events/bus.py
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: dict):
        for handler in self._handlers.get(event_type, []):
            handler(payload)

event_bus = EventBus()
```

```python
# modules/orders/domain/services.py
from shared.events.bus import event_bus

class OrderService:
    def place_order(self, order_data: dict):
        order = self.repo.create(order_data)
        event_bus.publish("order.placed", {
            "order_id": order.id,
            "customer_id": order.customer_id,
            "total": order.total,
        })
        return order
```

```python
# modules/notifications/domain/services.py
from shared.events.bus import event_bus

class NotificationService:
    def __init__(self):
        event_bus.subscribe("order.placed", self.on_order_placed)

    def on_order_placed(self, payload: dict):
        self.send_confirmation_email(payload["customer_id"], payload["order_id"])
```

This pattern prepares you for microservices extraction later -- replace the in-process bus with a message broker.

## Shared Kernel Pattern

Place truly shared domain concepts in a shared kernel. Keep it minimal. If only two modules share a concept, it probably belongs in one of them.

```python
# shared/kernel/money.py
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError(f"Cannot add {self.currency} and {other.currency}")
        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __mul__(self, quantity: int) -> "Money":
        return Money(amount=self.amount * quantity, currency=self.currency)
```

Good candidates for the shared kernel: Money, Address, DateRange, UserId. Do not put business logic or services in the shared kernel.

## Database Schema Organization

Use schema-per-module (PostgreSQL) or table prefix conventions to enforce data ownership at the database level.

```sql
-- Each module owns its own schema
CREATE SCHEMA orders;
CREATE SCHEMA payments;
CREATE SCHEMA inventory;
CREATE SCHEMA users;

-- orders module tables
CREATE TABLE orders.orders (
    id BIGSERIAL PRIMARY KEY,
    customer_id BIGINT NOT NULL,  -- references users.users(id) conceptually, NOT as FK
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders.order_items (
    id BIGSERIAL PRIMARY KEY,
    order_id BIGINT REFERENCES orders.orders(id),
    product_id BIGINT NOT NULL,  -- conceptual reference to inventory module
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL
);
```

Do not create foreign keys across module schemas. Cross-module references are conceptual -- enforced at the application layer, not the database. This keeps modules independently deployable if you extract them later.

## Dependency Injection

Use dependency injection to wire modules together. This makes modules testable and boundaries explicit.

```python
# main.py
from modules.orders.domain.services import OrderService
from modules.orders.repository.order_repo import OrderRepository
from modules.payments.domain.services import PaymentService
from modules.payments.repository.payment_repo import PaymentRepository
from shared.database.session import get_session

def bootstrap():
    session = get_session()

    order_repo = OrderRepository(session)
    payment_repo = PaymentRepository(session)

    order_service = OrderService(order_repo=order_repo)
    payment_service = PaymentService(
        payment_repo=payment_repo,
        order_service=order_service,
    )

    return {
        "order_service": order_service,
        "payment_service": payment_service,
    }
```

## When to Extract to Microservices

Extract a module to a service when ALL of these are true:
1. The module has a clear, stable API boundary
2. A different team will own and deploy it independently
3. It needs to scale independently from the rest of the application
4. You have the infrastructure to support distributed systems (CI/CD per service, monitoring, tracing)

Do NOT extract when:
- You just want "clean architecture" -- a modular monolith achieves that
- The module has tight data coupling with other modules
- Your team is small (under 10 engineers)
- You do not have production-grade observability in place

## Performance Optimization

Profile before optimizing. Use database query analysis and application profiling to find actual bottlenecks.

```python
# Use database-level caching for hot queries
import functools
from shared.cache import cache

class ProductService:
    @cache.memoize(timeout=300)  # 5 minute cache
    def get_product_catalog(self, category_id: int):
        return self.repo.find_by_category(category_id)

    def update_product(self, product_id: int, data: dict):
        product = self.repo.update(product_id, data)
        cache.delete_memoized(self.get_product_catalog, product.category_id)
        return product
```

For heavy background work, use an in-process task queue that can later be replaced with Celery or Sidekiq:

```python
import threading
from queue import Queue

class BackgroundWorker:
    def __init__(self):
        self.queue = Queue()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        while True:
            task, args = self.queue.get()
            try:
                task(*args)
            except Exception as e:
                logger.error(f"Background task failed: {e}")
            self.queue.task_done()

    def enqueue(self, task, *args):
        self.queue.put((task, args))

worker = BackgroundWorker()
worker.enqueue(send_welcome_email, user.id)
```

## Deployment Strategies

Deploy monoliths with blue-green or rolling deployments:

```yaml
# docker-compose.yml for a monolith
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379/0
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
        order: start-first  # start new before stopping old
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
```

Run database migrations separately from application deployment. Migrations must be backward-compatible so the old application version still works during rollout:

```bash
# Deploy process:
# 1. Run backward-compatible migrations
python manage.py migrate

# 2. Deploy new application version (rolling update)
docker service update --image myapp:v2.1 myapp_app

# 3. (optional) Run cleanup migration after all instances are on new version
python manage.py migrate --run-cleanup
```

## Common Pitfalls

1. **Big ball of mud.** Without module boundaries, a monolith degrades into an unmaintainable tangle. Define and enforce module boundaries from day one.
2. **Circular dependencies.** If module A depends on module B and B depends on A, extract the shared concept into the shared kernel or introduce an event.
3. **Premature extraction.** Extracting a service before the module boundary is stable creates tight coupling between services. Get the boundary right in the monolith first.
4. **God modules.** If a module has 50+ files, it is too big. Split it into sub-modules with clear responsibilities.
5. **Shared mutable state.** Do not use global variables or module-level mutable state. Pass dependencies through constructors.
