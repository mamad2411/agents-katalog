---
name: quantai-service
description: >
  Crypto 单因子量化研究服务 Skill。当用户说"写一个因子"、"研究因子"、"量化打工"、
  "提交因子"、"因子回测"时加载此 Skill。
  Agent 负责编写因子插件代码并通过 HTTP 接口与服务器交互，
  服务器负责所有数据处理和计算，Agent 本地无需任何市场数据。
---

# QuantAI Service — Agent 操作手册

## 服务地址

```
BASE_URL = http://47.129.240.216:8000
```

> 启动前用 `curl ${BASE_URL}/health` 确认服务在线，若连接失败立刻告知用户。

---

## ⛔ 严禁行为

1. **禁止在本地运行任何 quant-factor-loop 脚本**（`run_workflow.py`、`step*.py` 等），所有计算都在服务器上。
2. **禁止下载或存储 parquet 数据文件**，不要尝试访问服务器上的数据文件。
3. **禁止修改 `/home/ec2-user/quant-factor-loop/` 下的任何文件**，该目录只属于服务器内部。
4. **轮询时禁止无限等待**：单个 Job 最长等待 30 分钟，超时后告知用户并停止。
5. **禁止跳过 retest 步骤**：Step 4C 的 C# 编译失败时必须修复 strategy.cs 后 retest，不能直接宣告失败。
6. **禁止等待 Step 5 及之后的步骤**：Step 4C 完成后立即获取结果，不再轮询。Step 5-16 是服务端内部调优，与用户无关。

---

## Agent 本地约定路径

每次开始新任务时，将以下路径记录到工作变量中：

```
~/quant_agent/
└── jobs/
    └── {job_id}/
        ├── plugin.py               ← 提交时上传的因子插件（阶段2完成后保存）
        ├── strategy.cs             ← Step 4a 生成的 C# 策略（strategy_cs_ready=true 后下载）
        ├── factor_card_default.json← Step 4C 默认参数因子档案卡（Step 4C 完成后下载）
        └── step4c/
            ├── equity_curves.png   ← Step 4C 默认参数权益曲线图（Step 4C 完成后下载）
            └── trade_log.csv       ← Step 4C 默认参数交易记录（Step 4C 完成后下载）
```

> **说明**：服务器内部会跑两次云端回测——Step 4C（默认参数）和 Step 11（调优参数）。
> Agent 只下载并展示给用户**默认参数版**（`default_` 前缀文件），调优参数版留在服务端。

---

## 服务器内部流程（Agent 无需操作，仅供了解）

提交任务后，服务器自动执行以下步骤，**Agent 全程只需轮询等待**：

```
Step 1-3   加载配置、计算前向收益、设置退出规则
Step 4A    生成 C# 策略代码（strategy.cs）
Step 4B    计算原始信号（Python 研究镜像）
Step 4C    默认参数云端回测 ← 用户看到的结果来自这里
Step 5-10  Z-score / EWMA / 网格搜索（服务端内部分析）
Step 11    调优参数云端回测（服务端内部分析）
Step 12-16 因子画像、汇总、敏感性、分组、因子档案卡（服务端内部，Agent 无需关心）
Step 16D   生成默认参数因子档案卡（服务端内部，Agent 无需关心）
```

> Agent 唯一需要介入的场景：C# 编译失败（`failed_step="4c"`）→ 修复 strategy.cs → retest。
> Step 4C 回测完成后，Agent 即可获取结果并展示给用户，**无需等待 Step 5 及之后的步骤**。

---

## Agent 工作流程（必须按顺序执行）

### 阶段 -1：选择工作模式

每次启动时，**第一步**先询问用户选择工作模式：

```
请问这次要：
A）打工模式 ── 从服务器领取发布的研究任务，AI 自主设计技术路径
B）自由定义 ── 由你直接描述想研究的因子

（输入 A 或 B，或直接描述因子想法）
```

#### A. 打工模式

1. 拉取任务列表并展示：

```bash
curl -s ${BASE_URL}/tasks
```

输出示例：
```json
[
  {"task_id": "task_momentum_001", "title": "短期价格动量", "category": "momentum"},
  {"task_id": "task_volume_001",   "title": "主动成交量失衡", "category": "volume"}
]
```

2. 请用户选择一个任务（或 AI 根据本地归档自动选一个尚未研究过的类别）。

