---
name: computer-use-drive
description: "Use when 用 AI 直接操作桌面窗口（鼠标/键盘/截图）。"
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [computer-use, gui, automation, windows]
---

# 用 computer_use 拖桌面窗口

比浏览器自动化强的地方：能开原生应用、能点安装向导、能读你正在用的窗口。

## When to Use

- 用户要“你看着我操作/你自己点一下”
- 原生应用（exe、安装向导、游戏客户端、Electron 客户端）
- 浏览器撞上风控/登录墙，需要真人身份操作
- 验收 GUI 效果（截图给人看）

## 铁律：先用手上的工具，别造轮子

这类活最容易失控的方式，是先把能力“造”出来再去干活。顺序必须是：

1. **先看 toolset 有没有现成的**：`computer_use`（可见窗口的真实鼠标键盘）、`browser_exec`（无头 CDP + 无障碍树）、`browser_vault_*`（掩码弹窗 + 加密填充）、`/browser connect`（接管用户正在用的浏览器）。这四个覆盖绝大多数需求。
2. **只有现成工具确实够不到，才写脚本**。动笔前先分清“能力缺口”和“配置问题”：端口被占、扩展没开、profile 被锁、守护进程卡死——全是配置问题，不是要你重写一个浏览器。
3. **同一个操作失败 2~3 次就换路，并且明确告诉用户“这条路走不通，我换 X”**。不要在同一处反复改参数、改坐标、加重试。用户会先失去耐心，然后才轮到你发现问题。
   **元素/字段检测返回空、或连续两次点不中，立刻截图看一眼。** 继续往下加解析层（execution context、frame tree、自定义选择器）的成本远高于一张截图，而截图会直接告诉你“页面上到底有没有那个东西、它在哪个区域”。先看图，再决定要不要写解析代码。
4. **用户说「不要写脚本，直接操作」时，就是字面意思**：用现有工具点、输、看，不要新增任何 .py。
5. 造出来的东西要**当场验证并给出数字**（窗口标题、字段数、字符长度、帧大小），不要只报“已修复”。这个用户对“说已修但实际没好”极其敏感，结论必须带可复现证据。
6. **不要用固定 `sleep` 等页面**。点击/提交后轮询目标状态（URL 变化、错误文案、元素出现），0.4s 一次、设个上限。固定 `sleep 8` 让每一步都白等 8 秒，用户会直接问「为什么这么慢」；而工具链本身很快——实测取一帧 6~19ms、单次 CDP 动作（连接+求值）5~30ms、python 冷启动 94~127ms。慢只可能来自固定 sleep、服务重启、或每步一个独立进程。
7. **用户说「停下」「不要乱做」就立刻停手。** 不要边停边把手上那步做完，也不要顺手“再修一下”。停下来的第一句话是现状清单：哪些已经改了、哪些没动、怎么撤回——用户判断要不要继续靠的是这份清单，不是解释。

## 前置

```bash
hermes computer-use status     # 应显示 installed + Runtime contract ready
hermes tools list | grep computer_use
```

Windows 上驱动在 `$HERMES_HOME/tools/cua-driver-<ver>-win32-x64/cua-driver.exe`。

## 打包给别的 agent：标准 MCP server

`scripts/mcp_server.py` 是一个**真正的 MCP stdio server**（JSON-RPC over stdio），
把浏览器能力和凭据能力一起暴露出去。同一份文件，三种客户端配置：

Claude Desktop / Claude Code（JSON）:

```json
{"mcpServers": {"browser": {"command": "python",
  "args": ["<绝对路径>/scripts/mcp_server.py", "--cdp-endpoint", "http://127.0.0.1:18763"]}}}
```

Codex CLI（`~/.codex/config.toml`，注意是 TOML 且顶层键 `mcp_servers`）:

```toml
[mcp_servers.browser]
command = "python"
args = ["<绝对路径>/scripts/mcp_server.py", "--cdp-endpoint", "http://127.0.0.1:18763"]
startup_timeout_sec = 60   # 默认 10s，npx 首次下载会超时
```

Hermes（`hermes mcp add browser --command python --args <路径> --cdp-endpoint http://127.0.0.1:18763`）。

它暴露 **27 个工具**：25 个 `browser_*`（快照/点击/输入/导航/标签页/截图/求值）
转发给微软官方 `@playwright/mcp` 子进程，另外 2 个自己实现：

| 工具 | 作用 |
|---|---|
| `cred_list` | 列出 handle / label / origin，**没有密码** |
| `cred_fill` | 按 origin 找到凭据 → 让本机代理解密并注入 → 可选提交。密码不回到模型上下文 |

实测：`initialize` 正常、`tools/list` 27 个、`browser_snapshot` 187ms 返回 54KB 无障碍树、
`cred_list` 走 broker 拿到 3 条凭据。

## 多 agent 隔离：一个 session 一套环境

两个 agent 共用一个浏览器会互相抢标签、快照 ref 互相失效、登录态串号。`scripts/session.py`
给每个 agent 开一套完全独立的：

```bash
python session.py new --name a1 --url https://example.com
python session.py list
python session.py stop --name a1
```

一个 session 独占：

| 资源 | 独立内容 |
|---|---|
| 桌面 | `HermesDesk-<name>` |
| profile | `<profiles>/<name>`（独立 cookie / 扩展 / 登录态，互不可见） |
| CDP | 18763 起顺排 |
| 推流 / 驱动 | 8765 / 8897 起顺排 |
| 预览 | `http://127.0.0.1:<stream>/ctl` |

实测 `a1`：cdp=18764 / stream=8766 / driver=8898，它只看得到 example.com；
主 session 同时仍开着 Cloudflare + QQ 邮箱，两边互不影响。`stop` 只关该桌面的 Chrome
和它自己的两个服务，主 session 三个端口照常。

## 安装第一步：在聊天里问用户装哪里

浏览器 profile 里装着登录态、钱包扩展、凭据库，**装错盘以后迁移很麻烦**。所以第一次运行前
必须让用户选，不要默认塞进 C 盘（实测这台机器 C 盘只剩 5.2GB）。

```bash
python setup.py --options     # 输出候选，JSON
python setup.py --home "D:\hermes-browser"   # 用户选完再落盘
python setup.py --show        # 看当前配置
```

