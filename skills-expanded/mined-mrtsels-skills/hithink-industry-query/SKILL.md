---
name: hithink-industry-query
description: 查询行业估值、财务、盈利、行情、板块排名等数据，支持自然语言问句输入，返回相关行业数据结果。数据来源：同花顺问财。
---

# 问财行业数据 — hithink-industry-query

## 技能概述

行业数据查询，支持：
- 行业估值数据查询
- 行业财务指标查询
- 行业盈利数据查询
- 行业行情数据查询
- 板块排名数据查询

数据来源：**同花顺问财** (https://www.iwencai.com/unifiedwap/chat)

## CLI 使用

```bash
python3 scripts/cli.py --query "A股行业估值排名"
python3 scripts/cli.py --query "银行业盈利数据"
python3 scripts/cli.py --query "新能源板块行情"
python3 scripts/cli.py --query "行业涨跌幅排名"
```

## 环境变量

- `IWENCAI_BASE_URL` — API 基础地址
- `IWENCAI_API_KEY` — API 密钥（必填，可从 iwencai.com/skillhub 获取）

## API 规范

**端点：** `POST https://openapi.iwencai.com/v1/query2data`

**Claw Headers：**
| Header | 值 |
|--------|-----|
| Authorization | Bearer {IWENCAI_API_KEY} |
| X-Claw-Call-Type | normal / retry |
| X-Claw-Skill-Id | hithink-industry-query |
| X-Claw-Skill-Version | 1.0.0 |
| X-Claw-Trace-Id | 64字符hex（每次新生成） |

## 错误处理

- 无数据时放宽条件重试（最多2次，用 `X-Claw-Call-Type: retry`）
- 密钥缺失时提示用户到技能商店获取
