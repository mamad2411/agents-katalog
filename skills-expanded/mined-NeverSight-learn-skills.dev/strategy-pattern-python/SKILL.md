---
name: strategy-pattern-python
description: Implements the Strategy pattern in Python backends. Run when the user mentions strategy pattern, or when you see or need a switch on type/method, multiple behaviors under the same contract, or interchangeable algorithms—apply this skill proactively without the user naming it.
---

# Strategy Pattern (Python Backend)

**Why:** Strategy lets you define a family of algorithms, put each in a separate class, and make them interchangeable so the context stays stable while behavior is swapped at runtime ([Refactoring.Guru](https://refactoring.guru/design-patterns/strategy)).

**Hard constraints:** Context must depend only on a strategy protocol/ABC, not concrete implementations. Use composition (context holds a strategy reference); avoid inheritance for variant behavior. Keep each strategy in its own class/module when it has real logic.

---

## When to use

- Different variants of the same algorithm (e.g. payment methods, route builders, serializers) and you want to switch at runtime.
- A class is bloated with conditionals (e.g. `if method == "card": ... elif method == "paypal": ...`); extract each branch into a strategy.
- You need to isolate algorithm details from the rest of the backend logic (Open/Closed: add strategies without changing context).

---

## Structure

| Role | Responsibility |
|------|-----------------|
| **Context** | Holds a reference to one strategy; delegates the varying work to it; exposes a setter (or constructor) so clients can inject/replace the strategy. |
| **Strategy (protocol/ABC)** | Common contract for all strategies (e.g. single method like `execute(data)` or `build_route(origin, dest)`). |
| **Concrete strategies** | Implement the protocol/ABC; each encapsulates one variant of the algorithm. |
| **Client** | Chooses a concrete strategy and passes it to the context (e.g. from request params, config, or factory). |

Context does not know concrete strategy types—only the interface.

---

## Code contrast

### ❌ ANTI-PATTERN: Bloated handler with conditionals

```python
# One big class; every new payment method forces edits here.
class PaymentService:
    def process_payment(self, amount: float, method: str, details: dict) -> dict:
        if method == "stripe":
            return self._stripe_charge(amount, details)
        if method == "paypal":
            return self._paypal_charge(amount, details)
        if method == "bank":
            return self._bank_transfer(amount, details)
        raise ValueError("Unknown method")

    def _stripe_charge(self, amount: float, details: dict) -> dict: ...
    def _paypal_charge(self, amount: float, details: dict) -> dict: ...
    def _bank_transfer(self, amount: float, details: dict) -> dict: ...
```

Problems: context grows with every variant; touching one method risks breaking others; hard to test in isolation; violates Open/Closed.

### ✅ TOP-CODER PATTERN: Strategy protocol + concrete strategies + context

**Strategy protocol** (contract):

```python
# strategies/payment_strategy.py
from typing import Protocol, runtime_checkable

@runtime_checkable
class PaymentStrategy(Protocol):
    def execute(self, amount: float, details: dict) -> dict:
        """Return dict with at least 'id' key."""
        ...
```

**Concrete strategies** (one variant per class):

```python
# strategies/stripe_strategy.py
class StripeStrategy:
    def execute(self, amount: float, details: dict) -> dict:
        payment_intent = stripe.PaymentIntent.create(amount=amount, **details)
        return {"id": payment_intent.id}

# strategies/paypal_strategy.py
class PaypalStrategy:
    def execute(self, amount: float, details: dict) -> dict:
        order = paypal_client.orders.create(amount=amount, **details)
        return {"id": order.id}
```

**Context** (depends only on the protocol):

```python
# services/payment_context.py
class PaymentContext:
    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def process_payment(self, amount: float, details: dict) -> dict:
        return self._strategy.execute(amount, details)
```

**Client** (e.g. FastAPI route) selects strategy and calls context:

```python
# routes/payments.py
strategies: dict[str, PaymentStrategy] = {
    "stripe": StripeStrategy(),
    "paypal": PaypalStrategy(),
}
context = PaymentContext(strategies["stripe"])

@router.post("/pay")
def pay(body: PayBody) -> dict:
    strategy = strategies.get(body.method, strategies["stripe"])
    context.set_strategy(strategy)
    return context.process_payment(body.amount, body.details)
```

Benefits: add new payment methods by adding a new strategy class and registering it; context and other strategies stay unchanged; each strategy is easy to unit test.

---

## Python backend notes

- **Protocol vs ABC:** Prefer `typing.Protocol` for structural subtyping (no inheritance required). Use `abc.ABC` when you need a shared base with default or mixin behavior.
- **Async:** If strategies do I/O, use `async def execute(...)` and `AsyncPaymentStrategy`; context awaits and returns. Keep sync and async protocol/contexts separate if you mix both.
- **DI:** Inject the strategy (or a strategy factory) into the context so tests can pass mocks or fakes; works well with FastAPI dependencies or Django injection.
- **Modules:** One module per concrete strategy when logic is non-trivial (e.g. `strategies/stripe_strategy.py`); keep the protocol in a shared module (e.g. `strategies/base.py` or `strategies/payment_strategy.py`).
- **No overkill:** If you only have one or two fixed algorithms and they rarely change, a simple conditional or single implementation may be enough; avoid extra classes for the sake of it.

---

## Reference

- [Strategy pattern — Refactoring.Guru](https://refactoring.guru/design-patterns/strategy): intent, problem/solution, structure, applicability, pros/cons, relations with State/Command/Template Method.
