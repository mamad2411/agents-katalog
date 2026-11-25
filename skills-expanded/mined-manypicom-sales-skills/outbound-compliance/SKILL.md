---
name: outbound-compliance
description: Understand and meet the legal requirements for cold B2B email — GDPR, CAN-SPAM, CASL, PECR and the bulk sender rules. Use whenever the user mentions GDPR, CAN-SPAM, CASL, PECR, ePrivacy, cold email legality, consent, legitimate interest, opt-out requirements, unsubscribe links, data protection, or asks whether cold emailing is legal. Also use before starting outbound into a new country.
---

# Outbound Compliance

Cold B2B email is legal in most of the world, with conditions that differ by jurisdiction. The conditions are not onerous and most of them describe what a decent sender would do anyway.

**This is a practical summary, not legal advice.** For a programme at any scale, or into a regulated sector, get a lawyer in the relevant jurisdiction to review it. What follows is enough to design the programme correctly and to know which questions to ask.

## The map

| Region | Law | B2B cold email | Requirements |
|---|---|---|---|
| **US** | CAN-SPAM | Legal, opt-out basis | Accurate headers, honest subject, physical address, working opt-out honoured within 10 days |
| **EU/EEA** | GDPR + ePrivacy | Generally legal B2B under legitimate interest, varies by member state | Lawful basis, transparency, right to object honoured immediately, records |
| **UK** | UK GDPR + PECR | Legal to corporate subscribers | Same as EU. PECR is lighter for corporate bodies than for individuals |
| **Canada** | CASL | Consent-based, strict | Express or implied consent, identification, opt-out. Significant penalties |
| **Australia** | Spam Act | Consent-based, inferred consent possible for business roles | Identify, opt-out, consent basis |
| **Germany** | GDPR + UWG | Restrictive in practice | Prior consent expected for email marketing. Take advice |

Two to be careful with: **Canada** is genuinely consent-based rather than opt-out, and enforcement is real. **Germany** is stricter than GDPR alone implies, and a common trap for people who assume "EU means legitimate interest".

## GDPR for B2B outbound

The persistent myth is that GDPR bans cold email. It doesn't. It requires a lawful basis and a set of obligations around it.

**Legitimate interest** is the usual basis for B2B outreach. To rely on it you need to be able to show three things, ideally written down before you start:

1. **The interest is legitimate.** Direct marketing is explicitly recognised as one in the recitals.
2. **Processing is necessary** for it. You can't reach a business decision-maker about a business product without contacting them.
3. **It's balanced** against the person's rights. This is the part that carries the weight.

The balancing test is where most programmes would fail if examined, and it's also a good design guide. It's satisfied by:

- **Genuine relevance.** The message relates to their professional role. Emailing a warehouse manager about enterprise sales software fails this immediately.
- **Role-based addresses**, not personal ones. `sarah@company.com` is a work address. `sarah.jones@gmail.com` used for work is much weaker ground.
- **Reasonable expectation.** Would a professional in this role be surprised to receive it? A relevant B2B pitch, no. Something unrelated to their job, yes.
- **Proportionate data.** Name, role, company, work email. Not their personal life.
- **Easy objection**, honoured immediately and permanently.

**Practical obligations:**

- **Say where you got their details** if asked. Answer honestly and specifically — "your details were on your company's team page" defuses the question; evasion turns it into a complaint.
- **A privacy notice** they can reach, explaining the processing and their rights.
- **Honour objections immediately.** Not within 30 days. Immediately, and permanently.
- **Honour access and erasure requests** within a month.
- **Keep a record** of your legitimate interest assessment. One page is enough, and having it is most of the value.

## The universal requirements

Whatever the jurisdiction, these are always required and always sensible:

- **Accurate sender identity.** Real name, real company, real domain. No spoofing.
- **Honest subject lines.** No "RE:" on a first email, no false claims.
- **A working opt-out**, honoured promptly and permanently.
- **A physical postal address** — required by CAN-SPAM and good practice everywhere. It can be in the signature.
- **No emailing anyone who has opted out.** Ever, from any campaign.

## The bulk sender rules

Separate from law, and enforced by the mailbox providers themselves. Google and Yahoo require, for meaningful volume:

- SPF and DKIM configured, with DMARC published
- Alignment between the From domain and the authenticated domain
- **One-click unsubscribe** via `List-Unsubscribe` and `List-Unsubscribe-Post` headers on bulk mail
- Spam complaint rate under 0.3%, ideally under 0.1%

Failing these means filtering, not a warning letter. See `spf-dkim-dmarc-setup`.

## The opt-out, practically

For cold B2B, a plain-text line works better than a marketing-style footer:

> Not the right person, or not interested? Reply "no" and I'll stop.

It's honest, low-friction, and it gives someone an alternative to the spam button — which matters, because a complaint costs the domain far more than an opt-out costs you.

Then actually stop. Suppress the address permanently, workspace-wide, across every campaign and every client. Re-enrolling someone who opted out is both a legal problem and the fastest way to generate a complaint. See `suppression-list-management`.

## Data sourcing and retention

Compliance exposure is created at list-build time, not at send time.

- **Don't buy lists.** You have no defensible basis for the data, you can't say where it came from, and it usually contains addresses gathered without any basis at all.
- **Record the source of every lead.** Which search, which site, which date. This is what turns "where did you get my details" from a problem into a sentence.
- **Collect only what you need.** Name, role, company, work email, and the researched business fact. Not personal information.
- **Delete what you don't use.** Indefinite retention of unworked prospect data is hard to justify.
- **Check the terms** of any source you scrape. Terms-of-service violations are a separate exposure from data protection, and it's the client's exposure, not the tool's. See `web-scraping-lead-data`.

## Agencies and processors

If you run outbound for clients, be clear about roles. Typically the client is the controller and you're the processor, which means a written data processing agreement, processing only on documented instructions, appropriate security, and clarity on what happens to the data at the end of the engagement.

Keep client data genuinely separated — separate lists, separate suppression lists, separate sending infrastructure. See `agency-multi-client-outbound`.

## Don't do these

- **Don't claim GDPR bans cold email**, and don't claim it doesn't apply to B2B. Both are wrong and both lead to bad decisions.
- **Don't buy lists.**
- **Don't hide the opt-out.**
- **Don't argue with an opt-out request.**
- **Don't email personal addresses** for business purposes.
- **Don't send into Canada or Germany** on the assumption that opt-out is enough.
- **Don't treat this page as legal advice.** Get a review for anything at scale.

## Related skills

`suppression-list-management`, `email-deliverability`, `reply-handling`, `lead-sourcing`, `crm-data-hygiene`, `agency-multi-client-outbound`, `web-scraping-lead-data`
