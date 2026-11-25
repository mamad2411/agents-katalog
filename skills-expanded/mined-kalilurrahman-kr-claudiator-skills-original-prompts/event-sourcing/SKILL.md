---
name: event-sourcing
description: Implement event sourcing pattern where state is derived from an immutable sequence of events. Outputs event store design, aggregate patterns, projection builders, and command/event handlers.
argument-hint: [domain, aggregate types, projection requirements, event store technology]
allowed-tools: Read, Write, Bash
---

# Event Sourcing

Event sourcing stores every state change as an immutable event rather than overwriting current state. The current state is always derived by replaying events. This enables a complete audit log, temporal queries, and the ability to rebuild any projection from scratch.

## When to Use Event Sourcing

**Use when:**
- Complete audit log is required (finance, healthcare, compliance)
- Temporal queries: "what was the state at 3pm last Tuesday?"
- Multiple read models needed from the same write data
- Complex domain with many state transitions

**Don't use when:**
- Simple CRUD with no history requirements
- Team unfamiliar with the pattern — learning curve is steep
- High write throughput + simple queries — overhead isn't worth it

## Process

1. **Define the domain events** — past-tense, immutable facts (`OrderPlaced`, `PaymentProcessed`).
2. **Design aggregates** — domain objects that enforce invariants and emit events.
3. **Implement the event store** — append-only log with optimistic concurrency.
4. **Build projections** — read models derived from event streams.
5. **Handle commands** — validate → load aggregate → apply command → persist events.
6. **Rebuild projections** — replay events to create new or fix existing read models.

## Output Format

### Event Definitions

```python
# domain/events.py
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events. Immutable."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    aggregate_id: str = ""
    aggregate_version: int = 0

@dataclass(frozen=True)
class OrderPlaced(DomainEvent):
    user_id: str = ""
    items: tuple = field(default_factory=tuple)  # Immutable
    total_cents: int = 0
    shipping_address: dict = field(default_factory=dict)

@dataclass(frozen=True)
class OrderConfirmed(DomainEvent):
    confirmed_by: str = ""

@dataclass(frozen=True)
class PaymentProcessed(DomainEvent):
    payment_provider: str = ""
    payment_id: str = ""
    amount_cents: int = 0

@dataclass(frozen=True)
class PaymentFailed(DomainEvent):
    reason: str = ""
    error_code: str = ""

@dataclass(frozen=True)
class OrderShipped(DomainEvent):
    carrier: str = ""
    tracking_number: str = ""
    estimated_delivery: str = ""

@dataclass(frozen=True)
class OrderCancelled(DomainEvent):
    reason: str = ""
    cancelled_by: str = ""

@dataclass(frozen=True)
class OrderRefunded(DomainEvent):
    refund_amount_cents: int = 0
    refund_id: str = ""
```

### Aggregate