3. 拉取选中任务的完整描述：

```bash
TASK_ID="task_momentum_001"
curl -s ${BASE_URL}/tasks/${TASK_ID}
```

4. 阅读 `description` 和 `hints`，**AI 自主决定技术路径**（不需要再问用户实现细节），直接进入**阶段 0b** 提取任务信息。进入阶段 0b 时将 `fwd_period` 采用任务 JSON 中的值（默认 16）。

> 注意：任务永远是 `open` 状态，多个 AI 可以同时研究同一任务，结果越多样越好，**不存在"已被领取"的情况**。

#### B. 自由定义

用户直接描述因子逻辑，进入**阶段 0b**（现有流程，无变化）。

---

### 阶段 0：确认任务

**0a. 查重——检查已研究过的因子**

写代码前先扫描本地归档，避免重复研究同类因子：

```bash
for f in ~/quant_agent/jobs/*/plugin.py; do
  [ -f "$f" ] && grep -H "^FACTOR_TYPE" "$f"
done
```

输出示例：

```
/home/ec2-user/quant_agent/jobs/job_20260312_153001_f4a2c1/plugin.py:FACTOR_TYPE = "rsi_oversold_bounce"
/home/ec2-user/quant_agent/jobs/job_20260315_063800_a1b2c3/plugin.py:FACTOR_TYPE = "bollinger_breakout"
```

- 若用户要求的因子逻辑与已有 `FACTOR_TYPE` **本质相同**（仅参数不同），告知用户已有该因子并展示历史 job_id，询问是改参数重跑还是确认要新建。
- 若逻辑有实质区别（如 RSI 超卖 vs RSI 背离），正常继续。
- 归档目录为空时跳过此步。

**0b. 提取任务信息**

从用户描述中提取：

| 信息 | 说明 | 示例 |
|------|------|------|
| 因子逻辑 | 用自然语言描述信号如何产生 | "RSI低于30时做多" |
| 核心参数 | 窗口期、阈值等超参 | `rsi_period=14, oversold=30` |
| `factor_type` | 因子类型标识（snake_case，全局唯一） | `rsi_oversold_bounce` |
| `factor_name` | 因子名称（含主要参数值） | `rsi_14_ob30` |

若用户描述不清晰，主动补问这几项，确认后再写代码。

---

### 阶段 1：编写因子插件 plugin.py

插件文件包含两部分，**必须同时实现，逻辑必须完全一致**：

1. **`FACTOR_SECTIONS`**：C# 代码片段，服务器用它生成 `strategy.cs`
2. **`build_signal()`**：Python 函数，服务器用它做超参网格搜索

#### 插件文件完整模板

