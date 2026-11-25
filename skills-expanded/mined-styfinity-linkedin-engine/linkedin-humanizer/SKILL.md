---
name: linkedin-humanizer
description: Strip the AI fingerprints out of any draft (a post, a DM, a comment) so it reads like a real person wrote it. Use before publishing anything written or edited with AI.
argument-hint: "[the draft to clean]"
---

# LinkedIn Humanizer

The draft that reads like a machine wrote it gets ignored. This skill removes the tells and puts the human voice back in, without touching the meaning.

## Inputs
- Any draft (a post, a DM, a comment): $ARGUMENTS
- The brief (persona voice, pains, offer) loads automatically, so use it to match the operator's real register.

## Do this
1. Remove every em-dash. Replace with a comma, a period, or " - ".
2. Strip banned AI vocabulary: leverage, delve, landscape, navigate, utilize, foster, robust, supercharge, seamless, unlock, elevate, harness, empower, streamline, "game-changer", and any thesaurus word a person would not say out loud.
3. Break up rule-of-three symmetric lists. Real people do not write in perfect triplets.
4. Delete fake-candid openers: "Let me be honest", "Here's the thing", "I'll be the first to admit". Cut straight to the point.
5. Vary the sentence length. Uniform rhythm is the loudest AI tell. Put a short one next to a long one.
6. Put the human back: one casual run-on with a comma splice, plain low-reading-level words, one direct un-hedged opinion, and a flat statement (not a question) to end on.
7. Keep "I" not "we" in the hook. The operator is one person, not a brand.

## Output
The cleaned draft first. Then a short bullet diff: what was changed and why. Then a one-line verdict: PUBLISH, or STILL READS AI - fix these (name the exact phrases).

## Rules
- Never change the meaning or the claims. Keep all numbers exactly as written.
- This is a polish pass, not a rewrite. If a line is already human, leave it.
- If anything still reads like AI after the pass, flag the specific phrase, do not silently let it through.
- No em-dashes in the output. Obviously.
- This skill only cleans drafts. It does not publish. The operator approves and posts.
