---
name: tick-microstructure
description: |
  A 股 L1 快照 tick 微观结构分析工具箱（知识库 + 可移植 Python 包 tick_analysis）。
  从 3 秒快照+五档盘口+累计量额笔数计算：资金流向/主动买卖(Lee-Ready/BVC)、盘口压力(OBI/微价/委比)、
  流动性(有效价差/Kyle λ/Amihud/Roll)、笔均与大中小单、集合竞价(开/收盘)、执行分析(VWAP/TWAP/滑点)。
  通过可移植列契约接入任意 tick 源(打包 parquet/xtquant 原始/其他)。含 L1/L2 边界与坑位，
  避免对快照 tick 过度解读(无法识别逐笔/真实大单/撤单/席位)。
  当需要从 tick 数据做资金流/盘口/流动性/竞价/执行分析时使用。
---

# tick-microstructure

## 1. 定位

A 股 **Level-1 快照 tick**（3 秒切片 + 五档买卖盘口 + 累计成交量/额/笔数）的微观结构分析工具箱，
提供知识库（本文 + references/）与自包含 Python 包（`tick_analysis/`，仅依赖 pandas/numpy）。

适用数据：QMT/xtquant 采集的 `a_share_tick.py` 打包 parquet，或任何映射到本技能列契约的 tick 源。

---

## 2. 30 秒上手

```python
import tick_analysis as ta

# 方式 A：读本项目打包 parquet（含手->股自动转换）
df = ta.from_packed_parquet("Z:/A股冷数据/tick_by_day/2026/06/26.parquet",
                             stock_code="002602.SZ")

# 方式 B：xtquant 原始（dict/DataFrame，含手->股转换）
# df = ta.from_xtquant(raw_dict["002602.SZ"], stock_code="002602.SZ")

# 一键全套指标
result = ta.analyze(df)
```

**真实输出示例（002602.SZ，2026-06-26）：**

```
002602.SZ 当日 4831 条 tick
全单主动净额: +0.12 亿  (买12.85/卖12.72)
主力净额    : +0.12 亿  尾盘 -0.10 亿
VWAP        : 13.695
盘口OBI均值 : +0.164  价差 7.7bp
Amihud      : 0.0275
竞价: open 13.68 / prev_close 13.74 / close 13.67
```

默认 method=bvc（更适合 3 秒聚合；Lee-Ready 可选但在聚合 bar 上方向有偏，见 references/methods.md）

`analyze()` 返回 dict：`money_flow / main_force / orderbook / liquidity / auction / vwap`。

单独调用示例：

```python
# 资金流向（全单）
mf = ta.money_flow(df, method="lee_ready")   # {"buy":..., "sell":..., "net":..., "net_ratio":...}

# 主力净额含日内累计
main = ta.main_force_flow(df, big_threshold=50e4, method="lee_ready")
main["cum_net"].plot(title="日内累计主力净额")  # 注意：裸 .plot() 以行号为 x 轴；按时间轴对齐见 references/recipes.md 第 2 节

# 盘口
obi = ta.order_book_imbalance(df, levels=5)  # pd.Series in [-1, 1]

# 竞价
ta.auction_features(df)   # {"open_price":..., "close_price":..., ...}

# 流动性
ta.amihud_illiquidity(df)    # float（单日，建议多日聚合）
ta.kyle_lambda(df)           # float
```

---

## 3. 数据契约速查

契约 DataFrame：**单只股票**、按 `datetime` 升序，列名遵循下表。

### 必需列

| 列 | 含义 | 类型 | 单位 |
|---|---|---|---|
| `datetime` | 北京时间（tz-naive 或 UTC+8） | datetime64[ns] | — |
| `last_price` | 最新价 | float | 元 |
| `volume` | 累计成交量 | int/float | **股（shares）** |
| `amount` | 累计成交额 | float | 元 |
| `transaction_num` | 累计成交笔数 | int/float | — |

### 盘口列（至少一档）

`bid_price_1..5`、`ask_price_1..5`、`bid_vol_1..5`、`ask_vol_1..5`

盘口 vol 列保留数据源原生单位（仅用于比值计算，不换算）。

### 可选列

`open, high, low, last_close, stock_code, stock_status`

### 单位说明（重要）

QMT/xtquant 原始 tick 中 `volume` 为**手（lots = 100 股）**，而 `amount` 为元。
`from_xtquant` 和 `from_packed_parquet` 均通过 `lot_size=100` 自动将手转为股，
使契约不变量 `amount ≈ vwap × volume` 成立。

**`from_dataframe`（通用映射）不做任何单位缩放**——调用方必须自行保证传入的 `volume` 已是股。

详见 [references/data-contract.md](references/data-contract.md)。

---

## 4. 方法索引

