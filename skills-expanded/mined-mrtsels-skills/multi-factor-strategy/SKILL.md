---
name: multi-factor-strategy
description: 多因子选股策略创建工具。引导用户定义选股策略，生成YAML配置文件，使用 quantcli 执行多因子选股。
---

# Multi-Factor Strategy Assistant — 多因子选股策略

## 安装 quantcli

```bash
pip install quantcli
```

## 快速开始

创建策略 YAML 文件：

```yaml
name: Value-Growth Hybrid Strategy
version: 1.0.0
description: ROE + 动量因子选股

screening:
  fundamental_conditions:
    - "roe > 0.10"
    - "pe_ttm < 30"
    - "pe_ttm > 0"
  daily_conditions:
    - "close > ma10"
  limit: 100

factors:
  - name: ma10_deviation
    expr: "(close - ma(close, 10)) / ma(close, 10)"
    direction: negative
  - factors/alpha_001.yaml
  - factors/alpha_008.yaml

ranking:
  weights:
    ma10_deviation: 0.20
    factors/alpha_001.yaml: 0.40
    factors/alpha_008.yaml: 0.40
  normalize: zscore

output:
  limit: 30
  columns: [symbol, name, score, roe, pe_ttm, close, ma10_deviation]
```

运行：
```bash
quantcli filter run -f your_strategy.yaml
```

## 因子配置

支持两种方式（可混用）：
- **内联**：YAML 中直接定义表达式
- **外部引用**：引用 `factors/` 目录下的因子文件

## 常用基本面因子

| 因子 | 表达式 | 方向 | 说明 |
|------|--------|------|------|
| roe | `roe` | positive | 净资产收益率 |
| pe | `pe` | negative | 市盈率（低更好） |
| pb | `pb` | negative | 市净率 |
| netprofitmargin | `netprofitmargin` | positive | 净利润率 |
| revenue_growth | `revenue_yoy` | positive | 营收增长率 |

## 常用技术因子

| 因子 | 表达式 | 方向 | 说明 |
|------|--------|------|------|
| momentum | `(close/delay(close,20))-1` | positive | N日动量 |
| ma_deviation | `(close-ma(close,10))/ma(close,10)` | negative | 均线偏离度 |
| volume_ratio | `volume/ma(volume,5)` | negative | 量比 |

## 内置 Alpha101 因子

包含 40 个 WorldQuant Alpha101 因子（alpha_001 ~ alpha_040），按分类：
- alpha_001~010：反转、资金流、趋势、动量
- alpha_011~020：波动率、动量、量价
- alpha_021~030：量价、趋势、强度
- alpha_031~040：仓位、波动率、资金

查看全部因子：
```bash
quantcli factors list
```

## 工作流

1. 确定策略目标（价值/成长/动量/混合）
2. 选择因子组合
3. 配置权重（核心因子 0.3-0.4，辅助因子 0.1-0.2）
4. 生成策略 YAML
5. 运行 `quantcli filter run -f strategy.yaml`

## 支持的表达式函数

- **数据处理**：`delay(x,n)`, `ma(x,n)`, `ema(x,n)`, `rolling_sum()`, `rolling_std()`
- **技术指标**：`rsi()`, `correlation()`, `cross_up()`, `cross_down()`
- **排名/标准化**：`rank()`, `zscore()`, `sign()`, `clamp()`
- **条件**：`where(cond,t,f)`, `if(cond,t,f)`
- **基础字段**：`open,high,low,close,volume,pe,pb,roe,netprofitmargin`
