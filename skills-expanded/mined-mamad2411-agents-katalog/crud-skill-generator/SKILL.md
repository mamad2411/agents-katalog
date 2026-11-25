---
name: crud-skill-generator
description: "Generate a project-specific CRUD patterns skill. Use for any project with a database to document entity creation patterns. Triggers on: generate crud skill, create crud patterns, crud-skill-generator."
type: meta
generates: crud-patterns
trigger:
  condition: database exists
---

# CRUD Skill Generator

Generate a project-specific `crud-patterns` skill that documents exactly how to create, read, update, and delete entities in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing CRUD patterns in the codebase
3. Ask clarifying questions about data patterns
4. Generate `docs/skills/crud-patterns/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Extract:
- `stack.framework` — Next.js, Express, Gin, etc.
- `database.type` — postgres, mysql, mongodb, etc.
- `database.client` — supabase, prisma, drizzle, pgx, etc.
- `capabilities.multiTenant` — affects how entities are scoped
- `security.inputValidation` — zod, yup, etc.

---

## Step 2: Analyze Existing Patterns

Search for CRUD patterns:

```bash
# Find API routes
find . -type f \( -name "route.ts" -o -name "*.api.ts" \) | grep -v node_modules | head -20

# Find server actions
grep -r "use server" --include="*.ts" --include="*.tsx" | head -20

# Find form components
find . -type f -name "*Form*.tsx" | grep -v node_modules | head -10

# Find validation schemas
find . -type f \( -name "*schema*" -o -name "*validation*" \) | grep -v node_modules | head -10

# Look at an existing entity implementation
ls -la src/app/api/ 2>/dev/null || ls -la app/api/ 2>/dev/null
```

Pick one well-implemented entity as the reference pattern.

---

## Step 3: Clarifying Questions

```
I found the following CRUD patterns:

Database Client: [detected]
API Style: [REST routes / Server Actions / tRPC / GraphQL]
Validation: [detected]
Forms: [detected]

Please confirm or correct:

1. How are mutations handled?
   A. REST API routes (POST/PUT/DELETE)
   B. Next.js Server Actions
   C. tRPC procedures
   D. GraphQL mutations
   E. Mix of above

2. Where does validation happen?
   A. Client-side only
   B. Server-side only
   C. Both client and server (shared schemas)
   D. Database constraints only

3. How are forms built?
   A. react-hook-form
   B. Formik
   C. Native form handling
   D. Server Actions with useFormState
   E. Other: [specify]

4. What's the reference entity to model patterns after?
   [Show list of detected entities, let user pick]
```

---

## Step 4: Generate the Skill

Create `docs/skills/crud-patterns/SKILL.md`:

```markdown
---
name: crud-patterns
description: "Create, read, update, and delete entities in [PROJECT_NAME]"
project-specific: true
generated-by: crud-skill-generator
generated-at: [DATE]
---

# CRUD Patterns Skill

Standard patterns for entity operations in this project.

---

## Quick Reference

| Operation | Pattern |
|-----------|---------|
| Create | [Server Action / API route] |
| Read (list) | [Server component / API] |
| Read (single) | [Server component / API] |
| Update | [Server Action / API route] |
| Delete | [Server Action / API route] |

---

## Tech Stack

- **Database:** [DATABASE_TYPE] via [DATABASE_CLIENT]
- **Validation:** [VALIDATION_LIB]
- **Forms:** [FORM_LIB]
- **API Style:** [API_STYLE]

---

## Creating an Entity

### Step 1: Define the Schema

