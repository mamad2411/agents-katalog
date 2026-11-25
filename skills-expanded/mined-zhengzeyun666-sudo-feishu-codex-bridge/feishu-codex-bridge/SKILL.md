---
name: feishu-codex-bridge
description: 通过 cc-connect Hook 将飞书消息写入本地队列，供 Codex CLI 或活跃的 Codex 桌面版任务读取和回复。当用户想配置 cc-connect、搭建飞书-Codex 消息交接时使用此技能。
---

# 飞书连接 cc-connect 与 Codex

通过 cc-connect + Hook 中继，将飞书消息交接给本机 Codex：

- 飞书私聊/群聊收发消息
- cc-connect 的 Codex CLI agent 处理普通对话
- 活跃的 Codex 桌面版任务读取 inbox 后回复或发送文件

> 当前不是无人值守的桌面版远程控制。桌面版需要有一个正在运行的任务主动读取 `inbox.jsonl`；本仓库不包含常驻轮询器，也不会自行触发桌面操作。

## 重要说明：路径与环境

本文档中出现的路径是**示例**，请根据你的实际环境替换：

- `~/.hermes/node/bin` → 你的 npm 全局 bin 目录（`npm config get prefix`/bin）
- `/Users/YOUR_USERNAME` → 你的用户目录（`whoami` 查看）
- `cli_YOUR_APP_ID` / `YOUR_APP_SECRET` → 飞书应用凭证
- `ou_YOUR_OPEN_ID` → 启动后在飞书私聊机器人发送 `/whoami` 获取

## 架构

```
飞书消息 → cc-connect(WebSocket) → Hook(relay.py) → inbox.jsonl
                                                        ↓ 主动读取
飞书 ← cc-connect send --file ← Codex CLI / Codex 桌面版任务
```

cc-connect 内置的 Codex CLI agent 同时运行处理普通消息；桌面版任务可在用户明确授权时读取 inbox 并执行高级操作。

## 前置条件

- **Codex 桌面版** 已安装
- **Node.js >= 18** 已安装
- **Python 3** 已安装
- **飞书账号**（个人即可，无需企业认证）

## 第一步：安装 cc-connect

### 方式 A：npm 安装（推荐）

```bash
npm install -g cc-connect
```

如果 npm 访问慢，设置国内镜像：

```bash
npm config set registry https://registry.npmmirror.com
npm install -g cc-connect
```

### 方式 B：Homebrew（macOS）

```bash
brew install cc-connect
```

### 方式 C：直接下载二进制

