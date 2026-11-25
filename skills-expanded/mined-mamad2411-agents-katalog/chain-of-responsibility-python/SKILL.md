---
name: chain-of-responsibility-python
description: Implements the Chain of Responsibility pattern in Python. Use when the user mentions chain of responsibility, CoR, or when you need to chain handlers that each process and pass to the next—validation pipelines, processing steps, transformation chains, or any sequential pipeline.
---

# Chain of Responsibility (Python)

**Why:** Chain of Responsibility lets you pass a request (or context) along a chain of handlers. Each handler decides whether to process it and pass to the next, or short-circuit. You avoid one big function with all steps and keep each step in its own class ([Refactoring.Guru](https://refactoring.guru/design-patterns/chain-of-responsibility)).

**Hard constraints:** Handlers share a single interface (e.g. `handle(context)`). Each handler holds a reference to the next; the client composes the chain. A handler either processes and passes, or passes without processing.

---

## When to use

- **Validation:** Multi-rule validation (required → format → range) where you want to add or reorder rules without editing a single validator.
- **Any sequential pipeline:** Processing steps, transformation chains, or multi-step checks where order matters and each step can process and pass (or stop).
- You want to decouple the sender from concrete handlers and add or reorder steps without changing existing code (Single Responsibility; Open/Closed).

---

## Structure

| Role | Responsibility |
|------|-----------------|
| **Handler (protocol/ABC)** | Declares `handle(context)` (and optionally `set_next(next)`). All concrete handlers implement this. |
| **Base handler (optional)** | Holds `_next` reference; default `handle()` forwards to `_next` if present. Reduces boilerplate. |
| **Concrete handlers** | Implement `handle()`. Process the context (e.g. add errors, transform, check); call `self._next.handle(context)` or return. |
| **Client** | Builds the chain (e.g. `a.set_next(b).set_next(c)`) and invokes the first handler with the initial context. |

A context object is passed through the chain; handlers read it, optionally mutate it, and pass it along (e.g. for validation: `value`, `field_name`, `errors`).

---

## Code contrast (validation example)

Validation is a common use; the same structure applies to any chain. Below: validation.

### ❌ ANTI-PATTERN: One function with all rules

```python
# One function; every new rule forces edits.
def validate_order_input(data: OrderInput) -> list[dict]:
    errors = []
    if not (data.email or "").strip():
        errors.append({"field": "email", "message": "email is required"})
    elif not re.match(r"^[^@]+@[^@]+\.\w+$", data.email):
        errors.append({"field": "email", "message": "invalid email"})
    if data.amount is None or not (1 <= data.amount <= 10000):
        errors.append({"field": "amount", "message": "amount must be 1-10000"})
    return errors
```

Problems: order and logic are hardcoded; adding/removing a rule touches this function; rules are hard to test in isolation; violates Open/Closed.

### ✅ TOP-CODER PATTERN: Validator protocol + base handler + concrete validators + client-built chain

**Validator protocol and context:**

```python
# validators/base.py
from typing import Protocol, runtime_checkable, Optional
from dataclasses import field, dataclass

@runtime_checkable
class Validator(Protocol):
    def validate(self, context: "ValidationContext") -> None: ...
    def set_next(self, next_validator: "Validator") -> "Validator": ...

@dataclass
class ValidationContext:
    value: any
    field_name: str
    errors: list = field(default_factory=list)

class BaseValidator:
    def __init__(self) -> None:
        self._next: Optional[Validator] = None

    def set_next(self, next_validator: Validator) -> Validator:
        self._next = next_validator
        return next_validator

    def validate(self, context: ValidationContext) -> None:
        if self._next:
            self._next.validate(context)
```

**Concrete validators** (each does one check, then passes):

```python
# validators/required.py
from .base import BaseValidator, ValidationContext

class RequiredValidator(BaseValidator):
    def validate(self, context: ValidationContext) -> None:
        if context.value is None or str(context.value).strip() == "":
            context.errors.append({
                "field": context.field_name,
                "message": f"{context.field_name} is required",
            })
        super().validate(context)

# validators/email_format.py
import re
EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.\w+$")

class EmailFormatValidator(BaseValidator):
    def validate(self, context: ValidationContext) -> None:
        if context.value and not EMAIL_RE.match(str(context.value)):
            context.errors.append({"field": context.field_name, "message": "invalid email format"})
        super().validate(context)

# validators/range.py
class RangeValidator(BaseValidator):
    def __init__(self, min_val: float, max_val: float) -> None:
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, context: ValidationContext) -> None:
        try:
            n = float(context.value) if context.value is not None else None
        except (TypeError, ValueError):
            n = None
        if context.value is not None and (n is None or n < self.min_val or n > self.max_val):
            context.errors.append({
                "field": context.field_name,
                "message": f"must be between {self.min_val} and {self.max_val}",
            })
        super().validate(context)
```

**Client** (e.g. service or FastAPI dependency) builds one chain per field and runs it:

```python
# services/order_validation.py
from validators.required import RequiredValidator
from validators.email_format import EmailFormatValidator
from validators.range import RangeValidator
from validators.base import ValidationContext

email_chain = RequiredValidator()
email_chain.set_next(EmailFormatValidator())

amount_chain = RequiredValidator()
amount_chain.set_next(RangeValidator(1, 10_000))

def validate_order_input(data: OrderInput) -> list[dict]:
    ctx = ValidationContext(value=None, field_name="", errors=[])
    ctx.value, ctx.field_name = data.email, "email"
    email_chain.validate(ctx)
    ctx.value, ctx.field_name = data.amount, "amount"
    amount_chain.validate(ctx)
    return ctx.errors
```

Benefits: add or reorder validators by composing the chain; each validator is a single class, easy to unit test.

---

## Python notes

- **Validation context:** Use a dataclass or simple class with `value`, `field_name`, and `errors: list` so validators append to the same list. For fail-fast, skip calling `super().validate(context)` when a validator adds an error.
- **Protocol vs ABC:** Prefer `typing.Protocol` for the validator contract; use `BaseValidator` only for the common “forward to next” logic.
- **Chaining:** `set_next` can return the next validator so the client can write `required.set_next(email_format).set_next(amount_range)`.
- **Modules:** One module per validator when logic is non-trivial (e.g. `validators/email_format.py`); keep protocol and base in `validators/base.py`.
- **No overkill:** For one or two fixed steps, a simple function may be enough; use CoR when you have many steps or dynamic composition.
- **General chains:** Same pattern works for non-validation pipelines (e.g. data transformation, enrichment, multi-step processing)—use a context that fits the domain and handlers that process and pass.

---

## Pipeline vs Chain of Responsibility

| Feature | Pipeline | Chain of Responsibility |
|---------|----------|--------------------------|
| **Execution** | Fixed, mandatory sequence | Conditional; handler decides whether to pass to the next |
| **Flow** | Linear, no branching | Allows flexible termination and branching |
| **Termination** | Runs to completion (barring errors) | Can be terminated early by a handler |
| **Use cases** | Data processing, parsing, ETL | Event handling, approval workflows, validation, message filtering |

Use **Pipeline** when every stage must run in a fixed order (e.g. data transformation: parse → normalize → enrich → serialize). Use **CoR** when handlers can short-circuit or decide not to pass (e.g. validation, approval chains).

---

## Reference

- [Chain of Responsibility — Refactoring.Guru](https://refactoring.guru/design-patterns/chain-of-responsibility): intent, problem/solution, structure, applicability, pros/cons, relations with Command/Decorator/Composite.
