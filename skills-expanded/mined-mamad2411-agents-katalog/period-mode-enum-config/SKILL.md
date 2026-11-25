---
tags: [backend, period, mode, enum, config]
name: period-mode-enum-config
description: One enum `Mode` holds all (intervalMs, isFullData, dateFormat, retention, chartFormat) tuples for every time-series granularity — single source of truth across repository/service/chart layers.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Time-series app supports many modes (RAW/MIN_15/HOUR_3/MONTH_2); constants for interval/retention/format drift between layers.
linked_knowledge:
  - period-interval-naming-convention
---

See `content.md`.
