---
name: model-switch-cobuddy
title: Switch All Profiles to baidu/cobuddy:free [DEPRECATED — 2026-05-18]
description: MODEL ROUTING IS DEPRECATED. Cobuddy routing was stripped from root config and chief config during 2026-05-18 hardening. Chief now uses deepseek/deepseek-v4-flash:free. This skill exists for historical reference only.
version: 1.0.0
type: reference
status: deprecated
deprecated: 2026-05-18
category: ai
license: MIT
tested: not-applicable
tested_note: Historical reference only.
superseded_by: chief-execution-discipline (model routing section)
reason: cobuddy:free was a temporary experiment. Model routing now lives in chief config.yaml only. No cobuddy references remain in active configs.
created: 2026-05-18
tags:
  - model-routing
  - deprecated
  - cobuddy
  - historical
---

# Model Switch: All Profiles → baidu/cobuddy:free [DEPRECATED]

**⚠️ This skill is deprecated.** Cobuddy routing was stripped 2026-05-18. Chief now uses `deepseek/deepseek-v4-flash:free` via OpenRouter as the sole model. The root config's `model_routing` section with cobuddy overrides was removed during system hardening.

## Historical Record
Switched all 4 Hermes profiles from various models to `baidu/cobuddy:free` on OpenRouter.

## Before → After
| Profile | Previous Model | New Model |
|---------|---------------|-----------|
| chief | openrouter/owl-alpha | baidu/cobuddy:free |
| forge | deepseek/deepseek-v4-flash | baidu/cobuddy:free |
| intel | inclusionai/ring-2.6-1t | baidu/cobuddy:free |
| pulse | deepseek-v4-pro | baidu/cobuddy:free |

## Config Change
File: `/.hermes/config.yaml`
- `default_tier_1`: `inclusionai/ring-2.6-1t` → `baidu/cobuddy:free`
- All `profile_overrides` primaries → `baidu/cobuddy:free`

## Rationale
CoBuddy is a Baidu code-gen model optimized for agent workflows with high inference throughput and low latency. Free tier on OpenRouter provides cost-effective coverage across all profiles while maintaining quality.
