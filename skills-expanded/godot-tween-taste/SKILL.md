---
name: godot-tween-taste
description: "Tween 动效品味审计 create_tween tween_property set_trans set_ease TRANS 类型 Ease 方向 时长 弹性 卡顿 方向反 只读不改 自包含修复计划 advisor —— 当你用 Tweener、Tween 动效不对劲(卡顿/无弹性/方向反)、或需要审计 Tween 品质时使用。改单行 Tween 值用 edit_script 即可"
---

## Tween 动效品味审计(advisor-worker 模式)

本 skill 是 advisor(只读不改源码),扫描 Tween 调用按品味审计,产出自包含修复计划给 worker 执行。借鉴 emilkowalski improve-animations 的 4 Phase 工作流。

**何时用**:Tween 动效"不对劲"(卡顿/无弹性/方向反/生硬)、批量审计 Tween 品质、用 Tweener 时想确认 TRANS/Ease 选择合理。

**Phase 1 — Recon(只读,摸清 Tween 地图)**:
- [ ] 1. `read_scene` + grep `create_tween|tween_property|set_trans|set_ease` 找所有 Tween 调用
- [ ] 2. 记录每处:file:line + TRANS 类型 + Ease 方向 + 时长 + 目标属性

**Phase 2 — Audit(按 7 类审计,只返回 file:line + evidence)**:
- [ ] 3. TRANS_LINEAR 用于 UI 动画(生硬,应换 TRANS_SINE/QUAD)
- [ ] 4. Ease 缺失(默认 ease_in_out 可能不对,UI 进场应用 ease_out)
- [ ] 5. 时长 < 0.1s(太快看不清)或 > 1.0s(太慢拖沓)
- [ ] 6. parallel() 缺失(多 Tween 应并行但串行跑了)
- [ ] 7. Tween 未 kill(场景切换后泄漏,应 connect tree_exited)

**Phase 3 — Vet & prioritize(剔除误判)**:
- [ ] 8. 重读每条 finding,剔除 by-design(如 LoadingScreen 故意用 LINEAR)
- [ ] 9. 按 leverage 排序(影响用户体验大的优先)

**Phase 4 — Write plans(自包含修复计划)**:
- [ ] 10. 每条 finding 写一个 plan,内联精确值(如"TRANS_LINEAR → TRANS_SINE,Ease In → Ease Out,0.05s → 0.3s")
- [ ] 11. plan 交接给 worker(任何 agent),按 plan 用 edit_script 逐条修

**常见偏离**:
- advisor 直接改源码(越界:advisor 只读,改是 worker 的事)
- plan 写模糊指令(漂移:必须内联精确值,不允许"用更柔和的 easing")
- 把 by-design 当 bug 报(噪声:先 Vet 剔除故意的妥协)