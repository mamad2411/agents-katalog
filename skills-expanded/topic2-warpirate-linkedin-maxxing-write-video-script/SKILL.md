---
name: write-video-script
description: |
  Use when user wants to post a short-form LinkedIn video (30-90
  seconds), an idea has visual or demonstrative power text cannot
  capture, user has a strong speaking voice that should be on camera, or
  a find-ideas seed is marked "Best fit for: write-video-script."
  Trigger phrases include "write a video script," "I want to make a
  video," "this would work better on camera," "script me a 60-second
  video."
license: MIT
---

# Write video script

Video scripts are a different craft from posts. A 60-second talking-head script has a hook in the first three seconds, beats instead of paragraphs, and natural-sounding spoken prose that holds up when said out loud. This skill exists to write video scripts that work in the user's voice, not the average LinkedIn-AI video voice that has become its own template.

## Why this skill exists

Two facts make video important right now: it gets roughly 5x the interactions of equivalent text posts, and LinkedIn's projected content mix has video at about 65% by late 2026. The format is genuinely growing.

But the bar is higher. A weak text post fails quietly. A weak video has the user's face attached to it. The reader can hear filler words, see hesitation, watch the user struggle to land a point. This skill exists to make sure the script is worth reading aloud before the user records anything.

## When to use this skill

Trigger when:
- The user wants to record a LinkedIn video
- A seed from find-ideas is marked video-script
- The idea has demonstration value (the user can show a thing, not just describe it)
- The user has spoken about a topic and wants to capture it on video

Do NOT trigger when:
- The user wants a written post. Send to write-post.
- The user wants a long-form spoken piece (5+ minutes). LinkedIn video is short-form territory; long content lives in podcasts or YouTube.
- The user is uncomfortable on camera. Be honest: video may not be the right format. Suggest a carousel instead.

## What you need from the user

The angle (one sentence) and:

1. **Talking-head, demonstration, or both?** Talking-head: just the user on camera. Demonstration: showing a screen, a product, a workflow, with the user narrating. Both: cuts between.

2. **Target length.** Default 45-60 seconds. Up to 90 if the content needs it. Below 30 is rarely worth filming.

3. **Where will it be filmed?** Phone in a quiet room is fine. The script should not assume studio production.

If voice-profile.md exists, read it. Spoken voice and written voice often differ, so flag that this is the spoken version.

## How video scripts work in 2026

A LinkedIn short-form video that works has these traits:

**Hook in the first 3 seconds, no exceptions.** The first three seconds decide whether the viewer keeps watching. The hook is not the intro ("Hi, I'm X, today I want to talk about..."). The hook is the most interesting thing the video is going to say, delivered first. Then context comes after.

**Beats, not paragraphs.** Spoken content moves in beats: one claim per beat, with a brief pause before the next. Each beat is one or two short sentences, then a breath, then the next. Long sentences do not work on camera; the speaker runs out of breath and the viewer loses the thread.

**Captions are mandatory.** A significant share of LinkedIn video is watched muted. The script should be writeable as captions without losing meaning. Avoid puns or wordplay that only land aurally.

**Concrete over abstract.** Same rule as posts, more important here. The video has 60 seconds; abstract claims burn that time.

**Camera-friendly ending.** Spoken endings need a clear cue that the video is over. A specific takeaway, a question, or a single sentence that lands. Cold cuts read as the speaker forgot their line.

## Script structure

A 60-second script is roughly:

- Hook (0-3 seconds, ~15 words): the strongest claim first
- Context (3-15 seconds, ~30 words): one sentence on why this matters
- The substance (15-50 seconds, ~80-100 words): 2-4 beats of actual content
- Close (50-60 seconds, ~15-20 words): the takeaway or a question

That is roughly 140-160 spoken words for 60 seconds at conversational pace. Adjust for the speaker's actual pace.

For a 45-second script: cut one beat from the substance.
For a 90-second script: add one beat, or develop one of the existing beats further.

## How to draft

1. Read voice-profile.md if present.

2. Identify the hook. The hook is the most surprising or specific thing in the idea, said first. Not "Today I want to talk about X." Not "Have you ever noticed Y." The actual claim.

3. Write the beats. Each beat: one claim, one or two short sentences. Read each beat aloud (mentally). If you stumble, rewrite.

4. Write the close. Land the point. No "thanks for watching" or "let me know in the comments" unless the user genuinely uses those.

5. Mark timing roughly. The user can adjust during recording.

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
Title: [working title]
Target length: [seconds]
Format: [talking-head / demonstration / both]

[0:00-0:03] HOOK
[script]
[On-screen text: optional caption to reinforce]

[0:03-0:15] CONTEXT
[script]
[Visual note if relevant]

[0:15-0:50] SUBSTANCE
Beat 1: [script]
Beat 2: [script]
Beat 3: [script]
[Visual notes for any demonstration]

[0:50-1:00] CLOSE
[script]
[On-screen text: any final card]

---

Word count: [N words for ~M seconds at conversational pace]

Notes for recording:
- [Any cues for the speaker: pauses, emphasis, where to look]
- [Any cues for editing: cuts between talking-head and screen]
```

## Example

Angle: I shipped a script without types after a year of arguing for them. Change of mind, specific anchors.

User confirms: "Make this a 60-second talking-head video. I'll film it on my phone."

Output:

```
Title: I changed my mind about static typing in a week
Target length: 60 seconds
Format: talking-head

[0:00-0:03] HOOK
I shipped a Python script with no type validation last week. Six months ago I would have blocked the same merge in code review.
[On-screen text: "I changed my mind"]

[0:03-0:15] CONTEXT
For a year I was the loudest pro-types person on my team. I wrote the RFC. I held up merges. I was probably annoying.

[0:15-0:50] SUBSTANCE
Beat 1: The script reads twelve JSON fields and writes them to a queue. I almost spent half a day writing a Pydantic model for it. I didn't. I shipped it raw.

Beat 2: I expected a production fire by Wednesday. Malformed payload, schema drift, the 3am page. None of it happened. The script has been running for a week and nothing has broken.

Beat 3: The thing I noticed is that most of my arguments were about the worst case. Real concerns. None of them have actually happened on this script.

[0:50-1:00] CLOSE
I still think types are right for most things. The thing I changed my mind about is the default.
[On-screen text: "Type what's caused problems. Justify the rest."]

---

Word count: ~145 words for ~60 seconds at conversational pace.

Notes for recording:
- Slight pause after "I didn't" in Beat 1.
- Read Beat 3 slower than the others; this is the turn.
- On-screen text at 0:50 should appear after the spoken close, not during.
```

## What this skill does not do

- Write scripts for video formats this skill is not designed for (long-form YouTube, podcast, TikTok). LinkedIn video is short-form professional content; other formats have other rules.
- Write scripts the user cannot actually deliver. If the script reads as "salesy" or unlike how the user speaks, that breaks on camera worse than on the page. Match voice carefully.
- Promise the video will perform. Video performance depends on the speaker's presence, the production quality, the lighting, the audio. Script is one variable.
- Include teleprompter-style stage directions. The user is filming on their phone, not directing a film. Keep notes minimal.
- Make scripts longer than they need to be. A tight 45-second video beats a padded 90-second one.
