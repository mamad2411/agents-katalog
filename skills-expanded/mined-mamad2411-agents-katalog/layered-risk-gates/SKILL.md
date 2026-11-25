---
name: layered-risk-gates
description: Three-layer safety pattern for autonomous action loops — pre-action admission gate, in-flight monitor (stop/target thresholds), and a consecutive-failure circuit breaker — so a single runaway loop can't clear out the account before a human sees it.
category: arch
tags: [risk, circuit-breaker, safety, autonomous, limits, guardrails]
triggers: ["risk management", "position sizing", "max daily loss", "consecutive losses", "stop loss", "take profit", "kill switch", "circuit breaker"]
source_project: kis-java-bundle
version: 0.1.0-draft
---
