---
name: deepseek-daily-briefing
description: "每日自动推送 DeepSeek API 余额和用量监控简报"
version: 1.0.0
---

# DeepSeek Daily Briefing

每日自动推送 DeepSeek API 余额、花费和 Token 用量监控。使用 `no_agent=true` 模式直接执行 Python 脚本，不消耗 LLM Token。

## 认证

需要两个凭据：

```bash
# ~/.hermes/.env
DEEPSEEK_API_KEY=sk-your_key_here

# ~/.hermes/deepseek_platform_token
# DeepSeek Platform API Token（从 Web 控制台获取）
your_platform_token_here
```

## 可用 API 端点

### 余额查询（API Key 认证）
```
GET https://api.deepseek.com/user/balance
Authorization: Bearer <DEEPSEEK_API_KEY>
```

### 用户总览（Platform Token）
```
GET https://platform.deepseek.com/api/v0/users/get_user_summary
```

### 花费明细（Platform Token）
```
GET https://platform.deepseek.com/api/v0/usage/cost?year=2026&month=06
```

### Token 用量（Platform Token）
```
GET https://platform.deepseek.com/api/v0/usage/amount?year=2026&month=06
```

## 脚本说明

脚本 `deepseek_daily_briefing.py` 执行流程：

1. 读取凭据（`DEEPSEEK_API_KEY` + Platform Token）
2. 调用余额接口获取当前余额
3. 调用用户总览获取本月累计花费和 Token 用量
4. 调用花费明细获取昨日和今日的按模型细分
5. 输出 Markdown 格式报告

## Cron 部署

```bash
cronjob action=create \
  name="DeepSeek 每日用量简报" \
  schedule="0 9 * * *" \
  no_agent=true \
  script="deepseek_daily_briefing.py" \
  workdir="$HOME/.hermes" \
  deliver="feishu"
```

> ⚠️ **script 路径注意事项**：`script` 参数只传文件名（如 `deepseek_daily_briefing.py`），系统会自动在前面补 `scripts/`。不要传 `scripts/foo.py`，否则会变成 `scripts/scripts/foo.py`。
>
> ⚠️ **deliver 注意事项**：显式设置 `deliver` 到目标平台（`feishu`/`telegram` 等），`origin` 默认值可能因会话过期而投递失败。

## 最佳实践

- **使用 Python 标准库**：`no_agent=true` 的 cron 脚本运行在最小环境中，`urllib.request.urlopen()` 比 `subprocess.run(["curl", ...])` 更可靠（curl 可能不在 PATH 中）
- **跨月边界处理**：脚本自动计算昨天和今天的年月参数，不会在月末/月初报错
- **凭据文件管理**：API Key 放在 `.env`，Platform Token 放在独立文件中（便于权限分离）

## 参考

- [DeepSeek API 官方文档](https://api-docs.deepseek.com/zh-cn/)
- [DeepSeek 定价](https://api-docs.deepseek.com/zh-cn/quick_start/pricing/)
