---
name: godot-mcp-verify-loop
description: "验证闭环 run_and_verify validate_scripts verify_delivery read_scene edit_script 交付门禁 编译 跨文件依赖 parse error 场景树完整性 —— 当你改完代码/场景需要验证或交付前自检时使用"
---

## 改 → 跑 → 验证闭环

把"理解 → 改 → 跑 → 编译验证 → 交付门禁"串成 checklist，避免只跑一种验证就交付。工具细节见 `godot-mcp-core.md`。

**何时用**：改完代码/场景后需要验证、交付前自检时。

**checklist**：
- [ ] 1. `read_scene` / `read_script` — 理解现有结构（属性类型解析）
- [ ] 2. `edit_script`（**search_and_replace 优先**）/ `write_script` — 修改
- [ ] 3. `run_and_verify(capture_tree=true)` — headless 跑 + 结构化错误分析（自动识别 autoload 相关 headless_limitation）
- [ ] 4. `validate_scripts` — 触发 Godot 完整 `load()` 编译（含**跨文件依赖**，捕 headless 运行遗漏的 Parse Error）
- [ ] 5. `verify_delivery` — 交付门禁（场景树完整性 + 脚本健康 + 性能 + 自定义断言 + GDD 合规）

**常见偏离**：
- 只跑 `run_and_verify` 不跑 `validate_scripts`（漏跨文件编译错误——两者可能不一致，以 run_and_verify 实跑为准但 validate_scripts 补跨文件依赖）
- 运行时工具（signal/tilemap/particles 等）误认为持久化（headless 退出即丢失，持久化须 add_node + save_scene）
- 忘记 `_mcp_done()`（execute_gdscript 片段模式超时）
