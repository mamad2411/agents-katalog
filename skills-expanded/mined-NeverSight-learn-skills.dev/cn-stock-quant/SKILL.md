---
name: cn-stock-quant
description: |
  A股个股全面量化分析。当用户要求分析某只A股股票（如"分析600900"、"做一次XX的量化分析"、"XX量化报告"、"帮我看看XX基本面"）时触发。覆盖：历史估值分位、FCF分红模型、因子信号、风险指标、资金面、同行对比、事件日历、量化交易规则回测。输出专业量化报告，可选输出到飞书文档。
---

# A股个股量化分析

## 快速开始

运行主脚本（自动识别6位数字股票代码）：

```bash
cd {baseDir}/scripts && python3 quant_analysis.py 600900
```

带参数运行：

```bash
# 指定分析模块
python3 quant_analysis.py 600900 --modules valuation,factors,risk

# 输出JSON（便于下游处理）
python3 quant_analysis.py 600900 --format json

# 同行对比（自动检测同行业公司）
python3 quant_analysis.py 600900 --peer-compare
```

## 分析模块

| 模块 | 参数 | 说明 |
|------|------|------|
| valuation | `-m valuation` | 历史PE/PB分位数（3/5/10年） |
| fcf | `-m fcf` | 自由现金流、分红率、DDM估值 |
| factors | `-m factors` | 9因子信号（反转/动量/量能/波动） |
| risk | `-m risk` | 夏普/Sortino/Calmar/最大回撤/VaR |
| momentum | `-m momentum` | 动量分组回测、反转规则 |
| capital | `-m capital` | 量价关系、筹码分布、OBV |
| events | `-m events` | 事件日历、季节性统计 |
| trading | `-m trading` | 量化交易规则回测 |
| peers | `--peer-compare` | 同行PE/PB/股息率/技术面对比 |

默认运行全部模块。

## 数据源

- **行情数据：** akshare `stock_zh_a_hist`（A股日线，2015年起）
- **财务数据：** akshare `stock_financial_*_ths`（同花顺财务报表）
- **实时行情：** 腾讯API `qt.gtimg.cn`（PE/PB/市值/股息率）
- **同行识别：** 按行业自动匹配（见 `references/peer_groups.md`）

依赖：`pip install akshare pandas numpy`

## 输出到飞书

创建飞书文档并写入报告：

```python
# 1. 创建文档
feishu_doc(action="create", title="XX量化分析报告", owner_open_id="ou_xxx")

# 2. 写入内容（飞书不支持markdown表格，用列表替代）
feishu_doc(action="write", doc_token="xxx", content=report)

# 3. 设置公开链接
# 见 scripts/set_public_link.py
```

## 详细方法论

参见：
- [references/factor_definitions.md](references/factor_definitions.md) — 因子定义与计算方法
- [references/trading_rules.md](references/trading_rules.md) — 交易规则模板与回测方法
- [references/peer_groups.md](references/peer_groups.md) — 行业同行分组

## 输出格式

报告按以下结构输出（各模块可独立使用）：

```
一、历史估值分位数（PE/PB分位）
二、自由现金流 & 分红量化模型
三、因子信号系统（9因子评分）
四、风险指标量化（夏普/回撤/VaR）
五、动量与反转量化规则
六、资金面量化（量价/筹码/OBV）
七、事件驱动日历 & 季节性
八、量化交易规则回测
九、同行横向对比
十、综合量化评分 & 操作建议
```

## 注意事项

- 财务数据仅支持年报/半年报/季报披露后更新
- PE分位计算用年度EPS，年末切换，非实时滚动
- 腾讯API的字段映射可能变化，需定期验证
- akshare 接口偶有限流，遇错自动重试（最多3次）
