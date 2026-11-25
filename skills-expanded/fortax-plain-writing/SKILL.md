---
name: fortax-plain-writing
description: Make a client mail, notice reply, deadline reminder or WhatsApp message read like the firm wrote it, not like an AI drafted it - removes the tells (not-X-but-Y, triads, inflated words, staged openers, bold labels, leftovers) without changing a single figure, date, section or condition. Run it on anything before it leaves the office. Typical asks - "isko natural bana do", "AI jaisa lag raha hai, theek karo", "mail ko thoda simple karo", "reply ki language tight karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "Tell list adapted from blader/humanizer, https://github.com/blader/humanizer (MIT), which builds on Wikipedia's Signs of AI writing"
---

# Plain writing

## Why this matters here

A client can tell when a mail was machine-written, and so can an officer reading a reply to a
notice. Both then trust the content less. The firm's name is on it, so it has to sound like the firm.

Run this on any text that leaves the office: client mails, deadline reminders, document requests,
notice replies, WhatsApp updates, cover letters on a filing.

## The one rule that outranks style

**Rewriting never changes a fact.** Every figure, date, section, form number, ARN, name and qualifier
survives untouched. You may cut a sentence that says nothing, merge paragraphs, or change the order.
You may not add a claim, soften a caveat, or drop a condition to make a line read better. If a
sentence needs a detail you do not have, write a shorter sentence or ask the CA. This sits above
everything below.

## Match the register before you edit

Read the firm's own past letters first — whatever the CA points you to, a firm templates folder, or
the client's `Correspondence/` folder (`fortax-client-folder`). That is the voice. Where the firm
writes plainly, write plainly; where it writes formally, stay formal.

Three registers, and they are not the same:

| Going to | Register |
|---|---|
| A client, routine | Warm, direct, short. Hinglish is fine if the firm already writes that way |
| A department, in reply to a notice | Formal, impersonal, point-wise against the notice's own paragraph numbers. Do not "simplify" this into casual prose |
| WhatsApp | One idea, one message, no formatting, no attachments described in prose |

Formality is not an AI tell. Padding is.

## The tells to remove

Act on any one of these on sight.

**Not X but Y.** "It is not just a delay, it is a compliance risk." The negative half names something
nobody claimed so the positive half sounds bigger. State the point: "A delay here attracts a late
fee."

**The closing line that repeats the paragraph.** "That is the real risk here." "Please note the
above." If it adds nothing, cut it. A short sentence earns its place by carrying a new fact.

**Triads by habit.** "Accurate, timely and compliant." Three items because three sounds complete, not
because there are three things. Say the one that matters.

**Inflation.** "Critical", "seamless", "robust", "ensure", "leverage", "delve", "landscape",
"navigate the complexities". A due date is a due date.

**Staged openers.** "In today's regulatory environment…", "As you may be aware…". Start with the
thing. "Your GSTR-3B for August is due."

**Bold on every label.** One or two bolds in a mail, on the figure or the date that must not be
missed. Not on every line's first two words.

**Dashes doing a comma's job.** Indian professional writing rarely uses them. Use a comma, a full
stop, or two sentences.

**Leftovers.** "Certainly!", "Here is the draft", "I hope this helps", "Let me know if you need
anything else" when the CA did not ask for it. Also any placeholder you left: `[insert amount]`, `XX`,
`TBD`. A placeholder in a mail that goes out is a failure.

**Apologising by default.** "Sorry for the inconvenience" on a routine reminder. Say it when the firm
actually caused something.

## How to work

1. Read the draft once and mark every tell.
2. Rewrite whole sentences rather than patching phrases. A patched sentence still reads patched.
3. Vary the length. Real writing alternates short and long; AI writing runs at one pace.
4. **The added-fact gate. Do this literally, not from memory.** List every concrete noun in your
   rewrite: each form name, period, amount, date, client name, ARN. For each one, point at where it
   appears in the original draft. Anything you cannot point at, delete.
   This is the failure this skill exists to prevent. A vague draft that said "the relevant documents"
   must not come back as "the GSTR-3B working paper for August 2026" — you do not know that, and a
   client who receives the wrong period stops trusting the firm. When the original is vague, the
   rewrite stays vague, or you ask the CA which return it is.
5. Check nothing was lost either: every figure, condition and caveat from the original is still
   there, and no placeholder survived.
6. Then search once more for the five that survive most rewrites: a not-X-but-Y, a repeating closer,
   a dash, a triad, a bold label.

## What good looks like

Before:

> In today's dynamic regulatory landscape, it is not just important but absolutely critical to
> ensure that your GST compliance obligations are met in a timely and accurate manner. Please find
> attached the relevant documents. Let me know if you need anything else.

After:

> The documents are attached. Please review them and tell us if anything needs changing.

Shorter, and it says what the client has to do. Note what it does **not** say: the original never
named a return or a period, so neither does the rewrite. If the CA wants the specifics in there, they
tell you what they are.

With the facts supplied, the same mail becomes:

> Your GSTR-3B for August 2026 is due on the 20th. We have the sales register but not the purchase
> invoices for the month. Please send those and we will file on time.
>
> The working paper is attached.

## Where this does not apply

Statutory text quoted in a reply stays exactly as it is. A section, a notification's wording, a
judgment's ratio, a portal's own error message: quote them verbatim, and never rewrite them for
readability.

## Output

The rewritten text, one line naming what you changed at the shape level, and one line reading
`Facts added: none` — or, if the draft was too vague to rewrite honestly, the question you need
answered instead of a rewrite. Then the CA reads it and sends it themselves; see
`fortax-client-comms`. Nothing leaves the office from you.

## Attribution

The tell list is adapted from [humanizer](https://github.com/blader/humanizer) (MIT; licence in
`LICENSE-THIRD-PARTY-humanizer.txt`), which builds on Wikipedia's "Signs of AI writing", and is
rewritten here for Indian professional correspondence.
