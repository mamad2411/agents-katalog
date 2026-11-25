---
name: sop-market-research
description: 跨境电商市场调研 Skill（Shopee BR / Mercado Livre）。把虾多拉等工具导出的类目 CSV 洗成标准数据，算市场容量、品牌/卖家集中度（CR3/CR10/HHI）、价格带分箱与波谷检测、配置交叉表，并解读"这个类目值不值得进"。当用户要"看类目 / 市场分析 / 价格带 / 竞品集中度 / 选品前置调研"时使用。
allowed-tools:
  - Bash(python *)
  - Read
  - Write
metadata:
  version: 0.4.0
  category: e-commerce/market-research
  license: MIT
---

# 01 · Market Research Skill（市场调研）

**分工边界：数字由脚本算，"意味着什么、下一步做什么"由你（Agent）解读。**
不要自己重算指标——报告里的数字是脚本算的确定性结果；怀疑数字有问题就输出
`[METRIC_SUSPECT]`，让使用者检查脚本参数。

## 最小输入

```text
1. 类目商品数据 CSV/Excel（虾多拉等工具导出：商品名/价格/月销量/月销售额/卖家/品牌…）
2. 类目名称 + 平台
3. （可选）配置维度字段名，如 功率,承重
```

## 三条底线

1. **不编造数据** —— 输入里没有的字段不许猜，缺关键列就报 `[INPUT_MISSING]` 并列出可用列
2. **不替代选品决策** —— 输出的是分析结论与下一步建议，最终决策必须由人做
3. **数字必须可溯源** —— 解读中引用的每个数字都要能在脚本报报告里指到出处

## 工作流

```text
[Step 1] 跑 shaduola_parser.py 洗数据（脏格式 → 标准化 JSON）
         支持 R$ 1.234,56 / 1,234 / 1.2万 / 4个月 / 月销售额缺失按 价格×销量 补算
[Step 2] 跑 market_metrics.py 出指标报告（容量 / CR3·CR10·HHI / 价格带波谷 / 配置交叉表）
[Step 3] 按 prompts/02_market_analysis.md 解读：
         → 这个类目值不值得进（容量、集中度、价格带下界 vs 成本可行价）
         → 主流配置是什么、哪里有机会配置
         → 结论喂给 02 Product Strategy
```

## 命令速查

```bash
# ① 洗数据（CSV/Excel 都吃；--profile 只看列识别不产出）
python scripts/shaduola_parser.py 类目导出.csv -o data.normalized.json

# ② 算指标（--config-fields 按类目改）
python scripts/market_metrics.py data.normalized.json \
    --bins 10 --config-fields "功率,承重,容量" --format md -o report

# ③ 没有真实数据时，先生成带脏数据的样本验证环境
python scripts/make_sample.py
```

## 解读时的判断阈值（SOP 内置，写进你的分析）

- 品牌 CR3 高但**前三名全是白牌** → 买家不认品牌，新店仍有空间
- 卖家「销售额份额 < 商品数份额」→ 占位型不是效率型，是可超越对象
- 价格带波谷边界 ≈ 成本可行价 → 市场结构与成本结构吻合，该价位可信
- 配置「商品数多但平均销量低」→ 最卷的段，只能当价格锚不能做主推
- 波谷检测**默认不平滑**（平滑会抹掉陡峭波谷）；主体数 ≤ n 时 CR-n 无意义，改看 CR3 + HHI

## 已知限制

- 数据采集本身不在本 Skill 内（虾多拉/卖家后台导出由使用者提供）
- 指标均**未含巴西税费**，涉及利润判断时提醒使用者自行补税率
- 销量数据是平台展示口径，存在刷单噪声，结论注明数据来源与时间