`--options` 返回的每一项都带可用性和剩余空间：

```json
[{"id":"localappdata","label":"系统用户数据目录（推荐，默认）",
  "path":"C:\Users\<你>\AppData\Local\hermes-browser","writable":true,"free_gb":5.2,"note":""},
 {"id":"drive_d","label":"D 盘根目录","path":"D:\hermes-browser","writable":true,"free_gb":180.3,"note":""}]
```

**agent 该怎么做**：把这份列表渲染成聊天里的选项（Hermes 用 `clarify`，其他客户端直接提问），
把 `free_gb` 一起显示出来——空间小于 5GB 的要提醒用户。用户选完，跑 `setup.py --home <path>`，
然后把输出里的 `home` 和 `settings_file` 念给用户确认。**不要替用户决定**。

落盘位置固定在 `%LOCALAPPDATA%\hermes-browser\settings.json`（指针文件，位置固定才不会找不到），
内容形如 `{"home": "D:\hermes-browser", "installed_at": "..."}`。之后：

- `profiles/` → `<home>/profiles`
- 凭据库 → `<home>/vault/broker.json`
- 端口记录 → `<home>/ports.json`

优先级：`HERMES_*` 环境变量 > `settings.json` 的 `home` > 旧路径兼容 > 默认值。
**旧路径兼容**：只有用户没选过位置时，才回落到 `<legacy-profiles>` / `<legacy-home>\vault\broker.json`（这样老机器升级不会丢钱包）。用户一旦在 setup 里选了新目录，就以新目录为准。

## 可移植：没有固定盘符、没有固定端口

发给别人时最容易炸的两件事——写死盘符、写死端口。现在全部走环境变量 + 自动回退：

| 变量 | 默认值 | 说明 |
|---|---|---|
| `HERMES_BROWSER_HOME` | `%LOCALAPPDATA%\hermes-browser`（mac/Linux: `~/.local/share/hermes-browser`） | profile、vault、ports.json 的根 |
| `HERMES_PROFILES` | `<HOME>/profiles` | Chrome profile 根目录 |
| `HERMES_VAULT` | `<HOME>/vault/broker.json` | 凭据库 |
| `HERMES_CHROME` | 自动探测（Win 两处 Program Files / LocalAppData，mac `/Applications`，Linux `google-chrome`/`chromium`） | 浏览器可执行文件 |
| `HERMES_DESK` | `HermesDesk` | 私有桌面名 |
| `HERMES_CDP_PORT` / `HERMES_STREAM_PORT` / `HERMES_BROKER_PORT` / `HERMES_DRIVER_PORT` | 18763 / 8765 / 8899 / 8897 | 各自端口 |
| `HERMES_PYTHON` | `pythonw`（PATH 里找不到就 `python`） | 启动服务用的解释器 |

### 访问令牌：挡住同机其他进程

8899 上跑的是凭据代理，**任何本机进程**都能 `GET /inject_sel?handle=...` 让浏览器把密码填进
一个 origin 相同的页面。所以除只读探针外，全部要 `X-Hermes-Token`。

- token 首次启动自动生成（32 字节随机），写到 `<home>/token.txt`，权限 600
- 客户端（`cred_dialog.py`、`login_flow.py`）自己从同一文件读，用户无感
- `HERMES_TOKEN` 环境变量优先，方便临时覆盖

| 端口 | 免 token（只读探针） | 需要 token |
|---|---|---|
| 8899 broker | `/health` | `/list` `/describe` `/save` `/inject*` `/delete` |
| 8897 driver | `/status` | `/snap` `/click` `/type` `/goto` `/eval` `/tool` |
| 8765 stream | `/snapshot` `/stream` `/ctl` `/view` | `/c` `/t` `/k` `/focus` |

`/ctl` 页面由服务自己吐出，token 在渲染时注入（`var TOKEN = "__TOKEN__"` 被替换），
所以控制页照常能点能打字。实测矩阵：无 token 调 `/list` `/describe` `/snap` `/c` 全 401，
带 token 全 200。

### 错误码与审计

`/inject_sel` 失败不再只回一段文字，带 `code`：

| code | 含义 | agent 该做什么 |
|---|---|---|
| `unauthorized` | 没带 token | 从 `<home>/token.txt` 读 |
| `no_target` | 没有匹配的页面 | 检查 `?url=` 关键字 |
| `origin_mismatch` | 页面 origin ≠ 凭据绑定 origin | 不要绕过，换正确的 handle |
| `not_found` | 选择器找不到元素 | 重新快照拿新选择器 |
| `verify_failed` | 读回校验不通过 | 重新弹窗让用户重输，**不要提交** |
| `decrypt_failed` / `no_handle` | 凭据库问题 | 重新 `/save` |

每次注入都写一行 `<home>/audit.jsonl`：时间、action、origin、handle、ok、code。**不记明文**。

### 端口被占就自动换（`ports.py`）

默认端口只是"首选"，不是"必须"。`ports.py` 的规则：

1. 默认端口空着 → 用。
2. 被占，但探针认出**是我们自己的服务**（broker 看 `/health` 返回 `"ok"`、driver 看 `/status` 返回 `"ready"`、stream 看 `/snapshot` 返回 JPEG、cdp 看 `/json/version` 返回 `"Browser"`）→ 继续用。
   **探针必须挑免 token 的只读端点。** 给服务加了鉴权以后，如果探针还打 `/list` 这类受保护接口，会拿到 401、认领失败，结果是每次启动都在新端口上再起一个实例。鉴权矩阵里“免 token”那一列，就是探针能用的全部端点。
3. 被别的程序占着 → 从默认值往上找第一个空闲端口。

实际端口写进 `<HOME>/ports.json`，客户端（`cred_dialog.py`、`login_flow.py`）读它，不靠猜。
`cdp` 例外：那是**已经开着的浏览器**的端口，只能沿用，绝不自动改（改了就连不上）。

```bash
python ports.py           # 看当前分配 + 每个端口是谁的
python ports.py --free    # 重新分配并写入
```

### 起服务用 `svc.py`，不要用 .bat

