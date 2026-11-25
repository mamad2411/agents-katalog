---
name: lovrabet
description: 当用户请求涉及 Lovrabet/云兔/yuntoo 平台的数据集查询、SQL 创建、BFF 开发时使用。触发词：数据集、数据表、自定义 SQL、filter、sql.execute、bff.execute、get_dataset_detail、validate_sql_content、save_or_update_custom_sql、save_or_update_bff_script、@lovrabet/sdk、MCP SQL 工作流、多表关联、lovrabet 开发。
---

# Lovrabet 开发工作流（路由指南）

Lovrabet 中文名为**云兔**，也常写作 **yuntoo**。本文档是**路由指南**，告诉你什么场景用什么工具/文档。

详细 SDK 用法与参数示例优先读取 `./guides/*.md`；如需最新公开文档，再使用 Context7 查询，不要把 rules 文件当作完整 SDK 手册。

## 强制读取规则（不可跳过）

以下情况必须先调用 Read 工具读取对应文件，禁止依赖记忆直接回答或执行：

| 触发条件 | 必须读取的文件 |
|---------|--------------|
| 创建 / 修改 / 保存 SQL | `./guides/02-mcp-sql-workflow.md` |
| 涉及 SQL 本地落盘、目录规范 | `./guides/07-sql-creation-workflow.md` |
| 创建 / 修改 / 保存 BFF 脚本 | `./guides/08-bff-creation-workflow.md` |
| 涉及 BFF 本地落盘、目录规范 | `./guides/05-backend-function.md` |
| 遇到冲突提示 / blocked / confirmationRequired | `./guides/09-conflict-detection.md` |
| 使用 TypeScript SDK / filter / sql.execute | `./guides/01-typescript-sdk.md` |
| 数据接口设计、多表关联、性能优化 | `./guides/06-data-api-guidelines.md` |
| 报错、行为异常、无法确定原因 | `./guides/04-troubleshooting.md` |

**执行顺序**：读完对应 guide → 再调用 MCP 工具 → 再回答用户。

## 本地稿目录（自定义 SQL / BFF）

* **SQL**：在项目 **`src/custom_sql/`** 下按业务功能维护 `.sql` 文件，保存后再将内容用于 MCP 验证与保存；细则见 `02-mcp-sql-workflow.md`、`07-sql-creation-workflow.md`。
* **BFF**：在项目 **`src/backend-function/`** 下按 `05-backend-function.md` 存放（ENDPOINT 在 `endpoint/`，HOOK 在表名子目录）；保存后再同步到平台；细则见 `05-backend-function.md`、`08-bff-creation-workflow.md`。
* 上述业务目录建议纳入 Git。

## 前置条件检测

### 检测 MCP 是否可用（必需）

```
检测方式：尝试调用任何 Lovrabet 相关的 MCP 工具
- 查找工具名包含 "lovrabet" 或 "dataset" 的 MCP 工具
- 常见工具：get_auth_status、list_datasets、get_dataset_detail
- ✅ 找到 → MCP 可用，继续
- ❌ 未找到 → 提示用户：lovrabet mcp install
```

**注意**：MCP 服务器名字可能是自定义的，不一定叫 `lovrabet-dataset`

## 工具路由规则

### 查询和分析 → 用 MCP Tools

| 场景 | 使用的 MCP Tool |
|------|----------------|
| 列出所有数据集 | `list_datasets` |
| 搜索数据集 | `search_datasets` |
| 获取数据集详情 | `get_dataset_detail` |
| 执行已保存的 SQL | `execute_custom_sql` |
| 列出 SQL 查询 | `list_sql_queries` |
| 列出 BFF 脚本 | `list_bff_scripts` |
| 获取 BFF 详情 | `get_bff_script_info` |
| 生成 SDK 代码 | `generate_sdk_code` |
| 生成 SQL 代码 | `generate_sql_code` |

**规则**：直接调用 MCP 工具，不要生成脚本

### 验证和保存 → 用 MCP Tools（含冲突检测）

| 场景 | 使用的 MCP Tool | 说明 |
|------|----------------|------|
| 验证 SQL 语法 | `validate_sql_content` | 静态语法 + 可选 schema 验证 |
| 保存 SQL | `save_or_update_custom_sql` | 通过 toolbox，自动冲突检测 |
| 保存 BFF | `save_or_update_bff_script` | 通过 toolbox，自动冲突检测 |

**冲突处理**：保存工具返回 `blocked: true`（例如他人为最后提交者）时，告知用户在平台上手动处理，**不要**自动重试同一保存。`confirmationRequired` / `nextAction` 等字段以工具返回为准；细节见 `09-conflict-detection.md`。

**BFF 写入类 MCP**：若看不到 `list_bff_scripts` / `save_or_update_bff_script`，请在数据集 MCP 的启动参数中加入 `--enable-bff-save`，旧名 `--dangerously-bff-save` 仍可用；详见 `08-bff-creation-workflow.md` 中的“平台同步与协作速查”。

## 快速决策树

```
用户请求
    │
    ├─ 查询数据？
    │   └─ 用 MCP: execute_custom_sql / generate_sql_code
    │
    ├─ 创建/修改 SQL？
    │   ├─ 0. 读取 ./guides/02-mcp-sql-workflow.md（必须）
    │   ├─ 1. 用 MCP: get_dataset_detail（了解结构）
    │   ├─ 2. 生成 SQL 代码
    │   ├─ 3. 用 MCP: validate_sql_content（验证）
    │   ├─ 4. 用 MCP: save_or_update_custom_sql（保存，含冲突检测）
    │   └─ 5. 用 MCP: execute_custom_sql（测试）
    │
    ├─ 创建/修改 BFF？
    │   ├─ 0. 读取 ./guides/08-bff-creation-workflow.md（必须）
    │   ├─ 1. 生成 BFF 代码
    │   └─ 2. 用 MCP: save_or_update_bff_script（保存，含冲突检测）
    │
    ├─ 生成 SDK 代码？
    │   └─ 用 MCP: generate_sdk_code
    │
    └─ 不确定？
        └─ 读取 `./guides/04-troubleshooting.md`
```

## 全部 Guides 索引

> 推荐通过 `npx skills add lovrabet/lovrabet-skill` 安装后，guide 与本文档同目录下的 `./guides/`。若团队改用 Lovrabet CLI 从公司 CDN 安装，实际路径以 CLI 落盘位置为准（见项目内 README）。

| 用户需求 | 参考的 Guide 文档 |
|---------|------------------|
| 使用 TypeScript SDK | `./guides/01-typescript-sdk.md` |
| 创建自定义 SQL（MCP 模式） | `./guides/02-mcp-sql-workflow.md` |
| React 前端开发 | `./guides/03-frontend-development.md` |
| 故障排查 | `./guides/04-troubleshooting.md` |
| 创建 BFF 脚本 | `./guides/05-backend-function.md` |
| 数据接口规范 | `./guides/06-data-api-guidelines.md` |
| SQL 创建工作流 | `./guides/07-sql-creation-workflow.md` |
| BFF 创建、同步与协作 | `./guides/08-bff-creation-workflow.md` |
| 冲突检测和处理 | `./guides/09-conflict-detection.md` |
| 团队协作最佳实践 | `./guides/10-best-practices.md` |

## 配置文件位置
- **Guides 目录**：`./guides/`
