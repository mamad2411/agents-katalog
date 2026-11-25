---
name: supabase-skill-generator
description: "Generate a project-specific Supabase database skill. Use when a project has supabase in integrations or database.client is supabase. Triggers on: generate supabase skill, create supabase patterns, supabase-skill-generator."
type: meta
generates: supabase-patterns
trigger:
  integration: supabase
  databaseClient: supabase
---

# Supabase Skill Generator

Generate a project-specific `supabase-patterns` skill that documents exactly how Supabase database operations work in THIS project.

> **Note:** This skill covers database patterns (queries, RLS, realtime). For authentication patterns, see the existing `auth-supabase-otp` and `auth-supabase-password` skills.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing Supabase implementation
3. Ask clarifying questions about database patterns
4. Generate `docs/skills/supabase-patterns/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Look for:
- `database.client: "supabase"`
- Integration with name "supabase"
- `capabilities.realtime: true` (for realtime patterns)
- `capabilities.multiTenant: true` (for org-scoped RLS)

---

## Step 2: Analyze Existing Supabase Implementation

```bash
# Find Supabase client files
find . -type f -name "*.ts" | xargs grep -l "createClient.*supabase\|@supabase/ssr\|@supabase/supabase-js" 2>/dev/null | grep -v node_modules

# Find server client creation
grep -r "createClient\|createServerClient" --include="*.ts" | grep -v node_modules | head -10

# Find browser client creation (if any)
grep -r "createBrowserClient" --include="*.ts" | grep -v node_modules | head -5

# Find RLS policies (if supabase/ directory exists)
find ./supabase -name "*.sql" 2>/dev/null | xargs grep -i "create policy\|enable row level security" 2>/dev/null | head -20

