# Database Interactions with Drizzle for Logistics Agents

This project uses Drizzle ORM for all database operations related to logistics, shipping, and rate quoting. All database interactions must use the defined schema and follow Drizzle patterns.

## Schema Location

The database schema should be defined in [src/db/schema.ts](mdc:src/db/schema.ts) and should include logistics-specific tables:

- **ordersTable**: Order specifications with origin, destination, dimensions, weight, and requirements
- **quotesTable**: Rate quotes from carriers with pricing, transit time, and service levels
- **carriersTable**: Carrier information, capabilities, and contract rates
- **shipmentsTable**: Active shipments with status, tracking, and SLA monitoring
- **tendersTable**: Tender records with carrier selection and confirmation details
- **userProgressTable**: User interaction history and preference tracking

## Database Connection

The database connection should be configured in [src/db/index.ts](mdc:src/db/index.ts) using:
- PostgreSQL database (recommended: Neon, Supabase, or similar)
- Drizzle ORM wrapper
- Environment variable `DATABASE_URL` for connection string

## Required Patterns

### 1. Always Import Schema
```typescript
import { ordersTable, quotesTable, carriersTable, shipmentsTable, tendersTable } from "@/db/schema";
import { db } from "@/db";
```

### 2. Use Drizzle Query Builder
```typescript
// ✅ Correct - Using Drizzle queries
const orders = await db.select().from(ordersTable).where(eq(ordersTable.userId, userId));

// ❌ Incorrect - Raw SQL
const orders = await db.execute(sql`SELECT * FROM orders WHERE user_id = ${userId}`);
```

### 3. Import Required Drizzle Functions
```typescript
import { eq, and, or, desc, asc, count, sum, gte, lte, like } from "drizzle-orm";
```

### 4. Follow Schema Relations
```typescript
// Use defined relations for joins
const orderWithQuotes = await db.query.ordersTable.findFirst({
  where: eq(ordersTable.id, orderId),
  with: {
    quotes: true,
    carrier: true
  }
});
```

### 5. Type Safety
Always use the schema types for type safety:
```typescript
import type { Order, Quote, Carrier, Shipment, Tender } from "@/db/schema";
```

## Common Query Patterns for Logistics

### Insert Operations
```typescript
const newOrder = await db.insert(ordersTable).values({
  origin: "Los Angeles, CA",
  destination: "New York, NY",
  weight: 500,
  dimensions: { length: 48, width: 40, height: 36 },
  specialHandling: ["electronics", "fragile"],
  userId: "user_123",
  requiredDeliveryDate: new Date("2024-02-15")
}).returning();
```

### Select Operations with Logistics Logic
```typescript
// Get orders by route
const laToNycOrders = await db.select()
  .from(ordersTable)
  .where(and(
    eq(ordersTable.origin, "Los Angeles, CA"),
    eq(ordersTable.destination, "New York, NY")
  ));

// Get quotes within price range
const affordableQuotes = await db.select()
  .from(quotesTable)
  .where(and(
    gte(quotesTable.totalCost, 100),
    lte(quotesTable.totalCost, 500)
  ));

// Get carriers by service type
const ltlCarriers = await db.select()
  .from(carriersTable)
  .where(eq(carriersTable.serviceType, "LTL"));
```

### Update Operations
```typescript
await db.update(quotesTable)
  .set({ 
    status: "accepted",
    acceptedAt: new Date(),
    updatedAt: new Date()
  })
  .where(eq(quotesTable.id, quoteId));
```

### Delete Operations
```typescript
await db.delete(quotesTable).where(eq(quotesTable.orderId, orderId));
```

## Logistics-Specific Query Patterns

### Rate Comparison Queries
```typescript
// Compare rates across carriers for an order
const rateComparison = await db.select({
  carrierName: carriersTable.name,
  serviceType: carriersTable.serviceType,
  totalCost: quotesTable.totalCost,
  transitTime: quotesTable.transitTime,
  serviceLevel: quotesTable.serviceLevel
})
.from(quotesTable)
.innerJoin(carriersTable, eq(quotesTable.carrierId, carriersTable.id))
.where(eq(quotesTable.orderId, orderId))
.orderBy(asc(quotesTable.totalCost));
```

### Capacity and Availability Queries
```typescript
// Check carrier availability for a route
const availableCarriers = await db.select()
  .from(carriersTable)
  .where(and(
    eq(carriersTable.origin, origin),
    eq(carriersTable.destination, destination),
    eq(carriersTable.isActive, true)
  ));
```

### Audit Trail Queries
```typescript
// Get tender history for compliance
const tenderHistory = await db.select()
  .from(tendersTable)
  .where(eq(tendersTable.orderId, orderId))
  .orderBy(desc(tendersTable.createdAt));
```

## Error Handling

Always wrap database operations in try-catch blocks with logistics-specific error messages:

```typescript
try {
  const result = await db.select().from(ordersTable);
  return result;
} catch (error) {
  console.error("Database error:", error);
  throw new Error("Failed to fetch orders - check database connection");
}
```

## Performance Considerations

1. **Use specific selects** instead of `SELECT *` for large logistics datasets
2. **Limit results** when querying shipment history or quote comparisons
3. **Use indexes** on frequently queried columns like origin, destination, dates
4. **Batch operations** for multiple quote insertions or updates
5. **Cache frequently accessed data** like carrier information and contract rates

## Migration and Schema Changes

- Schema changes must be made in [src/db/schema.ts](mdc:src/db/schema.ts)
- Use Drizzle migrations for production schema updates
- Test schema changes thoroughly before deployment
- Consider backward compatibility for logistics data

## Testing Database Operations

Use the test file at [src/db/test.ts](mdc:src/db/test.ts) for testing database operations and queries specific to logistics scenarios.

## Logistics Data Validation

Always validate logistics-specific data:
- Weight and dimensions must be positive numbers
- Origin and destination must be valid locations
- Dates must be in the future for delivery requirements
- Cost values must be positive and reasonable
- Service levels must match carrier capabilities
description:
globs:
alwaysApply: true
---
