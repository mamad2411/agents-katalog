---
name: report-search
description: 收录了主流投研机构发布的研究报告，帮你快速获取专业、深度的分析逻辑、投资评级、目标价等重要投研决策信息。数据来源：同花顺问财。
---

# Report Search — 研究报告搜索

## 技能概述

搜索主流投研机构发布的研究报告，支持按公司名、行业、报告类型、投资评级、目标价等条件查询。

数据来源：**同花顺问财** (https://www.iwencai.com/unifiedwap/chat)

## CLI 使用

```bash
python3 scripts/report_search.py "贵州茅台研报" --size 10
python3 scripts/report_search.py "新能源行业 研报 投资评级" --size 5 --output raw-report-response.json
```

## 环境变量

- `IWENCAI_BASE_URL` — API 基础地址（默认 `https://openapi.iwencai.com`）
- `IWENCAI_API_KEY` — API 密钥（必填，可从 iwencai.com/skillhub 获取）

## API 规范

**端点：** `POST /v1/comprehensive/search`

**请求体：**
```json
{"query": "贵州茅台研报", "channels": ["report"], "app_id": "AIME_SKILL", "size": 10}
```

**Claw Headers：**
| Header | 值 |
|--------|-----|
| Authorization | Bearer {IWENCAI_API_KEY} |
| X-Claw-Skill-Id | report-search |
| X-Claw-Skill-Version | 1.0.0 |
| X-Claw-Trace-Id | 64字符hex（每次新生成） |

## 工作流

1. 确保 `IWENCAI_API_KEY` 已设置
2. 将用户问题转为精准搜索 query（每家公司/行业一条）
3. 调用 `scripts/report_search.py`
4. 解析原始响应，提取标题、机构、发布时间、评级、目标价、核心逻辑
5. 标注数据来源为同花顺问财
