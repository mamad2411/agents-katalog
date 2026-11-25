---
name: godot-mcp-bridge-e2e
description: "bridge e2e 运行时验证 game_bridge_install run_project wait_for_bridge game_query ping game_input game_wait take_screenshot frame-verify 录制 回归测试 输入模拟 —— 当你需要验证运行时行为、做 E2E 测试、模拟输入或回归测试时使用"
---

## 运行时验证 / E2E 流程

把"安装 Bridge → 启动游戏 → 连接 → 模拟输入 → 留证"串成可遵循的 checklist，避免遗漏前置步骤。工具细节见 `godot-mcp-bridge.md` 与 `godot-mcp-recording.md`。

**何时用**：需要验证运行时行为、做 E2E 测试、模拟输入、回归测试、Bug 复现时。

**checklist**：
- [ ] 1. `game_bridge_install(project_path)` — 一次性安装 Bridge autoload（端口 9081，写 project.godot）
- [ ] 2. `run_project(project_path, wait_for_bridge=true)` — 启动游戏并等 Bridge 就绪（`bridge_timeout` 默认 10s）
- [ ] 3. `game_query(method="ping")` — 确认连接（期望 `status: "ok"`）；未连排查：未 install / 游戏没运行 / 密钥权限
- [ ] 4. 操作 + 验证：`game_input`（send_key/send_mouse_click/send_text）模拟输入 → `game_wait`（wait_for_node/wait_for_property）等状态变化
- [ ] 5. 留证：`take_screenshot`（**GPU viewport 真渲染**，非 headless 空白）/ 或 `frame-verify`（反作弊退化检测）

**常见偏离**：
- 忘记 `game_bridge_install`（query/input 直接报 BRIDGE_NOT_CONNECTED）
- 游戏没运行就 query（Bridge 只在游戏运行时监听）
- 用 headless `screenshot` 做运行时视觉确认（headless 用 RendererDummy，2D/3D 均空白）→ 必须用 bridge `take_screenshot`
- 节点路径不用绝对路径（`game_write`/`game_wait` 的 `path` 必须以 `/root/` 开头）
