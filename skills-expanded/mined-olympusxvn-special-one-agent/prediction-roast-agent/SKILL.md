---
name: prediction-roast-agent
description: >-
  Prediction Roast agent pattern — dual MemWal memory (structured profile +
  semantic lines), regex intent, toxicity meter, compact roast prompts. Use for
  accountability agents, sports banter bots, Memory Moment demos, or Walrus
  Sessions Prediction Roast track.
---

# Prediction Roast Agent

Memory **is** the product: roasts reference the user's own predictions, flip-flops,
and wrong calls — not generic trash talk.

**Judge walkthrough:** [SUBMISSION.md](../../../SUBMISSION.md) ·
**Technical latency / recall:** [FINAL_FEEDBACK.md](../../../FINAL_FEEDBACK.md)

Related: [memwal-serverless](../memwal-serverless/SKILL.md),
[memwal-multi-tenant-setup](../memwal-multi-tenant-setup/SKILL.md).

---

## Dual memory model

| Layer | Storage | Read | Write |
|-------|---------|------|-------|
| **Structured** | `FAN_PROFILE_JSON:{...}` | Profile load / parse from recall | `persistProfileEnqueue` |
| **Semantic** | Plain lines | `recall(query)` | `rememberForWallet` fire-and-forget |

Semantic line examples:

```text
Favorite team: Brazil. User supports Brazil for World Cup 2026.
Prediction: Brazil 3-0 Argentina — PENDING
Prediction WRONG: said 3-0, actual 1-2
Flip-flop: switched from Argentina to Brazil
Roast delivered: …
```

Types: `lib/memory/types.ts` (`FanMemory`, `Prediction`).

---

## Intent detection (regex — hot path)

`detectIntent(text)` → `ParsedIntent`:

| Intent | Triggers |
|--------|----------|
| `set_team` | "I support Brazil", "my team is France" |
| `prediction` | "I predict 3-0", "Brazil will beat Argentina" |
| `report_result` | "Argentina won 1-0", score reports |
| `banter` | default |

Implementation: `lib/ai/intent.ts` — **no LLM call** before stream.

Apply synchronously: `applyIntentToProfile(wallet, profile, intent)`.

---

## Toxicity meter (1–10)

```typescript
// lib/memory/toxicity.ts
raw = 1 + wrongCount*1.5 + flip_flop_count*2 + (highConfidenceWrong ? 2 : 0);
level = clamp(round(raw), 1, 10);
```

Inject into system prompt as `tox:{level}` — hotter roasts as receipts pile up.

---

## System prompt shape

```typescript
// lib/ai/build-prompt.ts
parts = [
  MR_TOXIC_FAST_PROMPT,           // persona — keep short for serverless
  `tox:${toxicityLevel}`,
  `fan:${JSON.stringify(compactFanProfile(profile))}`,
  "## WALRUS_MEMORY …",           // max 2 lines × 80 chars
];
```

Compact profile: `{ team, flips, confidence, last }` — not full JSON dump.

Persona file: `lib/ai/system-prompt.ts` (`MR_TOXIC_FAST_PROMPT`).

---

## Prediction lifecycle

```text
PENDING → user reports result OR /api/matches/sync resolves fixture
       → CORRECT | WRONG
       → semantic line + toxicity update + roast callback
```

Sync **off** chat hot path — user triggers **Check my predictions** or separate API.

---

## Judge-visible UI

| Surface | Shows |
|---------|-------|
| **Walrus Memory Ledger** | Open + resolved predictions, team, toxicity |
| Chat stream | Recalled memory callbacks |
| MemWal LIVE + explorer | On-chain proof |

Components: `PredictionCard`, `ToxicityMeter`, `MemWalStatus`.

Refresh ledger: `POST /api/memory/profile` after each chat turn.

---

## Memory Moment demo script

**Day 1:** declare team + prediction → ledger updates → roast.  
**Day 4+ (same wallet):** ask "how are my predictions?" → agent references
prior Brazil support / WRONG calls without re-stating context.

Full script: [SUBMISSION.md](../../../SUBMISSION.md) § Memory Moment.

---

## Serverless constraints

Follow [memwal-serverless](../memwal-serverless/SKILL.md):

- Parallel profile + recall caps
- Fire-and-forget writes
- Short stream output

Without recall, Memory Moment is weaker — re-enable with caps per
[recall-optimization.md](../memwal-serverless/recall-optimization.md).

---

## Repo map

| Path | Role |
|------|------|
| `lib/memory/fan-profile.ts` | Profile CRUD + cache |
| `lib/memory/apply-intent.ts` | Intent → profile mutation |
| `lib/memory/toxicity.ts` | Meter |
| `lib/ai/intent.ts` | Regex parser |
| `lib/ai/build-prompt.ts` | System prompt assembly |
| `components/chat/PredictionCard.tsx` | Judge ledger UI |
| `app/api/matches/sync/route.ts` | Fixture resolution |
