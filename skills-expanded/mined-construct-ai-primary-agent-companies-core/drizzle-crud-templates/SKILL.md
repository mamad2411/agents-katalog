---
name: drizzle-crud-templates
description: >
  Routes Drizzle ORM template generation to the Database CRUD Orchestrator for
  generating type-safe, FK-aware CRUD operations in TypeScript/Python against
  Paperclip's Supabase database. Bridges the gap between schema introspection
  and programmatic agent access.
company: paperclipforge-ai
---

# Drizzle CRUD Templates

## Overview
This skill generates type-safe Drizzle ORM CRUD templates for programmatic database operations against Paperclip's Supabase database. It handles FK resolution, transaction wrapping, and type validation so that consuming agents get compile-safe data access code.

## Routing Criteria

Route to this skill when:
- TypeScript Drizzle ORM code is needed for CRUD operations
- Python supabase-py code is needed for programmatic access
- Type-safe FK lookup templates are required
- Transaction-wrapped CRUD patterns are needed
- Auto-generated repository/service layer code is desired
- Migration from raw SQL to ORM-based access is planned

## Template Patterns

### TypeScript (Drizzle ORM)

#### Repository Pattern Template

```typescript
// packages/db/src/repositories/agents.repository.ts
import { db } from '../db';
import { agents, companies, agentApiKeys } from '../schema';
import { eq, and } from 'drizzle-orm';

export class AgentRepository {
  /**
   * Create agent with FK-safe references
   * Auto-resolves company_id from company name
   */
  async create(data: {
    name: string;
    title: string;
    companyName: string;
    reportsToAgentName?: string;
    role?: string;
    status?: 'active' | 'idle' | 'paused';
    capabilities?: string;
    adapterConfig?: Record<string, unknown>;
  }) {
    return db.transaction(async (tx) => {
      // Resolve company FK
      const [company] = await tx
        .select()
        .from(companies)
        .where(eq(companies.name, data.companyName))
        .limit(1);
      if (!company) throw new Error(`Company "${data.companyName}" not found`);

      // Resolve manager FK (optional)
      let reportsToId: string | null = null;
      if (data.reportsToAgentName) {
        const [manager] = await tx
          .select({ id: agents.id })
          .from(agents)
          .where(
            and(
              eq(agents.name, data.reportsToAgentName),
              eq(agents.companyId, company.id)
            )
          )
          .limit(1);
        if (!manager) throw new Error(`Manager "${data.reportsToAgentName}" not found`);
        reportsToId = manager.id;
      }

      // Insert with resolved FKs
      const [agent] = await tx
        .insert(agents)
        .values({
          id: crypto.randomUUID(),
          companyId: company.id,
          name: data.name,
          title: data.title,
          role: data.role ?? 'specialist',
          status: data.status ?? 'active',
          reportsTo: reportsToId,
          capabilities: data.capabilities ?? null,
          adapterConfig: data.adapterConfig ?? {},
          createdAt: new Date(),
          updatedAt: new Date(),
        })
        .returning();

      return agent;
    });
  }

  /**
   * Safe delete with FK cascade awareness
   */
  async delete(id: string) {
    return db.transaction(async (tx) => {
      // 1. Delete CASCADE children explicitly
      await tx.delete(agentApiKeys).where(eq(agentApiKeys.agentId, id));

      // 2. Nullify SET NULL references
      await tx
        .update(agents)
        .set({ reportsTo: null })
        .where(eq(agents.reportsTo, id));

      // 3. Delete target
      const [deleted] = await tx
        .delete(agents)
        .where(eq(agents.id, id))
        .returning();

      return deleted;
    });
  }
}
```

#### Service Layer Template

```typescript
// services/agent.service.ts
import { AgentRepository } from '../repositories/agents.repository';
import { z } from 'zod';

const CreateAgentSchema = z.object({
  name: z.string().min(1).max(100),
  title: z.string().min(1).max(200),
  companyName: z.string().min(1),
  reportsToAgentName: z.string().optional(),
  role: z.string().default('specialist'),
});

export class AgentService {
  constructor(private repo: AgentRepository) {}

  async createAgent(input: unknown) {
    const validated = CreateAgentSchema.parse(input);
    return this.repo.create(validated);
  }

  async deleteAgent(id: string) {
    return this.repo.delete(id);
  }
}
```

### Python (supabase-py)

```python
# repositories/agent_repository.py
from supabase import create_client
from typing import Optional
import uuid

class AgentRepository:
    def __init__(self, supabase_url: str, service_role_key: str):
        self.client = create_client(supabase_url, service_role_key)

    def create(self, name: str, title: str, company_name: str,
               reports_to_name: Optional[str] = None) -> dict:
        # Resolve company FK
        company = (self.client.table('companies')
                   .select('id')
                   .eq('name', company_name)
                   .execute())
        if not company.data:
            raise ValueError(f"Company '{company_name}' not found")
        company_id = company.data[0]['id']

        # Resolve reports_to FK (optional)
        reports_to_id = None
        if reports_to_name:
            manager = (self.client.table('agents')
                      .select('id')
                      .eq('name', reports_to_name)
                      .eq('company_id', company_id)
                      .execute())
            if manager.data:
                reports_to_id = manager.data[0]['id']

        # Insert with resolved FKs
        result = (self.client.table('agents')
                  .insert({
                      'id': str(uuid.uuid4()),
                      'company_id': company_id,
                      'name': name,
                      'title': title,
                      'reports_to': reports_to_id,
                      'status': 'active',
                  })
                  .execute())

        return result.data[0]

    def bulk_delete(self, agent_ids: list[str]) -> dict:
        """FK-safe bulk deletion"""
        # Delete in dependency order - children first
        for table in ['agent_api_keys', 'agent_config_revisions',
                      'agent_runtime_state', 'agent_wakeup_requests',
                      'agent_task_sessions']:
            (self.client.table(table)
             .delete()
             .in_('agent_id', agent_ids)
             .execute())

        # Nullify self-references
        (self.client.table('agents')
         .update({'reports_to': None})
         .in_('reports_to', agent_ids)
         .execute())

        # Delete targets
        return (self.client.table('agents')
                .delete()
                .in_('id', agent_ids)
                .execute())
```

## Integration with Drizzle Kit

After schema changes are made via Supabase visual editor:

```bash
# 1. Introspect updated schema from Supabase
npx drizzle-kit introspect:pg \
  --connection-string="postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres" \
  --out="./packages/db/src/schema"

# 2. Generate migration
pnpm db:generate

# 3. Push schema changes
DATABASE_URL="postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres" \
  npx drizzle-kit push

# 4. Update template types
# The CRUD Orchestrator will auto-regenerate templates based on updated schema
```

## Template Validation Checklist

Before generating any template, verify:
- [ ] FK referenced tables exist in schema
- [ ] Column names match snake_case convention
- [ ] FK rules are understood (CASCADE/SET NULL/NO ACTION)
- [ ] Self-referencing FKs are handled
- [ ] Transaction boundaries are correct
- [ ] Error handling covers FK violation scenarios
- [ ] Types match Drizzle-generated schema types

## Related Skills

- `crud-operations` - Core CRUD patterns using generated templates
- `fk-dependency-graph` - FK resolution intelligence for templates
- `database-schema-inspection` - Schema metadata for template generation
- `sql-generation` - Raw SQL fallback for ORM-unsupported operations

---

*This skill ensures all generated CRUD templates are type-safe, FK-aware, and ready for immediate use by consuming agents.*