---
name: claude-notify

description: >
  Desktop notifications for Claude Code.
  Support Windows Toast and macOS Notification Center.
  Popup notification when Claude Code finishes tasks
  or requires user input.

metadata:
  author: qyzxcswbll
  version: "2.0.2"

  tags:
    - claude
    - claude-code
    - notification
    - notify
    - toast
    - popup
    - desktop
    - windows
    - macos
    - hooks
---

# Claude Code Notify Setup

## 概述

安装后在 Claude Code 中执行（二选一）：

- **CLI 版**（终端）：输入 `/notify-setup`
- **VSCode 版**（聊天框）：用户说 **「配置桌面通知」**

自动完成以下配置：

- 任务完成时弹出通知，显示你最后一条输入
- 需要你回应时弹出通知

支持 Windows 10/11 Toast 通知和 macOS 通知中心。零额外依赖。

## 执行步骤

### 1. 检测操作系统

判断当前操作系统。仅支持 Windows 和 macOS，Linux 不支持则提示退出。

### 2. 创建通知脚本

#### Windows

写入 `~/.claude/notify.ps1`（必须 `.ps1` 扩展名，PowerShell 需要）。

**编码要求**：先写 UTF-8 内容，然后执行 `[System.IO.File]::WriteAllText(path, content, [System.Text.Encoding]::UTF8)` 方法写入文件以保证 UTF-8 BOM。不使用 `Out-File` 或 `Set-Content`（它们默认用 UTF-16 或无 BOM）。

```powershell
param([string]$Event = 'stop')

# 开关检测——存在 ~/.claude/.notifymute 文件就不弹窗
if (Test-Path (Join-Path $env:USERPROFILE '.claude\.notifymute')) { exit 0 }

# 从 stdin 原始文本中提取 transcript_path
$transcriptPath = ""
try {
    if ([Console]::IsInputRedirected) {
        $raw = [Console]::In.ReadToEnd()
        if ($raw -match '"transcript_path"\s*:\s*"([^"]+)"') {
            $transcriptPath = $matches[1] -replace '\\\\', '\'
        }
    }
} catch {}

$projectName = ""
$sessionName = ""
$context = ""

if ($transcriptPath -and (Test-Path $transcriptPath)) {
    try {
        $headLines = Get-Content $transcriptPath -Encoding UTF8 -TotalCount 20
        foreach ($line in $headLines) {
            if (-not $projectName -and ($line -match '"cwd"\s*:\s*"([^"]+)"')) {
                $cwd = $matches[1] -replace '\\\\', '\'
                $projectName = Split-Path $cwd -Leaf
            }
            if (-not $sessionName -and ($line -match '"role"\s*:\s*"user"')) {
                try {
                    $msg = $line | ConvertFrom-Json
                    $content = $msg.message.content
                    if ($content -is [array]) { $content = ($content | Where-Object { $_.type -eq "text" } | Select-Object -First 1).text }
                    if ($content) {
                        $sessionName = ($content -replace "`n", " ").Trim()
                        if ($sessionName.Length -gt 5) { $sessionName = $sessionName.Substring(0, 5) }
                    }
                } catch {}
            }
            if ($projectName -and $sessionName) { break }
        }
    } catch {}

    try {
        # 从 transcript 尾部提取最后一条用户消息（跳过 tool_result 找有文字的那条）
        $tailLines = Get-Content $transcriptPath -Encoding UTF8 -Tail 100
        for ($i = $tailLines.Length - 1; $i -ge 0; $i--) {
            if ($tailLines[$i] -match '"role"\s*:\s*"user"') {
                try {
                    $msg = $tailLines[$i] | ConvertFrom-Json
                    $content = $msg.message.content
                    if ($content -is [array]) {
                        $content = ($content | Where-Object { $_.type -eq "text" } | Select-Object -First 1).text
                    }
                    if ($content) {
                        $context = ($content -replace "`n", " ").Trim()
                        if ($context.Length -gt 60) { $context = $context.Substring(0, 57) + "..." }
                        break
                    }
                } catch {}
            }
        }
    } catch {}
}

