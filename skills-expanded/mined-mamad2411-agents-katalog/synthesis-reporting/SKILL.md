---
name: synthesis-reporting
description: Turns gathered, verified findings into an answer a reader can act on: states the conclusion first, supports it with attributed evidence, distinguishes fact from inference from opinion, quantifies confidence, surfaces the disagreements and the gaps, and recommends without overreaching what the evidence supports. The output half of research; source-research and source-verification are the input. Use to write up a research finding for a decision.
license: MIT
metadata:
  category: research
  version: 1.0.0
  depends_on: [research-core, source-research]
  outputs: [research-answer, evidence-trail, confidence-statement, open-questions]
---

# Synthesis Reporting

Research that is never written up clearly is research that was not done, as far
as the reader is concerned. Synthesis turns a pile of attributed findings into
an answer to the question, stated so a reader can act on it and check it. It is
the output half; `source-research` and `source-verification` are the input.

## 1. Conclusion first

The reader needs the answer before the evidence, not after it.

```
lead        the answer to the question, in the first lines, as directly as the
            evidence allows
qualify     with the confidence and the conditions, in the same breath, so the
            answer is not read as more certain than it is
then        the evidence that supports it, for the reader who needs to check
```

A report that withholds the conclusion until the end forces every reader to do
the synthesis the report was supposed to do.

## 2. Support with attributed evidence

```
attribute   every load-bearing statement to a consulted source, per research-core
type        mark fact, inference, and opinion so the reader knows which is which
trail       the reader can follow any claim to its source and location
weight      the evidence for the conclusion is presented in proportion to how much
            it carries; a decisive source is not buried beside a minor one
```

## 3. Quantify confidence

```
high        multiple independent primary sources agree; verified
moderate    good sources, some gaps or minor conflict, reasonable inference
low         thin sources, unresolved conflict, or heavy inference; say so plainly
state       the confidence per conclusion, not one global hedge; different parts
            of an answer are known to different degrees
```

Confidence is a statement the reader acts on. "We are highly confident of X and
can only guess at Y" is more useful than a uniform "this is our best
understanding".

## 4. Surface disagreement and gaps

```
conflict    where sources disagreed, present it, per research-core; do not resolve
            it silently in favour of the tidy answer
gap         what could not be established, and what would establish it
implication what the gaps mean for the decision: does the missing piece change
            the answer, or only its confidence
```

## 5. Recommend without overreaching

```
recommend   when the question asks for a recommendation, give one, tied to the
            evidence and the decision's weighting
bound       the recommendation does not claim more than the evidence supports; a
            moderate-confidence finding produces a recommendation hedged to match
alternatives   name what a different weighting or a filled gap would change
separate    keep the finding (what is true) distinct from the recommendation
            (what to do about it); a reader may accept one and not the other
```

## 6. Prohibitions

- Never bury the conclusion at the end; lead with it, qualified.
- Never present a load-bearing claim without its attribution.
- Never state one global confidence for an answer known to different degrees.
- Never resolve a real source conflict silently to reach a clean answer.
- Never omit a gap that could change the decision.
- Never let the recommendation claim more certainty than the finding supports.
- Never blend fact, inference, and opinion into an undifferentiated narrative.

## 7. Protocol

1. State the conclusion to the question first, with its confidence and conditions.
2. Present the supporting evidence, each attributed and typed.
3. Give confidence per conclusion, not one blanket hedge.
4. Surface the conflicts and the gaps, with what each means for the decision.
5. Recommend, if asked, bounded to what the evidence supports, with alternatives.
6. Keep finding and recommendation separate.
7. Provide the evidence trail so any claim can be checked.

## 8. Auto-critique

Score from 0 to 5: conclusion led and qualified, every load-bearing claim
attributed and typed, confidence stated per conclusion, conflicts surfaced, gaps
named with their effect on the decision, recommendation bounded to the evidence,
finding kept distinct from recommendation.

Threshold: no axis below 3, average at least 4. A conclusion presented as more
certain than the evidence supports, or a load-bearing claim with no attribution,
caps the score until fixed.

## 9. Interfaces

- Upstream: `research-core` sets the evidence and confidence standard,
  `source-research` supplies the attributed findings, `source-verification`
  supplies the verdicts and confidence, `competitive-analysis` supplies the
  comparative matrix.
- Downstream: `report-writing` renders the synthesis as a formal document for a
  decision; the career and business skills consume the synthesised answer.
- Lateral: `self-critique` for the reviewer roles, `decision-records` when the
  synthesised answer informs a recorded decision.

## 10. Note on scope

This skill writes up research findings; it does not gather them. A synthesis with
no `source-research` behind it has nothing to synthesise and is not written from
the researcher's prior belief. If the findings are thin, the honest synthesis
says so and reports low confidence, rather than compensating with confident prose.
