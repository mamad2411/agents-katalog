---
name: hithink-astock-selector
description: 通过自然语言查询进行A股股票筛选，支持行情指标、技术形态、财务指标、行业概念等多条件组合筛选。返回符合条件的相关股票数据。数据来源：同花顺问财。
---

# 问财选A股 — hithink-astock-selector

## 技能概述

通过自然语言查询进行 A 股智能筛选：
- 行情指标筛选（股价、涨跌幅、成交量等）
- 技术形态筛选（均线多头、突破新高、K线形态等）
- 财务指标筛选（营收、利润、PE、PB 等）
- 行业概念筛选（科技、医药、消费等）
- 多条件组合筛选

数据来源：**同花顺问财** (https://www.iwencai.com/unifiedwap/chat)

## CLI 使用

```bash
python3 scripts/cli.py --query "今日涨跌幅超过5%的A股有哪些？"
python3 scripts/cli.py --query "科技股有哪些" --page "1" --limit "20"
python3 scripts/cli.py --query "银行股" --api-key "your-key"
python3 scripts/cli.py --query "银行股" --call-type "retry"
```

## 环境变量

需要 `IWENCAI_API_KEY` 环境变量。如未设置，会提示用户到同花顺SkillHub获取。

## API 调用说明

**端点：** `POST https://openapi.iwencai.com/v1/query2data`

**请求头：**
| Header | 值 |
|--------|-----|
| Authorization | Bearer {IWENCAI_API_KEY} |
| Content-Type | application/json |
| X-Claw-Call-Type | normal / retry |
| X-Claw-Skill-Id | hithink-astock-selector |
| X-Claw-Skill-Version | 1.0.0 |
| X-Claw-Trace-Id | 64字符hex（每次新生成） |

**请求体：**
```json
{"query": "今日涨跌幅大于5%", "page": "1", "limit": "10", "is_cache": "1", "expand_index": "true"}
```

**响应：**
- `datas` — 股票列表
- `code_count` — 符合条件的总股票数
- `chunks_info` — 查询条件解析

## 错误处理

- 无数据时放宽条件重试（最多2次，重试时用 `X-Claw-Call-Type: retry`）
- 密钥缺失时提示用户到技能商店获取

## 数据来源标注

引用数据时必须标注 **数据来源于同花顺问财** (https://www.iwencai.com/unifiedwap/chat)
