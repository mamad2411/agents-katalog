---
name: cold-email-agency
description: Write B2B cold emails and 4-step follow-up sequences that sell AI/automation services to US SMBs. Use when the user asks for cold outreach, a prospecting sequence, or reply-rate fixes.
---

# Cold Email for AI Agencies

Goal: get a *reply*, not a sale. One email = one idea = one ask.

## Inputs (ask if missing)
1. ICP: industry, company size, role (e.g. "owner of a 5-20 person HVAC company in Texas").
2. The ONE pain you solve in their words (missed calls, slow quotes, no follow-up, manual data entry).
3. Proof: a number, a case, or a demo (if none, use a free audit/teardown as proof).
4. The ask: low-friction (a 2-min Loom, "worth a look?", a free audit), never "book a 30-min call" on email 1.

## Rules
- 50-90 words. Subject 2-4 words, lowercase, no clickbait ("missed calls", "quick idea for [company]").
- First line is about THEM (a trigger: hiring post, reviews, site speed, ad they run). Never "I hope this finds you well".
- No AI buzzwords above the fold for non-tech buyers: say "answers every call in 2 rings", not "AI voice agent".
- One CTA, phrased as a yes/no question.
- Plain text, no images, no tracking pixels on step 1 (deliverability).
- Personalization variables: `[first_name]`, `[company]`, `[trigger]`, `[city]`.

## Sequence (default)
| Step | Day | Angle |
|---|---|---|
| 1 | 0 | Trigger + pain + soft ask |
| 2 | 3 | Proof: mini case or number |
| 3 | 7 | Give value: 1 specific fix they can do without you |
| 4 | 12 | Breakup: "should I close the loop?" |

## Output format
For each step: subject, body, and 2 A/B variants of the first line. Then a checklist: SPF/DKIM/DMARC, warmed inbox, <40 sends/inbox/day, separate sending domain.

## Example (step 1)
Subject: missed calls
> Hi [first_name] — saw [company] has 140+ Google reviews but the phone went to voicemail when I called at 6pm. For HVAC that's usually a $400+ job going to the next listing. We set up a system that answers and books those calls automatically. Worth a 2-min video showing how it'd work for you?
