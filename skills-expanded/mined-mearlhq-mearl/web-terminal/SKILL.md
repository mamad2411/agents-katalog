---
name: web-terminal
description: 使用 mearl terminal 操作已打开的 xterm.js 和 Ghostty Web 终端。发现标签页和 iframe 中的面板，读取滚屏或视口，发送文本和按键，等待提示符，并在支持的终端获取命令输出和退出码。
install:
  description: 注册 Web 终端 CLI 插件
  command: npx @mearl/setup plugin "$SKILL_DIR"
version: "3.1.0"
---

# Web 终端

使用 Mearl 已连接的浏览器和已打开的终端。用 list 检查一个文档，或用 discover 查找标签页及可访问的 HTTP(S) iframe。读写沿用 tabId 和 frameId。多面板时给 read、wait、send、key 或 exec 传入 --paneId=ID，或使用 --selector='#容器ID'。paneId 对应当前页面中的实际面板，隐藏的面板需要先切到前台，重载或重建后重新 list。写操作使用终端所在文档的完整 URL。discover 的 unavailable 字段列出无法检查的 frame。

```bash
npx @mearl/setup plugin /absolute/path/to/skills/web-terminal
mearl terminal list 12345
mearl terminal discover 12345
mearl terminal read 12345 80
mearl terminal wait 12345 'Ready' --waitMs=5000
mearl terminal screen 12345 terminal.png --selector='#terminal'
mearl terminal send 12345 'https://example.com/terminal/' 'printf hello'
mearl terminal key 12345 'https://example.com/terminal/' Enter
mearl terminal exec 12345 'https://example.com/terminal/' 'printf "%s\n" hello'
```

| 页面 | 读取 | 输入 | 命令结果 |
| --- | --- | --- | --- |
| ttyd 及公开 xterm.js 实例的应用 | 滚屏、活动缓冲区、软换行合并 | 文本、原始终端序列、控制键 | 缓冲区及控制序列，capture 为 buffer |
| 使用 DOM 渲染或提供无障碍文本的 xterm.js 页面 | 当前视口 | 粘贴文本和独立控制键 | 屏幕标记，capture 为 screen |
| GoTTY 默认 WebGL 或其他使用 xterm.js 选区机制的页面 | 通过选区读取当前视口 | 页面接受合成粘贴和按键时可用 | 屏幕标记，capture 为 screen |
| JupyterLab Terminal、code-server 集成终端 | 当前视口 | 粘贴文本和按键 | 屏幕标记，capture 为 screen |
| 公开实例的 Ghostty Web | 滚屏和当前视口 | 文本和按键 | 从滚屏读取屏幕标记，capture 为 screen |
| Ghostty Web 官方示例等封装实例的页面 | screen 截图 | 粘贴文本和按键 | 通过截图核对 |
| 无法提供文本的终端 | screen 截图 | 取决于页面控件 | 按屏幕核对 |

自有应用可以把已打开的 xterm.js 或 Ghostty Web 实例放在 window.mearlTerminals 对象中，支持多个实例。插件也识别 window.term 和 window.terminal。list 和 discover 里的 engine 字段表示检测到的模拟器。

## 读取和交互

- read 默认读取最近 40 行，最多 200 行。--view=viewport 只取当前视口。source 为 buffer 时，buffer 字段区分 normal 和 alternate。viewport 表示来自 DOM 或无障碍文本，selection 表示来自 xterm.js 的临时选区。
- selection 使用页面内的复制事件取文本，并清理临时选区。存在用户选区、正在输入法组字或 TUI 开启鼠标事件时，使用 screen 截图。Linux 的 xterm.js 可能更新中键粘贴选区。
- wait 只在当前终端视口里匹配指定的字面文本，可用于等待提示符或 TUI 状态。默认 10 秒，可用 --waitMs 调整。
- screen 将 PNG 保存到插件执行宿主的指定路径。可用顶层 CSS 选择器裁切终端容器或 iframe。
- send 输入文本。实例公开时按原始终端序列发送，通过页面输入时使用粘贴。可以用 JSON payload 传 \r（Enter），或者使用 key 单独发送 Enter、Escape、方向键、Tab、Backspace、Home、End、PageUp、PageDown、Delete、Shift+Tab、F1 到 F12 和 Ctrl+A 到 Ctrl+Z。dispatched 表示输入已交给页面。用 read 确认后端响应。
- key 也接受单个 ASCII 字符和最多 32 个按键。Vim 等 TUI 可以用 key 发送按键序列，例如 Escape : q '!' Enter。支持粘贴的终端可能把 send 当作括号粘贴。
- Ghostty Web 页面未公开终端实例时，粘贴文本用 send。该页面的 Ctrl+V 交由浏览器处理。
- 执行输入前查看提示符和交互状态。页面只读、断开连接或正在等待不同的输入时，先恢复该会话。

## 执行脚本

exec 用于停在交互式 shell 提示符的会话。默认 --shell=posix，PowerShell 会话传 --shell=powershell。多行脚本在继承当前工作目录和导出环境的子进程中运行。持续交互使用 send 和 key。

exec 返回 executionId、status，以及完成后的 exitCode、text 和 truncated。text 是终端呈现的合并输出，包括标准错误。默认最多 200 行，可用 --lines=NUM 调整到最多 2000 行，另有 65536 字符上限。屏幕标记模式会在终端显示本次命令的起止标记。有公开缓冲区时会从近期滚屏中查找标记，其余终端读取当前视口。采集范围内缺少起始标记，或输出超出行数或字符上限时，结果标为 truncated。非零退出码仍返回完整 JSON，Mearl CLI 退出码为 1。

exec 默认自动选择采集方式。tmux 等中间层过滤控制序列时，可在 shell 提示符使用 --capture=screen，通过可见的起止标记确认结果。

默认等待 10 秒。使用 --waitMs=0 立即返回 executionId，或者增加 waitMs 并给 Mearl 的 --timeout 留出更长时间。status 可查看当前输出，follow --verbose 在 stderr 显示新增内容或重绘，最终结果仍从 stdout 返回 JSON。只支持视口读取的终端在跟踪期间保持滚动位置在底部。分屏很窄时可加宽面板，让完成标记保留在同一行。

每个面板同时跟踪一个 exec，最多 10 分钟。记录保存在当前页面文档，刷新、重新连接或中间层过滤控制序列时，可能无法取回退出码。用 key 发送 Ctrl+C 时，记录返回 interrupt-sent，再用 read 核对终端状态。

~~~bash
mearl terminal exec 12345 'https://example.com/terminal/' 'sleep 2; printf done' --waitMs=0
mearl terminal status 12345 EXECUTION_ID
mearl terminal follow 12345 EXECUTION_ID --waitMs=20000 --timeout 30 --verbose
~~~

## 云终端和文件传输

从站点自己的入口打开会话，再用 discover 检查页面暴露的终端。登录、授权、连接恢复和上传下载由站点提供。已有文件控件时，用 Mearl 的 page_upload 上传，或用 page_download 监听并保存下载结果。
