---
name: customware-ai
description: Use this skill when adding or changing AI chat, text generation, reasoning, tools, model selection, or structured JSON output in a Customware-generated React Router and Hono app. It covers the server-only Customware AI Gateway, AI SDK with the OpenRouter adapter, AI Elements UI, supported model choices, and mandatory live model and structured-output checks.
---

# Customware AI

Build AI features through the Customware AI Gateway. Use AI SDK on the Hono backend and AI Elements in the React Router SPA when a chat UI is needed.

**Preflight security rule:** Treat `.env` and every `.env.*` file as inaccessible. Do not read, list, search, preview, or request permission for them. Only a runtime command using `node --env-file=.env ...` may reference `.env`, and that command must not print environment values.

This is the single skill for the complete integration. Do not install or ask the agent to use a separate AI Elements skill; the relevant AI Elements guidance is adapted into this skill's references.

## Read First

- Always read [references/gateway-backend.md](references/gateway-backend.md).
- Always read [references/models.md](references/models.md).
- For chat or other conversational UI, read [references/ai-elements-ui.md](references/ai-elements-ui.md).
- For server tools, tool-backed chat, or any AI action that fetches live app data, read [references/tool-usage.md](references/tool-usage.md).
- For card-style AI UI, tool-rendered UI, typed message parts, or streamed custom UI state, read [references/generative-ui.md](references/generative-ui.md).
- For AI UI, read [references/ai-elements-catalog.md](references/ai-elements-catalog.md), select the needed components, then read only those linked files under `references/components/`. Open a component's linked example files only while implementing it. Never load the entire components folder or all examples.
- For JSON or other typed output, read [references/structured-output.md](references/structured-output.md).
- When starting from bundled code, read [references/examples.md](references/examples.md).
- Before finishing any implementation, read and follow [references/verification.md](references/verification.md).

## Non-Negotiables

- Call the Customware AI Gateway only from server code. Browser code calls the app's own Hono endpoint.
- Read the gateway secret only from `CUSTOMWARE_AI_GATEWAY_KEY`.
- Never expose the key through `VITE_*`, browser bundles, API responses, logs, HTML, or client-side state.
- Never read `.env` or any `.env.*` file with a file/tool read, and never request permission to do so. Never run `cat`, `head`, `tail`, `sed`, `awk`, `rg`, `grep`, `ls`, `stat`, or any other command against `.env`. The only allowed reference is a check command whose argument is exactly `node --env-file=.env ...`; that command must not print environment variables. Never inspect the key by printing `printenv`, request headers, or provider objects. Log only non-sensitive pass/fail evidence.
- Hardcode the Customware gateway base URL in server code. Do not add a gateway URL environment variable.
- Use this exact adapter base URL:
  `https://app.customware.ai/api/orgs/${orgId}/projects/${projectId}/ai/v1`
- Always use the real Customware `orgId` and `projectId`. Never use placeholders or accept them from the browser for each request.
- Use `@openrouter/ai-sdk-provider`; do not use provider-specific SDKs or call OpenRouter directly.
- Do not pass a preset, provider routing, fallback model list, metadata, trace id, or OpenRouter user id. The gateway owns these controls.
- Default to `google/gemini-3-flash-preview` unless the user selects another model or the task clearly requires one of the documented alternatives.
- Keep the chosen model id and provider options in one server-owned module/constant. Routes and services must import that value; do not duplicate model literals or add a model catalog/picker when the feature does not require user choice.
- If the user names or changes a model during development, send a live `hi` request through that exact model before finishing.
- If the feature generates JSON, run the one-key structured-output check before finishing.
- Match the requested JSON field names and shape exactly. Define one shared Zod contract in a neutral shared module/package (for example `shared/contracts/`) that both app and server may import; the browser must never import from `server/`, and the schema/enums must never be duplicated. Product-requested limits, such as a 20,000-character input bound, are valid when documented by the feature.
- Any upstream AI failure must become a generic, user-safe error at the app boundary; never render raw transport/provider errors.
- Keep database access server-owned. Never execute arbitrary model-written SQL. If a feature needs database access, let the model choose a structured tool input and let the server build the read-only, parameterized query from allowlisted filters, tables, or query helpers.
- AI Elements works in the React Router client-only SPA. Do not introduce Next.js or App Router route handlers. Generated `"use client"` directives are harmless React boundary markers and do not require Next.js.
- Use pnpm only. Install AI Elements through the bundled installer, which runs non-interactive `pnpm dlx shadcn@latest add ... --yes` commands and isolates registry-matched primitives from the template's existing UI contracts.

