---
name: linkedin-voice-profiler
description: Read the user's real past posts and DMs and build a compact voice ruleset so every other skill writes like them. Use once at setup, or again when the writing starts to drift.
argument-hint: "[paste of 5-15 real posts/DMs, or a path to them]"
---

# LinkedIn Voice Profiler

Every skill in this engine writes in the user's voice. This skill builds that voice profile from their real words, not a guessed persona, so the rest of the motion sounds like them and not like generic AI.

## Inputs
- A paste of 5 to 15 of the user's real posts and DMs, or a path to a file holding them: $ARGUMENTS
- The brief loads automatically. This skill writes the "## Voice profile" block back into it.

## Do this
Read only the supplied samples. Extract, from the real text:
1. Sentence rhythm. Short and punchy, long and rolling, or mixed. Note typical length and how lines break.
2. Favourite verbs and recurring phrases. The words they reach for again and again.
3. Contraction habits ("do not" vs "don't"), emoji habits (which, how often, or never), and swearing tolerance.
4. Opening patterns and closing patterns. How they hook a post and how they sign off a DM.
5. Register tiers. If the samples show it, separate the cold-outreach voice from the warm, replying-to-a-peer voice.
6. Banned tells. The phrases and tics they never use, so other skills avoid them.
Then compress all of it into a DO list, a DON'T list, and 3 verbatim sample lines lifted straight from the input.

## Output
A ready-to-paste "## Voice profile" block for linkedin-brief.md: the DO list, the DON'T list, the cold-vs-warm register notes if found, and the 3 verbatim sample lines. End with a one-line note: paste this into linkedin-brief.md and the SessionStart hook will load it into every session after that, so /linkedin-humanizer and the copywriting skills write in this voice automatically.

## Rules
- Build the profile from the user's REAL words only. Never invent a persona or borrow a style they did not write.
- If fewer than 5 usable samples are supplied, say so and ask for more rather than guessing.
- Capture register tiers (cold vs warm) only if the samples actually show two registers. Do not fabricate a second voice.
- Quote sample lines verbatim. Do not polish or rewrite them.
- No em-dashes.
