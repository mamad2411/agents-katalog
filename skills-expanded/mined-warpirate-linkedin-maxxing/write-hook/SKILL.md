---
name: write-hook
description: |
  Use when user has a LinkedIn post body but a weak opening, wants to
  A/B several hook angles before drafting the full post, or their
  existing post is not earning "see more" expand clicks. Trigger phrases
  include "write a hook," "fix my hook," "give me 5 hook variants," "the
  first line of my post is weak," "rewrite the opening." Hook must fit
  the 210-character LinkedIn fold.
license: MIT
---

# Write hook

The hook is the most important part of a LinkedIn post and the easiest one to write badly. This skill exists to generate several hook angles, all under the 210-character fold, that earn the "see more" click without resorting to bait.

## Why the hook matters

LinkedIn shows the first ~210 characters of any post before the "See more" cut. If the reader does not click, the post earns no dwell time, and LinkedIn deprioritizes it. The hook is the entire ad for the rest of the post. A weak hook means the rest of the post is unread no matter how good it is.

A good hook does one job: open a curiosity gap or commit to a specific claim that the reader wants the resolution of. It does not give away the post. It does not summarize the post. It earns the click.

## When to use this skill

Trigger when:
- The user has a post draft and wants the opening sharpened
- The user wants to compare 3-5 different hook angles before drafting
- The user's recent posts have low expand rates (visible in analyze-performance output)
- The user is staring at a blank screen and the post body will come once the hook lands

Do NOT trigger when:
- The user needs a full post written. Send them to write-post.
- The user wants to study viral hooks from other posts. That is a different request; this skill writes hooks, not analyzes them.

## What you need from the user

The angle of the post (one sentence is enough) and either the post body (if it exists) or a quick description of what the post will say. Ask:

"What is the post about, in one sentence? And do you have the body yet, or are we hooking-first?"

If voice-profile.md exists, read it. The hook should match the user's actual opening style.

## How hooks work in 2026

Hooks fall into roughly six types that still perform on LinkedIn:

1. **Specific number.** "47% of our pipeline closes in the last 5 days of the quarter." Works because the specificity signals real data, not opinion.

2. **Confession.** "I shipped a feature this week I'm not sure about." Works because vulnerability earns curiosity.

3. **Contrarian claim against received wisdom.** "Most B2B PMs are wrong about onboarding." Works if the user is willing to defend it.

4. **Story setup with implied payoff.** "A founder asked me to review her pitch deck yesterday. I told her to delete two slides." Works because it implies a resolution the reader wants.

5. **Unusual fact.** "The longest-running script in our codebase was written on a Sunday in 2019. Nobody knows by whom." Works because it is hard to fabricate.

6. **Change of mind.** "I used to argue for type checking on every endpoint. I shipped a script without types last week." Works because the contradiction is the post.

Hooks that fail in 2026, regardless of how clever:

- "Have you ever wondered..."
- "Let me tell you a story..."
- "Here's what I learned this week."
- "Three lessons from my last role."
- "Most people don't realize..."
- Anything starting with "Imagine"
- Anything ending in a generic question ("Thoughts?")

## How to draft variants

Produce 3-5 hooks, each from a different type above. Each must:

- Be under 210 characters including spaces
- Open a curiosity gap or commit to a defensible claim
- Use specific detail when possible
- Match the user's voice (if voice-profile.md exists)

Order the variants from strongest to weakest. Mark the strongest one and say why.

## Drafting constraints (apply WHILE writing, not after)

Output must read as written by a human on the first pass. The constraints below are how you write, not a checklist to apply later. Do not narrate this process to the user. Do not show a "before humanizer / after humanizer" sequence. Just produce clean output.

