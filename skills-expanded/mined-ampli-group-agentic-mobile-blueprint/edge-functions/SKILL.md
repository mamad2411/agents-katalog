---
name: edge-functions
description: Supabase Edge Function development patterns with Deno runtime. Use when creating, modifying, or debugging edge functions. For Langfuse tracing see the langfuse-tracing skill. For Sentry error handling see the sentry-integration skill.
---

# Supabase Edge Functions

## Runtime

Deno. Entry point: `Deno.serve()`. Files live in `supabase/functions/<name>/index.ts`.

## New Function Scaffold

```typescript
import { initSentry, handleError } from "../_shared/sentry.ts";

initSentry();

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });

  try {
    const body = await req.json();
    const result = { message: "Hello" };
    return new Response(JSON.stringify(result), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (error) {
    return handleError(error, { functionName: "my-function", corsHeaders });
  }
});
```

For AI calls, wrap with `withTrace()` — see the **langfuse-tracing** skill.

## Imports

- Shared code: `../_shared/sentry.ts`, `../_shared/langfuse/gemini.ts`
- External: via import map in `supabase/functions/deno.json`
- Convention: `npm:` prefix for npm packages, URLs for Deno packages

## Calling from Frontend/Mobile

```typescript
const { data, error } = await supabase.functions.invoke('my-function', {
  body: { prompt: 'Hello' },
});
```

## Database Migrations

Path: `supabase/migrations/`. Naming: `00000000000000_slug.sql`.

Rules:
- Enable RLS on every table
- Policies use `auth.uid()` for row-level access
- Add `updated_at` trigger for mutable tables
- Index foreign keys and common filter columns
- Storage bucket policies: `auth.uid()::text = (storage.foldername(name))[1]`

## Local Development

```bash
mise run supabase:function   # Starts functions with hot reload
```

Env vars for functions go in `supabase/functions/.env.local`.

## Deploy

```bash
supabase functions deploy <function-name>
```
