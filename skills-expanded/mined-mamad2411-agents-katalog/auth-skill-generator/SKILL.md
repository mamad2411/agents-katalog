---
name: auth-skill-generator
description: "Generate a project-specific auth-flow skill. Use when a project has authentication: true but no auth-flow skill. Triggers on: generate auth skill, create auth patterns, auth-skill-generator."
type: meta
generates: auth-flow
trigger:
  capability: authentication
---

# Auth Skill Generator

Generate a project-specific `auth-flow` skill that documents exactly how authentication works in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing auth implementation in the codebase
3. Ask clarifying questions about auth patterns
4. Generate `docs/skills/auth-flow/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Extract:
- `stack.framework` — Next.js, Express, etc.
- `database.client` — Supabase, Prisma, etc.
- `integrations[]` — Look for auth providers (supabase, auth0, clerk, etc.)
- `apps[]` — Frontend/backend structure

---

## Step 2: Analyze Existing Auth Implementation

Search for auth patterns in the codebase:

```bash
# Find auth-related files
find . -type f \( -name "*auth*" -o -name "*session*" -o -name "*login*" \) | grep -v node_modules | grep -v .git

# Find middleware
find . -type f -name "*middleware*" | grep -v node_modules

# Find hooks related to auth
find . -type f -name "use*" | grep -vi node_modules | xargs grep -l -i "session\|auth\|user" 2>/dev/null
```

Read key files to understand the patterns:
- Auth middleware/wrapper
- Session hook
- Login/logout functions
- Protected route patterns

---

## Step 3: Clarifying Questions

Ask the user to confirm or clarify:

```
I found the following auth patterns in your codebase:

Auth Provider: [detected]
Session Storage: [detected]
Auth Middleware: [path]
Session Hook: [path]

Please confirm or correct:

1. How is auth state managed?
   A. Supabase Auth (cookies)
   B. JWT in localStorage
   C. Session cookies (server-side)
   D. Other: [specify]

2. How are pages protected?
   A. Middleware checks auth before render
   B. getServerSideProps checks auth
   C. Client-side redirect in useEffect
   D. HOC wrapper
   E. Other: [specify]

3. How are API routes protected?
   A. Auth middleware
   B. Per-route auth check
   C. Both
   D. Other: [specify]

4. Is there role-based access control (RBAC)?
   A. No, just authenticated/not
   B. Yes, simple roles (admin/user)
   C. Yes, permission-based
   D. Yes, organization-scoped roles
```

---

## Step 4: Generate the Skill

Create `docs/skills/auth-flow/SKILL.md` with project-specific content:

```markdown
---
name: auth-flow
description: "Add authentication protection to pages and API routes in [PROJECT_NAME]"
project-specific: true
generated-by: auth-skill-generator
generated-at: [DATE]
---

# Auth Flow Skill

Add authentication protection to pages and API routes.

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Protect a page | [project-specific pattern] |
| Protect an API route | [project-specific pattern] |
| Get current user | [project-specific pattern] |
| Check permissions | [project-specific pattern] |

---

## Page Protection

### Pattern: Server-Side Auth Check

[Include actual code from this project, e.g.:]

\`\`\`typescript
// In your page file (e.g., src/app/dashboard/page.tsx)
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) {
    redirect('/login')
  }
  
  // Page content here
}
\`\`\`

### Pattern: Client Component with Auth

\`\`\`typescript
'use client'

import { useSession } from '@/hooks/useSession'
import { redirect } from 'next/navigation'

export function ProtectedComponent() {
  const { user, loading } = useSession()
  
  if (loading) return <LoadingSpinner />
  if (!user) {
    redirect('/login')
    return null
  }
  
  // Component content
}
\`\`\`

---

## API Route Protection

### Pattern: Protected API Route

\`\`\`typescript
// In your API route (e.g., src/app/api/resource/route.ts)
import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  
  // Handle request
}
\`\`\`

---

## Getting Current User

### In Server Components/Actions

\`\`\`typescript
import { createClient } from '@/lib/supabase/server'

const supabase = await createClient()
const { data: { user } } = await supabase.auth.getUser()
\`\`\`

### In Client Components

\`\`\`typescript
import { useSession } from '@/hooks/useSession'

const { user, loading } = useSession()
\`\`\`

---

## Multi-Tenant Context

[If multiTenant: true]

When fetching data, always scope to the user's organization:

\`\`\`typescript
const { data } = await supabase
  .from('resources')
  .select('*')
  .eq('organization_id', user.organization_id)
\`\`\`

---

## Common Patterns

### Redirect After Login

\`\`\`typescript
// Store intended destination before redirecting to login
const returnTo = encodeURIComponent(window.location.pathname)
router.push(\`/login?returnTo=\${returnTo}\`)
\`\`\`

### Check Specific Permission

\`\`\`typescript
import { hasPermission } from '@/lib/permissions'

if (!hasPermission(user, 'resource:write')) {
  return <NotAuthorized />
}
\`\`\`

---

## Key Files

| File | Purpose |
|------|---------|
| \`[AUTH_MIDDLEWARE_PATH]\` | Auth middleware |
| \`[SESSION_HOOK_PATH]\` | Session hook for client components |
| \`[AUTH_LIB_PATH]\` | Auth utilities |
| \`[PERMISSIONS_PATH]\` | Permission checking (if RBAC) |

---

## Checklist

When adding auth to a new page or route:

- [ ] Import auth utilities from correct location
- [ ] Handle loading state (don't flash content)
- [ ] Redirect unauthenticated users appropriately
- [ ] Scope data queries to user's organization (if multi-tenant)
- [ ] Check specific permissions if needed (if RBAC)
- [ ] Test both authenticated and unauthenticated flows
```

---

## Step 5: Update project.json

Add the generated skill to the project manifest:

```json
{
  "skills": {
    "projectSkillsPath": "docs/skills/",
    "generated": [
      {
        "name": "auth-flow",
        "generatedFrom": "auth-skill-generator",
        "generatedAt": "2026-02-20"
      }
    ]
  }
}
```

---

## Step 6: Create Directory

```bash
mkdir -p docs/skills/auth-flow
```

Write the generated skill to `docs/skills/auth-flow/SKILL.md`.

---

## Output

After running this generator:

```
Created: docs/skills/auth-flow/SKILL.md

This skill documents how to:
- Protect pages with server-side auth checks
- Protect API routes
- Get the current user in server/client contexts
- Handle multi-tenant scoping

Agents will now use this skill when adding auth to new pages.
```

---

## Customization Points

The generated skill should include actual paths and patterns from THIS project:

| Placeholder | Discovered From |
|-------------|-----------------|
| `[AUTH_MIDDLEWARE_PATH]` | File search for middleware |
| `[SESSION_HOOK_PATH]` | File search for useSession/useAuth |
| `[AUTH_LIB_PATH]` | File search for auth utilities |
| `[SUPABASE_CLIENT_PATH]` | File search for Supabase client |

Replace placeholders with actual discovered values before writing the skill.
