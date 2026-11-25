---
name: value-objects
description: "[Pragmatic DDD Architecture] Guide for creating DDD Value Objects (VOs). Use when defining a new Value Object in a domain layer. Covers immutability patterns, private constructors, random/from builders, Railway-oriented error handling via neverthrow Result, TypeScript branded error types, and co-locating errors within the VO file."
---

# DDD Value Objects

## 1. Core Principles (RFC 2119)

Value Objects (VOs) in this project are immutable containers for domain primitives. They guarantee that an instantiated primitive is always valid according to business rules. 
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

- **Immutability**: Class properties MUST be `private readonly`. No setters are allowed. Operations that "change" a VO MUST return a new instance.
- **Encapsulation**: Constructors MUST be `private`.
- **Creation via Static Methods**: You MUST use `static from(value: T)` to instantiate. You MAY use `static random()` for testing or generation (like generating a new UUID).
- **Railway-Oriented Validation**: The `from()` method MUST NOT throw. Instead, it MUST return a `Result<MyVO, InvalidMyVOError>` using `neverthrow`.
- **Validation Isolation**: You MUST provide a `static checkValidity(value: T): boolean` method. This allows external validation checks without instantiation.
- **Helper Functions**: Value Objects MAY contain pure helper functions that evaluate or mutate algebraically (e.g., `isGreaterThan(other: ValueObject)`, `add(other: ValueObject)`, `equals(other: ValueObject)`). These logic-heavy domain methods are encouraged inside VOs.
- **Value Extraction & Branded Types**: VOs MUST export a Branded Primitive Type and MUST only use a `.toBranded()` method to extract the raw value when crossing boundaries (e.g., Server Action boundaries returning to the client).

## 2. Permitted "Infrastructure" Dependencies in the Domain

While the domain layer is theoretically pure, implementing complex specification parsers (like UUID, Email, or URL) from scratch is unviable and error-prone. Therefore, the following "infrastructure" libraries are strictly considered extensions of our domain and MUST be used when needed:

- **UUID (v7)**: If a Value Object requires UUID generation or validation, it MUST use UUID version 7 (via an external library like `uuid`). You MUST NOT implement your own UUID generator.
- **Zod**: You MAY use `zod` internally in `checkValidity()` for complex structural validation (e.g., `z.uuid()`, `z.email()`, or `z.url()`).
- **Neverthrow**: The `Result` type is central to our domain architecture.

## 3. Branded Types & Error Mapping

Errors related to a specific VO (e.g., parsing/validation errors) MUST be defined in the **same file** as the VO. This keeps domain meaning perfectly coupled.

All domain errors MUST use TypeScript branding to allow for safe `instanceof` narrowing.
Additionally, the primitive value itself MUST be branded so external clients/layers (like ORMs or UI) receive type-safe validated strings/numbers.

```typescript
declare const uniqueBrand: unique symbol;
export type BrandedDomainConcept = string & { readonly [uniqueBrand]: never };

declare const uniqueError: unique symbol;
export class InvalidDomainConceptError extends Error {
  declare private readonly [uniqueError]: never;
  private readonly invalidValue: string;
  // ...
}
```

## 4. Structure of a Value Object

Here is the perfect template for a Value Object in this architecture.

### Example Implementation

```typescript
import { Result, ok, err } from "neverthrow";
import { z } from "zod";

// 1. Primitive Branded Type
declare const brandedTopicNameSymbol: unique symbol;
export type BrandedTopicName = string & { readonly [brandedTopicNameSymbol]: never };

// 2. Co-located Error Class
declare const unique: unique symbol;

export class InvalidTopicNameError extends Error {
  declare private readonly [unique]: never;
  private readonly invalidValue: string;

  constructor(invalidValue: string) {
    super(`The topic name "${invalidValue}" is invalid.`);
    this.invalidValue = invalidValue;
  }

  getInvalidValue(): string {
    return this.invalidValue;
  }
}

// 3. The Value Object
export class TopicName {
  static readonly MIN_LENGTH = 3;
  static readonly MAX_LENGTH = 50;

  // Immutability
  private readonly value: string;

  // Private constructor
  private constructor(value: string) {
    this.value = value.trim();
  }

  // Pure validation check
  static checkValidity(value: string): boolean {
    const trimmed = value.trim();
    // Zod can be used for things like z.email().safeParse(value).success
    return trimmed.length >= TopicName.MIN_LENGTH && trimmed.length <= TopicName.MAX_LENGTH;
  }

  // Instantiation via Result pattern
  static from(value: string): Result<TopicName, InvalidTopicNameError> {
    const trimmed = value.trim();
    
    if (!TopicName.checkValidity(trimmed)) {
      return err(new InvalidTopicNameError(trimmed));
    }
    
    return ok(new TopicName(trimmed));
  }

  // Test / System generation
  static random(): TopicName {
    return new TopicName(`topic-${Math.floor(Math.random() * 10000)}`);
  }

  // Safe extraction for cross-boundary serialization and queries
  toBranded(): BrandedTopicName {
    return this.value as BrandedTopicName;
  }
}
```

## 5. Helpful References

Rather than providing every variant of helper logic in this document, we rely on concrete reference files built from actual DDD project specifications provided in the `.agents/skills/value-objects/references/` folder. Ensure you read these files to copy the robust structure:

- [Positive Integer VO](references/positiveInteger.md): Example of a numeric VO featuring extensive helper/domain operations (`isGreaterThan`, `add`, `subtract`, `min`, `max`).
- [Folder Name VO](references/folderName.md): Example of string constraints based on bounds mapping (business rules).
- [UUID VO](references/uuid.md): Example of infrastructure dependency usage inside the domain (generating and validating UUIDv7).
- [Email VO](references/email.md): Example of using `zod` locally in the domain specifically strictly for standard formatting checks (`z.email()`).