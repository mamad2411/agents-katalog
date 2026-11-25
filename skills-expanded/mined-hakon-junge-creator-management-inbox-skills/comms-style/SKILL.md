---
name: comms-style
description: >
  Wording rules for creator emails in the user's own voice (their voice.md plus house
  style). Use whenever the inbox drafts a creator email, or for "reply to this
  creator", "counter this rate", "how should I say this to them". Wording only:
  strategy comes from negotiation-playbook, facts from company-context.
---

# Comms style: sound like the user

The bar: the user would send it without changing a word, and the creator can't tell it
wasn't typed by hand.

## Load order (every drafting session)

1. `inbox profile-dir` -> the active profile folder.
2. **`voice.md`**: `~/.claude/voice/voice.md` (`$VOICE_HOME`) if Your Voice built one, else
   the profile's; updates go there too. It wins every wording question (register,
   openers, emoji, the "never" list), over the mechanics below.
3. **`settings.md`**: house-style switches (em dashes, banned words, exclamation marks).
   `inbox draft` also enforces them in code, but write them right the first time.

**No voice yet** (`voice.md` still mostly `TODO`)? Write in the neutral default below and
tell the user once per session: "Drafts sound generic until you build your voice - say
'build my voice', about 10 minutes." `references/example-voice.md` is a complete fictional
profile, the model answer for `voice.md`: never imitate it as the user's voice or borrow
its name, title or backstory.

**Identity is not tone.** Whoever runs the workflow signs as themselves: identity from the
connected mailbox and `me.md`, tone from `voice.md`.

## Shared creator-email mechanics

- **Greeting register:** fuller for substantive, negotiation and difficult emails; lighter
  for quick, warm replies. Mirror the sender's energy and their noun (*budget* -> budget,
  *rate* -> rate).
- **Acknowledge first, then move:** before a counter or a decline, credit what the creator
  did well or got right - it makes a firm position land as fair.
- **Every ask carries an exit:** a low-pressure close, so they can say no without it
  costing the relationship.
- **Calls:** never propose one, logistics included, unless the thread makes it genuinely
  logical; accept warmly when the creator asks in a live conversation. A decline stays in
  writing - a call offered with a no reads as a consolation prize.
- **Links, two kinds:** something to click (form, brief, walkthrough, calendar, page) =
  descriptive words hyperlinked; something to copy (a join or tracking link, a promo URL,
  anything for a video description) = a bare URL on its own line. A reply that asks them
  to do a thing carries that thing's link, even if an earlier email had it - never "the
  link in my last email".
- **One currency, stated inline:** the profile's `{{CURRENCY}}`, unit next to the number
  ("900 USD per video"); a creator negotiating in another currency gets theirs mirrored.
- **Product words:** the exact terms in `company.md` ("always say" / "never say", the
  exact name of any unit the product counts in); never a generic synonym for a named
  thing.
- **We-framing on agreed numbers:** "the total we had in mind", never "you had in mind" -
  a shared agreement, not a conceded demand. Copy stays evergreen: never reference an
  expired offer.
- **One person on the thread:** finance or another team is looped in internally, never
  CC'd onto the creator email.

## Neutral default voice

- Clear, warm, brief. One idea per paragraph. Plain words.
- "Hi [Name]," to open; no "Hope you're doing well".
- Specific thanks rather than generic praise.
- No exclamation marks unless the creator uses them heavily; no emoji.
- Close with a simple forward-looking line; the email signature carries the name.
- No em dashes; a spaced hyphen instead.

## Other channels

Chat: short, line breaks, a decision stated with a recommendation. Internal docs: outcome
first, then context, then numbered points. LinkedIn or social posts: `voice.md` covers
them only if the sent-mail sample included posts; otherwise the email register, and say
the post voice is unverified.
