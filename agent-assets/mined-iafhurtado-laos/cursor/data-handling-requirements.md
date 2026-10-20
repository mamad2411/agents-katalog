# Data Handling Requirements for Logistics Agents

## Database Query Helper Functions

**ALWAYS** use helper functions from the `db/queries` directory for all database operations. Never write raw database queries directly in server components or server actions.

### Directory Structure:
```
db/
  ├── queries/
  │   ├── orders.ts
  │   ├── quotes.ts
  │   ├── carriers.ts
  │   ├── shipments.ts
  │   ├── tenders.ts
  │   └── index.ts
  ├── schema.ts
  └── index.ts
```

### Correct Pattern for Query Functions:
```tsx
// db/queries/orders.ts
import { db } from '@/db';
import { ordersTable } from '@/db/schema';
import { eq, and, gte, lte } from 'drizzle-orm';

export async function getAllOrders() {
  return await db.query.ordersTable.findMany();
}

export async function getOrderById(id: string) {
  return await db.query.ordersTable.findFirst({
    where: eq(ordersTable.id, id)
  });
}

export async function getOrdersByRoute(origin: string, destination: string) {
  return await db.select()
    .from(ordersTable)
    .where(and(
      eq(ordersTable.origin, origin),
      eq(ordersTable.destination, destination)
    ));
}

export async function createOrder(data: CreateOrderInput) {
  return await db.insert(ordersTable).values(data).returning();
}

export async function updateOrder(id: string, data: UpdateOrderInput) {
  return await db.update(ordersTable)
    .set(data)
    .where(eq(ordersTable.id, id))
    .returning();
}

export async function deleteOrder(id: string) {
  return await db.delete(ordersTable).where(eq(ordersTable.id, id));
}
```

### Correct Pattern for Index File:
```tsx
// db/queries/index.ts
export * from './orders';
export * from './quotes';
export * from './carriers';
export * from './shipments';
export * from './tenders';
```

## Server Components for Data Retrieval

**ALWAYS** use server components for data retrieval operations. Never fetch data directly in client components.

### Correct Pattern:
```tsx
// ✅ Good - Server Component using query helpers
import { getAllOrders, getQuotesByOrderId } from '@/db/queries';

async function OrdersList() {
  const orders = await getAllOrders();
  return (
    <div>
      {orders.map(order => (
        <OrderCard key={order.id} order={order} />
      ))}
    </div>
  );
}

async function OrderQuotes({ orderId }: { orderId: string }) {
  const quotes = await getQuotesByOrderId(orderId);
  return (
    <div>
      {quotes.map(quote => (
        <QuoteCard key={quote.id} quote={quote} />
      ))}
    </div>
  );
}
```

### Incorrect Pattern:
```tsx
// ❌ Bad - Client Component fetching data
'use client';
function OrdersList() {
  const [orders, setOrders] = useState();
  useEffect(() => {
    fetch('/api/orders').then(setOrders);
  }, []);
  return <div>{/* render orders */}</div>;
}

// ❌ Bad - Direct database queries in components
async function OrdersList() {
  const orders = await db.query.ordersTable.findMany(); // Don't do this
  return <div>{/* render orders */}</div>;
}
```

## Server Actions for Database Operations

**ALWAYS** use server actions for any database mutations (insert, update, delete). Never use API routes for database operations.

### Correct Pattern:
```tsx
// ✅ Good - Server Action using query helpers
'use server';
import { z } from 'zod';
import { createOrder, updateOrder } from '@/db/queries';

const CreateOrderSchema = z.object({
  origin: z.string().min(1, "Origin is required"),
  destination: z.string().min(1, "Destination is required"),
  weight: z.number().positive("Weight must be positive"),
  dimensions: z.object({
    length: z.number().positive(),
    width: z.number().positive(),
    height: z.number().positive()
  }),
  specialHandling: z.array(z.string()).optional(),
  requiredDeliveryDate: z.date().min(new Date(), "Delivery date must be in the future")
});

export async function handleCreateOrder(data: z.infer<typeof CreateOrderSchema>) {
  const validatedData = CreateOrderSchema.parse(data);
  return await createOrder(validatedData);
}
```

### Usage in Client Component:
```tsx
'use client';
import { handleCreateOrder } from './actions';

export function OrderForm() {
  const handleSubmit = async (formData: FormData) => {
    const data = {
      origin: formData.get('origin') as string,
      destination: formData.get('destination') as string,
      weight: Number(formData.get('weight')),
      dimensions: {
        length: Number(formData.get('length')),
        width: Number(formData.get('width')),
        height: Number(formData.get('height'))
      },
      specialHandling: formData.getAll('specialHandling') as string[],
      requiredDeliveryDate: new Date(formData.get('deliveryDate') as string)
    };
    await handleCreateOrder(data);
  };
  
  return <form action={handleSubmit}>{/* form fields */}</form>;
}
```

