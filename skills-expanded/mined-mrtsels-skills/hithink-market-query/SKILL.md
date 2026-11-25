---
name: hithink-market-query
description: 获取股票、ETF、指数等实时价格、涨跌幅、成交量、主力资金流向、大小单、技术指标等行情数据，支持自然语言问句输入。数据来源：同花顺问财。
---

# 问财行情数据 — hithink-market-query

## 技能概述

行情数据查询，支持：
- 股票实时价格、涨跌幅、涨跌额
- 成交量、成交额、换手率
- 主力资金流向、大单小单、主力净流入
- 技术指标（MACD、KDJ、RSI、布林线等）
- ETF 和指数行情（上证指数、沪深300、创业板指等）

数据来源：**同花顺问财** (https://www.iwencai.com/unifiedwap/chat)

## CLI 使用

```bash
python3 scripts/cli.py --query "同花顺最新价格"
python3 scripts/cli.py --query "主力资金流向"
python3 scripts/cli.py --query "上证指数行情" --page 2 --limit 20
python3 scripts/cli.py --query "MACD金叉"
```

## 环境变量

- `IWENCAI_BASE_URL` — API 基础地址
- `IWENCAI_API_KEY` — API 密钥（必填，可从 iwencai.com/skillhub 获取）

## API 规范

**端点：** `POST https://openapi.iwencai.com/v1/query2data`

**Claw Headers 必须携带：**
| Header | 值 |
|--------|-----|
| Authorization | Bearer {IWENCAI_API_KEY} |
| X-Claw-Call-Type | normal / retry |
| X-Claw-Skill-Id | hithink-market-query |
| X-Claw-Skill-Version | 1.0.0 |
| X-Claw-Trace-Id | 64字符hex（每次新生成） |

## 错误处理

- 无数据时放宽条件重试（最多2次，用 `X-Claw-Call-Type: retry`）
- 密钥缺失时提示用户到技能商店获取