从 git-bash 里跑 `cmd /c xxx.bat` 会弹出一个真实的 cmd 黑框（Windows 给 cmd.exe 分配控制台）。

**`DETACHED_PROCESS | CREATE_NO_WINDOW` 只解决“不弹窗”，解决不了“被收尾带走”。** 如果宿主用作业对象
收尾（Job Object + KILL_ON_JOB_CLOSE），detached 的子进程照样被杀——症状是：启动当时查端口是 UP，
隔一个回合再看全 DOWN，用户看到的就是“说启动好了，其实早没了”。

正确做法：用 WMI 创建进程，父进程变成 `WmiPrvSE.exe`，彻底在宿主的进程树之外。

```python
subprocess.run(["wmic", "process", "call", "create",
                f'"{pythonw}" "{script}" ' + " ".join(args)],
               capture_output=True, text=True)
# 成功时输出里有 ReturnValue = 0 和 ProcessId = <pid>
```

**验收看父子链，不要只看端口通不通**（端口可能是上一个没死的实例在应答）：

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId=<监听端口那个 pid>" |
  ForEach-Object { $p=$_; $par=Get-CimInstance Win32_Process -Filter "ProcessId=$($p.ParentProcessId)";
                   "$($p.Name) <- $($par.Name)" }
```

正确结果末端是 `WmiPrvSE.exe`；如果末端是 `bash.exe` / `python.exe`（你的宿主），就还没脱离，早晚会被杀。
注意 venv 里 `pythonw.exe` 常常再拉起一个 `python.exe` 干活，所以链是 `python.exe <- pythonw.exe <- WmiPrvSE.exe`，
多一层不算错。

WMI 不可用时会回退到 `Popen` + detached —— 那条路又会回到“会被杀”的状态，**回退时必须主动告诉用户**，
不要静默降级。

两条已证伪的“保活”做法，别再用：
- 用 Hermes 的 `background=true` + `persist_on_release=true` 起服务：实测仍然会被 `process.kill`（`exit_code: -15`），存活几十分钟后照样消失。
- `.bat` 里 `start /b`：只是不弹新窗口，**没有脱离进程树**，起它的那个 cmd 会话一结束，子进程跟着死。

判断标准：启动后**等过一个工具调用的生命周期再查一次端口**，还在才算真常驻。

```bash
python svc.py            # 缺哪个起哪个（会先去端口附近找已在运行的实例，避免起重复）
python svc.py --status   # 只看状态
python svc.py --stop     # 停三个
```

**起完立刻把画面给用户看**：`desktop_preview(action="open", url="http://127.0.0.1:<推流端口>/ctl", label="浏览器画面")`。
用户要的是“我能看着你操作”，不是“你报告说启动了”。`/ctl` 页面的端口由服务渲染时代入，
换过端口也能直接用这个地址，别手写 `desk_view.html` 的本地文件路径（`file://` 连不上本机服务）。

重复启动的坑：`svc.py` 只检查"端口是否通"会在服务还没绑上端口时误判，起出第二个实例。
所以启动前先用 `ports.find_existing()` 在默认端口附近扫特征接口，认出来就跳过。

`--stop` 之后**必须按端口核对一遍**（`netstat -ano | grep ":<端口> " | grep LISTENING`）：它按 `ports.json` 记的端口去杀，端口漂过或旧进程还占着默认端口时会漏杀，漏下的那个还会让下一次启动以为“已在运行”而跳过。

### 写这些脚本时的坑：路径里的反斜杠会被吃掉

用 bash heredoc（`python - <<'EOF'`）批量写含 Windows 路径的文件时，Python 会把 `\v` `\b` `\H` 当转义序列：
`<legacy-home>\vault\broker.json` 会变成垂直制表符 + 退格 + 字母 H，写进文件后表现为“某行莫名少字、
`grep` 搜不到、`os.path.exists` 永远 False”（`vault_path()` 明明存在却判不存在就是这个原因）。

规则：
- 路径一律用 raw string（`r"E:\..."`）或 `chr(92)` 拼接，别在普通字符串里裸写反斜杠；
- 批量改文件优先用 `patch` 工具（它按字面量匹配，不做转义），heredoc 只用来跑逻辑、不用来拼路径字面量；
- 写完扫一遍控制字符，有就是被吃了：
  `[i for i,l in enumerate(open(p,encoding='utf-8').read().splitlines()) if any(ord(c)<9 or 13<ord(c)<32 for c in l)]`

## 工作流

1. `list_windows` — 先看真实窗口列表（带 pid / window_id / z_index）
2. `capture(mode='som', app='<exe>')` — 拿到带编号的可交互元素 + 自动视觉分析 + 截图路径
3. 用 `element` 索引点击/输入，不要手算坐标
4. 改状态后重新 capture 验证，不要盲信任

```
capture  → element 索引
click    → element=N, button=left
 type    → element=N, text='...'（或全局 type 不带 element）
key      → keys='return' / 'ctrl+s' / 'ctrl+alt+t'
drag     → from_element → to_element
scroll   → direction + amount
set_value→ 下拉框/滑块直接设值，不开原生菜单
```

## Windows 上的真坑（实测）

1. **窗口最小化时后台投递静默失败**。`delivery_mode: background`（默认）走 PostMessage，对已最小化的窗口（bounds 变 `-32000,-32000`）会返回 `ok: true` 但**文本根本没进去**，`effect: unverifiable`。必须升 `delivery_mode: 'foreground'`（会短暂前置窗口，单独审批）。
2. **`type` 的 `\n` 不会变成回车**。多行要用 `action='key', keys='return'` 另发。
3. **element bounds 是原生桌面坐标，不是截图坐标**。截图 917x595 而桌面 1462x724 时缩放约 1.59x；用 `element` 就无需换算。
4. **capture 自身偶尔把窗口弄回最小化**，`capture_after=true` 拿到的可能是 `0x0` 的废图——改完状态后单独再 capture 一次。
5. **不要指向 cua-driver 自己的授权进程**，否则报 `Permission denied: Cua Driver refuses operations that target its own authorization process`。指定 `app=` 绕过。

## 验证标准

看标题栏有无 `*`（已修改）、看状态栏光标位置、看 `vision_analysis` 里的文字——不要只看工具返回的 `ok: true`。

