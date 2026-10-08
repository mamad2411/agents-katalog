## 项目概述

Browser Brain Loop：浏览器侧 AI Agent 系统。大脑（Kernel Engine + Loop Controller）运行在 Chrome 扩展的 Service Worker 中，SidePanel 提供对话 UI，本地 Bun WebSocket 服务（Bridge）仅做执行代理，提供 `read/write/edit/bash` 四个工具。

**架构铁律：大脑永远在浏览器侧，本地 WS 只做执行代理，不做任务决策。**

Kernel 引擎（50 个模块）聚合在 `BrainOrchestrator` 单例中，详见 [docs/kernel-architecture.md](docs/kernel-architecture.md)。

## 项目级系统提示词约束（Legacy/Fallback）

- 在本项目中进行功能开发或写代码时，**完全不要考虑 Legacy/Fallback 方案**，默认按目标态实现。
- 一旦发现现存的 Legacy/Fallback 路径，**必须立即询问用户是否删除**，未经确认不得继续沿用或扩展该路径。

## 项目级系统提示词约束（注入脚本）

- 所有注入到网页执行环境的脚本都必须按“单文件自包含”设计与交付，包括：
  - `manifest.json > content_scripts`
  - `chrome.scripting.executeScript` 注入文件
  - `world: "MAIN"` 的 page hook / injected script
- 这些脚本的最终产物**禁止**出现顶层 `import` / `export`、共享 chunk 依赖、运行时模块加载器假设。默认心智模型是“浏览器会把它当普通脚本直接执行”，不是 ESM 宿主。
- 如果确实需要复用逻辑，优先选择：
  - 在注入脚本内保留一份小型自包含实现
  - 或调整构建，使该入口最终产出单文件 bundle
- 禁止直接从注入脚本入口 import 共享模块后期待构建器“自动处理”；这在本项目里默认视为高风险错误。
- 任何涉及注入脚本的改动，完成前必须做两个校验：
  - 构建后检查对应 `dist/assets/*.js` 入口文件头部，确认没有顶层 `import` / `export`
  - 确认 `manifest` 或注入调用引用的就是该可直接执行的产物

## 外部参考仓库（设计对齐）

### Pi monorepo — Agent Core + LLM Provider

固定位置：`~/work/repos/_research/pi-mono/`

关键参考路径：
- `packages/ai/` — 统一消息模型 + Provider 双层
- `packages/coding-agent/src/core/model-registry.ts` — Model Registry
- `packages/coding-agent/docs/custom-provider.md` — 自定义 Provider 文档
- `packages/ai/src/providers/transform-messages.ts` — Message 变换

对齐要点：统一消息模型（role/content/tool_call）、Provider 双层（Adapter + Registry）、Model Registry 自动发现、Message 变换管道。

### AIPex — 浏览器自动化

固定位置：`~/work/repos/_research/AIPex/`

关键参考路径：
- `packages/browser-runtime/src/tools/` — 工具实现
- `packages/browser-runtime/src/automation/` — 自动化引擎
- `packages/browser-runtime/src/automation/snapshot-manager.ts` — 快照策略（CDP/DOM/auto）
- `packages/browser-runtime/src/utils/dom-snapshot.ts` — Content Script DOM 快照
- `packages/browser-runtime/src/utils/dom-action.ts` — DOM 合成事件执行
- `packages/browser-runtime/src/automation/debugger-manager.ts` — CDP debugger 生命周期

对齐要点：UID 元素定位、A11y-first 快照、双模式执行（semantic/coordinate）、Post-action stabilization。

