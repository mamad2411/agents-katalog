---
name: godot-router
description: "godot-mcp skill 路由器 不确定用哪个流程 入口匝道 决策树 E2E 安全编辑 验证闭环 动画审计 —— 当你不确定该用哪个 godot-mcp 流程、或需要把任务分发到具体子流程时使用。简单单工具操作(改单行/单次截图)不要用本 skill,直接调工具"
---

## godot-mcp 流程路由

本 skill 是 godot-mcp skill 体系的路由器。当你不确定该用哪个流程时,按以下决策树分发。

**何时用**:用户请求模糊(如"帮我改场景""验证一下"),或一个任务跨多个 skill 时。

**主流程(想法 → 可交付)**:
- [ ] 1. 改代码/场景 → 先 screenshot-verify 留证,再 godot-mcp-safe-edit 编辑,收尾 godot-mcp-verify-loop 验证
- [ ] 2. 不确定怎么改 → 用 game 工具的 game_query action 读真实运行时值,不要纸面猜
- [ ] 3. 批量建节点/文件 → 走 godot-mcp-safe-edit 的 batch 路径

**入口匝道(按任务类型分流)**:
- [ ] E2E 测试 / 模拟输入 / 回归测试 → `godot-mcp-bridge-e2e`
- [ ] 动画/动效不对劲(卡顿/无弹性/方向反)→ `godot-tween-taste`
- [ ] 视觉验证(操作前后截图对比)→ `screenshot-verify`
- [ ] 安全编辑(.gd/.tscn 改动)→ `godot-mcp-safe-edit`
- [ ] 交付前自检 → `godot-mcp-verify-loop`

**何时不用 skill**:
- 改单行 .gd → 直接 `edit_script`
- 只读探索(看场景结构)→ 直接 `read_scene` / `game_query`
- 单次截图 → 直接 `screenshot`

**常见偏离**:
- 每个操作都走路由器(过度:简单操作直接调工具,路由器只在不确定时用)
- 路由后不验证(漏:即使路由器分发,收尾仍需 verify-loop 或 screenshot-verify)