---
name: sr-voice
description: Captures how a creator actually writes and talks so every later draft sounds like them and not like a generic assistant. Use at the start of any content project, when drafts feel off or too polished, when someone says "make it sound like me", or before writing captions, scripts or posts for someone. Takes three to five real samples, extracts rhythm, vocabulary, humour, language mix and banned phrases, and saves short voice notes. Works in any language, including Hinglish and mixed-script text.
license: MIT
compatibility: Any agent that loads Agent Skills. Optional Python 3.9+ for the style check; works by hand without it.
metadata:
  author: Raj Bharti
  version: "0.1.2"
  family: showrunner
---

# Voice: sound like the person

Audiences forgive rough edges and punish sameness. This skill makes sure the draft is in the creator's voice before anyone polishes it.

## Get samples

Ask for three to five things the creator wrote or said without help from an AI: messages to friends, old posts, a voice note transcript, an email that went well, a talk. Different moods are better than five of the same. If they only have AI-assisted text, ask them to talk for two minutes about their topic and paste the transcript.

## Read them for

- **Rhythm.** Average sentence length, how often they use one-word sentences, fragments, questions.
- **Openers.** How they start a thought ("Look,", "So,", "Okay here's the thing").
- **Vocabulary.** Words they reach for, words they never use, jargon level, swearing level.
- **Language mix.** Whether they switch between languages, which one carries emotion, which one carries facts. Keep the mix. Do not translate it away.
- **Humour.** Dry, self-teasing, absurd, none. Match it or leave it out.
- **Stance.** Do they hedge ("I think", "maybe") or commit? Confident or humble?
- **Signature moves.** A phrase, a sign-off, a way of counting things.
- **What they never do.** No emojis, no exclamation marks, no hashtags, no hype.

## Write the voice notes

200 words at most. Concrete, with two or three real lines from the samples as examples. Format:

```
VOICE NOTES for [name]
Sounds like: [one sentence]
Rhythm: [short / mixed / long]; [fragments yes/no]
Language: [what, and how it mixes]
Humour: [kind]
Stance: [commits / hedges]
Always: [moves]
Never: [moves]
Real lines to imitate:
- "[from the samples]"
- "[from the samples]"
Banned phrases: [list]
```

Seed **banned phrases** with the creator's own dislikes plus the stock phrases in `sr-humanize` that they would never say. Save the list in `profile.voice.banned_phrases` (`profile_save`). The humanizer reads it.

## Check the voice

Write a 60-word paragraph on one of their topics using the notes. Ask: "Would you say this? What is the one word that is not you?" Adjust the notes with their answer. Two rounds is usually enough.

## Gate

`approve`. They confirm the notes sound like them before any drafting begins.

## Do not

- Flatten dialect, slang or code-switching into standard English.
- Invent anecdotes to make the voice "warmer". Ask for a real one.
- Quote the samples back in a way that exposes private details. Keep examples to what they are happy to publish.