**Background Mode 对齐**：BBL 的后台自动化模式参考 AIPex 的 5 层隔离机制实现，设计文档见 [docs/background-mode-design-2026-06.md](docs/background-mode-design-2026-06.md)。核心模块：
- `automation-mode.ts` — focus/background 状态管理
- `content/dom-snapshot-collector.ts` — Content Script DOM 快照（对标 AIPex `dom-snapshot.ts`）
- `dom-locator.ts` — DOM 操作执行器（对标 AIPex `dom-action.ts`）
- `background-failure-tracker.ts` — 连续失败追踪，3 次后附加 upgradeHint
- `stealth-tab.ts` — minimized window 隐身 tab（background 模式创建的 tab 对用户不可见）
- `runtime-infra.browser.ts` — snapshot/action 路由按 mode 分支 + mixed fallback（不支持的 action 降级 CDP）
- `runtime-loop.browser.ts` — background 模式过滤 screenshot/computer 工具

## 常用命令

```bash
# 一键开发（bridge + extension watcher）
BRIDGE_TOKEN="<token>" bun run brain:dev

# 单独启动 bridge
cd bridge && bun install && BRIDGE_TOKEN="<token>" bun run start

# 扩展构建
cd extension && bun run build

# 扩展热重载 watcher
BRIDGE_TOKEN="<token>" bun run brain:ext:watch

# Bridge 类型检查 + 单元测试
bun run check:brain-bridge

# 扩展测试（Vitest browser mode）
cd extension && bun run test

# Bridge 测试
cd bridge && bun test
cd bridge && bun test test/fs-guard.test.ts

# 类型检查
cd bridge && bunx tsc --noEmit

# E2E（纯 CDP，无 Playwright）
bun run brain:e2e
BRIDGE_TOKEN="<token>" bun run brain:e2e:live
CHROME_BIN="/path/to/chrome" bun run brain:e2e
BRAIN_E2E_HEADLESS=true bun run brain:e2e

# CDP 直连调试（连接用户正在使用的 Chrome）
# 推荐先启持久连接，后续所有检查都走同一条 CDP 会话
bun tools/cdp-debug.ts serve &
curl http://127.0.0.1:9333/targets
curl http://127.0.0.1:9333/dom
curl -X POST http://127.0.0.1:9333/eval -H 'Content-Type: application/json' -d '{"expr":"document.title"}'

# 直接模式（仅限一次性单步检查；Chrome M144+ 会重复弹 Allow）
bun tools/cdp-debug.ts targets              # 列出所有 Chrome 目标
bun tools/cdp-debug.ts screenshot           # 截图 SidePanel
bun tools/cdp-debug.ts dom                  # SidePanel DOM 概览
bun tools/cdp-debug.ts eval 'document.title' # 在 SidePanel 执行 JS
bun tools/cdp-debug.ts chat '你好'           # 在 SidePanel 发消息
bun tools/cdp-debug.ts sw-eval 'self.registration.scope' # SW 中执行 JS

# BDD 契约校验 + 门禁
bun run bdd:validate && bun run bdd:gate
bun run bdd:gate:live
```

live LLM 环境变量（用于 `brain:e2e:live`）：

```bash
BRAIN_E2E_LIVE_LLM_BASE="https://ai.chen.rs/v1"
BRAIN_E2E_LIVE_LLM_KEY="<key>"
BRAIN_E2E_LIVE_LLM_MODEL="gpt-5.3-codex"
# 可选：BRAIN_E2E_LIVE_ATTEMPTS=3 BRAIN_E2E_LIVE_MIN_PASS=2
```

## AI Agent 调试扩展指南

### 前置条件
Chrome Beta（≥ 144）需先在 `chrome://inspect/#remote-debugging` 启用远程调试。启用后 Chrome 会在 `~/Library/Application Support/Google/Chrome Beta/DevToolsActivePort` 写入端口和 WebSocket 路径。

如果机器上同时有多套 Chrome user-data-dir / profile 容器，不要默认猜测。优先显式指定：

```bash
CHROME_USER_DATA_DIR="/absolute/path/to/user-data-dir" bun tools/cdp-debug.ts targets
# 或更底层地直接指定
CHROME_DEVTOOLS_ACTIVE_PORT_FILE="/absolute/path/to/DevToolsActivePort" bun tools/cdp-debug.ts targets
```

