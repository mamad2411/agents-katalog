---
name: gerrit-restapi
description: |
  Gerrit 代码审查系统的 REST API 技能。用于执行当前仓库内已实现的 Gerrit REST API endpoint，并支持按需扩展新 endpoint。当需要查询变更、审查代码或执行项目管理相关操作时使用此技能。已有子命令时优先通过 scripts/gerrit_api.py 执行；接口未实现时允许自行编写请求代码。
---

# Gerrit REST API 技能

本技能通过 Gerrit REST API 与目标实例交互。

## 首次使用：配置引导

首次使用本技能时，先检查配置文件 `~/.bicv/gerrit.json` 是否存在。

**若配置不存在**，使用 AskUserQuestion 引导用户完成配置，生成 `~/.bicv/gerrit.json`：

1. 询问 Gerrit 服务器地址（示例：`http://10.100.193.154:8081`）
2. 询问 Gerrit 用户名
3. 询问 Gerrit HTTP 密码（在 Gerrit Settings → HTTP Password 中生成）

```json
{
  "default_system": "default",
  "systems": {
    "default": {
      "url": "<用户输入的地址>",
      "aliases": ["default", "main"],
      "username": "<用户名>",
      "http_password": "<HTTP密码>"
    }
  }
}
```

> 密码保存到本地配置文件，不会上传到代码仓库。

## 执行策略

### 优先复用已有脚本

当 `scripts/gerrit_api.py` 已包含目标接口的子命令时，**必须**直接调用该脚本，不得重复实现。这是为了保证一致性（统一的认证、错误处理、日志格式）和可维护性。

### 接口未实现时的选择

当现有脚本不覆盖目标 API 时，可以选择以下任一方式：

1. **扩展脚本**（推荐）：在 `scripts/gerrit_api.py` 中新增子命令，再执行。优点是可复用、可维护、可积累能力。
2. **临时请求**（允许）：自行编写 `curl`、`python` 或临时脚本完成请求。适合一次性探索、紧急调试或不常用的接口。

### 环境约束

- **脚本标准库**：扩展 `scripts/gerrit_api.py` 时，只使用 Python 标准库；不要引入 `requests`、`httpx` 或 shell 依赖。
- **认证复用**：临时请求通过 `~/.bicv/gerrit.json` 获取认证信息。

### 默认执行流程

1. 在 `references/` 中确认接口和参数。
2. 检查 `scripts/gerrit_api.py` 中是否已有对应子命令。
3. **有子命令**：直接执行该脚本。
4. **无子命令**：
   - 若该接口预计会重复使用，优先在脚本中新增子命令。
   - 若仅为一次性查询或调试，可编写临时请求代码或 curl 命令。

## 认证与配置

### Gerrit 服务器配置

| 配置项 | 说明 | 获取方式 |
|--------|------|---------|
| `url` | Gerrit 服务器地址 | 例如: `http://10.100.193.154:8081` 或 `https://gerrit.example.com` |
| `username` | Gerrit 用户名 | 登录 Gerrit 后在个人设置中查看 |
| `http_password` | HTTP 密码 | 在 Gerrit 个人设置页面生成 |

**获取 HTTP 密码的步骤:**
1. 登录 Gerrit Web UI
2. 进入 `Settings` -> `HTTP Password`
3. 点击 `Generate Password` 生成密码

### 认证方式

Gerrit REST API 支持多种认证方式:

1. **匿名访问**: 默认情况下，所有 REST 端点都假设为匿名访问（只读权限）
2. **HTTP Basic 认证**: 在端点 URL 前添加 `/a/` 前缀，使用 HTTP 密码进行认证
3. **Access Token**: 可以在 URL 的 `access_token` 查询参数中提供授权 cookie

详细协议说明见 `references/rest-api-protocol.md`。

### 连接配置

连接配置仅通过 `~/.bicv/gerrit.json` 文件管理，不支持环境变量方式。

配置加载优先级：
1. 显式参数：`--system`、`--gerrit`、`--user`
2. `~/.bicv/gerrit.json` 中的 `default_system`

### 多 Gerrit 系统配置

默认配置文件路径为 `~/.bicv/gerrit.json`。脚本不接受 `--config`；只能读取这个固定路径。

通过 `gerrit.json` 可以定义一个默认 Gerrit 系统，并扩展任意多个命名系统。

```json
{
  "default_system": "default",
  "systems": {
    "default": {
      "url": "https://gerrit.example.com",
      "aliases": ["default", "main", "主系统"],
      "username": "your_username",
      "http_password": "your_http_password"
    },
    "backup": {
      "url": "https://gerrit-backup.example.com",
      "aliases": ["backup", "备份系统"],
      "username": "backup_username",
      "http_password": "backup_password"
    }
  }
}
```

关键字段：`url`、`aliases`、`username`、`http_password`。

解析规则：
1. 未指定 `--system` 时，优先使用 `default_system`
2. 指定 `--system foo` 时，按系统名、`aliases`、URL 主机名、URL 中的 IP/域名匹配
3. `--user` 覆盖配置文件中的认证信息
4. 配置文件缺失时脚本直接报错退出

### 认证说明

认证信息由 `scripts/gerrit_api.py` 读取；临时请求时也通过 `~/.bicv/gerrit.json` 获取认证信息。

## 响应格式

详细协议说明见 `references/rest-api-protocol.md`，包括：
- JSON 响应格式和 XSSI 防护前缀 `)]}'`
- 时间戳格式: `yyyy-mm-dd hh:mm:ss.fffffffff` (UTC)
- URL 编码要求
- gzip 压缩支持

