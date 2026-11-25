---
name: openmark-polisher
description: Scrub English drafts for AI tells before publishing. Use for any English LinkedIn post or newsletter draft right after composition and BEFORE export. Removes em-dash-as-pause, weak hedges, rule-of-three patterns, AI vocabulary, negative parallelisms, and inflated symbolism. Triggers on "polish", "humanize", "make this sound human", "/polisher", or after any English composer output. Leaves Arabic and Hebrew drafts untouched — humanizer-* skills handle those.
metadata:
  type: composition
---

# OpenMark — Polisher (English AI-tell scrub)

The composer wrote a draft. Your job is to remove the residue that makes it read AI-shaped. ONE pass, ≤ 6 minutes. Output is the rewritten draft, nothing else.

## When to use vs not
- English drafts only. Arabic / Hebrew → use the `humanizer-ar-*` / `humanizer-he` skills.
- Run AFTER the composer sub-agent, BEFORE the verifier sub-agent.

## What to scrub (the 8 high-signal AI tells)

1. **Em dash used as a pause** (`—`). Replace with comma, colon, parentheses, or a line break. Hyphen compounds like `well-architected` stay.
2. **Filler hedges**: `actually`, `basically`, `really`, `simply`, `just` (when not numeric), `quite`. Delete.
3. **Pleasantries**: `Sure!`, `Of course!`, `Happy to`, `Here's what I found:`, `In conclusion`, `Bottom line:`. Delete or rewrite into the line.
4. **Rule of three** in lists or sentences (`X, Y, and Z`). If the three items don't all carry weight, cut to two or one. Two-element lists beat three-element padded lists.
5. **AI vocabulary**: `leverage`, `delve`, `synergy`, `unlock`, `streamline`, `seamless`, `robust`, `cutting-edge`, `revolutionize`, `paradigm`, `landscape` (when not literal), `journey`, `vibrant`, `tapestry`, `realm`. Replace with the specific noun.
6. **Negative parallelism**: `Not only X, but also Y`. Pick one. Say it once.
7. **Inflated symbolism**: `at its core`, `fundamentally`, `essentially`, `in essence`. Delete; if the sentence still reads, you didn't need it.
8. **Vague attributions**: `experts say`, `studies show`, `many believe`. Name the person, org, paper, or cut the claim.

## Workflow

1. Read the draft once for shape. Note the format (LinkedIn post / essay / roundup / comparison / analytical).
2. Run the 8 scrubs above, in order. Don't change meaning.
3. Re-check word count is still inside the schema bounds. If a deletion pushed you under, replace with one specific noun, not filler.
4. Confirm citations survived — every `[phrase](URL)` is still in the body.
5. Output the rewritten draft as the same Pydantic shape you received. No commentary, no diff, no "I removed X" — just the new draft.

## Voice anchors (don't lose these)

| Generic AI | Ahmad's voice |
|---|---|
| "leverage AI to streamline workflows" | "use the agent for the boring half" |
| "fundamentally transformative" | "actually changes the work" |
| "Three weeks ago, an agent shipped a pull request, the maintainer didn't notice, and the bot got merged." | "Three weeks ago an agent shipped its own pull request. The maintainer didn't notice for a day." |
| "In conclusion, the implications are significant." | (delete the sentence) |

## What NOT to do
- Don't change citations. Same URLs, same anchor positions.
- Don't change the schema shape. If you got a `LinkedInPost` in, return a `LinkedInPost` out with the same field names.
- Don't translate. English in, English out.
- Don't add new claims. You scrub, you don't research.

## Self-check before returning

Tick all four:
- [ ] No em dash used as a pause anywhere in the draft
- [ ] No `leverage` / `delve` / `synergy` / `unlock` / `streamline` / `seamless` / `realm` / `tapestry`
- [ ] No rule-of-three padding ("X, Y, and Z" where Z is the weakest)
- [ ] Word count still inside schema bounds

If any one fails, fix and re-check. Then return the draft.
