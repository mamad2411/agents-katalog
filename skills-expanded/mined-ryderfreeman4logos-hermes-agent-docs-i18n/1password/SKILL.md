---
name: 1password
description: Set up op CLI, sign in, and read or inject secrets.
version: 1.0.0
author: arceus77-7, enhanced by Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, secrets, 1password, op, cli]
    category: security
setup:
  help: "Create a service account at https://my.1password.com → Settings → Service Accounts"
  collect_secrets:
    - env_var: OP_SERVICE_ACCOUNT_TOKEN
      prompt: "1Password Service Account Token"
      provider_url: "https://developer.1password.com/docs/service-accounts/"
      secret: true
---

# 1Password CLI

当用户希望使用 1Password 来管理机密信息，而非通过明文环境变量或文件时，可使用此技能。

## 需求条件

- 1Password 账户
- 已安装 1Password CLI（`op`）
- 以下任意一种方式：桌面应用集成、服务账户令牌（`OP_SERVICE_ACCOUNT_TOKEN`）或 Connect 服务器
- 为在 Hermes 终端调用期间保持会话稳定，需配备 `tmux`（仅适用于桌面应用流程）

## 使用场景

- 安装或配置 1Password CLI
- 使用 `op signin` 登录
- 读取类似 `op://Vault/Item/field` 这样的机密信息引用
- 使用 `op inject` 将机密信息注入配置文件/模板中
- 通过 `op run` 使用带机密信息的环境变量运行命令

## 认证方式

### 服务账户（Hermes 推荐方式）

在 `${HERMES_HOME:-~/.hermes}/.env` 文件中设置 `OP_SERVICE_ACCOUNT_TOKEN`（该技能在首次加载时会提示用户输入此值）。
无需使用桌面应用。支持 `op read`、`op inject`、`op run` 命令。

```bash
export OP_SERVICE_ACCOUNT_TOKEN="your-token-here"
op whoami  # verify — should show Type: SERVICE_ACCOUNT
```

### 桌面应用集成（交互式）

1. 在 1Password 桌面应用中开启该功能：设置 → 开发者 → 与 1Password CLI 集成
2. 确保应用处于解锁状态
3. 运行 `op signin` 命令，并批准生物识别验证请求

### 连接服务器（自托管）

```bash
export OP_CONNECT_HOST="http://localhost:8080"
export OP_CONNECT_TOKEN="your-connect-token"
```

## 设置

1. 安装 CLI：

```bash
# macOS
brew install 1password-cli

# Linux (official package/install docs)
# See references/get-started.md for distro-specific links.

# Windows (winget)
winget install AgileBits.1Password.CLI
```

2. 验证：

```bash
op --version
```

3. 从上方选择一种认证方式并对其进行配置。

## Hermes 执行模式（桌面应用流程）

Hermes 的终端命令默认为非交互式，因此在多次调用之间可能会丢失认证上下文。
若要在桌面应用集成中可靠地使用 `op` 命令，请在独立的 tmux 会话中执行登录和密钥相关操作。

注意：当使用 `OP_SERVICE_ACCOUNT_TOKEN` 时无需此操作——该令牌会自动在多次终端调用之间保持有效。

```bash
SOCKET_DIR="${TMPDIR:-/tmp}/hermes-tmux-sockets"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/hermes-op.sock"
SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell

# Sign in (approve in desktop app when prompted)
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "eval \"\$(op signin --account my.1password.com)\"" Enter

# Verify auth
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter

# Example read
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op read 'op://Private/Npmjs/one-time password?attribute=otp'" Enter

# Capture output when needed
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200

# Cleanup
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

## 常见操作

### 读取机密信息

```bash
op read "op://app-prod/db/password"
```

### 获取一次性密码

```bash
op read "op://app-prod/npm/one-time password?attribute=otp"
```

### 注入模板中

```bash
echo "db_password: {{ op://app-prod/db/password }}" | op inject
```

### 使用密钥环境变量运行命令

```bash
export DB_PASSWORD="op://app-prod/db/password"  # example op:// reference, resolved by `op run`
op run -- sh -c '[ -n "$DB_PASSWORD" ] && echo "DB_PASSWORD is set" || echo "DB_PASSWORD missing"'
```

## 使用规范

- 除非用户明确要求，否则绝不要将原始密钥信息返回给用户。
- 建议使用 `op run` / `op inject` 命令，而非将密钥直接写入文件中。
- 若遇到“账户未登录”的错误提示，可在同一 tmux 会话中再次执行 `op signin` 命令。
- 在无法使用桌面应用集成环境（无界面模式/持续集成场景）时，请采用服务账户令牌认证方式。

## 关于持续集成/无界面模式的说明

在非交互式使用场景下，应通过 `OP_SERVICE_ACCOUNT_TOKEN` 进行身份验证，避免使用需要交互操作的 `op signin` 命令。
服务账户功能要求 CLI 版本至少为 2.18.0。

## 参考资料

- `references/get-started.md`
- `references/cli-examples.md`
- https://developer.1password.com/docs/cli/
- https://developer.1password.com/docs/service-accounts/
