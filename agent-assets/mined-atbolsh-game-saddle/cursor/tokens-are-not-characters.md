---
description: Never use text-length proxies for token counts; token-exact invariants stay token-exact
alwaysApply: true
---

# Tokens are not characters — no length proxies

Token count is a property of the tokenizer output, not of the text. Character
count, word count, or "chars // 32 buckets" do NOT predict token count: two
prompts with identical token length can differ by hundreds of characters
(and vice versa), and multimodal prompts add per-image soft tokens that text
length never sees. When an invariant is defined in token space, enforce it in
token space — encode first, then compare exact integers.

Real bug this rule comes from: at the time, `generate_batch` could only
true-batch rows whose **prompt token lengths were exactly equal** (the
Gemma 4 Unified left-pad prefill bug, transformers#47651 — since worked
around with token-exact arithmetic, which only sharpens the point). A
dispatcher "optimization" grouped requests by `text_chars // 32` buckets.
That proxy:

- could not create equal-token-length cohorts (chars don't determine tokens),
- actively *prevented* same-token-length prompts from ever batching when
  their char counts straddled a bucket boundary,
- was redundant anyway — `generate_batch` encodes each row and splits into
  exact-length cohorts itself.

Guidance:

- **The encode step is the only source of truth for length.** If a decision
  needs token counts, run the processor/tokenizer and read
  `input_ids.shape[1]`. If that's too expensive at the decision point, move
  the decision to where encodings already exist (as `generate_batch` does);
  do not substitute a cheaper text-space guess.
- **Don't pre-filter upstream of an exact check.** A heuristic gate in front
  of an exact grouping can only remove valid matches, never add them.
- Same discipline for truncation limits, context-window budgeting, and span
  arithmetic: `max_new_tokens`, offsets from offset mappings, and prompt-length
  slicing are token quantities; `len(text)` is never a stand-in.
