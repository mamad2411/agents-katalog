---
name: generation-pipeline
description: |
  Orchestrates the full multi-pass generation sequence for a skill-based writing
  tool: sources → compiled prompt → outline → draft → quality check. Wires
  skill-template-engine and source-grounding together with streaming output to
  Claude. Handles token budget enforcement, streaming SSE output, quality assertion,
  and graceful failure at every stage.
  Use when: a user Brief has been submitted, compilation and source-fetching must
  run, and a complete generated document is the expected output.
  Trigger on: "generate document", "run generation pipeline", "start generation",
  "generate with skill", or any request that takes a validated Brief and must
  produce a streamed, quality-checked document.
author: Robin Westerlund
version: 1.0.0
---

# Generation Pipeline

> Orchestrates the full multi-pass generation sequence — sources, compiled prompt, outline, draft, quality check — and streams the result to the user.

## Purpose

Having a compiled prompt and verified sources is not enough — they must be executed in the right order, with streaming, within a token budget, with quality checked before the document is saved. Without an orchestration layer, every integration point (source timing, streaming setup, quality assertion, error recovery) gets re-implemented per skill, per feature. The generation pipeline is the single path that all skill-based generation takes, regardless of skill.

## Audience

- Primary: AI agents and backend engineers implementing the generation API route (`/api/generate`)
- Secondary: Developers integrating new SkillTemplates who need to understand how their template will be executed

## When to Use

- A user has submitted a validated Brief and generation must begin
- A failed generation needs to be retried (the pipeline handles retries with state preservation)
- The generation API route needs implementation or modification
- Streaming output to a frontend SSE endpoint is required

## When Not to Use

| If the situation is... | Use instead | Why |
|------------------------|-------------|-----|
| You only need to compile a prompt, not generate | `skill-template-engine` | Pipeline is overkill; just run Steps 1–2 |
| You only need sources without generating | `source-grounding` | Pipeline is overkill; just run `source-grounding` directly |
| You need to validate a Brief schema without generating | `skill-template-engine` Step 2 only | Full pipeline adds unnecessary latency |

## Required Context

Gather or confirm:

- A validated `Brief` object (Brief validation already passed — the pipeline does not re-validate)
- The target `skillSlug` identifying which SkillTemplate to load
- `ANTHROPIC_API_KEY`, `SEARCH_API_KEY`, and `SEARCH_PROVIDER` in environment
- An active SSE response stream open to the client (the pipeline writes to it in real time)
- The user's `document_id` for saving the final output to the database

## Process

### Step 1: Fan-Out — Compile Prompt and Fetch Sources in Parallel

**Action:** Start `skill-template-engine` and `source-grounding` concurrently — do not wait for one before starting the other.
**Inputs:** Validated `Brief`, `skillSlug`
**Outputs:** `[CompiledPrompt, SourceContext]` (both resolved before Step 2)

Use `Promise.all` to run compilation and source-fetching simultaneously. This parallelism eliminates 3–8s of latency from the critical path.

```typescript
const [compiled, sources] = await Promise.all([
  skillTemplateEngine.compile(skillSlug, brief),
  sourceGrounding.fetch(brief.topic, brief.angle)
]);
```

After both resolve: if `compiled` is a `ValidationError`, abort and return the error to the client. If `sources.fallback === true`, inject the no-sources notice and continue — do not abort generation over missing sources.

**Do NOT:** Await source-grounding before starting compilation, or await compilation before starting source-grounding. Sequential execution adds unnecessary latency.

### Step 2: Inject Sources and Build the Final Prompt

**Action:** Pass the `SourceContext` into the `CompiledPrompt` via the template engine's source injection.
**Inputs:** `CompiledPrompt` from Step 1, `SourceContext` from Step 1
**Outputs:** Final `CompiledPrompt` with source layer populated

Call `skillTemplateEngine.injectSources(compiled, sources)`. This is a fast in-memory operation — it substitutes the `{{sources}}` placeholder in the compiled user prompt with the formatted `SourceContext`. Returns an updated `CompiledPrompt`.

**Do NOT:** Manually concatenate source excerpts into the prompt string. Use the template engine's injection method — it handles formatting, escaping, and the no-sources fallback consistently.

### Step 3: Generate the Outline

**Action:** Call Claude with the compiled prompt to produce a structured outline.
**Inputs:** Final `CompiledPrompt`, `ANTHROPIC_API_KEY`
**Outputs:** Outline text (non-streaming — stored in memory, not sent to client yet)

Call Claude (non-streaming) with:
- `system`: `compiled.system`
- `user`: `compiled.user` + `"\n\nProduce a structured outline only. Do not write the full draft yet."`
- `max_tokens`: 500 (outline is short; enforce the budget)
- `model`: `claude-sonnet-4-6`

Store the outline. Do not stream it to the client — outlines are internal scaffolding. Emit a progress event to the SSE stream: `{ event: "outline_complete", status: "generating_draft" }`.

| If... | Then... | Because... |
|-------|---------|------------|
| Claude returns an outline | Continue to Step 4 | Nominal path |
| API returns 4xx/5xx | Emit `{ event: "error", stage: "outline", retryable: true }`, abort | Non-recoverable at this stage without retry |
| Outline token count > 500 | Truncate to 500 tokens | Budget enforcement; outline does not need to be long |