## 参考文档

`references/` 下保存 Gerrit REST API 参考全集，不代表这些端点当前都已有实现。

### 当前实现覆盖范围

当前 `scripts/gerrit_api.py` 只实现了以下子命令与端点：

| 子命令 | 方法 | 端点 |
|------|------|------|
| `query-changes` | `GET` | `/changes/` |
| `get-change` | `GET` | `/changes/{change-id}` |
| `get-change-details` | `GET` | `/changes/{change-id}/detail` |
| `list-reviewers` | `GET` | `/changes/{change-id}/reviewers/` |
| `list-revisions` | `GET` | `/changes/{change-id}` + `o=ALL_REVISIONS` |
| `get-revision` | `GET` | `/changes/{change-id}` + `o=ALL_REVISIONS` |
| `list-change-messages` | `GET` | `/changes/{change-id}/messages/` |
| `get-topic` | `GET` | `/changes/{change-id}/topic` |
| `list-files` | `GET` | `/changes/{change-id}/revisions/{revision-id}/files/` |
| `list-projects` | `GET` | `/projects/` |
| `get-project` | `GET` | `/projects/{project-name}` |
| `list-branches` | `GET` | `/projects/{project-name}/branches/` |
| `get-branch` | `GET` | `/projects/{project-name}/branches/{branch-id}` |
| `query-accounts` | `GET` | `/accounts/` |
| `get-account` | `GET` | `/accounts/{account-id}` |
| `get-account-detail` | `GET` | `/accounts/{account-id}/detail` |
| `list-groups` | `GET` | `/groups/` |
| `get-group` | `GET` | `/groups/{group-id}` |
| `list-group-members` | `GET` | `/groups/{group-id}/members/` |
| `add-reviewer` | `POST` | `/changes/{change-id}/reviewers` |
| `post-review` | `POST` | `/changes/{change-id}/revisions/{revision}/review` |
| `create-change` | `POST` | `/changes/` |

仍未整组覆盖：`access`、`accounts`、`config`、`documentation`、`groups`、`plugins`、`projects`；`changes` 也只覆盖部分接口。

处理原则：
1. 先看 `references/*.md` 确认目标 endpoint
2. 再看 `scripts/gerrit_api.py` 是否已有对应子命令
3. 已有子命令则直接调用脚本
4. 没有实现时，可选择扩展脚本或编写临时请求

大文件定位：
- `references/changes-endpoints.md`：搜索 `## /changes/{change-id}`
- `references/projects-endpoints.md`：搜索 `## /projects/{project-name}`

## 环境与工具选择

### 运行前提

| 环境 | 运行方式 | 说明 |
|------|----------|------|
| Linux | `python3` | 依赖 Python 3 标准库 |
| macOS | `python3` | 依赖 Python 3 标准库 |
| Windows | `python3` | 依赖 Python 3 标准库 |

### Python 环境检查

执行脚本前，只检查 Python 3 是否可用；不需要额外安装第三方库。

```bash
python3 --version
```

```powershell
python3 --version
```

## 使用方式

代表性命令：

```bash
# 查询变更
python3 scripts/gerrit_api.py query-changes --query "status:open"

# 获取变更及 patch set 上下文
python3 scripts/gerrit_api.py get-change-details --change-id "project~master~I123456"
python3 scripts/gerrit_api.py list-revisions --change-id "project~master~I123456" --option CURRENT_COMMIT
python3 scripts/gerrit_api.py list-files --change-id "project~master~I123456" --revision-id current

# 查询项目 / 账号 / 用户组
python3 scripts/gerrit_api.py list-projects --description --limit 20
python3 scripts/gerrit_api.py query-accounts --query "name:John" --details
python3 scripts/gerrit_api.py list-groups --limit 20

# 写操作
python3 scripts/gerrit_api.py add-reviewer --change-id "project~master~I123456" --reviewer "user@example.com" --user "username:password"
python3 scripts/gerrit_api.py post-review --change-id "project~master~I123456" --message "LGTM" --user "username:password"
```

## 安全审查：高危与严重操作确认机制

在使用本技能执行任何写操作（POST/PUT/DELETE）前，必须先判断操作的危险等级。所有 **严重** 和 **高危** 操作在执行前**必须征得用户确认**。

### 确认规则

1. **每次操作独立确认**：针对每一个具体的严重或高危操作，都必须单独向用户确认。不能因为某种类型的操作已确认过一次，后续同类型操作就跳过确认。
2. **确认内容明确**：确认时必须告知用户即将执行的具体 API 接口、HTTP 方法、目标资源以及对系统的影响。
3. **用户明确同意后方可执行**：只有用户明确回复"确认"、"执行"、"同意"等肯定答复后，才能执行操作。用户拒绝或无响应时不得执行。

完整高危矩阵见 `references/safety-confirmation-matrix.md`。

## 详细参考

### references/ 目录

关键参考：
- `rest-api-protocol.md`：协议、XSSI、防护、响应格式
- `changes-endpoints.md`：变更相关端点
- `projects-endpoints.md`：项目与分支相关端点
- `accounts-endpoints.md`：账号相关端点
- `groups-endpoints.md`：用户组相关端点
- `safety-confirmation-matrix.md`：高危/严重操作确认矩阵
- `config-schema.md`：本 skill 配置文件 `~/.bicv/gerrit.json` 的字段说明

### scripts/ 目录

| 目录 | 文件 | 用途 |
|------|------|------|
| `scripts/` | `gerrit_api.py` | 单入口脚本，包含已实现的全部子命令 |
