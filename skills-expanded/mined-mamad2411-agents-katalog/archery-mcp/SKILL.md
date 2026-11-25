---
name: archery-mcp
description: Archery SQL审核查询平台 MCP 工具集 - SQL工单提交/审核/执行、在线查询、实例管理
version: 0.1.0
mcp:
  archery:
    command: uvx
    args:
      - archery-mcp-server@latest
    env:
      ARCHERY_BASE_URL: ""
      ARCHERY_USERNAME: ""
      ARCHERY_PASSWORD: ""
---

# Archery MCP Server

将 [Archery](https://github.com/hhyo/Archery) SQL 审核查询平台的 API 封装为 MCP 工具，让 AI Agent 能直接操作 Archery。

## 安装后配置

安装此 skill 后，需要在 MCP 配置中填入实际的 Archery 连接信息：

```json
{
  "mcpServers": {
    "archery": {
      "command": "uvx",
      "args": ["archery-mcp-server@latest"],
      "env": {
        "ARCHERY_BASE_URL": "http://your-archery-host.com",
        "ARCHERY_USERNAME": "your_username",
        "ARCHERY_PASSWORD": "your_password"
      }
    }
  }
}
```

## 何时使用

当用户提到以下关键词时，使用对应工具：

- **SQL上线/工单/DDL变更/DML变更** → 工单管理工具
- **审核SQL/检查SQL/预检** → `sql_check`
- **查数据/SELECT/在线查询** → `sqlquery_execute`
- **实例/数据库连接** → 实例管理工具
- **用户/权限/资源组** → 用户管理工具

## 工具清单（26个）

### SQL 工单管理

| 工具 | 触发词 | 说明 |
|------|--------|------|
| `workflow_list` | 查看工单、工单列表 | 获取工单列表（支持状态/实例/提交人过滤） |
| `workflow_submit` | 提交工单、上线SQL | 提交 SQL 上线工单 |
| `workflow_audit` | 审核工单、通过、驳回 | 审核操作（pass/cancel） |
| `workflow_execute` | 执行工单 | 执行已审核通过的工单 |
| `workflow_pending_list` | 待审核、待办 | 查看待审核工单 |
| `workflow_log` | 工单日志 | 查看工单流转日志 |

### SQL 审核

| 工具 | 触发词 | 说明 |
|------|--------|------|
| `sql_check` | 检查SQL、审核SQL、预检 | 语法审核（不执行） |

### SQL 查询

| 工具 | 触发词 | 说明 |
|------|--------|------|
| `sqlquery_instances` | 可查询的实例 | 获取用户可访问的查询实例 |
| `sqlquery_resources` | 看库、看表、看字段 | 浏览实例下的资源 |
| `sqlquery_describe_table` | 表结构、DESC | 获取表结构详情 |
| `sqlquery_execute` | 查数据、SELECT | 执行 SELECT 查询 |
| `sqlquery_logs` | 查询历史 | 获取查询日志 |
| `sqlquery_favorite` | 收藏查询 | 收藏/取消收藏 |

### 实例管理

| 工具 | 触发词 | 说明 |
|------|--------|------|
| `instance_list` | 实例列表 | 获取实例列表 |
| `instance_create` | 添加实例 | 创建实例配置 |
| `instance_update` | 修改实例 | 更新实例信息 |
| `instance_delete` | 删除实例 | 删除实例 |
| `instance_resource` | 实例下的库/表 | 获取实例内资源 |
| `instance_table_lookup` | 找表、表在哪 | 按表名反查实例 |

### 用户管理

| 工具 | 触发词 | 说明 |
|------|--------|------|
| `user_list` | 用户列表 | 获取用户列表 |
| `user_create` | 创建用户 | 创建新用户 |
| `user_update` | 修改用户 | 更新用户 |
| `user_delete` | 删除用户 | 删除用户 |

### 资源组 & 权限组

| 工具 | 触发词 | 说明 |
|------|--------|------|
| `resource_group_list` | 资源组列表 | 获取资源组 |
| `resource_group_create` | 创建资源组 | 创建资源组 |
| `auth_group_list` | 权限组列表 | 获取权限组 |
| `auth_group_create` | 创建权限组 | 创建权限组 |

## 常见操作流程

### 提交并审核 SQL 上线

```
1. instance_list          → 确认目标实例
2. instance_resource      → 确认数据库名
3. sql_check              → 预检 SQL
4. resource_group_list    → 确认资源组
5. workflow_submit        → 提交工单
6. workflow_audit         → 审核通过
7. workflow_execute       → 执行
```

### 在线查询数据

```
1. sqlquery_instances     → 获取可查询实例
2. sqlquery_resources     → 浏览库/表
3. sqlquery_execute       → 执行查询
```

### 处理待审核工单

```
1. workflow_pending_list  → 获取待办
2. workflow_audit         → 通过或驳回
```

## 暂未覆盖的功能

以下功能需通过 Archery Web 页面操作：
- 数据导出工单、数据字典、查询权限申请
- SQL优化（SOAR/SQLAdvisor）、慢查日志
- 会话管理、数据库账号管理、参数配置
- 数据归档、My2SQL、SchemaSync
- 系统配置、审计日志
