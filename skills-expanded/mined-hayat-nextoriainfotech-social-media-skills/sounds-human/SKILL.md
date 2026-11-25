---
name: sounds-human
description: Rewrites captions, replies and short posts so they stop sounding machine-written: removes dash-heavy punctuation, filler words, stacked short fragments, fake candor, rule-of-three lists and empty hype, while keeping the meaning, the facts and the owner's voice. Use when the user says a draft "sounds like AI", "too robotic", "make it natural", or as a final pass after reply-in-my-voice or post-everywhere. Never adds facts, numbers, stories or claims that were not in the original. Not for changing what a post says, only how it says it.
license: MIT
---

# Sounds human

Make text read like a person wrote it, without changing what it says.

## When to use

- "This caption sounds like ChatGPT."
- "Make these replies less robotic."
- Final pass on any draft before the user approves it.

## Hard rules

1. **Meaning and facts stay exactly the same.** Don't add numbers, anecdotes, emotions, opinions or claims. Don't drop a fact either.
2. **Keep the owner's voice.** If `voice-profile.md` or the connector's `get_voice` is available, its habits win over the list below (if the owner loves exclamation marks, keep them).
3. **Same language.** An Arabic draft stays Arabic; don't translate.
4. **Shorter is usually better,** but don't cut the point or the call to action.
5. **Don't fake humanity.** No invented typos, no pretend personal stories, and never a line claiming the text wasn't AI-assisted.

## Steps

1. Read the draft and find the tells using [references/ai-tells.md](references/ai-tells.md).
2. Rewrite: plain words, natural rhythm, one idea per sentence, the point first.
3. Show **before and after**, with a one-line note of what changed. For several items, a short table.
4. If the user wants, list the tells you found so they can avoid them next time.

## Example

Before: "In today's fast-paced world, finding the perfect gift can be challenging. That's where we come in. Handmade. Thoughtful. Unique. Discover our collection today!"

After: "Stuck on a gift? Everything in our shop is made by hand, and no two pieces are the same. Have a look."

Changed: removed the cliché opener, the fragment stack and the generic "discover" call to action; kept the three facts (handmade, unique, a shop to visit).

## Related skills

Use after `reply-in-my-voice` and `post-everywhere`. Works with no connector and no account.
