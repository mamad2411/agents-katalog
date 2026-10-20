---
tags: [backend, collection, routing, period]
name: collection-routing-by-period
description: Single resolver maps `(Period.Mode, from, to)` → time-series collection (raw view / 1-min / hour-with-monthly-suffix / day). Callers never hardcode collection names.
category: backend
version: 1.0.0
source_project: lucida-measurement
trigger: Time-series query picks between raw / hour / day collections or views based on range + interval.
---

See `content.md`.
