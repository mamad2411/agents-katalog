---
name: ai-tools-skill-generator
description: "Generate a project-specific AI tools skill. Use when a project has ai: true and aiTools configuration. Triggers on: generate ai tools skill, create chatbot tools, ai-tools-skill-generator."
type: meta
generates: ai-tools
trigger:
  capability: ai
  config: capabilities.aiTools
---

# AI Tools Skill Generator

Generate a project-specific `ai-tools` skill that documents exactly how to create and update AI/chatbot tools in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing AI tools implementation
3. Ask clarifying questions about tool patterns
4. Generate `docs/skills/ai-tools/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Look for:
- `capabilities.ai: true`
- `capabilities.aiTools.system` — openai-functions, langchain, mcp, custom
- `capabilities.aiTools.schemaPath` — where tool schemas live
- `capabilities.aiTools.implementationPath` — where implementations live

---

## Step 2: Analyze Existing AI Tools

```bash
# Find tool definitions
find . -type f \( -name "*tool*" -o -name "*function*" \) | grep -v node_modules | head -20

# Find OpenAI integration
grep -r "openai\|chatgpt\|gpt-4\|gpt-3" --include="*.ts" | head -10

# Find existing tool schemas
find . -type f -name "*.ts" | xargs grep -l "type.*function\|tools\[" | head -10

# Look at tools directory
ls -la src/lib/ai/tools/ 2>/dev/null || ls -la lib/tools/ 2>/dev/null
```

---

## Step 3: Clarifying Questions

```
I found the following AI tools patterns:

Tool System: [detected]
Schema Location: [path if found]
Implementation Location: [path if found]

Please confirm or correct:

1. What AI tool system do you use?
   A. OpenAI function calling
   B. LangChain tools
   C. MCP (Model Context Protocol)
   D. Custom implementation
   E. Other: [specify]

2. How are tools defined?
   A. JSON schemas + TypeScript implementations
   B. TypeScript decorators
   C. Zod schemas with auto-generation
   D. Inline in chat configuration

3. Where do tools live?
   A. Single tools directory
   B. Co-located with features
   C. Generated from API specs
```

---

## Step 4: Generate the Skill

Create `docs/skills/ai-tools/SKILL.md`:

```markdown
---
name: ai-tools
description: "Create and update AI chatbot tools in [PROJECT_NAME]"
project-specific: true
generated-by: ai-tools-skill-generator
generated-at: [DATE]
---

# AI Tools Skill

How to create and modify AI/chatbot tools in this project.

---

## Quick Reference

| Task | Location |
|------|----------|
| Add new tool | `[TOOLS_PATH]` |
| Define schema | `[SCHEMA_PATH]` |
| Implement handler | `[IMPLEMENTATION_PATH]` |
| Register tool | `[REGISTRATION_PATH]` |

---

## Architecture

- **Tool System:** [TOOL_SYSTEM] (e.g., OpenAI function calling)
- **Schema Path:** `[SCHEMA_PATH]`
- **Implementation Path:** `[IMPLEMENTATION_PATH]`

---

## Key Files

| File | Purpose |
|------|---------|
| `[SCHEMA_PATH]` | Tool schema definitions |
| `[IMPLEMENTATION_PATH]` | Tool implementations |
| `[TYPES_PATH]` | Tool type definitions |
| `[REGISTRY_PATH]` | Tool registration |

---

## Creating a New Tool

### Step 1: Define the Schema

