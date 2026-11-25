---
name: python-patterns-advanced
description: "When to activate: design patterns in Python, dependency injection, factory pattern, observer, command, strategy"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Advanced Python Design Patterns

## Dependency Injection with Containers
```python
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    db_engine = providers.Singleton(
        create_async_engine,
        url=config.database_url,
    )
    
    session_factory = providers.Factory(
        AsyncSession,
        bind=db_engine,
    )
    
    user_repo = providers.Factory(UserRepository, session=session_factory)
    user_service = providers.Factory(UserService, repo=user_repo)

container = Container()
container.config.from_pydantic(settings)

@inject
async def create_user_endpoint(
    body: UserCreate,
    service: UserService = Provide[Container.user_service],
) -> User:
    return await service.create(body)
```

## Factory Pattern
```python
from typing import Protocol

class Notifier(Protocol):
    async def send(self, recipient: str, message: str) -> bool: ...

class EmailNotifier:
    async def send(self, recipient: str, message: str) -> bool:
        return await send_email(to=recipient, body=message)

class SlackNotifier:
    async def send(self, recipient: str, message: str) -> bool:
        return await post_slack_message(channel=recipient, text=message)

class SMSNotifier:
    async def send(self, recipient: str, message: str) -> bool:
        return await send_sms(to=recipient, text=message)

NOTIFIERS: dict[str, type[Notifier]] = {
    "email": EmailNotifier,
    "slack": SlackNotifier,
    "sms": SMSNotifier,
}

def create_notifier(channel: str) -> Notifier:
    if channel not in NOTIFIERS:
        raise ValueError(f"Unknown channel: {channel}. Available: {list(NOTIFIERS)}")
    return NOTIFIERS[channel]()
```

## Observer Pattern (Event System)
```python
from collections import defaultdict
from typing import Callable, Awaitable

EventHandler = Callable[..., Awaitable[None]]

class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
    
    def subscribe(self, event: str, handler: EventHandler) -> None:
        self._handlers[event].append(handler)
    
    def on(self, event: str):
        def decorator(fn: EventHandler) -> EventHandler:
            self.subscribe(event, fn)
            return fn
        return decorator
    
    async def emit(self, event: str, **kwargs) -> None:
        for handler in self._handlers[event]:
            await handler(**kwargs)

bus = EventBus()

@bus.on("user.created")
async def send_welcome_email(user_id: int, email: str) -> None:
    await email_service.send_welcome(email)

@bus.on("user.created")
async def provision_resources(user_id: int, **kwargs) -> None:
    await resource_service.provision(user_id)

# Emit
await bus.emit("user.created", user_id=user.id, email=user.email)
```

## Strategy Pattern
```python
from typing import Protocol

class PricingStrategy(Protocol):
    def calculate(self, base_price: int, quantity: int) -> int: ...

class StandardPricing:
    def calculate(self, base_price: int, quantity: int) -> int:
        return base_price * quantity

class BulkPricing:
    def calculate(self, base_price: int, quantity: int) -> int:
        if quantity >= 10:
            return int(base_price * quantity * 0.9)
        return base_price * quantity

class Checkout:
    def __init__(self, pricing: PricingStrategy) -> None:
        self._pricing = pricing
    
    def total(self, base_price: int, quantity: int) -> int:
        return self._pricing.calculate(base_price, quantity)
```
