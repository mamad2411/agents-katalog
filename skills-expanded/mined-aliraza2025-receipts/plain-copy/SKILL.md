---
name: plain-copy
description: Rewrites product, portfolio, and launch copy into plain, specific language by removing AI-sounding filler, em dashes, inflated verbs, and vague outcomes, without adding any new claims. Use when the user asks to edit, polish, humanize, de-AI, or simplify copy, or when text "sounds like ChatGPT".
---

# Plain copy

Plain copy says what happened, for whom, and how you know. This skill edits for clarity and removes the patterns that make writing sound generated, while never adding facts.

## Workflow

1. **Run `claim-receipts` first** if the text contains numbers or outcomes. Plain wording on a false claim is still false.
2. **Edit** using the rules below.
3. **Return** the rewrite, then a short list of the changes that altered meaning (not every word swap).

## Rules

- **No em dashes.** Use a period, comma, colon, or parentheses instead.
- **Concrete over abstract.** "Cut quoting time on calls" over "streamlined operational workflows". If you cannot make it concrete from the source, keep it short and general rather than inventing specifics.
- **Plain verbs.** built, shipped, measured, cut, fixed, tested, wrote. Avoid: leverage, utilize, empower, unlock, elevate, revolutionize, supercharge, seamless, robust, cutting-edge, game-changing, delve, tapestry, landscape, realm.
- **No filler frames.** Cut "In today's fast-paced world", "It's worth noting that", "At the end of the day", "Not only X but also Y" when X and Y are not a real contrast.
- **No reflexive triplets.** Lists of three adjectives or three parallel clauses only when there really are three things.
- **Numbers keep their scope.** Never drop a denominator, date, or sample description while shortening.
- **Say who did it.** Replace vague "we" with the actual actor when the source makes it clear.
- **Keep honest hedges, cut empty ones.** "On a 19-link benchmark" stays. "Arguably", "potentially", "in many ways" go.
- **Short sentences, one idea each.** Aim for an average under 20 words.

## Example

Before (a deliberately bad draft):
"Leveraging cutting-edge AI, CrediClip seamlessly empowers users to unlock the truth behind short-form video, delivering robust credibility insights at scale."

After:
"CrediClip takes a TikTok, Instagram, or YouTube Shorts link and returns a credibility score, risk flags, and the evidence behind them. When it cannot recover enough evidence, it says so."

Meaning changes: removed "at scale" (no source); added the abstention sentence only because the product's documented behavior includes it.
