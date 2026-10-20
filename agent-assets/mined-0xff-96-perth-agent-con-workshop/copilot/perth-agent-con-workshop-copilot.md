# Copilot review instructions

This is a CopilotKit v2 + A2UI workshop app (Node/TypeScript, React 18, Vite).
When reviewing a pull request, prioritise this stack's known pitfalls:

- **Default every array/object prop** in `useComponent`/A2UI-rendered components —
  streaming delivers partial props, and `undefined.map` white-screens the page.
- **CopilotKit v2 imports** must come from the `/v2` subpaths
  (`@copilotkit/runtime/v2`, `@copilotkit/react-core/v2`) — not a 2.x major.
- **Model format is slash** (`openai/gpt-4.1`, `anthropic/claude-sonnet-4-6`),
  never a colon.
- **`server.ts` must `import "dotenv/config"` first**, or the API key won't load.
- **`<CopilotKit>` needs `useSingleEndpoint={false}` and `runtimeUrl="/api/copilotkit"`**;
  select the agent with `agentId` (e.g. `agentId="l3"`).
- **L4 surfaces are host-authored** via tools returning `{ a2ui_operations: [...] }`
  with inlined literal values — root-level `{path}` bindings don't resolve for
  `Metric.value`.
- **New L3 components** need a colocated `<name>.test.tsx` and registration via
  `useComponent({ name, description, parameters, render })`.

Also flag the usual correctness issues. Never approve a change that commits an API
key or a `.env` file — keys live in local `.env` only.

The quality gate is `npm run typecheck`, `npx vitest run`, and `npm run build`
(the `/verify` command).
