---
name: model-stats
description: 查询 tiny-llm-proxy 网关上的模型调用统计信息（调用次数、Token 消耗、按模型/时间/协议维度聚合等）。当用户需要查看网关模型调用统计、用量排行、消费趋势时说"查一下模型用量"、"统计一下网关数据"、"看看各模型调用量"、"模型调用排行"时触发。
---

# Model Stats

查询 tiny-llm-proxy 网关上的模型调用统计信息，支持按模型、时间窗口、协议维度聚合。

## Quick Reference

| 任务             | 命令                                                                                 |
| ---------------- | ------------------------------------------------------------------------------------ |
| 查询今日用量概览 | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts`                                     |
| 按模型聚合       | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --group-by model`                    |
| 按日期聚合       | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --group-by day`                      |
| 按协议聚合       | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --group-by protocol`                 |
| 指定时间范围     | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --start 2025-05-01 --end 2025-05-03` |
| 过滤特定 Key     | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --key-name pi`                       |
| 过滤特定模型     | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --model gpt-4o`                      |
| 过滤特定协议     | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --protocol openai`                   |
| JSON 格式输出    | `bun ${CLAUDE_SKILL_DIR}/scripts/query-stats.ts --json`                              |

## 参数说明

| 参数         | 说明                                   | 默认值                               |
| ------------ | -------------------------------------- | ------------------------------------ |
| `--start`    | 开始日期（YYYY-MM-DD）                 | 当天                                 |
| `--end`      | 结束日期（YYYY-MM-DD）                 | 当天                                 |
| `--group-by` | 聚合维度：`model` / `day` / `protocol` | `model`                              |
| `--json`     | JSON 格式输出原始数据                  | -                                    |
| `--url`      | 网关地址                               | `https://new.fortao.cn`              |
| `--key`      | API Key（需 admin 权限）               | 从环境变量 `TINY_LLM_PROXY_KEY` 读取 |
| `--key-name` | 按 API Key 名称过滤                    | -                                    |
| `--model`    | 按模型名称过滤                         | -                                    |
| `--protocol` | 按协议过滤：`openai` / `anthropic`     | -                                    |

## 返回结果

### 表格输出（默认）

- **Breakdown** — 按 `--group-by` 维度聚合的明细列表，包含各维度下的请求数、输入/输出 Token 及占比
- **Summary** — 总计：总调用次数、总输入 Token、总输出 Token、总 Token

示例：

```
Stats: 2026-05-01 ~ 2026-05-04
  Group by: model

Model                          │ Requests │ Prompt Tokens │ Completion Tokens │ Prompt% │ Comp%
───────────────────────────────┼──────────┼───────────────┼───────────────────┼─────────┼───────
glm-5.1                        │      136 │     1,061,875 │            51,538 │  100.0% │ 100.0%

────────────────────────────────────────────────────────────
Summary
────────────────────────────────────────────────────────────
Total Requests:       136
Total Prompt:         1,061,875 tokens
Total Completion:     51,538 tokens
Total Tokens:         1,113,413 tokens
```

### JSON 输出（`--json`）

```json
{
  "data": [
    {
      "date": "2026-05-04",
      "key_name": "pi",
      "model": "glm-5.1",
      "protocol": "anthropic",
      "prompt_tokens": 806784,
      "completion_tokens": 20521,
      "request_count": 64
    }
  ],
  "summary": {
    "prompt_tokens": 1061875,
    "completion_tokens": 51538,
    "request_count": 136
  }
}
```

## 接口说明

脚本调用网关的 `GET /v1/stats` 端点，该端点要求调用者使用 **admin 角色** 的 API Key。

服务端响应原始行数据（按 `date + key_name + model + protocol` 联合主键聚合），脚本在客户端按 `--group-by` 维度进行二次聚合后展示。

## 错误处理

| 错误信息                        | 原因                  | 解决方案                               |
| ------------------------------- | --------------------- | -------------------------------------- |
| `TINY_LLM_PROXY_KEY is not set` | 未设置 API Key        | `export TINY_LLM_PROXY_KEY="your-key"` |
| `HTTP Error 401`                | API Key 无效          | 检查环境变量或 `--key` 参数            |
| `HTTP Error 403`                | API Key 非 admin 角色 | 使用具有 admin 角色的 Key              |
| `HTTP Error 404`                | 统计接口不存在        | 确认网关版本是否支持统计查询           |
| `Connection error`              | 服务未启动或网络问题  | 检查网络，确认网关可达                 |
