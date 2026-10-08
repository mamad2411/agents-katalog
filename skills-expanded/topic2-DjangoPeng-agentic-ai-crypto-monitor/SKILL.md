---
name: crypto-monitor
description: |
  定期巡检加密货币行情，通过 CoinGecko API 获取 BTC、ETH、LTC 的实时价格（USD/CNY）
  和 24h 涨跌幅。涨跌幅超过阈值时推送行情摘要，全部正常时回复 HEARTBEAT_OK。
  支持 /crypto-monitor 斜杠命令触发，也可通过自然语言触发（如"帮我看一下 BTC 行情"、
  "加密货币价格怎么样"、"crypto price check"）。
  配合 Cron 定时任务实现自动巡检。
metadata:
  openclaw:
    requires:
      env:
        - COINGECKO_API_KEY
        - MONITOR_THRESHOLD_PERCENT
      bins:
        - curl
        - jq
---

# crypto-monitor — 加密货币行情巡检

## 环境变量

| 变量名 | 必需 | 默认值 | 说明 |
|--------|------|--------|------|
| `COINGECKO_API_KEY` | ✅ | — | CoinGecko Demo API Key（`CG-` 开头） |
| `MONITOR_THRESHOLD_PERCENT` | ❌ | `3` | 涨跌幅告警阈值（百分比） |

## 执行步骤

### 1. 环境检查

读取环境变量，确认 `COINGECKO_API_KEY` 已配置。若为空则报错并终止。
`MONITOR_THRESHOLD_PERCENT` 未设置时使用默认值 `3`。

### 2. 调用 CoinGecko API

获取 BTC、ETH、LTC 的实时行情数据：

```bash
curl -s "https://api.coingecko.com/api/v3/simple/price?\
ids=bitcoin,ethereum,litecoin&\
vs_currencies=usd,cny&\
include_24hr_change=true&\
x_cg_demo_api_key=${COINGECKO_API_KEY}"
```

### 3. 解析数据

用 `jq` 提取每个币种的：
- USD 价格（`usd`）
- CNY 价格（`cny`）
- 24h USD 涨跌幅（`usd_24h_change`）

### 4. 阈值判断

对每个币种，检查 `|usd_24h_change|` 是否超过 `MONITOR_THRESHOLD_PERCENT`：
- **超过阈值** → 标记为异动币种，纳入行情摘要
- **未超过** → 标记为正常

### 5. 输出结果

根据判断结果选择输出格式（见下方"输出格式"部分）。

## 异常处理

### 超时 / 网络错误
- API 调用失败时，等待 **10 秒** 后重试 **1 次**
- 仍然失败则报告：`❌ CoinGecko API 调用失败: [HTTP 状态码 / 错误信息]`

### 限流（HTTP 429）
- 收到 429 响应时，等待 **60 秒** 后重试
- 仍返回 429 则报告：`⚠️ CoinGecko API 限流，请等待后重试（Demo 计划限制 30 calls/min）`

### 数据异常
- 返回 JSON 中缺少预期字段时，报告具体缺失内容
- 价格为 0 或负数时标记为异常数据

## 输出格式

### 有超阈值币种时

```
📊 加密货币行情巡检报告

⚠️ 异动币种：
- BTC：$103,200 / ¥752,300（24h +5.2% ⬆️ 超过阈值 3%）

✅ 正常币种：
- ETH：$2,650 / ¥19,300（24h -1.1%）
- LTC：$87 / ¥634（24h +0.8%）

📋 阈值设置：±3%
⏰ 检查时间：2024-01-01 12:00 UTC
```

### 全部在阈值内时

```
HEARTBEAT_OK
```

## 停止条件

- 全部币种涨跌幅在阈值范围内 → 输出 `HEARTBEAT_OK`，任务完成
- 有币种超过阈值 → 输出行情摘要，任务完成
- API 多次失败 → 输出错误报告，任务完成

## Cron 定时配置

推荐通过飞书 DM 让 Agent 创建 cron 任务：

```
请帮我创建一个 cron 定时任务：
- 任务名称：crypto-check
- 执行频率：每 4 小时
- 执行内容：调用 crypto-monitor Skill
```

对应 crontab 配置：`0 */4 * * *  openclaw run crypto-monitor`
