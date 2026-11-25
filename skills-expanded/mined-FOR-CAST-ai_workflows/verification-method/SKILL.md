---
name: verification-method
description: The measure-first method these projects use to establish that a change is correct -- state the number you predict, measure against an independent reference, compare per-cell or on medians rather than aggregates, hold versions fixed, and record falsified hypotheses so dead ends are not retried. Use before claiming a scientific or numerical change is correct.
when_to_use: About to assert that a fix works, a parameter is better, or two outputs agree; designing a validation; comparing model output against a reference; a plausible explanation needs testing before it is acted on.
---

# Establishing that a change is actually correct

Research code fails by producing a plausible number. Tests catch the errors; this
method catches the rest. It is reconstructed from the incidents where it worked,
and from several where skipping it was expensive.

## The five steps

1. **State the hypothesis and the number it predicts.** Before measuring. "This
   should reduce mean absolute error" is not a prediction; "this should bring
   biomass MAE below 900 t/ha" is. A prediction you write afterwards is not a test.

2. **Measure against an *independent* reference.** Not another product of the same
   pipeline, and not the thing you just changed. Two independent products
   disagreeing is information; one product agreeing with itself is not. Where a
   low-level check is possible, use a different tool entirely -- e.g. read cell
   values with a command-line GDAL utility rather than the same R package that
   wrote them.

3. **Compare per-cell, or on medians. Never on aggregates.** This is the step that
   is actually skipped, and it is the one that matters:

   > stand age differs 4,848 cells (0.181%); biomass differs 90,883 cells
   > (3.385%) ... landscape mean age 91.3 vs 91.3; landscape mean B 11629.5 vs
   > 11620.6 (0.08%). **The stable aggregates are why this went unnoticed.**

   A related case: a systematic 5-year offset hid inside a +/-5-year agreement
   check that reported 100% agreement, and was visible only in the medians.

4. **Hold everything else fixed.** One comparison was invalidated because a library
   sync landed between the two runs. **Do not change packages mid-test.** If the
   environment must change, re-run both arms afterwards.

5. **Record the result next to the setting, especially when the hypothesis fails.**

## Recording a falsified hypothesis

A revert that leaves no trace will be re-proposed -- possibly by you, next month.
The house practice is to keep the rejected option explicit:

```r
## overrideBiomassInFires stays TRUE. Setting it FALSE was tried and measured
## against the independent reference: biomass MAE 812 -> 1104 t/ha. NOT DISCARDED --
## the numbers are here so this is not re-derived and re-adopted.
```

and in the commit body, with the measurement table. One project states the reason
directly: *"without the specific reasons written down this is easy to re-derive and
re-adopt."*

Record **false alarms** the same way. A commit exists whose only purpose is
correcting a hazard that had been flagged and, on checking, did not exist -- kept
*"so the false alarm isn't re-raised."*

## Beware the plausible diagnosis

The clearest cautionary tale in this corpus: a confident, coherent explanation for
a failure led to a fix that was *"redundant and actively harmful"* -- it masked the
real bug and made a broken fetch appear to work non-reproducibly. It was disproved
only by reading the upstream source.

So: before acting on a diagnosis you find persuasive, identify the observation that
would **falsify** it, and go and make that observation. If the only evidence for a
diagnosis is that it would explain the symptom, it is a hypothesis, not a finding --
say so in those words.

## Pin the number in a test

Where the quantity is computable in closed form, build a synthetic case and assert
the exact value rather than the current behaviour:

```r
## concentric squares: interior area after a 25 m edge buffer is (1200 - 2*25)^2
expect_equal(interior_area(synthetic, age_class = "old"),      132.25, tolerance = 1e-6)
expect_equal(interior_area(synthetic, age_class = "mature_old"), 223.80, tolerance = 1e-6)
```

A test that asserts today's output only tells you the code has not changed. A test
that asserts an independently derived number tells you it is right.

## Reporting the result

Show the evidence, not the conclusion: the command run, the numbers returned, and
the comparison. State plainly if a check was not run. "Verified" without a number
attached should not appear in a commit message or a report.