### CDP 直连工具 (`tools/cdp-debug.ts`)

本工具通过 CDP WebSocket 直连用户正在使用的 Chrome，可完整访问所有扩展目标：

#### 推荐：持久服务模式（避免重复 Chrome 授权弹窗）

每次直接运行 `bun tools/cdp-debug.ts <cmd>` 都会新建 WebSocket 连接，Chrome M144+ 每次新连接都弹授权框。使用 `serve` 模式只需授权一次：

```bash
# 1. 后台启动持久服务（只弹一次授权窗口）
bun tools/cdp-debug.ts serve &

# 2. 通过 HTTP 发送命令，不再弹窗
curl http://127.0.0.1:9333/targets
curl http://127.0.0.1:9333/screenshot > /tmp/ss.png
curl http://127.0.0.1:9333/dom
curl -X POST http://127.0.0.1:9333/eval -H 'Content-Type: application/json' -d '{"expr":"document.title"}'
curl -X POST http://127.0.0.1:9333/sw-eval -H 'Content-Type: application/json' -d '{"expr":"self.registration.scope"}'
curl -X POST http://127.0.0.1:9333/chat -H 'Content-Type: application/json' -d '{"message":"你好"}'
```

**Agent 强制规则**：
- 同一轮里只要预期会做 `2` 次及以上浏览器检查/点击/轮询，必须先启动 `serve`，后续全部复用 `http://127.0.0.1:9333`。
- 非必要不要重复运行 `bun tools/cdp-debug.ts eval/dom/chat/...` 这种一次性命令；它们每次都会新建 CDP 连接，造成重复 `Allow`。
- 需要复杂 DOM 调试时，优先保持一条长连接完成整套动作，不要每一步都重新 attach。
- 进入扩展调试前，先调用 `/targets` 确认当前 SidePanel / Service Worker target；**不要硬编码扩展 ID 或旧的 `chrome-extension://...` URL**，因为扩展重装后 ID 可能变化。
- 机器上存在多套 Chrome 数据目录时，必须先显式设置 `CHROME_USER_DATA_DIR` 或 `CHROME_DEVTOOLS_ACTIVE_PORT_FILE`，再启动 `serve`；不要让工具自己猜“哪套 profile”。
- 如果已经有 `serve` 进程在跑，优先复用现有 `9333` 连接；不要重复启动新的持久服务实例。

#### 直接模式（每次都弹授权窗口，简单场景可用）

| 命令 | 用途 | 示例 |
|------|------|------|
| `targets` | 列出所有 Chrome target | `bun tools/cdp-debug.ts targets` |
| `screenshot` | 截图 SidePanel（或指定 target） | `bun tools/cdp-debug.ts screenshot --target sw` |
| `dom` | 获取 SidePanel DOM 概览 | `bun tools/cdp-debug.ts dom` |
| `eval` | 在 SidePanel 执行 JS | `bun tools/cdp-debug.ts eval 'document.title'` |
| `chat` | 发消息并等待回复 | `bun tools/cdp-debug.ts chat '你好'` |
| `sw-eval` | 在 Service Worker 中执行 JS | `bun tools/cdp-debug.ts sw-eval 'self.registration.scope'` |

**目标过滤器**（用于 `--target`）：`sidepanel`（默认）、`sw`、`sandbox`、或 URL/标题子串。

### Bridge HTTP API 调试

Bridge（端口 8787）暴露内核诊断数据：

```bash
# 列出诊断导出
curl 'http://127.0.0.1:8787/api/diagnostics?token=<BRIDGE_TOKEN>'
# 列出调试快照
curl 'http://127.0.0.1:8787/api/debug-snapshots?token=<BRIDGE_TOKEN>'
# 下载具体诊断
curl 'http://127.0.0.1:8787/api/diagnostics/<id>?token=<BRIDGE_TOKEN>'
```

