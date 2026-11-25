---
name: dsh-browser-agent
description: >
  浏览器自动化 + 视觉识别（给纯文本模型）。当用户需要打开/控制真实浏览器里的网页
  （导航、点击、输入、滚动、提取文本、截图）、端到端测试 web 项目、或做 UI 视觉验证，
  而当前模型看不到图片时使用。技能通过本地 HTTP 桥驱动 Playwright 浏览器，并用视觉模型
  （默认 GLM-4V）把截图转成文字，文本模型始终是决策者。
---

# dsh-browser-agent

给纯文本模型的浏览器自动化 + 视觉识别。一个长驻浏览器走本地 HTTP 桥；截图由视觉模型转成
文字，文本模型（你）负责推理与决策。

## 结构

- `cli.mjs` —— 统一 CLI（`node cli.mjs <命令>`）。
- `src/bridge.mjs` —— 常驻桥（Playwright 浏览器 + HTTP API）。
- `src/vlm.mjs` —— 视觉调用器（GLM / custom / local）。
- `plugins/cordis/` —— Cordis 插件（把 CLI 包装成 `browser_*` 原生工具）。
- `plugins/sidebar/` —— 右侧浏览器侧边栏插件（host.js + client.js，镜像受控浏览器画面）。
- `scripts/start.ps1`、`scripts/start.sh` —— 幂等启动脚本。

## 1. 启动桥（每会话一次）

先看桥是否已在运行（比如别的窗口已启动）：

```powershell
node cli.mjs ping
```

- `{"ok":true,...}` → 复用，跳到第 2 步。
- `bridge not running` → 启动一个。

**作为后台 job 启动。** 先正常权限试；若报 `browserType.launch: spawn EPERM`（沙箱拦了
Playwright 的命名管道），用提权（`sandbox_permissions = danger-full-access`）重试同一条命令
——用户需批准一次。

```powershell
# Windows
pwsh -NoProfile -File "scripts\start.ps1"
# macOS / Linux
bash scripts/start.sh
```

`scripts/start.ps1` 是幂等的：有桥就复用，没有才拉起，只清 Chromium 残留锁（登录态保留）。

## 2. 控制浏览器

在项目目录下运行，或用 `cli.mjs` 的绝对路径。

```powershell
node cli.mjs open "http://你的地址"     # 打开
node cli.mjs snapshot                    # 元素清单（带 ref）
node cli.mjs screenshot shot.png         # 截图
node cli.mjs click 3                     # 点击 ref 3
node cli.mjs type 3 "要输入的文本"        # 输入
node cli.mjs press Enter                 # 按键
node cli.mjs scroll bottom               # down/up/bottom/top
node cli.mjs eval "document.title"       # 执行 JS 拿结果
node cli.mjs text                        # 页面文本
```

**定位策略**：优先 `snapshot`（文本 + ref）定位元素，多数步骤不需要视觉；只有需要"看"
（布局、图片、验证码、canvas、视觉还原）时才用视觉。

## 3. 视觉（截图 → 文字）

```powershell
node cli.mjs see "描述这个页面和可点击元素"
node cli.mjs see --thinking "详细分析这张图表"
node cli.mjs vision 本地图片.png "图里有什么文字？"
```

- `glm`（默认）`glm-4.6v-flash`；`--thinking` 用 `glm-4.1v-thinking-flash`。
- 429 自动降级到 thinking 模型。
- 视觉需要 `GLM_API_KEY`。若 key 只在 Windows 用户注册表（harness 启动早于 key 设置），先注入：

```powershell
$env:GLM_API_KEY = [Environment]::GetEnvironmentVariable('GLM_API_KEY','User')
```

（或设 `VLM_PROVIDER=custom` + `VLM_BASE_URL`/`VLM_MODEL`/`VLM_API_KEY`，或 `VLM_PROVIDER=local` 用 Ollama。）

## 4. 循环

```
open 页面 → snapshot →（需要看才 see）→ click/type → snapshot → ... 直到完成
```

每步把观察结果汇报给用户；操作前后用 `see` 描述视觉状态。

## 环境注意点（DeepSeek Harness 沙箱）

1. 启动浏览器可能报 `spawn EPERM` —— 用提权启动桥，或 attach 模式：自己
   `--remote-debugging-port=9222` 起浏览器并设 `BA_CDP_URL=http://127.0.0.1:9222`。
2. PowerShell HTTPS 可能报 `SEC_E_NO_CREDENTIALS`；CLI 走 Node 的 TLS，用 `node cli.mjs ...`，
   别用 `Invoke-RestMethod`。
3. 自己新增的 `.ps1` 保持 ASCII-only（脚本源码里的中文可能让 pwsh 解析失败）；中文只能作参数传。

## Cordis 插件（可选）

见 `plugins/cordis/README.md`。按它把 `host.js` 用 `cordis_define` 注册，就能在会话里直接用
`browser_*` 工具（`browser_open`/`browser_snapshot`/`browser_see` 等 10 个），无需手敲 CLI。

## 侧边栏预览（可选）

见 `plugins/sidebar/README.md`。把 `host.js` + `client.js` 用 `cordis_define` 注册，就能在 DSH
界面右侧呼出一个浏览器侧栏：截图镜像受控浏览器的真实画面（含 agent 的操作），支持点击/滚动
回传交互，以及 URL 输入框手动导航。

## 停止

```powershell
node cli.mjs stop
```
