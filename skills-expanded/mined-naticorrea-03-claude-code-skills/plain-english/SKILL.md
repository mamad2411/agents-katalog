---
name: plain-english
description: Rewrite an explanation so the user actually wants to read it: short, plain, no jargon. Use the MOMENT they signal a reply was too long, too technical, or they just don't want to read it: "/plain", "in plain english", "english please", "shorter", "tldr", "too technical", "too long", "say that simpler", "dumb it down", "eli5", "what does that actually mean", "just tell me", "redo that", "rephrase that", or any sign they're bouncing off a wall of text or jargon. Default target is the last thing Claude said; the user can also point it at any other text (an email, a doc, something they paste). On-demand only, never auto-fires.
---

# Plain English

## What this is for

Users keep having to tell Claude to redo, rephrase, or "use plain English." The root cause usually isn't formatting. It's that the explanation is too long, buried in jargon, or explaining things they didn't need explained. They bounce off it and have to ask again.

This skill is the fast fix. The user fires it, you rewrite the thing so they actually read it.

## What to do

Default target is **the last thing you said**. If the user points it somewhere else (an email, a doc, text they paste), rewrite that instead.

Rewrite it so:

- **Lead with the answer.** First line says the thing or what it means for them. No runway, no "so basically," no "great question."
- **Cut the jargon.** If a technical word is genuinely load-bearing, drop one plain phrase next to it in parentheses. Otherwise replace it. Assume the reader is smart but does not want to debug your internals.
- **Shorter than you think.** Most of these collapse to 2-4 sentences or a few bullets. If the original was ten lines, the rewrite is probably three.
- **Drop what they can't act on.** The caveats, the "it's worth noting," the background they didn't ask for. If it doesn't change what they do next, it goes.
- **Keep it human.** No filler, no corporate buzzwords, no "it's not X, it's Y" constructions, short sentences. If it reads like a LinkedIn post, it's wrong.

Then just give the clean version. Don't show the before, don't explain what you trimmed, don't apologize for the first one. They asked for the short version, so the response to "make it shorter" should not itself be long.

## The instinct to carry forward

The bigger signal: if the user is invoking this, the last answer missed. Carry that into the rest of the session without being told. Default to shorter and plainer for the rest of the conversation. They can always ask for more depth. They rarely will.

## Examples

**Example 1, too technical**

Before:
> The cron routine fires via a scheduled trigger on a weekday cadence and the dedup logic keys off whether the thread already has a draft, so idempotency is preserved across overlapping invocations.

After:
> It runs every weekday morning. It won't double-draft the same email because it checks whether a draft already exists first.

**Example 2, too long**

Before: (eight lines walking through every step of how a report gets built, the data sources, the fallback path, and three caveats)

After:
> The report is built from the live numbers, with a screenshot-paste backup if the data source is down. Want me to run one now?

**Example 3, they just don't want to read it**

Before: (a dense paragraph weighing three options with tradeoffs)

After:
> Go with option B. It's the least work and you can change it later. The other two lock you in.
>
> Want the reasoning, or is that enough?