Session Diagnostics（`bbl.diagnostic.v4`）包含：`summary`（运行状态/步数/最后错误）、`timeline`（步骤执行轨迹）、`eventTypeCounts`、`sandbox`/`agent`/`llm`/`tools` trace。

### AI Agent 调试工作流

1. **UI 问题** → 先 `bun tools/cdp-debug.ts serve &` → 用 `curl /targets|/dom|/eval|/screenshot` 复用持久连接 → 分析 → 修改代码 → 继续复用同一连接验证
2. **内核问题** → Bridge API 下载诊断 → 分析 `summary.lastError` 和 `timeline` → 定位根因
3. **全链路** → 持久连接下调用 `/chat` 发消息 → 同时下载当次的 Bridge 诊断 → 前后对比

### 技术原理

CDP 直连绕过 `chrome-devtools-mcp` 的 autoConnect 握手，直接从 `DevToolsActivePort` 读取 WebSocket URL。通过 `Target.attachToTarget(flatten: true)` 获取 sessionId，再用 sessionId 范围内的 `Page.captureScreenshot`、`Runtime.evaluate` 等 CDP 命令操作指定 target。

扩展 ID：`jhfgfgnkpceegbkojajfadeijojekgod`（仅当前机器最近一次观测值，调试时仍以 `/targets` 实时结果为准）  
SidePanel 输入框：`<textarea placeholder="/技能 @标签">`  
发送按钮：`<button aria-label="发送消息">`

## 架构

```
browser-brain-loop/
├── bridge/              # Bun 本地 WS 服务 (ws://127.0.0.1:8787)
│   └── src/
│       ├── server.ts         # Bun.serve WS 入口，认证/并发控制/审计
│       ├── dispatcher.ts     # invoke 分发到 tools/
│       ├── config.ts         # 环境变量配置
│       ├── cmd-registry.ts   # bash 命令白名单
│       ├── fs-guard.ts       # 路径守卫（god/strict）
│       ├── protocol.ts       # WS 帧解析
│       └── tools/            # read/write/edit/bash
├── extension/           # MV3 Chrome 扩展（Vite 8 + Vue 3 + TS）
│   ├── src/
│   │   ├── background/
│   │   │   └── sw-main.ts         # Service Worker 入口 → BrainOrchestrator + RuntimeRouter
│   │   ├── content/
│   │   │   └── dom-snapshot-collector.ts  # Content Script: DOM 快照采集（background mode）
│   │   ├── panel/
│   │   │   ├── main.ts            # SidePanel Vue app
│   │   │   ├── plugin-studio-main.ts  # Plugin Studio 入口
│   │   │   ├── components/        # Vue 组件（Chat/Settings/Plugins/Skills/...）
│   │   │   ├── stores/            # Pinia stores
│   │   │   └── utils/             # UI 工具函数
│   │   └── sw/kernel/             # Kernel 引擎（50 模块）→ docs/kernel-architecture.md
│   │       ├── orchestrator.browser.ts    # BrainOrchestrator 单例
│   │       ├── runtime-loop.browser.ts    # LLM loop 引擎
│   │       ├── runtime-router.ts          # SW 消息路由
│   │       ├── automation-mode.ts         # 自动化模式状态管理（focus/background）
│   │       ├── dom-locator.ts             # DOM 操作执行器（background mode, chrome.scripting）
│   │       ├── background-failure-tracker.ts # 后台模式连续失败追踪（auto-upgrade hint）
│   │       ├── stealth-tab.ts             # 隐身 tab 管理（minimized window，background 模式用）
│   │       ├── tool-contract-registry.ts  # 工具 Schema（45 内置）
│   │       ├── tool-provider-registry.ts  # 工具执行层
│   │       ├── plugin-runtime.ts          # 插件系统
│   │       ├── skill-registry.ts          # Skill 管理
│   │       ├── virtual-fs.browser.ts      # mem:// 虚拟文件系统
│   │       └── ...                        # 其余 23 个模块
│   ├── vite.config.ts   # 5 入口：sidepanel / debug / plugin-studio / service-worker / dom-snapshot-collector
│   └── manifest.json
├── bdd/                 # 行为契约驱动开发
│   ├── contracts/       # BHV-* 契约 JSON
│   ├── features/        # Gherkin .feature
│   ├── mappings/        # contract-to-tests.json
│   ├── schemas/         # JSON Schema
│   └── evidence/        # e2e 证据
└── tools/               # 构建/测试/门禁脚本
```

