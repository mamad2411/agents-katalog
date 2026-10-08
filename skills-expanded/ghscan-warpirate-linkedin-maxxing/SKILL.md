---
name: repurpose-content
description: |
  Use when user has one piece of existing content (podcast or video
  transcript, blog post, internal doc, talk, older LinkedIn post that
  performed, long email) and wants multiple LinkedIn-shaped pieces from
  different angles. Trigger phrases include "repurpose this," "turn this
  into LinkedIn posts," "give me 5 posts from this article," "I have a
  transcript I want to use," or when user uploads a long-form file and
  asks how to use it on LinkedIn.
license: MIT
---

# Repurpose content

One strong piece of source content can become five to ten LinkedIn posts, each from a different angle, because long-form material almost always contains multiple distinct ideas the original author treated as one. This skill exists to find those distinct ideas and shape each into something LinkedIn-sized, in the user's voice, without producing variations on the same thing.

## Why this skill exists

Most LinkedIn AI tools that claim "repurposing" just rewrite the source into a shorter version, then rewrite it again with different phrasing. The result is five posts that say the same thing five ways. They cannibalize each other and bore the audience.

Real repurposing finds the different claims, examples, and moments inside the source and shapes each one into its own LinkedIn-native piece. A talk has multiple beats; each beat can be its own post. A blog post has a main argument and several supporting points; the supporting points can be standalone posts. A podcast transcript has the speaker saying surprising things at specific moments; those moments become posts.

The test: if two of the repurposed pieces could be confused for each other, the repurposing failed.

## When to use this skill

Trigger when:
- The user uploads a long-form file and asks what to do with it on LinkedIn
- The user has a past blog post, talk, or article and wants to extract LinkedIn pieces from it
- The user has a podcast or video transcript (theirs or one they were in) and wants to share it
- A past LinkedIn post performed well and the user wants to mine adjacent angles
- The user has internal docs (decisions, postmortems, design reviews) that can be made public

Do NOT trigger when:
- The user wants to write a new post from a fresh idea. Send to find-ideas, then write-post.
- The user wants to translate the source into a different format with the same content. That is a format conversion, not repurposing.
- The source contains nothing publicly shareable. Repurposing cannot manufacture material.

## What you need from the user

The source content. Either pasted into chat, uploaded as a file, or linked (the user needs to paste the text since URLs often will not fetch). Plus:

1. What is the source? (talk, blog, podcast, internal doc, old post)
2. How many pieces do they want? (Default: 3-5. Cap at 7. More than 7 from one source tends to dilute.)
3. What formats are open? (Posts, carousels, video scripts, or only text posts.)

If voice-profile.md exists, read it.

## How repurposing works

A good repurposing pass has three steps:

**1. Read the source for distinct ideas.** A 30-minute talk has roughly 4-8 distinct beats. A 1,500-word blog post has 3-5. A podcast episode usually has 5-10 "moments" (a surprising claim, a specific story, a turn of phrase). The first job is to identify these without summarizing the whole.

**2. For each distinct idea, identify its anchor.** What is the specific moment, quote, number, or detail from the source that makes this idea LinkedIn-postable? If you cannot point to a specific anchor in the source, the idea is too generic.

**3. Choose a format and an angle.** Each piece gets:
- A format (post, carousel, video script)
- An angle (the one-line first-person claim, like find-ideas seeds)
- The source anchor (the line, moment, or detail that grounds it)

The output of this skill is essentially a batch of find-ideas seeds, each derived from the source, ready to be sent to the appropriate writing skill.

## Output format

```
Source: [type and brief description]
Pieces produced: [N]

---

Piece 1: [format]. [one-line angle]

Source anchor: [the specific line, quote, moment, or detail from the source that grounds this piece]

Why this angle: [one sentence on what makes it postable]

Best fit for: [write-post / build-carousel / write-video-script / write-longform]

---

Piece 2: [format]. [one-line angle]

Source anchor: ...

[continue for each piece]

---

Suggested cadence: [if relevant: how to space the pieces over time so they do not feel like a barrage from one source]
```

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

## A note on cadence

Repurposing produces multiple pieces from one source. Posting them all in one week reads as "I had one thought and milked it." Space them. A reasonable default: one piece per week, two weeks between the strongest two pieces. If the source is from a talk the user gave, the first piece can reference the talk explicitly; the later ones should stand alone without that frame.

For newsletter writers, the source may be the basis of one full issue plus 2-3 feed posts that point back to the newsletter.

## Example

Source: A 45-minute podcast transcript where the user (a CTO) talks about scaling an engineering team from 5 to 30 people.

User asks: "Give me 5 LinkedIn pieces from this."

Output:

```
Source: 45-min podcast on scaling an eng team from 5 to 30
Pieces produced: 5

---

Piece 1 (post): The first hire who is not technical breaks the team's mental model, and nobody warns you

Source anchor: At ~12:00, you say "the day we hired our first PM, every engineer's calendar changed and we had no idea why."

Why this angle: A specific, hard-to-fabricate moment with a concrete trigger (the PM hire) and a non-obvious consequence (calendar disruption). Almost certainly resonates with anyone who has scaled past 10.

Best fit for: write-post

---

Piece 2 (carousel): How our 1:1 system broke at every team size, and what we changed each time

Source anchor: At ~24:00, you describe the 1:1 cadence at 5, 10, 20, and 30 people and what failed at each step.

Why this angle: Has natural sequential structure (4 size milestones, 4 failure modes, 4 fixes). Perfect carousel content.

Best fit for: build-carousel

---

Piece 3 (post): I stopped doing technical interviews when the team hit 15

Source anchor: At ~31:00, the moment you describe handing off the technical bar to a hiring committee.

Why this angle: A specific change of mind by a CTO, with a clear trigger (size 15). The kind of contrarian claim that earns comments from people on both sides of the founder/IC debate.

Best fit for: write-post

---

Piece 4 (video script): The metric I track instead of velocity at this stage

Source anchor: At ~38:00, you say "velocity stopped meaning anything around size 20. I started tracking how often someone says 'I don't know who owns this.'"

Why this angle: The specific surrogate metric is unusual and memorable. Works well on camera because the surprise is in the speaker's voice.

Best fit for: write-video-script

---

Piece 5 (longform): What "founder mode" actually breaks at size 25

Source anchor: A throughline across the second half of the transcript, where you push back on the popular "founder mode" framing.

Why this angle: A point of view on a current debate, with first-hand evidence at a specific scale. Long-form because the argument needs space to engage with the opposing position.

Best fit for: write-longform

---

Suggested cadence: Lead with Piece 3 (the change of mind), follow two weeks later with Piece 1 (the PM moment), then Piece 4 (video) the following week. Save Piece 2 (carousel) for a week when you have time to design slides. Piece 5 (longform) when you have a Saturday morning.
```

## What this skill does not do

- Produce 10 minor variations on the same idea. The whole point of this skill is finding distinct ideas in the source. If you cannot find 5 distinct ideas, return 3.
- Fabricate quotes the source does not contain. Every source anchor must point to a real line or moment.
- Translate the source verbatim into a "shorter version." That is conversion, not repurposing. Send to write-post if the user wants the source compressed.
- Repurpose copyrighted material the user does not own. If the source is someone else's blog or podcast, the user can repurpose their *response* to it (which is original commentary), not the content itself.
- Strip context from a source in a way that makes the user's point misleading. If a specific anchor only makes sense in the source's context, it is not a good standalone piece.
