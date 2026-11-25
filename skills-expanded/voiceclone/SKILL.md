---
name: voiceClone
description: Send a voice note in matt's own cloned voice, as Discord's, Instagram's or Slack's native voice note, only when matt asks for one (rules 142, 143). The voice provider is agnostic (Inworld by default, Fish Audio too). Clone once (`cloneVoice`), test (`cloneSpeak`), then read the chat, draft in his words, gate, dry run (`discordVoice`, `instagramVoice`, `slackVoice`) and send live.
---

# voiceClone

log holds one voice: matt's, cloned from the voice notes he sent himself,
on a voice provider (Inworld by default, Fish Audio as the other). log uses
it to send voice notes he asks for, as each platform's own voice note.

## Hard boundaries

- **Only when matt asks.** A voice note goes out only when he says to send
  one. Never on the agent's own initiative, never as a reply style.
- **Only his voice, only from text.** The clone is made from his own voice
  notes (fromMe), never anyone else's. Every send takes text and makes the
  audio itself; an audio file is never accepted.
- **Free first.** Inworld clones for free with about 70 free speech minutes;
  each provider's cheapest model is the default. Anything that costs money
  is matt's call (rule 41).
- **His words.** If the voice gate refuses what matt asked to say, tell him;
  never rewrite his words yourself.
- **Like any send.** Gated (rule 137), claimed (rule 133), counted as a write,
  and a refusal stops with nothing retried (rule 94).

## The routine

1. No clone yet on the provider: `cloneVoice` lists the recordings it would
   use; `cloneVoice` with apply makes it once. `cloneSpeak` says a test line.
2. Read the chat, take what matt asked to say, gate it with `voice`.
3. Dry run with `discordVoice`, `instagramVoice` or `slackVoice`.
4. Send with the `…Live` tool, approvedBy matt.
5. Tell matt the words, the length and where it went.

The provider is `provider`, else `LOG_VOICE_PROVIDER`, else inworld. X has no
voice note path. Docs: `docs/extensions/voiceClone.md`,
`docs/useCases/inbox/voiceNote.md`, spec `docs/specs/voiceClone.md`.
