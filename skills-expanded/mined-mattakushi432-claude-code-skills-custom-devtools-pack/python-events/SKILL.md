---
name: python-events
description: "When to activate: event-driven architecture, domain events, event sourcing, Kafka, RabbitMQ, NATS"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Python Event-Driven Patterns

## Domain Events
```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class UserRegistered(DomainEvent):
    user_id: int
    email: str
    name: str

@dataclass(frozen=True)
class OrderPlaced(DomainEvent):
    order_id: UUID
    user_id: int
    total_amount_cents: int
```

## Transactional Outbox Pattern
```python
class OutboxMessage(Base):
    __tablename__ = "outbox_messages"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    event_type: Mapped[str] = mapped_column(index=True)
    payload: Mapped[dict] = mapped_column(JSON)
    published: Mapped[bool] = mapped_column(default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

async def create_user_and_emit(session: AsyncSession, data: dict) -> User:
    user = User(**data)
    session.add(user)
    
    # Write event to outbox in same transaction
    outbox = OutboxMessage(
        event_type="user.registered",
        payload={"user_id": user.id, "email": user.email},
    )
    session.add(outbox)
    await session.commit()  # atomic: both or neither
    
    return user

# Relay: poll outbox and publish to broker
async def relay_outbox(session: AsyncSession, publisher: Publisher) -> None:
    pending = await session.execute(
        select(OutboxMessage).where(~OutboxMessage.published).limit(100)
    )
    for msg in pending.scalars():
        await publisher.publish(msg.event_type, msg.payload)
        msg.published = True
    await session.commit()
```

## Kafka with aiokafka
```python
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json

async def produce_event(topic: str, event: dict, key: str | None = None) -> None:
    producer = AIOKafkaProducer(
        bootstrap_servers="kafka:9092",
        value_serializer=lambda v: json.dumps(v).encode(),
        key_serializer=lambda k: k.encode() if k else None,
    )
    async with producer:
        await producer.send_and_wait(topic, value=event, key=key)

async def consume_events(topic: str, group_id: str, handler: Callable) -> None:
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers="kafka:9092",
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode()),
        enable_auto_commit=False,  # manual commit for at-least-once
    )
    async with consumer:
        async for msg in consumer:
            try:
                await handler(msg.value)
                await consumer.commit()
            except Exception:
                logger.exception("Failed to process message", extra={"offset": msg.offset})
                # Don't commit — will be redelivered
```
