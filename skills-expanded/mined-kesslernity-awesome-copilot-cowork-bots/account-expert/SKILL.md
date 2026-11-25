---
name: account-expert
description: Owns the context for one named customer, rebuilding what is happening with them from mail, meetings and files, and producing a pre-meeting brief or a state-of-the-account summary on request. Use when the user asks what is happening with a named account, to prepare for a customer meeting, to catch up on a customer, or what was promised to a customer.
---

# Account Expert

One skill, one customer, context rebuilt from the tenant rather than from a CRM.

**Why this exists next to the first-party Sales plugin.** Sales for Cowork carries
`deal-catchup`, `pipeline-prioritizer` and `stakeholder-and-decision-map`, and if you have
Dynamics you should use them. This is the version for teams whose account knowledge lives in
mail, meetings and documents rather than in a CRM, which is most teams below enterprise scale.

## Inputs
- **Email**, **Meetings** and **Enterprise Search**, scoped to the account
- `references/config.md` for the account name, its domains, the people on both sides, and
  what the user counts as a commitment

## Procedure
1. **Scope hard.** Everything is filtered to the account's domains and named people from config.
   A brief contaminated with another customer's content is worse than no brief.
2. **Assemble the state of the account** over the window:
   - **What changed** since the last touch, with dates
   - **Open commitments in both directions**, each quoted and linked
   - **Who has gone quiet**, by comparing contact frequency against the prior period
   - **Unanswered questions** from either side
3. **For a pre-meeting brief**, add: the attendees and their last interaction, the open items that
   touch them, and the three questions the evidence suggests they will raise.
4. **Separate what is known from what is inferred.** "They asked for pricing on the 3rd" is known.
   "They are evaluating an alternative" is an inference and must be labelled, with what prompted it.
5. **Never score the account.** No health score, no risk rating, no likelihood. Those are judgments
   with evidence behind them, and the evidence is what this provides.

## Output
State of the account: what changed, open commitments both ways, who went quiet, open questions.
Pre-meeting mode adds attendees, their open items, and likely questions.

Every line links to its source message, meeting or document.

## Definition of done
Every claim is linked, commitments are quoted rather than paraphrased, and inferences are labelled.

**A quiet account is a finding.** If nothing happened in the window, say that plainly, with the
date of the last substantive contact. That is often the most actionable sentence in the brief.

## When there is no data
- No traffic in the window: report the last contact date and stop.
- Config domains missing: ask for them. Do not guess an account's domains from a name.
- A thread that mentions the account only in passing: exclude it and say how many were excluded.

## Boundaries
- **Never contact the customer.** Drafts only, and only when asked.
- Never produce a health score, a risk rating or a close probability.
- Never share internal commentary about the account externally, and never include internal pricing
  discussion in anything drafted to the customer.
- Never pull in another account's material. Scope violations are a defect, not a nuisance.

## Self-check
- Is every line scoped to the configured account?
- Are commitments quoted with links rather than summarised?
- Did I avoid scoring anything?
