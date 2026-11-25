---
name: evolve-bug-fix-may18
title: Evolve Bug Fix — strategy_name Key Mismatch
description: Root cause analysis and fix for KeyError on strategy_name during trade logging
version: 1.0.0
type: reference
status: active
created: 2026-05-18
category: development
license: MIT
tested: runtime
tested_note: Skill documents a verified production fix; creator provenance needs manual review.
tags:
  - bug-fix
  - strategy-learner
  - key-mismatch
  - sandbox
---

# Evolve Bug Fix — `strategy_name` Key Mismatch (May 18, 2026)

## Problem
The `strategy_learner.py` `log_trade()` function extracted the strategy name with:
```python
strategy_name = trade.get("strategy_name", "default")
```

But the sandbox (`sandbox.py`) and unified launcher (`hermes_trading.py`) passed the key as `"strategy"`:
```python
{"action": "log", "trade": {"strategy": "owl-alpha-v3", ...}}
```

Result: Every trade landed in the `"default"` bucket. When `evolve` was called with `"owl-alpha-v3"`, it returned:
```json
{"status": "not_found", "message": "Strategy 'owl-alpha-v3' not found in database."}
```

## Fix
Accept either key with fallback chain:
```python
strategy_name = trade.get("strategy_name") or trade.get("strategy", "default")
```

## Lesson
When multiple modules share trade data via JSON, explicitly document the expected key names. Use a shared schema or at minimum a comment listing accepted key variants.
