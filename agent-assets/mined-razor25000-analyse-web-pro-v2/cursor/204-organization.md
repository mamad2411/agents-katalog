---
description: EXPLAIN how work multi-tenant model with organization
globs: *.ts, *.tsx
alwaysApply: false
---
## Context

* The application define a multi-tenant model
* The multi-tenant model name is `Organization`
* Every table must be linked to `Organization` and the user can be a member of it.
* The plan and payment is always link to the `Organization`
* The orgainzation is defined in [better-auth.prisma](mdc:prisma/schema/better-auth.prisma)

## Methods

- You muse always use organization for resources. Everything must be linked to an organization, not a user.

- To get an organization, you can use `getCurrentOrgCache` or `getRequiredCurrentOrgCache` function.

```ts
import { getCurrentOrgCache } from "@/lib/react/cache";

const org = await getCurrentOrgCache();
```

The `cache` version avoid to make the request multiple time.

## Rules

You must always include the organization inside Prisma query to avoid getting data from other organization :

```ts
const org = await getRequiredCurrentOrgCache();

const tags = await prisma.tag.findMany({
  where: {
    // Verify the organization
    organizationId: org.id,
  }
});
```

## Subscribtion

The subscribtion is inside the current org :

```ts
import { getPlanLimits } from "@/lib/auth-plans";
import { getRequiredCurrentOrgCache } from "@/lib/react/cache";

const org = await getRequiredCurrentOrgCache();
const subscription = org.subscription;

// Get the plan limit
const maxMembers = getPlanLimits(org.subscription?.plan ?? "basic").members;
```

## Roles

The roles is defined in [auth-permissions.ts](mdc:src/lib/auth/auth-permissions.ts) with the permissions.