```python
# domain/order_aggregate.py
from typing import Optional
from dataclasses import dataclass, field
from .events import *

class InvalidStateTransition(Exception):
    pass

class OrderAggregate:
    """
    Order aggregate — enforces business invariants.
    State is derived entirely from replayed events.
    Never persisted directly — only events are stored.
    """
    
    def __init__(self, order_id: str):
        self.order_id = order_id
        self.version = 0           # Optimistic concurrency version
        self._events: list[DomainEvent] = []  # Uncommitted events
        
        # State derived from events
        self.status: Optional[str] = None
        self.user_id: Optional[str] = None
        self.items: list = []
        self.total_cents: int = 0
        self.payment_id: Optional[str] = None
        self.is_paid: bool = False
    
    # ── Command handlers ──────────────────────────────────
    
    def place(self, user_id: str, items: list, total_cents: int, shipping_address: dict):
        """Command: place a new order."""
        if self.status is not None:
            raise InvalidStateTransition(f"Cannot place order in state: {self.status}")
        
        # Validate invariants
        if not items:
            raise ValueError("Order must have at least one item")
        if total_cents <= 0:
            raise ValueError("Order total must be positive")
        
        self._apply(OrderPlaced(
            aggregate_id=self.order_id,
            user_id=user_id,
            items=tuple(items),
            total_cents=total_cents,
            shipping_address=shipping_address,
        ))
    
    def process_payment(self, payment_provider: str, payment_id: str, amount_cents: int):
        if self.status != "pending":
            raise InvalidStateTransition(f"Cannot process payment in state: {self.status}")
        
        self._apply(PaymentProcessed(
            aggregate_id=self.order_id,
            payment_provider=payment_provider,
            payment_id=payment_id,
            amount_cents=amount_cents,
        ))
    
    def fail_payment(self, reason: str, error_code: str):
        if self.status != "pending":
            raise InvalidStateTransition(f"Cannot fail payment in state: {self.status}")
        
        self._apply(PaymentFailed(
            aggregate_id=self.order_id,
            reason=reason,
            error_code=error_code,
        ))
    
    def ship(self, carrier: str, tracking_number: str, estimated_delivery: str):
        if self.status != "paid":
            raise InvalidStateTransition(f"Cannot ship order in state: {self.status}")
        
        self._apply(OrderShipped(
            aggregate_id=self.order_id,
            carrier=carrier,
            tracking_number=tracking_number,
            estimated_delivery=estimated_delivery,
        ))
    
    def cancel(self, reason: str, cancelled_by: str):
        if self.status in ("shipped", "delivered", "cancelled"):
            raise InvalidStateTransition(f"Cannot cancel order in state: {self.status}")
        
        self._apply(OrderCancelled(
            aggregate_id=self.order_id,
            reason=reason,
            cancelled_by=cancelled_by,
        ))
    
    # ── Event application (state mutations) ───────────────
    
    def _apply(self, event: DomainEvent, is_replay: bool = False):
        """Apply an event — mutates state. Called for both new events and replays."""
        
        handler = {
            OrderPlaced: self._on_order_placed,
            PaymentProcessed: self._on_payment_processed,
            PaymentFailed: self._on_payment_failed,
            OrderShipped: self._on_order_shipped,
            OrderCancelled: self._on_order_cancelled,
        }.get(type(event))
        
        if handler:
            handler(event)
        
        self.version += 1
        
        if not is_replay:
            self._events.append(event)  # Buffer uncommitted events
    
    def _on_order_placed(self, event: OrderPlaced):
        self.status = "pending"
        self.user_id = event.user_id
        self.items = list(event.items)
        self.total_cents = event.total_cents
    
    def _on_payment_processed(self, event: PaymentProcessed):
        self.status = "paid"
        self.payment_id = event.payment_id
        self.is_paid = True
    
    def _on_payment_failed(self, event: PaymentFailed):
        self.status = "payment_failed"
    
    def _on_order_shipped(self, event: OrderShipped):
        self.status = "shipped"
    
    def _on_order_cancelled(self, event: OrderCancelled):
        self.status = "cancelled"
    
    # ── Reconstruction from events ────────────────────────
    
    @classmethod
    def load(cls, order_id: str, events: list[DomainEvent]) -> 'OrderAggregate':
        """Reconstruct aggregate state by replaying all historical events."""
        aggregate = cls(order_id)
        for event in events:
            aggregate._apply(event, is_replay=True)
        return aggregate
    
    def uncommitted_events(self) -> list[DomainEvent]:
        return list(self._events)
    
    def mark_committed(self):
        self._events.clear()
```

### Event Store

```python
# infrastructure/event_store.py
import json
import asyncpg
from datetime import datetime, timezone
from typing import Type

class OptimisticConcurrencyError(Exception):
    pass

class EventStore:
    """
    Append-only event store backed by PostgreSQL.
    Optimistic concurrency via expected_version.
    """
    
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
    
    async def append_events(
        self,
        aggregate_id: str,
        events: list,
        expected_version: int,
    ):
        """
        Append events to the store.
        expected_version: the version the caller believes the aggregate is at.
        Raises OptimisticConcurrencyError if another writer has appended events since.
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Check current version (optimistic lock)
                current_version = await conn.fetchval(
                    "SELECT COALESCE(MAX(version), 0) FROM events WHERE aggregate_id = $1",
                    aggregate_id
                )
                
                if current_version != expected_version:
                    raise OptimisticConcurrencyError(
                        f"Concurrency conflict: expected version {expected_version}, "
                        f"current version {current_version}"
                    )
                
                # Append events
                for i, event in enumerate(events):
                    version = expected_version + i + 1
                    await conn.execute(
                        """
                        INSERT INTO events (
                            event_id, aggregate_id, version,
                            event_type, event_data, occurred_at
                        ) VALUES ($1, $2, $3, $4, $5, $6)
                        """,
                        event.event_id,
                        aggregate_id,
                        version,
                        type(event).__name__,
                        json.dumps(self._serialize(event)),
                        event.occurred_at,
                    )
    
    async def load_events(self, aggregate_id: str, from_version: int = 0) -> list:
        """Load all events for an aggregate, optionally from a specific version."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT event_type, event_data, version
                FROM events
                WHERE aggregate_id = $1 AND version > $2
                ORDER BY version ASC
                """,
                aggregate_id, from_version
            )
        
        return [self._deserialize(row["event_type"], row["event_data"]) for row in rows]
    
    async def load_events_by_type(
        self, event_type: str, after: datetime = None, limit: int = 1000
    ) -> list:
        """Load events of a specific type — for projections."""
        async with self.pool.acquire() as conn:
            query = "SELECT event_data, occurred_at FROM events WHERE event_type = $1"
            params = [event_type]
            
            if after:
                query += " AND occurred_at > $2"
                params.append(after)
            
            query += f" ORDER BY occurred_at ASC LIMIT {limit}"
            rows = await conn.fetch(query, *params)
        
        return [self._deserialize(event_type, row["event_data"]) for row in rows]
    
    def _serialize(self, event) -> dict:
        """Convert event to storable dict."""
        import dataclasses
        return {k: v for k, v in dataclasses.asdict(event).items()
                if k not in ("event_id", "occurred_at", "aggregate_id", "aggregate_version")}
    
    def _deserialize(self, event_type: str, data: str) -> object:
        """Reconstruct event from stored data."""
        event_classes = {
            "OrderPlaced": OrderPlaced,
            "PaymentProcessed": PaymentProcessed,
            "PaymentFailed": PaymentFailed,
            "OrderShipped": OrderShipped,
            "OrderCancelled": OrderCancelled,
        }
        cls = event_classes.get(event_type)
        if not cls:
            raise ValueError(f"Unknown event type: {event_type}")
        return cls(**json.loads(data))


# Schema
CREATE_EVENTS_TABLE = """
CREATE TABLE IF NOT EXISTS events (
    event_id        UUID PRIMARY KEY,
    aggregate_id    VARCHAR(255) NOT NULL,
    version         INTEGER NOT NULL,
    event_type      VARCHAR(255) NOT NULL,
    event_data      JSONB NOT NULL,
    occurred_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    UNIQUE(aggregate_id, version)   -- Optimistic concurrency constraint
);

CREATE INDEX idx_events_aggregate ON events(aggregate_id, version);
CREATE INDEX idx_events_type ON events(event_type, occurred_at);
CREATE INDEX idx_events_occurred ON events(occurred_at);
"""
```