# 模式检测——优雅弹窗分流
$notifyModePath = Join-Path $env:USERPROFILE '.claude\notify-mode'
if (Test-Path $notifyModePath) {
    $mode = (Get-Content $notifyModePath -Encoding UTF8).Trim().ToLower()
    if ($mode -eq "elegant") {
        $elegantScript = Join-Path $env:USERPROFILE '.claude\notify-elegant.ps1'
        if (Test-Path $elegantScript) {
            & $elegantScript -Event $Event -ProjectName $projectName -SessionName $sessionName -Context $context
            exit 0
        }
    }
}

# XML 转义函数（防止用户输入含 <>& 导致 Toast 崩溃）
function Escape-Xml([string]$text) {
    if (-not $text) { return "" }
    return [System.Security.SecurityElement]::Escape($text)
}

# 标题：项目名（第一行）
$title = Escape-Xml $(if ($projectName) { $projectName } else { "Claude Code" })

# 副标题：会话名（第二行，带图标）
$subtitle = Escape-Xml $(if ($sessionName) { "⚙ $sessionName" } else { "" })

# 内容：第三行
$isStop = ($Event -eq 'stop')
if ($isStop) {
    $body = Escape-Xml $(if ($context) { "✨ 搞定了: $context" } else { "✨ 搞定了~" })
} else {
    $body = Escape-Xml $(if ($context) { "💬 需要你瞅一眼: $context" } else { "💬 需要你瞅一眼" })
}

# Windows Toast
try {
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
    $null = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    if ($subtitle) {
        $toastXml = "<?xml version=""1.0"" encoding=""utf-8""?><toast><visual><binding template=""ToastText04""><text id=""1"">$title</text><text id=""2"">$subtitle</text><text id=""3"">$body</text></binding></visual></toast>"
    } else {
        $toastXml = "<?xml version=""1.0"" encoding=""utf-8""?><toast><visual><binding template=""ToastText02""><text id=""1"">$title</text><text id=""2"">$body</text></binding></visual></toast>"
    }
    $xml.LoadXml($toastXml)
    $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code").Show($toast)
} catch {
    # 静默失败，绝不阻塞
}
exit 0
```

#### macOS

写入 `~/.claude/notify`（无扩展名）。

```bash
#!/bin/bash
EVENT=${1:-stop}

# 开关检测——存在 ~/.claude/.notifymute 文件就不弹窗
if [ -f "$HOME/.claude/.notifymute" ]; then exit 0; fi

INPUT=$(cat)

TRANSCRIPT_PATH=$(echo "$INPUT" | grep -o '"transcript_path" *: *"[^"]*"' | sed 's/"transcript_path" *: *"\(.*\)"$/\1/' | sed 's/\\\\/\//g')

PROJECT_NAME=""
SESSION_NAME=""
CONTEXT=""

