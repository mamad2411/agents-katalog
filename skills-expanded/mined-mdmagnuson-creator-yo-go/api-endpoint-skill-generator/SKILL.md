---
name: api-endpoint-skill-generator
description: "Generate a project-specific API patterns skill. Use when a project has api: true to document endpoint creation patterns. Triggers on: generate api skill, create endpoint patterns, api-endpoint-skill-generator."
type: meta
generates: api-patterns
trigger:
  capability: api
---

# API Endpoint Skill Generator

Generate a project-specific `api-patterns` skill that documents exactly how to create API endpoints in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing API implementation
3. Ask clarifying questions about API patterns
4. Generate `docs/skills/api-patterns/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Extract:
- `stack.framework` — Next.js, Express, Gin, FastAPI, etc.
- `stack.languages` — TypeScript, Go, Python, etc.
- `capabilities.api` — Should be true
- `security.inputValidation` — zod, joi, etc.
- `security.authMiddleware` — Path to auth middleware

---

## Step 2: Analyze Existing API Implementation

```bash
# Find API routes (Next.js)
find . -path "*/api/*" -name "route.ts" | grep -v node_modules | head -20

# Find API routes (Express)
find . -type f -name "*.ts" | xargs grep -l "router\.\|app\." | head -20

# Find controllers (Go/Python)
find . -type f \( -name "*controller*" -o -name "*handler*" \) | grep -v node_modules

# Find middleware
find . -type f -name "*middleware*" | grep -v node_modules

# Look at existing endpoint structure
cat $(find . -path "*/api/*" -name "route.ts" | head -1) 2>/dev/null
```

---

## Step 3: Clarifying Questions

```
I found the following API patterns:

Framework: [detected]
Route Style: [file-based / router / decorators]
Auth Middleware: [detected path]
Validation: [detected]

Please confirm or correct:

1. What type of API is this?
   A. REST (resource-based endpoints)
   B. GraphQL
   C. tRPC
   D. RPC-style (action-based endpoints)
   E. Mix

2. How is authentication handled?
   A. Middleware on all routes
   B. Per-route auth decorators/wrappers
   C. Mix of protected and public routes
   D. No auth (public API)

3. What's the response format?
   A. JSON with { data, error } wrapper
   B. JSON with { success, data, message }
   C. Raw data (no wrapper)
   D. JSON:API spec
   E. Other: [specify]

4. How are errors handled?
   A. Centralized error handler
   B. Per-route try/catch
   C. Error middleware
   D. Mix
```

---

## Step 4: Generate the Skill

Create `docs/skills/api-patterns/SKILL.md`:

```markdown
---
name: api-patterns
description: "Create and modify API endpoints in [PROJECT_NAME]"
project-specific: true
generated-by: api-endpoint-skill-generator
generated-at: [DATE]
---

# API Patterns Skill

Standard patterns for API endpoints in this project.

---

## Quick Reference

| Task | Location |
|------|----------|
| Add new endpoint | `src/app/api/[resource]/route.ts` |
| Add auth check | Import from `@/lib/auth` |
| Validate input | Use Zod schema |
| Return success | `NextResponse.json({ data })` |
| Return error | `NextResponse.json({ error }, { status })` |

---

## Endpoint Structure

### File Location

```
src/app/api/
  [resource]/
    route.ts          # GET (list), POST (create)
    [id]/
      route.ts        # GET (single), PUT (update), DELETE
```

### Basic Endpoint Template

