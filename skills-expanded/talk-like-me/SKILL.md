---
name: talk-like-me
description: >-
  Learn the user's own writing voice from how they actually talk to you, and
  write their user-facing copy in that voice instead of a generic one. Use this
  WHENEVER you produce text meant to sound like the user: website and landing
  page copy, bios, taglines, social posts, emails, READMEs, or any "write this
  for me" task in their name. Build a voice profile from the conversation history
  (vocabulary, sentence length, formality, humor, directness, language mix,
  punctuation habits), save it to your memory so you do not re-analyze every
  session, reuse it, and update it only when the user's style genuinely shifts or
  they ask you to. This shapes the user's content, not how you narrate your own
  work.
---

# Talk like me

Generic copy reads as nobody's. When you write a homepage or a bio for a user, it
should sound like them: the words they reach for, how long their sentences run,
how formal or blunt they are, whether they joke, whether they mix languages. You
already have a large sample of exactly that, the conversation itself. This skill
turns that sample into a reusable voice, applies it to the user's content, and
saves it so you are not re-deriving the person every time.

The rule: when you write something that goes out in the user's name, match the
user's voice, not the default assistant voice. Learn it once, persist it, reuse
it.

## Build the voice profile

Read how the user actually writes to you and capture the patterns, not the topics:

- **Vocabulary and register:** plain or technical, casual or formal, the specific
  words and phrases they repeat.
- **Sentence shape:** short and clipped, or long and winding. Do they fragment for
  effect? Start with "and"/"but"?
- **Tone:** warm, dry, blunt, playful, earnest, self-deprecating, confident.
- **Directness:** do they get straight to the point, or build up to it? How do
  they give an opinion or push back?
- **Humor and personality:** sarcasm, understatement, enthusiasm, swearing, emoji
  habits (and which ones).
- **Language:** if they mix languages (for example Turkish and English), where and
  how. Keep their actual code-switching pattern.
- **Punctuation and rhythm:** lowercase starts, ellipses, exclamation use, how
  they break up thoughts.

Write the profile as concrete, usable guidance ("short declarative sentences,
dry humor, starts replies with the conclusion, mixes Turkish and English, rarely
uses exclamation marks"), not vague adjectives.

## Save it to memory

Do not re-analyze the whole history on every request. The first time you build the
profile, save it to your persistent memory as a single voice profile for this
user. On later tasks, recall that profile and use it directly.

- Keep one profile per user, updated in place. Do not scatter duplicates.
- Store it as concrete style rules plus a couple of short real examples of the
  user's phrasing, so future-you can match it without re-reading everything.
- If your environment has no persistent memory, keep the profile in the working
  context and rebuild it only when it is actually missing.

## Apply it

When writing the user's content, run it through the profile: would the user have
phrased it this way? Adjust word choice, sentence length, and tone to match. The
goal is that a person who knows the user would believe they wrote it.

This covers their outward content: site copy, bios, posts, emails, docs in their
voice. It does not mean you adopt their voice when you explain your own work or
report what you did; that stays clear and direct.

## When to update

Persist, do not churn. Update the saved profile only when:

- the user's style has genuinely shifted over time (not a one-off message in a
  different mood), or
- the user explicitly tells you to change how they sound, or corrects a draft in a
  way that reveals the profile was wrong.

A single off-tone message is not a reason to rewrite the profile. Real, repeated
drift is. When you do update, edit the existing profile rather than adding a
second one, and note what changed.

## A note on the other skills

The user's authentic voice wins for their own content. If they genuinely write a
certain way, honor it. But the default AI tells they do not actually use still get
cleaned: pair this with `no-em-dashes`, `no-fancy-ascii`, `no-filler-phrases`, and
`no-ai-signoffs` unless the user's real voice clearly includes one of those.

## Before you deliver

Read the draft as if you were the user seeing their own site copy. Does it sound
like them, or like a generic brand voice? Fix the lines that ring false. If this is
the first time, make sure the profile is saved to memory; if the user's style has
clearly moved, update the saved profile in place.
