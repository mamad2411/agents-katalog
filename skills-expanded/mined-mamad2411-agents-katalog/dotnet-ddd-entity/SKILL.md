---
name: dotnet-ddd-entity
description: Create DDD domain entities, aggregate roots, value objects, and strongly-typed IDs following enterprise patterns. Use when user says "create entity", "add aggregate", "new value object", "domain model", "strongly-typed ID", or asks to model domain concepts. Do NOT use for DTOs, database models, or infrastructure concerns.
metadata:
  author: Claude-DotNet-Ultimate
  version: 1.0.0
  category: domain-driven-design
---

# DDD Entity Creation

## Base Classes (Already in Project)

This project uses these base classes in `src/Core/Common/`:

- `BaseEntity<TId>` — Generic entity with Id, audit fields, equality by Id
- `AggregateRoot<TId>` — Extends BaseEntity, collects domain events
- `ValueObject` — Abstract class with structural equality via `GetEqualityComponents()`
- `IDomainEvent` / `DomainEvent` — Base event with EventId + OccurredOn

## Creating a New Entity

### Step 1: Create Strongly-Typed ID

Place in `src/Core/Domain/Entities/`:

```csharp
namespace ClaudeDotNetUltimate.Core.Domain.Entities;

public readonly record struct ProductId(Guid Value)
{
    public static ProductId New() => new(Guid.NewGuid());
    public static ProductId From(Guid value) => new(value);
    public override string ToString() => Value.ToString();
}
```

### Step 2: Create Entity or Aggregate Root

For child entities (owned by an aggregate):
```csharp
namespace ClaudeDotNetUltimate.Core.Domain.Entities;

public sealed class OrderItem : BaseEntity<Guid>
{
    public OrderId OrderId { get; private set; }
    public string ProductName { get; private set; } = string.Empty;
    public Money UnitPrice { get; private set; }
    public int Quantity { get; private set; }
    public Money TotalPrice => Money.From(UnitPrice.Amount * Quantity, UnitPrice.Currency);

    private OrderItem() { }

    internal OrderItem(OrderId orderId, string productName, Money unitPrice, int quantity)
    {
        Id = Guid.NewGuid();
        OrderId = orderId;
        ProductName = productName;
        UnitPrice = unitPrice;
        Quantity = quantity;
    }
}
```

For aggregate roots:
```csharp
namespace ClaudeDotNetUltimate.Core.Domain.Entities;

public sealed class Product : AggregateRoot<ProductId>
{
    public string Name { get; private set; } = string.Empty;
    public Money Price { get; private set; }
    public bool IsActive { get; private set; }

    private Product() { }

    public static Product Create(string name, Money price)
    {
        var product = new Product
        {
            Id = ProductId.New(),
            Name = name,
            Price = price,
            IsActive = true
        };
        product.AddDomainEvent(new ProductCreatedEvent(product.Id, name));
        return product;
    }

    public void UpdatePrice(Money newPrice)
    {
        Price = newPrice;
        AddDomainEvent(new ProductPriceChangedEvent(Id, newPrice.Amount));
    }
}
```

## Rules

### Aggregate Root Rules
- Has a **factory method** (`Create()`) — never public constructors
- **Private parameterless constructor** for EF Core
- All **mutations** through methods, not property setters
- Raises **domain events** on state changes
- Contains **invariant enforcement** (business rules)
- Child entities created **only through the aggregate**

### Value Object Rules
- **Immutable** — use `readonly record struct` or sealed class extending `ValueObject`
- Override `GetEqualityComponents()` for structural equality
- Include **factory methods** with validation
- No identity — equality by value

```csharp
public sealed class Address : ValueObject
{
    public string Street { get; }
    public string City { get; }
    public string State { get; }
    public string PostalCode { get; }
    public string Country { get; }

    private Address(string street, string city, string state, string postalCode, string country)
    {
        Street = street; City = city; State = state;
        PostalCode = postalCode; Country = country;
    }

    public static Address Create(string street, string city, string state, string postalCode, string country)
    {
        if (string.IsNullOrWhiteSpace(street)) throw new ArgumentException("Street is required");
        return new Address(street, city, state, postalCode, country);
    }

    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Street; yield return City; yield return State;
        yield return PostalCode; yield return Country;
    }
}
```

### Strongly-Typed ID Rules
- Always `readonly record struct`
- Include `New()` and `From(Guid)` factory methods
- Override `ToString()`

## Checklist

- [ ] Strongly-typed ID created
- [ ] Private parameterless constructor for EF Core
- [ ] Factory method (not public constructor)
- [ ] All setters are `private set`
- [ ] Domain events raised on state changes
- [ ] Business rules enforced in entity methods
- [ ] Unit tests for all domain logic
