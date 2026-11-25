---
name: specforge-ports-dsl
description: "Write port interface blocks in .spec files (the port kind is declared by the builtin @specforge/software extension). Each port declares an interface contract with a direction (inbound/outbound/bidirectional), a category, and `method` signatures with typed parameters and Result return types. Use when defining boundaries between the domain and external systems in hexagonal architecture."
---

# SpecForge Ports DSL

> **Declared by `@specforge/software`**, a builtin extension. The `port` kind exists only in a project that loads it:
> run `specforge extensions` first, and if it is not listed, do not write `port` blocks (add it with
> `specforge add @specforge/software`, or write the kinds the project's own extensions declare). `verify` needs
> `@specforge/testing`. `specforge infer-guide port` prints the fields.

Ports define the boundaries in hexagonal architecture -- the "holes" that adapters plug into. Typed edits do not cover
`method` lines yet: write a port with methods by hand, then run `specforge check`.

## Block Syntax

```spec
port UserRepository "User Repository" {
  direction outbound
  category  "persistence/user"

  method create(cmd: CreateUserCommand) -> Result<User, DuplicateEmailError>
  method findById(id: string) -> Result<User, UserNotFoundError>
  method update(id: string, cmd: UpdateUserCommand) -> Result<User, UserUpdateError>
  method delete(id: string) -> Result<void, UserNotFoundError>

  verify integration "the SQL adapter satisfies the repository contract"
}
```

## Fields Reference

| Field | Type | Description |
|-------|------|-------------|
| `direction` | enum `inbound` `outbound` `bidirectional` (required) | Who calls whom. |
| `category` | string | A word or a path, e.g. `"persistence/user"`, `http`. |
| `methods` | block | The `method` lines of the body. |
| `types` | reference list -> type | Derived from the method signatures; do not write it. |
| `description` | string | Human-readable summary. |
| `refs` | string list | Declared `ref` IDs. |

### Direction

| Direction | Meaning | Examples |
|-----------|---------|----------|
| `inbound` | The outside world calls into the system (driving port) | `UserAPI`, `WebhookHandler` |
| `outbound` | The system calls out (driven port) | `UserRepository`, `EmailService` |
| `bidirectional` | Both | a websocket session |

### Method signatures

`method name(param: Type, other?: Type) -> ReturnType`

- `?` after a parameter name marks it optional.
- A type is a primitive (`string`, `number`, `integer`, `boolean`, `timestamp`, `date`), a declared `type`, an array
  (`Task[]`), a generic (`Result<Task, TaskError>`), the unit type `()`, or `void`/`never`.
- A type name that is not a primitive and not a declared `type` is E004.
- A return type takes no `?` and no `A | B` inside a generic: declare a union `type` for several errors.
- A method has no body: preconditions and postconditions belong on the behaviors that use the port (`requires` /
  `ensures`, from `@specforge/formal`).

### Verify kinds

With `@specforge/testing`: `integration`, `unit`.

## Relationships

A port lists no behaviors: behaviors name it in `ports`. With `@specforge/product` loaded, a module names the ports it
consumes (`ports`) and defines (`ports_defined`).

## Writing Rules

1. **PascalCase names by convention** -- `UserRepository`, `EmailService`, `PaymentGateway`.
2. **Naming** -- `{Entity}Repository` for persistence, `{Service}Service` or `{Service}Gateway` for external,
   `{Domain}API` for inbound.
3. **Return Result types** -- explicit errors, no thrown exceptions.
4. **One port per concern** -- do not mix persistence and messaging in one port.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E002 | core | Two ports share an ID. |
| E006 | core | `direction` is missing. |
| E061 | core | `direction` outside its enum. |
| E004 | core | A method names an unknown type. |
| W005 | software | No behavior uses the port. |
| W004 | testing | No `verify` obligation. |
| W033 | formal | Asymmetric connectivity between the behaviors that use the port (`specforge analyze`). |

## Examples

### Outbound: External Service

```spec
port EmailService "Email Service" {
  direction outbound
  category  "external/email"

  method send(to: string, template: EmailTemplate, data: EmailData) -> Result<void, EmailDeliveryError>
  method sendBulk(recipients: BulkEmailRequest) -> Result<BulkEmailResult, EmailDeliveryError>

  verify integration "a sandbox provider receives the message"
}
```

### Inbound: API Surface

```spec
port UserAPI "User API" {
  direction inbound
  category  "api/user"

  method createUser(cmd: CreateUserCommand) -> Result<User, DuplicateEmailError>
  method getUser(id: string) -> Result<User, UserNotFoundError>
  method listUsers(query: UserQuery, cursor?: string) -> Result<UserPage, never>

  verify unit "listUsers without a cursor returns the first page"
}
```

### Payment Gateway

```spec
port PaymentGateway "Payment Gateway" {
  direction outbound
  category  "external/payment"

  method charge(amount: Money, method: PaymentMethod) -> Result<Receipt, PaymentError>

  verify integration "a sandbox charge returns a receipt with a transaction ID"
}
```

## What NOT to Do

- Do not define behavioral contracts in ports -- ports define signatures, behaviors define semantics
- Do not give a method a `{ requires … ensures … }` body -- it does not parse; put conditions on the behavior
- Do not mix inbound and outbound concerns in a single port
