---
name: domain-entity-typed-ids
description: Determine how to type domain entity identifiers based on the project's type system. Use when an agent needs to create, modify, review, or interpret the type of a domain entity's identifier. In languages with a nominal type system, use typed IDs — a distinct type per domain entity that wraps the underlying identifier type. In languages with a structural type system, use typed IDs only if the language offers a low-friction mechanism to make them nominally distinct. Otherwise, use the underlying identifier type directly.
---

# Domain Entity Typed IDs

## Goal

Choose the right level of type distinction for domain entity identifiers based on whether the project's type system is nominal or structural.

In a nominal type system, two types with the same structure are distinct if they have different names. A typed ID — a dedicated type per domain entity wrapping the underlying identifier — provides compile-time safety against mixing identifiers of different entities at no meaningful cost.

In a structural type system, two types with the same structure are interchangeable regardless of their names. A typed ID only provides safety if the language offers a low-friction mechanism to make the types nominally distinct. If achieving nominal distinction requires patterns that add significant boilerplate, ceremony, or ergonomic friction, use the underlying identifier type directly instead.

## What Counts as In Scope

Apply this skill to code that does one or more of these things:

- defines the type of a domain entity's identifier
- introduces a new domain entity that needs an identifier type
- changes or refactors how a domain entity's identifier is typed
- reviews whether an identifier type provides appropriate type safety for the project's type system

## The Rule

1. In nominal type systems, use typed IDs.
   - Define a distinct type per domain entity that wraps the underlying identifier type.
   - Use the language's idiomatic lightweight wrapper — inline classes, value classes, newtypes, or the equivalent.
   - The typed ID ensures that identifiers of different entities are incompatible at compile time.

2. In structural type systems, assess friction before choosing.
   - If the language offers a low-friction mechanism to make structurally identical types nominally distinct — and that mechanism does not add significant boilerplate to construction, serialization, or persistence — use typed IDs.
   - If achieving nominal distinction requires patterns that are verbose, non-idiomatic, or poorly supported by the ecosystem — such as branded types that need manual casting, custom constructors, and special serialization handling — use the underlying identifier type directly.

3. When using the underlying type directly, rely on parameter naming for clarity.
   - Name parameters and fields clearly — `customerId`, `orderId` — so the intent is readable even without type distinction.
   - Accept that the compiler will not catch accidental ID swaps in this case.

4. Do not mix approaches within the same project.
   - All domain entity identifiers in a project must follow the same convention — either all typed IDs or all underlying type.
   - Follow the project's established convention. If no convention exists, choose based on the rules above and apply consistently.

## Detection Workflow

1. Determine the type system of the project's language.
   - Nominal: Kotlin, Java, Scala, Rust, Swift, C#, Go, Haskell — types are distinct by name.
   - Structural: TypeScript, Python, Elixir, Clojure — types are interchangeable if structurally identical.

2. Check the project's existing convention.
   - Look for how existing domain entity IDs are typed.
   - If a convention exists, follow it.

3. If no convention exists, apply the rule.
   - Nominal type system → use typed IDs.
   - Structural type system → assess whether a low-friction mechanism exists for nominal distinction. If yes, use typed IDs. If no, use the underlying type directly.

## Writing or Changing Domain Entity ID Types

1. For nominal type systems — define a typed ID per domain entity:

   ```kt
   // Kotlin — inline value class
   @JvmInline
   value class OrderId(val value: UUID)

   @JvmInline
   value class CustomerId(val value: UUID)
   ```

   ```java
   // Java — record
   public record OrderId(UUID value) {}
   public record CustomerId(UUID value) {}
   ```

   ```rs
   // Rust — newtype
   pub struct OrderId(pub Uuid);
   pub struct CustomerId(pub Uuid);
   ```

   ```swift
   // Swift — struct wrapper
   struct OrderId: Hashable {
       let value: UUID
   }

   struct CustomerId: Hashable {
       let value: UUID
   }
   ```

   ```cs
   // C# — readonly record struct
   public readonly record struct OrderId(Guid Value);
   public readonly record struct CustomerId(Guid Value);
   ```

   ```go
   // Go — named type
   type OrderId uuid.UUID
   type CustomerId uuid.UUID
   ```

2. For structural type systems where typed IDs add friction — use the underlying type:

   ```ts
   // TypeScript — use the underlying type directly
   class Order {
     readonly id: string
     readonly customerId: string
   }
   ```

   ```py
   // Python — use the underlying type directly
   @dataclass(frozen=True)
   class Order:
       id: UUID
       customer_id: UUID
   ```

3. For structural type systems where a low-friction mechanism exists — use typed IDs:

   ```ts
   // TypeScript with a library like ts-brand or a project convention
   // that makes branded types ergonomic — use typed IDs
   type OrderId = Brand<string, 'OrderId'>
   type CustomerId = Brand<string, 'CustomerId'>
   ```

## Examples

Nominal type system — typed IDs prevent accidental swaps at compile time:

```kt
fun assignOrderToCustomer(orderId: OrderId, customerId: CustomerId) { /* ... */ }

val orderId = OrderId(UUID.randomUUID())
val customerId = CustomerId(UUID.randomUUID())

assignOrderToCustomer(orderId, customerId)       // compiles
assignOrderToCustomer(customerId, orderId)        // compile error
```

Structural type system without low-friction mechanism — rely on naming:

```ts
const assignOrderToCustomer = (orderId: string, customerId: string) => { /* ... */ }

// The compiler does not catch this swap — naming discipline is the safeguard
assignOrderToCustomer(orderId, customerId)
```

## Review Questions

When reading or reviewing code, ask:

- Is the project's type system nominal or structural?
- If nominal, are domain entity IDs defined as distinct typed IDs?
- If structural, does the project use a low-friction mechanism for nominal distinction, or does it use the underlying type directly?
- Is the approach consistent across all domain entity identifiers in the project?
- If typed IDs are used in a structural type system, do they add significant boilerplate or friction?

If the approach does not match the type system and project conventions, apply this skill.

## Report the Outcome

When finishing the task:

- state the project's type system classification — nominal or structural
- state which domain entity ID types were created or changed
- state whether typed IDs or the underlying type was used, and why
- state whether the approach is consistent with the rest of the project
