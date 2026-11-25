---
name: memwal-serverless
description: >-
  MemWal on Vercel/Next.js serverless — multi-tenant namespaces, fire-and-forget
  remember(), parallel recall budgets, chat hot-path rules. Use when integrating
  MemWal with streaming LLM on serverless, FUNCTION_INVOCATION_TIMEOUT, remember
  vs rememberAndWait, or Walrus Memory production deploy.
---

# MemWal Serverless — Agent Skill

Production patterns from **Mr. Toxic Special One** on Vercel (`hkg1`) + MemWal
mainnet. **Judges / deep evidence:** [FINAL_FEEDBACK.md](../../../FINAL_FEEDBACK.md).

Related repo skills: [memwal-multi-tenant-setup](../memwal-multi-tenant-setup/SKILL.md),
[sui-wallet-stateless-auth](../sui-wallet-stateless-auth/SKILL.md),
[prediction-roast-agent](../prediction-roast-agent/SKILL.md).

MemWal issue filed from this work: [#277](https://github.com/MystenLabs/MemWal/issues/277) (Open).

---

## When to use

- Next.js `/api/chat` (or similar) streams LLM + reads/writes MemWal.
- Message 3 hits `FUNCTION_INVOCATION_TIMEOUT` on Vercel.
- Choosing `remember()` vs `rememberAndWait()` on the hot path.
- Tuning TTFT with profile load + semantic recall.

---

## Serverless wall-clock budget

| Plan | Typical cap | Implication |
|------|-------------|-------------|
| Vercel Hobby | ~10s | Short stream + minimal blocking |
| Vercel Pro + `maxDuration: 60` | up to 60s | Room for parallel recall |

Set in `vercel.json`:

```json
{ "functions": { "app/api/chat/route.ts": { "maxDuration": 60 } } }
```

Also export `export const maxDuration = 60` in the route file.

---

## Hot path invariants (never break)

1. **Never `rememberAndWait()` before `streamText()`** — use `remember()` fire-and-forget.
2. **Parallel read** — `Promise.all([loadProfileFast, recallMemories])`, separate timeouts.
3. **Cap prompt** — compact profile JSON + max 2 memories × 80 chars.
4. **Cap stream** — low `maxOutputTokens` (e.g. 70), short system persona.
5. **Cap history** — last N turns, truncate message text to model.
6. **`onFinish`** — update cache + `void remember(...)`; do not await before response ends.
7. **No heavy sync on chat** — fixture resolution → separate route/button (`/api/matches/sync`).
8. **Regex intent only** on hot path — no extra LLM call before stream.

---

## Reference chat turn (this repo)

```typescript
export const maxDuration = 60;

// 1. Auth (stateless — see sui-wallet-stateless-auth skill)
const auth = await assertWalletAuth(walletAddress, authMessage, authSignature);
if (!auth.ok) return NextResponse.json({ error: auth.error }, { status: 401 });

// 2. Parallel MemWal reads — separate budgets
const [baseProfile, recalledMemories] = await Promise.all([
  loadFanProfileFast(walletAddress, 500),
  recallMemories(walletAddress, lastUserText, { limit: 2, timeoutMs: 800 }),
]);

// 3. Sync in-memory mutation (no MemWal await)
const profile = applyIntentToProfile(walletAddress, baseProfile, intent);
if (intentMutatesProfile(intent)) persistProfileEnqueue(walletAddress, profile);

// 4. Stream
const result = streamText({
  model,
  system: buildSystemPrompt({ fanProfile: profile, recalledMemories, toxicityLevel }),
  messages: cappedHistory,
  maxOutputTokens: 70,
  onFinish: ({ text }) => {
    setProfileCache(walletAddress, appendRoastToProfile(profile, text, topics));
    rememberSemanticLine(walletAddress, `Roast delivered: ${text.slice(0, 200)}`);
  },
});

return result.toUIMessageStreamResponse();
```

Implementation: `app/api/chat/route.ts`, `lib/memory/fan-profile.ts`.

---

## Write patterns

| Operation | Hot path | Cold path / admin |
|-----------|----------|-------------------|
| Semantic line | `rememberForWallet()` | — |
| Profile snapshot | `persistProfileEnqueue()` (async) | `persistProfileAndWait()` OK |
| User must see write before continue | Never on stream path | Dedicated commit API |

---

## Latency stack we fixed (anti-patterns)

| Anti-pattern | Symptom |
|--------------|---------|
| `rememberAndWait()` pre-stream | +1–3s TTFT; message 3 timeout |
| Sequential profile then recall | Latencies sum |
| `syncPendingPredictions()` every turn | Unbounded blocking |
| Extra LLM intent call | Full round-trip per message |
| Fat prompt + long stream | Lambda runs until stream ends |

Full post-mortem: [FINAL_FEEDBACK.md](../../../FINAL_FEEDBACK.md).

---

## Recall optimization

Semantic recall is required for **Memory Moment** demos but must stay bounded.
See [recall-optimization.md](./recall-optimization.md) — implementation in
`lib/memory/recall.ts`.

Quick rules:

- Direct `recall()` first; avoid `restore()` on hot path (429 risk).
- Skip `restore()` for ~45s after commit (`commit-session.ts`).
- In-memory cache per wallet+query (TTL ~3 min).
- Exponential backoff on 429; return `[]` on timeout — stream anyway.
- Legacy namespace fallback only when primary returns zero hits.

---

## Trade-offs (honest)

| Choice | Cost | Benefit |
|--------|------|---------|
| Fire-and-forget write | Persistence lags seconds | Demo survives timeout |
| Recall cap 800ms | +0.5–1s TTFT | Strong callback roasts |
| Short output | Less prose depth | Fits serverless budget |

---

## Repo map

| File | Role |
|------|------|
| `app/api/chat/route.ts` | Streaming hot path |
| `lib/memory/fan-profile.ts` | Profile cache, fast load, enqueue |
| `lib/memory/recall.ts` | Optimized recall |
| `lib/memory/wallet-memory.ts` | remember/recall wrappers |
| `FINAL_FEEDBACK.md` | Judge-facing latency write-up |
| `CHANGELOG.md` | Mitigation history |