## Kernel 概要

Kernel 引擎（`extension/src/sw/kernel/`）由 `BrainOrchestrator` 聚合 6 大子系统，详见 [docs/kernel-architecture.md](docs/kernel-architecture.md)：

- **Orchestrator**：Session 生命周期 + RunState 状态机（running/paused/stopped/compacting/queue）
- **Tool 双层**：ToolContract（Schema，46 内置工具）+ ToolProvider（执行，3 种 mode: script/cdp/bridge）
- **LLM Provider**：`LlmProviderAdapter` 接口 + OpenAI-compatible 默认实现 + Profile 多路由 + 升级策略
- **Plugin 系统**：`AgentPluginDefinition` + 权限模型 + 卸载自动恢复 + Plugin Studio
- **Skill 系统**：IndexedDB 持久化 + `<skill>` prompt block 注入 + `create_skill` 原子创建
- **Virtual FS**：`mem://` 浏览器侧 VFS + LIFO 沙箱 + Runtime Strategy（browser-first / host-first）

辅助子系统：Hook 系统（17 个 hook 点）、事件总线（50+ 事件类型）、Compaction（overflow/threshold）、Snapshot Enricher。

## 扩展侧工具契约

45 个内置工具，按类别：

**文件/Shell（8）：** `host_bash`, `browser_bash`, `host_read_file`, `browser_read_file`, `host_write_file`, `browser_write_file`, `host_edit_file`, `browser_edit_file`

**元素交互（8）：** `search_elements`, `click`, `fill_element_by_uid`, `select_option_by_uid`, `hover_element_by_uid`, `get_editor_value`, `fill_form`, `computer`

**导航/滚动（4）：** `press_key`, `scroll_page`, `navigate_tab`, `scroll_to_element`

**Tab 管理（6）：** `get_all_tabs`, `get_current_tab`, `create_new_tab`, `get_tab_info`, `close_tab`, `ungroup_tabs`

**验证/视觉/下载（8）：** `get_page_metadata`, `highlight_element`, `highlight_text_inline`, `capture_screenshot`, `capture_tab_screenshot`, `capture_screenshot_with_highlight`, `download_image`, `download_chat_images`

**Intervention（4）：** `list_interventions`, `get_intervention_info`, `request_intervention`, `cancel_intervention`

**Skill（7）：** `create_skill`, `load_skill`, `execute_skill_script`, `read_skill_reference`, `get_skill_asset`, `list_skills`, `get_skill_info`

**元素定位优先级：** `uid` > `ref` > `backendNodeId` > `selector`（fallback）

## UI 与无障碍 (Accessibility First)

所有 UI 开发必须遵循以下无障碍标准，确保产品对所有用户（包括辅助技术用户）友好：

- **语义化 HTML**：优先使用 `<header>`, `<main>`, `<nav>`, `<article>`, `<button>`, `<ul>` 等语义标签，避免滥用 `div`。
- **ARIA 属性**：
  - 所有图标按钮必须具备明确的 `aria-label`。
  - 复杂组件必须包含状态描述（`aria-expanded`, `aria-haspopup`, `aria-controls`）。
  - 实时变化区域（如消息列表）必须标记 `role="log"` 和 `aria-live="polite"`。
  - 列表项使用 `role="listitem"`，当前项使用 `aria-current="true"`。
