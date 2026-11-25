---
name: cold-email-copywriting
description: Write cold emails that get replies — structure, first lines, specificity, length and the CTA. Use whenever the user asks for a cold email, outreach email, sales email, prospecting email, email template, or wants an existing email reviewed, rewritten or critiqued. Also use when reply rates are low, when emails are being ignored, or when someone asks why their outreach isn't working.
---

# Cold Email Copywriting

A cold email is an interruption. The recipient didn't ask for it, owes you nothing, and decides in about three seconds whether to keep reading. Everything below follows from that.

The bar is not "is this a good email". It's **would this specific person, reading this on a phone between meetings, think it was worth the interruption?**

## What good looks like

```
Subject: [3-5 words, lowercase, specific, no pitch]

[First line: something true about them that took effort to find.
Not their name. Not their company name. A fact.]

[The connection: why that fact means this email is relevant.
One or two sentences.]

[What you do, in their language, in one sentence. Ideally with
a number attached to a result for someone like them.]

[The ask: small, specific, easy to answer.]

[Name]
```

Under 100 words. Under 75 is better. On a phone that's a screen and a half, and anything longer gets deferred, which means never.

## The first line

The most important sentence, and the one where almost every cold email fails.

**Doesn't work:** "Hi {{first_name}}, I hope this email finds you well." "I came across {{company}} and was impressed." "As the {{title}} at {{company}}, you probably..."

All three are visibly automated. The merge fields prove a machine wrote it, and "I was impressed by your company" is what you write when you haven't looked at it.

**Works:** something specific and recent that required looking.

> Saw you're hiring two SDRs in Munich — that's the third sales role this quarter.

> Your changelog says you shipped the Zapier integration last month. Most teams do that when customers start asking for automation they can't build.

> You've got 340 reviews on Capterra averaging 4.6, and about a dozen of the recent ones mention onboarding taking longer than expected.

Each proves a human looked, and each sets up the email's actual point. That's what makes it worth reading rather than a compliment.

## Specificity is the whole technique

Vague sentences read as mass mail regardless of merge fields. Specific ones read as personal even when the structure is templated.

| Vague | Specific |
|---|---|
| "helps companies grow" | "gets reply rates from 1% to 4% on cold email" |
| "many of our clients" | "three agencies your size" |
| "significant improvement" | "cut their bounce rate from 8% to under 1%" |
| "I'd love to connect" | "worth 15 minutes on Thursday?" |
| "leading provider of" | delete this sentence entirely |

The rule: if a sentence could appear in a competitor's email with the product name swapped, it's saying nothing. Cut it or make it specific.

## The ask

Make it small. The email's job is a reply, not a sale.

**Too big:** "Book a 30-minute demo." You're asking a stranger for half an hour based on 80 words.

**Better:** "Worth a look?" — "Want me to send the 3-line version?" — "Is this something you own, or should I be talking to someone else?"

That last one is unusually effective. It's easy to answer, it's genuinely useful to you either way, and it doesn't ask them to buy anything. See `meeting-booking-cta`.

One ask per email. Two questions get zero answers.

## Length

Every sentence has to earn its place. The cuts that almost always help:

- The opening pleasantry
- Your company's founding story
- The feature list
- The second and third value propositions
- Anything explaining why you're emailing them, if the first line already did
- "Let me know if you'd like to learn more"

Write it, then cut a third. The cut version almost always performs better.

## Formatting

- **Plain text.** No images, no HTML templates, no logo, no signature graphic. Those look like marketing and are filtered like marketing.
- **No links in the first email**, or one at most. Links suppress deliverability and give a reason not to reply. See `spam-filter-triggers`.
- **Short paragraphs**, one to two sentences.
- **No bold, no colour, no fonts.** It should look like an email a person typed.
- **A plain signature.** Name, role, company. Not a vCard, not a banner, not four social icons.
- **Sentence-case subject lines**, or lowercase. Title Case reads as a newsletter.

## Subject lines

Three to five words. The job is to get the email opened without misleading anyone about what's inside.

Works: `quick question`, `{{company}} + {{your company}}`, `your Capterra reviews`, `SDR hiring`, `re: outbound`

Doesn't: anything with an exclamation mark, anything promising a percentage increase, "RE:" or "FW:" on an email that isn't one, all caps, emoji, and anything that reads like a subject line a marketer wrote.

Detail in `subject-line-optimization`.

## The tone problem

Most cold email is written in a register nobody uses in speech. Read every line aloud. If you wouldn't say it to someone across a table, rewrite it.

Signals of the wrong register: no contractions, "leverage", "solutions", "reach out", "circle back", "touch base", "in today's landscape", "I wanted to reach out because", "at the end of the day", and any sentence beginning "As a {{title}}".

Signals of the right one: contractions, short sentences, one clear point, a question a human would ask.

## What not to claim

- **Don't invent a mutual connection.** It gets checked.
- **Don't fake a previous conversation.** "Following up on my last email" when there wasn't one is a lie people notice and remember.
- **Don't invent case studies or numbers.** Use real ones or none.
- **Don't imply they signed up for something.**
- **Don't use false urgency.** "Only two spots left" from a stranger is transparent.

Beyond being wrong, all of these are found out quickly, and the person who catches you tells other people.

## Reviewing an email

Run these in order:

1. **Would a stranger think this was worth the interruption?** If no, nothing else matters.
2. **Is the first line specific to them**, and did it take effort?
3. **Could this exact email be sent to 500 other companies?** If yes, it will perform like it.
4. **Is it under 100 words?**
5. **Is there exactly one ask, and is it small?**
6. **Read aloud — does it sound like speech?**
7. **Is every claim true and substantiated?**
8. **On a phone, is it one screen?**

## Where the personalisation comes from

The first line is the whole email, and it requires a real fact about that company. Finding one per lead is where cold email either becomes work or becomes generic.

The scalable version is to research the fact at list-build time rather than at writing time. See `personalization-at-scale`.

[ManyPI](https://manypi.com) supports this directly: `extra_columns` on a lead search researches whatever you specify per lead — the tool they use, the product line they sell, what their reviews complain about — and stores it as a custom field you merge into the first line. Its `draft_email` tool also has your brand's positioning and personas as context, so the pitch half doesn't have to be retyped per message. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

A generated email that reads like a generated email is worse than no email, because it burns the prospect permanently. Whatever drafts it, the specificity test above is the bar.

## Related skills

`personalization-at-scale`, `subject-line-optimization`, `email-sequence-design`, `meeting-booking-cta`, `spam-filter-triggers`, `reply-handling`
