---
name: backend-principles
description: Backend architecture principles — Layered Architecture (Controller/Service/Repository) and DDD adoption guidelines. Use when designing backend structure, organizing business logic, or deciding whether to adopt DDD.
user-invocable: false
---

# Backend Architecture Principles

## Layered Architecture (Controller / Service / Repository)

Use **Layered Architecture** instead of traditional MVC. Each layer has a clear responsibility:

| Layer | Responsibility |
|-------|---------------|
| **Controller** | Receives requests, validates input, orchestrates multiple services to fulfill business flows, returns responses |
| **Service** | Single-responsibility business logic unit — does NOT call other services |
| **Repository** | Data access abstraction, encapsulates DB query logic |

### Service Layer: Strict Single Responsibility

Each service owns exactly one business capability and only accesses repositories/gateways within its own domain. A service may contain business logic (calculations, validations, transformations), but must NEVER orchestrate a multi-step business flow or call other services.

**Wrong** — service orchestrates the entire business flow:

```typescript
class OrderService {
  // BAD: service is orchestrating — checking inventory, charging payment,
  // creating order, and sending notifications. This is controller's job.
  async createOrder(dto: CreateOrderDto) {
    const inventory = await this.inventoryRepo.check(dto.items);
    if (!inventory.available) throw new ConflictException('Out of stock');

    const payment = await this.paymentGateway.charge(dto.amount);
    const order = await this.orderRepo.create({ ...dto, paymentId: payment.id });
    await this.notificationService.send(order); // BAD: service calling service
    return order;
  }
}
```

**Correct** — each service owns its domain logic, controller orchestrates the flow:

```typescript
class OrderService {
  // Service owns order-specific business logic
  async create(items: Item[], paymentId: string): Promise<Order> {
    const totalAmount = items.reduce((sum, i) => sum + i.price * i.quantity, 0);
    const order = Order.build({ items, paymentId, totalAmount, status: 'created' });
    return this.orderRepo.save(order);
  }
}

class InventoryService {
  // Service owns inventory-specific business logic
  async reserve(items: Item[]): Promise<ReservationResult> {
    const availability = await this.inventoryRepo.checkBatch(items);
    const unavailable = items.filter((i) => !availability.has(i.sku));
    if (unavailable.length) return { success: false, unavailable };
    await this.inventoryRepo.reserveBatch(items);
    return { success: true, unavailable: [] };
  }
}

class PaymentService {
  async charge(amount: number, method: PaymentMethod): Promise<PaymentResult> {
    return this.paymentGateway.process(amount, method);
  }
}

// Controller orchestrates services to implement the business flow
class OrderController {
  async createOrder(req: Request, res: Response) {
    const reservation = await this.inventoryService.reserve(req.body.items);
    if (!reservation.success) return res.conflict({ unavailable: reservation.unavailable });

    const payment = await this.paymentService.charge(req.body.amount, req.body.method);
    if (!payment.success) return res.paymentRequired('Payment failed');

    const order = await this.orderService.create(req.body.items, payment.id);
    await this.notificationService.notify(req.user, order);

    return res.created(order);
  }
}
```

### Why Controllers Orchestrate?

- **Readability**: Business flow is visible at a glance in the controller — no chasing call chains across services
- **Testability**: Each service is tested independently — no mocking other services
- **Maintainability**: Changing the flow only touches the controller, not individual services
- **No circular dependencies**: Services never reference each other

### When Controllers Get Fat

If a controller method grows too long (30-40+ lines), extract it into a **use case** or **workflow**. A use case is an orchestration layer — it composes services to fulfill a specific business flow, just like a controller does, but as a standalone unit.

- Use case can call multiple services (it is an orchestrator, not a service)
- Use case does NOT contain domain logic itself — that stays in services
- Controller becomes a thin HTTP adapter: parse request → call use case → format response

```typescript
// Use case: orchestration extracted from controller
class CreateOrderUseCase {
  async execute(input: CreateOrderInput): Promise<Order> {
    const reservation = await this.inventoryService.reserve(input.items);
    if (!reservation.success) throw new ConflictException('Out of stock');

    const payment = await this.paymentService.charge(input.amount, input.method);
    if (!payment.success) throw new PaymentRequiredException('Payment failed');

    const order = await this.orderService.create(input.items, payment.id);
    await this.notificationService.notify(input.userId, order);
    return order;
  }
}

// Controller becomes a thin HTTP adapter
class OrderController {
  async createOrder(req: Request, res: Response) {
    const order = await this.createOrderUseCase.execute(req.body);
    return res.created(order);
  }
}
```

---

## Domain-Driven Design (DDD)

DDD is a design philosophy centered on the business domain — not a pattern, but a way of thinking.

Core idea:

> Structure software to reflect real business rules, not around databases or frameworks.

### Core Concepts

- **Ubiquitous Language** — Developers and business use the same terms; code naming reflects business language
- **Bounded Context** — Explicit boundaries; the same term can have different meanings in different contexts
- **Aggregate** — Consistency boundary ensuring related data transitions are atomic
- **Entity / Value Object** — Entities have identity; Value Objects are defined by their values
- **Domain Event** — Significant events in the domain, used for cross-context communication

### When to Use DDD

The more items you match, the more DDD (at least lightweight) is worth adopting:

1. **Complex, frequently changing business rules** — Heavy conditionals, discount/permission/exception rules that change often
2. **State machines exist** — Order flows, approval workflows, complex state transitions
3. **High consistency requirements** — Single operation affects multiple tables, intermediate inconsistency is unacceptable
4. **Service layer growing out of control** — Single files with hundreds of lines, business rules scattered everywhere, duplicated logic (Anemic Model symptoms)
5. **Multiple subsystems interact** — Payments + orders + inventory + logistics, cross-domain integration
6. **Ambiguous business semantics** — Same term means different things in different departments

### When NOT to Use DDD

- **Pure CRUD systems** — Admin panels, form-based apps, basic data maintenance
- **Small scope, stable requirements** — Rules rarely change, no complex state transitions
- **Team unfamiliar with DDD** — Without understanding core concepts, it degrades to folder renaming

### Adoption Strategy by Scale

| Scale | Strategy |
|-------|----------|
| **Small** | Layered Architecture + Controller/Service/Repository, modularize as needed |
| **Medium** | Lightweight DDD — introduce Entity/Value Object, move core rules into Domain Model |
| **Large / High complexity** | Full DDD — Bounded Context, Aggregate, Domain Event, paired with Clean/Hexagonal Architecture |

### One-Line Summary

> DDD addresses **business complexity**, not role count or folder structure. Without business complexity, DDD only adds development cost.