- **键盘导航**：
  - 所有交互元素必须可通过 `Tab` 键聚焦。
  - 核心列表（如会话列表）必须支持 `ArrowUp/ArrowDown` 方向键导航及 `Enter` 确认。
  - 必须确保焦点可见性（使用 `focus-visible` 样式）。
- **图标降噪**：纯装饰性图标必须标记 `aria-hidden="true"`。

## 关键协议

Bridge WS 通信使用统一 `invoke` 帧格式：
- 请求：`{ type: "invoke", id, tool, args, sessionId?, parentSessionId?, agentId? }`
- 成功：`{ id, ok: true, data, sessionId? }`
- 失败：`{ id, ok: false, error: { code, message, details? } }`
- 事件：`{ type: "event", event: "invoke.started|stdout|stderr|finished", ... }`

错误码前缀：`E_PATH`（路径拒绝）、`E_TOOL`（未知工具）、`E_ARGS`（参数错误）、`E_CMD`（命令未白名单）、`E_BUSY`（并发上限）。

## Bridge 模式

- **god**（默认）：文件系统无限制，`bash.exec` 默认启用
- **strict**：需 `BRIDGE_ROOTS` 限制路径范围，命令受 `allowInStrict` 过滤

关键环境变量：`BRIDGE_TOKEN`、`BRIDGE_MODE`、`BRIDGE_ROOTS`、`BRIDGE_PORT`(8787)、`BRIDGE_ENABLE_BASH_EXEC`、`BRIDGE_MAX_CONCURRENCY`(6)。

## 对话调试

- 当需要调试某个会话/对话为什么失败、卡住、无进展、工具调用异常时，**优先使用诊断导出 API**，不要让用户粘贴整段大诊断 JSON 到对话上下文。
- 正确做法：先让系统生成诊断链接，再由 Agent 用命令行下载到本地文件，然后用 `rg`、`jq`、`sed` 等工具离线检索。
- 模块级窄接口见 [docs/debug-interfaces.md](docs/debug-interfaces.md)。外部 AI / Codex 先按模块抓 `brain.debug.snapshot`，证据不足时再下载完整 diagnostics。
- 诊断 JSON 结构约定见 [docs/diagnostics-format.md](docs/diagnostics-format.md)。外部 AI / Codex 进入仓库后，调试诊断时应先读这份文档，再下载 JSON。
- 全局模块调试快照结构约定见 [docs/debug-snapshot-format.md](docs/debug-snapshot-format.md)。当问题更像 plugin/skill/provider/runtime cache 异常，而不是单会话故障时，优先使用这类快照。
- 诊断 API 走本地 Bridge HTTP：
  - `GET /api/diagnostics?token=<BRIDGE_TOKEN>`：列出已有导出
  - `GET /api/diagnostics/<id>?token=<BRIDGE_TOKEN>`：下载单个诊断 JSON
  - `GET /api/debug-snapshots?token=<BRIDGE_TOKEN>`：列出已有调试快照
  - `GET /api/debug-snapshots/<id>?token=<BRIDGE_TOKEN>`：下载单个调试快照 JSON
- **调试面板导出**：DebugView 面板的"导出调试日志"按钮会同时发布诊断 + 调试快照到 Bridge，并将下载链接复制到剪贴板。用户提供此链接后可直接用 `curl` 下载。
- 典型调试流程：

```bash
# 1. 列出所有导出（诊断 + 快照）
curl 'http://127.0.0.1:8787/api/diagnostics?token=<BRIDGE_TOKEN>'
curl 'http://127.0.0.1:8787/api/debug-snapshots?token=<BRIDGE_TOKEN>'

# 2. 下载单个诊断
curl 'http://127.0.0.1:8787/api/diagnostics/<id>?token=<BRIDGE_TOKEN>' -o diag.json

# 3. 下载单个调试快照
curl 'http://127.0.0.1:8787/api/debug-snapshots/<id>?token=<BRIDGE_TOKEN>' -o snapshot.json

# 4. 本地搜索关键线索
rg 'loop_error|llm.skipped|step_finished|failed_execute|failed_verify|no_progress' diag.json

# 5. 快照中检索插件/运行时异常
jq '.payload.data.plugins.summary' snapshot.json
jq '.payload.data.runtime.summary' snapshot.json
```