**必须跑第二遍。** 第一次成功不代表对：表单第一次填是空框（`insertText` 的追加语义看不出来），第二次才有旧值；页面多了一条错误提示后坐标会整体下移。凡是“注入 / 填充 / 重试”类改动，验收标准是**连续两次都正确**，再加故意错一次，看它会不会自己重弹。

## 自己的桌面（完全不碰用户桌面）

`computer_use` 只能驱动用户当前桌面。要真正隔离，Windows 上用 Win32 桌面对象：

- `user32.CreateDesktopW("HermesDesk", ..., GENERIC_ALL=0x10000000, None)`
- `CreateProcessW` 时把 `STARTUPINFO.lpDesktop = "HermesDesk"`，子进程的窗口就不会出现在用户桌面
- 枚举：在**没有建过窗口的新线程**里 `SetThreadDesktop(hDesk)` → `EnumDesktopWindows`
- 输入：`WM_SETTEXT (0x000C)` 写、`WM_GETTEXT (0x000D)` 读回 —— 全消息级，零像素、零焦点
- 截图（需要时）：`PrintWindow(hwnd, hdc, PW_RENDERFULLCONTENT=2)` + `GetDIBits`
- 子控件：`FindWindowExW(hwnd, None, "Edit", None)`

坑：
1. 桌面对象同名复用，进程退出后窗口仍留在上面 —— 跑多次会累积多个同名窗口，按标题找会拿错，得先 `taskkill` 清场。
2. `EnumDesktopWindows` 会把 `Tooltip` / `CiceroUIWndFrame` / `Default IME` 这类系统窗口一起返回，必须同时按标题 + `GetWindowRect` 尺寸 >50x50 过滤。
3. 一个线程只能 `SetThreadDesktop` 一次，且必须在建窗口前；单独开 threading.Thread 做。
4. `SendMessageW` 带字符串参数不能直接改 argtypes，用 `ctypes.WINFUNCTYPE(w.LPARAM, w.HWND, w.UINT, w.WPARAM, w.LPCWSTR)(("SendMessageW", user32))`。
5. 这条路线是 Windows 专属。Linux 用 `hermes computer-use screen start`（Bot Screen / Xvfb over VNC）；要最大隔离就用 `terminal.backend: docker`。

参考实现（已随技能内置，不要指向 scratch，那里 24h 会清）：

**改脚本只改技能目录里的这一份。** 在别处留一份副本（临时工作目录、项目里）迟早会漂移：改完在副本上验证通过，服务却还在跑旧的那份，症状是“明明修了却没生效”。从技能目录启动服务，`svc.py` 用 `%~dp0`/`__file__` 定位同目录脚本，天然不会跑错文件。
- `scripts/private_desktop.py` — 建桌面 / 生进程 / 枚举 / `WM_SETTEXT`+`WM_GETTEXT` 闭环 / `PrintWindow` 截帧
- `scripts/desk_chrome.py` — 按桌面名起独立 Chrome（一桌面一 profile 目录 + 可选 CDP 端口）
- `scripts/desk_stream.py` — 把该桌面窗口推成 `127.0.0.1:PORT/snapshot` + `/stream.mjpg` + `/cursor` + 反向输入 `/c` `/t` `/k`
- `scripts/vault_broker.py` + `scripts/cred_form.html` — 凭据代理（DPAPI 加密 + handle + 最后一公里注入）与它按页面字段自适应生成的表单页
- `scripts/desk_browser.py` — CDP 驱动（真实点击/输入 + 光标同步 + 坐标标定）
- `scripts/svc.py` — **起三个常驻服务的唯一正确方式**：用 WMI（`Win32_Process.Create`）起 pythonw，父进程是 `WmiPrvSE.exe`，既无控制台窗口也不在宿主进程树里（`DETACHED_PROCESS` 做不到后者）；带 `--status` / `--stop`，并先用 `ports.find_existing()` 认出已在运行的实例，避免重复启动
- `scripts/ports.py` — 端口分配：默认端口被别人占了自动换，实际端口写 `<HOME>/ports.json`；`cdp` 例外，只沿用不改
- `scripts/auth.py` — 本机服务访问令牌：首次启动生成 32 字节随机串写 `<home>/token.txt`，`check(headers, query)` 给各服务用，`headers_for_client()` 给客户端用；`HERMES_TOKEN` 可覆盖
- `scripts/setup.py` — 首次安装：`--options` 出候选目录（带可写性/剩余空间），`--home` 落盘到 `settings.json`
- `scripts/start_services.bat` — 仅给“人类双击”用；`start /b` **不能**脱离进程树，别用它给 agent 起服务
- `templates/desk_view.html` — 聊天里看实时画面的 canvas 查看器（只读）
- `templates/desk_ctl.html` — 同一套画面的**可操作**版本：点画面 = 真实点击，打字 = 送进私有桌面

### 在私有桌面上开浏览器，必须给隔离 profile

profile 目录、cookie 文件、真实 profile 副本、密码库各自存在哪，和"登录态会不会丢"的判定：
`references/browser-data-locations.md`。

直接用 `chrome.exe <url>` 会命中已在运行的 Chrome 单例，把 URL 丢进**用户自己**的窗口；就算没命中，也默认用用户 profile，cookie / 登录态全串。固定写法：

```
chrome.exe --user-data-dir="<legacy-profiles>\<桌面名>" --new-window \
           --no-first-run --no-default-browser-check --disable-gpu \
           --remote-debugging-port=<空闲端口> \
           --window-size=1280,860 --window-position=0,0 "<url>"
```