\`\`\`typescript
// src/app/api/[resource]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { createResourceSchema } from '@/lib/schemas/resource'

// GET /api/resources - List all
export async function GET(request: NextRequest) {
  try {
    const supabase = await createClient()
    const { data: { user } } = await supabase.auth.getUser()
    
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    
    const { data, error } = await supabase
      .from('resources')
      .select('*')
      .eq('organization_id', user.user_metadata.organization_id)
      .order('created_at', { ascending: false })
    
    if (error) throw error
    
    return NextResponse.json({ data })
  } catch (error) {
    console.error('GET /api/resources error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

// POST /api/resources - Create new
export async function POST(request: NextRequest) {
  try {
    const supabase = await createClient()
    const { data: { user } } = await supabase.auth.getUser()
    
    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      )
    }
    
    // Parse and validate body
    const body = await request.json()
    const validated = createResourceSchema.parse(body)
    
    const { data, error } = await supabase
      .from('resources')
      .insert({
        ...validated,
        organization_id: user.user_metadata.organization_id,
        created_by: user.id,
      })
      .select()
      .single()
    
    if (error) throw error
    
    return NextResponse.json({ data }, { status: 201 })
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    console.error('POST /api/resources error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
\`\`\`

---

## Authentication

### Protected Endpoint (default)

\`\`\`typescript
const { data: { user } } = await supabase.auth.getUser()

if (!user) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
}
\`\`\`

### Public Endpoint

No auth check needed, but document clearly:

\`\`\`typescript
// PUBLIC ENDPOINT - no auth required
export async function GET(request: NextRequest) {
  // ...
}
\`\`\`

### Role-Based Access

\`\`\`typescript
import { hasPermission } from '@/lib/permissions'

if (!hasPermission(user, 'resources:write')) {
  return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
}
\`\`\`

---

## Input Validation

Always validate request body with Zod:

\`\`\`typescript
import { z } from 'zod'

const createResourceSchema = z.object({
  name: z.string().min(1).max(100),
  type: z.enum(['A', 'B', 'C']),
  metadata: z.record(z.unknown()).optional(),
})

// In handler
try {
  const validated = createResourceSchema.parse(body)
} catch (error) {
  if (error instanceof z.ZodError) {
    return NextResponse.json(
      { error: 'Validation failed', details: error.errors },
      { status: 400 }
    )
  }
}
\`\`\`

---

## Query Parameters

\`\`\`typescript
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  
  const page = parseInt(searchParams.get('page') ?? '1')
  const limit = parseInt(searchParams.get('limit') ?? '20')
  const search = searchParams.get('search') ?? ''
  
  // Use in query
  let query = supabase.from('resources').select('*', { count: 'exact' })
  
  if (search) {
    query = query.ilike('name', \`%\${search}%\`)
  }
  
  const { data, count } = await query
    .range((page - 1) * limit, page * limit - 1)
  
  return NextResponse.json({
    data,
    pagination: { page, limit, total: count }
  })
}
\`\`\`

---

## Path Parameters

\`\`\`typescript
// src/app/api/resources/[id]/route.ts

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params
  
  const { data, error } = await supabase
    .from('resources')
    .select('*')
    .eq('id', id)
    .single()
  
  if (!data) {
    return NextResponse.json({ error: 'Not found' }, { status: 404 })
  }
  
  return NextResponse.json({ data })
}
\`\`\`

---

## Response Format

### Success Responses

\`\`\`typescript
// Single item
return NextResponse.json({ data: resource })

// List
return NextResponse.json({ data: resources })

// Created
return NextResponse.json({ data: resource }, { status: 201 })

// No content
return new NextResponse(null, { status: 204 })
\`\`\`

### Error Responses

\`\`\`typescript
// 400 Bad Request - validation error
return NextResponse.json(
  { error: 'Validation failed', details: [...] },
  { status: 400 }
)

// 401 Unauthorized - not logged in
return NextResponse.json(
  { error: 'Unauthorized' },
  { status: 401 }
)

// 403 Forbidden - logged in but no permission
return NextResponse.json(
  { error: 'Forbidden' },
  { status: 403 }
)

// 404 Not Found
return NextResponse.json(
  { error: 'Resource not found' },
  { status: 404 }
)

// 500 Internal Server Error
return NextResponse.json(
  { error: 'Internal server error' },
  { status: 500 }
)
\`\`\`

---

## Checklist

When adding a new API endpoint:

- [ ] Create route file in correct location
- [ ] Add authentication check (unless public)
- [ ] Add input validation with Zod
- [ ] Scope queries to organization (if multi-tenant)
- [ ] Handle all error cases
- [ ] Use correct HTTP status codes
- [ ] Log errors (don't expose details to client)
- [ ] Test happy path and error cases
- [ ] Document in API docs (if applicable)
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "api-patterns",
  "generatedFrom": "api-endpoint-skill-generator",
  "generatedAt": "2026-02-20"
}
```
