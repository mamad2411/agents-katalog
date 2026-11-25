---
name: proposal-builder
description: Turns a lead dossier into a one-page client proposal with scope, three anchored pricing options, timeline, and a single next step. Use when the user says "write a proposal", "send them a quote", "put together an offer", "proposal for this lead", or has a qualified lead ready to price. Don't use for researching the lead itself — use lead-research-dossier — or for billing after a yes — use invoice-runner.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Sales, Proposals, Pricing]
    related_skills: [lead-research-dossier, cold-outreach-sequencer, pipeline-tracker, invoice-runner]
---

# Proposal Builder

Converts a lead dossier into a proposal a busy buyer can say yes to in one read: tight scope, three pricing options anchored high, a believable timeline, and exactly one next step. The standard: one page, zero filler, every line traceable to something the dossier actually says. This skill produces **drafts only** — the user reviews and sends every proposal themselves.

## When to Use

- A lead is qualified (dossier or call notes exist) and the user wants to price the work.
- User asks to "write a proposal", "quote this", "make an offer doc".
- Repricing or re-scoping an existing proposal after client feedback.
- **Not for:** researching the prospect — use `lead-research-dossier`. Not for first-touch outreach — use `cold-outreach-sequencer`. Not for invoicing a signed client — use `invoice-runner`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Find the dossier | `ls` the leads folder, then `read_file` the dossier for this lead |
| Today's date for the header | `date "+%B %d, %Y"` |
| Word-count the draft (one page ≈ ≤450 words) | `python3 -c "print(len(open('proposal-draft.md').read().split()))"` |
| Save the draft | write `proposal-<client>-<YYYY-MM-DD>.md` next to the dossier |
| Log it in the pipeline | hand off to `pipeline-tracker` with stage = "Proposal sent" once the user actually sends |

## Procedure

1. **Precheck** — locate the lead dossier or call notes and `read_file` them. No dossier means no proposal: ask for the source material or point the user to `lead-research-dossier` and stop. Never invent the client's problem.
2. **Extract the pain** — pull from the dossier: the client's stated problem, what it costs them (time or money), who decides, and any budget signal. Write these as 3–4 bullets and confirm with the user before pricing.
3. **Scope** — define deliverables as outcomes, not activities ("a booked-calls pipeline", not "10 hours of consulting"). 3–5 bullets max, plus one explicit "not included" line to prevent scope creep.
4. **Price three options, anchor high** — present in this order: **Premium first** (everything plus speed or done-for-you), **Standard** (the one you expect them to pick), **Starter** (smallest honest version). Premium should be 2.5–4x Starter. Name each option after the outcome, never "Bronze/Silver/Gold". If the user has no price instincts, propose numbers from the dossier's budget signals and get an explicit OK.
5. **Timeline + next step** — realistic dates from `date`, padded ~20% for review cycles. End with exactly ONE call to action ("Reply 'Option 2' and I'll send the invoice and kickoff link") — a proposal with three CTAs gets zero replies.
6. **Assemble and trim** — fill the template, run the word-count check, cut until ≤450 words. Every sentence must survive the question "does this help them decide?"
7. **Deliver as draft (send-gate)** — save the file and show it to the user. This skill never emails, DMs, or otherwise sends the proposal. Explicitly say: "Draft only — review the numbers, then send it yourself." After the user confirms it went out, update `pipeline-tracker`.

## Output Template

```
# Proposal: {Outcome headline} — {Client}
{Date} · Prepared by {User/Company} · Valid 14 days

## The problem
{2–3 sentences in the client's own words, from the dossier.}

## What we'll do
- {Deliverable as outcome}
- {Deliverable}
- {Deliverable}
Not included: {one line}.

## Options
**1. {Premium name}** — {what's added} — **${X,XXX}**
**2. {Standard name}** — {core scope above} — **${X,XXX}**  ← most clients pick this
**3. {Starter name}** — {smallest honest version} — **${XXX}**

## Timeline
Kickoff within {N} days of go-ahead · {Milestone} by {date} · Done by {date}

## Next step
{One sentence, one action.}
```

## Pitfalls

- **Proposal written from imagination, not the dossier** — the client reads generic pain points and bounces. Recovery: re-open the dossier, quote their actual words in "The problem", and delete any claim you can't trace to a source line.
- **Options priced too close together** (e.g., $900 / $1,000 / $1,100) — the anchor does nothing. Recovery: respread so Premium is 2.5–4x Starter and Standard sits where you actually want them to land.
- **Scope creep baked in** — vague verbs like "support" or "ongoing help" become unpaid work. Recovery: rewrite each deliverable with a countable noun and add the "Not included" line before the user sends.
- **Two pages of throat-clearing** — buyers skim. Recovery: run the word-count command; if over 450, cut the company backstory first — it's about them, not you.
- **Agent sends the proposal itself** — never. Recovery: if you're about to attach or send, stop; the rail is drafts-only, the user sends.

## Verification

- [ ] Output matches the template and is ≤450 words (checked with the python3 word count)
- [ ] "The problem" section quotes or paraphrases the dossier — nothing invented
- [ ] Three options present, premium-first, spread ≥2.5x, user approved the numbers
- [ ] Exactly one next-step CTA
- [ ] File saved as a draft; nothing was sent by the agent