\`\`\`typescript
// src/lib/schemas/[entity].ts
import { z } from 'zod'

export const createEntitySchema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().optional(),
  // Add fields as needed
})

export const updateEntitySchema = createEntitySchema.partial()

export type CreateEntityInput = z.infer<typeof createEntitySchema>
export type UpdateEntityInput = z.infer<typeof updateEntitySchema>
\`\`\`

### Step 2: Create Server Action (or API Route)

\`\`\`typescript
// src/actions/[entity].ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { createEntitySchema } from '@/lib/schemas/[entity]'
import { revalidatePath } from 'next/cache'

export async function createEntity(input: CreateEntityInput) {
  // Validate
  const validated = createEntitySchema.parse(input)
  
  // Get auth context
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) {
    throw new Error('Unauthorized')
  }
  
  // Insert with tenant scope
  const { data, error } = await supabase
    .from('entities')
    .insert({
      ...validated,
      organization_id: user.user_metadata.organization_id,
      created_by: user.id,
    })
    .select()
    .single()
  
  if (error) throw error
  
  revalidatePath('/entities')
  return data
}
\`\`\`

### Step 3: Create Form Component

\`\`\`typescript
// src/components/EntityForm.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { createEntitySchema, CreateEntityInput } from '@/lib/schemas/entity'
import { createEntity } from '@/actions/entity'

export function EntityForm() {
  const form = useForm<CreateEntityInput>({
    resolver: zodResolver(createEntitySchema),
    defaultValues: { name: '', description: '' }
  })
  
  const onSubmit = async (data: CreateEntityInput) => {
    try {
      await createEntity(data)
      form.reset()
      // Show success toast
    } catch (error) {
      // Show error toast
    }
  }
  
  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  )
}
\`\`\`

---

## Reading Entities

### List (Server Component)

\`\`\`typescript
// src/app/entities/page.tsx
import { createClient } from '@/lib/supabase/server'

export default async function EntitiesPage() {
  const supabase = await createClient()
  
  const { data: entities } = await supabase
    .from('entities')
    .select('*')
    .order('created_at', { ascending: false })
  
  return <EntityList entities={entities ?? []} />
}
\`\`\`

### Single (Server Component)

\`\`\`typescript
// src/app/entities/[id]/page.tsx
import { createClient } from '@/lib/supabase/server'
import { notFound } from 'next/navigation'

export default async function EntityPage({ params }: { params: { id: string } }) {
  const supabase = await createClient()
  
  const { data: entity } = await supabase
    .from('entities')
    .select('*')
    .eq('id', params.id)
    .single()
  
  if (!entity) notFound()
  
  return <EntityDetail entity={entity} />
}
\`\`\`

---

## Updating an Entity

\`\`\`typescript
// src/actions/[entity].ts
export async function updateEntity(id: string, input: UpdateEntityInput) {
  const validated = updateEntitySchema.parse(input)
  
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) throw new Error('Unauthorized')
  
  const { data, error } = await supabase
    .from('entities')
    .update({
      ...validated,
      updated_at: new Date().toISOString(),
    })
    .eq('id', id)
    .eq('organization_id', user.user_metadata.organization_id) // Tenant scope!
    .select()
    .single()
  
  if (error) throw error
  
  revalidatePath(\`/entities/\${id}\`)
  return data
}
\`\`\`

---

## Deleting an Entity

\`\`\`typescript
// src/actions/[entity].ts
export async function deleteEntity(id: string) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()
  
  if (!user) throw new Error('Unauthorized')
  
  const { error } = await supabase
    .from('entities')
    .delete()
    .eq('id', id)
    .eq('organization_id', user.user_metadata.organization_id) // Tenant scope!
  
  if (error) throw error
  
  revalidatePath('/entities')
}
\`\`\`

---

## Database Migration

When adding a new entity, create a migration:

\`\`\`sql
-- supabase/migrations/YYYYMMDD_create_entities.sql

CREATE TABLE entities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  organization_id UUID NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL,
  description TEXT,
  created_by UUID NOT NULL REFERENCES auth.users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE entities ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their org's entities"
ON entities FOR ALL
USING (organization_id = (auth.jwt() ->> 'organization_id')::uuid);

-- Index
CREATE INDEX idx_entities_org ON entities(organization_id);
\`\`\`

---

## File Structure

For a new entity "Widget":

```
src/
  lib/schemas/
    widget.ts           # Zod schemas
  actions/
    widget.ts           # Server actions
  app/
    widgets/
      page.tsx          # List page
      [id]/
        page.tsx        # Detail page
        edit/
          page.tsx      # Edit page
      new/
        page.tsx        # Create page
  components/
    widgets/
      WidgetForm.tsx    # Form component
      WidgetList.tsx    # List component
      WidgetCard.tsx    # Card component

supabase/migrations/
  YYYYMMDD_create_widgets.sql
```

---

## Checklist

When adding a new entity:

- [ ] Create Zod schema with create/update variants
- [ ] Create database migration with RLS
- [ ] Create server actions (create, update, delete)
- [ ] Create list page (server component)
- [ ] Create detail page (server component)
- [ ] Create form component
- [ ] Add tenant scoping to all queries
- [ ] Add proper error handling
- [ ] Test CRUD operations
- [ ] Run migration
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "crud-patterns",
  "generatedFrom": "crud-skill-generator",
  "generatedAt": "2026-02-20"
}
```
