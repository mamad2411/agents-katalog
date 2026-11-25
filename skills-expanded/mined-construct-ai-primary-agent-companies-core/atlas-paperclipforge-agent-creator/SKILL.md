---
name: atlas-paperclipforge-agent-creator
description: Routes agent creation, management, and lifecycle orchestration tasks to the Agent Creator specialist.
company: paperclipforge-ai
---

# Agent Creator and Manager

## Overview
This skill routes all agent creation, management, and lifecycle orchestration tasks to Atlas, the specialized Agent Creator and Manager for the Paperclip ecosystem. Atlas handles the complete process of designing, implementing, and deploying new AI agents across all companies.

## Routing Criteria

Route to this skill when:
- Creating new agents for any Paperclip company
- Agent lifecycle management and configuration
- Skill definition and routing setup
- Model assignment and optimization
- Agent performance monitoring and optimization
- Cross-company agent integration
- Agent decommissioning and knowledge transfer
- Agent architecture design and planning

## Capabilities

### Agent Creation & Design
- **Agent Specification**: Comprehensive agent role definition and capability planning
- **Skill Architecture**: Design of skill sets with proper routing and integration logic
- **Model Selection**: Optimal AI model assignment based on task complexity and requirements
- **Integration Planning**: Cross-company integration and collaboration pattern design

### Technical Implementation
- **Database Operations**: Complex SQL execution for agent registration and metadata management
- **API Configuration**: Agent API access setup and authentication configuration
- **Skill Routing**: Sophisticated routing logic implementation for task distribution
- **Performance Optimization**: Agent performance benchmarking and optimization strategies

### Lifecycle Management
- **Configuration Management**: Agent parameter setup, permissions, and access controls
- **Version Control**: Agent updates, skill enhancements, and capability expansions
- **Monitoring Systems**: Performance tracking and optimization opportunity identification
- **Quality Assurance**: Agent functionality validation and integration quality checks

## Related Skills

- `assignment-specialist-paperclipforge-issue-routing` - Agent workload and task assignment optimization
- `quality-controller-paperclipforge-quality-assurance` - Agent validation and quality assurance
- `operations-director-paperclipforge-operations-management` - Operational oversight and coordination

## Examples

## SQL Templates

**Use pre-validated templates from `docs-paperclip/schema/templates/`:**

| Operation | Template |
|-----------|---------|
| Create agent | `REGISTER-agent.sql` |
| Add API key | `ADD-agent-api-keys.sql` |
| Delete agent | `DELETE-agent.sql` |
| Validate schema | `CHECK-column-existence.sql` |

**⚠️ CRITICAL**: The `agents` table has TWO name fields:
- `name` = agent identifier (e.g., "infraforge-ai-supabase-specialist")
- `title` = human-readable name (e.g., "Supabase DB Specialist")

**Never use `slug`** - this column does NOT exist in the schema.

### Agent Creation Workflow (Template-Derived)
```sql
-- Use REGISTER-agent.sql template from docs-paperclip/schema/templates/
BEGIN;

INSERT INTO agents (
  id, company_id, name, role, title, capabilities,
  reports_to, status, metadata, permissions, created_at, updated_at
) VALUES (
  gen_random_uuid(),
  (SELECT id FROM companies WHERE name = 'InfraForge AI'),
  'Nimbus',
  'specialist',
  'Supabase Database Specialist',
  'Supabase API mastery, PostgreSQL expertise, SQL generation/testing',
  (SELECT id FROM agents WHERE name = 'orchestrator-infraforge-ceo'),
  'active',
  '{"team": "infrastructure", "specialization": "Supabase Database Operations"}'::jsonb,
  '{"can_access_supabase": true, "database_admin": true}'::jsonb,
  NOW(),
  NOW()
);

COMMIT;
```

### Skill Definition Process
```yaml
# Agent skill specification
name: supabase-specialist
description: Routes Supabase database operations to specialized agent
routing_criteria:
  - supabase_api_operations
  - postgresql_expertise
  - sql_generation_testing
  - authentication_troubleshooting
capabilities:
  - REST API operations
  - GraphQL query development
  - Real-time subscriptions
  - Performance optimization
```

### Model Assignment Strategy
```sql
-- Optimal model assignment for complex database operations
INSERT INTO agent_models (
  agent_id, model_id, assignment_type, priority,
  temperature, max_tokens, assigned_by, reason
) VALUES (
  'infraforge-ai-supabase-specialist',
  'GLM-5.1',
  'primary',
  1,
  0.1,
  4096,
  'atlas-agent-creator',
  'Advanced reasoning required for complex SQL generation and database optimization'
);
```

---

*This skill routes to Atlas, the Agent Creator and Manager, for comprehensive agent lifecycle management across the Paperclip ecosystem.*