```python
import pandas as pd
import numpy as np
from typing import Any, Dict

FACTOR_TYPE = "<factor_type>"   # 与提交时的 factor_type 参数保持一致

FACTOR_DEFAULT_PARAMS = {
    "param1": <default_int>,    # 所有超参及默认值，key 用 snake_case
}

FACTOR_SECTIONS = {
    # ── 注释类（人类可读） ───────────────────────────────────────────────
    "__FACTOR_DESCRIPTION__": "因子的中文描述",
    "__FACTOR_FORMULA__":     "信号公式（注释用）",
    "__FACTOR_TYPE__":        "<factor_type>",

    # ── C# 类字段声明（每行末尾必须有 \n） ──────────────────────────────
    "__FACTOR_PARAM_FIELDS__": (
        "        private int _param1;\n"
        # 每个字段一行，注意 8 个空格缩进
    ),

    # ── C# 构造函数初始化（每行末尾必须有 \n） ───────────────────────────
    "__FACTOR_INIT__": (
        '            _param1 = GetIntParameter("param1", <default>);\n'
        # key 用连字符（"param-one"），对应 Python 端 key 用下划线（"param_one"）
    ),

    # ── 初始化日志（每行末尾必须有 \n） ─────────────────────────────────
    "__FACTOR_LOG__": (
        '            Log($"[INIT] param1={_param1}");\n'
    ),

    # ── 滑动窗口大小（合法 C# 整数表达式，不加引号） ─────────────────────
    "__PRICE_WINDOW_EXPR__": "_param1 + 1",

    # ── 额外数据列 Buffer 声明（每行末尾必须有 \n，仅用 close 时填 ""） ──
    # FactorCsvBar 字段类型（决定 Enqueue 时是否需要强转）：
    #   decimal : Open / High / Low / Close / Volume
    #             → Enqueue 时必须写 (double)bar.Volume 等，否则 CS1503 编译报错
    #   double  : TakerBuyVolume / TakerSellVolume / TakerBuyQuoteVolume /
    #             TakerSellQuoteVolume / TakerBuyTrades / TakerSellTrades / QuoteVolume
    #             → 直接 Enqueue，无需转型
    "__EXTRA_BUF_FIELDS__": "",   # 示例：'        private readonly Queue<double> _volBuf = new Queue<double>();\n'

    # ── 额外列每 bar 入队（每行末尾必须有 \n，不用时填 ""） ─────────────
    # decimal 字段示例：'            _volBuf.Enqueue((double)bar.Volume);\n'
    # double  字段示例：'            _takerBuyBuf.Enqueue(bar.TakerBuyVolume);\n'
    "__EXTRA_BUF_ENQUEUE__": "",

    # ── 额外列超窗口出队（每行末尾必须有 \n，不用时填 ""） ──────────────
    "__EXTRA_BUF_DEQUEUE__": "",  # 示例：'            if (_volBuf.Count > requiredBars) _volBuf.Dequeue();\n'

    # ── 额外列转数组供计算体使用（每行末尾必须有 \n，不用时填 ""） ────────
    "__EXTRA_BUF_TOARRAY__": "",  # 示例：'            var volumes = _volBuf.ToArray();\n'

    # ── C# 信号计算主体 ──────────────────────────────────────────────────
    # 始终可用：prices[]（close，从旧到新）
    # 若声明了 __EXTRA_BUF_TOARRAY__，对应数组也在此可用
    # 必须给 rawSignal 赋值（正=看多，负=看空）并 return true
    # 数据不足时 return false（不要 throw）
    "__FACTOR_COMPUTE_BODY__": """
            // C# 计算逻辑
            var n = prices.Length;
            if (n < _param1) return false;
            // ... 计算 ...
            rawSignal = <signal_value>;
            return true;
""",
}


def build_signal(
    close: pd.DataFrame,
    params: Dict[str, Any],
    # 声明因子用到的列（框架自动注入，与 close 地位相同）：
    # open, high, low, volume, quote_volume,
    # taker_buy_volume, taker_sell_volume,
    # taker_buy_quote_volume, taker_sell_quote_volume,
    # taker_buy_trades, taker_sell_trades
    **_kwargs,
) -> pd.DataFrame:
    """
    close  : pd.DataFrame，index=UTC DatetimeIndex，columns=币种代码
    params : dict，key 与 FACTOR_DEFAULT_PARAMS 一致
    返回   : 与 close 同形状的 DataFrame，正=看多，负=看空，NaN=无信号
    逻辑必须与 FACTOR_SECTIONS.__FACTOR_COMPUTE_BODY__ 完全一致
    """
    param1 = int(params.get("param1", <default>))
    # ... Python 实现 ...
    return signal.reindex_like(close)
```

#### C# 代码约束（违反会导致 Step 4C 编译失败）

| 约束 | 说明 |
|------|------|
| `__PRICE_WINDOW_EXPR__` | 必须是纯 C# 整数表达式，不加引号，如 `_window + 1` |
| `rawSignal` | 必须在 `__FACTOR_COMPUTE_BODY__` 中被赋值 |
| 数据不足 | 用 `return false`，不要 `throw` 或 `return true` 而不赋值 |
| 类型 | 所有计算用 `double`，不用 `decimal` 或 `float` |
| 禁止调用 | `Securities[].GetLastData()`、`Portfolio`、`Order`、`SetHoldings` |
| 参数 key | `GetIntParameter("param-name", default)` 用连字符 |
| 每行末尾 | `__FACTOR_PARAM_FIELDS__` / `__FACTOR_INIT__` / `__FACTOR_LOG__` / `__EXTRA_BUF_FIELDS__` / `__EXTRA_BUF_ENQUEUE__` / `__EXTRA_BUF_DEQUEUE__` / `__EXTRA_BUF_TOARRAY__` 每行末尾加 `\n` |
| 不用额外列时 | `__EXTRA_BUF_FIELDS__` / `__EXTRA_BUF_ENQUEUE__` / `__EXTRA_BUF_DEQUEUE__` / `__EXTRA_BUF_TOARRAY__` 填空字符串 `""` |
| 额外列数组长度 | 额外列 buf 使用与 close 相同的 `requiredBars` 窗口大小 |
| **decimal → double 强转** | `Open`/`High`/`Low`/`Close`/`Volume` 是 `decimal`，Enqueue 时必须写 `(double)bar.Volume` 否则报 `CS1503`；`TakerBuy*/TakerSell*/QuoteVolume` 已是 `double`，无需转型 |

