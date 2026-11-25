---
name: tdx-obv-ma-strategy
description: OBV + MA 量价共振策略——个股诊断、全市场选股、持仓择时。当用户要用 OBV/能量潮/量价关系配合均线做分析选股，要找「量价共振」「量价背离」「顶背离/底背离」「放量突破」「缩量上涨」的票，或要对某只票做量价体检、给买卖点和止损位时使用。基于本地通达信 tqcenter，需终端已启动。不负责纯基本面筛选、涨停板/龙虎榜数据、真实下单。
---

# OBV + MA 量价共振策略

价格会骗人，成交量不会。这套模板把**价格趋势（MA）**和**资金进出（OBV）**拆成两个独立维度各 50 分，
用两者的**共振与背离**做判断——只有价涨且 OBV 同步推高，上涨才有资金背书。

## 先决条件

通达信终端必须在跑。不确定就先 `tdx_status` → 必要时 `tdx_connect`。
扫描脚本直连 tqcenter（不走 MCP），所以**全市场扫描不占对话上下文**。

## 云端通道（无需本地终端，供任意 agent 使用）

`--channel cloud` 走 tdxhub TQLEX 后端（与 tdx-finance-mcp 插件同源），只需 token
（环境变量 `TDX_API_TOKEN`/`TDX_API_KEY`，或向上查找 `.mcp.json` 自动读取）。
OBV/MAOBV/MA 由 PBFXT 日K本地复算（与 Volume 同源自算，量纲自动对齐，无需 --sector）。

```
# 个股诊断（其他 agent 只要有 tdx-finance-mcp token 即可运行）
py -3.13 scripts/obv_ma_scan.py --channel cloud --codes 600519.SH --json
# 批量（清单外置：每行一个代码）
py -3.13 scripts/obv_ma_scan.py --channel cloud --codes-file list.txt --min-score 85 --out out.csv
```

限制：cloud 不支持 `--universe`（云端无股票池接口）——全市场扫描仍需 local；
`--count` 默认 250，两通道口径一致可直接对拍。


## 三种模式（按用户意图选一个）

| 用户想要 | 模式 | 怎么做 |
|---|---|---|
| 「帮我看看 600674 的量价」 | **个股诊断** | 脚本 `--codes` + `--json`，按 `references/scoring.md` 的模板出诊断 |
| 「全A/沪深300 里选量价共振的票」 | **全市场选股** | 脚本 `--universe` + `--min-score`，出排序表 |
| 「我持仓的 XXX 还能拿吗」 | **择时信号** | 先跑个股诊断，再按下面的操作映射给动作+仓位+止损 |

### 模式一：个股诊断

```
py -3.13 <skill>/scripts/obv_ma_scan.py --codes 600674.SH,000001.SZ --json
```

拿到 JSON 后按 `references/scoring.md` 的输出模板写诊断。**必须解释分数，不能只报数**：
低分要说清是价格拖累还是量能拖累，命中背离要单独点出来。

### 模式二：全市场选股

```
# 沪深300 里的强共振
py -3.13 <skill>/scripts/obv_ma_scan.py --universe 23 --min-score 90 --no-topdiv --top 20

# 全A，只要双多共振，结果落盘
py -3.13 <skill>/scripts/obv_ma_scan.py --universe 5 --min-score 85 --quadrant 双多共振 \
    --no-topdiv --min-amount 1 --out D:\cc-workspace\tdx-local\obv_ma_scan.csv --top 30

# 潜伏底背离（价弱量强，左侧）
py -3.13 <skill>/scripts/obv_ma_scan.py --universe 5 --quadrant 价弱量强 --min-amount 1 --top 30
```

**选股模式一律带 `--min-amount 1`**（20 日均额下限，亿元）。薄票的 OBV 回撤天数噪音大，
一笔大单就能动好几天的量；全A 均额中位数才 1.19 亿，不滤会有大半是流动性陷阱。

池子编码：`5` 全A · `50` 沪深A · `23` 沪深300 · `24` 中证500 · `51` 创业板 · `52` 科创板 · `0` 自选股 · `1` 持仓股。
完整清单 `tdx_list_enums(group='stock_list_category')`。

**阈值定标**：`--min-score` 不是绝对标准，取决于行情冷暖。牛市里全A 能有上千只 ≥80，
这时要提到 90 才够挑。先不带阈值跑一遍看分布，再定线——**别把宽市场的 80 分当成强信号报给用户**。

