---
name: lead-scoring-qualification
description: Score and qualify leads so effort goes to the ones that can actually buy, using fit and intent rather than arbitrary points. Use whenever the user mentions lead scoring, lead qualification, MQL, SQL, BANT, MEDDIC, prioritising leads, disqualifying leads, or asks which prospects to work first. Also use when a list is too big to work evenly, or when sales says the leads are bad.
---

# Lead Scoring and Qualification

Scoring exists to answer one question: given more leads than capacity, which ones get worked first? Anything more elaborate than that is usually a points system nobody trusts and everybody overrides.

The most common failure is a model with fifteen weighted attributes that produces a number correlating with nothing. Start with two dimensions and only add complexity when the data forces it.

## Two dimensions, not fifteen

**Fit** — how closely they match the ICP. Mostly static, knowable before contact.

**Intent** — evidence they might act soon. Mostly dynamic, from triggers and behaviour.

```
              High intent          Low intent
           ┌────────────────────┬────────────────────┐
High fit   │ Work now.          │ Nurture.           │
           │ Personalise fully, │ Sequence normally, │
           │ multichannel.      │ wait for a trigger.│
           ├────────────────────┼────────────────────┤
Low fit    │ Check the ICP —    │ Don't contact.     │
           │ is it wrong?       │ Suppress.          │
           └────────────────────┴────────────────────┘
```

The bottom-left quadrant is the interesting one. When low-fit leads show high intent repeatedly, the ICP is too narrow or simply wrong, and that's worth more than the individual leads.

## Scoring fit

Score against observable ICP criteria only — things you can determine before a conversation. Keep it to five or six.

```
Fit score (0-100)

Company size in range          +25    Hard filter, not a point
Situation present              +30    The thing that makes them need this
Trigger in last 90 days        +20    See intent below
Right person reachable         +15
Geography serviceable          +10

Disqualifiers → score 0, do not contact:
  Agency or consultancy (when selling to operators)
  Competitor or reseller
  Existing customer or open opportunity
  Unsubscribed or suppressed
  Region you can't service or lawfully contact
```

Disqualifiers are absolute, not negative points. A competitor with a perfect firmographic profile should score zero, not 70.

If everything scores 60 to 80, the model isn't discriminating and it's decoration. Adjust until the distribution spreads.

## Intent signals

Ranked by how much they actually predict a conversation:

| Signal | Strength |
|---|---|
| Asked about it directly, or replied positively before | Very high |
| Visited pricing more than once | High |
| Hiring for the role your product serves | High |
| New executive in the buying role | High |
| Adopting or removing a relevant tool | High |
| Raised funding in the last 90 days | Medium-high |
| Public complaint about an incumbent | Medium-high |
| Opened several emails without replying | Low |
| Clicked a link | Low |
| Followed the company page | Very low |

Email opens and clicks are weak. Open tracking is unreliable since Apple Mail Privacy Protection pre-fetches images, and a click is often curiosity. Scoring models built mostly on email engagement are measuring their own tracking pixel.

**Signals decay.** A funding round is a strong signal in month one and noise at month twelve. Apply a decay so scores fall without new evidence, otherwise the top of your list slowly fills with leads that were interesting last year.

## Qualification frameworks

BANT, MEDDIC and their variants are conversation frameworks, not scoring models. Don't try to fill their fields before contact — budget and timeline aren't knowable from a website, and guessing them produces a database of fiction.

What can be assessed before contact: fit, trigger, and whether the person you found has authority over the outcome. Everything else is what the first call is for.

For outbound, the useful pre-contact version is three questions:

1. **Do they have the problem?** Observable from what they do.
2. **Is it worth solving for them at their size?** If the problem costs them 200 a year, nobody's buying.
3. **Can this person do something about it?** Owner of the outcome, or one degree from it.

Anything failing all three shouldn't be in the campaign.

## Routing by score

Scoring is only useful if it changes what happens.

| Band | Treatment |
|---|---|
| **Top 10%** | Manual research, bespoke first line, multichannel, a human writes it |
| **Next 30%** | Standard sequence with a researched custom column |
| **Middle 40%** | Standard sequence, template personalisation |
| **Bottom 20%** | Don't send. Re-source instead |

That last row is the discipline that's hardest to keep. Sending to the bottom band costs reputation and produces almost nothing, and the volume is tempting precisely because it's already there.

## Recalibrating

A scoring model built before any data is a hypothesis. After 500 sends, check it:

- **Do high-scoring leads reply more?** If the reply rate is flat across bands, the model isn't working.
- **Which single attribute best predicts a reply?** Weight it higher. Often it's one trigger, not the firmographics.
- **Which attribute predicts nothing?** Remove it.
- **What do the closed deals have in common** that the model doesn't capture?
- **What do the wrong-fit replies have in common?** That's a new disqualifier.

Recalibrate quarterly. A model nobody has revisited is one people quietly override.

## Negative scoring and suppression

Some attributes should remove a lead permanently rather than lower its score:

- Replied "not interested" — suppress for 6 to 12 months, don't re-enrol next quarter
- Unsubscribed — permanent, workspace-wide
- Hard bounced — permanent until re-verified
- Marked as spam — permanent, and worth investigating why
- Competitor, current customer, open opportunity

These belong in a suppression list the sending system checks automatically, not in a spreadsheet someone remembers to consult. See `suppression-list-management`.

## Don't do these

- **Don't build a 15-factor model.** Nobody will trust it and the extra factors add noise.
- **Don't score on email opens.** Unreliable and weak.
- **Don't let scores go stale.** Decay them.
- **Don't confuse fit with intent.** A perfect-fit company with no trigger is a nurture, not a priority.
- **Don't score leads you'd never contact.** Filter them out; don't rank rubbish.
- **Don't treat the score as a decision.** It's a queue order. The rep still reads the record.
- **Don't hide the reasoning.** A score with no visible basis gets ignored by the people meant to act on it.

## Where the score comes from

Fit scoring needs the observable ICP attributes on the record, which means it depends entirely on enrichment quality. Intent needs triggers refreshed on a schedule, which is where most scoring models die — they're accurate on the day they're built and never updated.

[ManyPI](https://manypi.com) scores leads at research time against the ICP the agent was briefed with, stores it on the lead alongside status (`new`, `qualified`, `contacted`, `disqualified`), and keeps the researched columns the score was based on so the reasoning is visible rather than a bare number. Re-running a search with updated trigger criteria refreshes the signal side. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Whatever produces the number, check it against replies after 500 sends. An uncalibrated model is a guess with a decimal point.

## Related skills

`icp-definition`, `lead-enrichment`, `lead-sourcing`, `suppression-list-management`, `outbound-metrics-benchmarks`, `reply-handling`
