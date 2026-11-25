---
name: autoloop
description: Issue 驱动的全自动 Agent 管线 — 为任意 GitHub 仓库部署 cron 轮询 + Claude Code 自动修复 + 延迟验证 + 人工升级的闭环工作流（自动运维、纯 Shell）。
metadata:
  version: 1.0.0
  author: OpenClaw
---

# AutoLoop

为任意 GitHub 仓库部署 **issue 驱动的全自动 Agent 管线**。

## 工作流

```
GitHub Issue (type:service label)
    ↓  cron */30
gh-issue-router.sh — 按 label 路由
    ↓
auto-fix.sh — CC 执行修复
    ↓  输出 FIXED:
标记 pending-verify
    ↓  下一轮 cron
延迟验证（verify 块 或 CC 验证）
    ↓  通过
auto-close issue
    ↓  失败 ≥3 次
标记 needs-decision + TG 通知人工
```

## 依赖

| 依赖 | 安装方式 |
|------|----------|
| `gh` (GitHub CLI) | https://cli.github.com/ |
| `claude` (Claude Code) | `npm install -g @anthropic-ai/claude-code` |
| `python3` | 系统自带或 `apt install python3` |
| `setfacl` (可选) | `apt install acl` |

## 快速开始

```bash
# 在仓库/skill 目录下执行
bash install.sh --repo user/repo

# 自定义参数
bash install.sh \
    --repo myorg/myapp \
    --user agent \
    --cron-interval 15 \
    --max-retries 5 \
    --work-dir /opt/workspace
```

## 安装参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--repo` | (必需) | 目标 GitHub 仓库 `OWNER/REPO` |
| `--user` | `ccworker` | CC 执行用户名 |
| `--work-dir` | `/root/clawd` | 工作目录 |
| `--log-dir` | `/var/log/autoloop` | 日志目录 |
| `--cron-interval` | `30` | cron 轮询间隔(分钟) |
| `--max-retries` | `3` | issue 最大自动修复重试次数 |
| `--tg-script` | (空) | Telegram 通知脚本路径 |
| `--skip-user` | - | 跳过用户创建 |
| `--skip-cron` | - | 跳过 cron 配置 |

## Issue 编写规范

### 基本格式

标题给人看，body 给 CC 看：

```markdown
标题: Redis 连接池耗尽导致 API 500

body:
检查 /srv/myapp/services/api 的 Redis 连接配置。
当前 max_connections=10 不够用，需要增加到 50。

修改 config.py 中的 REDIS_MAX_CONNECTIONS。
重启服务后验证 API 返回 200。
```

### 可选：内嵌验证块

在 body 中加入 ` ```verify ` 代码块，auto-fix 会自动用这段命令验证修复结果：

````markdown
```verify
curl -s http://localhost:8080/health | grep -q '"status":"ok"'
```
````

### Labels

| Label | 含义 |
|-------|------|
| `type:service` | 服务/运维类，自动修复 |
| `type:bug` | Bug，router 记录，不自动修复 |
| `type:enhancement` | 功能增强，人工处理 |
| `type:reading` | 阅读/研究任务，router 记录，不自动修复 |
| `pending-verify` | 等待下一轮自动验证 |
| `needs-decision` | 重试耗尽，需人工介入 |

## 核心脚本

| 脚本 | 用途 |
|------|------|
| `install.sh` | 一键安装与配置 |
| `scripts/cc.sh` | CC 调用封装（bypassPermissions） |
| `scripts/auto-fix.sh` | 主轮询：扫 issue → CC 修 → 验证 → close |
| `scripts/gh-issue-router.sh` | 按 label 路由分发 |

## 日志与排错

```bash
# 查看实时日志
tail -f /var/log/autoloop/auto-fix.log

# 查看 cron 日志
tail -f /var/log/autoloop/cron.log

# 手动触发一次
. <install-dir>/.env
bash <install-dir>/scripts/auto-fix.sh

# 查看当前 cron
crontab -l | grep autoloop
```

## 卸载

```bash
# 移除 cron
crontab -l | grep -v '# autoloop:' | crontab -

# 删除日志
rm -rf /var/log/autoloop

# 删除 skill 目录
rm -rf <install-dir>

# 可选：删除执行用户（会一并删掉复制过去的 gh/Claude 凭证）
userdel -r ccworker
```

## 安全提示

- CC 以 `bypassPermissions` 运行，并持有复制过去的 gh/Claude 凭证；`verify` 代码块由 cron 用户（通常是 root）以 `bash -c` 执行。
- 建议只用于私有仓库，或只有可信协作者能打标签、编辑 issue 的仓库。
- 只有能打 `type:service` 标签的人才能触发修复。
