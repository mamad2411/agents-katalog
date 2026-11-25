---
name: write-as-friend
description: "Draft casual messages — Discord, Slack, text, informal email — in the user's own voice, as plain text with no markdown."
disable-model-invocation: true
---

# Write as Friend

Casual counterpart to [`write-as-human`](../write-as-human/SKILL.md). Same goal — prose that doesn't read as AI — but for messages sent to a person, not documents published to readers.

**Read `write-as-human` first.** Every tell in it still applies. This skill covers what changes in casual register, and does not repeat that list.

Usage: `/write-as-friend [medium] <what to say>` — e.g. `/write-as-friend discord tell manuel the notes feature is in staging`.

## What changes

Formal AI writing gets caught on ornate vocabulary. Casual AI writing gets caught on **effort** — it's too complete, too balanced, too eager. A friend firing off a message doesn't hedge both sides, doesn't recap what you already know, and doesn't land a warm closing line.

| Casual AI tell | What a person does |
|---|---|
| "Hey! Just wanted to reach out about..." | Says the thing. "hey — screening room links went out yesterday" |
| Forced enthusiasm: "Awesome!", "Love this!", "Super excited" | Neutral by default. Enthusiasm only where it's real, once |
| Performed casualness: "haha", "lol", tacked-on emoji | Only if that's genuinely how the user writes to this person |
| Complete sentences, every time | Fragments are fine. "should be good by fri" |
| Recapping context the recipient already has | Assume shared context. They were there |
| Balanced both-sides hedging | Pick a side. It's a message, not a memo |
| A closing line that wraps things up | Just stop. Or "lmk" |
| Em dashes and semicolons | Comma, period, or a new line |

## Mechanics

- **Plain text only.** No markdown. No `**bold**`, no `#` headings, no `-` bullet lists in prose. If something genuinely needs a list, use plain lines or "1." "2.".
- **Loose capitalization is fine** — lowercase sentence starts, lowercase "i". Match how the user writes. Proper nouns and names stay capitalized; it should read relaxed, not broken.
- **No hard line wrapping.** One line per paragraph. Break only where a break is meant. Line breaks get mangled when pasted anywhere else.
- **Contractions always.** "it's", "won't", "I'd".
- **Short.** A casual message that runs long stops being casual. If it needs to be long, it's an email — say so.

## Medium

The optional first argument tunes format. **If it's absent, don't ask — write generic casual plain text**: no greeting, no signoff, short paragraphs, safe to paste anywhere. Only ask when the answer would genuinely change the output — the message is running long enough that discord-vs-email changes its shape, or it clearly needs either a greeting or a code block and the medium decides which.

**discord / slack** — Short. Blank lines instead of paragraphs. Code goes in a fenced block (the one markdown exception; both render it). Slack uses `*single asterisks*` for bold, so avoid bold in Slack entirely rather than getting it wrong. No greeting, no signoff. Long content gets split at a natural break, and you say where the split is.

**text / sms / imessage** — Shortest. One thought. No greeting, no signoff, no links unless asked. If it takes more than about three lines, suggest a call instead.

**email** — Informal but still email. A greeting ("Hey Nicole,"), real paragraphs, and a signoff ("Thanks," / "— Tyler"). Subject line offered separately, not inside the body. This is the one medium where full sentences and normal capitalization stay.

**dm / other** — Treat as Discord unless the user says otherwise.

## Output

Print it in the reply as a fenced block the user can copy in one tap, including from a phone. Write to a file only when the user asks for one.

Either way, output the message and nothing else. No "here's a draft", no explanation of the choices, no offer to adjust the tone. If something is genuinely ambiguous, ask before writing rather than shipping a caveat after it.

## Common mistakes

- **Applying the formal register in lowercase.** Same sentence shapes, different capitalization, still reads as AI.
- **Blocking on the medium question.** No medium given means generic casual, not an interrogation.
- **Over-friendly opener.** "Hope you're doing well!" is the loudest tell in the list.
- **Explaining the message after writing it.** Send the message.
- **Markdown leaking in.** Bullets and bold are the giveaway that a machine wrote it.
- **Using the medium's slang because it's that medium.** Discord doesn't require "gg".
