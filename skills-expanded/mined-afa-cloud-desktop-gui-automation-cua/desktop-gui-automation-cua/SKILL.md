---
name: "desktop-gui-automation-cua"
description: "可泛用的 macOS 桌面 GUI 自动化（computer use）：cua-driver 做 AX→像素→桌面的三档降级，对任意 app 先 probe 判定模式再驱动；含识图定位、隐私处理、微信/iPhone 镜像案例。遇点击/输入/滚动/截图任意本机 app，或微信/IPhone 镜像/canvas 等 AX 空或稀疏的软件时用。"
when_to_use: "需要驱动 macOS 桌面应用（点击/输入/滚动/拖拽/截图）时；目标可能是任意原生 app、Electron、微信 4.x、iPhone Mirroring、Blender/canvas 等 AX 树为空或极稀疏的软件；用 cua-driver 而非 System Events/AppleScript。优先用本 skill 的泛用 computer_use.py，再用 send_wechat/iphonemirror 等 app 配方。"
---
# Desktop GUI Automation / Computer Use (cua-driver)

用本机 `cua-driver`（trycua）做 **macOS 桌面 GUI computer use**：对任意本机 app 执行"probe→定位→交互→验证"的泛用流程，AX→像素→桌面三档降级。涵盖任意 app，尤其微信 4.x / iPhone Mirroring / canvas 等 AX 空或稀疏的软件。

> 铁律：cua-driver 需 Accessibility + Screen Recording 双权限。操作前先 `cua-driver permissions status --json`。**绝不擅自升级到 unrestricted 权限档**；保持 standard 模式 + 会话授权。

> **版本与双形态**：本仓库同时作 skill（符号链接装进 agent 技能目录）与 DSH 插件（`plugin/` 的 `/cua`）提供。二者共享 `scripts/` 这一**单一事实源**（均不复制脚本），改一次仓库两端立即一致、不会漂移。版本以 `cua_lib.__version__` 为准，更新/自检用仓库 `update.sh`；每个脚本支持 `--version` 比对。

## 0. 通用工作流（对任意 app，照此执行）

接到"驱动 app X"的任务时，按序：

```
1. 定位:  python3 computer_use.py windows [X]         # 找 X 的窗口 (wid/pid)
2. 判定:  python3 computer_use.py probe X             # decide_mode → A/B/C 档 + AX 摘要
3. 快照:  python3 computer_use.py snapshot X --out t.png    # AX tree + 截图
          python3 computer_use.py inspect X "描述界面"      # 可选: 识图确认内容
4. 交互:  A档 → --token (element_token, 后台不抢焦点)
          B档 → --x/--y (window-local px, 前台)
          C档 → 强制前台 + get_desktop_state 全局像素
          (见 §1-3 各档详情; 附录 §9/§10 是微信/iPhone 案例)
5. 验证:  重新 snapshot / scroll 到底 / vision 识图确认结果
```

app 名传错(如 Finder→"访达")或找不到窗口时，先 `windows`/`list-apps` 看真实名称。

## 1. 核心原则

- **AX-token 优先**：后台/隐藏/最小化窗口也能操作，**不抢前台**。`element_token` 定位最稳。
- **找不到 AX → 自动降级像素**：cua-driver 在 AX 树截断时提示 `Use pixel clicks for elements not visible in this partial tree`。这是"无 AX 界面"场景唯一可靠路径。
- **iPhone 镜像等强制前台目标**：接受抢焦点，单独 Space + 批量缓解抖动。
- **先取证再动作**：每轮先快照确认目标再动手，避免盲点。

## 2. 泛用脚本入口 & 工具

`computer_use.py` 是泛用驱动入口（对任意 app）；`send_wechat.py` / `iphonemirror.py` 是 app 案例配方，`vision.py` 是识图，`cua_lib.py` 是共享底层。

```bash
export PATH="$HOME/.local/bin:$PATH"
D=<安装脚本的目录>/scripts      # DSH: ~/.dsh/skills/desktop-gui-automation-cua/scripts ; 其他 agent 见 README 安装位置
# 泛用驱动(推荐)
python3 $D/computer_use.py probe <app>            # 判定 A/B/C 档
python3 $D/computer_use.py snapshot <app> --out t.png
python3 $D/computer_use.py click <app> --token s0000...0   # A 档 AX
python3 $D/computer_use.py click <app> --x 120 --y 750     # B/C 档像素(window-local px)
python3 $D/computer_use.py type <app> "文本"                # 文本输入
python3 $D/computer_use.py vision t.png "描述"
# 底层 cua-driver 直接调用
cua-driver call get_window_state   # / list_windows / list_apps / zoom ...
# 单工具 schema
cua-driver describe click          # zoom / type_text / scroll / verify_state / set_value
```

