---
name: cua-driver
description: 通过 cua-driver 的 MCP 工具（cua_ 前缀）操作本机 Windows 真实桌面：枚举应用与窗口、读取窗口的无障碍树与截图、按元素索引或坐标点击/输入/滚动/拖拽，并验证动作是否真的生效。当用户要求操作、驱动、自动化某个真实桌面应用，或需要查看/验证某个窗口的实际界面（而不只是文件内容）时使用。
license: Apache-2.0
compatibility: Windows 交互会话（Session 1+）；需已安装 cua-driver 并在 ~/.synapse/mcp.json 启用 cua 服务器（stdio，tool_prefix=cua_）。不需要管理员权限或额外系统授权。
allowed_tools: cua_list_apps, cua_list_windows, cua_get_window_state, cua_get_desktop_state, cua_get_screen_size, cua_launch_app, cua_click, cua_type_text, cua_press_key, cua_hotkey, cua_set_value, cua_scroll, cua_drag, cua_zoom, cua_start_session, cua_end_session, cua_kill_app
---

# Cua Driver（Windows 桌面自动化）

驱动本机真实桌面：看得到窗口、点得准控件、且**不抢焦点、不动真实鼠标**。

## 触发场景

- 用户要求操作/自动化某个真实桌面应用（记事本、计算器、资源管理器、企业内网软件…）。
- 需要「看到」某个窗口的实际界面，而不只是读文件。
- 需要验证某个桌面动作是否真的生效。

## 工具面

| 类别 | 工具 | 说明 |
| --- | --- | --- |
| 枚举 | `cua_list_apps` | 运行中 + 已安装应用；`active` 字段标示是否前台 |
| 枚举 | `cua_list_windows` | 顶层窗口（含 `window_id`/`pid`/`bounds`/`z_index`）。窗口级判断一律用它，不要用 `list_apps` |
| 观察 | `cua_get_window_state` | **核心工具**：返回无障碍树 + 截图 + 结构化字段。动作前必调 |
| 观察 | `cua_get_desktop_state` | 整屏截图（真实像素，不缩放），用于 desktop scope 动作 |
| 观察 | `cua_get_screen_size` | 主屏物理像素尺寸与缩放比 |
| 观察 | `cua_zoom` | 放大窗口截图的局部，用于读小字/认图标 |
| 动作 | `cua_click` / `cua_drag` / `cua_scroll` | 指针类 |
| 动作 | `cua_type_text` / `cua_press_key` / `cua_hotkey` | 键盘类 |
| 动作 | `cua_set_value` | 直接写控件值（UIA ValuePattern）。**填表首选**：原子写入、不需要焦点、不受最小化影响，且浏览器上仍能后台执行 |
| 动作 | `cua_launch_app` / `cua_kill_app` | 应用生命周期 |
| 会话 | `cua_start_session` / `cua_end_session` | 多步操作建议开一个会话，便于收尾清理。注意 `end_session` 会**连隐式会话一起结束**，之后必须显式 `start_session` 才能继续 |

## 核心不变式：先快照，再动作

**元素索引是「快照绑定」的。** 每次 `cua_get_window_state` 会生成新的 `snapshot_id`，
旧快照立即失效（复用会报 `element_token is stale`）。

因此顺序**不可颠倒**：

```
1. 定位   cua_list_windows                      → 拿到 pid + window_id
2. 快照   cua_get_window_state(pid, window_id)  → 拿到树 + snapshot_id
3. 动作   cua_click(element_index, snapshot_id, window_id)
4. 验证   再取一次 cua_get_window_state          → 确认状态真的变了
```

跳过第 2 步直接点元素索引，会得到：

```
click: bare element_index is not accepted; pass element_token, or snapshot_id together with element_index
```

## `cua_get_window_state` 的三段结果

| 段 | 内容 | 用途 |
| --- | --- | --- |
| 树（markdown） | `[N] Role "label" [value=... actions=[...]]` | `N` 就是 `element_index`；`actions` 决定该用哪个工具 |
| 截图 | 图像块（小窗口）或占位符（大窗口被剪枝） | 视觉确认与像素定位 |
| `structuredContent:` | `snapshot_id` / `window_bounds` / `elements_complete` / 折叠后的 `elements` | 动作必需的控制字段 |

**两者要交叉验证**：树在某些控件上会说谎（自绘控件、canvas），截图才是真相。

`elements` 常被折叠成 `<omitted 40063 chars, 168 items>` —— 这是正常的，树的 markdown 里
已经有 `element_index` 与 `actions`。只有需要 `element_token` 时才需要展开。

## 验证动作是否生效（最容易漏的一步）

`cua_click` 的返回是：