## Workflow

1. Inspect the generated app and identify its package manager, Hono entry point, React Router structure, and real Customware org/project ids.
2. Read the relevant references listed above.
3. Add `ai`, `@ai-sdk/react`, `@openrouter/ai-sdk-provider`, and `zod` with pnpm only when missing. Complete this dependency install before running the AI Elements installer or any live check.
4. Add a focused server provider helper using `CUSTOMWARE_AI_GATEWAY_KEY` and the fixed gateway URL.
5. Add the Hono endpoint before static-file serving and SPA fallback routes. In this React Router SPA, do not export `HydrateFallback` from a non-root route; use the template’s existing root fallback only.
6. Keep the model and its reasoning configuration server-owned. If the UI offers model selection, validate it against the small allow-list in [references/models.md](references/models.md).
7. For chat, install only the selected AI Elements with `scripts/install-ai-elements.mjs`, then connect `useChat` to the app's Hono endpoint.
8. For structured output, use the current AI SDK `generateText` with `Output.object` and a Zod schema.
9. For tool calling, define the tool on the server with `tool({ inputSchema, execute })`, keep the action boundary server-owned, and use a bounded multi-step setting such as `stopWhen: stepCountIs(5)` when the model must answer after the tool result.
10. For `PromptInputSubmit`, allow the Stop action while status is `submitted` or `streaming`; do not pass an input-empty disabled condition that disables Stop after the submitted input is cleared.
11. Run the mandatory live checks and browser-level UI verification in [references/verification.md](references/verification.md) from the target project, then run the app's normal type/check/build command. If interactive verification fails, inspect the actual page/console from the project-local script before claiming the app is broken.
12. Lazy-load client AI UI with `React.lazy`/dynamic import at the route or pane boundary. Keep server-only AI SDK calls (`streamText`, `generateText`, tools) and the gateway provider server-only; `DefaultChatTransport` is the supported client transport for `useChat`. Do not lazy-load server code into the browser. Treat a large AI UI bundle warning as a real performance issue and isolate heavy Streamdown/AI Elements code from the initial chunk.

## Version-aware API usage

Package APIs can change. When usage is uncertain, inspect the installed packages in the target project's `node_modules/` before coding:

- Read `.d.ts` files for the type contract and available props/returns.
- Read the actual `.js`/`.mjs` implementation for runtime behavior and defaults.
- Apply this to `ai`, `@ai-sdk/react`, `@openrouter/ai-sdk-provider`, and installed AI Elements components. The installed version and source take precedence over copied examples or stale docs.

## Copy-Ready Examples

- Use `assets/ai-chat/` for a minimal streaming chat.
- Use `assets/sql-tool-chat/` for tool-backed chat with visible tool state and a safe read-only SQL pattern.
- Use `assets/generative-ui-chat/` for tool-driven end-user card UI inside chat.
- Use `assets/email-parser/` for internal server-only typed JSON generation.
- Copy only the files needed by the target feature, adapt their import paths, and supply the real org/project ids where the route or service is mounted.
- Treat assets as starting code, not files to execute inside the skill repository.

## Boundaries

- Use `customware-support-widget` instead when the request is only to embed the existing support agent widget.
- Do not build a second browser-to-gateway path alongside the Hono path.
- Do not silently replace an unavailable user-selected model with another model.
- Do not create a second key, per-project key, or direct OpenRouter key in the generated app.
- Do not display, mask, copy, or otherwise surface `CUSTOMWARE_AI_GATEWAY_KEY` in the UI. It is not an AI Elements environment-variable display use case.
