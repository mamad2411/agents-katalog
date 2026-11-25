---
name: talk-to-assets
description: Use this skill after the user gives a conference talk, webinar, podcast appearance, or recorded interview to produce a multi-channel asset bundle from the recording or transcript. Triggers on phrases like "assets from [talk]", "post-event content", "extract from this recording", or when the user references a recently delivered talk and wants to repurpose it. Produces 8-10 assets from one source.
---

# Conference Talk to Multi-Channel Assets

## When to use this skill

The user just delivered a 30 to 60 minute talk, panel, webinar, or interview. Without this skill, they typically write one LinkedIn post about it and call it done. The talk is worth 10x more in surface area, but the activation energy to extract the rest is high enough to kill the practice. This skill removes the activation energy and produces the full bundle in one pass.

## Input the user provides

- The talk transcript, recording, or slide deck
- Context: where the talk was given, who the audience was, what the speaker's posting cadence is
- Optionally: voice samples from prior posts to match register

## What this skill does

From a single source, produces the following assets in one pass:

1. **Three LinkedIn posts** with different hooks (specific result, contrarian claim, story opener)
2. **One Substack adaptation** that takes the talk's arc and rewrites it for a reading audience
3. **One one-page handout** for attendees who requested follow-up
4. **Five quote-card text snippets** suitable for graphic design (one strong line each, no context dependency)
5. **One thank-you note** to the conference organizer in the speaker's voice
6. **One draft email** for audience members who left contact info, with the handout attached
7. **Two podcast pitch lines** (if the speaker is interested in being booked on adjacent shows)
8. **One internal team brief** if the talk relates to ongoing work, summarizing what was said and what feedback came back

## Output structure

```
# Asset Bundle: [Talk title]
*Event: [name]. Date: [date]. Audience: [type and rough size].*

---

## LinkedIn Post 1: Specific Result Hook
[Draft, 1200-1800 characters, with a hook that names a concrete outcome from the talk]

## LinkedIn Post 2: Contrarian Claim Hook
[Draft, 1200-1800 characters, with a hook that states a position the audience might push back on]

## LinkedIn Post 3: Story Opener Hook
[Draft, 1200-1800 characters, opens with a specific moment from the talk or the lead-up]

---

## Substack Adaptation
[Title and opening paragraph at minimum, 1500-2500 words total when expanded. Includes 3 key takeaways block per workspace convention.]

---

## One-Page Handout for Attendees
[Compressed version of the talk's core argument, with 3 takeaways, 1 recommended next step, and the speaker's contact info]

---

## Quote Cards (5)
1. "[Standalone quote 1, no context needed]"
2. "[Standalone quote 2]"
3. "[Standalone quote 3]"
4. "[Standalone quote 4]"
5. "[Standalone quote 5]"

---

## Thank-You Note to Organizer
[Personal email, 100-150 words, mentions one specific thing about the event that was well-run]

---

## Audience Follow-Up Email
[150-200 words, with handout attached, ending with one clear CTA]

---

## Podcast Pitch Lines (2)
1. [Pitch angle 1 - the contrarian one]
2. [Pitch angle 2 - the practical one]

---

## Internal Team Brief
[For colleagues who could not attend, 300-500 words on what was covered, what feedback was received, and what to do about it]
```

## Calibration notes

- All assets must be in the speaker's voice. If voice samples are provided, study them for sentence length, vocabulary, opening style, and closing style. Match deliberately.
- Quote cards must work without context. If a line requires three sentences of setup to make sense, it is not a quote card.
- LinkedIn posts should each have a distinct hook. Do not write three variations of the same hook.
- The Substack adaptation is the highest-effort asset. Do not skip the takeaways block. Adapt the talk's arc, do not just transcribe.
- The thank-you note matters. It is the smallest asset and the highest-trust asset for future bookings.

## Voice matching

Watch for these specific markers in voice samples:
- First-person plural vs. singular usage
- Tendency toward short punchy sentences vs. longer analytical ones
- Use of humor, irony, self-deprecation
- Opening conventions (story, claim, question, stat)
- Closing conventions (challenge, principle, CTA, observation)
- Punctuation habits (em-dash usage, parentheticals, fragment cadence)

## When NOT to use this skill

- Talks the speaker is not happy with (post-event reflection should happen first)
- Off-the-record or NDA-restricted talks
- Internal-only presentations not meant for external audiences