```
✅ Performed UIA Invoke on [31] (screen (546,662)).
{"delivery": {"mode": "background"}, "effect": "unverifiable", "route": "accessibility"}
```

**`effect: "unverifiable"` 不代表失败，也不代表成功** —— UIA Invoke 没有回执。
唯一可靠的验证是**再取一次 `cua_get_window_state` 读应用状态**（例如读计算器的
`CalculatorResults` 文本确认显示为 42）。

## 大窗口截图：改走落盘

| 窗口规模 | 截图 | 说明 |
| --- | --- | --- |
| 小（如计算器 474×667） | 直接作为图像送达 | 直接看即可 |
| 大（如资源管理器 1372×754，base64 ≈ 308KB） | 被剪枝成 `[previous screenshot removed to save context]` | 受 `image_window_middleware` 的单图窗口 + payload 预算约束 |

大窗口需要看图时，传 `screenshot_out_file` 让它落盘，再用 `read_file` 按需读：

```
cua_get_window_state(pid, window_id, screenshot_out_file="<workspace>/.cua/shots/win.png")
→ 返回文本里带路径；再用 read_file(file_path="/.cua/shots/win.png") 看图
```

注意返回的路径带 `\\?\` 扩展长度前缀，映射到 Synapse 虚拟路径时要转成 workspace 相对路径。

## 后台投递与降级阶梯

默认 `delivery_mode: "background"`：**不抬升窗口、不移动真实鼠标、不切换前台**。

正确顺序（不要跳级）：

1. `element_index` 寻址（走 UIA，最稳，可作用于后台/最小化窗口）
2. 退化到 `x, y`（窗口局部截图像素；驱动会先做 UIA hit-test，命中可调用元素仍走无障碍）
3. 仍然失败 → **只对那一个动作**重试 `delivery_mode: "foreground"`

`background_unavailable` 是**结构化拒绝**，不是静默失败。它会明确告诉你这个动作必须前台，
此时才升级 —— **不要因为目标"看起来像" Chromium/GTK 就预先传 `foreground`**。

## 读内容 vs 定位控件：两条通道

| 目的 | 首选 | 理由 |
| --- | --- | --- |
| 读**内容**（评分、简介、正文、界面外观） | **截图** | 一次读全；树可能有上千个元素且会被边界截断 |
| 读**控件**（哪个按钮、`element_index`、`actions`） | **树** | 精确、可寻址，拿到索引才能发起动作 |

两者由 `cua_get_window_state` 同时返回，按用途挑，不要只用一个。实测读一个内容密集的网页时，
截图一步给出答案，而遍历 1264 个元素的树既慢又会被截断。

## 先探测 a11y 树，再决定走哪条路径

不要假设某个应用"应该"有树。动手前先花一次调用探测它 —— **用一个不匹配的 `query`，输出几乎为零，
但 `element_count` / `total_element_count` 照常完整**：

```
cua_get_window_state(pid, window_id, query="zzzznomatch", max_elements=200)
→ elements: []            ← 投影为空，不占上下文
  element_count: 115      ← 但树规模照常报告
```

实测各类目标的元素数：

| 目标 | 元素数 | 可精确操作 |
| --- | --- | --- |
| 资源管理器（Win32 经典控件） | 168 | ✅ |
| Chrome / Edge（Chromium） | 61–1264 | ✅ |
| Ndd 记事本（Qt） | 115 | ✅ |
| Windows 设置（`ApplicationFrameHost` 承载） | 52 | ✅ |
| 计算器（UWP / XAML） | 39 | ✅ |
| 记事本（WinUI3） | 32 | ✅ |
| wezterm 终端 | 5 | ⚠️ 几乎无（终端本就是字符网格） |
| 命令面板（CmdPal） | 4 | ⚠️ 极少 |
| WebView2 宿主（拆分进程形态） | 2 | ❌ |
| 微信（自绘 `MMUIRenderSubWindowHW`） | 0 | ❌ 仅像素 |
| Microsoft To Do | 0 | ❌ 仅像素 |
| Windows 设置（`SystemSettings.exe` 承载的实例） | 0 | ❌ 仅像素 |

**判据不是"什么软件"，而是"它用什么 UI 框架 + 这个实例是否暴露 UIA"：**

| 通常有树 | 通常没有 |
| --- | --- |
| Win32 经典控件、Qt | 自绘 UI（微信、To Do） |
| UWP / WinUI3 / XAML | 部分 Electron / WebView2 拆分进程 |
| Chromium（Chrome / Edge） | 终端类（wezterm） |

**⚠️ 同一个应用的不同实例可能有完全不同的暴露程度。** 实测"设置"：由
`ApplicationFrameHost.exe` 承载的窗口有 52 个元素，而由 `SystemSettings.exe` 直接承载的窗口是 0。
所以**不要凭一次探测就给某个应用下结论** —— 每换一个窗口就重新探测。

`element_count: 0` 时驱动会给出结构化诊断，直接照它走：

```
{"degraded": true, "degraded_reason": "ax_tree_empty: ...",
 "escalation": {"reason": "non-AX surface — act by pixel (x,y) off the screenshot",
                "recommended": "px"}}
