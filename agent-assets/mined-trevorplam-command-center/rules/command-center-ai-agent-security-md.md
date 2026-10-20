---
description: Run AI Agent and Agentic Systems Security Check
globs: ['**/agents/**/*.ts', '**/ai/**/*.ts', '**/llm/**/*.ts', '**/tools/**/*.ts']
---

# Security: AI Agent & Agentic Systems Security

<audit_rules>

- You MUST implement prompt injection defenses using input sanitization, prompt templating, and instruction following techniques.
- You MUST enforce tool usage validation with explicit permission checks and sandboxed execution environments.
- You MUST implement output validation and sanitization to prevent data exfiltration and malicious content generation.
- You MUST configure rate limiting and cost controls to prevent unbounded consumption and resource exhaustion.
- You MUST ensure agent capabilities are properly scoped and limited to prevent excessive agency and unauthorized actions.
- You MUST implement audit logging for all agent decisions, tool usage, and external API calls.
- You MUST verify that system prompts and sensitive configurations are not exposed through output or error messages.
- You MUST implement human-in-the-loop controls for high-risk operations and critical decisions.
  </audit_rules>

<example_good>

```typescript
import { z } from 'zod'
import { sanitizeInput } from '@/lib/sanitize'
import { rateLimit } from '@/lib/rate-limit'

const ToolRequestSchema = z.object({
  tool: z.enum(['search', 'calculate', 'send_email']),
  parameters: z.object({
    query: z.string().max(1000),
    recipient: z.string().email().optional(),
  }),
})

export async function executeAgentTool(request: unknown, userId: string) {
  // Rate limiting
  await rateLimit(userId, { max: 10, window: '1m' })

  // Input validation and sanitization
  const validated = ToolRequestSchema.parse(request)
  const sanitizedQuery = sanitizeInput(validated.parameters.query)

  // Tool permission check
  if (validated.tool === 'send_email') {
    const hasPermission = await checkEmailPermission(userId)
    if (!hasPermission) {
      throw new Error('Insufficient permissions for email sending')
    }
  }

  // Audit logging
  await auditLog(userId, {
    action: 'tool_execution',
    tool: validated.tool,
    timestamp: new Date(),
  })

  // Execute in sandboxed environment
  return await executeInSandbox(validated.tool, {
    ...validated.parameters,
    query: sanitizedQuery,
  })
}
```

</example_good>

<example_bad>

```typescript
// BAD: No input validation, no rate limiting, no permissions
export async function executeAgentTool(request: any) {
  const { tool, parameters } = request

  // BAD: Direct execution without validation or sandboxing
  if (tool === 'send_email') {
    await sendEmail(parameters.recipient, parameters.content)
  }

  return { success: true }
}
```

</example_bad>