| 分析领域 | 函数 | 一行说明 |
|---|---|---|
| **资金流向/主动买卖** | `classify_trades(df, method)` | 每切片方向 ±1（BVC 返回买入额占比 ∈[0,1]） |
| | `money_flow(df, method)` | 全单主动买/卖/净额/净占比（dict） |
| | `main_force_flow(df, big_threshold, method)` | 大单脉冲主力净额 + 日内累计 Series + 开/尾盘净额 |
| **笔均/大中小单** | `avg_trade_amount(df)` | 笔均成交额 = ΔAmt/ΔCnt（Series） |
| | `trade_size_buckets(df, thresholds, labels)` | 大/中/小/特大单成交额汇总（Series by bucket） |
| **盘口压力** | `order_book_imbalance(df, levels)` | OBI = (ΣbidVol-ΣaskVol)/(ΣbidVol+ΣaskVol) ∈[-1,1] |
| | `microprice(df)` | Stoikov 微价（量加权中价，偏向成交侧） |
| | `weiba_weicha(df, levels)` | 委差 / 委比（DataFrame） |
| | `book_depth(df, levels, side)` | 五档挂单深度（Σ价×量） |
| | `quoted_spread(df, in_bps)` | 报价价差 ask1-bid1（绝对值或 bp） |
| **流动性** | `effective_spread(df, in_bps)` | 有效价差 = 2·|price-mid|/mid（同期中价，bp） |
| | `kyle_lambda(df, freq, method)` | Kyle λ：Δprice~签名成交量回归斜率 |
| | `amihud_illiquidity(df, freq)` | Amihud 非流动性 = mean(\|ret\|/成交额亿元) |
| | `roll_spread(df)` | Roll(1984) 隐含价差 = 2√(-cov(Δp_t, Δp_{t-1})) |
| **竞价** | `opening_auction(df)` | 开盘竞价（9:15-9:25）特征 dict |
| | `closing_auction(df)` | 收盘竞价（14:57-15:00）特征 dict |
| | `auction_features(df)` | 合并开/收盘关键特征（供批量扫描） |
| **执行分析** | `vwap(df, start, end)` | 成交量加权均价 = ΣdAmt/ΣdVol |
| | `twap(df, start, end)` | 时间加权均价（连续段 last_price 均值） |
| | `slippage_vs_vwap(fills, df)` | 成交均价相对 VWAP 的滑点（bp） |
| | `participation_rate(fills, df, start, end)` | 参与率 = 自身成交量/市场成交量 |
| | `implementation_shortfall(arrival_price, fills)` | 实现差额（IS, bp） |

详细公式、参数与局限见 [references/methods.md](references/methods.md)。

---

## 5. L1 / L2 边界（必读）

本技能仅适用于 **Level-1 快照 tick（3 秒切片）**。以下事情 L1 **做不到**：

| 需求 | 为什么 L1 做不到 | 需要什么 |
|---|---|---|
| 逐笔成交/委托明细 | L1 是 3 秒聚合，单快照可含数百笔 | L2 逐笔成交/委托 |
| 真实大单识别（精确） | 3 秒聚合稀释：大单可能与小单混在同一切片 | L2 逐笔成交 |
| 撤单 / 委托队列分析 | L1 盘口只是当前快照，无撤单信息 | L2 逐笔委托 |
| VPIN 精确分类 | 需要逐笔方向；L1 只能近似 | L2 逐笔成交 |
| 席位识别 | 完全无法 | 龙虎榜数据 |

**重要：本包所有"主力/大单"指标均为统计近似**——用"单切片 ΔAmt 阈值"判断大单脉冲，
方向与强弱的趋势相对可靠，但绝对金额不可轻信（3 秒内多笔小单之和会超过阈值）。

---

## 6. 坑位摘要

以下是使用 L1 快照 tick 最容易踩的坑，**本包已在内部处理**，但了解机制有助于正确使用：

1. **累计值必须 diff**：`volume/amount/transaction_num` 是当日累计值，内部调用 `to_increments()` 取差分。
2. **3 秒聚合稀释大单**：大单识别用切片 ΔAmt 阈值，是近似，不是精确。
3. **方向分类用滞后盘口**：`prev_bid1/prev_ask1` 取上一快照，避免 look-ahead 泄漏。
4. **竞价段 last_price 可能为 0/dVol=0**：需 `split_sessions()` 先切分，竞价函数已内部处理。
5. **UTC+8 转换**：`from_xtquant` 已将 UTC 毫秒时间戳 +8h；其他源须自行转换。
6. **涨跌停单边盘口**：OBI/价差遇单边盘口会失真，建议按 `stock_status` 过滤。
7. **`.empty` 无数据日**：批量循环时跳过此标记文件。
8. **Amihud/Kyle λ 单日噪声大**：单日值不稳定，应多日聚合使用。
9. **volume 单位（手 vs 股）**：`from_packed_parquet`/`from_xtquant` 已自动将手转为股；`from_dataframe` 不做转换，须自行保证 volume 是股，否则 VWAP/参与率会偏差 100 倍。

详见 [references/pitfalls.md](references/pitfalls.md)。
