---
name: multi-tenant-skill-generator
description: "Generate a project-specific tenant-context skill. Use when a project has multiTenant: true but no tenant-context skill. Triggers on: generate tenant skill, create multi-tenant patterns, multi-tenant-skill-generator."
type: meta
generates: tenant-context
trigger:
  capability: multiTenant
---

# Multi-Tenant Skill Generator

Generate a project-specific `tenant-context` skill that documents exactly how multi-tenancy works in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing multi-tenant implementation
3. Ask clarifying questions about tenant patterns
4. Generate `docs/skills/tenant-context/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Extract:
- `capabilities.multiTenant` — Should be true
- `database.client` — How data is stored
- `integrations[]` — Supabase RLS, etc.

---

## Step 2: Analyze Existing Tenant Implementation

Search for tenant patterns:

```bash
# Find organization/tenant related files
find . -type f \( -name "*org*" -o -name "*tenant*" -o -name "*organization*" \) | grep -v node_modules

# Find RLS policies (if Supabase)
find . -type f -name "*.sql" | xargs grep -l "POLICY\|RLS" 2>/dev/null

# Find tenant context providers
find . -type f -name "*.tsx" | xargs grep -l "organization\|tenant\|org_id" 2>/dev/null | head -20

# Find how org_id is passed
grep -r "organization_id\|org_id\|tenant_id" --include="*.ts" --include="*.tsx" | head -20
```

---

## Step 3: Clarifying Questions

```
I found the following multi-tenant patterns:

Tenant Model: [detected - organization, workspace, team, etc.]
Tenant ID Field: [detected - organization_id, tenant_id, etc.]
Isolation Strategy: [detected]

Please confirm or correct:

1. What is a "tenant" called in this project?
   A. Organization
   B. Workspace
   C. Team
   D. Company
   E. Other: [specify]

2. How is tenant isolation enforced?
   A. Application-level filtering (WHERE org_id = ?)
   B. Database RLS policies
   C. Both application and RLS
   D. Separate databases per tenant
   E. Other: [specify]

3. How does a user get their current tenant?
   A. From session/JWT claims
   B. From URL (subdomain or path)
   C. From a context provider
   D. From user profile lookup
   E. Other: [specify]

4. Can users belong to multiple tenants?
   A. No, one tenant per user
   B. Yes, with tenant switching
   C. Yes, with default tenant
```

---

## Step 4: Generate the Skill

Create `docs/skills/tenant-context/SKILL.md`:

```markdown
---
name: tenant-context
description: "Work with multi-tenant context in [PROJECT_NAME] - scoping data, switching tenants, enforcing isolation"
project-specific: true
generated-by: multi-tenant-skill-generator
generated-at: [DATE]
---

# Tenant Context Skill

How multi-tenancy works in this project and how to correctly scope all data operations.

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Get current org | [project-specific] |
| Scope a query | [project-specific] |
| Switch organization | [project-specific] |
| Create org-scoped resource | [project-specific] |

---

## Tenant Model

This project uses **[TENANT_NAME]** (e.g., "Organization") as the tenant boundary.

- Tenant ID field: `[TENANT_ID_FIELD]` (e.g., `organization_id`)
- Users can belong to: [one / multiple] tenant(s)
- Isolation: [RLS / application-level / both]

---

## Getting Current Tenant

### In Server Components/Actions

\`\`\`typescript
import { getCurrentOrganization } from '@/lib/organization'

const org = await getCurrentOrganization()
// org.id, org.name, org.slug
\`\`\`

### In Client Components

\`\`\`typescript
import { useOrganization } from '@/hooks/useOrganization'

const { organization, loading } = useOrganization()
\`\`\`

### From Session

\`\`\`typescript
import { createClient } from '@/lib/supabase/server'

const supabase = await createClient()
const { data: { user } } = await supabase.auth.getUser()
const orgId = user?.user_metadata?.organization_id
\`\`\`

---

## Scoping Database Queries

### CRITICAL: Every query MUST be scoped

\`\`\`typescript
// CORRECT - always scope to organization
const { data } = await supabase
  .from('resources')
  .select('*')
  .eq('organization_id', orgId)

// WRONG - fetches ALL organizations' data
const { data } = await supabase
  .from('resources')
  .select('*')
```

### With RLS (if enabled)

If RLS is enabled, the database enforces tenant isolation automatically via policies. However, you should still include the filter for:
- Clarity in code
- Defense in depth
- Working correctly if RLS is ever disabled

---

## Creating Tenant-Scoped Resources

Always include the tenant ID when inserting:

\`\`\`typescript
const { data, error } = await supabase
  .from('resources')
  .insert({
    name: 'New Resource',
    organization_id: orgId,  // REQUIRED
    created_by: userId
  })
\`\`\`

---

## Switching Tenants

[If users can belong to multiple tenants]

\`\`\`typescript
import { switchOrganization } from '@/lib/organization'

// Switch to a different organization
await switchOrganization(newOrgId)

// This updates the session and redirects
\`\`\`

---

## URL-Based Tenant Resolution

[If tenant is determined by URL]

\`\`\`typescript
// From subdomain: acme.app.com → org = "acme"
const org = request.headers.get('host')?.split('.')[0]

// From path: /org/acme/dashboard → org = "acme"
const org = params.orgSlug
\`\`\`

---

## RLS Policies

[If using Supabase RLS]

The following RLS policies enforce tenant isolation:

\`\`\`sql
-- Example policy on resources table
CREATE POLICY "Users can only see their org's resources"
ON resources FOR SELECT
USING (organization_id = auth.jwt() ->> 'organization_id');
\`\`\`

**Location:** `[MIGRATIONS_PATH]`

---

## Common Mistakes

### 1. Forgetting to scope queries
```typescript
// BAD - security vulnerability
const { data } = await supabase.from('resources').select('*')

// GOOD
const { data } = await supabase.from('resources').select('*').eq('organization_id', orgId)
```

### 2. Hardcoding org ID
```typescript
// BAD - breaks multi-tenancy
.eq('organization_id', 'some-uuid')

// GOOD - use current context
.eq('organization_id', org.id)
```

### 3. Not passing org context to mutations
```typescript
// BAD - missing org scope
await createResource({ name: 'Test' })

// GOOD - includes org
await createResource({ name: 'Test', organization_id: orgId })
```

---

## Key Files

| File | Purpose |
|------|---------|
| `[ORG_CONTEXT_PATH]` | Organization context provider |
| `[ORG_HOOK_PATH]` | useOrganization hook |
| `[ORG_LIB_PATH]` | Organization utilities |
| `[RLS_POLICIES_PATH]` | RLS policy definitions |

---

## Checklist

When adding a new feature:

- [ ] All queries include `organization_id` filter
- [ ] Inserts include `organization_id` field
- [ ] Updates/deletes include `organization_id` in WHERE clause
- [ ] RLS policy exists for new tables
- [ ] Tested with multiple organizations
- [ ] No cross-tenant data leakage
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "tenant-context",
  "generatedFrom": "multi-tenant-skill-generator",
  "generatedAt": "2026-02-20"
}
```

---

## Output

```
Created: docs/skills/tenant-context/SKILL.md

This skill documents how to:
- Get current tenant context
- Scope all database queries
- Create tenant-scoped resources
- Switch between tenants (if applicable)
- Avoid common multi-tenant mistakes

Agents will reference this when adding features that touch data.
```