# python3 检测——不存在则跳过上下文解析，直接发基础通知
if command -v python3 &> /dev/null && [ -n "$TRANSCRIPT_PATH" ] && [ -f "$TRANSCRIPT_PATH" ]; then
    # 从 transcript 头部提取项目名和会话名（前 5 字）
    META=$(python3 -c "
import json, sys
path = '$TRANSCRIPT_PATH'
project = ''
session = ''
with open(path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 20:
            break
        try:
            msg = json.loads(line)
            msg_content = msg.get('message', {}) if isinstance(msg, dict) else {}
            if not project and msg.get('cwd'):
                cwd = msg.get('cwd')
                project = cwd.rstrip('\\\\').split('\\\\')[-1]
            if not session and msg_content.get('role') == 'user':
                content = msg_content.get('content', '')
                if isinstance(content, list):
                    texts = [c['text'] for c in content if c.get('type') == 'text']
                    content = texts[0] if texts else ''
                session = content.replace(chr(10), ' ').replace(chr(13), '').strip()[:5]
        except:
            pass
        if project and session:
            break
print(json.dumps({'project': project, 'session': session}))
" 2>/dev/null)

    PROJECT_NAME=$(echo "$META" | python3 -c "import sys,json; print(json.load(sys.stdin).get('project',''))" 2>/dev/null)
    SESSION_NAME=$(echo "$META" | python3 -c "import sys,json; print(json.load(sys.stdin).get('session',''))" 2>/dev/null)

    # 从 transcript 尾部提取最后一条用户消息
    CONTEXT=$(python3 -c "
import json, sys
path = '$TRANSCRIPT_PATH'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in reversed(lines[-100:]):
        try:
            msg = json.loads(line)
            if msg.get('message', {}).get('role') != 'user':
                continue
            content = msg['message'].get('content', '')
            if isinstance(content, list):
                texts = [c['text'] for c in content if c.get('type') == 'text']
                content = texts[0] if texts else ''
            content = content.replace(chr(10), ' ').replace(chr(13), '').strip()
            if len(content) > 60:
                content = content[:57] + '...'
            print(content, end='')
            break
        except:
            pass
" 2>/dev/null)
fi

# 标题与内容组装
if [ -n "$PROJECT_NAME" ]; then TITLE="$PROJECT_NAME"; else TITLE="Claude Code"; fi
if [ -n "$SESSION_NAME" ]; then TITLE="$TITLE ⚙ $SESSION_NAME"; fi

if [ "$EVENT" = "stop" ]; then
    [ -n "$CONTEXT" ] && BODY="✨ 搞定了: $CONTEXT" || BODY="✨ 搞定了~"
else
    [ -n "$CONTEXT" ] && BODY="💬 需要你瞅一眼: $CONTEXT" || BODY="💬 需要你瞅一眼"
fi

# 使用环境变量传递给 osascript，彻底杜绝转义问题
export CLAUDE_NOTIFY_TITLE="$TITLE"
export CLAUDE_NOTIFY_BODY="$BODY"
osascript -e 'display notification (system attribute "CLAUDE_NOTIFY_BODY") with title (system attribute "CLAUDE_NOTIFY_TITLE")' 2>/dev/null
```

写完后执行 `chmod +x ~/.claude/notify`。

#### Windows 开关脚本

写入 `~/.claude/notify-toggle.ps1`（UTF-8 BOM 编码，同 notify.ps1）：

```powershell
# notify-toggle.ps1 — 双击运行，一键开关 Claude Code 通知
$flagPath = Join-Path $env:USERPROFILE '.claude\.notifymute'
if (Test-Path $flagPath) {
    Remove-Item $flagPath -Force
    $body = "通知已开启 🔔"
} else {
    New-Item $flagPath -ItemType File -Force | Out-Null
    $body = "通知已关闭 🔕"
}

# XML 转义函数
function Escape-Xml([string]$text) {
    if (-not $text) { return "" }
    return [System.Security.SecurityElement]::Escape($text)
}

$bodyEscaped = Escape-Xml $body

try {
    Add-Type -AssemblyName System.Runtime.WindowsRuntime
    $null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
    $null = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $toastXml = "<?xml version=""1.0"" encoding=""utf-8""?><toast><visual><binding template=""ToastText02""><text id=""1"">Claude Code 通知</text><text id=""2"">$bodyEscaped</text></binding></visual></toast>"
    $xml.LoadXml($toastXml)
    $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code").Show($toast)
} catch {
    # 静默失败，不弹窗也不阻塞
}
```

写入 `~/.claude/notify-toggle.bat`（纯 ASCII）：

```batch
@echo off
powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\.claude\notify-toggle.ps1"
```

#### macOS 开关脚本

写入 `~/.claude/notify-toggle.sh`，执行 `chmod +x ~/.claude/notify-toggle.sh`：

```bash
#!/bin/bash
FLAG="$HOME/.claude/.notifymute"
if [ -f "$FLAG" ]; then
    rm "$FLAG"
    BODY="通知已开启 🔔"
else
    touch "$FLAG"
    BODY="通知已关闭 🔕"
fi

# 使用环境变量传递，杜绝转义问题
export CLAUDE_TOGGLE_BODY="$BODY"
osascript -e 'display notification (system attribute "CLAUDE_TOGGLE_BODY") with title "Claude Code 通知"'
```

### 3. 配置 hooks

读取 `~/.claude/settings.json`。

- 如果文件不存在则创建设置文件
- 如果已存在 `hooks` 字段，合并 `Stop` 和 `Notification` 事件（保留已有配置）
- 如果没有 `hooks` 字段则添加

Windows hooks 配置（AI 安装时用 `$env:USERPROFILE` 展开为绝对路径后写入）：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell -ExecutionPolicy Bypass -File \"<USERPROFILE>\\.claude\\notify.ps1\" -Event stop",
            "timeout": 15
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "powershell -ExecutionPolicy Bypass -File \"<USERPROFILE>\\.claude\\notify.ps1\" -Event notification",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

macOS hooks 配置：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/notify stop",
            "timeout": 15
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/notify notification",
            "timeout": 15
          }
        ]
      }
    ]
  }
}
```

### 4. 验证

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File "$env:USERPROFILE\.claude\notify.ps1" -Event stop
```

macOS：

```bash
echo '{}' | bash ~/.claude/notify stop
```

无报错即成功。告知用户配置完成，之后每次 Claude 完成任务或需要回应时都会弹出通知。

### 5. 开关通知（可选）

临时不需要通知时，双击运行一次开关脚本，通知就会关闭。再运行一次，重新开启。

**Windows：** 双击 `%USERPROFILE%\.claude\notify-toggle.bat`，或 Win+R 运行：
```
%USERPROFILE%\.claude\notify-toggle.bat
```

**macOS：** 双击 `~/.claude/notify-toggle.sh`，或终端执行：
```bash
bash ~/.claude/notify-toggle.sh
```

## V2 优雅弹窗

### 模式切换（用户会说）
- **切换优雅弹窗** / **打开定制弹窗** — 切换为优雅弹窗模式
- **切回系统通知** — 切换为系统 Toast 模式

### 安装优雅弹窗脚本

AI 必须严格按以下步骤执行：

1. **读取并写入优雅弹窗脚本**：使用 `Read` 工具读取当前项目下的 `hooks/notify-elegant.ps1` 文件内容，然后使用 `Write` 工具将其完整写入到 `~/.claude/notify-elegant.ps1`（必须确保使用 UTF-8 BOM 编码）。
2. **读取并写入配置服务脚本**：使用 `Read` 工具读取当前项目下的 `hooks/notify-config-server.py` 文件内容，然后使用 `Write` 工具将其完整写入到 `~/.claude/notify-config-server.py`。
3. **创建主题目录**：执行 `mkdir -p ~/.claude/themes` 创建目录（如果不存在）。

### 启动配置服务
用户说「定制弹窗」时，AI 执行以下逻辑：

1. **检测服务是否已运行**：执行 `python3 -c "import socket; s=socket.socket(); s.settimeout(2); print(0 if s.connect_ex(('localhost',18765))==0 else 1)"`。如果返回 0 表示服务已在运行，跳过启动步骤。
2. **如果服务未运行**：执行 `python3 ~/.claude/notify-config-server.py &` 在后台启动配置服务。
3. **打开浏览器**：在浏览器打开 `docs/design-v2-preview.html`。
4. 告知用户在网页上选择主题、图标、上传立绘后点保存。

### 注意事项
- 模式标记存储在 `~/.claude/notify-mode`（内容为 `raw` 或 `elegant`）
- 配置存储在 `~/.claude/notify-config.json`
- 立绘图片存储在 `~/.claude/themes/character.png`
- 配置服务需要 Python 3，端口 18765

## 注意事项（给 AI 自己看）

- 通知脚本文件创建后不要删，hooks 事件会一直调用它
- Windows 脚本必须 UTF-8 BOM 编码，否则 PowerShell 5.1 解析带中文的脚本会报 `MissingEndCurlyBrace` 错误
- macOS 脚本无需 BOM，普通 UTF-8 即可
- `[Console]::In.ReadToEnd()` 只能消费 stdin 一次，重复调用返回空
- Stop 事件的 stdin 中不含 `transcript_messages` 字段，需通过 `transcript_path` 读 JSONL 文件提取用户消息
- **macOS 通知**：已使用环境变量传参，不再需要手动转义双引号
- **Windows hooks 命令路径必须用绝对路径**（`C:\Users\xxx\.claude\notify.ps1`），`%USERPROFILE%` 在 VSCode Claude Code hook 环境中不会被展开。安装时用 `$env:USERPROFILE` 展开后写入 JSON
- **修改 settings.json 时，必须使用 Node.js 或 Python 脚本进行安全的 JSON 解析和合并**，绝对不允许使用正则表达式或字符串替换，以免破坏用户原有的配置结构
- **Windows 执行策略**：如果用户提示「无法加载文件，因为在此系统上禁止运行脚本」，请在管理员 PowerShell 中执行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`，Hook 命令中已内置 `-ExecutionPolicy Bypass` 参数绕过