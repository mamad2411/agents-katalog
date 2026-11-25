---
name: yt-voice
description: >-
  Build or refresh an optional creator voice profile from their own
  transcripts and stated audience, vocabulary, and format preferences. Use for "set up
  my voice", "write my voice.md", "make the scripts sound like me", "my
  scripts don't sound like me", or first-time setup of the YouTube pack.
---

# yt-voice

Read the [shared operating guide](../yt/references/operating-guide.md) for profile lookup, helper paths,
capability limits, and cross-skill routing before using this workflow.

Build a reusable voice profile from how the creator actually talks. Other skills can use it when
available, but do not require it before doing useful work. Save to the user's chosen location, or
`<workspace>/.youtube-agent/voice.md` in a local workspace. In ChatGPT, return the profile as a
file or reusable text for the user to attach to their Project or later conversations.

A tool lives here and it runs. It measures the things you cannot hear about yourself.

```bash
python3 "$YT_SKILL_DIR/voiceprint.py" best-video.txt second.srt third.txt
```

## The move

1. **Get three transcripts** of the creator's own best-performing videos - the words they actually
   said, not their scripts. Pasted, `.srt`, `.vtt`, or ask them to export captions from Studio. If
   they have none (new channel), fall back to the interview below.
2. **Run `voiceprint.py`** across all of them. It returns mean sentence length, filler rate, the
   signature words they lean on, and the hype words they already use. These are measurements, not
   grades - a long sentence is not worse than a short one, it is just a thing the scripts must respect.
3. **Fill the six sections** of [the voice template](assets/voice.md) from the measurements plus a short interview:
   - *Who I am talking to* - one named person, not "creators".
   - *How I actually talk* - from the mean sentence length and signature words.
   - *Words I never use* - the hype words to ban (the creator chooses from the ones voiceprint found).
   - *Words I do use* - the signature words. Keep them; they are what makes a script sound like them.
   - *What I will not claim* - numbers, results, tools they have not got. The skills refuse these.
   - *My format* - length, on-camera or not, intro or not, whether they swear.
4. **Write the profile** to the requested path, or `.youtube-agent/voice.md` in the workspace.
   Preserve an existing profile's useful details and incorporate the requested updates. In ChatGPT,
   provide the file or text. Mark inferred audience/tone details so the creator can correct them.

## New channel, no transcripts

Interview instead: who is the one viewer, three phrases that are theirs, three words that are not,
their format. Thinner than a voiceprint, but enough to start - and refresh it from real transcripts
after three uploads.

## What to hand back

- the saved or attachable voice profile, with its actual location if written
- the voiceprint measurements that informed it
- one line: the one section to tighten after their next three videos
