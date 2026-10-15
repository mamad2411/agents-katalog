---
name: use-route-constants
description: Explains the standard of using centralized route constants instead of hardcoded strings for navigation in the frontend.
---

# Use Route Constants Skill

To ensure scalability and prevent broken links across the frontend, **no hardcoded strings** should be used for navigation or redirects. All route paths must be imported from the centralized routing dictionary.

## The Standard

The central dictionary is located at `frontend/src/config/routes.ts`.

It exports a constant `ROUTES` object that contains all available paths in the application.

## How to Apply It

Whenever you need to use `next/link` or `useRouter().push()`, you MUST import the `ROUTES` constant.

**❌ Bad (Hardcoded string):**
```tsx
import Link from 'next/link';

<Link href="/login">Login</Link>
```

**✅ Good (Using Route Constant):**
```tsx
import Link from 'next/link';
import { ROUTES } from '@/src/config/routes';

<Link href={ROUTES.AUTH.LOGIN}>Login</Link>
```

### Dynamic Routes
If a new route is dynamic (e.g., requires an ID), add a helper function to `routes.ts`:

```typescript
// in routes.ts
export const ROUTES = {
  // ...
  USER_PROFILE: (id: string | number) => `/users/${id}`,
};
```

And use it identically:
```tsx
<Link href={ROUTES.USER_PROFILE(user.id)}>Profile</Link>
```

Always check `frontend/src/config/routes.ts` or add to it before implementing any navigation flow.
