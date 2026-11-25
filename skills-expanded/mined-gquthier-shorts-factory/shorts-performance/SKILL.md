---
name: shorts-performance
description: Analyze channel-specific short-video performance and outliers to guide the next clips in Shorts Factory. Use for format/topic comparisons, metric selection or research.
---

# Shorts Performance

Read `src/lib/performance.ts` and `docs/research.md`. Distinguish views, impressions, reach, complete interactions and unavailable metrics. Use the most recent snapshot per publication; do not sum historical snapshots. Compare formats and subjects within a channel.

Performance signals need three mature clips per side; hook feedback needs five per type and five comparison clips. A mature publication is at least 72 hours old. These are exploratory signals, not significance tests. Track publication age and the chosen metric.

For external accounts, compare each candidate with the median of at least 12 other same-account posts within ±60 days, excluding pinned/declared partnerships from the baseline. Examine actual openings and normal-performing controls. Public views cannot establish paid/organic distribution, retention or causality. Preserve source URLs and observation dates in local research.

Freeze the filters and evidence used for idea generation. Never turn another creator’s reported result into the user’s claim. Missing data is unknown, never zero. Run performance tests and `python3 -m unittest discover -s test -p '*_test.py'`.
