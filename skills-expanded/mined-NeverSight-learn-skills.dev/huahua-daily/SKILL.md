---
name: huahua-daily
description: 花花日记助手 - 查询用户的基金持仓、今日收益、累计收益、市场行情等数据，并可向 App 发送交易请求信号
version: 1.0.0
author: baiye1997
permissions: 网络访问权限（用于查询花花日记后端 API）
metadata: {"openclaw":{"requires":{"env":["BAIYE_AGENT_TOKEN"]},"primaryEnv":"BAIYE_AGENT_TOKEN","emoji":"🌸","os":["darwin","linux","win32"]}}
---

# 花花日记助手 (HuahuaDaily)

## 1. Description

花花日记助手让 AI 直接读取用户在花花日记 App 中的基金持仓数据，提供持仓收益查询、市场行情查看、基金搜索等功能。所有工具均需 Agent Token（花花日记 PRO 会员专属），数据来自云端同步。

交易操作（买入/卖出）不直接执行，AI 通过 `request_transaction` 发送信号，由用户在 App 中一键确认后生效。

## 2. When to use

- 用户说："我今天收益多少？"、"帮我看一下我的持仓"、"我的总资产是多少？"
- 用户说："易方达蓝筹现在涨了多少？"、"帮我查一下 110022 的净值"
- 用户说："今天大盘怎么样？"、"沪深300涨跌如何？"
- 用户说："帮我搜一下华夏基金"、"查一下这只基金的费率"
- 用户说："帮我看看这只基金近一年排名"、"今天走势怎么样？"
- 用户说："我想买 1000 元易方达消费"、"帮我发一个卖出请求"

## 3. How to use

1. **首次使用**：确认 `BAIYE_AGENT_TOKEN` 已通过环境变量配置；若未配置，引导用户前往 https://huahuadaily.preview.aliyun-zeabur.cn/ 注册账号并开通 PRO 会员，在「设置 → Agent Token」生成后配置到环境变量；

2. **查询总览**：优先调用 `get_summary`，返回总资产、今日收益、累计收益；如需明细再调用 `get_records`；返回结果中须将 `dataUpdatedAt` 同步时间告知用户（如"数据同步于 XX 时间"），让用户判断数据是否最新；

3. **查询单只基金行情**：
   - 用户已提供代码（如"查 110022"）：直接调用 `get_item_estimate`，无需先搜索；
   - 用户只给名称：先调用 `search_item` 找到 code，再调 `get_item_estimate`；
   - 用户需要深度分析（历史、胜率、排名等）：调用 `get_item_detail`（较慢，仅需深度信息时使用）；

4. **查询市场整体**：调用 `get_overview` 或 `get_indices`；

5. **发送交易信号**：
   - 若 code 来自搜索结果，须先向用户确认：「是【基金名 code:XXXXXX】吗？确认后我来发送请求。」
   - 用户确认后再调用 `request_transaction`；
   - 调用完成后明确告知：「信号已发送，请打开 App 确认后才会生效，AI 不会直接执行交易。」

6. **数据过时处理**：若用户提到"刚刚刷新"或数据明显滞后，提示其在 App「设置 → 立即同步」手动上传后再查询；

7. **结果复用**：同一次对话中，一次查询结果可回答多个相关问题，不必重复调用同一工具。

## 4. 可用工具

### 认证
- `set_token` — 运行时设置 Agent Token（推荐用环境变量，通常无需调用）

### 数据查询
- `search_item(query)` — 按编号/名称搜索，返回最多 20 条（仅 code 未知时使用）
- `get_item_estimate(codes)` — 批量获取今日实时估算净值（最多 50 个）；日常查行情首选，轻量快速
- `get_item_detail(code)` — 基金深度信息（历史收益率、胜率分析、净值序列、费率）；仅需深度分析时使用
- `get_item_history(code)` — 历史净值走势
- `get_item_dividends(code)` — 历史派息记录
- `get_fund_timeline(code)` — 今日分时估值走势（非交易日返回空）
- `get_fund_fees(code)` — 申购/赎回/管理/托管费率
- `get_fund_period_rank(code)` — 近 1/3/6 月、1 年业绩及同类排名百分位
- `get_daily_rank()` — 今日涨跌幅排行榜

### 概览数据
- `get_status()` — 今日是否交易日
- `get_overview()` — 市场整体概览（指数 + 板块 + 涨跌榜）
- `get_indices()` — 主要指数实时数据（沪深、创业板、纳斯达克等）

### 记录管理（需 PRO 会员 + Agent Token）
- `get_current_user()` — 当前账号信息
- `get_summary()` — 持仓总览摘要（总市值/今日收益/累计收益/收益率），含 `dataUpdatedAt`
- `get_records()` — 完整持仓明细（holdings 持仓 + watchlist 观察列），含实时收益计算和 `dataUpdatedAt`
- `request_transaction(item_code, item_name, record_type, amount, date?, note?)` — 向 App 发送买入/卖出请求信号

## 5. Edge cases

- **未配置 Token**：工具返回错误提示，引导用户前往 https://huahuadaily.preview.aliyun-zeabur.cn/ 注册/登录，开通 PRO 会员后在「设置 → Agent Token」生成并配置到环境变量 `BAIYE_AGENT_TOKEN`；
- **Token 无效/过期**：收到 401 错误，引导用户前往 https://huahuadaily.preview.aliyun-zeabur.cn/ 在「设置 → Agent Token」重新生成，并更新环境变量；
- **数据过时**（用户刚在 App 刷新）：提醒用户在 App「设置 → 立即同步」手动上传最新数据，否则 MCP 仍读取旧的云同步数据；
- **非交易日查询今日收益**：`todayProfit` 为 0，属正常现象，说明"今日未开市，显示的是官方净值下的持仓状态"；
- **基金估算为空**（盘前/节假日）：`estimatedNav` 为 null，`todayProfit` 为 0，属正常，无需报错；
- **搜索无结果**：引导用户确认基金编号或名称是否正确；
- **request_transaction 后**：明确告知用户"信号已发送，请打开 App 确认后才会记录交易"，不要误导用户认为已成功执行。
