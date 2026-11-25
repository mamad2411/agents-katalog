---
name: sd
description: 启动 Speckit Delivery 的统一 SDD 路由。
disable-model-invocation: true
---

# SD

Use this human-invoked entry point for a delivery request. Read and execute the
canonical router at `../speckit-delivery/SKILL.md` before selecting a lane.

Keep `speckit-delivery` as the source of truth for routing and completion
conditions. `$sd` is only the memorable facade; it adds no lifecycle policy of
its own.
