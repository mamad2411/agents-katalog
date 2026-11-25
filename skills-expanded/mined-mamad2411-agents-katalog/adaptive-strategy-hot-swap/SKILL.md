---
name: adaptive-strategy-hot-swap
description: Periodically re-evaluate candidate strategies/policies against recent data, swap the active one only when a weighted composite score beats the incumbent by a hysteresis threshold — prevents flapping while staying adaptive.
category: arch
tags: [strategy, adaptive, hot-swap, hysteresis, rebalance, composite-score, backtest]
triggers: ["shouldUpdateStrategy", "reanalyze", "strategy update", "hot swap", "policy rotation", "best strategy", "composite score", "hysteresis threshold"]
source_project: kis-java-bundle
version: 0.1.0-draft
---
