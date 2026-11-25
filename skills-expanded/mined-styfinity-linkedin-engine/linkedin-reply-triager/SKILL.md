---
name: linkedin-reply-triager
description: Classify every inbound LinkedIn reply and route it to the right next move. Use when replies land in the inbox and you need to decide who is hot, who needs nurture, and who to drop.
argument-hint: "[one reply or a batch of replies pasted in]"
---

# LinkedIn Reply Triager

The inbox sorter. Replies are not equal. This skill reads each one, names what bucket it belongs in, and hands it to the right next skill so nothing rots and nothing gets a sales pitch it did not ask for.

## Inputs
- One reply or a batch of replies, pasted in (include who said what if it is a thread): $ARGUMENTS
- The brief (persona, offer, pains) loads automatically.

## Do this
For each reply, in order:
1. Read the actual words, not the timing. A reply that came in slow can still be HOT; a fast one can be a brush-off.
2. Classify into exactly one bucket: HOT, WARM, COLD, OBJECTION, WRONG-PERSON, or HOSTILE.
3. Name the tell. Quote the one phrase or signal that put it in that bucket. One line.
4. Route it:
   - HOT (buying signal, asking how it works, wants a call) to /linkedin-sell-by-chat, or /linkedin-booking-closer if they are ready for a time.
   - WARM (interested but not now, soft yes, "keep me posted") to /linkedin-followup-adapter.
   - COLD (one-word, flat, polite-but-dead) to /linkedin-cold-reviver.
   - OBJECTION (price, timing, trust, "already have someone") to /linkedin-objection-handler.
   - WRONG-PERSON (not their call, not their remit) ask for the right contact, warmly.
   - HOSTILE (annoyed, "stop messaging me") stop the sequence, no further outreach.
5. Write a one-line suggested next message in the operator's voice.

## Output
Per reply: the class, the tell (quoted), the route (the slash-skill or the action), and a one-line suggested next message. Label each clearly. Batch input gets one block per reply.

## Rules
- Route every reply. No reply is left unclassified.
- Read the words, not a timer. The bucket comes from what they said.
- Nothing sends here. This skill only sorts and suggests; the routed skill drafts, the operator approves.
- No em-dashes. Use a comma, a period, or " - ".