从 [GitHub Releases](https://github.com/chenhg5/cc-connect/releases) 下载对应平台的二进制：

```bash
# macOS Apple Silicon
curl -L -o cc-connect "https://github.com/chenhg5/cc-connect/releases/latest/download/cc-connect-darwin-arm64"
chmod +x cc-connect
sudo mv cc-connect /usr/local/bin/
```

```bash
# macOS Intel
curl -L -o cc-connect "https://github.com/chenhg5/cc-connect/releases/latest/download/cc-connect-darwin-amd64"
chmod +x cc-connect
sudo mv cc-connect /usr/local/bin/
```

```bash
# Linux amd64
curl -L -o cc-connect "https://github.com/chenhg5/cc-connect/releases/latest/download/cc-connect-linux-amd64"
chmod +x cc-connect
sudo mv cc-connect /usr/local/bin/
```

#### GitHub 加速（国内用户）

如果 GitHub 下载慢，使用镜像：

```bash
# ghproxy 加速
curl -L -o cc-connect "https://ghproxy.com/https://github.com/chenhg5/cc-connect/releases/latest/download/cc-connect-darwin-arm64"

# moeyy 加速
curl -L -o cc-connect "https://github.moeyy.xyz/https://github.com/chenhg5/cc-connect/releases/latest/download/cc-connect-darwin-arm64"
```

macOS 下载后如提示安全警告，移除隔离标记：

```bash
xattr -d com.apple.quarantine cc-connect
```

### 验证安装

```bash
cc-connect --version
```

如果提示 `command not found`，npm 全局 bin 目录不在 PATH 中：

```bash
# 方法 1：找到 bin 目录并临时加入 PATH
npm config get prefix
# 假设输出 /usr/local，则 bin 在 /usr/local/bin
# 假设输出 ~/.hermes/node，则：
export PATH="$(npm config get prefix)/bin:$PATH"

# 方法 2：永久加入 ~/.zshrc
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## 第二步：创建飞书机器人

1. 访问 [飞书开放平台](https://open.feishu.cn/) → 控制台 → 创建企业自建应用
2. 应用名称随意，如 `Codex助手`
3. 记录 **App ID**（`cli_xxx` 格式）和 **App Secret**

### 2.1 启用机器人

**应用能力 → 机器人 → 启用**

### 2.2 权限管理

搜索并添加以下权限，点击「申请发布」：

| 权限 | 标识 | 用途 |
|------|------|------|
| 获取用户基本信息 | `contact:user.base:readonly` | 识别用户 |
| 接收群聊 @ 消息 | `im:message.group_at_msg:readonly` | 群聊互动 |
| 接收私聊消息 | `im:message.p2p_msg:readonly` | 私聊互动 |
| 读取群消息内容 | `im:message.group_msg` | 读取群消息 |
| 以机器人身份发消息 | `im:message:send_as_bot` | 回复消息 |

### 2.3 事件订阅（关键！容易出错）

**事件与回调 → 事件配置**

- ✅ 订阅方式：选择 **「使用长连接接收事件」**（不是 HTTP 回调！）
- ✅ 添加事件：搜索并添加 `im.message.receive_v1`
- ✅ 点击保存

### 2.4 版本发布（必须做！）

**版本管理与发布 → 创建版本**

填写版本号（如 `1.0.0`）和更新说明 → **申请发布**。

> ⚠️ 仅保存权限和事件配置是不够的，必须创建版本并发布才生效！

## 第三步：配置 cc-connect

### 3.1 一键配置（推荐）

```bash
cc-connect feishu setup --project my-workspace --app cli_YOUR_APP_ID:YOUR_APP_SECRET
```

这会自动写入 `~/.cc-connect/config.toml`。

### 3.2 手动配置

如果一键配置不行，手动创建 `~/.cc-connect/config.toml`，参考仓库中的 [config.toml.template](config.toml.template)。

关键字段：
- `work_dir` → 单个项目目录，不要直接填写整个用户主目录
- `app_id` / `app_secret` → 飞书应用凭证
- `allow_from` → 允许使用机器人的 open_id
- `admin_from` → 必须写在 `[[projects]]` 层级，控制特权命令使用者
- `mode` → Codex 建议先用 `suggest`；`yolo` 会绕过审批和沙箱
- `[[hooks]]` 中的 `command` 路径 → 指向 relay.py

如果首次配置时不知道 open_id，可临时把 `allow_from` 设为 `*`，只发送 `/whoami`；拿到 ID 后立即写入 `allow_from` 和 `admin_from`，再重启 cc-connect。

### 3.3 部署中继脚本

将仓库中的 [relay.py](relay.py) 复制到 `~/.cc-connect/relay.py`：

```bash
cp relay.py ~/.cc-connect/
chmod 700 ~/.cc-connect
chmod +x ~/.cc-connect/relay.py
chmod 600 ~/.cc-connect/config.toml
```

> relay.py 的详细注释和说明见文件本身，这里不重复内嵌，保持文档和代码分离。

## 第四步：启动

### 前台运行（首次调试）

```bash
export PATH="$(npm config get prefix)/bin:$PATH"
cd ~/.cc-connect
touch inbox.jsonl
chmod 600 inbox.jsonl config.toml
cc-connect --force
```

看到 `platform ready` 和 `connected to wss://msg-frontier.feishu.cn` 即成功。

### 注册为系统服务（推荐，开机自启）

```bash
cc-connect daemon install --work-dir ~/.cc-connect
```

管理命令：
```bash
cc-connect daemon status     # 查看状态
cc-connect daemon restart    # 重启
cc-connect daemon logs -f    # 实时日志
cc-connect daemon stop       # 停止
cc-connect daemon uninstall  # 卸载
```

## 第五步：验证链路

1. 在飞书上私聊机器人，发送 "你好"
2. 检查 inbox：`tail -n 1 ~/.cc-connect/inbox.jsonl`
3. 应看到你的消息内容，包括 `session_key`、`content` 等字段

### 测试桌面版回复

```bash
cc-connect send -s "feishu:CHAT_ID:OPEN_ID" -m "Codex 桌面版已就绪 ✅"
```

（`CHAT_ID` 和 `OPEN_ID` 从 inbox.jsonl 的 `session_key` 中提取）

## 第六步：日常使用

### 发送消息

```bash
cc-connect send -s "feishu:{chat_id}:{open_id}" -m "消息内容"
```

### 发送文件

```bash
cc-connect send -s "feishu:{chat_id}:{open_id}" --file "/path/to/file.xlsx" -m "文件说明"
```

### Session Key 格式

`feishu:{chat_id}:{open_id}` — 从 `~/.cc-connect/inbox.jsonl` 中 `session_key` 字段获取。

## 工作流程

```
你（飞书）          CLI agent            桌面版 Codex
   │                  │                      │
   ├─"你好"──────────→│                      │
   │←─"你好！"───────┤                      │
   │                  │                      │
   ├─"发桌面的        │                      │
   │  report.xlsx"───→│                      │
   │                  ├─(hook→inbox)────────→│
   │                  │                      ├─轮询 inbox
   │                  │                      ├─找到文件并发送
   │←─📎 report.xlsx ─┼─────────────────────┤
```

## 飞书常用命令

| 命令 | 用途 |
|------|------|
| `/whoami` | 获取 open_id |
| `/new` | 新会话 |
| `/compress` | 压缩上下文 |
| `/model` | 查看/切换模型 |
| `/mode` | 切换 agent 模式 |
| `/help` | 帮助 |

## 已知限制

### Hook 无法条件路由

cc-connect 的 Hook 在 `message.received` 时无条件触发，无法根据消息内容决定是否走 CLI agent 还是桌面版。这意味着：

- CLI agent 会处理**所有**消息（包括它做不了的）
- 桌面版通过 inbox 并行接收消息，可以额外处理
- 两条回复可能同时到达飞书（CLI 一条 + 桌面版一条）

**当前折中方案：** CLI 处理简单消息，桌面版截获后做高级操作（文件发送、浏览器操控）。如果 CLI 回复说"我做不了"，桌面版可以之后补发。

### 无 Codex 桌面版原生 agent 类型

cc-connect 的 `agent.type = "codex"` 底层调用的是 `codex exec --json`（CLI 模式），不具备桌面版的插件能力（Computer Use、浏览器控制、文档处理等）。Codex 桌面版 `app-server` 使用内部协议，无法直接被 cc-connect 调用。

这就是为什么需要通过 Hook + inbox 中继的方案来让桌面版参与——本质上是 workaround。

### inbox 轮询非实时

桌面版 Codex 需要在一个正在运行的任务中主动读取 inbox.jsonl 才能发现新消息，不是推送模式。这意味着：

- 桌面版不在当前会话时，消息会堆积在 inbox 中
- 桌面版处理有延迟（取决于轮询频率）

## 进阶：模型与 Provider

模型和第三方 Provider 由 cc-connect 与 Codex CLI 的当前配置决定。请以 cc-connect 官方 `config.example.toml` 和 Codex 文档为准，不要直接照抄未经验证的模型名。

## 故障排查

### 飞书消息无回复

1. 确认事件订阅方式为「长连接」
2. 确认权限和事件已发布（发布后等 2-5 分钟）
3. 在飞书开发者后台查看「事件与回调 → 日志」是否有推送记录
4. 确认 cc-connect 日志中 `connected to wss://msg-frontier.feishu.cn`

### inbox.jsonl 无消息

1. 确认 config.toml 中 `[[hooks]]` 的 `command` 路径拼写正确
2. 在仓库中运行中继测试：`python3 -m unittest -v`
3. 查看 cc-connect 日志是否有 `hooks: command executed`

### 启动冲突

```bash
# 完整清理
pkill -f cc-connect
rm -f ~/.cc-connect/.config.toml.lock ~/.cc-connect/run/api.sock
# 重新启动
cc-connect --force
```

### npm 安装失败

```bash
# 切换淘宝镜像
npm config set registry https://registry.npmmirror.com
# 使用 cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
cnpm install -g cc-connect
```

### macOS 安全警告

```bash
# 允许运行未签名应用
xattr -d com.apple.quarantine /path/to/cc-connect
# 或在系统设置 → 隐私与安全性 → 仍要打开
```

## 参考

- cc-connect 项目：https://github.com/chenhg5/cc-connect
- 飞书接入文档：https://github.com/chenhg5/cc-connect/blob/main/docs/feishu.md
- 飞书开放平台：https://open.feishu.cn
