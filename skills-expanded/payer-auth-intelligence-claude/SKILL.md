@AGENTS.md

# payer-auth-intelligence — Project Bible

Payer-side agentic prior authorization decisioning POC. An in-process
LangGraph.js StateGraph receives a PA submission, evaluates it across four agent
nodes, and routes to auto-approve / auto-deny / pending-info / human-review.
All data is synthetic. No PHI, ever.

See `payer-auth-intelligence-prd.md` for the full specification and
`DECISIONS.md` for the architectural decision log.

## Build rules for Claude Code sessions

1. Read `DECISIONS.md` before any build session; append new decisions at the end.
2. Never modify adapter interfaces in `types/adapters.types.ts` / `adapters/`
   once defined — they are immutable enterprise integration contracts (D-005).
3. Never use real PHI, real plan identifiers, or real NPI numbers in mock data.
4. Never hardcode the LLM provider — always route through `lib/llm-client.ts`.
5. Never auto-deny based on cost, plan type, or provider identity — clinical and
   coverage criteria only (D-006).
6. Document every non-obvious design choice inline with a `// DECISION:` comment.
7. Run a type check (`bun run typecheck`) and confirm zero TypeScript errors
   before ending any session.
8. Update `DECISIONS.md` at the end of each session: built, decided, deferred, why.
9. Agent node files in `agents/` must NOT import `@langchain/langgraph` directly.
   Import state types from `graph/state.ts` and call the LLM via `lib/llm-client.ts`.
10. `graph/graph.ts` is the single source of truth for graph topology — no graph
    construction logic anywhere else.

## Local commands

This environment lacks native SWC bindings, so Turbopack is unavailable here.
Use the webpack flag locally:

```bash
NEXT_PUBLIC_APP_ENV=mock next dev --webpack    # dashboard
bun scripts/smoke-graph.ts                     # run all 8 scenarios through the graph
bun run typecheck                              # tsc --noEmit (authoritative type gate)
```

On platforms with native bindings, `bun run dev` (Turbopack) works as normal.

## Architecture at a glance

- `graph/` — state, edges, topology (`graph.ts`), Studio export (`graph.standalone.ts`)
- `agents/` — five node implementations (intake, benefit_check, med_necessity, routing, human_review)
- `lib/llm-client.ts` — Anthropic ↔ Bedrock switch via `LLM_PROVIDER`
- `lib/mock/` — 8 synthetic submissions, reference data, mock node functions
- `adapters/` — four immutable integration contracts with mock implementations
- `lib/pipeline.ts` — runs/resumes the graph; `lib/decision-store.ts` holds cases
- `app/api/decisions/` — POST run, GET list/by-id, POST resume
- `components/dashboard/` — the payer decisioning console UI
- `infrastructure/` — AWS CDK stack (Track 3)