`--user-data-dir` 放 scratch 里登录态会跟着被清。**本机固定约定**：所有私有桌面浏览器的数据都在
`<legacy-profiles>\<桌面名>\`，一个桌面一个目录，永不共享 profile。scratch 只放脚本。

### 只杀自己那个窗口的进程

不要 `taskkill /IM chrome.exe` —— 会杀掉用户正在用的浏览器。正确做法：枚举该桌面窗口 → `GetWindowThreadProcessId(hwnd)` 取 pid → 只杀它。桌面对象上枚举到的 hwnd 一定属于你自己启的进程。

一个 Chrome 实例在本机实测是 **12 个进程**（1 主进程 + 8 renderer + gpu + 2 utility + crashpad），所以「一个浏览器 = 一个进程」的直觉是错的：按名字杀会连用户的浏览器一起带走，按进程数判断健康也没意义。

### 多个私有桌面：一桌面一世界

需要多个互不影响的浏览环境时，**桌面名就是唯一键**，四样东西全部按名字派生：

| 维度 | 规则 |
|---|---|
| profile | `<legacy-profiles>\<桌面名>\` |
| 进程 | 每桌面独立 Chrome 进程树 |
| CDP 端口 | 每桌面一个：`--remote-debugging-port=<端口>` |
| 推流端口 | 每桌面一个：`desk_stream.py --port <端口> --desktop <桌面名>` |
| 查看器 | 每桌面一个 HTML（复制 `templates/desk_view.html`，改 `SNAP` 端口和标题） |

验收：枚举各桌面窗口，每个桌面应**只**看到自己的那个 Chrome；cookie / localStorage / 历史零交叉。

### 持久化：重开要能接着用

用户说「下次打开不能什么都没了」时，光把 profile 放对位置不够，四件事缺一样就白弄：

1. **profile 必须在持久盘**。`cache/scratch` 下 24h 被清，登录态跟着没。
2. **绝不用 `taskkill /F` 关 Chrome**。强杀会丢未刷盘的 cookie，还在 Preferences 留 `exit_type: Crashed`。正确：对每个顶层窗口 `PostMessageW(hwnd, WM_CLOSE=0x0010)`，轮询 `OpenProcess` + `GetExitCodeProcess != STILL_ACTIVE(259)` 等它自己退，超时才强杀。实测优雅退出 0.5–1.0s。
3. **不要依赖 `--restore-last-session`**。实测会对同一个 profile 时灵时不灵，还会带回「要恢复页面吗？」气泡。自己存：关之前 CDP `/json` 取 page 列表 → 写 `<profile>/hermes-tabs.json`；重开时把 URL 列表当参数传（`chrome.exe --user-data-dir=... url1 url2`）。
4. **启动前清崩溃标记**。Chrome **未运行**时把 `Default/Preferences` 的 `profile.exit_type` 改 `"Normal"`、`exited_cleanly` 改 `true`，否则永远弹恢复气泡。注意：Chrome **运行中**读这个文件永远看到 `Crashed`（它启动时自己写），别误判。

验收脚本思路：CDP 写 `localStorage` + `document.cookie` 标记 → 优雅关 → 重开 → 读回一致 → PASS。标记能跨多轮重启活下来才算数。

批量恢复：`scripts/desk_restore.py` 枚举 `<legacy-profiles>\*` 下的 profile，按 `desktops.json` 里的 cdp/stream 端口逐个 `--restore`，一条命令重建所有桌面。

### 用 CDP 驱动私有桌面上的浏览器

窗口渲染出来了不等于能操作。要点击/输入就得开 CDP，两个坑：

1. **`--remote-debugging-port` 绑不上不报错**。端口被占时 Chrome 照常启动、窗口照常出现，但 CDP 根本没绑上，`/json` 返回的是**别的程序**（Electron 客户端、TradingView、别的 Chrome 实例）。
   必须核对：`curl -s 127.0.0.1:<端口>/json/version` 的 `Browser` 字段和 `User-Agent` 是不是自己的浏览器。
   选端口前先 `netstat -ano | grep -c ":<端口> "`，非 0 就换。
2. **视口坐标 ≠ 窗口坐标**。CDP 给的是视口坐标，`PrintWindow` 截的是整个窗口（含标签栏/工具栏）。换算：
   ```
   ox = (window.screenX - winRect.left) + (outerWidth  - innerWidth ) // 2
   oy = (window.screenY - winRect.top ) + (outerHeight - innerHeight)
   ```
   `outerHeight - innerHeight` 就是标题栏+标签栏+工具栏的高度；横向那个除法是两侧边框。
   别拍脑袋写常量，每次用 JS 读出来再算——窗口尺寸、缩放、边框一变常量就错。
3. **多标签页时必须显式指定目标页**。脚本按“第一个 page”或“含 chrome-extension 的 page”挑目标，多开一个标签就会永远盯着错的那个：表现为 `/describe` 返回上一个站点的 title、`fields` 为空，你怎么改选择器都没用。接口要带 `?url=<host 子串>` 这类 hint，并在没有匹配时**报错而不是回退到默认页**——静默回退会让你在错页面上调半天。
4. **改完服务代码重启后，先确认新代码真的在跑**。旧进程常常还占着端口，`taskkill` 掉的那个可能只是父进程：用 `netstat -ano | grep ":<端口> " | grep LISTENING` 拿真正在监听的 PID 再杀，重启后用一个只有新逻辑才会返回的结果去验证。否则你会在旧版本上反复验证，然后怀疑自己逻辑写错。
5. **点了没反应，先问“那个坐标上到底是谁”**。`document.elementFromPoint(x,y)` 返回 `null` = 元素在视口外或被遮挡，返回别的元素 = 坐标错位（页面重排过）。确认元素正确却不响应时，兜底用 `el.click()`——React 的 onClick 照样触发。
   实测两次都是这个模式：新版 GitHub 建仓按钮真实鼠标点三次无效、`elementFromPoint` 返回 `null`，改 `el.click()` 一次成功；邮件弹窗里 `.click()` 打到了子节点 `<div class="ui-btn-text">` 没反应，改点父容器 `.xmail-ui-btn` 才关掉。
   现代 SPA 站点的完整打法（选择器怎么挑、浮层怎么点、破坏性操作怎么验）：`references/modern-web-ui-driving.md`。

### 键盘必须发给顶层 page，不是 iframe target

扩展钱包这类 UI 跑在 OOPIF（`ses.html`）里，光是“找元素”要在 iframe target 上找，但**输入事件（鼠标和键盘）必须发到顶层 page target**：

- 发给 page target + 页面坐标 → Chrome 按几何路由到正确的 frame，鼠标能聚焦、`Input.insertText` 能落到像素坐标下的输入框
- 发给 iframe target → 鼠标坐标被当成 iframe 自己的视口坐标（差一个偏移量），键盘事件直接丢弃，`value.length` 永远是 0

实测：同一时刻，发给 iframe target 的 `insertText`/`dispatchKeyEvent(char)` 全部无效；改发给 page target，`insertText('a')` 立即让密码框长度变 1。

所以定位和输入分开：
1. 遍历所有 chrome-extension target，在各自的 DOM/shadow DOM 里找文本（得到 iframe 内坐标）
2. 从顶层 page 量 `iframe.getBoundingClientRect()`，相加得到页面坐标
3. 鼠标/键盘一律发给顶层 page

### 驱动浏览器时把光标画出来

用户看着你操作时，**必须让人看得见光标点在哪**。纯 CDP 驱动不会产生真实光标，帧里什么都没有，用户只能猜。

做法：推流服务暴露 `/cursor?x=&y=&click=1`，渲染帧时用 PIL 在图上画箭头 + 点击涟漪（0.7s 扩散消失，静止 2.5s 后淡出）。每次 `Input.dispatchMouseEvent` 前后同步调一次，坐标用上面换算出的窗口坐标。

顺手的效果：cursor 端点也是自检手段——涟漪落点偏了，说明坐标换算错了。参考实现 `scripts/desk_browser.py`。


## 首选驱动：按 ref 操作（Playwright MCP，不再算坐标）

手搓 CDP 的问题不是慢在协议上（单次动作 5~30ms），而是**慢在找元素**：每找一个按钮都要
试选择器、量 rect、算 iframe 偏移，一步一个来回，错了还要重来。

换成微软官方 `@playwright/mcp`：一次 `browser_snapshot` 返回整页无障碍树，每个可交互元素带
`[ref=e42]`，之后 `browser_click {target:"e42"}` 直接点——**不写选择器、不算坐标、iframe 内容
自动进树**（OKX 钱包那种 `ses.html` 也在里面）。

`scripts/browser_daemon.py` 把它包成常驻服务（ref 只在同一会话有效，所以必须常驻）：

```bash
python scripts/browser_daemon.py --cdp 18763 --port 8897     # 连私有桌面上的 Chrome
curl "http://127.0.0.1:8897/snap"                            # 整页快照 + 标签页列表
curl "http://127.0.0.1:8897/click?target=e42&element=搜索"
curl "http://127.0.0.1:8897/type?target=e12&text=hello"
curl "http://127.0.0.1:8897/tool?name=browser_tabs&args=%7B%22action%22%3A%22select%22%2C%22index%22%3A1%7D"
```

实测（GitHub 首页 / QQ 邮箱 / OKX 钱包）：

| 动作 | 耗时 |
|---|---|
| 快照整页（含 ref、含标签页） | 50~250ms |
| 按 ref 点击 | 433ms（含 250ms settle） |
| 按 ref 输入 | 41ms |
| 切标签页 | 11~22ms |
| 按 Esc | 26ms |
| 读 QQ 邮箱正文 | 68~84ms |

对比老做法：一次点击要「量 rect → 算偏移 → dispatch 三个鼠标事件 → 再截图确认」，3 个来回起步，
加上失败重试和 `sleep`，用户感知就是「识别半天」。

启动参数里两个关键项（`browser_daemon.py` 已内置）：
- `--snapshot-mode none`：动作后不再附带整页快照。GitHub 这种大页面这一项就省 2 秒（2349ms → 433ms）。
- `--timeout-settle 250`：动作后只等 250ms 安定，默认 500ms。

要什么状态就自己 `/snap` 一次（几十毫秒），别指望动作返回值里带快照。

**注意 ref 的生命周期**：ref 是「上一次快照」里的临时编号，页面一变就失效，报
`Ref e42 not found in the current page snapshot` 就重新 `/snap` 再点。

想让 Hermes 直接拥有这 25 个 `browser_*` 工具（不用经 daemon），让用户自己跑（agent 不能写 config）：

```bash
hermes mcp add playwright --command npx --args -y @playwright/mcp@latest --cdp-endpoint http://127.0.0.1:18763
```

### 踩过的坑（按 ref 操作时）

1. **ref 可能带 frame 前缀**：`[ref=e104]` 也可能写成 `[ref=f1e104]`（iframe 里的元素）。正则别只写 `e\d+`，用 `[\w]+`。
2. **`button:text-is("Create repository")` 这类严格文本选择器经常不匹配**（按钮里还有子元素/空格）。先 `/snap` 拿 ref 再点，比猜选择器稳。
3. **弹窗里的按钮必须用 Playwright 真实点击**。`eval` 里 `el.click()` 在 GitHub 的删除弹窗上**不会推进 React 状态**：按钮变灰、输入框不出现。用 `browser_click`。
4. **同名按钮有两个**：删除弹窗里外层入口和提交按钮都叫 `Delete this repository`。用 id 区分：`#repo-delete-proceed-button`、`#verification_field`。
5. **提交类按钮慢是正常的**：点击会等导航完成，2~5s。`browser_click` 默认 5s 超时，慢页面会报 `TimeoutError`——**但动作往往已经生效**，先查 URL/状态再决定要不要重试，别盲目重点。
6. **`#verification_field` 这类确认框如果 Playwright 报"does not match"，多半是元素存在但不可见**（弹窗还在动画/被遮）。先确认 `document.querySelector` 找得到、再看可见性；实在不行用原生 setter + `input` 事件绕过：`Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el, 值)` 再 `dispatchEvent(new Event('input',{bubbles:true}))`。