### Projections

```python
# projections/order_read_model.py
class OrderProjection:
    """
    Read model for order queries.
    Built by processing event stream — completely denormalized for fast reads.
    Can be rebuilt from scratch by replaying all events.
    """
    
    def __init__(self, db):
        self.db = db
    
    async def handle(self, event):
        """Route events to appropriate handlers."""
        handlers = {
            "OrderPlaced": self.on_order_placed,
            "PaymentProcessed": self.on_payment_processed,
            "PaymentFailed": self.on_payment_failed,
            "OrderShipped": self.on_order_shipped,
            "OrderCancelled": self.on_order_cancelled,
        }
        handler = handlers.get(type(event).__name__)
        if handler:
            await handler(event)
    
    async def on_order_placed(self, event: OrderPlaced):
        await self.db.execute(
            """
            INSERT INTO order_read_model (
                order_id, user_id, status, total_cents,
                items, created_at, updated_at
            ) VALUES ($1, $2, 'pending', $3, $4, $5, $5)
            ON CONFLICT (order_id) DO NOTHING
            """,
            event.aggregate_id, event.user_id, event.total_cents,
            json.dumps(list(event.items)), event.occurred_at,
        )
    
    async def on_payment_processed(self, event: PaymentProcessed):
        await self.db.execute(
            "UPDATE order_read_model SET status='paid', payment_id=$2, updated_at=$3 WHERE order_id=$1",
            event.aggregate_id, event.payment_id, event.occurred_at,
        )
    
    async def on_order_cancelled(self, event: OrderCancelled):
        await self.db.execute(
            "UPDATE order_read_model SET status='cancelled', cancel_reason=$2, updated_at=$3 WHERE order_id=$1",
            event.aggregate_id, event.reason, event.occurred_at,
        )
    
    async def rebuild(self, event_store: EventStore):
        """Rebuild entire read model from event history."""
        await self.db.execute("TRUNCATE order_read_model")
        
        all_events = await event_store.load_events_by_type("OrderPlaced", limit=100000)
        # Then load other event types and merge by time...
        # (In practice: use a single sorted stream of all events)
        
        for event in all_events:
            await self.handle(event)
        
        print(f"Rebuilt projection from {len(all_events)} events")
```

## Rules

- **Events are past-tense, immutable facts** — `OrderPlaced`, not `PlaceOrder`; never modify stored events.
- **Aggregates emit events, never mutate directly** — all state changes flow through event application.
- **Optimistic concurrency at the event store** — the `expected_version` check prevents lost updates.
- **Projections are disposable** — they're derived; rebuild them anytime from the event log.
- **Separate command model from query model** — aggregates handle writes; projections handle reads (CQRS).
- **Event schema migration is hard** — version your events from day one (`OrderPlaced.v2`).
- **Snapshots for long-lived aggregates** — store periodic snapshots to avoid replaying 10,000 events on every load.
- **Idempotent event handlers** — projections may receive the same event twice; handle duplicates gracefully.
- **Don't put behavior in projections** — they transform events to read models; no business logic.
- **Test by replaying** — event sourcing tests replay events and assert on derived state, not mocked calls.