**分数到 90 以上会饱和**（实跑：108 只入选票里 33 只满分 100），这时必须加二级判别轴，
否则给不出有意义的排序。推荐漏斗：

```
≥90 分 + --no-topdiv + --min-amount 1
  → 双多共振           （象限）
  → dd_penalty = 0     （无量能退潮）
  → obv_nh20 = true    （OBV 同步创 20 日新高，量能确认而非滞后）
  → 乖离 0~8%          （不追高）
  → 按「20 日资金流入强度」排序 —— 算法见 references/scoring.md
```

ST 标的默认已剔除（`--include-st` 可保留）。

选出来的票可以写回终端自定义板块：`tdx_create_sector` + `tdx_send_user_block`。

### 模式三：择时信号

先拿到个股诊断，再按象限 + 分数映射操作：

| 象限 | 含义 | 动作 | 仓位 |
|---|---|---|---|
| **双多共振**（价≥25 量≥25） | 价涨量增，资金背书 | 总分≥85 买入/加仓；65~85 持有 | 乖离<8% 可 6~8 成；>15% 只持有不加 |
| **价强量弱** | 价格新高但 OBV 跟不上 | 减仓，不加；带顶背离标记则优先减 | 降到 3~5 成 |
| **价弱量强** | 价格破位但 OBV 在吸筹 | 观察；底背离 + OBV 上穿 MAOBV 才左侧试仓 | ≤3 成试探 |
| **量价双空** | 价跌量出 | 回避 / 清仓 | 0 |

必给的三个价位：**止损** MA10（短线）或 MA20（波段）· **买点** 回踩 MA5/MA10 不破 ·
**确认** 收盘破 20 日高 且 OBV 同步新高（`obv_nh20=true`）。

**`obv_dd_days` 要单独看一眼**：它是 OBV 距 20 日峰值回撤了几天的平均量，>3 会触发扣分
（`dd_penalty`），但即使没到 3 也是有效的减仓参考——高分票带着 2~3 天量的退潮，
说明资金已在撤，只是还没到惩罚门槛。

## 两条硬约束（踩过坑）

1. **OBV 绝对值不可跨样本比较。** OBV 是从窗口第一根 K 线开始的累加值，换 `count` 值就整体平移
   （600674 在 `count=250` 下 642 万，`count=120` 下 453 万），不同股票之间还有股本量级差。
   所以只能用**斜率、与 MAOBV 的相对位置、区间百分位、新高状态**，绝不比大小。
   脚本里 `--count` 默认 250，**不要随意改**，改了历史结果就不可比。
2. **可视化通道在当前 mock 环境不可用。** `tdx_send_bt_data` 返回空指针，`tdx_print_to_tdx` 会因
   tqcenter 内部 emoji 在 GBK stdout 下崩。结论一律在对话里出表格，不要试图推图。

## 参考文件

- `references/scoring.md` — 打分细则（每一分怎么来的）、量能退潮档位标定、四象限定义、
  输出模板。改阈值先读这个。**分数会掩盖结构，单票诊断前务必拉 OBV 明细核对**，原因见该文件。
- `references/tdx-formulas.md` — 可选：把策略装进通达信自己的公式管理器，在客户端图上直接看信号 /
  用内置条件选股。含完整公式源码和安装步骤。
- `scripts/obv_ma_scan.py` — 扫描器。改评分逻辑改 `score_one()`，改取数改 `fetch_chunk()`。

## MCP 路线（脚本不可用时的兜底）

脚本挂了才走这条，它会把大量数据搬进对话：

```
tdx_formula_process_mul_zb(formula_name="OBV",  formula_arg="30",
    stock_list=[...], return_count=60, count=250, dividend_type=1, xsflag=2)
tdx_formula_process_mul_zb(formula_name="MA", formula_arg="5,10,20,60",
    stock_list=[...], return_count=6,  count=250, dividend_type=1, xsflag=3)
```

注意 `dividend_type` 在公式接口是**整数**（0/1/2），在 K 线接口是**字符串**（none/front/back）。
OBV 内置公式出两条线 `OBV` 和 `MAOBV`（参数 M 默认 30，即 MAOBV 的周期）；
MA 出 8 条线 `MA1..MA8`，只传 4 个参数时 `MA5..MA8` 为 null。
批量接口忽略 `set_data_info`，数据源完全由本次参数决定。
