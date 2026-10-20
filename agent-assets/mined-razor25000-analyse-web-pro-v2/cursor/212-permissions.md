---
description: 
globs: 
alwaysApply: false
---
## Context

- Our applications handle permissions with BetterAuth file [auth-permissions.ts](mdc:src/lib/auth/auth-permissions.ts)
- Permissions is based on roles
- We have utility methods to test permissions 

## Test permissions server-side only in [101-client-components.mdc](mdc:.cursor/rules/general/101-client-components.mdc) and [107-server-components.mdc](mdc:.cursor/rules/general/107-server-components.mdc)

To do that, we can use `hasPermission` method :

```tsx
import { hasPermission } from "@/lib/auth/auth-org";

export default async function RoutePage(
  props: PageParams<{
    orgSlug: string;
  }>,
) {
  const params = await props.params;

  return (
    <LayoutActions>
      {(await hasPermission({
        member: ["create"],
      })) ? (
        <Link
          href={`/orgs/${params.orgSlug}/settings/members`}
          className={buttonVariants({ variant: "outline" })}
        >
          Invite member
        </Link>
      ) : null}
    </LayoutActions>
  );
}
```