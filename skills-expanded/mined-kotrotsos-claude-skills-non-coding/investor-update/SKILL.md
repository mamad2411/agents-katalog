---
name: investor-update
description: Use this skill to draft a recurring monthly or quarterly investor update for a startup or scale-up. Triggers on phrases like "investor update for [month]", "draft this month's investor email", "write the [month] update", or when the user references their investor mailing list cadence. Produces a structured update in the founder's voice that protects the cadence even when the founder is tired.
---

# Investor Update Generator

## When to use this skill

The user is a founder or executive who sends recurring updates to investors and advisors. They wrote the first six carefully. By month nine they are drifting. By month twelve the discipline is gone. This skill protects the cadence by removing the activation energy from drafting each update.

## Input the user provides

- Time period the update covers (month or quarter)
- Headline metrics for the period
- Wins worth mentioning
- Lowlights or risks worth acknowledging
- Specific asks of investors (introductions, hiring, advice, capital)
- Optionally: prior update for continuity

## What this skill does

1. Pulls the structure the founder has committed to
2. Maintains continuity with prior updates (referencing forward commitments and whether they were met)
3. Writes in the founder's voice (review prior updates as voice samples if available)
4. Distinguishes signal from noise (does not include metrics that move randomly, does include metrics that compound or trend)
5. Produces a draft in the structure below

## Output structure

```
Subject: [Company] Investor Update, [Month YYYY]

Hi all,

[One paragraph hook. What is the headline of this month. Concrete, specific, no hype.]

## The numbers

| Metric | This period | Last period | Change |
|--------|------------|-------------|--------|
| [Metric 1] | [value] | [value] | [delta] |
| [Metric 2] | [value] | [value] | [delta] |
| [Metric 3] | [value] | [value] | [delta] |

[One paragraph reading of the numbers. What changed, what it means, what we are watching.]

## Wins
- [Specific win 1 with the why]
- [Specific win 2 with the why]
- [Specific win 3 with the why]

## Lowlights
- [Honest acknowledgment 1, with what we are doing about it]
- [Honest acknowledgment 2]

## What we said last month and how we did
- [Last month's commitment 1]: [delivered / partial / missed, with one-sentence reason]
- [Last month's commitment 2]: same

## What we are doing next month
- [Specific commitment 1]
- [Specific commitment 2]

## Asks
1. **[Specific ask, e.g. intros to X type of buyer]**: [why it matters now, what good looks like]
2. **[Specific ask 2]**: same

Thanks for reading.

[Founder name]
```

## Calibration notes

- Investor trust compounds through cadence. Cadence survives through removal of activation energy. The skill exists to remove the activation energy.
- The "What we said last month and how we did" section is the highest-trust-building section. It is also the one most founders skip. Do not skip it. Honest accountability on past commitments builds more trust than hiding misses.
- Ask for specific things. "Intros" is too vague. "Intros to VP of Engineering at Series B fintech companies" is useful.
- One headline per update. If everything is highlighted, nothing is highlighted.
- Length: 400-700 words for monthly. Longer is not better.

## Voice calibration

If the founder has shared prior updates, study them for:
- First-person plural vs. singular (most use "we" but some founders use "I" deliberately)
- Tone of self-criticism (some founders are blunt about lowlights, some are measured)
- Use of humor or warmth
- How they sign off

Match the existing voice. Do not import a generic startup-bro register that does not match how this founder actually writes.

## When NOT to use this skill

- First-time fundraising decks (different format)
- Crisis communications (different structure needed)
- Board reports (more formal, more data, different audience)
