---
name: ab-test-significance
description: >-
  Use when the user wants to check whether an A/B test result is statistically
  significant, or to size a test before running it. Also use when the user
  mentions A/B test, split test, statistical significance, p-value, confidence
  level, conversion lift, sample size, or "is this result real / can we call
  the test." Produces lift, p-value, a significance verdict, and required
  sample size; compares averages such as revenue per visitor with Welch's
  t-test; and checks the visitor split for a sample ratio mismatch.
license: MIT
metadata:
  search_description: "Check whether an A/B test result is statistically significant, or size a test before you run it: lift, p-value, a significance verdict and the sample needed."
  publisher: AAJ
  slug: ab-test-significance
  category: Analytics & Experimentation
  phase: Execute
  difficulty: Starter
  card: >-
    Checks whether an A/B result is significant, or sizes a test before you run it.
  version: 1.2.0
  sprint: unit-economics-retention
  topic: analytics-budget
  secondary_topics: [website-conversion]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Visitors and conversions for control and variant, or visitors, mean and standard deviation of a per-visitor value (to evaluate) OR baseline rate and minimum detectable effect (to size a test)
  outputs: Conversion rates or averages, relative lift, p-value, interval on the difference, significance verdict, a sample ratio check, and required sample size
  related_aaj:
    - https://aajconsult.com/tools/ab-test-significance-calculator
    - https://aajconsult.com/blog/ab-testing-complete-guide
  related: [website-conversion-audit, paid-media-budget-allocation]
  tags: [ab-testing, significance, p-value, sample-size, cro, experimentation]
---

# A/B Test Design & Significance

Tell the user whether a test result is **real or noise**, and how big a test needs to be before it can answer the question. Most teams call tests too early on too little data; this keeps the decision honest with a proper two-proportion z-test.

## When to use

The user has an A/B test result to evaluate, or wants to size a test before launching it.

## Workflow

**To evaluate a result:** gather visitors and conversions for control and variant, pick a confidence level (usually 95%), and run the engine. **For an average per visitor** (revenue per visitor, order value), add `"metric":"mean"` and give each arm its visitors, mean and standard deviation, or its values (one per visitor, zeros included); the engine runs Welch's t-test. **To plan a test:** take the baseline conversion rate and the minimum lift worth detecting (the MDE), and compute the required sample size. If the traffic split was not 50/50, pass it as `"plannedSplit"` so the sample ratio check uses it.

> Paths assume you installed with `npx skills add`. From a clone of this repo, use `skills/ab-test-significance/resources/…` instead.

```bash
node .agents/skills/ab-test-significance/resources/significance.js  # demo (5.0% vs 6.2%)
node .agents/skills/ab-test-significance/resources/significance.js '{"control":{"visitors":4000,"conversions":200},"variant":{"visitors":4050,"conversions":250},"confidence":95}'
node .agents/skills/ab-test-significance/resources/significance.js '{"metric":"mean","control":{"visitors":4000,"mean":2.31,"sd":11.8},"variant":{"visitors":4050,"mean":2.87,"sd":13.1}}'  # revenue per visitor
node .agents/skills/ab-test-significance/resources/significance.js '{"plan":true,"baselineRate":5,"mde":1,"confidence":95,"power":80}'  # sample size
node .agents/skills/ab-test-significance/resources/significance.js --help
```

If your analytics tool reports visitors and a conversion rate, not a count, give each arm `"rate"` as a fraction from 0 to 1 in place of `"conversions"` (`{"visitors":4000,"rate":0.05}`). The engine works out the count and prints it; do not multiply it yourself.

It returns rates (or averages), relative and absolute lift, the test statistic and p, a significance verdict at your confidence level with an interval on the difference, and a sample ratio check; or, in plan mode, the visitors needed per variant.

## Interpret the result

- **Significant** (p < 1 − confidence) means the difference is unlikely to be chance at that level — the winner is real. **Not significant** means keep running or treat as no detected difference; it does **not** prove the variants are equal.
- **Sample ratio mismatch.** The engine tests the visitor counts against the planned split with a chi-square test and flags a mismatch below p = 0.0005, the threshold Microsoft's Experimentation Platform uses ([Fabijan et al., 2020](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)). A mismatch usually means a redirect, bot or tracking problem; find the cause before trusting the verdict.
- **Averages** use Welch's t-test with Welch-Satterthwaite degrees of freedom ([NIST/SEMATECH 1.3.5.3](https://itl.nist.gov/div898/handbook/eda/section3/eda353.htm)), which does not assume the two arms have the same spread. Revenue per visitor is skewed by a few large orders, so the test needs more visitors than a conversion test to see the same lift.
- **Size the test first.** If the required sample (plan mode) is far above your traffic, the test can't realistically resolve that small a lift — pick a bigger change or a longer window.

## Present the result

- **Rates and lift** for control and variant (absolute and relative), or the averages and their difference.
- **z (or t) and p**, and whether it is significant at the chosen confidence.
- **The sample ratio check**, first, when it flags a mismatch.
- **Required sample size** per variant, and whether the traffic can reach it.
- The **verdict in one line**: call it, keep running, or treat as no detected difference.

**Show where it came from.** Open your answer with "AAJ `ab-test-significance` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/ab-test-significance`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Don't peek and stop early.** Calling a test the moment it crosses significance inflates false positives; decide the sample size up front and run to it.
- **Significance ≠ importance.** A tiny, significant lift may not be worth shipping; weigh the effect size.
- **One metric, pre-declared.** Testing many metrics until one is significant is p-hacking.
- **Mind the cycle.** Run at least one full business cycle (e.g., a week) to avoid day-of-week skew.
- **Conversions, not clicks.** Test toward the real outcome, not a proxy.

## Related AAJ resources

- Interactive tool: https://aajconsult.com/tools/ab-test-significance-calculator

## Related skills

`website-conversion-audit` (find what to test) · `aaj-marketing-psychology` (generate hypotheses) · `marketing-report` (measure correctly).

## Credits

Original AAJ skill. The Agent Skills format and Corey Haines' `coreyhaines31/marketingskills` (MIT) were references for structure and coverage; this skill is independently written. See the repository README.