## Zod Validation Requirements

**ALWAYS** use Zod for data validation. Every server action must validate its input data with Zod.

### Required Pattern:
```tsx
'use server';
import { z } from 'zod';
import { createQuote } from '@/db/queries';

// ✅ Good - Define schema and type
const QuoteSchema = z.object({
  orderId: z.string().uuid("Invalid order ID"),
  carrierId: z.string().uuid("Invalid carrier ID"),
  totalCost: z.number().positive("Cost must be positive"),
  transitTime: z.number().positive("Transit time must be positive"),
  serviceLevel: z.enum(["standard", "express", "premium"]),
  validUntil: z.date().min(new Date(), "Quote must be valid in the future")
});

// ✅ Good - Extract TypeScript type from schema
type QuoteInput = z.infer<typeof QuoteSchema>;

export async function handleCreateQuote(data: QuoteInput) {
  // ✅ Good - Validate input data
  const validatedData = QuoteSchema.parse(data);
  
  // Use query helper function
  return await createQuote(validatedData);
}
```

## TypeScript Type Requirements

**NEVER** use `FormData` as the type for server action parameters. Always define proper TypeScript types using Zod schemas.

### Incorrect Pattern:
```tsx
// ❌ Bad - Using FormData type
'use server';
export async function createOrder(formData: FormData) {
  // Don't do this
}
```

### Correct Pattern:
```tsx
// ✅ Good - Using proper TypeScript types
'use server';
import { z } from 'zod';
import { createOrder } from '@/db/queries';

const CreateOrderSchema = z.object({
  origin: z.string().min(1),
  destination: z.string().min(1),
  weight: z.number().positive(),
  dimensions: z.object({
    length: z.number().positive(),
    width: z.number().positive(),
    height: z.number().positive()
  })
});

type CreateOrderInput = z.infer<typeof CreateOrderSchema>;

export async function handleCreateOrder(data: CreateOrderInput) {
  const validatedData = CreateOrderSchema.parse(data);
  return await createOrder(validatedData);
}
```

## Logistics-Specific Validation Schemas

### Order Validation:
```tsx
// lib/schemas/order.ts
import { z } from 'zod';

export const OrderSchema = z.object({
  id: z.string().uuid().optional(),
  origin: z.string().min(1, 'Origin is required').max(200, 'Origin too long'),
  destination: z.string().min(1, 'Destination is required').max(200, 'Destination too long'),
  weight: z.number().positive('Weight must be positive').max(100000, 'Weight exceeds maximum'),
  dimensions: z.object({
    length: z.number().positive('Length must be positive').max(1000, 'Length too long'),
    width: z.number().positive('Width must be positive').max(1000, 'Width too long'),
    height: z.number().positive('Height must be positive').max(1000, 'Height too long')
  }),
  specialHandling: z.array(z.string()).optional(),
  requiredDeliveryDate: z.date().min(new Date(), 'Delivery date must be in the future'),
  userId: z.string().uuid('Invalid user ID')
});

export type Order = z.infer<typeof OrderSchema>;
export type CreateOrderInput = Omit<Order, 'id'>;
export type UpdateOrderInput = Order;
```

### Quote Validation:
```tsx
// lib/schemas/quote.ts
import { z } from 'zod';

export const QuoteSchema = z.object({
  id: z.string().uuid().optional(),
  orderId: z.string().uuid('Invalid order ID'),
  carrierId: z.string().uuid('Invalid carrier ID'),
  totalCost: z.number().positive('Cost must be positive').max(1000000, 'Cost exceeds maximum'),
  transitTime: z.number().positive('Transit time must be positive').max(365, 'Transit time too long'),
  serviceLevel: z.enum(['standard', 'express', 'premium'], {
    errorMap: () => ({ message: 'Invalid service level' })
  }),
  validUntil: z.date().min(new Date(), 'Quote must be valid in the future'),
  notes: z.string().max(1000, 'Notes too long').optional()
});

export type Quote = z.infer<typeof QuoteSchema>;
export type CreateQuoteInput = Omit<Quote, 'id'>;
export type UpdateQuoteInput = Quote;
```

## Complete Example for Logistics

Here's a complete example showing all requirements for a logistics order system:

