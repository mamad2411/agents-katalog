---
name: dotnet-ef-migration
description: Manage EF Core migrations, entity configurations, and database schema for PostgreSQL. Use when user says "add migration", "database update", "entity configuration", "fluent API", "configure table", "EF Core mapping", "schema change", or asks about persistence layer. Do NOT use for domain logic or application features.
metadata:
  author: Claude-DotNet-Ultimate
  version: 1.0.0
  category: persistence
---

# EF Core Migrations & Configuration

## Migration Commands

```bash
# Create migration
dotnet ef migrations add <Name> --project src/Infrastructure --startup-project src/Api

# Apply migrations
dotnet ef database update --project src/Infrastructure --startup-project src/Api

# Remove last migration (if not applied)
dotnet ef migrations remove --project src/Infrastructure --startup-project src/Api

# Generate SQL script (for production)
dotnet ef migrations script --idempotent --project src/Infrastructure --startup-project src/Api
```

## Entity Configuration

Place in `src/Infrastructure/Persistence/Configurations/`:

```csharp
namespace ClaudeDotNetUltimate.Infrastructure.Persistence.Configurations;

public sealed class ProductConfiguration : IEntityTypeConfiguration<Product>
{
    public void Configure(EntityTypeBuilder<Product> builder)
    {
        builder.ToTable("products");

        builder.HasKey(p => p.Id);

        builder.Property(p => p.Id)
            .HasColumnName("id")
            .HasConversion(
                id => id.Value,
                value => ProductId.From(value));

        builder.Property(p => p.Name)
            .HasColumnName("name")
            .HasMaxLength(200)
            .IsRequired();

        builder.Property(p => p.IsActive)
            .HasColumnName("is_active")
            .HasDefaultValue(true);

        // Value Object: Money (owned entity)
        builder.OwnsOne(p => p.Price, priceBuilder =>
        {
            priceBuilder.Property(m => m.Amount)
                .HasColumnName("price_amount")
                .HasColumnType("decimal(18,2)")
                .IsRequired();

            priceBuilder.Property(m => m.Currency)
                .HasColumnName("price_currency")
                .HasMaxLength(3)
                .IsRequired();
        });

        // Indexes
        builder.HasIndex(p => p.Name);
        builder.HasIndex(p => p.IsActive);
        builder.HasIndex(p => p.CreatedAt);

        // Ignore computed properties
        builder.Ignore(p => p.DomainEvents);
    }
}
```

## Configuration Patterns

### Strongly-Typed ID Conversion
```csharp
builder.Property(x => x.Id)
    .HasConversion(id => id.Value, value => new ProductId(value));
```

### Value Object (Owned Entity)
```csharp
builder.OwnsOne(x => x.Address, addressBuilder =>
{
    addressBuilder.Property(a => a.Street).HasColumnName("shipping_street").HasMaxLength(200);
    addressBuilder.Property(a => a.City).HasColumnName("shipping_city").HasMaxLength(100);
    addressBuilder.Property(a => a.State).HasColumnName("shipping_state").HasMaxLength(50);
    addressBuilder.Property(a => a.PostalCode).HasColumnName("shipping_postal_code").HasMaxLength(20);
    addressBuilder.Property(a => a.Country).HasColumnName("shipping_country").HasMaxLength(100);
});
```

### One-to-Many Relationship
```csharp
builder.HasMany(o => o.Items)
    .WithOne()
    .HasForeignKey(i => i.OrderId)
    .OnDelete(DeleteBehavior.Cascade);
```

### Naming Conventions
- Tables: `snake_case` plural (`orders`, `order_items`)
- Columns: `snake_case` (`created_at`, `customer_id`)
- Indexes: auto-generated or explicit `IX_{table}_{column}`

## Adding a New Entity to DbContext

In `src/Infrastructure/Persistence/ApplicationDbContext.cs`:
```csharp
public DbSet<Product> Products => Set<Product>();
```

## Repository Pattern

In `src/Infrastructure/Persistence/Repositories/`:

```csharp
public sealed class ProductRepository(ApplicationDbContext context) : IProductRepository
{
    public async Task<Product?> GetByIdAsync(ProductId id, CancellationToken ct = default)
        => await context.Products.FirstOrDefaultAsync(p => p.Id == id, ct);

    public async Task AddAsync(Product product, CancellationToken ct = default)
        => await context.Products.AddAsync(product, ct);

    public void Update(Product product)
        => context.Products.Update(product);
}
```

## Rules

- **snake_case** for all table and column names
- **Value objects** mapped as owned entities
- **Strongly-typed IDs** use HasConversion
- **Never** use Include() in performance-critical paths — use projections
- **AsSplitQuery()** when multiple Includes cause cartesian explosion
- **AsNoTracking()** for read-only queries
- Ignore `DomainEvents` and computed properties
- Create indexes for frequently queried columns
- Use `HasColumnType("decimal(18,2)")` for money
