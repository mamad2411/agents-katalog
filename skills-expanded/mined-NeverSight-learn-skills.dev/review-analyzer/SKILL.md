---
name: review-analyzer
description: >
  对用户评论/反馈数据进行批量智能分析：语言检测、翻译、质量评估、话题分类（预定义+自动发现）、
  情感分析、阻断性问题检测、自定义标签打标，并生成结构化 JSON 结果和汇总报告。
  当用户需要分析评论、理解用户反馈、做舆情分析、检测玩家问题时使用此 Skill。
  即使用户只是说"帮我看看这些评论都在说什么"，也应该触发此 Skill。
---

# Review Analyzer

对评论/反馈数据进行批量智能分析，输出结构化的逐条分析结果和整体汇总报告。

## 适用场景

- 分析采集 Skill（App Store / Google Play / Gmail）输出的 CSV 文件
- 分析任何包含用户评论/反馈的 CSV 或文本数据
- 定期分析新增评论，生成趋势报告

## 工作流程

### 1. 读取数据

读取用户指定的 CSV 文件。CSV 至少需要一个包含评论文本的列。自动识别以下常见列名：
- 评论内容：`content`、`Content`、`review`、`message`、`text`、`body`
- 评论 ID：`review_id`、`message_id`、`id`
- 作者：`author`、`sender`、`user`、`userName`
- 日期：`date`、`Date`、`timestamp`
- 评分：`rating`、`score`
- 平台：`platform`、`country`、`source`

如果列名不匹配，提示用户指定哪一列是评论内容。

### 2. 确认分析配置

向用户确认（有合理默认值，用户可以直接跳过）：

- 目标翻译语言：默认中文（`zh`）。如果评论本身就是目标语言，跳过翻译
- 预定义话题列表：用户可以提供（如 `["游戏玩法", "付费系统", "技术问题", "客服体验"]`），也可以不提供让 LLM 自动发现
- 自定义标签：用户可以定义额外的标签维度（如 `{"churn_risk": "评估用户流失风险", "feature_request": "是否包含功能请求"}`）
- 业务背景：可选的一段文字，帮助 LLM 理解分析的上下文（如"这是一款二次元手游，最近刚做了抽卡系统改版"）

### 3. 批量分析

将评论分批喂给 LLM 进行分析。每批的大小取决于评论长度——目标是尽量多塞，但要给输出留足空间。经验法则：

- 短评论（平均 < 100 字）：每批 30-50 条
- 中等评论（100-300 字）：每批 15-25 条
- 长评论（> 300 字）：每批 5-10 条

对每批评论，用一次 LLM 调用完成所有分析任务。这比逐条调用高效得多，因为 LLM 能在批次内建立上下文理解（比如发现多条评论在说同一个问题）。

#### 分析 Prompt 结构

使用以下 prompt 模板。根据用户的配置调整 `{predefined_topics}`、`{custom_tags}`、`{business_context}` 部分。如果用户没有提供某项配置，省略对应的 XML 块。

```xml
<system>
你是一位专业的用户反馈分析师。你的任务是对一批用户评论进行多维度分析。

对每条评论，你需要完成以下分析：

1. 语言检测：识别评论的原始语言（ISO 639-1 代码，如 en、zh、ja、ko）

2. 翻译：如果评论不是{target_language}，翻译为{target_language}。保持原意和语气。如果已经是目标语言，原样保留。

3. 内容质量评估：判断评论是否有分析价值
   - high：包含具体反馈、问题描述、建议或有实质内容的观点
   - medium：有一定信息量但比较笼统（如"游戏不错"、"体验一般"）
   - low：无意义内容（纯 emoji、广告、乱码、无关闲聊、单字回复如"ok"）

4. 话题分类：将评论归入一个话题
   {predefined_topics_block}
   如果评论不属于任何预定义话题，创建一个新话题，名称要简洁且有描述性（如"抽卡概率争议"、"新角色平衡性"）

5. 情感分析：
   - 基础情感：positive / negative / neutral
   - 细粒度情感（选一个最贴切的）：delighted / satisfied / hopeful / neutral / confused / disappointed / frustrated / angry

6. 阻断性问题检测：判断是否为阻断性问题（阻止用户正常使用产品的严重问题）
   阻断性问题的标准：
   - 无法登录或认证失败
   - 完全无法访问产品/游戏
   - 支付/充值交易异常
   - 更新后产品完全崩溃无法使用
   - 账号被误封或数据丢失
   
   以下不算阻断性问题（即使用户很不满）：
   - 普通 bug 或小故障
   - 性能抱怨但不影响使用
   - 内容/玩法不满意
   - 功能建议

   {custom_tags_block}

{business_context_block}

输出格式：对每条评论输出一个 JSON 对象，所有评论的结果放在一个 JSON 数组中。

每条评论的 JSON 结构：
{
  "index": 评论在本批次中的序号（从1开始）,
  "language": "ISO 639-1 语言代码",
  "translated": "翻译后的文本（如果不需要翻译则为空字符串）",
  "quality": "high/medium/low",
  "topic": "话题名称",
  "is_new_topic": true/false,
  "sentiment": "positive/negative/neutral",
  "sentiment_detail": "细粒度情感",
  "is_blocking": true/false,
  "blocking_type": "login/crash/payment/ban/data_loss/none",
  "tags": { 自定义标签的键值对 },
  "reasoning": "一句话解释你的判断依据（中文）"
}

直接输出 JSON 数组，不要包裹在 markdown 代码块中。
</system>
```

