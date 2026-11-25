---
name: himalaya
description: "Himalaya CLI: IMAP/SMTP email from terminal."
version: 1.1.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Communication]
    homepage: https://github.com/pimalaya/himalaya
prerequisites:
  commands: [himalaya]
---

# Himalaya 邮件 CLI

Himalaya 是一款命令行邮件客户端，允许您通过 IMAP、SMTP、Notmuch 或 Sendmail 后端在终端中管理邮件。

该功能与 Hermes 邮件网关适配器是相互独立的。网关适配器用于让用户向智能体发送邮件，且使用 Hermes 内置的 IMAP/SMTP 适配器；而此功能则让智能体能够通过终端工具操作邮箱，因此需要外部安装 `himalaya` CLI。

## 参考资料

- `references/configuration.md`（配置文件设置及 IMAP/SMTP 认证）
- `references/message-composition.md`（用于编写邮件的 MML 语法）

## 先决条件

1. 已安装 Himalaya CLI（可通过 `himalaya --version` 进行验证）
2. 在 `~/.config/himalaya/config.toml` 目录下存在配置文件
3. 已配置 IMAP/SMTP 凭据（密码将得到安全存储）

### 安装方法

```bash
# Pre-built binary (Linux/macOS — recommended)
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# macOS via Homebrew
brew install himalaya

# Or via cargo (any platform with Rust)
cargo install himalaya --locked
```

## 配置设置

运行交互式向导来创建账户：

```bash
himalaya account configure
```

或者手动创建 `~/.config/himalaya/config.toml` 文件：

```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"  # or use keyring

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"

# Folder aliases (himalaya v1.2.0+ syntax). Required whenever the
# server's folder names don't match himalaya's canonical names
# (inbox/sent/drafts/trash). Gmail is the common case — see
# `references/configuration.md` for the `[Gmail]/Sent Mail` mapping.
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "Sent"
folder.aliases.drafts = "Drafts"
folder.aliases.trash = "Trash"
```

> **关于别名语法的注意事项。** 在 1.2.0 版本之前的文档中使用了 `[accounts.NAME.folder.alias]` 这种子结构（其中 `alias` 为单数形式）。v1.2.0 版本会默默忽略这种格式——虽然 TOML 解析没有问题，但别名解析器根本不会读取它，因此所有查询都会直接转而使用标准名称。在 Gmail 环境下，这意味着在 SMTP 发送成功之后，保存到“已发送”文件夹的操作会失败，同时 `himalaya message send` 命令的返回码也会不为零。任何基于该错误码进行重试的调用方（无论是代理、脚本还是用户），都会重新执行整个发送流程——包括 SMTP 发送步骤——从而导致向收件人发送重复邮件。请始终使用 `folder.aliases.X` 这种格式（`alias` 为复数形式，采用点号分隔的键值结构，直接位于 `[accounts.NAME]` 下方）。

## Hermes 集成说明

- **读取、列出、搜索、移动、删除** 操作均可直接通过终端工具完成
- **撰写/回复/转发** 操作——为确保稳定性，建议使用管道输入方式（如 `cat << EOF | himalaya template send`）。交互式的 `$EDITOR` 模式可在设置 `pty=true` 并在后台运行进程工具的情况下使用，但前提是用户需熟悉所使用的编辑器及其命令
- 若需要结构化输出以便程序化解析，可使用 `--output json` 选项
- `himalaya account configure` 向导需要用户进行交互式输入——请使用 PTY 模式：`terminal(command="himalaya account configure", pty=true)`

## 常见操作

### 列出文件夹

```bash
himalaya folder list
```

### 列出邮件

列出收件箱中的邮件（默认）：

```bash
himalaya envelope list
```

列出特定文件夹中的邮件：

```bash
himalaya envelope list --folder "Sent"
```

带分页功能的列表：

```bash
himalaya envelope list --page 1 --page-size 20
```

### 搜索邮件

```bash
himalaya envelope list from john@example.com subject meeting
```

### 阅读邮件

通过邮件编号读取邮件（显示纯文本格式）：

```bash
himalaya message read 42
```

导出原始 MIME 数据：

```bash
himalaya message export 42 --full
```

### 回复邮件

若要通过 Hermes 以非交互方式回复邮件，需先读取原始邮件内容，撰写回复内容，然后再将其传递出去：

```bash
# Get the reply template, edit it, and send
himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send
```

或者手动构建回复：

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: sender@example.com
Subject: Re: Original Subject
In-Reply-To: <original-message-id>

Your reply here.
EOF
```

全组回复（交互式——需要使用 $EDITOR，建议采用上述模板方式）：

```bash
himalaya message reply 42 --all
```

### 转发邮件

```bash
# Get forward template and pipe with modifications
himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send
```

### 编写新邮件

**非交互模式（适用于 Hermes）**——通过标准输入管道传输消息：

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

或者使用 headers 标志：

```bash
himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"
```

注意：若不使用管道输入命令 `himalaya message write`，则会打开 `$EDITOR` 编辑器。虽然在开启 `pty=true` 且处于后台模式时该方式也能使用，但通过管道传输数据更为简单且可靠。

### 移动/复制邮件

将邮件移动到指定文件夹（格式为：目标文件夹路径，后跟邮件编号）：

```bash
himalaya message move "Archive" 42
```

复制到文件夹（先输入目标文件夹路径，再输入消息编号）：

```bash
himalaya message copy "Important" 42
```

### 删除邮件

```bash
himalaya message delete 42
```

### 管理标志位

添加标志位：

```bash
himalaya flag add 42 --flag seen
```

移除标志：

```bash
himalaya flag remove 42 --flag seen
```

## 多个账户

列出账户：

```bash
himalaya account list
```

使用指定账户：

```bash
himalaya --account work envelope list
```

## 附件

保存消息中的附件：

```bash
himalaya attachment download 42
```

保存到指定目录：

```bash
himalaya attachment download 42 --downloads-dir ~/Downloads
```

## 输出格式

大多数命令都支持使用 `--output` 参数来获取结构化输出：

```bash
himalaya envelope list --output json
himalaya envelope list --output plain
```

## 调试

启用调试日志记录：

```bash
RUST_LOG=debug himalaya envelope list
```

包含回溯信息的完整追踪日志：

```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

## 小贴士

- 如需了解详细使用方法，请使用 `himalaya --help` 或 `himalaya <command> --help`。
- 消息 ID 是相对于当前文件夹而言的；更改文件夹后需重新列出。
- 若要编写包含附件的富文本邮件，请使用 MML 语法（详见 `references/message-composition.md`）。
- 建议通过 `pass`、系统密钥环或能够输出密码的命令来安全地存储密码。
