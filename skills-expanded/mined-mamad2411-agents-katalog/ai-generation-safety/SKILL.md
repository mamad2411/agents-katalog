---
name: ai-generation-safety
description: "Review and harden AI generation pipelines, Gemini API integration, fallback paths, and output validation in PANaCEa. Use this skill whenever working on question generation, AI tutoring, Ghost Grader behavioral analysis, OSCE simulation, content enrichment, or any code that calls Gemini — even if the user just says 'the AI is returning bad results' or 'generation is failing'. Also use when adding new AI features, reviewing rate limiting, or auditing clinical accuracy of generated content."
---

# AI Generation Safety in PANaCEa

PANaCEa relies on Google Gemini for question generation, behavioral analysis, tutoring, and clinical simulation. Every AI-generated output is presented to PA students and may influence learning or clinical reasoning. This skill ensures all AI integrations are validated, rate-limited, fallback-safe, and clinically sound.

## Core Principle

**No AI output reaches a student without validation and a safe local fallback.** If Gemini is unavailable, the system must degrade gracefully.

## PANaCEa AI Surface Area

### 1. Question Generation
**Files:**
- `functions/api/questions/generate-batch.ts` — batch generation endpoint
- `functions/api/_shared/question-generator.ts` — Gemini calls for single questions
- `functions/api/_shared/aiQuestionService.ts` — orchestration layer
- `lib/verified-question-generator.ts` — client-side verification

**Models:** `gemini-2.5-flash` (default)

**Outputs:** Questions, vignettes, options, explanations, difficulty levels, distractor rationale

**Risk:** Hallucinated drug interactions, incorrect diagnosis, malformed JSON, distractor validity

---

### 2. Ghost Grader (Behavioral Confidence Analysis)
**Files:**
- `functions/api/_shared/analyzeBehaviorGemini.ts` — main implementation
- `lib/implicit-metrics.ts` — fallback local derivation

**Models:** `gemini-2.0-flash-exp`

**Inputs:** Time-to-first-click, answer switches, hover duration, correctness, dwell time

**Outputs:** Confidence (0–1), implied FSRS rating (1–4)

**Fallback:** `deriveContinuousRating()` — local Bayesian accumulation (low-cost backup)

**Status:** GOOD — has robust fallback; Gemini fail → local metrics (lines 134–150)

---

### 3. Clinical Tutor
**Files:**
- `functions/api/tutor/chat.ts` — deep-think tutoring endpoint
- Uses extended thinking + Google Search grounding

**Models:** `gemini-3-flash-preview` (primary), fallback `gemini-2.5-flash`

**Features:** Thought signatures preserved across turns, Socratic dialogue, PANCE blueprint focus

**Rate limit:** 10 req/min per `ai_endpoints` config

**Risk:** Outdated clinical guidelines, hallucinated citations, missing thought signature propagation

---

### 4. OSCE Live Simulation
**Files:**
- `functions/api/osce/live-engine.ts` — ephemeral token generation
- `functions/api/osce/chat.ts` — ongoing encounter chat
- Client-side WebSocket to Gemini (real-time audio + text)

**Models:** `gemini-2.0-flash-exp`

**Features:** Voice + text, dynamic persona (pain/mood), tools (get_current_vitals, reveal_lab_result)

**Fallback:** None currently (real-time WebSocket; graceful degrade to text-only)

**Risk:** Missed clinical reasoning cues, persona hallucination, tool hallucination

---

### 5. Embedding & Semantic Search
**Files:** `lib/services/` (content enrichment via embeddings)

**Model:** `text-embedding-005`

**Risk:** Dimension mismatch, stale cached vectors, poor retrieval for niche conditions

---

### 6. Rate Limiting & Cost Control
**Files:**
- `functions/api/_shared/rateLimiter.ts` — sliding window limiter
- `RATE_LIMITS.ai_endpoints` — 10 req/min

**Status:** Per-user tracking via auth ID; KV fallback for distributed rate limiting

---

## Validation Checklist

### A. Schema & Type Safety
- [ ] All Gemini responses parsed via `zod` schema (e.g., `geminiBehaviorOutputSchema`)
- [ ] JSON parsing wrapped in try-catch; fallback on parse error
- [ ] `safeParse()` used; never trust raw JSON
- [ ] Response fields bounded: string length limits, array sizes capped

