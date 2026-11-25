---
name: cold-outreach-sequencer
description: Turn a prospect dossier into a 3-touch outreach sequence — cold email, LinkedIn message, and follow-up — with personalization rules and anti-spam guardrails. Use when the user asks to "write outreach", "draft a cold email", "build a sequence", "follow up with this lead", or has a dossier and wants first contact. Always delivers drafts; never sends anything. Don't use for researching the prospect — run lead-research-dossier first.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Sales, Outreach, Copywriting]
    related_skills: [lead-research-dossier, pipeline-tracker, competitor-pricing-scan]
---

# Cold Outreach Sequencer

Converts a researched dossier into three short, personalized touches a busy prospect might actually answer. Hard rule: this skill produces **drafts only**. It never connects to an email account, never auto-sends, never schedules sends — the human presses every send button.

## When to Use

- User has a dossier (ideally from `lead-research-dossier`) and wants first-contact messaging.
- User wants a cold email, a LinkedIn touch, and a follow-up as one coherent sequence.
- User wants an existing cold draft tightened up against the guardrails below.
- **Not for:** researching the prospect — run `lead-research-dossier` first. Not for logging the touch — update `pipeline-tracker` after sending. Not for bulk spray-and-pray blasts: this skill personalizes one prospect at a time and will refuse mass-merge requests.

## Quick Reference

| Action | Command / Call |
|---|---|
| Input needed | Dossier: hooks, contact + role, ICP fit evidence, user's offer + proof point |
| Touch 1 | Cold email — ≤120 words, 1 hook, 1 low-friction CTA |
| Touch 2 (+2–3 days) | LinkedIn — ≤60 words, references a different hook, no link |
| Touch 3 (+4–5 days) | Follow-up email — ≤80 words, adds new value, clean break-up line |
| Personalization check | Hook passes "couldn't be sent to any other company" test |
| Spam check | See guardrails in step 5 |

## Procedure

1. **Precheck** — confirm you have: a dossier (or at minimum 2 verified personalization hooks), the contact's name + role, the user's offer in one sentence, and one proof point (metric, customer, result). Missing hooks? Stop and route to `lead-research-dossier` — outreach without research is spam.
2. **Frame the angle** — pick the single dossier signal that best connects prospect pain to the user's offer. One angle for the whole sequence; each touch expresses it differently.
3. **Draft Touch 1 (email)** — subject ≤5 words, lowercase-natural, no clickbait. Body: hook (1 sentence) → relevance bridge (1–2 sentences) → proof point → interest-based CTA ("worth a look?" not "grab 30 minutes on my calendar"). ≤120 words.
4. **Draft Touches 2 and 3** — LinkedIn touch uses a *different* hook, conversational, no links. Follow-up email adds something new (insight, resource, sharper question) — never "just bumping this". End touch 3 with a polite close-the-loop line.
5. **Guardrail pass** — enforce all of: no deception ("Re:" fakery, fake forwards, false familiarity), no fabricated claims or invented mutual connections, mention how you found them if natural, every email carries an opt-out line, no ALL-CAPS/spam-trigger phrasing ("act now", "guaranteed"), no more than 3 touches without a reply, and flag to the user that commercial email must comply with local law (CAN-SPAM/GDPR/PDPA — physical address + working unsubscribe on commercial sends).
6. **Deliver as drafts** — output the template. State plainly: "These are drafts. Review, personalize the bracketed bits if any, and send from your own client." If the user asks you to send automatically, decline and restate the drafts-only rule.
7. **Handoff** — remind the user to log the touch in `pipeline-tracker` (stage → Contacted, next_action → Touch 2 date).

## Output Template

```
# Outreach Sequence: <Contact> @ <Company>
Angle: <one sentence — the signal→offer connection>

## Touch 1 — Email (Day 0)
Subject: <≤5 words>
<body ≤120 words, ends with opt-out line>

## Touch 2 — LinkedIn (Day 2–3)
<≤60 words, no links>

## Touch 3 — Follow-up Email (Day 6–8)
Subject: Re: <touch 1 subject>
<body ≤80 words, new value + break-up line>

Send checklist: [ ] correct name/company  [ ] hooks still current  [ ] sent manually by you
```

## Pitfalls

- **Template smell** — if swapping the company name leaves the email intact, personalization failed. Recovery: rewrite the opening sentence around a hook that references something only this prospect did, dated within ~90 days.
- **Stale hook** — the "recent" funding round was 14 months ago; referencing it signals lazy research. Recovery: check hook dates in the dossier before drafting; if all hooks are old, refresh via `lead-research-dossier` first.
- **CTA too heavy** — asking a stranger for 30 minutes in touch 1 kills reply rates. Recovery: downgrade to an interest question; the meeting ask belongs in the reply thread, not the cold open.
- **User asks the agent to send** — tempting, out of bounds. Recovery: decline, explain the drafts-only guardrail (deliverability, consent, legal exposure), and hand over paste-ready drafts instead.

## Verification

- [ ] Exactly 3 touches, each within its word limit
- [ ] Each touch uses a hook; touches 1 and 2 use *different* hooks
- [ ] No fabricated claims, fake "Re:", or invented familiarity anywhere
- [ ] Emails include an opt-out line; compliance note surfaced to the user
- [ ] Delivered as drafts with an explicit "you send these manually" statement
- [ ] User pointed to `pipeline-tracker` for logging the touch
