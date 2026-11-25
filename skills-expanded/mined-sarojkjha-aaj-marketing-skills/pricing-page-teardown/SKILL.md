---
name: pricing-page-teardown
description: >-
  Use when the user wants to review a pricing page - their own or a
  competitor's - or is thinking about changing a price and asks whether a
  test would tell them anything. Also use when the user mentions pricing
  page audit, pricing page teardown, price test, price experiment, A/B
  testing a price, revenue per visitor, "should we raise prices", or
  "can we test this". Scores the page on 21 checks a buyer would notice,
  ranks the fixes against competitors, works out before launch whether a
  live price test can answer the question at your traffic, and reads a
  test against its planned size.
license: MIT
metadata:
  search_description: "Review a pricing page on 21 checks a buyer would notice, rank fixes against competitors, and see before launch whether a price test can answer the question."
  publisher: AAJ
  slug: pricing-page-teardown
  category: Strategy & Positioning
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Scores a pricing page on 21 buyer checks, and says whether a price test can answer the question at your traffic.
  version: 1.0.1
  topic: pricing-monetization
  secondary_topics: [website-conversion, analytics-budget]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Yes, partly, no or not-sure answers to the 21 checks for your pricing page and up to three competitors; for a price test, the current and test price per conversion, today's conversion, your honest guess at the test price, weekly pricing-page visitors and the weeks you could run it; afterwards each arm's visitors, conversions, revenue and the planned size
  outputs: Each page's weighted score by area with the top five fixes on yours and how many competitors already pass each; the break-even conversion, visitors and weeks a live test needs, the smallest change your traffic could detect, and a testable or not-testable call with alternatives; and a read-out against the planned size with a p-value, a not-randomised caveat where it applies, and a 90-day retention check
  related_aaj:
    - https://aajconsult.com/resources/pricing-page-teardown
    - https://aajconsult.com/tools/price-sensitivity-analyzer
    - https://aajconsult.com/tools/pricing-arpu-modeler
    - https://aajconsult.com/playbooks/pricing-packaging-playbook
  related: [pricing-and-packaging, ab-test-significance, website-conversion-audit, aaj-marketing-psychology]
  tags: [pricing-page, price-testing, revenue-per-visitor, rosca, teardown, competitor-pricing, a-b-test]
---

# Pricing Page Teardown

Most pricing-page reviews are opinions about layout. Most price tests are launched by teams who
find out afterwards that they never had the traffic to learn anything. This skill replaces both
with arithmetic: 21 checks scored on what a buyer can actually tell from the page, and a test plan
that says, before anything ships, whether a live test can answer the question in the weeks you
have. For Fieldnote, the invented scheduling app in the worked example, a $49 → $59 test at 2%
conversion and 3,000 visitors a week needs 126,757 visitors per arm, which is 85 weeks. That
result is the point: it is not unusual.

## When to use

The user is reviewing their pricing page, comparing it with competitors, considering a price
change, or has a price test running and wants to read it.

Do not use it to design the tiers or the value metric; `pricing-and-packaging` does that. Do not
use it to estimate willingness to pay; the `Price Sensitivity Analyzer` asks the four price
questions and gives the acceptable range.

## Before you start

1. **Look at the pages as a buyer, today.** Answer each check on what is visible now, not what
   is planned. "Not sure" scores zero; go and look.
2. **For a test, put the two prices on the same basis** (first month, first year, or first
   invoice) and pull conversion from at least a month of your own analytics.
3. **Write an honest guess at conversion at the test price.** The break-even line tells you how
   far it can fall before the new price loses revenue.
4. **Count the weeks you could keep a test clean.** Eight is AAJ's rule of thumb.

## Method

**Twenty-one checks in five areas** - clarity, choice, proof and risk, friction, honesty and
terms - each weighted 1 to 3 by what it costs a buyer (AAJ's judgement, not a benchmark). Yes
scores 2 points × weight, partly 1, no and not sure 0; unanswered checks are left out. Each page
gets a share of the weighted points available on the checks answered, and your fixes are ranked
by points lost and then by how many competitors already pass them.

**The honesty checks come first whatever they score.** In the US, ROSCA requires clear disclosure
of all material terms before billing information is taken, express informed consent, and a simple
way to stop recurring charges. California's automatic renewal law requires online cancellation for
online sign-ups and 7-30 days' notice of a change in the amount charged (contracts from 1 July
2025). The FTC's Guides Against Deceptive Pricing treat a fictitious former price as a false
bargain. The engine flags any of checks 18-20 that fail.

