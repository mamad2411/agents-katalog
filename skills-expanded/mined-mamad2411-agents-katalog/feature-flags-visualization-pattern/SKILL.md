---

name: feature-flags-visualization-pattern
description: Visualization pattern for feature-flag rollout, dependency, and A/B experiment dashboards
category: design
triggers:
  - feature flags visualization pattern
tags: [design, feature, flags, visualization, dashboard]
version: 1.0.0
---

# feature-flags-visualization-pattern

Feature-flag UIs cluster around three canonical views that share a common visual grammar: a rollout progress strip (percentage bar segmented by cohort/variant with color-coded states — off/canary/partial/full), a dependency graph (directed nodes where parent flags gate children, with edge labels showing the boolean condition like `requires=ON` or `variant=B`), and an A/B experiment panel (side-by-side variant cards showing exposure count, conversion rate, and a confidence-interval bar). Use a consistent flag-state palette across all three: gray=OFF, amber=PARTIAL/ROLLING, green=ON, blue=EXPERIMENT, red=KILL-SWITCH — so a user jumping between screens can read state at a glance.

Layout rule: put the flag identifier (key + environment badge) as a sticky header on every flag-scoped view, because flag keys are the only stable join across rollout/dependency/experiment screens. For the dependency graph specifically, render cycles as red dashed edges and highlight orphan flags (no parents, no children) in a side list — these are the two structural problems ops actually need to find. For rollout, overlay the target percentage as a ghost bar behind the actual-exposure bar so drift is visible without a second chart.

Interactive affordances that recur: click-a-flag-node-to-pin-context (all other panels filter to that flag), hover-variant-to-see-sample-size (avoids misreading a 2-user "100% conversion"), and a time scrubber that replays the rollout history — flags change frequently, so a static snapshot hides the most useful signal (who turned what on, when).
