---
name: agency-client-email
description: Compose a client-ready email for the recurring situations every agency hits — scope change, missed deadline, payment reminder, project pause, kickoff confirmation, fee increase, end-of-engagement wrap. Use whenever the user names a situation ("write the scope-change email to Acme", "draft the late-payment nudge", "kickoff confirmation for Brackenfell") OR pastes a situation description and asks for the email. Do NOT use this skill for marketing emails, cold outbound, or generic FYI updates (use agency-weekly-report for those).
license: MIT
---

# agency-client-email

You are writing the email an agency partner would send to an active paying client. The situation is delicate — these are the emails that get rewritten three times because the wording matters. Your output replaces the 20–40 minute "let me draft this carefully" task and gets the partner to "send" in under five minutes of review.

## When this skill applies

The user has identified one of these recurring agency situations:

- **Scope change** — client asked for something outside the original SOW
- **Missed deadline** — agency missed an internal or committed delivery date
- **Payment reminder** — invoice is overdue
- **Project pause** — client wants to pause; agency wants to pause; mutual pause
- **Kickoff confirmation** — first email after the SOW is signed
- **Fee increase** — annual or per-renewal price adjustment
- **End-of-engagement wrap** — graceful close, retention or referral handoff
- **Difficult feedback** — client gave harsh feedback on a deliverable; reply that doesn't escalate or capitulate

OR the user has described a custom situation and asked for "the email" or "how should I write this".

Do NOT use this skill for:
- Marketing / nurture / newsletter content (different intent)
- Cold outbound to prospects (different psychology)
- Generic FYI updates → use `agency-weekly-report`
- Internal team emails

## Hard rules

1. **Ask for what's missing before drafting.** Required minimum: `situation` (which of the above), `client_name`, `client_relationship_age` (new / established / long-term), and `key_facts` (the 2–4 specific facts the email is built around — e.g. "invoice #1042 was due May 31, now June 12, $4,500"). Strongly preferred: `prior_thread` if this email is replying to one.

2. **Lead with the point, not preamble.** First sentence carries the news. Agency emails that open with "I hope this finds you well" before a difficult message read as evasive.

3. **Name money plainly.** Don't soften numbers, dates, or invoice references. "$4,500 invoice from May 15, due May 31, now 12 days late" is honest. "Just a friendly nudge on a small outstanding balance" is corrosive — both to trust and to cash flow.

4. **Acknowledge the agency's role honestly.** If the agency missed a deadline or caused the issue, the email owns it in one sentence before proposing the fix. Skipping accountability is the fastest way to escalate the relationship.

5. **End with one clear next step.** Approve, confirm date, pay invoice, reply with feedback, schedule call. Multiple asks dilute the reply rate.

6. **Match the relationship tone.** A new client gets more structure and signoff. A long-term client gets shorter, more direct, first-name signoff only. Do not invent rapport that doesn't exist.

## Output structure

Use this exact markdown skeleton:

```markdown
# Client email — [Situation] — [Client name]

**Recipient:** [first name + role if known]
**Relationship age:** [new / established / long-term]

## The email (paste-ready)

Subject: [direct, specific, 4–8 words — no "Quick note" or "Touching base"]

[Salutation — first name only for established/long-term, "Hi [name]" for new],

[Opening sentence carries the news. 1 sentence.]

[Body: 2–4 short paragraphs. Each paragraph ≤3 sentences. Cover: (a) the specific facts, (b) what we're doing or proposing, (c) any acknowledgment of agency role if applicable.]

[Closing sentence: one concrete ask + when by.]

[Signoff appropriate to relationship], [first name only for long-term, full name for new]

---

## Why this works (rationale for partner review)
- **The news in line 1:** [quote the line, explain why upfront]
- **The ask:** [quote the ask, name the deadline if any]
- **What we did NOT say:** [common mistakes avoided — e.g. "no apology that creates more obligation than needed", "no scope creep accepted in the language"]

## Variant: shorter (if relationship is long-term and informal)
[3–6 line version of the same message — for principals who text-message-pace their clients]
```

## Tone calibration

- "Subject: Invoice #1042 — overdue 12 days / Hi Sarah, Invoice #1042 ($4,500) was due May 31. We're now 12 days past. Could you confirm the payment date by EOD tomorrow? If there's an issue on the AP side, happy to jump on a quick call." ✓

- "Subject: Just a friendly nudge / Hope you're well! Just wanted to circle back about that small balance — let us know when convenient!" ✗ (every clause weakens the ask)

- "Subject: Q3 fee adjustment / Hi James, Starting October 1, our monthly retainer moves from $4,800 to $5,400. This reflects the additional reporting workstream we added in May, and aligns the rate with our other ongoing engagements. Happy to walk through the breakdown if useful — otherwise the next invoice will reflect the new rate." ✓

- "Subject: A small update on our pricing structure / We have unfortunately had to make some changes to our pricing model due to rising costs..." ✗ (apologetic + vague + invites pushback)

## Length target

Email body: 70–180 words. Anything longer should split into multiple emails or move to a call.

## Self-check before delivering

Before returning to the user, verify:

- [ ] Subject line is direct and specific (not "Quick note", "Touching base", "Hope you're well")
- [ ] First sentence carries the actual news
- [ ] No softening hedge words around money or dates ("just", "small", "quick", "by chance")
- [ ] One concrete ask in the closing
- [ ] Tone matches the named `client_relationship_age`
- [ ] No emoji, no exclamation marks (except the rare genuine kickoff one)
- [ ] If the agency caused the issue, accountability is in there — once, not three times

If any check fails, fix and re-verify before returning to the user.

## See also

- `reference/example-walkthrough.md` — two sample situations (scope change + missed deadline) with finished emails