# Find table definitions
cat supabase/migrations/*.sql 2>/dev/null | grep -i "create table" | head -20

# Find realtime usage
grep -r "\.channel\|\.subscribe\|realtime" --include="*.ts" | grep -v node_modules | head -10

# Find common query patterns
grep -r "\.from(\|\.select(\|\.insert(\|\.update(\|\.delete(" --include="*.ts" | grep -v node_modules | head -15
```

---

## Step 3: Clarifying Questions

```
I found the following Supabase patterns:

Server Client: [path if found]
Browser Client: [path if found, or "not used"]
Migrations: [supabase/migrations/ if exists]
RLS: [enabled/not found]
Realtime: [used/not used]

Please confirm or correct:

1. How is the Supabase client created?
   A. Server-only (using @supabase/ssr createClient)
   B. Server + Browser clients (SSR + client-side)
   C. Browser-only (SPA, no SSR)
   D. Other: [specify]

2. How is RLS structured?
   A. User-based (user_id = auth.uid())
   B. Organization-based (org_id from user metadata)
   C. Role-based (roles table lookup)
   D. Mixed / Custom
   E. No RLS yet

3. What query patterns do you use?
   A. Direct queries (.from().select())
   B. RPC functions (database functions)
   C. Both
   D. Other: [specify]

4. Do you use Supabase Realtime?
   A. Yes, for live updates
   B. Yes, for presence
   C. Both
   D. No
```

---

## Step 4: Generate the Skill

Create `docs/skills/supabase-patterns/SKILL.md`:

```markdown
---
name: supabase-patterns
description: "Supabase database operations in [PROJECT_NAME]"
project-specific: true
generated-by: supabase-skill-generator
generated-at: [DATE]
---

# Supabase Patterns Skill

How to work with Supabase database in this project.

> **Auth patterns:** See `auth-supabase-otp` or `auth-supabase-password` skills for authentication. This skill covers database operations only.

---

## Quick Reference

| Task | How |
|------|-----|
| Get server client | `createClient()` from `@/lib/supabase/server` |
| Query data | `supabase.from('table').select()` |
| Insert data | `supabase.from('table').insert({...})` |
| Update data | `supabase.from('table').update({...}).eq('id', id)` |
| Delete data | `supabase.from('table').delete().eq('id', id)` |
| Subscribe to changes | `supabase.channel('name').on(...)` |

---

## Architecture

- **Client Type:** [Server-only / Server+Browser / Browser-only]
- **RLS Approach:** [User-based / Org-based / Role-based]
- **Realtime:** [Yes / No]
- **Migrations:** `supabase/migrations/`

---

## Key Files

| File | Purpose |
|------|---------|
| `[SERVER_CLIENT_PATH]` | Server Supabase client |
| `[BROWSER_CLIENT_PATH]` | Browser Supabase client (if used) |
| `supabase/migrations/` | Database migrations |
| `[TYPES_PATH]` | Generated database types |

---

## Server Client Usage

\`\`\`typescript
// [SERVER_CLIENT_PATH]
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Called from Server Component, ignore
          }
        },
      },
    }
  )
}
\`\`\`

### Using in Server Components

\`\`\`typescript
import { createClient } from '@/lib/supabase/server'

export default async function Page() {
  const supabase = await createClient()
  
  const { data: items, error } = await supabase
    .from('items')
    .select('*')
    .order('created_at', { ascending: false })
  
  if (error) {
    console.error('Error fetching items:', error)
    return <div>Error loading items</div>
  }
  
  return <ItemList items={items} />
}
\`\`\`

### Using in Server Actions

\`\`\`typescript
'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'

export async function createItem(formData: FormData) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) {
    return { error: 'Unauthorized' }
  }
  
  const { error } = await supabase
    .from('items')
    .insert({
      name: formData.get('name') as string,
      user_id: user.id,
      // If org-scoped:
      // organization_id: user.user_metadata.organization_id,
    })
  
  if (error) {
    return { error: error.message }
  }
  
  revalidatePath('/items')
  return { success: true }
}
\`\`\`

---

## Browser Client Usage

[If browser client is used]

\`\`\`typescript
// [BROWSER_CLIENT_PATH]
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
\`\`\`

### Using in Client Components

\`\`\`typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useEffect, useState } from 'react'

export function ItemList() {
  const [items, setItems] = useState([])
  const supabase = createClient()
  
  useEffect(() => {
    const fetchItems = async () => {
      const { data } = await supabase
        .from('items')
        .select('*')
      setItems(data ?? [])
    }
    fetchItems()
  }, [])
  
  return <ul>{items.map(item => <li key={item.id}>{item.name}</li>)}</ul>
}
\`\`\`

---

## RLS Policy Patterns

### [Based on project's RLS approach]

#### User-Based RLS

\`\`\`sql
-- Users can only see their own data
CREATE POLICY "Users can view own items"
  ON items FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own items"
  ON items FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own items"
  ON items FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own items"
  ON items FOR DELETE
  USING (auth.uid() = user_id);
\`\`\`

#### Organization-Based RLS

\`\`\`sql
-- Users can see data from their organization
CREATE POLICY "Org members can view items"
  ON items FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM organization_members
      WHERE user_id = auth.uid()
    )
  );

-- Or using JWT claims:
CREATE POLICY "Org members can view items"
  ON items FOR SELECT
  USING (
    organization_id = (auth.jwt() -> 'user_metadata' ->> 'organization_id')::uuid
  );
\`\`\`

---

## Query Patterns

### Select with Filtering

\`\`\`typescript
const { data, error } = await supabase
  .from('items')
  .select('id, name, created_at, user:users(name, email)')
  .eq('status', 'active')
  .order('created_at', { ascending: false })
  .limit(10)
\`\`\`

### Insert with Return

\`\`\`typescript
const { data, error } = await supabase
  .from('items')
  .insert({
    name: 'New Item',
    user_id: user.id,
  })
  .select()
  .single()
\`\`\`

### Update with Match

\`\`\`typescript
const { error } = await supabase
  .from('items')
  .update({ status: 'completed' })
  .eq('id', itemId)
  .eq('user_id', user.id)  // Extra safety with RLS
\`\`\`

### Upsert

\`\`\`typescript
const { data, error } = await supabase
  .from('settings')
  .upsert({
    user_id: user.id,
    theme: 'dark',
  }, {
    onConflict: 'user_id',
  })
\`\`\`

---

## Realtime Subscriptions

[If capabilities.realtime: true]

\`\`\`typescript
'use client'

import { createClient } from '@/lib/supabase/client'
import { useEffect } from 'react'

export function useRealtimeItems(onUpdate: (items: Item[]) => void) {
  const supabase = createClient()
  
  useEffect(() => {
    const channel = supabase
      .channel('items-changes')
      .on(
        'postgres_changes',
        {
          event: '*',
          schema: 'public',
          table: 'items',
        },
        (payload) => {
          console.log('Change received:', payload)
          // Refetch or update state
        }
      )
      .subscribe()
    
    return () => {
      supabase.removeChannel(channel)
    }
  }, [])
}
\`\`\`

---

## TypeScript Types

Generate types from your database:

\`\`\`bash
npx supabase gen types typescript --project-id [PROJECT_ID] > src/types/database.ts
\`\`\`

Use typed client:

\`\`\`typescript
import { Database } from '@/types/database'

const supabase = createClient<Database>()

// Now queries are typed
const { data } = await supabase
  .from('items')  // Autocomplete for table names
  .select('*')    // data is typed as Item[]
\`\`\`

---

## Environment Variables

\`\`\`bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...

# For admin operations (server-side only)
SUPABASE_SERVICE_ROLE_KEY=eyJ...
\`\`\`

---

## Checklist

When adding new database operations:

- [ ] Use server client for Server Components/Actions
- [ ] Use browser client only for client-side subscriptions
- [ ] Add RLS policies for new tables
- [ ] Generate TypeScript types after schema changes
- [ ] Handle errors properly (don't expose to users)
- [ ] Use `.single()` when expecting one row
- [ ] Add proper indexes for frequently queried columns
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "supabase-patterns",
  "generatedFrom": "supabase-skill-generator",
  "generatedAt": "2026-02-20",
  "triggeredBy": "database.client: supabase"
}
```

---

## Customization Points

The generated skill should include actual paths and patterns from THIS project:

| Placeholder | Discovered From |
|-------------|-----------------|
| `[SERVER_CLIENT_PATH]` | Search for `createServerClient` or `@supabase/ssr` |
| `[BROWSER_CLIENT_PATH]` | Search for `createBrowserClient` |
| `[TYPES_PATH]` | Look for `database.ts` or `supabase.ts` in types |
| `[RLS Approach]` | Analyze migration files for policy patterns |
| `[Realtime usage]` | Search for `.channel(` or `.subscribe(` |

Replace placeholders with actual discovered values before writing the skill.