**Do NOT:** Skip the outline pass and go directly to drafting. The outline grounds the draft and dramatically reduces structural variance across regenerations.

### Step 4: Generate the Draft (Streaming)

**Action:** Call Claude with the compiled prompt + outline to produce the full draft, streaming output to the client.
**Inputs:** Final `CompiledPrompt`, outline from Step 3, open SSE stream
**Outputs:** Streamed draft text sent to client; final draft text stored in memory

Call Claude (streaming) with:
- `system`: `compiled.system`
- `user`: `compiled.user` + `"\n\n[OUTLINE]\n" + outline + "\n[/OUTLINE]\n\nWrite the full draft now. Follow the outline structure exactly."`
- `max_tokens`: 3000 (long-form ceiling; adjust down for `length_tier: "short"`)
- `stream: true`

For each streaming chunk: emit `{ event: "chunk", content: chunkText }` to the SSE stream. Accumulate chunks in memory to build the full draft string.

On stream completion: emit `{ event: "draft_complete" }`. Store the full draft for Step 5.

**Do NOT:** Stream the outline to the client or re-stream the sources. The user expects to see the document appearing word by word — only draft content should stream.

### Step 5: Run Quality Assertion

**Action:** Check the completed draft against the skill's `quality_markers`.
**Inputs:** Full draft text from Step 4, `compiled.qualityMarkers`
**Outputs:** `QualityResult` — `passed: boolean`, `issues: string[]`

Run the following checks (from `quality_markers`):

| Check | How | On failure |
|-------|-----|-----------|
| Word count in range | `wordCount >= min_words && wordCount <= max_words` | Add issue: "Word count X outside range [min–max]" |
| Required sections present | Scan draft for each section heading in `required_sections` | Add issue: "Missing section: [name]" |
| Citation present (if required) | Check for at least one URL or inline citation pattern | Add issue: "No citations found — required" |
| Custom checks | Evaluate each string in `custom_checks` as a natural-language rule | Flag if likely violated |

Emit `{ event: "quality_result", passed: result.passed, issues: result.issues }` to the SSE stream.

**Do NOT:** Block saving if quality fails. Emit the result, let the client decide whether to show a warning or block save. The pipeline's job is to report, not to gate — the UI layer enforces the gate.

### Step 6: Save and Complete

**Action:** Save the draft and metadata to the database, close the SSE stream.
**Inputs:** Full draft, `QualityResult`, `document_id`, `brief`, `sources.verified`
**Outputs:** Saved `Document` record; SSE stream closed

Upsert the `Document` record:
- `content` = full draft text
- `word_count` = actual word count
- `status` = `quality_result.passed ? "complete" : "needs_review"`
- `brief` = serialized Brief
- Save each `VerifiedSource` from `sources.verified` to the `Source` table linked to `document_id`

Emit `{ event: "complete", document_id, status }` to the SSE stream. Close the stream.

**Do NOT:** Close the SSE stream before saving completes. If the stream closes before the save, the client shows "done" while the document may not be persisted.

## Output

Default output:

- Streamed SSE events: `outline_complete`, `chunk` (×N), `draft_complete`, `quality_result`, `complete`
- Saved `Document` record in the database with content, word count, status, and linked sources
- `QualityResult` embedded in the SSE stream (and optionally persisted to the Document record)

## Example

```
[T+0.0s]  POST /api/generate { skillSlug: "reaction-piece", brief: {...} }
[T+0.0s]  Promise.all: compilation + source-grounding started in parallel
[T+3.2s]  source-grounding returns 2 verified sources
[T+3.4s]  compilation completes; sources injected
[T+3.4s]  Outline generation started (max_tokens: 500)
[T+5.1s]  Outline complete → SSE: { event: "outline_complete" }
[T+5.1s]  Draft generation started (streaming, max_tokens: 3000)
[T+5.4s]  First chunk arrives → SSE: { event: "chunk", content: "..." }
           ... (streaming continues for ~40s)
[T+45s]   Draft complete → SSE: { event: "draft_complete" }
[T+45s]   Quality assertion: word_count=912 ✓, sections ✓, citations ✓
           SSE: { event: "quality_result", passed: true, issues: [] }
[T+45.2s] Document saved → SSE: { event: "complete", document_id: "doc_abc123" }
```

## Works Well With

- `skill-template-engine` — Steps 1–2 depend on it; provides the compiled prompt
- `source-grounding` — Step 1 runs it in parallel; provides the source context
- `skill-quality-assertion` — Step 5 logic is the inline version; the full skill can replace it for richer checks
- `skill_token_budget.md` — Apply token budget checks before Step 3 and Step 4 to enforce cost ceiling

## Notes

- The pipeline is stateful within a single generation (steps share memory). It is not designed for concurrent access to the same `document_id`.
- If the outline step fails and is retried, do NOT re-fetch sources — reuse the `SourceContext` from Step 1 to avoid double-charging the search API quota.
- First token latency target: < 5s. Steps 1–3 must complete within that window.
- Full generation latency target: < 90s for `length_tier: "long"` (3000 tokens at Sonnet throughput).
- For the cost ceiling gate (< $0.15 per generation), apply token budget checks from `skill_token_budget.md` before Steps 3 and 4.
