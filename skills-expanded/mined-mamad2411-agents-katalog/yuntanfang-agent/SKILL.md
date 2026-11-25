---
name: yuntanfang-agent
description: 云摊坊系统 Agent 总 skill。用于理解用户自然语言请求，选择可执行功能 API，返回可确认的前端 action，并提供系统功能导航帮助。
---

# 云摊坊 Agent Skill

## 目标

Agent 帮助普通用户更快掌握和使用云摊坊：

- 直接执行操作：找摊位、创建预约订单、提交评价、提交投诉。
- 辅助使用系统：解释功能入口、说明可以做什么、引导用户到正确页面。
- 保持可审计：模型只做意图识别和参数抽取，后端只执行白名单 action。

## 当前统一入口

`POST /api/agent/chat`

请求：

```json
{
  "message": "帮我找附近的糖画摊",
  "history": ["assistant: 你可以问我入口在哪"],
  "context": {
    "currentRoute": "/agent-order",
    "role": "consumer"
  }
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "reply": "已帮你找到 1 个相关摊位，可以点卡片查看详情或继续让我筛选。",
    "intent": "search_stalls",
    "action": {
      "type": "open_route",
      "label": "查看摊位列表",
      "route": "/stalls",
      "payload": {
        "keyword": "糖画",
        "category": "非遗好物"
      }
    },
    "cards": [],
    "processSteps": [
      {
        "title": "识别用户意图",
        "status": "completed",
        "detail": "search_stalls"
      }
    ],
    "suggestedPrompts": ["帮我找附近摊位", "帮我预约一份晚餐"],
    "status": "deepseek",
    "rawModelOutput": "{}"
  }
}
```

## 白名单意图

| Intent | 小 skill | 作用 |
| --- | --- | --- |
| `search_stalls` | `skills/search-stalls.md` | 搜索摊位、分类筛选、推荐附近摊位 |
| `create_order` | `skills/create-order.md` | 从自然语言生成预约订单草稿 |
| `submit_review` | `skills/submit-review.md` | 根据订单和内容提交评价 |
| `submit_complaint` | `skills/submit-complaint.md` | 生成投诉工单 |
| `system_help` | `skills/system-help.md` | 解释系统能力和功能入口 |

## 后端执行规则

1. 使用 DeepSeek 只输出 JSON 决策：

```json
{
  "intent": "create_order",
  "parameters": {
    "stallName": "烟火小摊",
    "productName": "招牌烤串(10串)",
    "quantity": 2,
    "pickupTime": "今天 18:30",
    "contact": ""
  }
}
```

2. 后端校验 intent，只接受白名单。
3. 后端按小 skill 的必需参数规则校验。参数不足时返回 `ask_clarification`，不要调用功能 API。
4. 后端将 API 返回的结果加工成用户可读的 `reply`，同时保留结构化 `cards`。
5. 前端只执行后端返回的 action，不执行模型原始文本。
6. DeepSeek 或功能 API 调用失败时最多重试 3 次；超过 3 次返回 `unavailable`。

## 参数来源规则

- 只能使用用户当前消息、历史中用户明确确认过的信息、真实接口返回的数据。
- 禁止模型为了调用 API 自己补商品、摊位、订单、投诉对象、评分、问题类型。
- 后端允许的系统默认值必须写在小 skill 中；未列出的字段都不能默认补齐。
- 必需参数不足时必须返回 `ask_clarification`，且不调用功能 API。
- 用户纠正前文时，以最新消息为准，清空被纠正的参数。

## 必需参数规则

- `search_stalls` 至少需要 `keyword` 或 `category`；“附近摊位”“帮我找摊位”这类泛化表达必须追问。
- `create_order` 必须有用户明确说出的 `productName`；只有 `stallName` 或“我想预约”时必须追问商品，不能按摊位默认补商品。
- `submit_review` 必须有具体订单号，且必须有明确评分信号（数字星级，或好评/中评/差评/一般等）。
- `submit_complaint` 必须有 `target`，且必须有 `type` 或 `description`。
- `system_help` 可直接响应，不要求必需参数。

## 系统默认值

| Intent | 字段 | 默认值 | 条件 |
| --- | --- | --- | --- |
| `create_order` | `quantity` | `1` | 用户未说数量 |
| `create_order` | `pickupTime` | `今天 19:00` | 用户未说取货时间 |
| `create_order` | `vendorId`/`stallId`/`stallName`/`price` | 从真实商品和摊位表反查 | 用户明确商品但未说摊位 |
| `submit_review` | `rating` | `5/3/1` | 用户明确说好评/中评或一般/差评 |
| `submit_review` | `content` | 按评分生成匹配文案 | 用户只给评分或好评/中评/差评 |
| `submit_complaint` | `type` | `其他问题` | 用户给了对象和描述但未说类型 |

默认值是后端规则，不是模型规则。模型输出不得为了匹配这些默认值而编造参数。

参数不足响应：

```json
{
  "intent": "search_stalls",
  "action": {
    "type": "ask_clarification",
    "label": "补充信息",
    "route": "",
    "payload": {}
  },
  "reply": "你想找哪类摊位？可以说地方特色、农家特产、非遗好物，或告诉我具体商品/位置。"
}
```

## 前端执行规则

- `open_route`：跳转到 `action.route`。
- `create_order`：用 `action.payload.orderPayload` 调用 `POST /api/orders`，成功后跳转真实订单详情。
- `submit_review`：用 `action.payload.orderId/rating/content` 调用 `POST /api/orders/{id}/reviews`，成功后跳转 `/my-reviews`。
- `submit_complaint`：用 `action.payload.vendorId/orderId/type/description` 调用 `POST /api/complaints`，成功后跳转 `/complaints`。

## 待开发

见 `TODO.md`。
