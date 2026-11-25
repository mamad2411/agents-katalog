---
name: aliyun-supabase-mcp-helper
description: 阿里云Supabase MCP服务器连接指南 - 用于查询和管理阿里云上的Supabase数据库
---

# 阿里云 Supabase MCP 连接指南

## 前置检查

在使用此 skill 前，先检查 MCP 工具是否可用：

```
尝试调用 ToolSearch 搜索 "aliyun-supabase"
```

**如果搜索结果为空或调用失败**，提示用户配置 MCP 服务器：

> 未检测到阿里云 Supabase MCP 服务器。请先在 Agent 对应的配置文件中添加 MCP 配置，官方配置说明文档：https://help.aliyun.com/zh/analyticdb/analyticdb-for-postgresql/supabase-mcp-user-guide
>
> ```json
> {
>   "mcpServers": {
>     "<自定义名称，如 aliyun-supabase>": {
>       "args": [
>         "-y",
>         "@aliyun-supabase/mcp-server-supabase@latest",
>         "--features=aliyun",
>         "--read-only",
>         "--project-id=<你的项目ID>",
>         "--region-id=<区域ID，如 cn-shenzhen>"
>       ],
>       "command": "npx",
>       "enabled": true,
>       "env": {
>         "ALIYUN_ACCESS_TOKEN": "<你的阿里云Access Token>"
>       },
>       "type": "stdio"
>     }
>   }
> }
> ```
>
> 配置说明：
> - `mcpServers` 的 key 是自定义名称，可随意命名
> - `project-id`: 阿里云 Supabase 项目 ID，可在控制台获取
> - `region-id`: 项目所在区域，如 `cn-shenzhen`、`cn-hangzhou`
> - `ALIYUN_ACCESS_TOKEN`: 阿里云访问令牌，格式为 `AccessKeyId|AccessKeySecret`

## 获取项目信息

调用以下工具获取当前MCP连接的项目列表：

```
mcp__aliyun-supabase__list_aliyun_supabase_projects
```

> 注意：工具名称中的 `aliyun-supabase` 取决于你在 `mcpServers` 中配置的 key 名称。如果配置为 `my-db`，则工具名称变为 `mcp__my-db__list_aliyun_supabase_projects`

从返回结果中提取：
- **projectId** - 项目ID
- **projectName** - 项目名称
- **publicConnectUrl** - 公开连接地址
- **regionId** - 区域

## 获取连接参数

### 步骤1: 获取API密钥

使用 `get_supabase_project_api_keys` 工具（无需参数）：

```
mcp__<你的MCP名称>__get_supabase_project_api_keys
```

返回结果中获取 `serviceRoleKey`：
```json
{
  "apiKeys": [
    {
      "apiKey": "jwt_token_here",
      "name": "serviceRoleKey"
    }
  ]
}
```

### 步骤2: 构建连接参数

- **url**: `https://{publicConnectUrl}` （从项目信息获取）
- **api_key**: 上一步获取的 `serviceRoleKey`

## 常用操作

### 查询表列表

```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
```

### 查询特定前缀的表

```sql
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'czwu%' 
ORDER BY table_name;
```

### 查看表结构

```sql
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name = 'your_table_name'
ORDER BY ordinal_position;
```

### 查询数据

```sql
SELECT * FROM public.your_table_name LIMIT 100;
```

## MCP工具分类

### 需要url和api_key参数的工具
- `execute_sql` - 执行SQL查询
- `list_table` - 列出表
- `list_columns` - 列出列
- `list_indexes` - 列出索引
- `list_extensions` - 列出扩展

### 仅需要project_id的工具（或无参数）
- `list_aliyun_supabase_projects` - 列出所有项目
- `get_supabase_project` - 获取项目详情
- `get_supabase_project_api_keys` - 获取API密钥
- `describe_regions` - 列出可用区域
- `describe_rds_vpcs` - 列出VPC

### 存储相关工具
- `list_storage_buckets` - 列出存储桶
- `list_storage_files` - 列出文件
- `upload_storage_file` - 上传文件
- `download_storage_file` - 下载文件
- `delete_storage_file` - 删除文件

### 认证相关工具
- `list_auth_users` - 列出用户
- `create_auth_user` - 创建用户
- `update_auth_user` - 更新用户
- `delete_auth_user` - 删除用户

### Edge Functions工具
- `list_edge_functions` - 列出函数
- `deploy_edge_function` - 部署函数
- `invoke_edge_function` - 调用函数
- `delete_edge_function` - 删除函数

## 注意事项

1. **只读模式**: 当前MCP配置为只读模式（`--read-only`），无法执行写操作
2. **Token有效期**: API密钥有有效期，过期后需要重新获取
3. **连接失败**: 如果遇到 `fetch failed` 错误，检查是否提供了正确的url和api_key参数
4. **工具命名**: MCP工具名称格式为 `mcp__<MCP名称>__<工具名>`，MCP名称取决于配置