## 3. 操作模式（AX → 像素三档降级）

### A 档 · AX-token 优先（后台不抢焦点）
目标在 AX 树里 → 用 `element_token`（或 `element_index + snapshot_id`）。
```bash
printf '{"pid":1234,"window_id":5678,"element_token":"...","button":"left"}' | cua-driver call click
printf '{"pid":1234,"window_id":5678,"element_token":"...","value":"文本"}' | cua-driver call set_value
```
- 会话列表/菜单栏/原生控件都能走这条。
- 每轮先重新快照（snapshot cache 按 pid+window_id 作用域，会被下一轮快照替换）。

### B 档 · 窗口截图像素（微信聊天区、canvas、自定义绘制）
AX 里找不到目标（eg 微信聊天正文/输入框/发送按钮）：
1. `get_window_state` 拿窗口 PNG 与尺寸（不含 element_token 也行，先把区域裁出来）。**实测该工具返回字段**：`screenshot_png_b64`（图）、`screenshot_width` / `screenshot_height`（截图像素）、`screenshot_scale`（Retina 倍率）、`window_bounds`（窗口几何）、`snapshot_id`。
2. `zoom` 裁局部：`{"pid","window_id","x1","y1","x2","y2"}`，**鼠标在裁剪图上定位**（zoom 会加 20% padding、限宽 500px）。
3. 动作时带 `from_zoom:true` 让坐标自动映射回全窗口空间：
```bash
printf '{"pid":1234,"window_id":5678,"x1":640,"y1":180,"x2":820,"y2":620}' | cua-driver call zoom
# 定位到裁剪图上的点 (X, Y) 后
printf '{"pid":1234,"window_id":5678,"x":X,"y":Y,"from_zoom":true}' | cua-driver call click
printf '{"pid":1234,"window_id":5678,"x":X,"y":Y,"text":"hi","from_zoom":true}' | cua-driver call type_text
```
- **像素坐标是窗口本地实际像素（top-left 原点）**；Retina 屏别把截图里看到的 2x 像素当 1x point——用 cua-driver 的 from_zoom 映射，不要自己换算。
- 像素点击需要窗口**可见**在屏上（CGEvent 需要锚点）。

### C 档 · 桌面级纯视觉（iPhone 镜像 / 全屏 Metal）
目标强制前台或塞满屏幕：
```bash
cua-driver call get_desktop_state '{}'     # screen-absolute 像素 + backing scale + 原生分辨率 PNG（无 AX）
# 之后用 screen 绝对坐标点击（scope 桌面）
```
- 识别到 iPhone Mirroring 等 → 先把它带到前台（必然抢焦点，接受），再 `get_desktop_state` + 全局点击。
- 缓解焦点抖动：把镜像放**单独 Space**、一次拿焦点批量执行多个动作、避免与终端输入交错。

### 判定表（快速选择）
| 目标 | AX 树 | 模式 |
|---|---|---|
| 原生 AppKit / Mail / Finder / 系统设置 | 完整 | A |
| Electron / Web 控件 | 深但可达 | A（行级 click 兜底）|
| **微信 4.x** | 会话列表/菜单可达，聊天区空 | A 导航 + **B 聊天区** |
| **iPhone Mirroring** | 几乎为空 + 强制前台 | **C** |
| Blender / canvas / WebGL | 空 | B 或 C |

## 4. 隐私 / 权限（macOS 严苛重点）

- 必须对**驱动自身身份**（`com.trycua.driver` 或宿主 agent 进程）授予 Accessibility + Screen Recording，双权限在重启宿主后生效。
- 命令级操作：
```bash
cua-driver permissions status --json   # 查：accessibility / screen_recording 布尔
cua-driver permissions grant           # 引导授权到 com.trycua.driver 身份
cua-driver doctor                      # 端到端自检
```
- **保持 standard 权限档**。cua-driver 有 permission-mode（standard/bounded/unrestricted）+ revoke + session-policy；被拒或受限时先查 `cua-driver call check_permissions`，不要设 `--dangerously-bypass-approvals`。
- 截屏 base64 默认只在内存；要落盘才加 `--screenshot-out-file <path>`。
- 对不可寻址对象 cua-driver 会**结构化拒绝**（`appNotFound` / `browser_route_unavailable`），不是静默假成功。
- 黑 / 白名单：如需阻止某些敏感 app，用 cua-driver 的 bundle denylist 配置而非放开权限。常见安全拒：直接传 bundle id 可能被 safety 策略拒（`... is not allowed ... for safety reasons`），用 app 名或换寻址。