```tsx
// lib/schemas/order.ts
import { z } from 'zod';

export const OrderSchema = z.object({
  id: z.string().uuid().optional(),
  origin: z.string().min(1, 'Origin is required'),
  destination: z.string().min(1, 'Destination is required'),
  weight: z.number().positive('Weight must be positive'),
  dimensions: z.object({
    length: z.number().positive(),
    width: z.number().positive(),
    height: z.number().positive()
  }),
  specialHandling: z.array(z.string()).optional(),
  requiredDeliveryDate: z.date().min(new Date(), 'Delivery date must be in the future'),
  userId: z.string().uuid('Invalid user ID')
});

export type Order = z.infer<typeof OrderSchema>;
export type CreateOrderInput = Omit<Order, 'id'>;
export type UpdateOrderInput = Order;

// db/queries/orders.ts
import { db } from '@/db';
import { ordersTable } from '@/db/schema';
import { eq, and, gte, lte } from 'drizzle-orm';
import type { CreateOrderInput, UpdateOrderInput } from '@/lib/schemas/order';

export async function getAllOrders() {
  return await db.query.ordersTable.findMany();
}

export async function getOrderById(id: string) {
  return await db.query.ordersTable.findFirst({
    where: eq(ordersTable.id, id)
  });
}

export async function createOrder(data: CreateOrderInput) {
  return await db.insert(ordersTable).values(data).returning();
}

export async function updateOrder(id: string, data: UpdateOrderInput) {
  return await db.update(ordersTable)
    .set(data)
    .where(eq(ordersTable.id, id))
    .returning();
}

export async function deleteOrder(id: string) {
  return await db.delete(ordersTable).where(eq(ordersTable.id, id));
}

// app/actions/order.ts
'use server';
import { z } from 'zod';
import { OrderSchema, CreateOrderInput, UpdateOrderInput } from '@/lib/schemas/order';
import { createOrder, updateOrder, deleteOrder } from '@/db/queries';

export async function handleCreateOrder(data: CreateOrderInput) {
  const validatedData = OrderSchema.parse(data);
  return await createOrder(validatedData);
}

export async function handleUpdateOrder(data: UpdateOrderInput) {
  const validatedData = OrderSchema.parse(data);
  return await updateOrder(validatedData.id!, validatedData);
}

export async function handleDeleteOrder(id: string) {
  const validatedId = z.string().uuid().parse(id);
  return await deleteOrder(validatedId);
}

// app/components/orders-list.tsx
// ✅ Server Component for data retrieval using query helpers
import { getAllOrders } from '@/db/queries';

async function OrdersList() {
  const allOrders = await getAllOrders();
  
  return (
    <div>
      {allOrders.map(order => (
        <OrderCard key={order.id} order={order} />
      ))}
    </div>
  );
}

// app/components/order-card.tsx
'use client';
import { handleUpdateOrder, handleDeleteOrder } from '@/app/actions/order';
import type { Order } from '@/lib/schemas/order';

export function OrderCard({ order }: { order: Order }) {
  const handleUpdate = async (formData: FormData) => {
    const data = {
      id: order.id,
      origin: formData.get('origin') as string,
      destination: formData.get('destination') as string,
      weight: Number(formData.get('weight')),
      dimensions: {
        length: Number(formData.get('length')),
        width: Number(formData.get('width')),
        height: Number(formData.get('height'))
      },
      specialHandling: formData.getAll('specialHandling') as string[],
      requiredDeliveryDate: new Date(formData.get('deliveryDate') as string),
      userId: order.userId
    };
    await handleUpdateOrder(data);
  };
  
  const handleDelete = async () => {
    await handleDeleteOrder(order.id!);
  };
  
  return (
    <div>
      <form action={handleUpdate}>
        {/* form fields */}
      </form>
      <button onClick={handleDelete}>Delete</button>
    </div>
  );
}
```

## Key Points Summary

1. **Query Helpers**: Always use helper functions from `db/queries` directory
2. **Data Retrieval**: Always use server components with query helpers
3. **Database Mutations**: Always use server actions with query helpers
4. **Validation**: Always use Zod schemas with logistics-specific validation rules
5. **TypeScript**: Always define proper types from Zod schemas
6. **Never use FormData as type**: Extract data and pass structured objects
7. **Validation**: Always validate input data in server actions before database operations
8. **Separation of Concerns**: Keep database logic in query helpers, validation in schemas, and business logic in server actions
9. **Logistics Data**: Validate weight, dimensions, dates, and locations according to logistics business rules
10. **Audit Trail**: Maintain proper logging and tracking for all logistics operations
description:
globs:
alwaysApply: true
---