```

### 无 a11y 时的像素路径

```
cua_get_window_state(..., screenshot_out_file=...)   → 截图落盘
cua_zoom(窗口局部矩形)                                → 放大读准坐标
cua_click(pid, window_id, x, y)                      → 像素点击（不要带 snapshot_id！）
cua_type_text(pid, window_id, text)                  → 输入（自绘输入框可后台）
再取一次截图验证
```

坐标空间是**窗口局部截图像素**，与 `screenshot_width/height` 1:1。`cua_zoom` 返回的图是放大后的，
要按缩放比换算回窗口坐标；换算方式：`窗口坐标 = 区域起点 + 放大图坐标 × (区域尺寸 / 放大图尺寸)`。

## 浏览器（Chromium：Chrome / Edge）

Chromium 是最需要"选对动作面"的目标：窗口类 `Chrome_WidgetWin_1` **会丢弃后台的键盘与文本
合成事件**，但接受 UIA 值写入。

### 三件套：按 event kind 分工

| 操作 | 工具 | event_kind | 后台可用 |
| --- | --- | --- | --- |
| 填值（输入框 / 搜索框） | `cua_set_value` | UIA ValuePattern | ✅ **是** |
| 逐字输入 | `cua_type_text` | `text_input` | ❌ 必须前台 |
| 按键（回车 / 快捷键） | `cua_press_key` / `cua_hotkey` | `keystroke` | ❌ 必须前台 |

浏览器上的实用组合：

```
cua_set_value 填值（后台）  →  cua_press_key 提交（前台）
```

实测拒绝长这样，照它升级即可：

```
{"code": "background_unavailable", "event_kind": "text_input",
 "target_class": "Chrome_WidgetWin_1",
 "escalation": {"recommended": "foreground"}}