### 还留着的老脚本什么时候用

- `desk_stream.py`：要给人看画面（推流/截图）——Playwright 不管窗口和标签栏。
- `vault_broker.py`：密码不进模型的那条路。
- `wclick.py` / `qclick.py`：MCP 没起来、或页面是 canvas 无 DOM 时的兜底。
- `desk_chrome.py` / `desk_restore.py`：私有桌面的生命周期管理。

## 把私有桌面推给人看（实时画面进聊天）

三条硬规则，细节与全部坑在 `references/streaming-and-capture.md`：

1. **别用 `PrintWindow`**——私有桌面不被 DWM 合成，只能拿到上一次的旧帧，`SetForegroundWindow`+`DwmFlush` 也救不回来。用 CDP `Page.captureScreenshot`。
2. **`Target.activateTarget` 在隐藏桌面上是空操作**，`visibilityState` 不会变；要显示指定标签只能按 URL 点名截图（`/focus?url=...`）。
3. **前端用 canvas 轮询 `/snapshot?t=`，不要 `<img src=.../stream.mjpg>`**——长连接一断就回落背景色，用户看到一闪一闪的黑屏。

推流服务必须带 `--cdp <端口>` 才走 CDP 截图路径；不带就退回窗口截图，画面会卡旧帧。

## 往私有桌面 Chrome 里装扩展

