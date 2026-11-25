---
name: aso-lint
description: Research, lint, and improve Apple App Store and Google Play listings with current platform rules, evidence-led keyword and competitor analysis, metadata optimization, localization, review synthesis, visual planning, and controlled experiments. Use for ASO audits, store metadata, app keywords, listing conversion, launches, updates, and experiment analysis. Includes a Rust linter.
tags: [general]
---

# ASO Lint

Improve app discovery and listing conversion without inventing market data.
Separate platform compliance, observed evidence, hypotheses, and measured results.

## Compose skills

Use `claude-seo` for evidence labels, current-source research, competitor/SERP
snapshots, content quality, prioritization, and measurement discipline. Use
`dev-browser` when store pages or visual assets require rendered inspection.
Missing tools do not block structural linting; label unavailable rank, volume,
download, review, or conversion data `setup required`.

## Establish scope

Record:

- platform: Apple, Google Play, or both;
- app identifier, market, locale, category, lifecycle stage, and release;
- current listing and proposed fields;
- product promise, audience, verified differentiators, and prohibited claims;
- first-party analytics, keyword/rank data, reviews, competitors, visual assets,
  and prior experiment results.

Generated keywords are hypotheses. Do not assign search volume, difficulty,
rank, downloads, benchmarks, or conversion lift without observed data.

## Verify rules

Read [references/platform-rules.md](references/platform-rules.md). Store policies
change. Recheck linked official Apple and Google sources before final compliance
claim. Update Rust rules only from authoritative evidence; add boundary tests
before changing limits.

## Run Rust linter

Runtime lives at `scripts/Cargo.toml`. Resolve it relative to installed
`SKILL.md`; use absolute manifest path. Rust/Cargo is required. First build uses
locked dependencies from local Cargo cache or crates.io.

Create a starter listing:

```bash
cargo run --quiet --locked --manifest-path <aso-manifest> -- \
  template --platform apple > listing.json
```

Lint one platform and locale per JSON file:

```bash
cargo run --quiet --locked --manifest-path <aso-manifest> -- \
  lint --input listing.json
```

Example Apple input:

```json
{
  "platform": "apple",
  "locale": "en-US",
  "name": "TaskFlow",
  "subtitle": "Plan less. Finish more.",
  "promotional_text": "New shared planning for focused teams.",
  "description": "Full product description",
  "keywords": "tasks,planner,focus,team",
  "whats_new": "Improved shared planning."
}
```

Exit `0` means required fields and enforced limits pass. Exit `2` means lint
findings. Output remains structural evidence—not App Review approval, ranking,
or conversion prediction. Apple keyword budget uses UTF-8 bytes.

## Research and optimize

1. Collect current store listings, reviews, visual assets, and first-party data.
   Record app ID/URL, locale, region, device, and capture time.
2. Build customer-language themes from observed reviews, support tickets, search
   data, and verified features. Exclude competitor marks, irrelevant terms, and
   unsupported superlatives.
3. Draft variants with one clear promise. Preserve natural language; avoid
   repeated keyword stuffing.
4. Lint every locale separately. Character counts do not replace store preview
   and submission validation.
5. Review first three screenshots as sequence: audience/problem, core outcome,
   differentiator/proof. Treat copy, order, and artwork as separate variables.
6. Prioritize by observed gap, expected mechanism, effort, risk, and measurement.

## Experiments

Change one major variable per test. Define hypothesis, primary metric, guardrails,
allocation, minimum run condition, and stop rule before launch. Analyze completed
two-variant counts:

```bash
cargo run --quiet --locked --manifest-path <aso-manifest> -- experiment \
  --control-conversions 120 --control-visitors 2000 \
  --variant-conversions 150 --variant-visitors 2000 --alpha 0.05
```

Rust output is a two-proportion z-test snapshot. Account for store experiment
method, sequential peeking, seasonality, multiple comparisons, novelty, and
traffic mix before rollout.

## Output

Return:

1. scope, sources, locale, region, and capture time;
2. structural lint report with stable rule IDs;
3. observed findings versus hypotheses;
4. before/after metadata with character or byte counts;
5. visual and localization plan;
6. experiment backlog with metrics, guardrails, and stop rules;
7. missing evidence, risks, owners, and next measurement.

This skill is adapted under MIT; see [NOTICE.md](NOTICE.md) and
[LICENSE.txt](LICENSE.txt).
