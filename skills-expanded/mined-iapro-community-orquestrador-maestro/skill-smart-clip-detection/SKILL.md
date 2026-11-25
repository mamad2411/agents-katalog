---
name: skill-smart-clip-detection
description: Use for AI-assisted clip detection from transcripts, livestreams, videos, podcasts, calls, or long-form content, including scored candidates, timestamps, batching, validation, prompt versioning, review queues, idempotent reprocessing, consent, and publishing-ready metadata.
category: media
risk: medium
source: local-media-ai-patterns
---

# Smart Clip Detection

Use this skill when a product needs to find short, valuable moments inside long audio or video content.

## Detection Contract

1. Start from transcript segments with timestamps when available. Add visual and audio signals only when they improve ranking.
2. Validate source consent, processing rights, language, duration, platform targets, and user quota before analysis.
3. Batch candidate generation by transcript windows. Send only segment text, timestamps, and compact metadata required for scoring.
4. Cache transcript segments, embeddings, signal extraction, and prompt outputs by source checksum plus prompt/schema version.
5. Score candidates by hook strength, self-contained meaning, novelty, emotion, clarity, platform fit, and editability.
6. Keep source timestamps, confidence, reason, title ideas, captions, aspect ratio, and source segment IDs.
7. Deduplicate overlapping candidates using timestamp overlap, semantic similarity, and source segment IDs.
8. Store enough metadata to regenerate or re-score after model, prompt, schema, or platform changes.
9. Prefer review queues over auto-publishing for customer-facing, paid, or brand-sensitive products.
10. Use idempotent render jobs for approved clips; never overwrite approved assets without a new version.

## Candidate Schema

```typescript
type ClipCandidate = {
  sourceAssetId: string;
  startMs: number;
  endMs: number;
  durationMs: number;
  score: number;
  confidence: number;
  reason: string;
  hookText: string;
  summary: string;
  titleOptions: string[];
  platformFit: Array<"TikTok" | "Reels" | "Shorts" | "LinkedIn" | "YouTube">;
  reviewStatus: "pending" | "approved" | "rejected" | "needs_edit";
  promptVersion: string;
};
```

## Token Reduction

- Chunk transcripts by coherent segments, not arbitrary character counts.
- Keep a rolling summary for context, but score only the current window and adjacent overlap.
- Use hashes for transcript excerpts in logs and persist full excerpts only when review requires them.
- Run cheap deterministic filters before model scoring: duration, silence, speaker count, and duplicate overlap.

## Verification

- Test empty transcript, missing timestamps, overlapping candidates, duplicate reprocessing, malformed model output, revoked consent, queue retry, and review approval/rejection.
- Compare outputs against a small labeled fixture to verify scoring changes before rollout.

## Related Skills

- `skill-live-processing`
- `skill-manual-video-processing`
- `skill-ai-orchestration`
- `skill-unified-analytics`

