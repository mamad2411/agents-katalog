---
name: "Backend"
description: "Server Actions, services, repositories, Zod validation, Prisma patterns, and error handling conventions"
applyTo: "server/**,src/server/**,lib/**,src/lib/**"
---

# Backend Instructions

## Action Result Type

All Server Actions must return a consistent `ActionResult` type. Define it in `lib/types.ts`:

```ts
type ActionResult<T = void> = { success: true; data: T } | { success: false; error: string };
```

Always use this — never return raw data or throw errors from actions.

```ts
// Good
return { success: true, data: reservation };
return { success: false, error: "Reservation not found" };

// Bad — never do this
return reservation;
throw new Error("Not found");
```

---

## Error Handling

### In Server Actions

Wrap the service call in try/catch. Log the real error, return a user-friendly message.

```ts
"use server";

export async function deleteReservation(id: string): Promise<ActionResult> {
  try {
    await reservationService.delete(id);
    return { success: true, data: undefined };
  } catch (error) {
    console.error("Failed to delete reservation:", error);
    return { success: false, error: "Failed to delete reservation" };
  }
}
```

### In Services

Throw descriptive errors. Let actions catch and translate them.

```ts
export const reservationService = {
  async delete(id: string) {
    const reservation = await reservationRepository.findById(id);
    if (!reservation) {
      throw new Error(`Reservation with id ${id} not found`);
    }
    return reservationRepository.delete(id);
  },
};
```

### In Repositories

Let Prisma errors propagate naturally — do not catch them in repositories.

---

## Naming Conventions

### Files

- Action files: `kebab-case` verb-noun — `create-reservation.ts`, `get-reservations.ts`
- Service files: `<entity>.service.ts` — `reservation.service.ts`
- Repository files: `<entity>.repository.ts` — `reservation.repository.ts`
- Schema files: `<entity>.schema.ts` — `reservation.schema.ts`

### Functions

- Action functions: `camelCase` verb-noun — `createReservation`, `getReservations`
- Service/repository methods: short verbs — `create`, `findById`, `findMany`, `update`, `delete`

### One action per file

Each Server Action file exports **one** action function. Do not bundle multiple actions in one file.

---

## Zod Validation

- Define **one schema per operation** (create, update) — not a single shared schema.
- Derive TypeScript types from Zod schemas using `z.infer<>`, never duplicate them manually.
- Place schemas in the domain's `schemas/` directory.

```ts
// server/reservations/schemas/reservation.schema.ts
import { z } from "zod";

export const createReservationSchema = z.object({
  name: z.string().min(1, "Name is required"),
  date: z.coerce.date(),
  guests: z.number().int().positive(),
});

export const updateReservationSchema = createReservationSchema.partial().extend({
  id: z.string().uuid(),
});
```

---

## Prisma Best Practices

### Select only what you need

Use `select` or `include` to avoid over-fetching. Don't return entire models when you only need a few fields.

```ts
// Good
async findMany() {
  return prisma.reservation.findMany({
    select: { id: true, name: true, date: true, guests: true },
  })
}

// Bad — fetches all columns and relations
async findMany() {
  return prisma.reservation.findMany()
}
```

### Transactions

When a service needs multiple related writes, use Prisma interactive transactions:

```ts
export const orderService = {
  async createWithItems(data: CreateOrderInput) {
    return prisma.$transaction(async (tx) => {
      const order = await tx.order.create({ data: { userId: data.userId } });
      await tx.orderItem.createMany({
        data: data.items.map((item) => ({ ...item, orderId: order.id })),
      });
      return order;
    });
  },
};
```

Note: transactions are the one exception where a **service** may use the Prisma client directly — pass `tx` instead of going through the repository.

### Migrations

- Always use `npx prisma migrate dev --name <descriptive-name>` to create migrations.
- Never edit the database manually — all changes go through the Prisma schema.
- Run `npx prisma generate` after schema changes to update the client.

---

## Revalidation

After mutating data in a Server Action, revalidate the relevant path so the UI reflects the change:

```ts
import { revalidatePath } from "next/cache";

export async function createReservation(formData: FormData): Promise<ActionResult<Reservation>> {
  // ... validate and create ...

  revalidatePath("/reservations");
  return { success: true, data: reservation };
}
```

---

## Environment Variables

- Access env vars only in backend code (`server/`, `lib/`), never in client components.
- Use `process.env.VARIABLE_NAME` directly — do not re-export env vars.
- Define all required variables in `.env.example` with placeholder values.

---

## Summary

| Concern            | Where                                 | Example                            |
| ------------------ | ------------------------------------- | ---------------------------------- |
| Input validation   | Actions (Zod)                         | `schema.safeParse(data)`           |
| Error handling     | Actions (try/catch)                   | `return { success: false, error }` |
| Business rules     | Services                              | availability checks, authorization |
| Database queries   | Repositories                          | `prisma.entity.findMany()`         |
| Transactions       | Services (with `prisma.$transaction`) | multi-table writes                 |
| Cache invalidation | Actions                               | `revalidatePath()`                 |
