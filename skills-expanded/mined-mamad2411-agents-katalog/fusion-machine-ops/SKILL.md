---
name: fusion-machine-ops
description: >
  装置运营与放电设计 (fusion machine operations & discharge design). Route here when the task is to
  design a discharge or operating scenario, map an operating point, analyze or mitigate a disruption,
  or check operational limits and safety boundaries. Triggers (English + 中文): 放电设计 (discharge
  design), 放电场景 (discharge scenario), L-mode / H-mode / advanced scenario / hybrid scenario,
  运行空间 (operating space), 运行点 (operating point), 破裂 (disruption), 破裂前兆 (disruption
  precursor), VDE (vertical displacement event), 逃逸电子 (runaway electrons), 大量气体注入 MGI
  (massive gas injection), SPI (shattered pellet injection), 破裂缓解 (disruption mitigation),
  Greenwald 极限 (Greenwald limit), Troyon 极限 (Troyon limit), Hugill 图 (Hugill diagram), 运行限制
  (operational limits), 安全边界 (safety boundary), β_N vs n/n_GW, q_95 vs I_p, P_aux vs n_e.
---

# Fusion Machine Ops — 装置运营与放电设计

Use this skill to design discharges, map operating space, analyze/mitigate disruptions, and check
operational limits. Machine parameters have a single source of truth in
`../fusion-shared/core/machine-database.md` — always reference it, never re-type its numbers.

## Routing protocol (static/dynamic split)

1. **Load the manifest** `manifest.yaml` — read `always_load` (shared core + stance + workflow).
2. **Detect the `task` axis** from the user request against `axes.task.detect`.
3. **Load the matching fragment(s)** from `axes.task.values` (more than one may fire since `multi: true`).
4. **Run `static/core/workflow.md`** end-to-end, applying each loaded fragment's domain rules.
5. **Reach references on demand** per `references.on_demand` conditions; never preload them.
6. **Emit the deliverable** using `templates/discharge-plan.md` (design) or
   `templates/disruption-report.md` (disruption), as applicable.
