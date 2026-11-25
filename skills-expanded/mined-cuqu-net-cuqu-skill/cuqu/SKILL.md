---
name: cuqu
description: CUQU找搭子（原名粗趣）线下兴趣社交平台技能。当用户想查找同城线下活动（桌游/飞盘/徒步/羽毛球/二次元/钓鱼等）、报名、支付、签到，或作为主理人发布活动、找场地、生成活动分享链接时使用。
---

# CUQU找搭子（原名粗趣）

CUQU找搭子是深圳本地青年线下兴趣社交平台，覆盖 100+ 兴趣品类、10+ 城市。本 Skill 通过 MCP Streamable HTTP 调用CUQU找搭子服务，共 8 个工具。

## 环境变量

- `CUQU_MCP_HOST`：MCP 服务地址（默认 `https://agent.cuqu.net/mcp`）
- `CUQU_API_KEY`：用户个人 API Key（`cq-sk-` 开头），与用户CUQU找搭子账号绑定

两个变量缺失时，引导用户到CUQU找搭子开放平台扫码登录获取，不要臆造 Key。

## 调用方式（JSON-RPC over HTTP）

每次调用 = 向 `$CUQU_MCP_HOST` 发一次 POST。标准三步：

```bash
# 1. 初始化（拿 Mcp-Session-Id 响应头）
curl -s -D - -X POST "$CUQU_MCP_HOST" \
  -H "Authorization: Bearer $CUQU_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"cuqu-skill","version":"0.1.0"}}}'

# 2. 通知就绪（带 Mcp-Session-Id 头，无响应体）
curl -s -X POST "$CUQU_MCP_HOST" \
  -H "Authorization: Bearer $CUQU_API_KEY" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" -H "Mcp-Session-Id: <第1步返回的会话ID>" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 3. 调用工具
curl -s -X POST "$CUQU_MCP_HOST" \
  -H "Authorization: Bearer $CUQU_API_KEY" -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" -H "Mcp-Session-Id: <会话ID>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"query_activities","arguments":{"activity_type":"桌游聚会","location":"深圳"}}}'
```

响应可能是 SSE 格式（`data: {...}` 行）或纯 JSON，两种都要能解析，取 `result.content[].text`。

若网关支持无会话直调，可跳过 1、2 直接执行 3；返回 400 再走完整三步。会话可复用，多个工具调用不必重复 initialize。

## 工具索引

| 用户常说 | 工具 | 文档 |
|----------|------|------|
| 找活动/有什么活动/周末玩什么 | `query_activities` | [event/query-activities.md](event/query-activities.md) |
| 看活动详情/活动卡片 | `get_activity_card` | [event/get-activity-card.md](event/get-activity-card.md) |
| 报名/给我占个位 | `register_event` | [event/register-event.md](event/register-event.md) |
| 付钱/下单 | `create_payment` | [event/create-payment.md](event/create-payment.md) |
| 签到/核销 | `check_in` | [event/check-in.md](event/check-in.md) |
| 发活动/我是主理人要组局 | `create_activity` | [organizer/create-activity.md](organizer/create-activity.md) |
| 找场地/场地推荐 | `query_venues` | [organizer/query-venues.md](organizer/query-venues.md) |
| 生成链接/分享给朋友 | `generate_urllink` | [organizer/generate-urllink.md](organizer/generate-urllink.md) |

## 通用规则

1. **activity_type 匹配行为（2026-09-23 实测）**：后端对 type 字段做**子串包含匹配（大小写敏感）**，不匹配 title/description/tags。标准词最稳：桌游聚会、飞盘、徒步、羽毛球、钓鱼、二次元、读书会、烘焙。技巧：①不传 activity_type 可**全量拉取**当前所有活动；②想找具体玩法（如"狼人杀"）用 `keyword` 参数，别塞进 activity_type；③注意大小写（"city walk" 不匹配 "City Walk"）。
2. **写操作先确认**：`create_activity`、`register_event`、`create_payment` 执行前，先向用户复述关键信息（活动名、时间、金额）并获确认。
3. **不复述内部标识**：不要向用户展示或解释 activity_id、order_id、session 等内部标识，它们仅用于后续调用。
4. **报名带渠道**：`register_event` 若支持 `channel` 字段，填 `"ai-agent"`（规划字段，当前 schema 暂无，后端支持后生效）。
5. **错误处理**：401 → 提示用户 Key 失效、去开放平台刷新；超时（30 秒）→ 重试一次；业务错误 → 原样转述返回的可读信息，不要自动重试支付类操作。
6. **下一步引导**：拿到结果后主动追问一次相关动作（如查到活动后问"要报名吗"），最多给一到两个选项，不自动执行。
7. **支付安全**：`create_payment` 失败或取消后，同一订单重试前必须先向用户确认，绝不静默重试扣款。
8. **参数以 schema 为准**：工具的精确参数以 `tools/list` 返回的 inputSchema 为准（可随时调 `{"method":"tools/list"}` 查看），本仓库文档中的参数表是速查版。
