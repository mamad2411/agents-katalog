---
name: gomtm-hermes-deploy
description: Use when deploying official NousResearch hermes-agent to a Linux server or Android/Termux device, especially for customer-owned VPS handoff, Telegram gateway setup, model provider configuration, or verifying an existing Hermes Agent deployment.
---

# gomtm Hermes Deploy

## 核心原则

标准部署只使用官方 `hermes-agent` 安装、配置和 gateway 命令。不要复用 `gomtm` / `mtmai` 内嵌 Hermes 逻辑，不要假定 `/workspace/hermes-agent` 是运行前提；本地源码最多只作只读参考。

## 官方资料

执行前重新打开当前官方文档，因为 installer、provider 名称、gateway 配置会变化：

- Linux 安装: `https://hermes-agent.nousresearch.com/docs/getting-started/installation`
- 模型 Provider: `https://hermes-agent.nousresearch.com/docs/integrations/providers`
- Telegram: `https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram`
- Gateway 服务: `https://hermes-agent.nousresearch.com/docs/user-guide/messaging/`
- Termux: `https://hermes-agent.nousresearch.com/docs/getting-started/termux`

## Linux VPS 主流程

### 1. 先确认边界

- 目标运行用户默认是 `code`，安装产物应位于 `/home/code/.hermes/` 和 `/home/code/.local/bin/hermes`。
- 服务器、Telegram bot、模型 key 属于客户；不要写入本仓文档、报告、commit 或截图。
- 发现已有 Hermes 安装、已有 gateway service、已有客户配置时，先备份并向用户确认，不要覆盖。
- 需要 Telegram 私聊验收时，必须拿到客户 Telegram 数字 user ID，或得到明确授权后才可临时开放 `*`。
- 如需 root 权限，只用于系统依赖、`loginctl enable-linger code`、service 检查等宿主操作；Hermes installer 和 Hermes 命令默认以 `code` 执行。

### 2. 预检

以 root 或已有运维账号登录后检查，不要打印 secret 文件内容：

```bash
id code
sudo -iu code bash -lc 'git --version'
sudo -iu code bash -lc 'test -x ~/.local/bin/hermes && ~/.local/bin/hermes --version || true'
sudo -iu code bash -lc 'test -d ~/.hermes && find ~/.hermes -maxdepth 1 -type f -printf "%f\n" || true'
systemctl --user -M code@ status hermes-gateway --no-pager || true
```

若 `code` 用户不存在、不能登录、`git` 缺失、或已有安装状态不明，先暂停并确认修复方式。

### 3. 官方 per-user 安装

必须以 `code` 用户运行官方 installer。不要使用 `sudo curl ... | sudo bash` 的 root-mode 安装，除非用户明确要求系统级安装。

```bash
sudo -iu code bash -lc 'curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash'
sudo -iu code bash -lc '~/.local/bin/hermes --version'
sudo -iu code bash -lc '~/.local/bin/hermes doctor'
sudo -iu code bash -lc '~/.local/bin/hermes config check'
```

期望布局：

| 内容 | 路径 |
| --- | --- |
| 源码与 venv | `/home/code/.hermes/hermes-agent/` |
| 命令入口 | `/home/code/.local/bin/hermes` |
| 配置、会话、日志 | `/home/code/.hermes/` |
| 主要配置 | `/home/code/.hermes/config.yaml` |
| secrets | `/home/code/.hermes/.env` |

### 4. 配置单一默认模型

优先使用 `hermes model` 交互配置；无人值守或自动化时可直接写官方配置文件。自定义 OpenAI-compatible endpoint 使用 `model.provider: custom`，不要使用旧的 `OPENAI_BASE_URL` / `LLM_MODEL` 方式。

`/home/code/.hermes/config.yaml` 示例，只放非 secret 或确需官方支持的模型字段：

```yaml
model:
  provider: custom
  default: <model-id>
  base_url: https://example.com/v1
  api_key: ${HERMES_MODEL_API_KEY}
  context_length: 1050000
```

`/home/code/.hermes/.env` 示例：

```env
HERMES_MODEL_API_KEY=<redacted>
```

如果当前 Hermes 版本要求 `model.api_key` 直接在 `config.yaml` 中配置，则可以按官方当前文档执行，但交付记录中只能写“已配置”，不要泄露值。配置后验证：

```bash
sudo -iu code bash -lc '~/.local/bin/hermes chat -q "Reply with OK" --quiet'
```

### 5. 配置 Telegram Gateway

Telegram 私聊必须有 bot token 和数字 user ID。用户名、bot name、手机号都不能替代 `TELEGRAM_ALLOWED_USERS`。

