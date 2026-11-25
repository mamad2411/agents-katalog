---
name: split-test-designer
description: Define one interpretable outbound experiment with frozen account-level assignment, copy versions and outcome measures.
---

# Design one test

Read [the experiment example](../../../company/experiment.example.json), [assignment](../../../functions/assign_test_variant/function.json) and [analysis](../../../functions/analyse_results/function.json).

Write the hypothesis before seeing outcomes. Define the eligible company/persona cohort, randomisation unit, two variant IDs, one changed dimension, fixed fields, observation window, primary metric and review trigger. A CTA comparison is a useful starting point when the offer and audience are already credible; it is not a universal rule.

Use `assign_test_variant` with the canonical account key. Freeze test_round, group_id, variant order and assignment algorithm for the round. Colleagues in one account receive the same variant. Keep prompt_version on every generated message and outcome.

Write both variants using `outbound-copywriter`; keep everything outside the tested dimension fixed. Avoid spintax on the test variable. Sender, timing and source differences can confound the result; record them.

Measure delivered enrollments, positive replies and meetings with deduplicated event IDs. State definitions and attribution window. Small-sample results remain descriptive; the example floor is a review trigger, not a significance calculation. Account-level assignment also means outcomes from colleagues are not independent observations.

Deliver a saved test plan and variant bodies. After results, use `analyse_results` for descriptive counts, document limitations and propose one next change. Do not automatically overwrite ICP or declare a winner from the larger raw reply count.
