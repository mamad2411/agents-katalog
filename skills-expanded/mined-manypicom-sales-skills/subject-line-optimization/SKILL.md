---
name: subject-line-optimization
description: Write and test cold email subject lines that get opened without misleading the recipient. Use whenever the user mentions subject lines, open rates, email headlines, preview text, preheaders, or wants subject lines written or reviewed. Also use when open rates are low, or when someone wants to A/B test the opener of a cold email.
---

# Subject Lines

A subject line has one job: get the email opened by someone who might genuinely care. Getting it opened by everyone is easy and worthless — a misleading subject produces an open, a moment of irritation, and sometimes a spam complaint.

Manage expectations before starting. **Subject lines are the least consequential variable in cold outbound**, well behind audience, offer and first line. They're the most tested because they're the easiest to test. If reply rates are the problem, the subject line is rarely the cause.

## What works

**Short.** Three to five words. Mobile clients truncate around 35 to 40 characters, and most cold email is first seen on a phone.

**Lowercase or sentence case.** Title Case reads as a newsletter. `quick question` looks like a person typed it; `Quick Question About Your Sales Process` looks like a campaign.

**Specific to them.** The strongest subject lines reference the thing the email is actually about.

```
your Capterra reviews
SDR hiring
the Munich office
{{company}} + {{our company}}
question about your API docs
```

**Curiosity without a trick.** A subject that makes someone want to know more, and then the email delivers on it.

**Plain.** No punctuation marks, no emoji, no brackets, no "RE:" on a first email.

## What doesn't

| Avoid | Why |
|---|---|
| `Quick Question!!!` | Exclamation marks read as promotional |
| `RE: our conversation` | A lie, on a first email. People notice |
| `🚀 Boost your revenue 300%` | Emoji plus a number plus a claim |
| `Following up on my previous email` | Only valid if there was one |
| `[Company Name] - Partnership Opportunity` | Brackets and title case, reads as bulk |
| `Are you the right person to speak to about...` | Long, and answers itself |
| `Free trial for {{company}}` | "Free" plus an offer, in a subject, from a stranger |

The pattern in all of them: they read as something a marketer wrote to a list, and that's exactly what a filter and a recipient are both trying to detect.

## Merge fields in subject lines

Use them sparingly and always with a fallback.

`{{first_name}}, quick question` becomes `, quick question` when the field is empty, which is both embarrassing and a strong bulk-mail signal. Set the fallback and test-render on 20 real leads before launching.

`{{company}}` is generally safer than `{{first_name}}` — company names are more reliably present and less likely to be malformed — but it also reads more like a mail merge. A specific fact usually beats either.

## Matching the subject to the email

The subject sets an expectation. The first line has to meet it, or the open is wasted and the reader learns to skip your next one.

```
Subject: SDR hiring
First line: Saw you're hiring two SDRs in Munich — third sales role this quarter.
```

That works because it's continuous. Someone who opened because of the subject immediately sees why they were emailed.

```
Subject: quick question
First line: I hope this email finds you well. I wanted to reach out because...
```

That doesn't. The subject promised a question and the email opens with filler.

## Preview text

The first line of the email shows next to the subject in most clients, effectively doubling the subject's length. Almost nobody uses it deliberately.

Because the first line of a good cold email is already the specific observation, this usually takes care of itself — as long as the email doesn't open with "Hi {{first_name}}," on its own line, which wastes the preview on a greeting.

Some clients let you set a hidden preheader. For plain-text cold email, don't bother. The first line is better used as the actual first line.

## Follow-up subjects

For step two, threading onto the original email is usually right. It gives context and looks like a normal follow-up rather than a new campaign.

For steps three and four, a fresh subject gives a second chance at the open, particularly if the first was ignored rather than rejected.

What not to do: `Re: Re: Re: quick question`, or a subject that guilts. `Did you see my email?` reads as entitled, and the honest answer is usually "yes, and I didn't reply".

## Testing

If you're going to test, do it properly or don't do it.

- **One variable.** Subject only, everything else identical.
- **Several hundred sends per variant.** At 100 each, a 48% versus 52% result is noise.
- **Split randomly**, not by list order — list order correlates with source, region and company size.
- **Measure replies, not just opens.** A subject that lifts opens and drops replies attracted the wrong people.
- **Run it once and move on.** Subject-line testing has a low ceiling.

And accept the measurement problem: **open tracking is unreliable.** Apple Mail Privacy Protection pre-fetches images and inflates opens; image blocking suppresses them. Directional over time, not accurate in absolute terms. This is the main reason not to over-invest in subject-line optimisation — you can't measure it well.

## When low open rates aren't a subject line problem

An open rate under about 25% on a cold list usually means filtering, not a weak subject. Check in this order:

1. **Authentication** — SPF, DKIM, DMARC passing. See `spf-dkim-dmarc-setup`
2. **Domain reputation and warmup** — see `email-warmup`
3. **List quality** — bounces, wrong-fit, stale addresses
4. **Content triggers** — links, images, attachments. See `spam-filter-triggers`
5. **Then** the subject line

A sudden drop from 50% to 15% with no content change is a deliverability event, not a copy problem. Rewriting subject lines in response wastes a week.

## Twenty that work

```
quick question                    {{company}} + {{us}}
your Capterra reviews             SDR hiring
the Munich office                 your API docs
question about {{company}}        outbound
re: your changelog                idea for {{company}}
worth 10 minutes?                 the checkout flow
your job post                     two SDRs
wrong person?                     {{company}}'s onboarding
one thing                         about your pricing page
saw your Series A                 not sure if you own this
```

Most are short, specific and unremarkable. That's the point — they look like internal email, which is the register you want.

## Don't do these

- **Don't mislead.** An open you tricked someone into is worse than no open.
- **Don't use "RE:" or "FW:"** on a first email.
- **Don't put a claim or a percentage in the subject.**
- **Don't use emoji** in B2B cold outbound.
- **Don't write a subject longer than the phone will show.**
- **Don't optimise subject lines** when reply rate is the problem.
- **Don't trust open-rate differences** on small samples.

## Related skills

`cold-email-copywriting`, `email-sequence-design`, `spam-filter-triggers`, `outbound-metrics-benchmarks`, `email-deliverability`
