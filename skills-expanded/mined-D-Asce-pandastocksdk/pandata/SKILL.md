---
name: pandata
description: >-
  Query A-share market data via pandaData, a NATS-backed A股 data API with
  AI stock selection. Use when the user asks for A-share quotes, fund flow,
  DDX, AI stock selection, or realtime stock snapshots.
---

# pandaData Skill

pandaData 提供基于 NATS 的 A股 数据通道：行情、资金流、DDX、AI 选股等，
全部以**请求/响应**方式调用。

## 接入

客户端模块 `panda_stock`（Python）。鉴权方式为 **phone + nid**（NATS 用户/密码）。

```python
from panda_stock import PandaStock

ps = PandaStock(phone="pandastock", nid="pandastock")
ps.connect_server()
```

## 能力（22 个请求接口）

> 服务端完整目录共 **210 个接口**（含港股 / 美股 / Level2 新通道），完整清单见 [`INTERFACES.md`](INTERFACES.md)；其中 22 个对公开测试账号开放。

- 实时快照：`get_ch_stock_real()` / `get_ch_market_real()` / `get_ch_concept_real()` / `get_ch_industry_real()`
- 列表：`get_ch_stock()` / `get_ch_concept()` / `get_ch_industry()`
- 单只实时：`get_ch_one_stock_real(code)`
- 历史：日线 / 分钟 / 概念 / 行业 / 指数
- 资讯：核心 / 国内 / 全球 / 期权
- 市场：涨跌停 / 龙虎榜 / 资金流 / 多空对比
- DDX：`get_ch_stock_ddx_data(code)`
- AI 选股：`get_ch_select_stock()`

## 参数 schema（调用示例）

- `get_ch_stock()` —— 股票列表
- `get_ch_stock_real()` —— A股实时快照
- `get_ch_market_real()` —— 指数实时快照
- `get_ch_concept_real()` —— 概念板块实时快照
- `get_ch_industry_real()` —— 行业板块实时快照
- `get_ch_one_stock_real(code)` —— 单只实时行情，code 如 `600519`
- `get_ch_stock_fund_flow(code)` —— 个股主力资金流
- `get_ch_stock_ddx_data(code)` —— 个股 DDX
- `get_core_new(date)` —— 核心资讯
- `get_ch_select_stock()` —— AI 选股结果

## 注意

- 公共测试账号：`phone="pandastock"` / `nid="pandastock"`，按 IP 限频、限接口；正式/高频请申请专属 phone/nid。
- 计费、配额、接口开放范围由 pandaData 服务端（NATS 网关）统一管控。
