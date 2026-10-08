# Supabase Auth Patterns

## Critical Requirements

1. Use `@supabase/ssr` package
2. Use existing client utilities from `/utils/supabase`
3. Never use `@supabase/auth-helpers-nextjs`

## Common Patterns

### 1. Anonymous Auth

```typescript
import { createClient } from '@/utils/supabase/server';

async function getOrCreateUser() {
  const supabase = await createClient();
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) {
    const { data: guestData, error: guestError } = await supabase.auth.signInAnonymously();
    if (guestError || !guestData.user) throw new Error('Failed to create guest account');
    return guestData.user;
  }

  return user;
}
```

### 2. Protected API Routes

```typescript
import { createClient } from '@/utils/supabase/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const supabase = await createClient();
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Protected route logic here
  return NextResponse.json({ data: 'Protected data' });
}
```

### 3. Protected Server Components

```typescript
import { createClient } from "@/utils/supabase/server";

export default async function ProtectedComponent() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) return <div>Please log in</div>;
  return <div>Protected content for {user.email}</div>;
}
```

### 4. Client-Side Auth State

```typescript
import { createClient } from '@/utils/supabase/client';
import { useEffect, useState } from 'react';

export function useAuth() {
  const [user, setUser] = useState(null);
  const supabase = createClient();

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  return user;
}
```

### 5. Sign Out

```typescript
import { createClient } from '@/utils/supabase/client';

export async function signOut() {
  const supabase = createClient();
  await supabase.auth.signOut();
}
```
