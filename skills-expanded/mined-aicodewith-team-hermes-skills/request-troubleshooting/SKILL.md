---
name: request-troubleshooting
description: >-
  Generic API request troubleshooting methodology — diagnose failures by
  request_id, user_id, or email. Analyze log chains, identify common
  failure patterns (rate limits, auth, timeouts, model config), and
  produce actionable reports with user-facing talking points.
triggers:
  - request_id with req_ prefix
  - user_id with user_ prefix
  - user asks to troubleshoot a request failure or anomaly
  - email-based user lookup for troubleshooting
---

# API 请求异常排查（通用方法论）

## 触发条件

用户提供 `request_id`（`req_` 前缀）或 `user_id`（`user_` 前缀），要求排查请求失败、卡顿或异常。

## 前置：确认日志系统接入

本 skill 假设项目已接入集中式日志系统。使用前确认：
- 日志查询工具名（MCP tool / CLI / API）
- 日志索引/logstore 名称
- 默认时间范围

如果项目尚未接入，先用项目现有手段（`journalctl`、`docker logs`、应用日志文件）替代。

## 排查步骤

### 1. 获取请求信息

**按 request_id 排查**（`req_` 前缀）：

直接查询日志系统中的完整请求链路：

```
query: "* and <request_id>"
limit: 50
```

**按 user_id 排查**（`user_` 前缀）：

先获取该用户最近请求列表，从结果中找到失败的 request_id，再查日志。

**按 email 排查**：

通过 email 反查 user_id，然后按 user_id 流程继续。

**查不到结果时**：扩大时间范围重试。如果 request_id 完全不存在于日志中，说明请求未到达服务端 — 通常是客户端侧问题（如模型 ID 拼写错误、本地校验失败、API 格式不匹配）。

### 2. 日志链路分析（按时间排序）

从原始日志中提取以下关键节点：

| # | 典型关键字 | 提取信息 |
|---|-----------|---------|
| 1 | `incoming request` / `request received` | method, path |
| 2 | `auth success` / `authenticated` | user_id, email |
| 3 | `model detected` / `routing to` | model, backend |
| 4 | `context size` / `token estimate` | body_bytes, estimated_tokens |
| 5 | `channel resolved` / `route selected` | channel_count, candidates |
| 6 | `trying upstream` / `attempt` | attempt number, priority |
| 7 | `upstream request` / `proxy to` | upstream_url, mapped_model |
| 8 | `upstream error` / `backend response` | **status, error_body（根因在这里）** |
| 9 | `failover` / `retry triggered` | category, trigger |
| 10 | `request completed` / `all failed` | final status |

### 3. 常见故障模式

| 上游错误 | 根因 | 解决方向 |
|---------|------|---------|
| `model_not_found` | 上游未配置该模型 | 去上游后台添加模型映射 |
| 429 `rate_limit` | 上游限流 | 增加配额或调整权重 |
| 401 `authentication` | API key 无效 | 检查凭证配置 |
| 422 `invalid_request` | 请求体过大/格式错 | 检查 body_bytes |
| `timeout` / `network` | 网络问题 | 检查上游 URL 可达性 |
| `no_available_channels` | 用户无可用路由 | 检查用户权限和白名单 |
| `circuit breaker open` | 渠道被熔断 | 检查该渠道近期错误率 |

### 4. 日志查询注意事项

- **关键词误匹配**：搜索 `model_not_found`、`upstream error` 等关键词可能匹配到其他日志（如审计日志中的用户对话历史），而非真正的代理错误。务必按 request_id 过滤出完整链路再做判断。
- **request_id 完全缺失**：如果 request_id 在日志中完全查不到，说明请求根本没到达服务端。排查客户端侧：模型 ID 拼写、本地校验、API 格式。
- **时间窗口**：分布式系统中各节点时钟可能不同步，扩大 ±5 分钟窗口避免漏掉日志。

### 5. 查数据库辅助（可选）

如果项目有请求日志表：

```sql
-- 用户信息
SELECT id, email, status, created_at FROM users WHERE id = '<user_id>';

-- 请求记录
SELECT request_id, backend, status, error_type, latency_ms, created_at
FROM request_log WHERE request_id = '<request_id>';

-- 用户路由配置
SELECT * FROM user_routing WHERE user_id = '<user_id>' AND enabled = true;
```

### 6. 输出格式

用中文输出三段：

1. **请求链路** — 时间线列出关键节点
2. **根因** — 一句话指出问题所在
3. **建议处理方式** — 含可回复用户的话术
