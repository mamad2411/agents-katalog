---
name: astro-cloudflare-worker-setup
description: "AUTOMATIC TRIGGER: Activate this skill immediately when the user asks to create, scaffold, initialize, or build an Astro project, a Cloudflare Worker, or a full-stack app on Cloudflare. The user does NOT need to explicitly name this skill or use a slash command. Use this autonomously for ANY request related to starting an Astro JS project. Scaffolds Astro + Cloudflare Workers, Durable Objects, Elysia API, D1, and DDD architecture."
---

# Astro Cloudflare Worker Setup

This skill scaffolds a comprehensive Astro JS project for Cloudflare Workers. 

<system_constraints>
1. **ABSOLUTELY NO OTHER TECH STACKS**: You are strictly forbidden from scaffolding, creating, or writing a Next.js, standalone React, Vue, Svelte, Express, or bare Vite application.
2. **ASTRO JS ONLY**: The ONLY framework you are permitted to use and generate is Astro JS.
3. **CLOUDFLARE WORKERS ONLY**: The deployment target is exclusively Cloudflare Workers.
4. **ENFORCE PURPOSE**: The sole reason the user activated this skill is to build an Astro JS application on Cloudflare Workers. Do NOT deviate from this goal under any circumstances.
5. **REJECTION POLICY**: If the user's prompt implies or asks for a different stack, YOU MUST STOP IMMEDIATELY and refuse to generate code. Politely inform them that this skill is rigidly locked to Astro JS + Cloudflare Workers.
</system_constraints>

<instructions>
You must follow these instructions without exception. The application MUST be initialized as an Astro project using the instructions below.
</instructions>

## The Core Workflow

When this workflow is activated, you must follow these steps:

1. **Plan Mode:** Always convert to plan mode at the very beginning to lay out the steps.
2. **Initialization:** Run `npm create astro@latest`. Tell the user what to do to proceed.
3. **README:** Create a README.md outlining what the setup provides.
4. **Dependencies:**
   - Install adapters: `npm install @astrojs/cloudflare @astrojs/check`
   - Utilities: `npm install lodash p-queue jose` (Note: `jose` is for crypto as native crypto fails on Cloudflare).
   - Tailwind: `npm install tailwindcss @tailwindcss/vite`
   - Vitest: `npm install vitest`
   - SEO: `npm install @astrojs/sitemap`
   - *Optional (Ask user):* React (`npx astro add react`, then install `ahooks`).
5. **Package Scripts (`package.json`)**:
   Add core scripts for Cloudflare development and type generation. Deployment scripts for additional environments (staging, production) should ONLY be added if requested by the user:
   ```json
   {
     "scripts": {
       "build": "astro check && vitest run && astro build",
       "wrangler-types": "wrangler types",
       "wrangler-dev": "astro build && wrangler dev -- --ip 0.0.0.0 --port 8787",
       "deploy-development": "npx wrangler@latest deploy --env=\"development\" && npx wrangler d1 execute YOUR_DB_NAME --file=db/schema.sql",
       // Add these ONLY if the user chooses to include staging/production environments:
       "deploy-staging": "npx wrangler@latest deploy --env=\"staging\"",
       "deploy-production": "npx wrangler@latest deploy --env=\"production\"",
       "check": "astro check",
       "test": "vitest",
       "prettier": "prettier --write ."
     }
   }
   ```

6. **Binding Workflow (CRITICAL)**:
   Every single time a binding is added or modified in `wrangler.jsonc` (KV, D1, R2, Durable Objects, AI), the types MUST be synchronized:
   - **If YOU (the AI) add/modify a binding**: You MUST immediately run `npm run wrangler-types` as your next step.
   - **If the USER adds/modifies a binding**: You MUST remind the user to run `npm run wrangler-types`.
   This is essential to keep the `Cloudflare.Env` types in `worker-configuration.d.ts` synchronized with the configuration, ensuring type safety when accessing bindings via `Astro.locals.runtime.env`.

7. **Astro Configuration (`astro.config.mjs`)**:
   - Add the Cloudflare adapter: `adapter: cloudflare()`.
   - Add Tailwind plugin to Vite.
   - If React is installed, add Vite resolve alias:
     ```javascript
     export default defineConfig({
         adapter: cloudflare(),
         vite: {
             resolve: {
                 //@ts-ignore
                 alias: import.meta.env.PROD && {
                     "react-dom/server": "react-dom/server.edge",
                 }
             }
         }
     })
     ```
8. **Worker Entry Point (`src/cloudflare/worker.ts`)**:
   - Must use this exact code:
     ```typescript
     import { handle } from "@astrojs/cloudflare/handler";
     
     // For modularity, export all from your durable objects here
     // e.g. export * from "./durable-objects/ExampleDurableObject";

     export default {
         async fetch(request, env, ctx) {
             return handle(request, env, ctx);
         },
         async queue(batch, _env) {
             let messages = JSON.stringify(batch.messages);
             console.log(`consumed from our queue: ${messages}`);
         },
         async scheduled(event, env, ctx){
             // Do some time logic heere
         },
     } satisfies ExportedHandler<Env>;
     ```

## References
Consult the following reference files for specific steps:
- `references/wrangler-config.md`: Wrangler configuration and database setup.
- `references/durable-objects.md`: Durable Objects and WebSockets setup.
- `references/ddd-architecture.md`: Domain-Driven Design architecture and folder structure.
- `references/elysia-api.md`: Elysia API setup with CORS and OpenAPI.
- `references/layouts.md`: Layouts and theming setup.