**Red flags:**
- Direct `JSON.parse()` without error handling
- No `zod` validation
- Unbounded arrays or deeply nested objects from Gemini

---

### B. Question Distractor Quality
**File:** `lib/distractorValidation.ts`

Check before persisting to `PreGeneratedQuestion`:
- [ ] Each distractor is plausible for a slightly different patient
- [ ] No "obviously wrong" options (e.g., "Pregnancy" as an answer option for a male patient)
- [ ] Distractor count matches question type (MC: 3 options, typically 1 correct)
- [ ] No duplicate options
- [ ] Rationale for each distractor explains why it's wrong for THIS stem

**Common failure:** Generic drug-interaction distractors that work for many questions (low signal)

---

### C. Clinical Accuracy Signals
- [ ] Drug names match FDA/Micromedex (watch for Gemini hallucination: "amoxicillin-clavulanic acid" vs "amoxicillin-clavulanate")
- [ ] Dosages align with PA formulary or PANCE reference
- [ ] Lab reference ranges use US units
- [ ] Diagnosis criteria match DSM-5, ICD-10, or board standard
- [ ] Procedure complications are real (not made up)

**Critical:** Run spot-checks on 10% of batch questions against known sources (Micromedex, UP TO DATE, PANCE Q-Bank)

---

### D. JSON Safety
- [ ] Response `responseMimeType: 'application/json'` enabled for Ghost Grader and question gen
- [ ] Empty response bodies handled (Gemini sometimes returns `candidates: []`)
- [ ] Malformed JSON captured with context logging

---

## Fallback Design Patterns

### GOOD: Ghost Grader (Resilient)
```typescript
try {
  const result = await analyzeBehaviorGemini(env, params);
  return result;  // { confidence, impliedRating, rawText }
} catch (error) {
  console.warn('[AI_SAFETY] Gemini API failed. Attempting local fallback.');
  const fallbackMetrics = deriveContinuousRating({...});
  return { confidence: fallbackMetrics.confidence, impliedRating: fallbackMetrics.discreteRating };
}
```

**Status:** Two-tier fallback (Gemini → local heuristics). Student always gets a confidence score.

---

### NEEDS WORK: Question Generation (No Fallback)
Current: `generateQuestionsWithGemini()` fails → returns empty array → batch aborts

**Improvement:** Reserve pre-generated pool; if generation fails, draw from backfill questions

---

### NEEDS WORK: OSCE Live (No Fallback)
Current: WebSocket disconnect → encounter paused

**Improvement:** Fall back to text-only chat on Gemini unavailability; continue assessment

---

## Rate Limiting & Cost Audit

### Current Config
```typescript
ai_endpoints: { maxRequests: 10, windowSeconds: 60 }  // 10 req/min per user
```

### Cost Drivers
| Feature | Model | Est. Input Tokens | Output Tokens | Cost/Call | Limits |
|---------|-------|-------------------|---------------|-----------|--------|
| Question Gen | gemini-2.5-flash | 2000–3000 | 500–800 | $0.01–0.02 | 50 q/batch max |
| Ghost Grader | gemini-2.0-flash-exp | 500–800 | 100–200 | ~$0.001 | 10 req/min |
| Tutor (thinking) | gemini-3-flash-preview | 5000–8000 | 1000–2000 | $0.10–0.30 | 10 req/min |
| OSCE Real-time | gemini-2.0-flash-exp | Streaming | Streaming | $0.10–0.50/min | Depends on WebSocket duration |

### Audit Checklist
- [ ] All Gemini calls include rate limit check before request
- [ ] Failed rate-limit hits return 429 with `Retry-After` header
- [ ] Batch size capped at 50 questions (prevent runaway generation)
- [ ] Tutor sessions have max token budget per turn (2048 tokens default)
- [ ] OSCE WebSocket closed after 15 min inactivity
- [ ] Cost tracking logged: `logger.info('Gemini call', { model, inputTokens, outputTokens, cost })`

---

## Common Failure Modes & Fixes

### 1. Gemini 429 (Rate Limit) Cascade
**Problem:** Student retries question generation every 2 seconds → 30 failed calls → cascade

**Fix:**
- Exponential backoff in client (use `retry-after` header)
- Server queues excess generation jobs; returns `{ queued: true, eta: 30s }`
- See: `functions/api/_shared/rateLimiter.ts`

---

