---
name: shorts-hooks
description: Write and assess source-grounded hooks in the creator’s voice for Shorts Factory. Use for headline quality, opening coherence or updating the hook playbook.
---

# Shorts Hooks

Read `prompts/copy-playbook.md`, `src/lib/hook-strategy.ts`, and the creator profile from the active data directory. Identify a concrete question the viewer will want answered and the exact spoken passage that answers it. Generate variants of two or three mechanisms that fit this clip. Keep the title and first spoken words on the same subject.

Faithfulness, audience, clarity, voice, coherence and actual payoff are vetoes. A high curiosity score cannot compensate for a false promise. Outlier observations are reference data; do not copy another creator’s phrases, facts, revenue, identity or persona.

For evaluation, compare candidates against the transcript and profile, including weak/control examples. Test the real model separately from mocked pipeline tests; disclose a quota block rather than reporting a successful qualitative evaluation. Run `node --no-warnings --test test/hook-strategy.test.ts test/hook-pipeline.test.ts`.