## 5. 交互工具速查

- `click`：`element_token`（AX）或 `x,y`（像素，window-local 或 from_zoom）；button left/right/middle；action press/show_menu/open/...；count 双击等。
- `type_text`：插文本。优先在目标元素聚焦/可见状态写；像素路径配合 from_zoom。
- `press_key` / `hotkey`：快捷键（如 `super+a`，xdotool key 风格）。
- `scroll`：目标化滚轮路径（`element_token` 或 `x,y`）命中嵌套 `overflow:auto` 区域；无目标用按键路径滚聚焦区。
- `drag`：`from_x,from_y,to_x,to_y`（窗口本地像素）。
- `set_value`：直接写可设置控件（比 type_text 语义化，适合 search/text field）。
- `verify_state`：确定性校验一轮动作是否生效。

## 6. 典型流程（微信聊天区像素降级示例）

```bash
# 1. 定位窗口
cua-driver call list_windows '{}' | jq '.windows[] | {wid:.window_id,pid,title,app_name}'
# 2. 快照会话区（AX 导航可用）
printf '{"pid":48292,"window_id":1828,"max_elements":200,"max_depth":8}' | cua-driver call get_window_state
# 3. 点开一个会话 —— AX token（列表项可达）
# 4. 聊天区/输入框在 AX 外 → zoom 裁右下输入区，from_zoom 点 + 打字
printf '{"pid":48292,"window_id":1828,"x1":640,"y1":600,"x2":820,"y2":680}' | cua-driver call zoom
printf '{"pid":48292,"window_id":1828,"x":30,"y":50,"from_zoom":true}' | cua-driver call click
printf '{"pid":48292,"window_id":1828,"x":30,"y":50,"text":"你好","from_zoom":true}' | cua-driver call type_text
```

## 7. 常见失败 → 解法

- **点击无效 / 截图黑**：Screen Recording 未授权 → `permissions grant` 后重启进程。
- **像素点错位**：截图用了 downscale 或 2x。→ 用 `from_zoom`（别手算），或用 `get_desktop_state` 的真实像素 + backing scale。
- **对象 couldn't resolve / element stale**：snapshot 过期 → 重新 `get_window_state` 拿新 token。
- **后台收不到输入**（canvas/镜像）：该 app 事件循环要 key-window state，后台无解 → 前台 + C 档。
- **安全拒绝**：bundle id 被 denylist → 换 app 名寻址或调整配置。

## 8. 识图（视觉验证）方法

主模型读不了图 / 缺视觉时，用本 skill 附带的识图脚本（可配置 endpoint）。**endpoint/key 配置见 README 与 `~/.config/vision-config.json`（安装时生成模板）**：

```bash
VISION_PY=<你安装脚本的位置>/vision.py   # 例: ~/.config/opencode/skills/desktop-gui-automation-cua/scripts/vision.py
python3 $VISION_PY /tmp/win.png "截图底部最新消息是什么？"
# 覆盖模型/超时可选:
python3 $VISION_PY /tmp/win.png "描述界面" --model gpt-4o --timeout 60
```

- 端点、key、模型来自 **环境变量或 `~/.config/vision-config.json`**：`VISION_BASE_URL` / `VISION_API_KEY` / `VISION_MODEL`（或配置文件 JSON）。任意 OpenAI 兼容多模态 `/chat/completions` 都行。
- 若 endpoint 在 `opencode.ai` 域名，脚本会自动带 Origin/Referer 头避免 Cloudflare 403；其他端点不带。
- 这是视觉定位与"操作结果验证"的默认手段。

- 这是 `inspect_image` 工具的关键替代：工具本身在部分会话会 `ctx is not defined`，直接调网关脚本永远可用。
- 图片先落盘（`get_window_state`/`zoom`/`get_desktop_state` 的 `--screenshot-out-file`），再喂给脚本。

## 9. 微信实操实测要点（2026 实证，直接照抄）

在真实微信（4.x）上向"小号"发句号"。"的完整可行链路（已验证成功）：

