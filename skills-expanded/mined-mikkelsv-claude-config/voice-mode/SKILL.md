---
name: voice-mode
description: Install a voice-input behavioral contract for the rest of the conversation. Use when starting an extended voice-dictated session (e.g. big planning work). Parses rambly input for intent, stays active until "voice mode off" or /implement.
---

# Voice Mode

Installs a behavioral contract for handling voice-dictated input. Invoke at the start of an extended voice-input session — typically big planning work where you'll be dictating throughout.

## When invoked

User types `/voice-mode <opening statement>`. The opening statement is itself voice-dictated.

## What this skill does

Two things, then gets out of the way:

1. **Acknowledge mode is on** — one short line confirming voice mode is active and naming the exit conditions.
2. **Respond to the opening statement under the contract** — let content cues route to whatever workflow fits. If the dump describes feature work, `wf-always-plan` will fire `/plan` naturally. Do not hardcode plan invocation here.

## The voice-mode contract (active until exit)

Apply to every user turn for the rest of the conversation:

- **Parse for intent, not literal text.** Voice-to-text produces false starts, mid-sentence course corrections ("what I mean is..."), trailing-off rambles, and redundant restatements. Read past them — the signal is what the user *meant*, not what the transcript captured.
- **Treat filler as noise.** "Um", "uh", filler conjunctions, and self-corrections are transcription artifacts, not content.
- **When ambiguous, ask before acting.** If the dump could mean two different things, surface the fork instead of guessing. Voice input raises ambiguity rate — patience pays off.
- **Don't take literal commands at face value.** If literal text reads like a strict instruction but the surrounding ramble suggests broader intent, go with intent. Surface the interpretation when it might be wrong.
- **Don't drift back to default behavior.** Each subsequent turn is still voice-mode unless an exit fires. Re-read this contract if drift is suspected mid-conversation.

## Exits

Voice mode ends when:

- User says "voice mode off" (or equivalent — "I'm typing now", "stop voice mode").
- `/implement` is invoked. Implementation is action-heavy and less conversational; voice-mode posture is no longer load-bearing.

On exit, acknowledge once and revert to default behavior.

## Out of scope

- **Auto-detection.** Skill activates only via explicit `/voice-mode`. No watching prompts for voice-style cues.
- **Visible synthesis.** Don't restate the dump as "cleaned text" for confirmation — that adds friction `/plan`'s natural question loop already handles. Surface interpretation only when ambiguity is real.
- **Cross-session persistence.** Each session starts fresh; voice mode does not carry over.
