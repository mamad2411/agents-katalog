---
name: browser-bridge
description: 通过 antigravity-browser-bridge MCP 控制浏览器：普通任务默认走 isolated（headless:true）后台静默引擎（零弹窗、不切换日常页面、不抢焦点、多会话并发）；需要复用本机日常已登录 Edge/Chrome 或 RPA 录制回放时显式使用 mode="extension"。多开 Antigravity 会话时由 Leader/Follower 自动中继。
---

# Browser Bridge（双轨浏览器控制）

`antigravity-browser-bridge` 采用双轨架构（本地桥接端口默认 `127.0.0.1:8767`）：

- **默认后台轨（`mode="isolated"`, `headless=true`）**：基于独立 `user-data-dir` 无头驱动本机 Edge/Chrome，适合日常网页读取、表单填报、测试、截图与多 Agent 并发；无黄色调试条、不创建可见窗口、不切换用户当前页面、不抢系统焦点。
- **显式可见扩展轨（`mode="extension"`）**：仅在明确需要操作用户日常已登录的 Edge/Chrome 标签页，或执行 RPA 录制/回放（`browser_record_start` / `browser_record_stop` / `browser_record_list` / `browser_record_replay`）时显式选择。

## 标准工作流（默认静默后台）

1. **直接执行后台操作**：调用 `browser_launch`（可选，默认 `mode="isolated", headless: true`）或直接 `browser_open`，后续调用无需再传 `mode`。如需核实模式/窗口来源，调 `browser_status` 检查返回里的 `mode`、`headless`、`sessionId` 与 `instanceReused`。
2. **`browser_snapshot`（建议 `compact: true`）**：获取页面结构与确定性 `ref`（支持穿透 iframe 与 open Shadow DOM）；禁止凭猜测点坐标。
3. **`browser_click` / `browser_type` / `browser_press` / `browser_select_option`**：优先传 `ref`，其次 `selector` / `text`。页面跳转或局部重渲染后重新 `browser_snapshot`。
4. **登录态与异常边界**：
   - 普通导航失败会直接返回 `NAVIGATION_FAILED`，不会自动打开可见登录窗、扩展安装页或切换到可见模式。
   - 遇到登录失效或验证码时返回 `awaiting_user_login` / `pending_captcha` 待处理状态；如需给隔离环境登录，只能显式调用 `browser_auth_sync` 或 `browser_open_auth_window(action="open")`，并在完成后调 `action="complete"` 切回无头模式。
   - 若请求后台模式但已有可见实例运行，会返回 `MODE_CONFLICT` 及恢复指引，绝不会强行关闭其他任务的窗口。
5. **需要操作日常浏览器或录制时**：显式调用 `browser_launch(mode="extension")`（仅本次实际启动/连接成功后，该会话后续省略 `mode` 的调用会保持在 `extension` 轨；`dryRun: true` 或失败不会改写会话模式）。切回后台时显式调 `browser_launch(mode="isolated")`。

## 工具速查

| 目的 | 工具 |
| --- | --- |
| 启动 / 校验引擎并设置会话轨 | `browser_launch`（默认 `isolated + headless:true`） |
| 模式、无头状态、会话与标签页列表 | `browser_status` |
| 标签页列表 / 切换 / 新建 / 关闭 | `browser_tabs` |
| 打开网址或搜索 | `browser_open` |
| 前进 / 后退 / 刷新 | `browser_history` |
| 结构化快照（带 ref，穿透 iframe/Shadow） | `browser_snapshot` |
| 点击 / 输入 / 按键 / 悬停 / 滚动 | `browser_click`、`browser_type`、`browser_press`、`browser_hover`、`browser_scroll` |
| 下拉选择 / 取文本 / 执行 JS / 等待 | `browser_select_option`、`browser_get_text`、`browser_evaluate`、`browser_wait_for` |
| 截图 / 控制台 / 网络 | `browser_screenshot`、`browser_console`、`browser_network` |
| 隔离态登录同步 / 一次性手动登录窗 | `browser_auth_sync`、`browser_open_auth_window` |
| RPA 录制开启 / 结束 / 查询 / 快放 | `browser_record_start`、`browser_record_stop`、`browser_record_list`、`browser_record_replay` |

## 扩展未安装时（仅 `mode="extension"` 需要）

`browser_launch(mode="extension")` 失败时会在返回字段给出扩展目录（`<插件根>\extension`）与安装步骤；普通后台模式无需安装扩展即可直接运行。

## 多会话与端口

- 第一个 MCP 进程是 Leader，独占 `127.0.0.1:8767` 并托管共享无头引擎与会话模式映射（按 `sessionId` 隔离）；后续进程自动成为 Follower 经 `POST /rpc` 中继。
- Leader 退出后 Follower 会在下次调用时自动接管端口，无需人工杀进程抢端口。
- 密码、OTP 与银行卡敏感字段默认受安全策略拦截；提交/删除/支付等不可逆操作前先确认。
- 验证启动参数而不开窗或切换会话模式时使用 `dryRun: true`。