- 如果用户直接给了"导出调试日志"的链接（可能包含两个 URL，一行诊断一行快照），逐个下载后分别分析。
- 调试入口优先级：
  - 先用 `brain.debug.snapshot` 取模块级小快照：`runtime` / `sandbox` / `plugins` / `skills`
  - 再用 diagnostics 导出拿整包会话证据
- 分析诊断时关注：
  - `summary.lastError`
  - `timeline`
  - `sandbox.summary`
  - `sandbox.trace`
  - `llm.trace`
  - `tools.trace`
  - `agent.loopRuns`
  - `rawEventTail`
- 推荐检索顺序：
  - `summary.lastError -> timeline -> sandbox.summary -> sandbox.trace -> llm.trace -> tools.trace -> agent.loopRuns -> rawEventTail`
- **diagnostics vs snapshot 选择策略**：
  - **会话级问题**（LLM 调用失败、tool 执行异常、loop 卡住/无进展）→ 优先用 diagnostics
  - **系统级问题**（plugin 加载失败、skill 注册异常、provider 配置错误、UI widget 不显示）→ 优先用 debug-snapshot
  - **交叉检索规则**：diagnostics 中出现 plugin 相关错误时（如 `rawEventTail` 含 `plugin.hook_error`），交叉查看 snapshot 的 `plugins[].lastError` + `uiState`
  - **uiState 字段**：snapshot 的 `plugins.uiState` 包含 `relayActive`（SidePanel 连接状态）和 per-plugin widget mount 状态，诊断 UI 不渲染问题时必查
  - 诊断 JSON 的 `diagnosticGuide.columnIndex` 提供 columnar 表的列名→索引映射，用 jq 查询时可直接引用
  - 诊断 JSON 的 `diagnosticGuide.hints` 包含根据 `lastError` 自动生成的诊断建议
  - llm.trace 的 `source` 列区分 `"compaction"` / `"hosted_chat_transport"` / `"llm_provider"`，`contentType` 列标记响应 transport 格式
- 分析调试快照时关注：
  - `payload.data.runtime.summary`
  - `payload.data.plugins.summary`
  - `payload.data.skills.summary`
  - `payload.data.skills.resolver`
  - `payload.data.plugins.capabilityProviders`
  - `payload.data.plugins.capabilityPolicies`
- 诊断原则：**先下载到文件、再搜索定位、最后只把结论和必要片段带回对话**；不要把整个诊断文件内容直接贴回模型上下文。
- 当需要看“当前 runtime 运行态”而不是历史诊断导出时，使用 `brain.debug.runtime`。结构约定见 [docs/runtime-debug-interface.md](docs/runtime-debug-interface.md)。
- `brain.debug.runtime` 适合外部 AI 查看：
  - 当前 session / queue / kernel 概况
  - plugin persisted registry / ui extensions / hook trace / runtime messages
  - skill installed 清单
  - 最近 `brain.*` 路由调用尾巴
  - sandbox runtime 摘要

## BDD 规则

- BDD 索引文档：`bdd/README.md`
- 契约 ID 格式：`BHV-*`，必须唯一
- 每个契约必须被至少一个 `.feature` 的 `@contract(...)` 引用
- 每个契约必须在 `contract-to-tests.json` 有映射且满足 `proof_requirements`
- gate 严格失败：任何缺失/映射不完整/目标路径不存在/`passed!=true` 都失败
- `BDD_GATE_PROFILE=default` 只检查默认契约；`BDD_GATE_PROFILE=live` 额外检查 `context.gate_profile=live` 契约
- 会话中断续跑参考 `bdd/SESSION-HANDOFF.md`