#### 参考实现（完整可运行的例子）

<details>
<summary>示例：RSI 超卖反弹因子（rsi_oversold_bounce）</summary>

```python
import pandas as pd
import numpy as np
from typing import Any, Dict

FACTOR_TYPE = "rsi_oversold_bounce"

FACTOR_DEFAULT_PARAMS = {
    "rsi_period": 14,
    "oversold":   30,
    "overbought": 70,
}

FACTOR_SECTIONS = {
    "__FACTOR_DESCRIPTION__": "RSI 超卖反弹：RSI < oversold 做多，RSI > overbought 做空",
    "__FACTOR_FORMULA__":     "RSI < oversold → +(oversold-RSI)/oversold; RSI > overbought → -(RSI-overbought)/(100-overbought)",
    "__FACTOR_TYPE__":        "rsi_oversold_bounce",
    "__FACTOR_PARAM_FIELDS__": (
        "        private int _rsiPeriod;\n"
        "        private double _oversold;\n"
        "        private double _overbought;\n"
        "        private double _prevGainEma;\n"
        "        private double _prevLossEma;\n"
        "        private bool _rsiInitialized;\n"
    ),
    "__FACTOR_INIT__": (
        '            _rsiPeriod = GetIntParameter("rsi-period", 14);\n'
        '            _oversold = GetDoubleParameter("oversold", 30.0);\n'
        '            _overbought = GetDoubleParameter("overbought", 70.0);\n'
        '            _prevGainEma = 0.0;\n'
        '            _prevLossEma = 0.0;\n'
        '            _rsiInitialized = false;\n'
    ),
    "__FACTOR_LOG__": (
        '            Log($"[INIT] rsi_period={_rsiPeriod} oversold={_oversold} overbought={_overbought}");\n'
    ),
    "__PRICE_WINDOW_EXPR__": "_rsiPeriod + 1",
    "__EXTRA_BUF_FIELDS__":   "",
    "__EXTRA_BUF_ENQUEUE__":  "",
    "__EXTRA_BUF_DEQUEUE__":  "",
    "__EXTRA_BUF_TOARRAY__":  "",
    "__FACTOR_COMPUTE_BODY__": """
            var n = prices.Length;
            if (n < _rsiPeriod + 1) return false;

            if (!_rsiInitialized)
            {
                double sumGain = 0.0, sumLoss = 0.0;
                for (int i = 1; i < n; i++)
                {
                    var change = prices[i] - prices[i - 1];
                    if (change > 0) sumGain += change;
                    else sumLoss += Math.Abs(change);
                }
                _prevGainEma = sumGain / _rsiPeriod;
                _prevLossEma = sumLoss / _rsiPeriod;
                _rsiInitialized = true;
            }
            else
            {
                var change = prices[n - 1] - prices[n - 2];
                var gain = change > 0 ? change : 0.0;
                var loss = change < 0 ? Math.Abs(change) : 0.0;
                _prevGainEma = (_prevGainEma * (_rsiPeriod - 1) + gain) / _rsiPeriod;
                _prevLossEma = (_prevLossEma * (_rsiPeriod - 1) + loss) / _rsiPeriod;
            }

            double rsi;
            if (_prevLossEma < 1e-12)
                rsi = 100.0;
            else
            {
                var rs = _prevGainEma / _prevLossEma;
                rsi = 100.0 - 100.0 / (1.0 + rs);
            }

            if (rsi < _oversold)
                rawSignal = (_oversold - rsi) / _oversold;
            else if (rsi > _overbought)
                rawSignal = -(rsi - _overbought) / (100.0 - _overbought);
            else
                rawSignal = 0.0;

            return true;
""",
}


def _compute_rsi_wilder(close: pd.DataFrame, period: int) -> pd.DataFrame:
    delta = close.diff()
    gain  = delta.clip(lower=0.0)
    loss  = (-delta).clip(lower=0.0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period, adjust=False).mean()
    rs  = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100.0 - 100.0 / (1.0 + rs)
    rsi.iloc[:period] = np.nan
    return rsi


def build_signal(close: pd.DataFrame, params: Dict[str, Any], **_) -> pd.DataFrame:
    rsi_period = int(params.get("rsi_period", 14))
    oversold   = float(params.get("oversold",   30.0))
    overbought = float(params.get("overbought", 70.0))

    rsi    = _compute_rsi_wilder(close, rsi_period)
    signal = pd.DataFrame(0.0, index=close.index, columns=close.columns)
    signal[rsi < oversold]   = (oversold   - rsi[rsi < oversold])   / oversold
    signal[rsi > overbought] = -(rsi[rsi > overbought] - overbought) / (100.0 - overbought)
    signal[rsi.isna()]       = np.nan
    return signal.reindex_like(close)
```

