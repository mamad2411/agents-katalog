---
description: EXPLAIN how to use API Route in our project
globs: **/route.ts
---
## Context

* API Route in NextJS enable developer to create API Endpoint to make GET / POST / PATCH / PUT / DELETE request
* We use `next-zod-route` to create safe-route.
* A safe-route is a route that verify the permission of the user, that parse params, body and query.

## Example 1 : Org Route

```ts
// app/api/org/[orgId]/route.ts
import { prisma } from "@/lib/prisma";
import { orgRoute } from "@/lib/safe-route";
import { z } from "zod";
import { NextResponse } from "next/server";

export const POST = orgRoute
  // Path params = /orgs/:orgId
  .params(
    z.object({
      orgId: z.string(),
    }),
  )
  // Body params = { name: "John" }
  .body(z.object({ name: z.string() }))
  // Query params = ?a=1&b=2
  .query(z.object({ query: z.string() }))
  .handler(async (req, { params, body, query, data }) => {
    // Safe check orgId
    const orgId = params.orgId;
    await prisma.organization.update({
      where: {
        id: params.orgId,
      },
      data: {
        name: body.name,
      },
    });

    return NextResponse.json({ ok: true }, { status: 200 })
  });
```

Our application use [204-organization.mdc](mdc:.cursor/rules/project/204-organization.mdc) to handle persmission

## Rules

- Always create org related routes insides `/api/org/[orgId]/*`
- Always use `orgRoute` to create safe routes inside `/api/org/[orgId]/*`
- In general, you can use `authRoute` to create safe routes that is NOT related to orgs.

## Route Type

* `orgRoute` only work in files URL that is children of `app/api/org/[orgId]`
* `tokenRoute` only work in files URL that is children of `/app/api/v1` and accept Bearer Token to retreive the org
* `authRoute` work everywhere and accept only authentificated user
* `route` work everywhere and accept everything.

## Error

`Error` is not catched and sent to the client by default. If you want the client to retrieve the error you must use `RouteError` :

```tsx
import { orgRoute, SafeRouteError } from "@/lib/safe-route";

export const GET = orgRoute
  .params(SubscriberParamsSchema)
  .handler(async (req, { params, data }) => {
    const subscriber = // ...

    if (!subscriber) {
      throw new SafeRouteError("Subscriber not found", 404);
    }
    // Automaticly send 200 with JSON
    return subscriber
  });
```

## Files

- [safe-route.ts](mdc:src/lib/safe-route.ts)
