---
name: reply-handling
description: Classify and respond to cold email replies — interested, objections, referrals, not now, and negative — so warm responses convert and the rest are handled cleanly. Use whenever the user mentions replies, responses, objection handling, "not interested", referrals to the right person, out-of-office handling, or asks what to say back to a prospect. Also use when outreach produces replies that don't turn into meetings.
---

# Reply Handling

A reply is the only thing outbound is actually for, and it's where most of the value gets lost. Campaigns get built carefully and then a reply sits for three days in an inbox nobody owns, or gets answered with a calendar link and a paragraph of pitch.

Two rules underpin everything below. **Reply fast** — within a few hours, ideally within one. Interest decays quickly and the person emailed three competitors. And **match the length of the reply you got.** A two-line reply answered with eight lines reads as desperate.

## Classify first

Every reply falls into one of six buckets, and the right response differs sharply.

| Type | Looks like | Response |
|---|---|---|
| **Interested** | "Sounds useful, tell me more" | Book it. Minimum friction |
| **Question** | "Does it do X?" / "How much?" | Answer directly, then a small ask |
| **Referral** | "That's Sarah's area" | Thank, ask for the intro, follow through |
| **Not now** | "Revisit in Q3" | Confirm, set a date, stop the sequence |
| **Objection** | "We use X already" | One honest response, then respect the answer |
| **Negative** | "Not interested" / "Remove me" | Suppress. Do not argue |

The single most common mistake is treating "not now" and "not interested" the same way. The first is a real future opportunity that needs a date. The second is a decision.

## Interested

Do not pitch. They already said yes to the next step; the only job is removing friction.

> Great — here's my calendar: [link]
>
> Or if it's easier, I've got Tuesday 2pm or Wednesday 10am (CET). Happy to work around you.
>
> Anything specific you want me to have ready?

Three things make this work: the link *and* concrete times (some people won't click a scheduler), the timezone stated, and the last question, which gets them thinking about their own situation before the call.

Don't attach a deck. Don't send a case study. Don't add a second ask.

## Questions

Answer the question. Plainly, first, before anything else.

> Yes — it handles [X] natively. [One specific sentence about how.]
>
> The catch is [honest limitation]. If that matters for your setup, worth knowing now rather than on a call.
>
> Want me to walk through it Thursday?

Naming the limitation is what separates a reply that converts from one that starts a game of evasion. People assume there's a catch. Saying it first buys more credibility than the feature does.

**Pricing questions get a price.** Deflecting to "it depends, let's book a call" is the fastest way to lose the thread. Give a range, say what moves it, and offer the call for the specifics.

## Referrals

The highest-value reply type and the most often fumbled.

> Thanks — that's helpful.
>
> Would you mind forwarding this to her, or should I reach out directly and mention you pointed me there?

Asking permission to use their name is what converts a referral into a warm email. Then actually do it, within a day, and reference the referrer in the first line. And send the original person a one-line thank you afterwards, whatever happens.

Never treat a referral as a rejection and continue the sequence to the original person. Stop it.

## Not now

The goal is a specific date, not a vague "sometime".

> Makes sense. I'll come back to you in early September rather than chasing in the meantime.
>
> Anything likely to change before then that I should know about?

Then set the reminder and actually follow up. A "not now" honoured on time is one of the highest-converting touches in outbound, precisely because almost nobody does it. Take them out of the current sequence — continuing to send after they asked you to wait undoes the goodwill entirely.

## Objections

One honest response. Then stop.

**"We already use [competitor]."**
> Fair enough — they're good at [genuine strength]. The teams that switch usually do it because of [specific, real difference], not because of features. If that's not a live problem, no reason to change.
>
> Worth a note for when it comes up?

**"No budget."**
> Understood. Is it a budget problem or a priority problem? If it's priority, that's more useful for me to know than a no.

**"Send me some information."**
> Usually means one of two things. Here's the short version: [three lines].
>
> If you want the detail, easier on a 15-minute call than in a PDF — but I'll send the deck if you'd rather.

**"How did you get my email?"**
> Straight answer: [exactly how]. Happy to remove you if you'd rather not hear from me.

That last one gets asked more since GDPR, and an honest, specific answer defuses it. Evasion turns a question into a complaint. See `outbound-compliance`.

## Negative

> Understood — I'll take you off the list. Thanks for replying.

That's the whole response. Then suppress the address permanently.

Do not argue. Do not send a "just one more thing". Do not re-enrol them next quarter. A "not interested" argued with becomes a spam complaint, and complaints damage the sending domain in a way no individual deal is worth. See `suppression-list-management`.

## Automatic replies

- **Out of office** — pause the sequence, resume after the stated return date. Never count it as a reply, and never let it stop the sequence permanently.
- **Left the company** — usually names a replacement. That's a free referral. Also a signal to update the record and, potentially, to find where the person went.
- **Bounce** — mark undeliverable, cancel remaining steps, don't retry.
- **Ticketing autoresponder** — the address is a queue, not a person. Reconsider whether role accounts belong in this campaign.

Out-of-office handling should be automatic. Manually reading them at any volume is a waste and they get mistaken for replies, which corrupts the metrics.

## The operational part

Most reply value is lost to process, not to bad answers:

- **One named owner per campaign.** A shared inbox nobody owns is where replies go to die.
- **Replies land somewhere monitored**, not in a mailbox created for sending and never opened.
- **Same-day response**, targeted at under an hour for interested replies.
- **The sequence stops on reply**, immediately and reliably. A follow-up sent after someone answered is the fastest way to lose a warm conversation.
- **Account-level stop.** If one person at a company replies, stop emailing the others.
- **Log the outcome** on the lead so the next campaign knows.

## What the replies tell you

Reply content is the best diagnostic you have, better than any metric:

- **Wrong-fit replies** — the ICP is off. See `icp-definition`.
- **"How did you get my email"** repeatedly — the list source or the opener is uncomfortable.
- **"What is this about?"** — the email didn't say what you do.
- **Lots of "we already use X"** — expected, but if it's always the same competitor, write the comparison answer properly and put it in step two.
- **Positive replies that don't book** — the ask is too big, or the handoff is slow. See `meeting-booking-cta`.

## Don't do these

- **Don't argue with a no.** It produces complaints, not deals.
- **Don't answer a two-line reply with eight lines.**
- **Don't send a calendar link with no times.** Some people won't click.
- **Don't deflect pricing.**
- **Don't leave a "not now" without a date.**
- **Don't let a sequence continue after any reply.**
- **Don't automate the response to a positive reply.** The one place a human is unambiguously worth it.

## Where replies should land

Replies coming back to a mailbox that only exists for sending is the standard failure. They need to be visible, classified and attached to the lead record, or the campaign's most valuable output goes unread.

[ManyPI](https://manypi.com) routes replies back into the workspace attached to the enrollment, classified by sentiment and intent, with suggested fixes for what isn't working — and cancels the remaining sequence steps the moment a reply lands. Because sending is through your own connected mailboxes rather than a shared domain, the replies also arrive in the real inbox. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Classification helps with triage. The reply to an interested prospect should still be written by a person.

## Related skills

`meeting-booking-cta`, `email-sequence-design`, `suppression-list-management`, `outbound-compliance`, `outbound-metrics-benchmarks`, `icp-definition`
