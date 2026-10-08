---
name: "Architecture"
description: "Domain-based project structure, layer responsibilities, data flow, and import rules for Next.js App Router with Server Actions and Prisma"
applyTo: "**"
---

# Architecture Instructions

This project uses **Next.js App Router** with **Server Actions** and **Prisma**.
Backend logic follows a **domain-based architecture** inside the `server/` directory.

---

## Project Structure

```
src/
  app/                        # Next.js routes and layouts
  components/                 # Reusable UI components
    ui/                       # shadcn/ui components
  lib/                        # Shared utilities (db, auth, helpers)
  server/                     # All backend logic
    reservations/
    users/
    auth/
    tables/
prisma/                       # Prisma schema and migrations
```

---

## Server Domain Structure

Each domain inside `server/` must follow this structure:

```
server/
  <domain>/
    actions/
      create-<entity>.ts
      update-<entity>.ts
      delete-<entity>.ts
    services/
      <entity>.service.ts
    repositories/
      <entity>.repository.ts
    schemas/
      <entity>.schema.ts
    types.ts
```

Each domain encapsulates all backend logic related to that feature.

---

## Layer Responsibilities

### Server Actions (`actions/`)

Entry point from the frontend. They validate input, call services, and return results.

**Must NOT** contain business logic or direct database queries.

```ts
"use server";

import { createReservationSchema } from "../schemas/reservation.schema";
import { reservationService } from "../services/reservation.service";

export async function createReservation(formData: FormData) {
  const parsed = createReservationSchema.safeParse({
    name: formData.get("name"),
    guests: Number(formData.get("guests")),
  });

  if (!parsed.success) {
    return { success: false, error: parsed.error.flatten() };
  }

  try {
    const reservation = await reservationService.create(parsed.data);
    return { success: true, data: reservation };
  } catch (error) {
    return { success: false, error: "Failed to create reservation" };
  }
}
```

### Services (`services/`)

Contain **business logic**. Coordinate repositories, enforce business rules, perform workflows.

**Must NOT** depend on frontend code or access the database directly.

```ts
import type { CreateReservationInput } from "../types";
import { reservationRepository } from "../repositories/reservation.repository";

export const reservationService = {
  async create(data: CreateReservationInput) {
    // Business logic goes here (e.g., availability checks, validation rules)
    return reservationRepository.create(data);
  },
};
```

### Repositories (`repositories/`)

Responsible for **database access only**. Communicate with Prisma and return data to services.

**Must NOT** contain business logic.

```ts
import { prisma } from "@/lib/db";
import type { CreateReservationInput } from "../types";

export const reservationRepository = {
  async create(data: CreateReservationInput) {
    return prisma.reservation.create({ data });
  },

  async findMany() {
    return prisma.reservation.findMany();
  },
};
```

### Schemas (`schemas/`)

Zod schemas for validating input data. Used in Server Actions before calling services.

```ts
import { z } from "zod";

export const createReservationSchema = z.object({
  name: z.string().min(1),
  guests: z.number().int().positive(),
});
```

### Types (`types.ts`)

Domain-specific TypeScript types.

```ts
import type { z } from "zod";
import type { createReservationSchema } from "./schemas/reservation.schema";

export type CreateReservationInput = z.infer<typeof createReservationSchema>;
```

---

## Database Access

Prisma client is defined in `lib/db.ts` using a singleton pattern to prevent connection leaks during development:

```ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient | undefined };

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== "production") {
  globalForPrisma.prisma = prisma;
}
```

Only repositories may import the Prisma client.

---

## Import Rules

Frontend components **may** import:

- `server/*/actions`

Frontend components **must NOT** import:

- `server/*/services`
- `server/*/repositories`
- `server/*/schemas`

---

## Data Flow

All backend operations follow this flow:

```
Component → Server Action → Service → Repository → Database
```

---

## Key Rules

- Use **Zod schemas** for all input validation in Server Actions.
- Server Actions must return a consistent result shape: `{ success: boolean, data?, error? }`.
- Never place business logic in Server Actions or repositories.
- Never access the database outside repositories.
- Keep domains independent and cohesive.
- Prefer small, focused services over large monolithic ones.
- Use Prisma migrations (`npx prisma migrate dev`) to manage schema changes.