其中可选块的模板：

```xml
<!-- 预定义话题块（如果用户提供了话题列表） -->
预定义话题列表：{topics_list}
优先将评论归入这些预定义话题。只有当评论确实不属于任何预定义话题时，才创建新话题。

<!-- 自定义标签块（如果用户定义了额外标签） -->
7. 自定义标签：
{custom_tags_description}
在 tags 字段中输出每个自定义标签的值。

<!-- 业务背景块（如果用户提供了背景信息） -->
业务背景（帮助你更好地理解评论的上下文）：
{business_context}
```

User prompt 模板：

```
请分析以下 {count} 条用户评论：

{reviews_xml}
```

其中 `{reviews_xml}` 格式为：

```xml
<review index="1">{content_1}</review>
<review index="2">{content_2}</review>
...
```

### 4. 解析输出并保存

将 LLM 返回的 JSON 数组解析后，与原始 CSV 数据合并，保存为新的 JSON 文件。

输出文件结构：

```json
{
  "metadata": {
    "source_file": "原始 CSV 文件路径",
    "total_reviews": 500,
    "analyzed_at": "2026-04-10T12:00:00Z",
    "config": {
      "target_language": "zh",
      "predefined_topics": ["..."],
      "custom_tags": {},
      "business_context": "..."
    }
  },
  "reviews": [
    {
      "review_id": "原始 ID",
      "author": "原始作者",
      "date": "原始日期",
      "rating": 5,
      "original_content": "原始评论文本",
      "language": "en",
      "translated": "翻译后的文本",
      "quality": "high",
      "topic": "Gacha System",
      "is_new_topic": false,
      "sentiment": "negative",
      "sentiment_detail": "frustrated",
      "is_blocking": false,
      "blocking_type": "none",
      "tags": {},
      "reasoning": "..."
    }
  ],
  "summary": { ... }
}
```

### 5. 生成汇总报告

在所有评论分析完成后，对结果做一次汇总分析。可以再做一次 LLM 调用，把统计数据喂给它生成自然语言报告，也可以用代码直接统计。

汇总内容包括：

```json
{
  "summary": {
    "quality_distribution": {"high": 320, "medium": 130, "low": 50},
    "sentiment_distribution": {"positive": 150, "negative": 250, "neutral": 100},
    "top_topics": [
      {"name": "抽卡概率", "count": 85, "sentiment_breakdown": {"positive": 5, "negative": 72, "neutral": 8}},
      {"name": "游戏性能", "count": 60, "sentiment_breakdown": {...}}
    ],
    "new_topics_discovered": ["新角色平衡性", "社交系统改进"],
    "blocking_issues": [
      {"type": "payment", "count": 12, "example_reviews": ["review_id_1", "review_id_2"]},
      {"type": "login", "count": 8, "example_reviews": ["review_id_3"]}
    ],
    "key_insights": "由 LLM 生成的 3-5 条关键洞察",
    "recommendations": "由 LLM 生成的 2-3 条可执行建议"
  }
}
```

### 6. 报告结果

向用户汇报：
- 分析了多少条评论
- 质量分布（多少条高/中/低质量）
- 情感分布概览
- 排名前 5 的话题及其情感倾向
- 发现的阻断性问题（如果有）
- 关键洞察和建议
- 输出文件的保存路径

## 输出文件

- `{source_name}_analysis.json`：完整的逐条分析结果 + 汇总
- 保存在与输入 CSV 同目录下，或用户指定的目录

## 注意事项

- 批量处理时注意 LLM 的上下文窗口限制。如果单批评论太长导致输出被截断，减小批次大小重试
- 如果 LLM 返回的 JSON 格式有误，尝试修复（常见问题：多余逗号、缺少引号）。如果修复失败，对该批次降级为逐条处理
- quality 为 low 的评论仍然会被分析（打标），但在汇总报告中会标注有多少低质量评论被包含
- 自动发现的新话题名称应该简洁（5-10 个字），避免过长的描述性名称