1. **微信会把会话开在独立聊天窗口**（如 wid=2087 title="小号"），而**独立聊天窗口的 AX 树是完整的**：输入框 `AXTextArea '输入'`、消息列表 `AXList '消息'`、标题、各按钮都标号。所以对这类会话，**主窗口聊天区 AX 空、独立窗口 AX 可用**——直接 AX token 操作，不必像素降级。
2. **写文本用 `set_value`**（AX, confirmed value_readback），比 type_text 可靠；`type_text` 在微信多窗口时会被 `same_pid_keyboard_ambiguity` 拒绝（Keyboard 无法定向到指定窗口）。
3. **发送必须先把窗口带到前台**：`bring_to_front`（返回 `bring_to_front_exact_window_verified` 才是真的前台）→ 点输入框设焦点 → `press_key {key:Return, delivery_mode:foreground}`。后台 Enter 不会触发微信发送。
4. **验证：最新消息在底部**，滚动要**往下**滚到真正底部（用滚轮 over 消息区 `direction:down`，AXList 的 page 滚可能在小程序/WebView 大块内容里失灵）。见上方第 8 节的识图脚本确认气泡。
5. 会话列表里"小号"这类不可靠命中时应改用**搜索框**（AXTextArea '搜索'）`set_value` 输入关键词，微信会过滤出该会话；清空用 set_value 空串。

## 10. iPhone 镜像（像素级操控，已验证）

iPhone Mirroring 窗口 = **AX 空（只有窗口外壳/菜单） + 强制前台接收输入**的 Metal 窗口。必须**像素级操控**。已封装 `scripts/iphonemirror.py`：

```bash
python3 iphonemirror.py find                 # 找镜像窗口(pid/wid/bounds)
python3 iphonemirror.py inspect "提示词"      # 截图 + mimo 描述当前iPhone屏幕
python3 iphonemirror.py tap "Dock栏的照片"     # 两阶段识图定位 + 像素点击(已验证能打开app)
python3 iphonemirror.py tapxy <x> <y>        # 直接 window-local px 点
python3 iphonemirror.py home                 # 点底部Home条回主屏(已验证)
python3 iphonemirror.py swipe up|down|left|right [比例]  # 触摸滑动(已实测在图库滚动生效)
python3 iphonemirror.py type <文本> [--tap "输入框描述"]  # 文本输入(输入框已聚焦则直接; --tap 自动聚焦)
python3 iphonemirror.py shot [path]          # 截图
```

实测要点（2026 验证通过）：
- **坐标铁则**：cua-driver click 的 x/y = **window-local screenshot px**（`get_window_state` 的 PNG 尺寸，如 708×1562）。**绝对不要用 screen 坐标或逻辑坐标**。
- **前台必须**：`bring_to_front {pid,window_id}` → `bring_to_front_exact_window_verified` 才确认前台；然后点击带 `delivery_mode:"foreground"`。若镜像本来就是前台(查询 frontmost)，可跳过 bring_to_front(它偶发卡住)。
- **tap 两阶段定位**：完整图 mimo 粗定位(归一化) → 以粗点为中心 zoom 放大 → mimo 在放大图精确定位 → 换算回全窗 px。避免 mimo 对绝对像素的误判(它给 y=1900 这种超界值)。
- **坐标定位更可靠的是 sips 裁剪校准**：`sips -c <h> <w> --cropOffset <y> <x> full.png --out cell.png` 裁出目标网格块，mimo 确认"图里就是该图标"+给块内坐标，再加 offset 回全图。(mimo 的绝对像素估计不稳定, 别依赖它直接给 px)
- **已验证成功的像素操作**：`tapxy` 打开备忘录(120,750)、`tap Dock栏的照片`(图库)、`home`、`swipe`(图库滚动)。
- **文本输入正解(已验证)**：iPhone 镜像前台 + **目标输入框已聚焦**(tap 点击聚焦**之后**) → `type_text` 用 `scope:"desktop"`(输入到前台镜像,首选) 或 `delivery_mode:"foreground"` → **文本能成功输入**(实测打"文本输入测试验证"进备忘录正文)。注意：iOS 虚拟键#盘**不会弹出**(镜像作为外部硬件键盘),这是平台行为,mirroir-mcp 同记录。之前 type 失效的根因是**输入框没聚焦**(主屏/非编辑态 type 被系统忽略), 不是 type 本身不行。
- 限制：Cmd+V 剪贴板不桥接; 个别 ISO 键(§±)受限(mirroir-mcp)。
- 启动：`open -a "iPhone Mirroring"`。

## 11. QQ 群聊发消息（泛用流程案例，已验证）

QQ(新版, QT/CEF) 给"自己的学习群"发句号——完全用本 skill §0 泛用流程，无 app 专用配方，一把跑通：