这几步每步都能卡人，顺序不能错：

1. **品牌版 Chrome 137+ 已经删了 `--load-extension`**。加上 `--disable-features=DisableLoadExtensionCommandLineSwitch` 号称能恢复，但实测 Chrome 155 仍不加载（`chrome://extensions` 列表空）。不要在这条路上花时间。
2. **扩展文件在 `Default/Extensions/<id>/<ver>/` 不等于装好**。商店装的扩展注册信息在 **`Secure Preferences`** 的 `extensions.settings` 里，不在 `Preferences`（那里永远是 0 条）。看错文件会得出“没装”的错误结论。
3. **external 安装（`location: 3`）默认是 disabled**。此时 `chrome-extension://<id>/...` 一律 `ERR_BLOCKED_BY_CLIENT`，看着像“扩展不存在”，其实是开关没拨。
4. **启用就是点开关**，而 `chrome://extensions` 是普通页面，CDP 可以直接点：
   - 深递归 shadow DOM：`extensions-manager` → `extensions-item-list` → `extensions-item`，**只查一层找不到 item**，必须递归进每个 `shadowRoot`
   - 名字：`item.shadowRoot.querySelector('#name')`；开关：`#enableToggle`（读 `.checked` 验证结果）
   - 坐标 `getBoundingClientRect()` 是视口坐标，点之前按前面的公式换算成窗口坐标，并先调 `/cursor` 让用户看到
5. 验证到底了没有：`Target.createTarget` 打开 `chrome-extension://<id>/popup-init.html`，能渲染出钱包欢迎页才算成。

本机现成脚本：`scripts/ext_click.py`（传扩展名，自动找开关并点击）。

坑：`websockets.connect(..., max_size=2e7)` 是 float，会报 `parser failed / 'float' object cannot be interpreted as an integer`，必须写 `20000000`。

## 凭据代理（密码不进模型、注入不经过我）

`scripts/vault_broker.py` —— 本地服务（默认 `127.0.0.1:8899`），对齐 Hark Handoff 的“令牌化 + 最后一公里注入”：

1. 用户在自己的浏览器里打开 `http://127.0.0.1:8899/?origin=<页面origin>&label=<标签>` 掩码输入一次密码
2. 服务用 Windows DPAPI 加密落盘（`$HERMES_HOME/vault/broker.json`），只返回 `cred_xxx` handle
3. agent 调 `GET /inject?handle=...&cdp=<端口>`，服务自己校验页面 origin、自己找输入框、自己 `insertText`
   - `GET /inject_sel?handle=&cdp=&url=&id_sel=&pwd_sel=&submit_sel=`：**普通网页登录走这条**。按选择器实时定位 → 填 → 读回校验 → 通过才提交，一次调用走完，返回 `{ok, verified, submitted, id_match, id_len, pwd_len}`
   - `GET /inject_at?handle=&cdp=&url=&x=&y=&ix=&iy=`：**只在跨域同进程 iframe 里用**（选择器够不到时），坐标由 agent 现算
   - `GET /describe?cdp=<端口>&url=<host 子串>`：`url` 必须带，否则永远盯着第一个标签
   - `GET /list` / `GET /delete?handle=`：清理试错留下的废 handle
4. 值只在服务内存里活一次；agent 只拿到 `{ok, fields, kind, origin}`

实测三项：
- 落盘是 DPAPI blob（文件里搜不到明文）
- origin 不匹配直接拒：`origin 不匹配：页面 chrome-extension://… ≠ 凭据 https://example.com`
- 正确 origin 一次填两个密码框：`{"ok": true, "fields": 2}`，页面里两个框都变 14 字符

坑：

1. **iframe 名字要用路径最后一段**。目标 url 是 `.../ses.html?sestheme=light#/password-type?from=create`，`url.split('/')[-1].split('?')[0]` 会得到 `light#/password-type`，匹配不上任何 iframe，偏移归零 → 点到空白处。正确：`split('#')[0].split('?')[0].split('/')[-1]`。
2. **多栏同密表单只填空框**（钱包「密码 / 确认密码」那种），全都有内容时才回退到第一个；**但登录重试必须覆盖旧值**——见下条。
3. 注入时必须“先点击再 insertText”，只 insertText 不点击不会生效。
4. **坐标一律现算，绝不缓存。** 登录失败后页面多一条错误提示条，整张表单下移几十像素，缓存的 `(x,y)` 就落到上一个框上——账号和密码一起塞进第一个输入框，账号叠成 `邮箱邮箱`。每次都用 `querySelector` 取当前 `getBoundingClientRect()`，或直接按字段类型实时找。
5. **输入前先 Ctrl+A。** `Input.insertText` 是追加语义，框里有内容就会接在后面；全选再输才是替换。
6. **填完读回校验，不通过就不提交。** 账号比内容相等（`input.value === 账号`），密码比长度（`value.length === 密码长度`）。不通过就重新弹窗——错表浪费尝试额度，还可能触发风控。
7. **失败要自己重弹，不能干等。** 提交后每 0.4s 轮询页面（上限 8s），命中错误文案（`incorrect username or password` / `密码错误` / `登录失败` …）就重新弹窗；用户明确要求「输错了应该再弹窗重新输入，而不是不作为」。

整套闭环已经脚本化，别再手搓一遍：

```
python scripts/login_flow.py --cdp 18763 --url github.com --origin https://github.com     --fields "用户名或邮箱:text,密码:password"     --id-sel "#login_field" --pwd-sel "#password" --submit-sel "input[type=submit]"
```

