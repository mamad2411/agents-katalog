---
name: no-ai-speak
description: Detect and remove "AI speak" (AIisms) from text - the overused words, phrases, and formatting tells that make writing sound machine-generated. Use when the user asks to de-slop, humanize, or clean up AI-sounding writing, check whether text reads as AI-generated, or rewrite a draft to sound human.
---

# no-ai-speak

Find and strip the tells cataloged in the AI Speak Dictionary from a piece of text.

## When to use

- "Does this sound like AI?" / "make this sound human" / "de-slop this" / "remove the AI speak".
- Before publishing anything you drafted, as a self-check.

## How to run it

1. **Detect.** If the repo's detector is available, run it to get located, ranked hits:

   ```
   python scripts/detect.py <file>           # or:  <text> | python scripts/detect.py -
   python scripts/detect.py <file> --json     # machine-readable
   ```

   The output lists each hit with its line, confidence (high/medium/low), and a "use instead" suggestion where one exists, plus a score (weighted hits per 1000 words) and a band (clean / light / noticeable / heavy).

   If you cannot run the script, scan by hand against [`general/master-wordlist.md`](../../../general/master-wordlist.md), [`general/phrases.md`](../../../general/phrases.md), and [`general/formatting-patterns.md`](../../../general/formatting-patterns.md).

2. **Rewrite.** Apply [`prompts/de-slop-rewrite.md`](../../de-slop-rewrite.md): replace inflated words with plain ones, delete filler phrases and canned openers/closers, unstack transitions, cut rhetorical tics and reflexive hedging, strip formatting bloat and em dashes, and vary sentence length. Keep meaning, facts, and code unchanged. Don't make it longer.

3. **Re-check.** Run the detector again and confirm the score dropped. Report the before/after score and the main changes.

## Principles

- **Clustering is the real tell.** One "robust" is fine; five AI words in a paragraph is the signal. Prioritize dense clusters.
- **Context matters.** Many words are legitimate in their field ("robust" in statistics, "delve" in a mining piece). Don't "fix" correct usage.
- **Don't overcorrect into a new tell.** Stilted word-swaps and forced short fragments are their own kind of slop. Aim for how a knowledgeable person actually writes.
- **Preserve the author's voice and register.** De-slopping removes machine habits; it should not flatten a real style.
