---
name: terminal
description: 双向交互终端会话工具，用于串口终端、SSH 交互 Shell、本地 Shell、设备控制台、AT/CLI 菜单、需要保持上下文的交互式调试；当用户提到交互终端、串口终端、SSH 终端、打开 shell、发送命令后继续读输出、保持会话、登录后操作、菜单式命令行时触发，也兼容 /terminal 显式调用。
---

# Terminal — 双向交互终端会话

统一封装串口、SSH 和本地 Shell 的双向交互会话。它补齐 `serial` 的“监控/发送是分离命令”和 `ssh` 的“远程命令多为一次性执行”之间的空白：当目标需要保持登录状态、菜单状态、REPL 状态或设备 CLI 上下文时，使用本 skill。

## 定位

- `serial`：扫描、监控、单次发送、日志、Hex 查看。
- `ssh`：OpenSSH 配置、远程命令、传输、隧道。
- `terminal`：保持一个可持续读写的交互式会话，并通过 `send/read` 驱动下一步判断。

## 配置

### 环境级配置 (`config.json`)

terminal skill 的环境级配置目前为空对象 `{}`。交互终端的关键参数通常和具体会话绑定，优先通过 `start` 命令显式传入，避免误连设备或误用凭据。

### 会话状态 (`.embeddedskills/state.json`)

后台会话运行时状态保存到工作区的 `.embeddedskills/state.json`，使用 `terminal_sessions` 字段记录会话名、后端、PID、TCP 控制端口和日志路径。

### 参数优先级

1. **CLI 参数** (`--port`, `--baudrate`, `--host`, `--name` 等) - 最高优先级
2. **会话状态** (`.embeddedskills/state.json` 中已启动的 `terminal_sessions`)
3. **默认值** - 最低优先级

## 子命令

| 子命令 | 用途 | 风险 |
|--------|------|------|
| `start` | 启动一个后台交互会话 | 中 |
| `list` | 列出现有会话 | 低 |
| `status` | 查询单个会话状态 | 低 |
| `send` | 向会话写入文本或 Hex 数据 | 中 |
| `read` | 读取并清空会话输出缓冲 | 低 |
| `attach` | 前台行模式接入会话 | 中 |
| `stop` | 停止会话并清理状态 | 中 |

## 后端

| 后端 | 适用场景 | 依赖 |
|------|----------|------|
| `serial` | MCU UART 控制台、AT 命令、Bootloader 菜单、板卡 CLI | `pyserial` |
| `ssh` | Linux 开发板交互 Shell、登录后持续操作 | OpenSSH 客户端 |
| `local` | 本机临时 Shell、REPL、CLI 程序交互 | Python 标准库 |

## 脚本调用

所有脚本位于 skill 目录的 `scripts/` 下，通过 `python` 直接调用。命令示例均以当前 skill 目录为基准。

```bash
# 启动串口终端
python scripts/terminal_session.py start serial --port COM11 --baudrate 115200 --name board

# 启动 SSH 终端，host 使用 ~/.ssh/config 中的 Host 别名
python scripts/terminal_session.py start ssh --host 1380-P904 --name devboard

# 启动本地 Shell
python scripts/terminal_session.py start local --name local-shell

# 发送一行命令并追加 CRLF
python scripts/terminal_session.py send board "help" --crlf

# 读取输出，最多等待 1 秒
python scripts/terminal_session.py read board --timeout 1

# 前台行模式接入
python scripts/terminal_session.py attach board

# 查询与停止
python scripts/terminal_session.py list
python scripts/terminal_session.py status board
python scripts/terminal_session.py stop board
```

## 会话状态详情

会话元数据保存到工作区：

```text
.embeddedskills/state.json
```

使用 `terminal_sessions` 字段记录：

```json
{
  "terminal_sessions": {
    "board": {
      "backend": "serial",
      "tcp_port": 23145,
      "pid": 1234,
      "started_at": "2026-05-26T10:00:00+08:00"
    }
  }
}
```

后台进程日志保存到：

```text
.embeddedskills/logs/terminal/
```

## 输出格式

脚本默认输出 JSON：

```json
{
  "status": "ok",
  "action": "read",
  "summary": "读取 42 字节",
  "details": {
    "session": "board",
    "text": "help\r\n..."
  }
}
```

错误输出：

```json
{
  "status": "error",
  "action": "send",
  "error": {
    "code": "session_unreachable",
    "message": "会话不可达，可能已退出"
  }
}
```

## 操作流程

1. 判断是否真的需要保持交互状态；若只是一次性远程命令，优先使用 `ssh`；若只是串口抓日志，优先使用 `serial`。
2. 选择后端：串口控制台用 `serial`，远程 shell 用 `ssh`，本机交互程序用 `local`。
3. `start` 后先 `read --timeout 1` 获取启动横幅、登录提示或 shell prompt。
4. 每次 `send` 后都用 `read --timeout <秒>` 观察反馈，再决定下一步。
5. 完成后执行 `stop`，避免后台进程长期占用串口、SSH 连接或本地 Shell。

## 核心规则

- 不自动猜测串口端口、波特率、SSH Host 或登录凭据。
- 未明确用途时不主动发送任何会改变设备状态的命令。
- 多个会话必须使用不同 `--name`，避免输出混淆。
- `read` 会清空当前输出缓冲；重要输出需要及时记录到最终回复。
- `attach` 是行模式，不等同于完整 TTY/raw 模式；需要全屏程序、vim、top、交互式密码输入时，优先让用户使用真实终端工具。
- 串口会话会独占真实串口；如果需要和外部串口工具共享端口，先使用 `serial` skill 的 mux 能力。
- SSH 后端使用 `~/.ssh/config` 的 Host 别名；配置主机、跳板机、传输文件仍交给 `ssh` skill。
- 失败时保留真实错误：端口占用、缺少 `pyserial`、`ssh` 不存在、Host 别名无法解析、进程已退出等都不要吞掉。