### 2. Malformed JSON from Gemini
**Problem:** `generationConfig: { responseMimeType: 'application/json' }` set, but Gemini returns markdown or plain text

**Symptoms:**
- `JSON.parse()` throws
- `zod` validation fails silently
- Fallback code path never exercised

**Fix:**
- Always use `zod.safeParse()`; log parse failures
- Wrap Gemini calls in timeout handler (`fetchWithTimeout`)
- Unit test response parsing with 10 real Gemini responses

---

### 3. Hallucinated Medical Facts
**Problem:** Gemini generates plausible-sounding but incorrect distractor: "Vancomycin dosage: 2000 mg QID" (should be 15–20 mg/kg Q8–12H)

**Fix:**
- Spot-check 10% of batches against Micromedex
- Flagging system: if distractor matches known incorrect drug dosage, escalate to review
- Implement automated check: validate drug names + dosages against trusted API (RxNorm)

---

### 4. Embedding Dimension Mismatch
**Problem:** `text-embedding-005` returns 768-dim vectors; code expects 1536

**Fix:**
- Store embedding model name in metadata
- On retrieval, verify dimension matches; if not, re-embed

---

### 5. Missing Thought Signature (Tutor)
**Problem:** `gemini-3-flash-preview` returns thought signature, but client doesn't pass it back in next turn → model loses reasoning

**Fix:**
- Schema requires `thoughtSignature?: string` on history turns
- Client extracts from previous model response: `data.candidates?.[0]?.content?.parts?.find(p => p.thoughtSignature)`
- Always include in next request: `previousThoughtSignatures: [sig]` or `parts: [{ thoughtSignature: sig }]`

---

### 6. Distractor Validation Failures
**Problem:** `validateDistractors()` rejects a batch; batch is discarded; student sees no new questions

**Fix:**
- Log rejection reason with full question + options for review
- Implement retry with adjusted prompt (e.g., "avoid drug-interaction distractors; use comorbidity-based distractors")
- Partial batch success: return valid questions, queue invalid ones for re-generation

---

## Model Routing & Selection

### When to Use Each Model
| Feature | Model | Why | Fallback |
|---------|-------|-----|----------|
| Question Gen | gemini-2.5-flash | Fast, cheap, good for structured output | gemini-2.0-flash-exp |
| Ghost Grader | gemini-2.0-flash-exp | Reliable JSON, low latency | local `deriveContinuousRating()` |
| Tutor (Deep Think) | gemini-3-flash-preview | Extended thinking for reasoning | gemini-2.5-flash (no thinking) |
| OSCE Real-time | gemini-2.0-flash-exp | Low latency for streaming voice | Text-only fallback |
| Embeddings | text-embedding-005 | 768 dims, clinical domain tuned | — |

### Model Availability Handling
```typescript
async function callGeminiWithFallback(
  primary: string,
  fallback: string,
  prompt: string
): Promise<string> {
  try {
    return await callGemini(primary, prompt);
  } catch (e) {
    if (e.status === 404 || e.message.includes('not found')) {
      console.warn(`Primary model ${primary} unavailable. Trying fallback ${fallback}.`);
      return await callGemini(fallback, prompt);
    }
    throw e;
  }
}
```

---

## Files to Inspect First

**When user reports AI issue:**
1. `functions/api/_shared/analyzeBehaviorGemini.ts` (Ghost Grader; easiest to test locally)
2. `functions/api/_shared/question-generator.ts` (prompt engineering + schema)
3. `functions/api/_shared/rateLimiter.ts` (check rate limit config)
4. `lib/distractorValidation.ts` (distractor rules)
5. `functions/api/tutor/chat.ts` (if tutor issue; check thought signature handling)
6. `functions/api/osce/live-engine.ts` (if OSCE issue; check tool definitions)

**To add fallback:**
- Edit API endpoint to call fallback function in `catch()` block
- Update types to allow `fallback: true` flag in response
- Test offline scenario in Vitest

---

## Composes With

- **clinical-safety-review** — audit generated clinical content (distractor rationale, explanations) for tone, accuracy, and patient safety tone
- **clinical-content-gen** — enrichment via embeddings; ensure embedding model and dimension match
- **cf-edge-api** — ensure Gemini calls use `context.env.GEMINI_API_KEY`, not raw `process.env`
- **panacea-verify** — after changes, run `npm test` to ensure schema parsing and fallback paths are covered