</details>

插件写好后保存到一个临时路径供提交用，提交后再按 job_id 归档。

<details>
<summary>示例：主力资金流入因子（taker_buy_ratio_momentum）— 使用 taker 额外列</summary>

```python
import pandas as pd
import numpy as np
from typing import Any, Dict

FACTOR_TYPE = "taker_buy_ratio_momentum"

FACTOR_DEFAULT_PARAMS = {
    "window": 20,
}

FACTOR_SECTIONS = {
    "__FACTOR_DESCRIPTION__": "主力资金流入：taker 主动买量占比的滚动均值偏离中性线 0.5",
    "__FACTOR_FORMULA__":     "buy_ratio = taker_buy_vol / (buy+sell); signal = rolling_mean(buy_ratio, w) - 0.5",
    "__FACTOR_TYPE__":        "taker_buy_ratio_momentum",
    "__FACTOR_PARAM_FIELDS__": (
        "        private int _window;\n"
    ),
    "__FACTOR_INIT__": (
        '            _window = GetIntParameter("window", 20);\n'
    ),
    "__FACTOR_LOG__": (
        '            Log($"[INIT] window={_window}");\n'
    ),
    "__PRICE_WINDOW_EXPR__": "_window",
    # ── 额外列：taker_buy_volume / taker_sell_volume ──────────────────
    "__EXTRA_BUF_FIELDS__": (
        "        private readonly Queue<double> _takerBuyBuf  = new Queue<double>();\n"
        "        private readonly Queue<double> _takerSellBuf = new Queue<double>();\n"
    ),
    "__EXTRA_BUF_ENQUEUE__": (
        "            _takerBuyBuf.Enqueue(bar.TakerBuyVolume);\n"
        "            _takerSellBuf.Enqueue(bar.TakerSellVolume);\n"
    ),
    "__EXTRA_BUF_DEQUEUE__": (
        "            if (_takerBuyBuf.Count  > requiredBars) _takerBuyBuf.Dequeue();\n"
        "            if (_takerSellBuf.Count > requiredBars) _takerSellBuf.Dequeue();\n"
    ),
    "__EXTRA_BUF_TOARRAY__": (
        "            var takerBuys  = _takerBuyBuf.ToArray();\n"
        "            var takerSells = _takerSellBuf.ToArray();\n"
    ),
    "__FACTOR_COMPUTE_BODY__": """
            var n = prices.Length;
            if (n < _window) return false;

            double sumRatio = 0.0;
            for (int i = 0; i < n; i++)
            {
                var total = takerBuys[i] + takerSells[i];
                var ratio = total > 1e-12 ? takerBuys[i] / total : 0.5;
                sumRatio += ratio;
            }
            rawSignal = sumRatio / n - 0.5;
            return true;
""",
}


def build_signal(
    close:            pd.DataFrame,
    params:           Dict[str, Any],
    taker_buy_volume: pd.DataFrame,
    taker_sell_volume: pd.DataFrame,
    **_kwargs,
) -> pd.DataFrame:
    window = int(params.get("window", 20))
    total = taker_buy_volume + taker_sell_volume
    buy_ratio = taker_buy_volume / total.replace(0, float("nan"))
    signal = buy_ratio.rolling(window).mean() - 0.5
    return signal.reindex_like(close)
```

</details>

---

### 阶段 2：提交任务

