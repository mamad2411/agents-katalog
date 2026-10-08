---
name: train-voice
description: |
  Use BEFORE any writing skill when user wants LinkedIn posts that sound
  like them rather than generic AI voice. Trigger phrases include "learn
  my voice," "train on my writing," "match my style," "make it sound
  like me," "here are my past posts," or when user uploads Shares.csv
  from LinkedIn data export. Also trigger proactively before first
  writing-skill use when voice-profile.md does not exist.
license: MIT
---

# Train voice

The most useful thing you can do for someone before they write a LinkedIn post is figure out how they actually sound. Every other AI tool skips this step and produces the same templated voice for everyone, which is exactly why LinkedIn is full of identical-sounding posts. This skill exists to fix that.

## Why this skill exists

LinkedIn's 2026 algorithm rewards content that holds attention. Generic-sounding content gets scrolled past. The fastest way to sound generic is to write in the average LinkedIn AI voice. The fastest way to sound like a real person is to write in the voice the user actually writes in.

Real voice is not "professional but approachable" or any other tone-deck label. It is concrete: sentence length, word choice, how the user opens and closes, whether they use semicolons, what they refuse to say, what they get excited about. The job here is to capture that from real samples and write it down so other skills can use it.

## When to use this skill

Trigger when:
- The user wants their posts to sound like them, not like a tool
- The user uploads samples of their writing (past posts, blog posts, emails they wrote, LinkedIn Shares.csv export)
- The user is about to use a writing skill for the first time and a voice profile does not exist yet
- The user says their current AI output "doesn't sound like me"

Do NOT trigger when:
- A voice-profile.md already exists and the user is not asking to update it
- The user explicitly says they want neutral, professional voice (some users do, especially for company-page posts)

## What you need from the user

Samples of their actual writing. In order of preference:

1. **LinkedIn data export (Shares.csv).** The cleanest source. Has every post they have ever written. The user gets this from LinkedIn Settings → Data Privacy → Get a copy of your data → Larger archive. Comes by email in 24-48 hours.
2. **Pasted samples.** 10-20 past LinkedIn posts pasted into chat. Less ideal because of effort, but workable.
3. **A blog, newsletter, or other writing.** If they have nothing on LinkedIn yet but have written elsewhere, this is fine. Note the channel difference in the profile (a blog reads differently from a LinkedIn post).
4. **Nothing yet.** Run the interview fallback (below).

Ask once: "Do you have past posts I can read, or a LinkedIn data export? Pasting 10-15 of your best past posts works too. If you have nothing yet, I can interview you instead." Do not loop on this. Pick the best source available and go.

## What to look for in the samples

Read the samples carefully. Look for these specific things, in this order:

**Sentence rhythm.** Average sentence length. Range from shortest to longest. Does the user mix short and long, or stay even? Do they use one-line sentences for emphasis?

**Opening patterns.** How do their posts start? Common types: a number, a question, a quote, a confession, a contrarian claim, a story setup, a definition. Note which the user actually uses.

**Closing patterns.** Some users close with a question. Some with a one-line summary. Some just stop. Some have a signature phrase. Note what they do.

**Word choice register.** Casual ("yeah," "weird," "stuff"), neutral, formal, technical. Most people mix. Note where they land and where they vary.

**Punctuation habits.** Em dashes, semicolons, parentheses, ellipses, all-caps, em-spaces, line breaks. Note what they use and what they avoid.

**Recurring phrases or verbal tics.** Things the user says often. "the thing is," "look," specific industry jargon, particular metaphors. These are voice fingerprints.

**What they refuse to do.** Look at what is NOT in the samples. No emojis? No hashtags? No "thoughts?" closer? No bold text? These are also voice signals.

**Topics and angles.** What do they write about, and at what angle? A founder writing about product, lessons learned, the team, hiring, mistakes. Note the recurring beats.

**Tells of their actual job/expertise.** The specific details that prove they know what they are talking about. Numbers, named tools, dates, customer types.

## What to write into voice-profile.md

A focused profile, not a dissertation. Save to `voice-profile.md` in the workspace root (or `~/.linkedin-maxxing/voice-profile.md` if a shared location is configured).

