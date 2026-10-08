# Cabinet Project Rules (apply to whole repo)

Scope: **entire repository**

## Security

- NEVER put OPENAI_API_KEY or SUPABASE_SERVICE_ROLE_KEY in client-side code.
- LLM calls must be server-side only (Netlify Functions).
- Every write/read must be scoped by user_id and protected by Supabase RLS.
- Netlify functions must verify Supabase JWT on every request.

## Coding style

- TypeScript everywhere.
- Small modules. No heavy agent frameworks for MVP.
- Prefer readable code over clever abstractions.
- Ensure loading/error UI states.

## Agent orchestration

- Parallel minister calls; Prime Minister runs last.
- Each minister response must include: Recommendation, Tradeoffs, Risks, Hard Question, Vote.
- Persist model metadata (model name, latency, token usage if available).

## Implementation process

Before writing code:

1. Summarize current repo state.
2. Propose minimal plan.
3. Implement in small steps.

If anything is unclear, make a best effort assumption and proceed.