**Plan the test on revenue per visitor, not conversion.** Break-even conversion at the test price
is today's conversion × current price ÷ test price. The visitors needed per arm come from a
two-sided test on revenue per visitor at your alpha and power (0.05 and 0.8 by default), and are
converted to weeks at your traffic. The engine also reports the smallest change your traffic could
detect in the weeks you have. Then:

- **testable:** the weeks needed fit in the weeks you have. Run to the full size; never stop early
  because it looks good;
- **not testable:** use an alternative - ask before you charge, change it for new customers and
  compare whole-week periods, quote it in sales-led deals, or test a bigger change (the sample
  shrinks with the square of the effect);
- **guess says no:** your own guess already has the test price losing revenue;
- **nothing to detect:** both guesses give the same revenue per visitor.

**Read against the plan.** Conversion, revenue per visitor and a two-sided z-test p-value per arm.
Below the planned size the read-out is "too early", whatever the p-value says. Before-after and
sales-quote designs are marked not randomised and read as direction. A 90-day retention check
per arm is asked for before any price becomes permanent.

## Workflow

**Step 1 - Score.** Your page and up to three competitors on the 21 checks.

**Step 2 - Fix.** The honesty checks first, then the top five by points lost.

**Step 3 - Plan.** Run the test plan. If it is not testable, pick the alternative and write down
its weakness.

**Step 4 - Decide the rules before launch.** Keep the test price if revenue per visitor is higher
with p below alpha at the full size; keep the current price otherwise; stop early only on a
guardrail (refunds, cancellations, discount requests, support tickets about price).

**Step 5 - Read.** Give the engine both arms and the planned size. Then the retention check at 90
days.

## Run the tool

```
node resources/pricing-teardown.js --demo
```

`run({ teardown, testPlan, testRead })` returns the scored pages with area shares and ranked fixes,
the plan with break-even, visitors per arm, weeks, minimum detectable change and verdict, and the
read-out with p-value, progress against plan, verdict and retention note.

## Present the result

1. **The scores**, yours against each competitor, and the area where you lose most.
2. **The top five fixes**, with the honesty checks called out first.
3. **The test plan in one sentence**: break-even, visitors per arm, weeks, and the verdict.
4. **The read-out** against the planned size, and whether retention has been checked.

**Show where it came from.** Open your answer with "AAJ `pricing-page-teardown` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/pricing-page-teardown`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never test on existing customers.** Their prices change with notice, never as an experiment.
- **Never stop a test because it looks good.** Checking repeatedly and stopping at the first
  significant reading inflates false positives.
- **Never read conversion alone.** A price that attracts trials can still lose revenue.
- **Do not use a former price you never charged.** It is a false bargain under the FTC guides.
- **I am not a lawyer.** The legal checks point at the rules; check them, and local rules outside
  the US, before relying on any of it.

## Sources

- 15 U.S.C. § 8403, [Restore Online Shoppers' Confidence Act](https://www.law.cornell.edu/uscode/text/15/8403) - disclosure, consent and cancellation for negative-option features.
- Cal. Bus. & Prof. Code [§ 17602](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=BPC&sectionNum=17602.) - automatic renewal: notice of a change in charge; online cancellation.
- 16 CFR § 233.1, [Former price comparisons](https://www.law.cornell.edu/cfr/text/16/233.1) - FTC Guides Against Deceptive Pricing.
- NIST/SEMATECH e-Handbook, [7.2.2.2 Sample sizes required](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm) - the sample-size formula.
- Evan Miller, [How Not To Run An A/B Test](https://www.evanmiller.org/how-not-to-run-an-ab-test.html) - on stopping early.

## Related AAJ resources

- The workbook this skill runs, with the competitor grid and a 30-row test log: https://aajconsult.com/resources/pricing-page-teardown
- Asking before you charge: https://aajconsult.com/tools/price-sensitivity-analyzer
- What a price change does to ARPU: https://aajconsult.com/tools/pricing-arpu-modeler
- Designing the tiers in the first place: https://aajconsult.com/playbooks/pricing-packaging-playbook

## Related skills

- `pricing-and-packaging` - the tiers and the value metric the page presents
- `ab-test-significance` - the same test maths for conversion rather than revenue per visitor
- `website-conversion-audit` - the rest of the page around the price table
- `aaj-marketing-psychology` - anchoring and choice architecture, and where persuasion ends

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
