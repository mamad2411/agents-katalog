---
name: specforge-behaviors-dsl
description: "Write behavior blocks in .spec files (the behavior kind is declared by the builtin @specforge/software extension). Each behavior declares one operation's contract with a snake_case ID, a contract statement using RFC 2119 keywords, links to invariants, types, ports, events and features, verify obligations (with @specforge/testing) and Design-by-Contract blocks requires/ensures/maintains (with @specforge/formal). Use when specifying what exactly a system does in a specific situation."
---

# SpecForge Behaviors DSL

> **Declared by `@specforge/software`**, a builtin extension. The `behavior` kind exists only in a project that
> loads it: run `specforge extensions` first, and if it is not listed, do not write `behavior` blocks (add it with
> `specforge add @specforge/software`, or write the kinds the project's own extensions declare). `verify` needs
> `@specforge/testing`; `requires`/`ensures`/`maintains`/`satisfies`/`abstract`/`refines`/`sync` need `@specforge/formal`.
> `specforge infer-guide behavior` prints the fields the loaded extensions declare.

Behaviors are the atomic unit of a software specification: each one describes a single operation, what it guarantees,
and what a test must prove about it.

Prefer typed edits over writing the block by hand: `specforge new behavior <id> "<title>" --in spec/<file>.spec
--contract "…" --category command`, then `specforge link <id> invariants <invariant>` and
`specforge link <id> --verify unit:"…"`.

## Block Syntax

```spec
behavior create_user "Create User" {
  category   command
  features   [user_management]
  invariants [email_uniqueness]
  types      [User, CreateUserCommand, DuplicateEmailError]
  ports      [UserRepository]
  produces   [user_created]

  contract """
    When a valid CreateUserCommand is received,
    the system MUST create a user record with a unique email
    and MUST return Result<User, DuplicateEmailError>.
  """

  requires {
    valid_command   "CreateUserCommand passes schema validation"
    email_available "no active user exists with the same email"
  }

  ensures {
    user_created    "a new User record exists in the datastore"
    email_unique    "email uniqueness holds after insertion"
  }

  verify unit        "insert user, retrieve by ID, assert equal"
  verify integration "insert user, restart process, the user persists"
  verify property    "email uniqueness holds under concurrent inserts"
}
```

## Fields Reference

`@specforge/software` declares:

| Field | Type | Description |
|-------|------|-------------|
| `contract` | string (required) | The behavioral contract, with RFC 2119 keywords (MUST, MUST NOT, SHOULD, MAY). |
| `category` | identifier | Classification for agent task routing, e.g. `command`, `query`, `handler`. Missing: W006. |
| `features` | reference list -> feature | Features this behavior implements (needs `@specforge/product` for the `feature` kind). |
| `invariants` | reference list -> invariant | Invariants this behavior enforces. |
| `types` | reference list -> type | Types this behavior uses. |
| `ports` | reference list -> port | Ports this behavior interacts with. |
| `produces` | reference list -> event | Events this behavior emits. |
| `consumes` | reference list -> event | Events this behavior reacts to. |
| `description` | string | Human-readable summary. |
| `status` | identifier | Lifecycle status. |
| `severity` | identifier | Impact level if this behavior fails. |
| `diagnostic` | identifier | Diagnostic message for validation tooling. |
| `refs` | string list | External references: declared `ref` IDs such as `gh.issue:42`. |

`@specforge/formal` adds:

| Field | Type | Description |
|-------|------|-------------|
| `requires` | block | Named preconditions, one `name "text"` per line. |
| `ensures` | block | Named postconditions, one `name "text"` per line. |
| `maintains` | block | Named frame conditions that hold throughout execution. |
| `satisfies` | reference list -> property | Temporal properties this behavior satisfies. |
| `abstract` | bool | A specification-only behavior that concrete behaviors refine; it owes no verify obligations. |
| `refines` | reference -> behavior | The abstract behavior this one refines; it must keep its `ensures` (E031). |
| `sync` | block | Synchronization bound: barrier, timeout or delivery. |

### Verify kinds

With `@specforge/testing` loaded, a behavior takes `verify <kind> "<what a test must prove>"` with kind `unit`,
`contract`, `integration`, `property` or `performance` (another kind is W009). `verify "<text>"` without a kind is
also accepted.

## Relationships

A behavior writes every relation itself; the other side never lists the behavior (writing it there is E079).

| Field | Edge | Target |
|-------|------|--------|
| `features` | `BehaviorImplementsFeature` | feature |
| `invariants` | `BehaviorEnforcesInvariant` | invariant |
| `types` | `BehaviorReferencesType` | type |
| `ports` | `BehaviorUsesPort` | port |
| `produces` / `consumes` | `BehaviorProducesEvent` / `BehaviorConsumesEvent` | event |
| `satisfies` | `BehaviorSatisfiesProperty` | property (formal) |
| `refines` | refinement edge | behavior (formal) |

Run `specforge schema --kind behavior` for the exact edge list of the loaded extensions.

## Writing Rules

1. **One logical operation per behavior** -- if it has MUST clauses for different operations, split it.
2. **Contract pattern** -- trigger ("When X") -> action -> guarantee -> error cases.
3. **Add at least one `verify`** -- or W004 fires (with `@specforge/testing`).
4. **Name the features it implements** in `features` -- or W001 fires.
5. **Set `category`** -- or W006 fires.
6. **References resolve project-wide** -- a `use` import is optional; a name that does not exist is E003.
7. **Use `abstract`/`refines` for refinement** -- a concrete behavior keeps every `ensures` of the abstract one (E031).

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E003 | core | A referenced name does not exist. |
| E006 | core | `contract` is missing. |
| E079 | core | A relation written on its other side (e.g. a `behaviors` list on a feature). |
| W001 | software | Behavior implements no feature. |
| W006 | software | Behavior missing `category`. |
| W004 | testing | No `verify` obligation. |
| W009 | testing | A `verify` kind outside the allowed set. |
| E031 | formal | A refinement drops an `ensures` condition of its abstract behavior. |
| W030 | formal | An `abstract` behavior nothing refines. |
| W096 | formal | `requires` without `ensures`. |
| W110 | formal | `refines` names a behavior that is not `abstract true`. |

`specforge explain <code>` gives the full text of any code.

## Examples

### Simple Query

```spec
behavior read_user_by_id "Read User by ID" {
  category   query
  features   [user_management]
  invariants [email_uniqueness]

  contract """
    Given a valid user ID,
    the system MUST return the user record or UserNotFoundError.
    MUST NOT return stale data after a successful write.
  """

  verify unit "insert then get by ID"
}
```

### Abstract Behavior with Refinement (needs `@specforge/formal`)

```spec
behavior process_payment "Process Payment" {
  category command
  abstract true

  contract """
    The system MUST process a payment and return a receipt
    or a PaymentFailedError.
  """

  requires {
    valid_amount "payment amount is positive"
  }

  ensures {
    receipt_returned "a valid receipt is returned on success"
    idempotent       "retrying the same payment ID is safe"
  }
}

behavior process_card_payment "Process Card Payment" {
  category command
  features [order_checkout]
  refines  process_payment

  contract """
    The system MUST process a payment through the card processor.
  """

  ensures {
    receipt_returned "a valid receipt is returned on success"
    idempotent       "retrying the same payment ID is safe"
  }

  verify unit     "a successful charge returns a receipt"
  verify unit     "a declined card returns PaymentFailedError"
  verify contract "the concrete behavior keeps the abstract ensures"
}
```

### Event-Producing Behavior

```spec
behavior place_order "Place Order" {
  category   command
  features   [order_checkout]
  invariants [inventory_accuracy]
  produces   [order_placed]

  contract """
    When a valid PlaceOrderCommand is received,
    the system MUST validate inventory availability,
    reserve items, create an order record,
    and MUST emit an order_placed event.
    MUST return Result<Order, InsufficientInventoryError>.
  """

  verify unit        "place order with available items"
  verify unit        "reject order when items are unavailable"
  verify integration "concurrent orders for the last item -- exactly one succeeds"
}
```

## What NOT to Do

- Do not write a behavior for a property ("No two users share the same ID" is an invariant)
- Do not write a `tests` field -- it is not declared; `specforge collect` records which tests prove which entities
- Do not use verify kinds the testing extension does not allow for behaviors (`e2e`, `refinement`, `load` are W009)
- Do not put implementation details in the `contract` -- describe what, not how
- Do not weaken an abstract behavior's `ensures` in a refinement (E031)