它做四件事：弹窗取凭据 → `/inject_sel` 填+读回校验 → 提交 → 轮询判失败并重弹（默认 3 次）。
实测 GitHub：第一次密码错自动重弹，第二次 `{"verified": true, "id_match": true, "submitted": true}` 后进 `/`，页面出现 `Welcome to GitHub, niwnix!`。

边界：扩展/私有桌面这种非 http origin 只要求页面自己的 `location.origin` 匹配（靠 `chrome-extension://<id>` 本身）；助记词/私钥不要进这个库。

### 表单要跟着页面走（字段自适应）

固定写死“密码”一栏的表单，用户会立刻反问“为什么不是页面上那两个框”。做法：

- 服务加 `GET /describe?cdp=<端口>`：走同一套 iframe 定位逻辑，返回 `{origin, title, fields:[{type,label}]}`；label 优先 `aria-label` → `placeholder` → `name`，都空才上溯 4 层祖先取短文本（≤24 字）
- 表单加载时调它，**按返回的字段数渲染同样数量的掩码输入框**，标题用页面 title、每栏标签用页面自己的文案
- 客户端先校验（多栏必须完全一致 + 最短长度），过了才 `POST /save`；失败只改提示文字，不清已填内容

实测钱包页 `#/password-type` 返回：`[{"type":"password","label":"至少输入 8 个字符"},{"type":"password","label":"再次输入新密码"}]`，表单就长成“密码 / 确认密码”两栏——标签来自活页面，不是硬编码。

**致命坑：`file://` 页面不能 fetch `http://127.0.0.1`。** 把表单做成 `::preview{file=...}` 内嵌控件，打开后是空的（fetch 被 Chrome 直接拦），`/describe` 一次都不会被调用，看起来像“服务挂了”。必须由凭据代理自己 `GET /form` 以 http 吐出这个页面，再在预览面板开 `http://127.0.0.1:8899/form`。这条适用于**任何**要回连本机服务的控件。

`vault_broker.py` 运行时从**自己所在目录**读 `cred_form.html`，两个文件必须放在一起（`scripts/` 下都已带）。

## 需要用户亲自输入时，先选对界面

密码/OTP 一律不代打，只能让用户自己输，但**输在哪**会决定整件事的复杂度：

1. **站点自己有扫码登录时，先推扫码。** 零凭据、零插件、零键盘注入；把实时画面或截图给用户扫就行。只有站点不给扫码（或用户明确要账号密码）才走密码登录。
2. **用户必须亲手打字时，可见窗口 > 隐藏桌面。** 隐藏桌面的价值是隔离，不是可用性：它有原生键盘/焦点，而隐藏桌面上你只能靠合成输入，一旦窗口没有前台焦点就会静默丢字符。要隔离才用两张桌子（profile 独立），不要为了“看起来高级”把需要用户交互的流程塞进隐藏桌面。
3. **登录框可能在同进程的跨域 iframe 里**（QQ/老站点常见）。特征：`/json` 的目标列表里没有那个 frame，顶层 `document.querySelectorAll('input')` 为空，`/describe` 返回 `fields: []`。
   **能拿到，别放弃**：`Runtime.enable` 后收 `Runtime.executionContextCreated` 事件，按 `origin` 找到那个 frame 的 context（如 `https://xui.ptlogin2.qq.com`），在它的 context 里 `querySelector` 取 rect，再把每层 iframe 的 `getBoundingClientRect()` 偏移逐层相加。QQ 实测链：`mail.qq.com` 内 `graph.qq.com` @(650,173) → 其内 `xui.ptlogin2` @(5,0) → 文字 @(85.3,278.9) → 页面坐标 (740.3,451.9)，一次命中；按截图估的 (740,441) 差 11px 就没点中。现成实现 `scripts/qclick.py`。
   有扫码入口时仍优先扫码（零凭据）；只有必须账号密码、且用户明确要你点时走这条路。
4. 弹窗形态的输入界面（无标题栏小卡片、按页面字段自适应）的完整做法：`references/popup-dialog-ui.md`。

## 不用截图的控制方式

| 层 | 怎么控 | 看什么 | 实时性 |
|---|---|---|---|
| AX 无障碍树 | `Accessibility.getFullAXTree` | role/name/state，LLM 直接读 | 拉取即快照，配合事件 |
| 结构化快照 | `DOMSnapshot.captureSnapshot` | 节点 + 文本 + 布局矩形 | 同上 |
| DOM / JS | `Runtime.evaluate` / `DOM.getDocument` | 任意状态 | 同上 |
| Win32 消息 | `WM_SETTEXT` / `WM_GETTEXT` / `PostMessage` | 读回值 | 同步 |
| 渲染帧（推） | `Page.startScreencast` | JPEG 帧，**变化才推** | 实测 143 ms/帧 |
| 像素轮询（回退） | `PrintWindow` / `capture(mode='som')` | 截图 | 350 ms 级 |

**理解页面一律先走 AX/DOM，不要靠截图**。Playwright MCP 的做法就是这个：accessibility snapshot + `ref`，官方文档明写截图更差（token 高、座标靠猜、需要视觉模型、布局一变就错）。截图只用于“给人看”。

实时帧用 `Page.startScreencast`（事件驱动，渲染进程主动推），不要用定时 `PrintWindow`：实测 B 站首页 3 秒 21 帧（143 ms/帧），静态页 3 秒只给 1 帧——这就是正确行为（没变化不发）。每帧必须回 `Page.screencastFrameAck`，否则不再推。
限制：screencast 只覆盖**页面视口**，不含标签栏/工具栏；那部分要 UIA（`pywinauto` / `uiautomation`）或 `PrintWindow`。

优先消息/无障碍树：快、不看分辨率、不会被最小化坑。只有前三种拿不到时才用像素。

## 其他路线（按需）

| 需求 | 用什么 |
|---|---|
| 原生应用 / 安装向导 / 任意窗口 | `computer_use`（已装） |
| 可见的浏览器窗口 + 平滑鼠标轨迹 | Playwright headed（`headless=False` + `mouse.move(steps=N)`），需自行装 |
| 接管你正在用的 Chrome | `/browser connect` + `--remote-debugging-port` |
| 独立 Linux 桌面流进 Hermes Desktop | Bot Screen（仅 Linux，Windows 不可用） |
