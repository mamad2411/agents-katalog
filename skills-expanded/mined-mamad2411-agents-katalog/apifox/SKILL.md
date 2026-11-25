---
name: apifox-skill
description: "Use when the user wants to read, search, or generate code from Apifox API documentation. Automatically fetches and caches OpenAPI specs from Apifox projects and exposes endpoints, schemas, and examples. Trigger on mentions of Apifox, 接口文档, API文档, project-id, 刷新接口文档, or generating models/code from Apifox."
disable-model-invocation: true
allowed-tools: Bash(node *)
argument-hint: "[--token=xxx] [--project-id=123] [--project-id=456] [--project-name=orders]"
---

# Apifox API Docs

## 概览

本 skill **直接替代 apifox-mcp-server**：通过 Apifox Open API 拉取项目接口文档，缓存在 skill 本地，然后让 AI 读取、搜索、生成代码。不再需要单独注册 MCP server，也不需要用户手动执行 node 脚本。

核心设计：

- `config.json`：统一配置 token + 多个 projectId（已加入 `.gitignore`）
- `scripts/fetch-project.mjs`：拉取并缓存项目接口文档
- `scripts/read-project.mjs`：读取缓存的接口文档
- `scripts/refresh-project.mjs`：强制刷新缓存

## 斜杠命令 `/apifox-skill`

用户只需输入 `/apifox-skill`，AI 自动完成后续流程。

### 1. 检查配置

```bash
node "${CLAUDE_SKILL_DIR}/scripts/read-config.mjs"
```

- `status=ready`：已有 `config.json`，跳到步骤 3。
- `status=not_ready`：进入步骤 2 初始化。

### 2. 初始化配置（自动）

解析 `$ARGUMENTS`：

- 如果已经是 `--token=... --project-id=...` 等标准参数格式，直接透传给 `init.mjs`。
- 如果是自然语言（例如「我的 token 是 afxp-xxx，新增项目：my-project id：123456」），必须先从文本中提取以下信息：
  1. **token**：匹配 `afxp-` 或 `afs-` 开头的字符串。
  2. **项目 ID**：匹配纯数字。
  3. **项目名称**：提取「新增项目：」或「项目名」后面的名称；未提供时使用 `project-{id}`。
  4. 多个项目时，按同样的方式提取每一组 `id` 和 `name`。
- 提取完成后，拼成标准参数格式再运行 `init.mjs`。

若 `$ARGUMENTS` 为空，使用 `AskUserQuestion` 依次收集：

1. Apifox API 访问令牌
2. 项目 ID（纯数字，多个用逗号分隔）
3. 每个项目的名称（可选，用于区分多项目）

然后拼成参数并运行：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/init.mjs" $ARGUMENTS
```

示例参数：

```bash
--token=afxp-xxx \
  --project-id=123456 --project-name=orders \
  --project-id=789012 --project-name=payments \
  -y
```

自然语言示例及转换：

```text
用户：/apifox-skill 我的 token 是 afxp-xxx，新增项目：my-project id：123456
AI 转换后：--token=afxp-xxx --project-id=123456 --project-name=my-project -y
```

> 若 `${CLAUDE_SKILL_DIR}` 未设置，脚本会从自身位置推导 skill 根目录；命令中也可替换为 skill 安装路径。

### 3. 配置就绪后

读取 `config.json`，向用户展示可用项目，并提供提示词示例：

- 「根据 orders 项目生成 User 模型代码」
- 「列出 payments 项目的所有接口」
- 「读取 orders 项目 /users 路径的接口定义」
- 「刷新 orders 项目的接口文档缓存」

## AI 自动驱动流程

当用户用自然语言请求 API 文档相关操作时，AI 自动调用脚本，**不要让用户手动执行 node 命令**。

### 示例 1：生成模型代码

用户：「根据 orders 项目生成 Product 模型代码」

AI 自动执行：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/fetch-project.mjs" --project-name=orders
node "${CLAUDE_SKILL_DIR}/scripts/read-project.mjs" --project-name=orders
```

然后基于返回的 OpenAPI spec 生成代码。

### 示例 2：只读索引，快速了解项目

用户：「orders 项目有哪些接口？」

AI 自动执行：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/read-project.mjs" --project-name=orders --index
```

### 示例 3：读取具体路径

用户：「orders 项目 /users 接口是怎么定义的？」

AI 自动执行：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/read-project.mjs" --project-name=orders --path=/users
```

### 示例 4：刷新缓存

用户：「刷新 orders 项目的接口文档」

AI 自动执行：

```bash
node "${CLAUDE_SKILL_DIR}/scripts/refresh-project.mjs" --project-name=orders
```

## 项目匹配规则

`--project-name` 支持：

1. 完整项目名（如 `orders`）
2. 项目名前缀（如 `ord` 匹配 `orders`）
3. 项目 ID（如 `123456`）

如果用户没有指定项目，默认使用 `config.json` 中的第一个项目。

## 常用提示词示例

把这些示例在 `/apifox-skill` 初始化完成后展示给用户：

```text
根据 orders 项目生成所有数据模型的 TypeScript 定义
根据 payments 项目生成 /transactions 接口的 MVC 代码
orders 项目 /users GET 接口的响应字段是什么
对比 orders 和 payments 两个项目的 User 模型差异
刷新 orders 项目的接口文档缓存
orders 项目有哪些 POST 接口
```

## 前置条件

- Node.js >= 18
- Apifox API 访问令牌（Apifox 头像 → 账号设置 → API 访问令牌 → 新建）
- 至少一个 Apifox 项目 ID（Apifox 项目 → 项目设置 → 基本设置，纯数字）

## 文件结构

安装后的 skill 目录结构：

```text
~/.claude/skills/apifox-skill/
├── SKILL.md                # 本文件
├── config.template.json    # 配置模板
├── .gitignore              # 忽略 config.json / data/cache
└── scripts/
    ├── init.mjs            # 初始化 / 更新 config.json
    ├── read-config.mjs     # 读取并校验 config.json
    ├── fetch-project.mjs   # 拉取项目接口文档并缓存
    ├── read-project.mjs    # 读取缓存的接口文档
    ├── refresh-project.mjs # 刷新缓存
    ├── lib/
    │   ├── config.mjs      # config.json 读写校验
    │   ├── apifox.mjs      # Apifox Open API 客户端
    │   └── cache.mjs       # 本地缓存管理
    └── test/
        └── e2e.mjs         # 端到端测试
```

## 完成检查

- [ ] `/apifox-skill` 成功生成 `config.json`
- [ ] `read-config.mjs` 返回 `status=ready`
- [ ] 用自然语言请求时，AI 自动调用 `fetch-project` / `read-project`
- [ ] AI 能基于接口文档生成代码