**Hard bans — never appear in output:**
- Em dashes (—) and en dashes (–). Use period, comma, colon, or parentheses.
- "It's not just X, it's Y" / "Not only X but Y" constructions.
- "The real question is," "at its core," "fundamentally," "what really matters."
- Signposting: "Let's dive in," "here's what you need to know," "let's break this down," "without further ado."
- Sycophancy: "Great question," "you're absolutely right," "I hope this helps," "let me know if..."
- Knowledge-cutoff hedges: "based on available information," "as of my last update."
- AI vocabulary: leverage, delve, tapestry, underscore, pivotal, crucial, vibrant, testament, landscape (abstract), interplay, intricate, fostering, enduring, garner, valuable, enhance, showcase, align with, additionally.
- Copula avoidance: "serves as," "stands as," "marks a," "represents a," "boasts," "features." Use is/are/has.
- Emoji decoration on bullets or headings.
- Title Case In Headings. Use sentence case.
- Curly quotes ("..."). Use straight quotes (") only.
- Bold for random emphasis. Bold only for genuine key terms.
- Rule-of-three padding where the third item is filler.
- Generic upbeat conclusions ("The future looks bright," "exciting times ahead").
- Aphorism formulas ("X is the language of Y," "X becomes a trap," "X is not a tool but a mirror").
- Theatrical openers: "Honestly?" "Look," "Here's the thing," used as standalone pause-and-reveal.
- Inline-header bullet lists (`- **Speed:** ...`). Write as prose.
- "-ing" tag-ons that add fake depth: "highlighting," "underscoring," "fostering," "reflecting," "showcasing," "ensuring," "contributing to."

**Required patterns:**
- Specific, hard-to-fabricate detail. Real numbers, real names, real quotes from the user's input.
- Vary sentence length. Short. Then longer ones that take their time. Mix.
- Active voice over passive. Concrete actor over hidden subject.
- Simple copulas (is/are/has) over fancy substitutes.
- One opinion or mixed feeling where the format allows (not for neutral reference text).
- Cut every filler phrase ("in order to" → "to," "due to the fact that" → "because," "at this point in time" → "now," "has the ability to" → "can").

**Final scan before output:**
1. Scan for `—` and `–`. Any hit means redraft.
2. Scan for any word in the AI-vocabulary list above. Any hit means rewrite that sentence.
3. Scan for "it's not X, it's Y" pattern. Any hit means rewrite.
4. If three short fragments appear in a row mid-paragraph, the rhythm is engineered. Vary.

Full 33-pattern reference: see humanizer/SKILL.md in this plugin.

## Output format

```
Hook variant 1 (specific number) [character count]:
[hook text]

Hook variant 2 (confession) [character count]:
[hook text]

Hook variant 3 (contrarian claim) [character count]:
[hook text]

Hook variant 4 (story setup) [character count]:
[hook text]

[Strongest: variant N. Why: one sentence on what makes it land.]
```

## Example

User input: "Post is about how I changed my mind on type validation in Python after spending a year arguing for it. The thing that did it was shipping a 12-field script without Pydantic and it being fine."

Output:

```
Hook variant 1 (confession) [108 chars]:
I shipped a script without types last week. Six months ago I would have blocked the same merge in review.

Hook variant 2 (change of mind) [156 chars]:
For a year I was the loudest pro-types person on my team. Then last week I shipped a script without a single type annotation. Here is what changed.

Hook variant 3 (specific number) [148 chars]:
I almost spent half a day writing a Pydantic model for 12 fields. I didn't. The script has been running for a week and nothing has broken.

Hook variant 4 (contrarian claim) [144 chars]:
Most of my arguments for static typing were about bugs that have not actually happened. I noticed this when I shipped a script without any types.

Strongest: Variant 1. The confession ("I shipped without types") immediately followed by the tension ("I would have blocked this") opens a question the reader wants resolved in 210 characters of space. The other variants give too much away or take too long to land.
```

## After the user picks one

Offer to pass the chosen hook plus angle to write-post for the full draft. Do not auto-draft; let the user decide.

## What this skill does not do

- Predict which hook will go viral. Engagement is unpredictable. The skill produces hooks that earn the click; whether the post goes viral depends on the body, the audience, and timing.
- Use templates from sales copy (PAS, problem-agitate-solve). These show up in LinkedIn's AI-slop detection now and are downranked.
- Produce 10+ variants by default. 3-5 distinct angles beats 10 minor variations.
- Write hooks for posts that are not really posts. If the user is trying to hook a sales pitch or a job ad, redirect them to a different format.