## Loop 编排约束（实现口径）

- LLM 消费 snapshot 时优先 `compact + 元信息`，不要把整段大 JSON 直接塞回对话。
- LLM 默认配置：`base=https://ai.chen.rs/v1`、`model=gpt-5.3-codex`（key 由运行时注入）。
- strict verify 模式下，`browser_action` 默认需要动作后验证；"执行成功"不等于"目标推进成功"。
- 终态 / 决策语义必须分层理解：
  - `loop_done.status` 是终态域：`done | failed_execute | failed_verify | progress_uncertain | max_steps | stopped | timeout`
  - `FailureReason` 是失败子域：`failed_execute | failed_verify | progress_uncertain`
  - `brain.agent.end` / `handleAgentEnd()` 是决策域：`continue | retry | done`
  - `action=done` 时 `reason` 应复用 canonical terminal status / failure reason，不再用模糊 `completed|error`
- ownership：
  - `threshold` compaction 由 `runtime-loop` 的 pre-send compaction check 触发
  - `overflow` compaction 由 `brain.agent.end` 输入上报，再由 `orchestrator.handleAgentEnd()` 触发
- 必须启用 `no_progress` 检测（重复签名 / ping-pong 往返）并提前终止当前轮。
- auto-repair 仅在 `failed_execute/failed_verify/progress_uncertain` 或 `loop_no_progress` 信号触发；`max_steps/stopped/timeout` 不自动续跑下一轮。
- `stopped` 回复优先状态文案，不回显 memory 中的大段 snapshot 内容。
- BDD 必须覆盖 LLM 能力门禁：`tool_call` 闭环成功、无 LLM 的规则降级成功、不可降级时 `failed_execute`、LLM HTTP 失败回退规则 planner。
- BDD 采用双层：默认 profile 用 mock 保证编排稳定；live profile 用真实 LLM 验证浏览器任务成功率（`brain:e2e:live` + `bdd:gate:live`）。
- **Runtime Strategy**：`browser-first`（默认走浏览器沙箱）/ `host-first`（默认走 host bridge），通过 `BrowserRuntimeStrategy` 配置。

## Issue 跟踪

对话中发现的待办事项、优化建议、已知 bug 记录在 `docs/backlog/` 目录，详见 [docs/backlog/README.md](docs/backlog/README.md)。

Agent 行为规范：
- **发现 issue**：对话中遇到值得跟踪的问题（bug、优化点、技术债），创建 `docs/backlog/YYYY-MM-DD-<slug>.md` 记录，用 frontmatter 标记 status/priority/tags
- **承接 issue**：用户指派或空闲时，扫描 `docs/backlog/` 中 `status: open` 的 issue 作为可接任务
- **更新状态**：开始处理改为 `in-progress`，完成改为 `done`
- **完成回写**：任务完成后，必须回到原 issue 文档末尾追加本次工作记录，至少包含：
  - `## 工作总结`：本次做了什么、结果是什么、还有哪些残留问题
  - `## 相关 commits`：列出本次相关 commit hash / message；如果当前改动尚未提交，明确写 `未提交`
  - 追加记录必须保留时间信息，按时间顺序附加在原文档末尾，不能覆盖历史记录
- **跨会话交接**：新 agent 进入仓库后，可读取 backlog 了解未完成工作，避免重复发现同一问题

## 技术栈

- 运行时：Bun（bridge）、Chrome MV3 + Service Worker（extension）
- 语言：TypeScript（全项目统一）
- 构建：Vite 8（4 入口：sidepanel / debug / plugin-studio / service-worker）
- UI：Vue 3.5 + Pinia 3 + Tailwind CSS 4
- 持久化：IndexedDB（via `idb` 8）
- 沙箱：`@lifo-sh/core` 0.5 + `@lifo-sh/ui` 0.5
- 测试：Vitest 4（extension browser tests）、bun test（bridge）、纯 CDP e2e
