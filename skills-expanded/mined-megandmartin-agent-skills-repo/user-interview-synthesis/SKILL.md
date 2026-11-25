---
name: user-interview-synthesis
description: Synthesize customer interview notes or transcripts with Mom Test discipline — separate facts from opinions from compliments, extract commitment signals, and generate next-interview questions. Use when the user says "synthesize my interviews", "what did I actually learn", "Mom Test this transcript", "did that interview validate anything", or pastes interview notes. Don't use for piles of written survey answers — that's survey-response-synthesizer.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Research & Analysis, Customer Discovery, Mom Test, Interviews]
    related_skills: [survey-response-synthesizer, competitor-teardown]
---

# User Interview Synthesis

Applies Rob Fitzpatrick's Mom Test (Day 3 material) to interview notes or transcripts: sort every statement into fact, opinion, or compliment; keep only facts and commitments as evidence; and produce the questions the *next* interview should ask. The standard: compliments are never counted as validation, "I would totally buy that" is filed as opinion, and the report is honest even when — especially when — the interviews validated nothing.

## When to Use

- User finished 1–10 customer interviews and wants to know what they actually learned.
- User asks whether an interview "validated" their idea.
- Before the next round: what to ask, whom, and what would change the decision.
- **Not for:** clustering many short written answers (`survey-response-synthesizer`); researching a competitor a prospect mentioned (`competitor-teardown`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Fact | past behavior with specifics: "last month I paid $X for Y", "we churned from Z in March" |
| Opinion | future/hypothetical: "I would...", "that sounds useful", "people would love this" |
| Compliment | "cool idea!", "great job" — social kindness; evidence weight: zero |
| Commitment | gave up something real: time (booked next meeting), reputation (an intro), money (paid, LOI, deposit) |
| Bad-question flag | interviewer pitched, led, or asked hypotheticals — taint downstream answers |
| Next questions | target the biggest unknown; phrased about past behavior, never the idea |

## Procedure

1. **Precheck** — collect: the notes/transcripts (one block per interviewee), who each person is (are they actually the target buyer?), and the hypothesis being tested ("<who> has <problem> and currently <workaround>"). No stated hypothesis? Reconstruct it with the user first — synthesis needs something to test against.
2. **Statement pass** — go through each transcript line by line. Extract every substantive statement verbatim with speaker + interview ID. Classify each as **fact** (specific past behavior/spend), **opinion** (future, hypothetical, generic praise of the idea), or **compliment**. When in doubt, downgrade — an ambiguous fact is an opinion.
3. **Flag tainted exchanges** — mark interviewer questions that pitched the idea, led the witness ("wouldn't it be great if..."), or asked about hypothetical futures. Answers to tainted questions get classified opinion at best, and the report says why.
4. **Commitment scan** — list every moment someone gave up something real: booked a follow-up, introduced a colleague, shared internal data, pre-paid, signed anything. Also list the *misses*: moments the interviewer could have asked for commitment and didn't.
5. **Score the hypothesis** — for each part of the hypothesis (who / problem / current workaround / willingness to pay), tally supporting facts vs contradicting facts. Opinions and compliments contribute zero. Verdict per part: supported / contradicted / untested — with the fact count that justifies it.
6. **Next-interview kit** — write 5–8 questions targeting the biggest untested or contradicted part. Every question must be about the interviewee's past or present ("walk me through the last time...", "what did that cost you?"), never about the user's idea. Add: who to talk to next and what evidence would change the verdict.
7. **Deliver** — fill the template. If n < 5 interviews, stamp the whole report "early signal — not evidence" regardless of how good it sounds.

## Output Template

```
# Interview Synthesis — <project> — <date>
Interviews: N | Target-profile matches: N of N | Hypothesis: <who/problem/workaround>

## Evidence ledger
| Int. | Statement (verbatim) | Class | Bears on |
|---|---|---|---|
| #2 | "We pay a VA $400/mo to do this" | FACT | problem cost |
| #3 | "I'd definitely use it" | OPINION (tainted: pitched first) | — |

## Commitments
- Given: <who did what real thing> | Missed asks: <where commitment wasn't requested>

## Hypothesis scorecard
| Part | Facts for | Facts against | Verdict (confidence) |

## What we still don't know
1. <biggest unknown>

## Next-interview kit
- Ask: "<past-behavior question>" → tests <unknown #>
- Talk to: <who> | Verdict-changing evidence: <what>
```

## Pitfalls

- **Compliments counted as validation** — "everyone loved it!" becomes "validated". Recovery: compliments are logged then excluded from every tally; if the ledger is mostly compliments, the finding is "we pitched instead of interviewed" — say it kindly and fix the next-interview kit.
- **Hypotheticals treated as facts** — "I would pay $50" recorded as pricing evidence. Recovery: anything conditional or future-tense is opinion by rule; the only pricing facts are what people pay today (for the problem or workaround) and money actually committed.
- **Leading questions poisoning the data** — enthusiastic answers to "wouldn't you love X?" Recovery: step 3's taint flags; tainted answers can't support the hypothesis, and the next-interview kit rephrases each tainted question into a past-behavior version.
- **Synthesizing to please the founder** — the user wants validation, and summaries drift positive. Recovery: the scorecard format forces fact counts per verdict; if facts-against outnumber facts-for, the verdict says contradicted, full stop.
- **Wrong people, right answers** — three interviews with friends who aren't the buyer. Recovery: profile-match count in the header; non-matching interviews get their facts kept but marked "off-profile" and excluded from the scorecard.

## Verification

- [ ] Every ledger entry is verbatim with interview ID; classifications spot-checked (3 random)
- [ ] Zero opinions or compliments counted in any scorecard tally
- [ ] Commitments list includes missed asks, not just wins
- [ ] Every next-interview question is past/present-behavior phrased
- [ ] n < 5 interviews → "early signal — not evidence" stamp present