```

### 能用 URL 直达的，就别驱动 UI

打开某个页面时优先：

```
cua_launch_app(urls=["https://example.com/search?q=<关键词>"])
```

它走 ShellExecuteEx：不激活窗口、不动鼠标、不需要前台。而"点地址栏 → 输入 → 回车"需要前台
键盘输入，还要应付地址栏的自动补全下拉。**能在 URL 里表达的导航/搜索参数，一律塞进 URL。**

### 页面树会剧烈波动，必须限幅

同一页面在几次读取之间可以是 78 → 24 → **1264** 个元素（内容加载、下拉展开、结果面板出现
都会改变树）。因此：

- 除非确实要全量，永远带 `max_elements` / `max_depth`
- 用 `total_element_count` 看真实规模（可能远大于 `returned_element_count`）
- 大页面用 `query` 投影

`query` 的行为要注意：**只返回匹配节点 + 祖先链，不含同级兄弟节点**。所以它适合"定位控件"，
不适合读"标签: 值"这类配对信息 —— 值的兄弟节点会被排除在外。读配对信息要放宽边界读整段，
或直接看截图。

### Chromium 特有的返回字段

- `capture_coverage: {"browser_chrome": {"status": "not_observable_in_window_scope"}}`
  —— 浏览器自有的权限气泡可能绘制在窗口之外，窗口截图看不到。
- 网页内元素带 `in_web_content: true`，`structuredContent.elements` 里含 `element_token`。

## Windows 平台要点

- **Store 应用用 AUMID 启动**。Win11 的 Calculator/Notepad/Paint 是打包应用，
  `System32` 下的 `.exe` 只是约 7KB 的 stub。用 `cua_launch_app(aumid="Microsoft.WindowsCalculator_8wekyb3d8bbwe!App")`。
- **能用协议 URI 直达的，就别在 UI 里导航。** Windows 设置支持 `ms-settings:` 协议：
  `cua_launch_app(urls=["ms-settings:windowsupdate"])` 直接落到「Windows 更新」页，
  免去在一个可能没有 a11y 树的界面里逐级点击（`ms-settings:display`、`ms-settings:appsfeatures` 等同理）。
  这与浏览器那条「URL 直达优先」是同一个原则 —— **能在地址/协议里表达的意图，一律别驱动 UI**。
- **`ApplicationFrameHost.exe` 会同时承载多个 UWP 窗口**（例如「设置」和「计算器」共用同一个 pid）。
  **不要对它 `kill_app`** —— 会连带关掉同进程的其他窗口。要关某个窗口，点它的关闭按钮
  （`element_index` 指向 `Button "关闭 …" [id=Close]`）。
- **`type_text` 对 XAML/WinUI3/UWP 宿主需要 `element_index`**（驱动会改走 UIA
  `ValuePattern.SetValue`，因为这类宿主的 CoreInput 只消费系统输入队列，`WM_CHAR` 会被丢弃）。
  直接 `cua_type_text(pid, text)` 会返回可操作的错误提示，引导你先取快照。
- **填表优先 `cua_set_value`** 而不是逐字输入：它是原子写入，不需要焦点，也不受最小化窗口影响。
- **坐标空间有两套，不要混用**：

  | 来源 | 空间 | 单位 |
  | --- | --- | --- |
  | `elements[].frame` | **屏幕绝对**（左上原点） | 物理像素 |
  | `click` 的 `x, y`（带 `pid`+`window_id`） | **窗口局部**（`get_window_state` PNG 左上原点） | 截图像素 |

  把 `frame` 的中心直接喂给 `click` 的 `x, y` 会点偏，且**不会报错**（坐标结构合法，只是指向别处）。

## 安全边界

> ⚠️ **这 17 个工具不受 Synapse 的 HITL 审批管辖。**
> `build_interrupt_on` 只覆盖 `execute` / `write_file` / `edit_file` / `patch`，
> 因此 `--require-approval` **管不到** `cua_click` / `cua_type_text` / `cua_hotkey` / `cua_kill_app`。
> `--readonly` 同样不是安全网（它只排除 write/execute 工具）。

由此得出的操作纪律：

- **只在用户明确要求操作桌面时才调用动作类工具**；纯观察需求用 `list_windows` / `get_window_state`。
- 先在**无害目标**（计算器、记事本）上验证，**不要一上来操作已登录的浏览器/账号/业务系统**。
- 关闭未保存的文档、删除、发送消息等破坏性动作前，先向用户确认。
- 操作期间用户可能正在同一台机器上工作 —— 优先用后台投递，避免抬升窗口。

## 常见失败模式

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `bare element_index is not accepted` | 没带 `snapshot_id` | 先 `get_window_state` 取本轮快照 |
| `element_token is stale` | 快照被下一次 `get_window_state` 替换了 | 重新取快照，不要缓存索引跨轮使用 |
| `background_unavailable` | 该动作必须前台（Chromium 坐标点击、GTK 按钮、VCL 加速键、WPF 拖拽…） | 只对该动作重试 `delivery_mode: "foreground"` |
| 点击返回成功但界面没变 | `effect` 本就不可验证；或坐标空间用错 | 取新快照读应用状态确认；检查是否混用了 `frame` 与截图像素 |
| `list_windows` 返回空 | 进程落在 Session 0（SSH/服务） | 需要交互会话中的 daemon；本地 TUI 场景不会遇到 |
| 窗口截图是占位符 | 大窗口被剪枝 | 传 `screenshot_out_file` 落盘 + `read_file` |
| 最小化窗口点不动 | 键盘类动作需要渲染器焦点 | 改用 `cua_set_value` 直接写值，或先恢复窗口 |
| 浏览器输入/按键被拒（`event_kind: text_input` / `keystroke`） | Chromium 丢弃后台合成输入 | 见「浏览器（Chromium）」：填值改 `set_value`，只有提交才升前台 |
| `query` 找不到想读的值 | 只返回匹配节点 + 祖先，不含兄弟节点 | 放宽 `max_elements`/`max_depth` 读整段，或看截图 |
| 报 `this session has ended` | `end_session` 连隐式会话一起结束了 | 显式 `cua_start_session` 开新会话 |
| `click: snapshot_id requires element_index` | 像素点击带了 `snapshot_id` | 像素点击（`x,y`）**不要**带 `snapshot_id` —— 它只与 `element_index` 配对 |
| `element_count: 0` / `degraded: ax_tree_empty` | 目标是无障碍树贫瘠的自绘 UI | 切像素路径：截图定位 → `cua_click(x,y)` → `type_text` |
| 同一应用换个窗口就没树了 | 承载进程不同（如「设置」的两种宿主） | 每个窗口独立探测，不要复用结论 |
| `type_text` 返回 "not verified" | 目标没有 ValuePattern 可回读（自绘输入框） | **这不等于失败**。用截图确认；实测微信自绘输入框接受 `PostMessage(WM_CHAR)` 并成功落字 |

## 不在本 skill 范围

`browser_*`（浏览器专用工具）、`start_recording` / `replay_trajectory`（轨迹录制）、
`history_status` / `history_query`（Computer History 预览）、`bring_to_front`
（显式破坏 no-foreground 契约）**均未加入白名单**。需要时应先在 `~/.synapse/mcp.json`
的 `include_tools` 中显式放开，并重新评估安全边界。