The file should contain:

```markdown
# Voice profile for [user's name if shared, otherwise "user"]

Generated [date] from [number of samples] samples of [source: LinkedIn posts / blog / interview / mixed].

## Sentence rhythm
[1-2 lines on length, mix, use of short sentences for emphasis]

## Opens
[2-4 specific opening patterns the user actually uses, with one real example each]

## Closes
[1-2 closing patterns, with example]

## Word choice
[register and notable habits, with examples of words the user uses and words they avoid]

## Punctuation
[what they use, what they avoid]

## Verbal tics and recurring phrases
[3-6 actual phrases from their writing]

## What they refuse to do
[bullet list of what is absent: emojis, hashtags, certain closers, etc.]

## Topics and angles
[3-5 recurring topic-and-angle pairs, with example post titles or one-liners]

## Tells of expertise
[2-4 things they reference that prove their domain knowledge]

## Things to NEVER do when writing in this voice
[hard nos: anything the user has explicitly said they hate, plus inferred patterns they avoid]

## Things to ALWAYS do
[2-3 things that are core to the voice, like "open with a number" or "end without a CTA"]
```

Length target: 200-400 words. Tight enough that downstream skills can read it quickly, specific enough to actually change output.

## Interview fallback (if no samples available)

If the user has no samples, run a short interview (4 questions, asked once):

1. Pick three LinkedIn posts (yours or someone else's) you wish you had written. What is it about them?
2. Pick three LinkedIn posts that make you cringe. What specifically bothers you?
3. When you write at work (a doc, an email, a Slack message), what is one thing about your style that comes up?
4. Are there any words, phrases, or styles you would never want in a post written for you? (emojis, hashtags, "thoughts?", em dashes, etc.)

From these answers, build a partial voice profile, marked at the top with "PROVISIONAL: built from preferences, not samples. Re-run train-voice with real samples when available."

## Output

Save the voice-profile.md to the workspace. Tell the user where it is and what it contains in 2-3 sentences. Show them the file path. Do not paste the whole file inline unless they ask.

End with: "Future writing skills will read this automatically. To update it, run train-voice again with new samples."

## How downstream skills use this file

Every writing skill in this repo (write-post, write-comment, write-longform, write-recommendation, write-hook, write-dm) is instructed to read voice-profile.md before drafting. If the file is missing, they fall back to asking one question about tone. If it is present, they match the voice patterns you wrote down.

This means the voice profile has real consequences. Be specific, not flowery. "Mixes short punchy sentences with longer ones, often opens with a number, never uses bullet points, signature closer is a question that sounds rhetorical but isn't" is useful. "Conversational and engaging" is not.

## What this skill does not do

- Invent a voice the user does not have. If the samples are thin or contradictory, say so. Mark the profile as provisional.
- Override the user's stated preferences. If they say "I never use hashtags" and one old post has a hashtag, trust the stated preference.
- Lock the user into one voice. People write differently for different topics. The profile captures their dominant patterns, not a single immutable style. Downstream skills should treat it as a strong default, not a rule.
- Score how "good" the user's voice is. The job is to capture it, not to judge it.

## Example

User uploads `Shares.csv` from LinkedIn data export with 47 past posts.

Skill reads them, then produces voice-profile.md that includes (truncated):

```markdown
## Sentence rhythm
Mostly medium sentences (15-25 words), with frequent one-line sentences for emphasis, usually after a longer setup. Average ~18 words. Rarely uses sentences longer than 35 words.

## Opens
- A specific number: "47% of our pipeline closes in the last 5 days of the quarter."
- A confession: "I shipped a feature this week I'm not sure about."
- A contrarian claim: "Most B2B PMs are wrong about onboarding."

## Closes
- Often ends with a question that is not rhetorical, like "What is your team doing differently?"
- Sometimes just stops after the strongest line.

## Verbal tics
- "Honestly" used twice per post on average, never as an opener (mid-sentence)
- "Worth knowing" as a transition into a point
- "Here is what I noticed" as a setup for a list
- Almost never uses "I think". Instead just states the claim
```

This file is now what every write-* skill reads before drafting a post.
