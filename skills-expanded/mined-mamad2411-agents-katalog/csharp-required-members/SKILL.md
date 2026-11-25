---
name: csharp-required-members
description: >
  Apply C# required members (required properties/fields, SetsRequiredMembers,
  RequiredMemberAttribute) for object initialization safety in owned .NET apps.
  Use when designing DTOs, options types, and domain objects that must be fully
  initialized via object initializers or constructors without null holes.
---

# C# Required Members

## Scope And Authorization

- **In scope:** C# 11+ codebases you maintain using `required` members.
- **Out of scope:** Disabling compiler safety globally to silence errors without design review.
- Prefer nullable reference types **on** alongside `required`.
- Pair with `csharp-style-conventions` and `code-quality-standards`.

## When To Use

- DTOs that must include certain properties at construction/initializer time.
- Replacing “forgot to set property” runtime nulls with compile-time errors.
- Records / classes with object initializers used widely in app code.
- Interop with constructors via `[SetsRequiredMembers]`.
- JSON deserialization considerations for required properties.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| JSON schema design broadly | `json-schema-design` |
| Minimal API security | `csharp-minimal-apis-security` |
| Raw string literals | `csharp-raw-string-literals` |
| Style only | `csharp-style-conventions` |
| Implementation quality baseline | `code-quality-standards` |

## Language model

| Feature | Behavior |
| --- | --- |
| `required` property | Must be set by object initializer or constructor marked appropriately |
| `required` field | Same for fields (less common in modern style) |
| `[SetsRequiredMembers]` | Constructor promises all required members assigned |
| Nullable annotations | Orthogonal: `required string Name` vs `string?` |

## Workflow

### 1. Confirm scope and success criteria

1. Types that are frequently partially initialized.
2. Success: compiler blocks incomplete initializers; serializers documented; tests cover construction paths.

### 2. Introduce required on DTOs

```csharp
public sealed class CreateUserRequest
{
    public required string Email { get; init; }
    public required string DisplayName { get; init; }
    public string? Title { get; init; }
}

// OK
var r = new CreateUserRequest
{
    Email = "a@example.com",
    DisplayName = "Ada",
};

// Compile error if Email omitted
```

### 3. Constructors and SetsRequiredMembers

```csharp
public sealed class User
{
    public required string Id { get; init; }
    public required string Email { get; init; }

    [SetsRequiredMembers]
    public User(string id, string email)
    {
        Id = id;
        Email = email;
    }
}
```

Only mark constructors that truly set **all** required members; incorrect use hides bugs.

### 4. Inheritance

1. Derived types may add more `required` members.
2. Object initializers must satisfy the full chain.
3. Prefer composition if required member hierarchies become painful.

### 5. JSON / model binding

```csharp
// System.Text.Json: required properties interact with deserialization
// Missing JSON properties may throw / fail depending on options and version
// Validate explicitly in Minimal APIs after bind
```

1. Confirm STJ settings (`PreferredObjectCreationHandling`, etc.) for your TFM.
2. For APIs: still validate with data annotations / FluentValidation — do not rely on `required` alone for untrusted JSON.
3. For `options` pattern: `ValidateOnStart` + data annotations remain useful.

### 6. Migration tactics

1. Add `required` to new types first.
2. For existing types, fix call sites incrementally; use constructor factories where initializers are sprawling.
3. Avoid `required` on EF Core entities if materialization conflicts — prefer domain DTOs.

### 7. Verify

```bash
dotnet build
dotnet test
# Ensure intentional incomplete initializer fails compile in a sandbox if documenting
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| DTO init | `required` + `init` | Optional props that are secretly mandatory |
| Constructor | `[SetsRequiredMembers]` truthful | Attribute without assigning all |
| API trust | required + validation | required only, trust JSON |
| Entities | Careful with ORMs | Break EF proxies with required init blindly |
| Nullable | `required string` non-null | `required string?` without reason |

## Output Checklist

- [ ] Critical DTOs use `required` where appropriate
- [ ] Constructor attributes audited
- [ ] Call sites compile under NRT
- [ ] JSON/ORM interactions tested
- [ ] Validation still present for untrusted input
- [ ] Style conventions followed
- [ ] Docs/examples updated
- [ ] No blanket safety disable
- [ ] Tests cover construction
- [ ] Residual gaps documented

## Rules

- `required` is compile-time initialization discipline, not full input validation.
- Be honest with `[SetsRequiredMembers]`.
- Focus on **C# required members** design and migration.
