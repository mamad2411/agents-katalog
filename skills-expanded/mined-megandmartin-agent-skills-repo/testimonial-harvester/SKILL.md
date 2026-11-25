---
name: testimonial-harvester
description: Mines customer feedback for testimonial-worthy quotes, drafts permission-ask messages, and structures approved quotes with usage rights recorded. Use when the user says "get testimonials", "find quotes from customers", "who said nice things", "social proof for the landing page", or wants to turn praise into marketing assets. Don't use for handling support complaints — use customer-support-inbox — or for cold outreach to strangers — use cold-outreach-sequencer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Business Ops, Marketing, Testimonials, Social-Proof]
    related_skills: [customer-support-inbox, cold-outreach-sequencer, weekly-revenue-report]
---

# Testimonial Harvester

Turns scattered praise — support threads, DMs, community posts, feedback forms — into a structured testimonial library the user can legally and confidently publish. Three stages: find the candidates, ask permission (drafts only), record the approved quote with its usage rights. The standard: **no quote is ever published without explicit permission on record**, and no permission-ask is ever sent by the agent.

## When to Use

- User wants social proof for a landing page, deck, or launch post.
- A pile of feedback exists (inbox export, community channel, form responses) and nobody has mined it.
- A customer just said something great and the user wants to capture it properly.
- **Not for:** working complaints — use `customer-support-inbox`. Not for messaging people with no prior relationship — use `cold-outreach-sequencer`.

## Quick Reference

| Action | Command / Call |
|---|---|
| Sweep feedback for praise signals | `grep -n -i -E "love|amazing|game.?changer|saved me|finally|recommend|worth|wow" feedback.txt` |
| Testimonial library | `testimonials.md` in the marketing folder — one entry per quote with status + rights |
| Check for duplicates | `grep -i "{customer name}" testimonials.md` |
| Count approved quotes | `grep -c "Status: approved" testimonials.md` |
| Check for pending asks going stale | `grep -B2 "Status: pending" testimonials.md` — nudge once after ~10 days, then let it go |
| Never re-ask list | `grep -B2 "Status: declined" testimonials.md` |

## Procedure

1. **Precheck** — locate the feedback source(s) and `testimonials.md` (create it with a header if missing). Confirm with the user which channels are fair game to mine — private messages are only usable with the sender's permission anyway, but don't even harvest from channels the user says are off-limits.
2. **Mine candidates** — read the source, then run the grep sweep to catch anything missed. A candidate needs: a specific outcome or feeling (not just "great product"), the customer's name/handle, and where/when they said it. Rank by specificity — "cut my invoicing from 3 hours to 20 minutes" beats "love it!".
3. **Draft permission asks (drafts only)** — for each candidate, draft a short personal message: quote back exactly what they said, ask permission to use it, and offer the choice of name + title/company, first name only, or anonymous. One message per person, warm not legalese. **The agent never sends these** — the user copies and sends personally; personal asks convert better anyway.
4. **Record responses** — when the user reports back, update each entry's status: `approved`, `approved-with-edits` (store their edited version verbatim), `anonymous-only`, or `declined` (keep the entry so nobody re-asks — mark it clearly and never surface the quote again).
5. **Structure approved quotes** — for each approval, finalize the library entry per the template: exact quote, attribution level granted, where it may be used (web/social/deck/ads — as granted, not assumed), date, and source link/reference. Tighten quotes for length only with the customer's OK; never change meaning.
6. **Deliver** — output new candidates, permission-ask drafts, and the current library scoreboard (approved / pending / declined).

## Output Template

```
# Testimonial Harvest — {Date}

## New candidates ({n})
1. {Name} — "{exact quote}" — {source, date} — specificity: high/med

## Permission-ask drafts (you send these — I don't)
### To {Name}
> {draft message quoting their words, asking permission + attribution preference}

## Library entry format (testimonials.md)
### {Name} — {Title, Company | first name | anonymous}
Quote: "{final approved text}"
Rights: {web / social / deck / ads} · Attribution: {level granted}
Status: approved · Asked: {date} · Approved: {date} · Source: {link/ref}

## Scoreboard
Approved {n} · Pending {n} · Declined {n} (never re-ask)
```

## Pitfalls

- **Quote used before permission lands** — a "pending" quote ends up on the landing page; trust and possibly law broken. Recovery: only `Status: approved` entries are publishable; audit any live copy against the library and pull anything unapproved.
- **Attribution beyond what was granted** — customer approved "first name only" and the site shows full name + company. Recovery: the Rights and Attribution lines are the contract; check them before every use and fix the live copy immediately.
- **Polished quote no longer sounds human** — over-editing turns "honestly this saved my launch" into marketing mush. Recovery: keep the customer's exact words; if you must trim, show them the trimmed version and get a fresh OK.
- **Re-asking someone who declined** — feels pushy, burns the relationship. Recovery: declined entries stay in the library as tombstones; grep for the name before drafting any ask.
- **Agent sends the permission asks** — never; personal asks from the founder convert and the rail is drafts-only. Recovery: output text drafts, no send calls of any kind.

## Verification

- [ ] Every candidate has name, exact quote, source, and date — nothing paraphrased
- [ ] Permission-ask drafts exist as text only; zero messages sent by the agent
- [ ] `testimonials.md` entries carry Status, Rights, and Attribution fields
- [ ] No approved-count mismatch: `grep -c "Status: approved"` equals the scoreboard number
- [ ] Declined entries preserved and excluded from all publishable output
- [ ] Candidates ranked by specificity, with the outcome-bearing quotes on top
