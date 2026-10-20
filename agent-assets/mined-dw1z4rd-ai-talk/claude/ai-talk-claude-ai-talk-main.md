# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev        # Start SvelteKit dev server (Vite, HMR)
npm run build      # Production build
npm run preview    # Serve production build locally
npm test           # Run Vitest (single run)
npm run test:watch # Vitest in watch mode
```

To run a single test file:
```bash
npx vitest run src/lib/live-judge/pairwise.test.ts
```

## Environment Setup

Copy `.env.example` to `.env`. Key variables:
- `ANTHROPIC_API_KEY` — Claude API
- `GEMINI_API_KEY` — Gemini API
- `OLLAMA_CLOUD_URL` / `OLLAMA_CLOUD_API_KEY` — Remote Ollama
- `USELOCAL` — Toggle local vs. cloud Ollama routing
- `DEBATE_STORE=file` — Durable persistence to `data/debates/*.json`; omit for in-memory

## Architecture Overview

AI-Talk is a **structured epistemic auditor**: a multi-agent debate engine where an LLM judge evaluates reasoning quality using adversarial dialogue. It is *not* a simple chatbot; the judge layer enforces causal argument tracking across turns and produces mechanistic verdicts.

### Tech Stack
- **SvelteKit 2 + Svelte 5** (full-stack, Node adapter — not statically prerenderable due to SSE streaming)
- **Tailwind CSS 4**, TypeScript 5.9, Vite 8
- **LLM Providers**: Ollama Cloud (default, 18+ models), Anthropic, OpenAI-compatible, Gemini
- **Persistence**: `DebateStore` interface with `FileDebateStore` and `MemoryDebateStore` implementations
- **Testing**: Vitest

### Key Source Paths

| Path | Role |
|------|------|
| `src/lib/agents.ts` (52KB) | Agent builder, `MODEL_CATALOG`, personality archetypes, `buildAdaptiveAgents()` |
| `src/lib/live-judge/core.ts` | `LiveJudgeSystem` class, `processTurn()`, session coordination |
| `src/lib/live-judge/analysis.ts` | `analyzeTurn()`, `compareTurns()`, `generateNarrativeVerdict()` |
| `src/lib/live-judge/types.ts` | All scoring and personality types (`JudgeScores`, `PairwiseRound`, `NarrativeVerdict`, etc.) |
| `src/lib/adaptive/types.ts` | Adaptive personality types (`AdaptiveAgentState`, `PersonalityParameters`, `MetaGoal`) |
| `src/lib/llm-agent/` | Provider abstraction (`LLMProvider` interface, Ollama/Anthropic/OpenAI/Gemini impls) |
| `src/lib/server/live-judge-service.ts` | Session lifecycle: `createSession()`, `resumeSession()`, `checkpointSession()`, `finalizeSession()` |
| `src/lib/server/debate-store.ts` | `DebateStore` interface + both implementations |
| `src/routes/api/chat/+server.ts` | Main SSE streaming endpoint — the debate turn loop |
| `src/routes/+page.svelte` (38KB) | Main UI: debate setup, SSE event handling, judge panel, history |

### Data Flow

1. Client POSTs debate params to `/api/chat`
2. Server streams SSE events: `debateId` → `turn_start` → `token` (per LLM token) → `message` → `judgeResult` → `scoreUpdate` → `narrativeVerdict` → `done`
3. Inside the turn loop, judge analysis (`analyzeTurn` + `compareTurns`) runs asynchronously — the promise for turn N-1's judge fires while turn N is generating, so judge and generation are pipelined
4. After each round, `checkpointSession()` fires as a background save (no await)
5. At completion, `finalizeSession()` writes the verdict and marks the record completed

### Scoring System

Scores have two layers:
- **Absolute** (`analyzeTurn`): Per-turn rubric on 5 dimensions — Logic (0–40), Rhetorical Force (0–30), Frame Control, Credibility, Tactical Effectiveness — plus an Overall (0–100)
- **Pairwise** (`compareTurns`): Sliding-window head-to-head comparison of consecutive turns; the winner/loser determines floor/ceiling clamping on absolute scores

**Retroactive adjustments**: Hollow claims flagged in round N apply a -4 penalty back to the originating turn's score. This is stored in `scoreAdjustmentsLog` on `LiveJudgePanel`.

### Adaptive Personality System

Each agent has a `ContinuousPersonality` (12 traits, 1–10 scale). After each judge round:
1. The judge emits `AdaptivePressure` signals (cognitive, emotional, strategic, credibility dimensions)
2. Traits shift based on elasticity and incoming pressure
3. A `hiddenDirective` is injected silently into the agent's system prompt for the next turn
4. The system prompt is regenerated from the updated personality parameters

Personality archetypes (`PERSONALITY_ARCHETYPES` in `agents.ts`): `engineer`, `philosopher`, `strategist`, `provocateur`.

### Persistence / Session Lifecycle

`DebateRecord` (serialized to JSON) includes: full transcript, serialized agent state (including adaptive personality), full `LiveJudgePanel` scoring history, and `NarrativeVerdict`. `hydrateAgent()` in `live-judge-service.ts` reconstructs live agents from a serialized record, restoring provider instances and personality state.

`DEBATE_STORE=file` writes to `data/debates/{uuid}.json`. Without it, `MemoryDebateStore` is used (dev default — state lost on restart).

### LLM Provider Routing

Model IDs in `MODEL_CATALOG` (agents.ts, lines ~119–191) map to provider factory functions. Models ending in `:cloud` or `-cloud` route to Ollama Cloud; `USELOCAL=true` overrides to local Ollama. The `withRetry` wrapper in `llm-agent/` provides exponential backoff.

### Test Files

Tests live alongside source in `src/lib/`:
- `live-judge/pairwise.test.ts`, `pressure.test.ts`, `doc-audit-mode.test.ts`
- `server/live-judge-service.test.ts`, `debate-store.test.ts`, `api-auth.test.ts`, `metering.test.ts`