`/home/code/.hermes/.env`：

```env
TELEGRAM_BOT_TOKEN=<redacted>
TELEGRAM_ALLOWED_USERS=<numeric-user-id>
```

可选 group 配置：

```env
TELEGRAM_GROUP_ALLOWED_USERS=<numeric-user-id>
TELEGRAM_GROUP_ALLOWED_CHATS=<negative-chat-id>
```

`/home/code/.hermes/config.yaml` 中可保留安全默认：

```yaml
telegram:
  require_mention: true
```

注意：

- 私聊验收只需要 `TELEGRAM_ALLOWED_USERS`。
- 群组中 bot 沉默时，先检查 BotFather privacy mode、是否为 admin、修改 privacy 后是否移除再重新添加。
- `TELEGRAM_ALLOWED_USERS=*` 只可在用户明确接受风险时临时使用；交付前必须收敛为客户 user ID。
- webhook 模式需要公网 HTTPS URL 和 `TELEGRAM_WEBHOOK_SECRET`；普通 always-on VPS 默认使用 polling 即可。

### 6. 安装并启动 gateway 服务

普通 VPS 优先使用 user service，并启用 linger 让 `code` 用户服务退出 SSH 后继续运行：

```bash
sudo loginctl enable-linger code
sudo -iu code bash -lc '~/.local/bin/hermes gateway install'
sudo -iu code bash -lc '~/.local/bin/hermes gateway start'
sudo -iu code bash -lc '~/.local/bin/hermes gateway status'
```

日志检查不要打印 `.env`：

```bash
sudo -iu code bash -lc 'tail -n 120 ~/.hermes/logs/gateway.log'
```

如用户明确要求 boot-time system service，再按官方 `sudo hermes gateway install --system` 路径执行；执行前确认不会与 user service 并存冲突。

### 7. 验收

最小验收清单：

- `sudo -iu code bash -lc '~/.local/bin/hermes --version'` 成功。
- `sudo -iu code bash -lc '~/.local/bin/hermes doctor'` 无阻塞错误。
- `sudo -iu code bash -lc '~/.local/bin/hermes config check'` 无必须迁移项。
- `sudo -iu code bash -lc '~/.local/bin/hermes chat -q "Reply with OK" --quiet'` 能调用模型回复。
- `sudo -iu code bash -lc '~/.local/bin/hermes gateway status'` 显示运行中。
- 被允许的 Telegram 用户私聊 bot 能得到回复。
- `~/.hermes/logs/gateway.log` 没有 token invalid、unauthorized、model auth failed、event loop crash 等错误。

交付说明必须包含：运行用户、安装路径、`hermes gateway status/start/stop/restart`、日志路径、bot username、已授权 user ID、模型 endpoint 名称、token/key 轮换方式。不得包含实际 token 或 API key。

## Android / Termux 补充

Termux 也使用官方 installer：

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Termux installer 会自动走 Android 分支，使用 `pkg` 安装依赖并优先尝试 `.[termux-all]`。如失败，按官方 Termux 文档补齐 `python`、`git`、`clang`、`rust`、`make`、`pkg-config`、`libffi`、`openssl`、`ca-certificates`、`curl` 后重试。

云端 Android 设备操作时，按需使用 `using-vmoscloud` 和 `gomtm-adb-operate`；不要把 Linux VPS 的 systemd/gateway service 步骤套到 Termux。

## 常见错误

| 错误 | 正确做法 |
| --- | --- |
| root-mode 安装到 `/root/.hermes` | 以 `code` 运行 per-user installer |
| 使用 gomtm/mtmai 内嵌 Hermes 配置 | 使用官方 `~/.hermes/config.yaml` 和 `.env` |
| 把 Telegram username 写入 allowlist | 使用数字 user ID |
| 不设 `TELEGRAM_ALLOWED_USERS` | 默认会拒绝用户；先配置 allowlist 或 pairing |
| SSH 前台运行 `hermes gateway` | 安装并启动 gateway service |
| 把 token 写进报告或 skill | 只写 `<redacted>`，secret 只进客户服务器 `.env` |
| 群组不响应就改代码 | 先查 BotFather privacy、admin、mention、group allowlist |
| 跳过模型烟雾测试 | 先 `hermes chat -q`，再验收 Telegram |

## 回滚

停止 gateway：

```bash
sudo -iu code bash -lc '~/.local/bin/hermes gateway stop'
```

恢复配置时，只恢复预先备份的 `/home/code/.hermes/config.yaml` 和 `/home/code/.hermes/.env`。bot token 泄露时让客户在 BotFather `/revoke` 或重新生成 token；模型 key 泄露时在模型 API 平台轮换。
