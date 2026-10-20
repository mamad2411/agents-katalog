---
name: pericles-mastra-tool
version: 2026.05.1
description: >
  How to author a Mastra createTool the Pericles way — the substrate every Skill
  formalizes. Use this WHENEVER you write or modify a tool in
  backend/src/mastra/tools: it covers the id/description, Zod input & output
  schemas, the execute({ context }) signature, the REQUIRED organization_id input
  field validated inside execute, the AbortSignal.timeout(10000) convention, and
  scorer wiring. A correctly built tool is a proto-Skill manifest, so doing this
  right makes the later registry lift trivial.
doctrine_refs: [§1, §2; Manifest §0]
depends_on: [pericles-tech-stack, pericles-tenant-isolation]
last_reconciled: 2026-05-28
---

# Pericles Mastra Tool (build skill)

A Mastra `createTool` already declares an id, description, Zod input/output schemas,
and an execute function. **That is structurally a proto-Skill manifest.** Build
every tool as if it will be lifted into the registry — because it will
(`pericles-skill-authoring`).

> **Authoritative existing rule:** `.claude/rules/04-tools.md` is the canonical
> tool standard in the repo (it is path-scoped to `backend/src/mastra/tools/**`).
> This skill complements it; if they ever diverge, that rule and `CLAUDE.md` win.

## When to use this skill

Writing a new tool, modifying one of the 13 existing monitoring tools, or reviewing
anything under `backend/src/mastra/tools/`.

## The required shape (as the codebase actually does it)

The real pattern, verified against `weather-disaster-monitor-tool.ts` and the 12
others:

```ts
import { createTool } from '@mastra/core/tools';   // NOTE: /tools subpath
import { z } from 'zod';
import { limitEvents, getFilterSummary } from './output-limiter.js'; // shared helper
import { toolLoggers } from './tool-logger.js';                      // per-tool logger

const logger = toolLoggers.<domain>;

export const <domain>MonitorTool = createTool({
  id: '<domain>-monitor',
  description: 'One precise sentence other Skills and the registry read.',
  inputSchema: z.object({
    organization_id: z.string().uuid().describe('Required for tenant isolation'),
    // ...domain inputs (locations, severity_threshold, lookback_hours, ...)
  }),
  outputSchema: z.object({ success: z.boolean(), events: z.array(/* ... */) }),
  execute: async ({ context }) => {
    const { organization_id, /* ...inputs */ } = context;     // inputs arrive on context
    if (!organization_id) throw new Error('organization_id is required'); // fail closed
    // external calls: signal: AbortSignal.timeout(10000)
    // scope every prisma query by organization_id
    return { success: true, events: /* ... */ };
  },
});
```

The non-negotiables:

1. **`organization_id` is a REQUIRED field in `inputSchema`** (`z.string().uuid()`),
   and is destructured from `context` and validated inside `execute`. This matches
   `.claude/rules/04-tools.md` and every existing tool. (Anti-forgery — ensuring the
   caller can only pass *their own* authenticated org — is enforced at the
   invocation/auth layer, not by omitting the field; see `pericles-tenant-isolation`.)
2. **Import from `@mastra/core/tools`** (the `/tools` subpath), and `z` from `zod`.
3. **`execute: async ({ context }) => …`** — inputs validated against `inputSchema`
   arrive on `context`. There is no separate `input` argument.
4. **Both Zod schemas present.** The output schema is also a security control: an
   injected "execute this" payload fails schema validation before any downstream
   Skill sees it (`pericles-prompts`).
5. **`AbortSignal.timeout(10000)` on every external fetch**, with the standard
   `User-Agent: Pericles-SupplyChainMonitor/1.0 (contact@pericles.cloud)` header.
6. **Reuse the shared helpers**: `output-limiter.ts` (`limitEvents`,
   `getFilterSummary`) to cap output size, and `tool-logger.ts` (`toolLoggers`) for
   structured per-tool logging.
7. **Scorer wiring** via `pericles-evals-scorers`; a tool bound for a `published`
   Skill needs an `eval_criteria` reference.

## What NOT to do

- Do not accept an `organization_id` that differs from the caller's authenticated
  org — the auth/invocation layer must bind it (`pericles-tenant-isolation`).
- Do not add a NEW external data source by inlining it — route new sources through
  MCP (`pericles-mcp-layer`). The 13 existing inlined integrations are grandfathered.
- Do not skip the output schema or emit free-form text where a typed structure works.
- Do not commit a consequential action from `execute()`; that belongs in an
  Execution Node (`pericles-execution-node`).

## Mapping a tool to a future Skill

`createTool` gives id/description/schemas/execute and the `organization_id`
convention; the manifest adds the categorized Skill ID + calendar version, schema
refs with back-compat checking, explicit `knowledge_sources`/`dependencies`,
registry-enforced tenant scoping, and required `eval_criteria`. Author the tool well
now and the lift (`pericles-skill-authoring`) is a metadata exercise.

## Verification

`organization_id` is a required uuid input, destructured from `context`, validated
first; import is `@mastra/core/tools`; output schema present and strict; external
calls use the 10s timeout; shared limiter/logger used; scorers wired. Add a test
asserting a missing/invalid `organization_id` throws.

## Existing standards (read alongside)

`CLAUDE.md` (Tool Pattern section); `.claude/rules/04-tools.md`,
`.claude/rules/06-mastra.md`; `.cursor/rules/700-ai/701-mastra-agent-core-standards-auto.mdc`.

## Open questions

- Whether net-new tools should still inline integrations or go straight to MCP given
  `.mcp.json` is currently empty — default to MCP per Doctrine §5; confirm with the
  platform team.

## Changelog

- 2026.05.1 — Reconciled against the live repo: organization_id is an inputSchema
  field destructured from context; `@mastra/core/tools` import; execute({ context });
  documented shared output-limiter/tool-logger helpers; referenced .claude/rules/04-tools.md.
- 2026.05.0 — Initial draft.