```
1. windows QQ         → 主窗口 wid(可见大窗, 实际有时 on=False 但能用)
2. probe QQ --wid N   → A档(AX 完整): 会话列表项是 AXStaticText(AX 树很大, 含群名/预览/时间)
3. snapshot 找目标    → AXStaticText label="自己的学习群" (idx 47) → 记 element_token
4. click --token      → 切到该群聊天(路由 suspected_noop/hit-test, 但仍生效)
5. inspect/vision     → 确认已打开群聊天; 聊天区含"输入框"(QT 里 AX 可能不暴露输入框元素)
6. sips 裁剪校准坐标  → 裁输入框区域, mimo 给 NX/NY → 得输入框中心 window-local px (~900,875)
7. click --x --y foreground + bring_to_front → 点输入框聚焦(确认光标出现)
8. type "。" (desktop scope) → 句号进输入框(识图确认)
9. key Return foreground  → 发送(QQ 默认 Enter 发送)
10. vision 验证         → "自己的学习群" 最新消息 = 句号；输入框已空
```

要点：
- QQ 的 AX **会话列表项可达**(群名是 AXStaticText)，但**点击静态文本可能 hit-test/suspected_noop**——别被 effect=noop 骗, 用识图确认真切换了。
- QT/CEF 的**聊天输入框可能不在 AX 树里** → 用 B 档像素:sips 裁输入框区+mimo 定位, 再前台聚焦点击。
- 发送: QQ 默认 **Enter 发送**; 若 Enter 换行则试 Ctrl+Enter 或点发送按钮。

## 12. 环境与依赖（这个 skill 能在别人电脑上用吗？）

**授权/权限（本机级，无法通过 skill 自带, 必须用户手动）**:
- macOS 的 **Accessibility + Screen Recording** 双权限，授予给**驱动进程自身**（`com.trycua.driver` 或宿主 agent 进程）。这是 macOS TCC 强制的, skill 无法代授。
- cua-driver 需可启动（守护进程 https://cua.ai 的产品）。

**外部 CLI（需已安装到 PATH）**:
- `cua-driver`（必需, 驱动核心）
- `sips`（macOS 自带）
- `osascript`（macOS 自带, 查前台用）
- `open`（macOS 自带）

**识图视觉（软依赖, 缺了则无法视觉定位/验证; 可配置, 可移植）**:
- `vision.py` 支持任意 OpenAI 兼容 `/chat/completions` 多模态端点。配置优先级: 命令行 `--model` > 环境变量（`VISION_API_KEY`/`VISION_BASE_URL`/`VISION_MODEL`）> 配置文件 `~/.config/vision-config.json`（JSON: `{"api_key","base_url","model"}`）。
- **换环境只需设 `VISION_API_KEY` + `VISION_BASE_URL`（或用配置文件），不必改代码**。例如: `VISION_BASE_URL=https://api.openai.com/v1 VISION_API_KEY=sk-... VISION_MODEL=gpt-4o`。
- 若 endpoint 设在 `opencode.ai` 域名，脚本会自动带 Origin/Referer 头规避 Cloudflare 403；其他端点不带。
- 缺视觉仍可纯 AX 工作（A 档），只是无法识图定位/验证。

**代码依赖**: `cua_lib.py`/`computer_use.py`/`vision.py` 只用 Python 标准库（python3 自带；配置文件用 JSON，不依赖 yaml）。`send_wechat.py`/`iphonemirror.py` 是可选 app 配方。

**可移植性结论**: 本仓库是一个自包含发布包（`scripts/` 单一事实源 + SKILL.md/README/install.sh/update.sh + plugin/ 可选壳）。换一台 **macOS 机器**：装好 cua-driver（`install.sh` 可自动装）、授予 Accessibility + Screen Recording 双权限（手动）、配一个多模态 API（环境变量或 `~/.config/vision-config.json`）→ 即可用。升级时在仓库里 `git pull && ./update.sh`（重建符号链接 + 版本自检，保证 skill 与插件一致、无漂移）。**Windows/Linux 需 cua-driver 对应平台后端**（它跨平台，但鼠标/键盘/AX 实现不同，本仓库的 app 配方含 macOS 特定逻辑需适配）。

## 13. 参考
- 底层驱动 cua-driver: https://github.com/trycua/cua
- Codex CUA 机制与"AX 不可达"应用研究（作者笔记）
- 逆向参考（Codex CUA 9 工具 / Skyshot 模型）: github.com/iFurySt/open-codex-computer-use
- iPhone 镜像限制: github.com/jfarcand/mirroir-mcp（limitations.md）
- 后台 CUA 方法论: github.com/antimatter15/macos-background-cua-skill
