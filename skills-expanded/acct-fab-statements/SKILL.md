---
name: acct-fab-statements
description: Builds FAB statements that link each need the customer stated to a feature, an advantage, a benefit in their terms and a real proof you supply, with needs that lack proof flagged and features that answer no stated need set aside. Use for "run acct-fab-statements", "FAB statements", "features advantages benefits", "benefit statements", "value proposition for this customer", "the customer asked so what", "turn features into benefits", "sales pitch for this account", part of the Claude for Account Executives Pack by 90n.
---

# FAB Statements

## When To Use
Your presentation lists features and the customer asks "so what?". Run this after discovery or a first meeting. It answers: for each need the customer stated, what does your offer change for them, and how do you prove it?

## When Not To Use
To answer one specific objection, run Objection Handling. With no need stated by the customer at all, run Discovery Call Questions first: statements with no need behind them go back to being a feature list.

## Inputs
- The needs the customer stated, in their words: call notes, discovery coverage grid.
- Your offer: features, product sheet or current deck.
- The proof you are allowed to use: customer stories the customer has agreed to, trials, figures with their source.
If you have none of this, I start from your offer and one need you describe, and mark the output as a first draft.

## Approach
Features, advantages, benefits is common selling practice, described here generically: a feature is what the offer is or does, an advantage is what that does better than the customer's current way, and a benefit is what it changes for this customer against a need they stated. I add a fourth column, proof, because a benefit with nothing behind it is a claim. I start from the need, never from the feature list. The failure it prevents: the pitch that stacks features, and the invented proof that falls at the first question.

## Workflow
1. I ask at most three questions: which needs did the customer state and when, which proof are you allowed to cite, and in which format will you present.
2. I list the needs in the customer's words, with source and date. A need you suppose is marked "to confirm" and does not get a benefit yet.
3. Feature: for each need, the part of your offer that answers it, in one factual line.
4. Advantage: what that feature does better than the way the customer works today, as they described it.
5. Benefit: what it changes for this customer in their terms (their delay, their workload, their risk). A brochure benefit that fits any customer is rewritten or cut.
6. Proof: something you supply and can show (a customer story with agreement, a trial, a figure with its source). With none I write "proof missing" and how to get it; I never fill the cell.
7. Features that answer no stated need leave the pitch and wait in reserve in case the customer asks. In Claude Slides the result becomes one slide per need, with its proof.

## Output Format
```markdown
# FAB Statements
[Account] · [format] · [date]
## Statements
| Stated need (their words, source) | Feature | Advantage over their current way | Benefit in their terms | Proof (source) |
|---|---|---|---|---|
| "[words]" ([call of date]) | [feature] | [advantage] | [benefit] | [proof] or "proof missing" |
## Proof to obtain
| Need | Missing proof | How to get it | Who, by when |
|---|---|---|---|
| [need] | [proof] | [trial, story to document] | [name, date] |
## Held in reserve
- [feature with no stated need]
## Needs to confirm
- [supposed need] · question: [question]
## Decision
[You] approve the proof you may cite and the order of presentation by [date].
```

## Done When
- Every row starts from a stated need with its source.
- Every proof exists and you can show it; the rest read "proof missing".
- Features with no need behind them are out of the pitch.

## Quality Bar
- The benefit speaks the customer's language, not the brochure's.
- No figure without its source; no customer named without their agreement.
- A proof shows what was achieved elsewhere, never a promise of the same result here.
- You present in your own words; I prepare the material, not a speech.
- Every proof comes from you and exists: no customer quote, figure or result is invented.

## Next
Run acct-objection-handling (Objection Handling) to prepare answers to the objections you heard, using this proof.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
