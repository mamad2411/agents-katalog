---
name: cold-email-20-videos
description: Write and review cold emails using what the 20 most-watched cold email videos of 2026 actually agree on, weighted by how many of them repeat each rule, and flag the choices they disagree on so you A/B test those instead of trusting one guru. Trigger on "write a cold email", "review my cold email", "cold email sequence", or /cold-email.
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /cold-email

Built from the transcripts of the 20 most-watched cold email videos published between March and September 2026 (203,575 views, 97,000 words). 422 pieces of advice were extracted, 392 were kept because their exact quote was found in the transcript, and they were grouped into 156 distinct rules. The number next to each rule is how many of the 20 videos say it. Sources are in `sources.md`.

No rule was repeated by more than 9 of the 20. Treat the weights as odds, not laws.

## Inputs

1. What you sell, in one sentence.
2. Who you are writing to: role, company, and one real detail about them (something they posted, launched, hired for, or complained about).
3. What you can give for free that is genuinely useful to them.

If input 2 has no real detail, stop and ask for one. A fake detail is worse than none.

## The rules, by weight

### Strong (6 to 9 of 20)

- **Lead with something free and useful, not a call ask.** (9/20) A tailored idea, a short list, a first piece of the work done. Not a PDF, not "hop on a call".
- **Personalize with one real, researched detail.** (8/20) If it could be sent to 1,000 people, rewrite it.
- **Keep it short.** (7/20) Around 50 to 80 words for the first email. Each sentence earns the next.
- **Test copy and offers continuously.** (7/20) Never judge the channel on one variant.
- **Follow up several times, a few days apart.** (6/20) Most say 2 to 5 follow-ups.

### Solid (4 to 5 of 20)

- **Verify every email before it goes out.** (5/20)
- **End with a soft question**, like "worth a look?" (5/20)
- **Segment by role and company type**, one message per segment. (5/20)
- **Subject lines short, casual, lowercase feel.** "quick question, {first name}". (5/20)
- **Recontact non-responders later with a new angle**, not the same email. (5/20)
- **First email in plain text, no links.** (4/20)
- **Show one proof point**: a result, a known customer. (4/20)
- **Target a real signal**: hiring, funding, new leader, expansion. (4/20)
- **Do not pitch or ask to close in email one.** (4/20)
- **Reply to interested people within minutes.** (4/20)

### Mentioned (3 of 20)

Simple words, no jargon · build copy from phrases your buyers used on calls · small specific lists beat huge generic ones · never send from your main domain.

## Where the experts disagree: do not pick, test

When a draft touches one of these, write **two versions** and label them A and B.

| Choice | Side A | Side B |
|---|---|---|
| Calendar link | Include a link or time slots to cut friction | Never put a calendar link in a cold email |
| Follow-ups | 2 to 5 short bumps | One follow-up only, framed as a new offer |
| Personalization depth | Deep, researched, company-specific | Light: over-personalizing email one backfires |
| CTA | Soft question | Specific, easy call ask |
| Volume | Start small and precise | Send far more than you think |

## Steps

1. Read the three inputs. Refuse to invent the personal detail.
2. Draft email one applying every Strong rule, then the Solid ones that fit.
3. Count the words. Over 90, cut.
4. Check it against the list: free value first, one real detail, no link, soft question, no pitch.
5. If a choice from the disagreement table applies, output version A and version B.
6. Draft follow-ups only if asked, each with a new angle.
7. Under the email, list which rules you applied, with their weight, and which choice is being A/B tested.

## Never

- Never claim a reply rate. None of these numbers are yours until you send.
- Never invent a mutual connection, a compliment, or a detail about the prospect.
- Never write "I hope this finds you well".
