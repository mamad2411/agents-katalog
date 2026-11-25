---
name: voice-builder
description: >
  Builds or updates the voice (voice.md) the inbox drafts use, from sent emails and a
  short interview. Use during inbox setup or when inbox drafts sound generic. With the
  Your Voice plugin installed, hand off to your-voice-builder: one voice for both.
---

# Voice builder

**Your Voice installed?** Use its `your-voice-builder` instead and stop: one voice for
every tool, which `comms-style` reads first. Else the goal is a `voice.md` they send
unedited; the model answer is `../comms-style/references/example-voice.md` (fictional).

Time budget: about 10 minutes of the user's time. Do the heavy lifting yourself.

## Step 1 - Gather their real writing

Run `inbox profile-dir` to find the profile folder, then:

- **Gmail connected** (`provider: gmail`): `inbox sent-samples --max 40`. Their own
  emails from the last 180 days, quotes stripped. Prefer creator and partner
  threads; skip internal one-liners and auto-replies.
- **Demo mode or not connected yet**: ask them to paste 5-10 emails they wrote
  (creator emails if possible - a negotiation, a piece of feedback, a decline,
  a quick reply). Pasted text is enough.
- **Nothing to sample** (brand new to email outreach): skip to Step 2 and build
  from the interview alone; mark the profile "interview-based, refine after 20
  sent emails".

Treat samples as private. You may quote the user's own sentences into `voice.md`,
but replace other people's names with `[Name]` and deal figures with `[fee]` or
`[views]`. Never copy samples anywhere else.

## Step 2 - The interview (short, plain questions)

Ask in small groups, offering options where you can (use the question tool if
available). Skip anything the samples already answer clearly - say what you
noticed instead and ask them to confirm.

1. "Three words you'd want a creator to use to describe your emails?"
2. "How do you usually open an email to a creator?" (show two openers you found)
3. "Emoji: never, rarely at the end, or freely? Which ones?"
4. "Exclamation marks: fine, or avoid?"
5. "Any words or phrases you never want in your emails?" (examples: "honestly",
   "per my last email", "circle back", em dashes)
6. "When you say no to a creator, what matters most to you?"
7. "When you negotiate, do you show how you got to a number?"
8. "How do you sign off?"

Answers to 3-5 also go into `settings.md`:
- em dashes off -> `em_dashes: replace`
- words to ban -> `banned_words: word=replacement, ...` (suggest a replacement for each,
  e.g. honestly=genuinely: announcing honesty implies the rest was optional)
- avoid exclamation marks -> `exclamation_marks: avoid`

Edit only inside the ```settings block. Tell them what you changed.

## Step 3 - Analyse, then write voice.md

Work through the samples section by section, the way the example voice is laid out:

| Section | What to extract |
|---|---|
| Core voice | 4-7 traits, each with the reason it works and a short real example |
| Openers and greetings | first-email, reply and quick-ack patterns, with examples |
| Email shapes | their actual structure for: first reply to an interested creator, content feedback, a rate conversation, a decline, a wrap-up |
| Formatting | dashes, bullets, bold, paragraph length, emoji (which, where, how often), exclamation marks, link style, P.S. |
| Sign-offs | how they close; whether they type their name |
| Negotiation voice | how they present numbers, concede, hold, exit |
| Your phrases | 5-15 lines they really use, quoted |
| Never | words, openers, habits absent from or rejected in their writing |

Rules for a profile that actually works:
- **Evidence over adjectives.** "Warm" is useless alone. "Warm through word choice -
  'really', 'love' - not emoji" is usable. Every trait gets an example.
- **Frequencies, not absolutes, where true.** "About one email in four ends with an
  emoji" beats "uses emoji".
- **Contradictions are information.** If they write differently to new creators than to
  long-time partners, record both.
- **Their words, not yours.** Don't upgrade their phrasing into polished copy.
- Keep it under ~1,200 words. A bloated profile makes drafts generic, not specific.

Write the result to `voice.md` in their profile folder (replace the template). Title
line: `# Voice profile: <their name>`.

## Step 4 - Prove it

Draft three short replies in the new voice, as text in the chat (don't save drafts):
use three emails from the active demo (`inbox unread`: a money ask, a content review, a
date) or three real unread threads if they prefer. Ask: "Would you send
these as they are? What would you change?"

Fold every correction back into `voice.md` - as a principle ("never opens with
'Thanks for reaching out'"), not as a one-off note. Repeat until they'd send the
drafts unchanged, usually one or two rounds.

## Updating an existing voice

- "Update my voice" / "my drafts keep saying X": read `voice.md`, make the smallest
  change that fixes it, and show the diff.
- After a few inbox runs, `inbox score` shows how often drafts were sent unedited and
  what changed when they weren't. Two or more edits pointing the same way = propose a
  voice.md change, and apply it only when the user agrees.
- Keep the profile tight: fold new rules into existing sections; don't append a log.