```bash
# 先把 plugin 写到临时文件
cat > /tmp/current_plugin.py << 'PLUGIN_EOF'
<plugin 内容>
PLUGIN_EOF

curl -s -X POST ${BASE_URL}/jobs/submit \
  -F "factor_kind=custom" \
  -F "factor_type=<factor_type>" \
  -F "factor_name=<factor_name>" \
  -F "params=<JSON字符串，如 {\"rsi_period\":14}>" \
  -F "fwd_period=16" \
  -F "plugin=@/tmp/current_plugin.py"
```

成功返回：

```json
{ "job_id": "job_20260312_153001_f4a2c1", "status": "queued" }
```

拿到 `job_id` 后，**将其设为 Shell 变量**并归档插件文件。`JOB_ID` 在当前会话的后续所有 Shell 调用中持续有效，无需写入文件：

```bash
JOB_ID="job_20260312_153001_f4a2c1"

mkdir -p ~/quant_agent/jobs/${JOB_ID}
cp /tmp/current_plugin.py ~/quant_agent/jobs/${JOB_ID}/plugin.py
```

> **builtin 因子**（`momentum` / `trend` / `mean_revert`）不需要上传 plugin，
> 改用 `factor_kind=builtin` 并省略 `-F "plugin=..."` 即可（无需归档 plugin.py）。

---

### 阶段 3：轮询等待

每 **15 秒**查询一次，最多等待 **30 分钟**。服务器内部步骤全自动执行，Agent 只需等。

```bash
curl -s ${BASE_URL}/jobs/${JOB_ID}/status
```

#### Agent 行为速查

| status | Agent 行为 |
|--------|-----------|
| `queued` / `running`（`current_step` < `"5"`） | 继续等待。每 2~3 次轮询告知用户当前进度 |
| `running`（`current_step` >= `"5"`）或 `done` | **Step 4C 已完成**，立即进入**阶段 4**获取结果，不再轮询 |
| `failed`（`failed_step="4c"`） | 进入**阶段 3b**修复 C# |
| `failed`（其他 step） | 告知用户服务器内部错误，无法修复 |
| `retesting` | 继续等待 |
| `retest_failed` | 查看 retest 日志，再次修复 strategy.cs |

> **关键规则**：一旦轮询发现 `current_step` 已进入 Step 5 或更后面的步骤，说明 Step 4C（默认参数回测）已完成，Agent 应立即停止轮询并进入阶段 4 获取结果。Step 5-16 是服务端内部调优分析，与用户无关。

#### strategy_cs_ready 标志

轮询时若返回 `"strategy_cs_ready": true`，立即下载并归档 strategy.cs（只需一次）：

```bash
mkdir -p ~/quant_agent/jobs/${JOB_ID}
curl -s ${BASE_URL}/jobs/${JOB_ID}/files/strategy.cs \
  -o ~/quant_agent/jobs/${JOB_ID}/strategy.cs
```

---

### 阶段 3b：修复 C# 编译错误并 retest

当 `status=failed` 且 `failed_step` 为 `"4c"` 时执行。

**1. 查看错误日志**

```bash
curl -s "${BASE_URL}/jobs/${JOB_ID}/logs?tail=80"
```

**2. 下载并修复 strategy.cs**

```bash
curl -s ${BASE_URL}/jobs/${JOB_ID}/files/strategy.cs \
  -o ~/quant_agent/jobs/${JOB_ID}/strategy.cs
```

根据日志中的错误信息修改。常见错误速查表：

| 错误信息 | 原因 | 修复方式 |
|---------|------|---------|
| `CS0019: Operator '/' cannot be applied to 'double' and 'decimal'` | C# 类型不匹配 | 在除法前加 `(double)` 强转 |
| `CS0103: The name 'xxx' does not exist` | 变量名拼写错误或作用域不对 | 检查 `__FACTOR_PARAM_FIELDS__` 中的声明 |
| `CS0128: A local variable named 'xxx' is already defined` | 变量名与模板框架冲突 | 在 `__FACTOR_COMPUTE_BODY__` 中重命名变量（**不要动框架代码**） |
| `CS1002: ; expected` | C# 语法错误 | 检查 `__FACTOR_COMPUTE_BODY__` 的每行结尾 |
| `rawSignal` 始终为 0 | `return true` 前忘记给 `rawSignal` 赋值 | 确保所有代码路径都给 `rawSignal` 赋值 |
| 回测运行时 NullReference | 访问了未初始化的字段 | 检查 `__FACTOR_INIT__` 是否遗漏了某个字段初始化 |