\`\`\`typescript
// [SCHEMA_PATH]/list-tasks.ts
import { z } from 'zod'

export const listTasksSchema = {
  name: 'list_tasks',
  description: 'List tasks for the current user, optionally filtered by status or project',
  parameters: z.object({
    status: z.enum(['pending', 'in_progress', 'completed']).optional()
      .describe('Filter by task status'),
    projectId: z.string().uuid().optional()
      .describe('Filter by project ID'),
    limit: z.number().min(1).max(100).default(20)
      .describe('Maximum number of tasks to return'),
  }),
}

export type ListTasksInput = z.infer<typeof listTasksSchema.parameters>
\`\`\`

### Step 2: Implement the Handler

\`\`\`typescript
// [IMPLEMENTATION_PATH]/list-tasks.ts
import { createClient } from '@/lib/supabase/server'
import { ListTasksInput } from '@/lib/ai/schemas/list-tasks'

export async function listTasks(
  input: ListTasksInput,
  context: { userId: string; organizationId: string }
) {
  const supabase = await createClient()
  
  let query = supabase
    .from('tasks')
    .select('id, title, status, due_date, project:projects(name)')
    .eq('organization_id', context.organizationId)
    .order('created_at', { ascending: false })
    .limit(input.limit)
  
  if (input.status) {
    query = query.eq('status', input.status)
  }
  
  if (input.projectId) {
    query = query.eq('project_id', input.projectId)
  }
  
  const { data, error } = await query
  
  if (error) throw error
  
  return {
    tasks: data,
    count: data.length,
  }
}
\`\`\`

### Step 3: Register the Tool

\`\`\`typescript
// [REGISTRY_PATH]/index.ts
import { listTasksSchema, ListTasksInput } from './schemas/list-tasks'
import { listTasks } from './handlers/list-tasks'
// ... other imports

export const tools = [
  {
    schema: listTasksSchema,
    handler: listTasks,
  },
  // ... other tools
]

// Export for OpenAI
export const toolDefinitions = tools.map(t => ({
  type: 'function' as const,
  function: {
    name: t.schema.name,
    description: t.schema.description,
    parameters: zodToJsonSchema(t.schema.parameters),
  },
}))

// Tool executor
export async function executeTool(
  name: string,
  args: unknown,
  context: ToolContext
) {
  const tool = tools.find(t => t.schema.name === name)
  if (!tool) throw new Error(\`Unknown tool: \${name}\`)
  
  const validated = tool.schema.parameters.parse(args)
  return tool.handler(validated, context)
}
\`\`\`

---

## Tool Design Guidelines

### Naming Convention

- Use snake_case: `list_tasks`, `create_project`, `update_user`
- Start with action verb: `get_`, `list_`, `create_`, `update_`, `delete_`
- Be specific: `list_tasks` not `tasks`

### Parameters

- Make parameters optional when sensible (provide defaults)
- Use enums for fixed choices
- Add `.describe()` to all parameters
- Validate with Zod

### Return Values

- Return structured data, not formatted text
- Include relevant IDs for follow-up actions
- Return counts/metadata when listing

### Error Handling

- Let errors propagate (caught by executor)
- Use descriptive error messages
- Don't expose internal details to users

---

## Common Tool Patterns

### List/Query

\`\`\`typescript
// List with filters
{
  name: 'list_items',
  description: 'List items with optional filters',
  parameters: z.object({
    status: z.enum(['active', 'archived']).optional(),
    search: z.string().optional(),
    limit: z.number().default(20),
    offset: z.number().default(0),
  }),
}
\`\`\`

### Get Single

\`\`\`typescript
{
  name: 'get_item',
  description: 'Get details of a specific item',
  parameters: z.object({
    id: z.string().uuid().describe('The item ID'),
  }),
}
\`\`\`

### Create

\`\`\`typescript
{
  name: 'create_item',
  description: 'Create a new item',
  parameters: z.object({
    name: z.string().min(1).describe('Item name'),
    description: z.string().optional(),
    type: z.enum(['A', 'B', 'C']),
  }),
}
\`\`\`

### Update

\`\`\`typescript
{
  name: 'update_item',
  description: 'Update an existing item',
  parameters: z.object({
    id: z.string().uuid().describe('The item ID'),
    name: z.string().min(1).optional(),
    status: z.enum(['active', 'archived']).optional(),
  }),
}
\`\`\`

---

## Testing Tools

### Unit Testing

\`\`\`typescript
import { listTasks } from '@/lib/ai/handlers/list-tasks'

describe('listTasks', () => {
  it('returns tasks for organization', async () => {
    const result = await listTasks(
      { limit: 10 },
      { userId: 'user-1', organizationId: 'org-1' }
    )
    
    expect(result.tasks).toHaveLength(expect.any(Number))
    expect(result.count).toBe(result.tasks.length)
  })
  
  it('filters by status', async () => {
    const result = await listTasks(
      { status: 'completed', limit: 10 },
      { userId: 'user-1', organizationId: 'org-1' }
    )
    
    expect(result.tasks.every(t => t.status === 'completed')).toBe(true)
  })
})
\`\`\`

### Manual Testing

Use the chat interface to test tools naturally:

> "Show me my pending tasks"
> "Create a task called 'Review PR' in the Web App project"
> "Mark task xyz as completed"

---

## Checklist

When adding a new tool:

- [ ] Define Zod schema with descriptions
- [ ] Implement handler with proper typing
- [ ] Scope queries to organization (tenant isolation)
- [ ] Register in tools index
- [ ] Add unit tests
- [ ] Test via chat interface
- [ ] Document in tool catalog (if exists)
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "ai-tools",
  "generatedFrom": "ai-tools-skill-generator",
  "generatedAt": "2026-02-20"
}
```
