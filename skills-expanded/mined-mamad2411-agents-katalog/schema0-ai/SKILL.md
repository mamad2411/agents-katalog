---
name: schema0-ai
description: AI SDK integration with ORPC — chat streaming, prompt-response, tool calling, and provider configuration
---

# AI Integration

AI SDK integration with ORPC for chat, prompt-response, and tool-calling features.

## Generator Commands

```bash
# Full-stack chat with streaming
schema0 sandbox exec "bun run .claude/skills/ai-integration/scripts/generate.ts chat <name>"

# Simple prompt-response (no streaming)
schema0 sandbox exec "bun run .claude/skills/ai-integration/scripts/generate.ts simple <name>"

# Backend router only
schema0 sandbox exec "bun run .claude/skills/ai-integration/scripts/generate.ts router <name>"

# Tool definition for function calling
schema0 sandbox exec "bun run .claude/skills/ai-integration/scripts/generate.ts tool <name>"
```

## Prerequisites

1. **Add API key** using `manage-secrets` skill to securely add it and update `packages/auth/env.ts`
2. **Install dependencies:**
   ```bash
   schema0 sandbox exec "bun add ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google @orpc/ai-sdk @orpc/client"
   ```
3. **Add key to env schema** in `packages/auth/env.ts` (e.g., `OPENAI_API_KEY: z.string().optional()`)

## Generated Files

| Template            | Output Location                        | Purpose                               |
| ------------------- | -------------------------------------- | ------------------------------------- |
| `ai-router.hbs`     | `packages/api/src/routers/[name].ts`   | ORPC router with AI SDK streaming     |
| `ai-chat-route.hbs` | `apps/web/src/routes/_auth.[name].tsx` | Full chat UI with streaming           |
| `ai-simple.hbs`     | `apps/web/src/routes/_auth.[name].tsx` | Simple prompt-response UI             |
| `ai-tool.hbs`       | `packages/api/src/tools/[name].ts`     | Tool definitions for function calling |

## Post-Generation Steps

1. Register router in `packages/api/src/routers/index.ts`
2. Add route to sidebar in `apps/web/src/components/app-sidebar.tsx`
3. Set the API key environment variable during build/deploy

## References

- `references/patterns.md` -- Chat mode, simple mode, tool calling, provider examples (OpenAI, Anthropic, Google), streaming, naming conventions
