---
name: specforge-types-dsl
description: "Write type definitions in .spec files (the type kind is declared by the builtin @specforge/software extension). Supports struct types with one `name Type` member per line and annotations (@readonly, @unique, @literal, @optional), union types (type X \"Title\" = a | b | c), and error types with the _tag pattern. Use when defining data shapes for domain entities, commands, errors, event payloads and value objects."
---

# SpecForge Types DSL

> **Declared by `@specforge/software`**, a builtin extension. The `type` kind exists only in a project that loads it:
> run `specforge extensions` first, and if it is not listed, do not write `type` blocks (add it with
> `specforge add @specforge/software`, or write the kinds the project's own extensions declare). `verify` needs
> `@specforge/testing`. `specforge infer-guide type` prints the fields.

Types define the data vocabulary: domain entities, commands, errors, value objects and event payloads. A type's body
is open: each line is a member, `name Type [annotations]`.

## Block Syntax

### Struct Type

```spec
type User "User" {
  id        string    @readonly @unique
  email     string    @unique
  name      string
  role      UserRole
  createdAt timestamp @readonly
  updatedAt timestamp @readonly

  verify unit "a user round-trips through JSON unchanged"
}
```

### Union Type

```spec
type UserRole "User Role" = admin | editor | viewer
```

A union may span lines, each continuation starting with `|`. Union types owe no `verify` obligation.

### Error Type (Tagged)

```spec
type DuplicateEmailError "Duplicate Email Error" {
  _tag    "DuplicateEmailError" @literal
  email   string
  message string
}
```

## Fields Reference

### Declared fields

| Field | Type | Description |
|-------|------|-------------|
| `extends` | reference -> type | Parent type this type extends. |
| `description` | string | Human-readable summary. |
| `refs` | string list | Declared `ref` IDs. |
| `composed_types` | reference list -> type | Derived from the member types; do not write it. |

Every other line in the body is a member: `name Type` followed by zero or more annotations.

### Member annotations

| Annotation | Meaning |
|------------|---------|
| `@readonly` | Set at creation, never modified after. |
| `@unique` | Unique across all instances of this type. |
| `@literal` | Fixed literal value (for tagged unions / discriminants). |
| `@optional` | May be absent. |

Another annotation is W010.

### Member types

Primitives: `string`, `number`, `integer`, `boolean`, `timestamp`, `date`, `float`, `object`. A member names one
type, a list `T[]` or a union `A | B`; a generic such as `Result<A, B>` is a port method's (a member does not parse
it, E001). A member naming no type is E004.

### Verify kinds

With `@specforge/testing`: `unit`, `property`.

## Relationships

| From | Field on the other entity |
|------|---------------------------|
| behavior | `types` |
| event | `payload` |
| port | its method signatures (derived `types`) |
| type | `extends`, or a member that names it |

## Writing Rules

1. **PascalCase names by convention** -- `User`, `CreateUserCommand`; any valid identifier is accepted.
2. **Suffix conventions** -- `*Command` for commands, `*Error` for errors, `*Payload` for event data.
3. **Use `_tag` + `@literal` for discriminated errors.**
4. **Use `@readonly` for identity and audit members**, `@unique` for business uniqueness.
5. **Every type needs a title** -- the string after the name (E076 otherwise), also for unions.

## Validation Rules

| Code | Owner | Rule |
|------|-------|------|
| E002 | core | Two types share an ID. |
| E076 | core | The type has no title. |
| E081 | core | A member written twice. |
| E004 | core | A member's type names no type and no primitive (a union body's variants are not checked). |
| W002 | software | No behavior, port or type references the type. |
| W010 | software | Unknown member annotation. |
| W004 | testing | A struct type with no `verify` obligation. |

## Examples

### Domain Entity

```spec
type Order "Order" {
  id         string    @readonly
  customerId string
  items      OrderItem[]
  status     OrderStatus
  total      number
  currency   string
  createdAt  timestamp @readonly
}
```

### Value Object

```spec
type OrderItem "Order Item" {
  productId string
  name      string
  quantity  integer
  unitPrice number
}
```

### Multi-line Union

```spec
type OrderStatus "Order Status" = pending
  | confirmed
  | shipped
  | delivered
  | cancelled
```

### Event Payload Type

```spec
type UserCreatedPayload "User Created Payload" {
  userId    string    @readonly
  email     string
  role      UserRole
  timestamp timestamp @readonly

  verify unit "round-trips through JSON unchanged"
}
```

## What NOT to Do

- Do not define operations on types -- use `port` blocks for methods
- Do not write `kind`, `fields` or `variants` lines -- the syntax itself says struct or union
- Do not mix type definitions with behavior contracts -- types are data shapes, behaviors are operations