**修复原则**：只修改 `#region FactorComputeBody` 区域内的代码，不要动框架代码。

**3. 提交 retest**

```bash
curl -s -X POST ${BASE_URL}/jobs/${JOB_ID}/retest \
  -F "strategy_cs=@~/quant_agent/jobs/${JOB_ID}/strategy.cs"
```

返回 `{ "status": "retesting" }` 后回到**阶段 3**继续轮询。retest 提交后，服务器自动从失败点恢复并跑完所有后续步骤。

> 若连续 3 次 retest 仍失败，考虑重写 plugin.py 后重新 POST `/jobs/submit` 开新任务。

---

### 阶段 4：获取结果、展示给用户、开始下一个因子

> **⚠️ 关键规则**：`current_step >= 5` 时 Step 4C 已完成，**直接下载文件**。
> **禁止调用 `/result` 接口**——该接口需要整个 pipeline（Step 16D）跑完才返回数据，
> 而用户只需要看 Step 4C 的默认参数回测结果，不需要等后续步骤。

#### 4a. 下载产物文件（Step 4C 完成即可下载）

```bash
JOB_DIR=~/quant_agent/jobs/${JOB_ID}
mkdir -p ${JOB_DIR}/step4c

curl -s ${BASE_URL}/jobs/${JOB_ID}/files/default_factor_card.json \
  -o ${JOB_DIR}/factor_card_default.json

curl -s ${BASE_URL}/jobs/${JOB_ID}/files/default_equity_curves.png \
  -o ${JOB_DIR}/step4c/equity_curves.png

curl -s ${BASE_URL}/jobs/${JOB_ID}/files/default_trade_log.csv \
  -o ${JOB_DIR}/step4c/trade_log.csv
```

#### 4b. 从 factor_card_default.json 读取结果并展示

下载完成后，直接读取本地的 `factor_card_default.json` 文件，从中提取关键指标：

| JSON 字段 | 用途 |
|-----------|------|
| `status` | `"pass"` 或 `"fail"` |
| `median_sharpe` | 默认参数中位 Sharpe |
| `icir` | IC 信息比率 |
| `median_annual_return` | 中位年化收益 |
| `median_max_drawdown` | 中位最大回撤 |
| `win_rate` | 胜率 |

同时打开 `equity_curves.png` 展示权益曲线图。

#### 4c. 展示结果并进入下一轮

用一段话总结核心表现：
- 重点突出 `status`（pass/fail）、`median_sharpe`、`icir`
- 如果 fail，分析原因并建议改进方向

**展示完结果后，直接与用户讨论下一个因子**——不需要等服务器做其他事情，这个因子的全部工作已经结束。

---

## 完整流程示意图

```
用户：「研究一个布林带宽度突破因子」
        │
        ▼
[阶段0] 确认 factor_type / factor_name / params
        │
        ▼
[阶段1] 写 plugin.py（C# 片段 + Python build_signal）
        │
        ▼
[阶段2] POST /jobs/submit → 拿到 job_id，归档 plugin.py
        │
        ▼
[阶段3] 轮询等待 Step 4C 完成（current_step >= 5 或 done）
        │
        ├─ strategy_cs_ready=true → 下载 strategy.cs
        ├─ failed (4c) → [阶段3b] 修 C# → retest → 回到轮询
        │
        └─ current_step >= 5 或 done
             │
             ▼
[阶段4] 下载 default_ 文件 → 展示因子卡片 → 讨论下一个因子
```

---

## 其他接口

```bash
# 查看 retest 日志
curl -s "${BASE_URL}/jobs/${JOB_ID}/retest_logs?tail=100"

# 健康检查
curl -s ${BASE_URL}/health
```

---

## 向用户汇报进度的节奏

- 提交任务后立即告知 job_id
- 每 2~3 次轮询告知用户当前进度（不必每次都说）
- 看到 `current_step="4c"` 时说「正在云端回测，约需 3~5 分钟」
- 遇到 C# 编译失败（仅 Step 4C）时告知用户「正在修复代码后重试」，不要抛出错误
- **一旦 `current_step` >= 5，立即停止轮询，获取结果**
- 结果出来后重点突出 pass/fail、median_sharpe、icir
- **只展示默认参数版卡片**，展示完直接进入下一个因子
