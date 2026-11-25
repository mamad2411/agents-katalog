---
name: dcf-model
description: Build discounted cash flow valuation workbooks in Excel.
version: 1.0.0
author: Anthropic (adapted by Nous Research)
license: Apache-2.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [finance, valuation, dcf, excel, openpyxl, modeling, investment-banking]
    related_skills: [excel-author, pptx-author, comps-analysis, lbo-model, 3-statement-model]
---

## 环境要求

该技能依赖于 **headless openpyxl** —— 您需要在磁盘上生成 .xlsx 格式的文件。在处理单元格着色、公式、命名范围以及敏感性分析表时，请遵循 `excel-author` 技能的相关规范。在交付结果之前务必重新计算：`python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx`。

# DCF模型构建器

## 概述

该技能能够按照投资银行的标准，为股票估值创建符合专业水准的DCF模型。每次分析都会生成一份结构完善的Excel模型（DCF表格底部会包含敏感性分析内容）。

## 工具说明

- 默认情况下，该技能会使用用户提供的所有信息以及MCP服务器可获取的数据源。

## 重要约束条件 —— 请先仔细阅读

以下约束适用于所有DCF模型的构建过程。在开始工作前请务必了解：

**必须使用公式而非硬编码值（绝对不可违反）：**
- 所有的预测值、利润率、折现率、现值以及敏感性分析相关的单元格都必须是有效的Excel公式 —— 绝不能是直接在Python中计算后以数值形式写入的
- 使用openpyxl时：`ws["D20"] = "=D19*(1+$B $8)"` 是正确写法；而 `ws["D20"] = calculated_revenue` 则是错误写法
- 唯一允许的硬编码数值包括：(1) 原始的历史数据，(2) 各项假设的驱动因素（如增长率、WACC参数、终值增长率等），(3) 实时的市场数据（如股价、债务余额）
- 如果您发现自己又在Python中计算某些数值后再将其写入模型 —— 请立即停止。当用户修改假设时，模型必须具备相应的灵活性。

**需与用户逐步骤确认，切勿直接从头到尾自动构建模型：**
- 数据检索完成后 → 向用户展示原始输入数据（营收、利润率、持股比例、净债务），并在进行预测前确认无误  
- 营收预测完成后 → 显示预测的营收总额及增长率，然后在计算利润率前再次确认  
- 自由现金流计算完成后 → 展示完整的自由现金流时间表，在计算加权平均资本成本前确认逻辑正确  
- 加权平均资本成本计算完成后 → 显示计算过程及输入参数，在进行折现前再次确认  
- 终值与现值计算完成后 → 展示股权价值推导过程（企业价值 → 股权价值 → 每股价值），在生成敏感性分析表前确认无误  
- 在每个阶段都会检测错误——如果在生成敏感性分析表后才发现利润率假设有误，将不得不重新计算后续所有数据  

**敏感性分析表：**
- **行数与列数需为奇数**（标准格式为5×5，有时也为7×7）——这样才能确保存在真正的中心单元格。
- **中心单元格即为基础案例**。需设置坐标轴数值，使得中间行标题与中间列标题恰好等于模型中的实际假设值（例如，若基础WACC为9.0%，则中间行为9.0%；若终端增长率为3.0%，则中间列为3.0%）。因此，中心单元格的输出值必须等于模型所隐含的实际股价——这是验证表格构建是否正确的关键依据。
- **用中蓝色填充色（#BDD7EE）加粗字体突出显示中心单元格**，以便立即识别出基础案例所在单元格。
- **需在所有单元格中填入完整的DCF重新计算公式**（通常3个表格×25个单元格=75个单元格）。
- 使用openpyxl循环以编程方式写入公式。
- **禁止使用占位符文本，禁止线性近似，也无需手动操作步骤**。
- 每个单元格都必须针对该组假设值重新计算完整的DCF结果。

**单元格注释说明：**
- 在为每个硬编码值创建时，需添加相应的单元格注释。
- 格式要求为：“来源：[系统/文档]，[日期]，[参考编号]，[如有网址则填写]”。
- 每个蓝色输入值在进入下一部分之前都必须附有注释。
- 不得将注释留到最后，也不得写“TODO：补充来源”这类内容。

**模型布局规划：**
- 在编写任何公式之前，必须先确定所有章节的行位置。
- 先填写所有的标题和标签。
- 接着添加所有的章节分隔符及空行。
- 最后再根据已确定的行位置写入公式。
- 公式创建完成后需立即进行测试。
- 在交付前运行命令 `python recalc.py model.xlsx 30`  
- 修正所有错误，直至状态显示为“success”  
- 公式中不得存在任何错误（如 #REF!、#DIV/0!、#VALUE! 等）  

**情景模块设置：**  
- 为熊市/基准市/牛市场景分别创建独立的模块  
- 在每个模块内，按预测年份横向展示各项假设条件  
- 使用 IF 公式实现逻辑判断：`=IF($B $6=1,[Bear cell],IF($B $6=2,[Base cell],[Bull cell]))`  
- 确保公式引用的单元格属于正确的情景模块  

## DCF 估值流程  

### 第一步：数据获取与验证  

从 MCP 服务器、用户提供的数据以及网络中获取数据。  

**数据来源优先级：**  
1. **MCP 服务器**（如已配置）——来自 Daloopa 等供应商的结构化金融数据  
2. **用户提供的数据**——用户研究所得的历史财务数据  
3. **网络搜索/获取**——根据需要获取当前股价、贝塔值、债务及现金状况等信息  

**验证检查清单：**  
- 核对净债务与净现金的数值（对估值至关重要）  
- 确认已发行稀释后股数（需注意近期的股票回购或发行情况）  
- 验证历史利润率是否与业务模式相符  
- 将营收增长率与行业基准进行对比分析  
- 确保税率处于合理范围（通常为 21%-28%）  

### 第二步：历史数据分析（3-5 年）  

对以下内容进行分析并形成记录：  
- **营收增长趋势**：计算复合年增长率，找出驱动因素  
- **利润率变化情况**：追踪毛利率、息税前利润率及自由现金流利润率的变化  
- **资本密集度**：分析折旧与摊销以及资本支出占营收的比重  
- **营运资金效率**：考察营运资金变动占营收增长率的百分比  
- **收益指标**：分析投资回报率与股本回报率的走势
创建汇总表，用于展示：
```
Historical Metrics (LTM):
Revenue: $X million
Revenue growth: X% CAGR
Gross margin: X%
EBIT margin: X%
D&A % of revenue: X%
CapEx % of revenue: X%
FCF margin: X%
```

### 第3步：制定收入预测

**预测方法：**
1. 以最新的实际收入数据（最近一个完整会计年度或最新财年的数据）作为起点；
2. 为每个预测年份应用相应的增长率；
3. 同时展示金额数值与计算得出的增长率。

**增长率设定原则：**
- 第1-2年：由于短期业务前景较为明朗，因此设定较高的增长率；
- 第3-4年：增长率逐步放缓，趋于行业平均水平；
- 第5年及以后：接近最终稳定增长率。

**公式结构：**
- 第N年的收入 = 第N-1年的收入 × (1 + 增长率)
- 第N年的增长率 = 第N年的收入 / 第N-1年的收入 - 1

**三情景预测法：**
```
Bear Case: Conservative growth (e.g., 8-12%)
Base Case: Most likely scenario (e.g., 12-16%)
Bull Case: Optimistic growth (e.g., 16-20%)
```

### 第4步：运营成本建模

**固定成本/变动成本分析：**

运营成本模型应体现真实的经营杠杆效应：
- **销售与市场费用**：根据业务模式不同，通常占收入的15%-40%
- **研发费用**：科技企业通常占收入的10%-30%
- **一般与管理费用**：通常占收入的8%-15%，且会随着公司规模扩大而呈现杠杆效应

**核心原则：**
- 所有百分比均以收入为基准，而非毛利润
- 需体现经营杠杆效应：随着收入增长，该比例应有所下降
- 需为销售与市场、研发、一般与管理费用分别设置独立的成本项目
- 毛利润 = 毛利润 - 总运营成本

**利润率提升框架：**
```
Current State → Target State (Year 5)
Gross Margin: X% → Y% (justify based on scale, efficiency)
EBIT Margin: X% → Y% (result of revenue growth + opex leverage)
```

### 第5步：自由现金流计算

**按正确顺序构建自由现金流：**

```
EBIT
(-) Taxes (EBIT × Tax Rate)
= NOPAT (Net Operating Profit After Tax)
(+) D&A (non-cash expense, % of revenue)
(-) CapEx (% of revenue, typically 4-8%)
(-) Δ NWC (change in working capital)
= Unlevered Free Cash Flow
```

**营运资金模型：**
- 按收入变动的百分比（收入差值）进行计算
- 典型范围：收入变动的 -2% 至 +2%
- 负数值表示现金来源（营运资金释放）
- 正数值表示现金消耗（营运资金占用）

**维护性资本支出与增长型资本支出：**
- 维护性资本支出：用于维持现有运营（约占收入的 2-3%）
- 增长型资本支出：用于业务扩张（约占额外收入的 2-5%）
- 总资本支出应与公司的成长战略保持一致

### 第6步：资本成本（WACC）研究

**股权成本的CAPM模型法：**

```
Cost of Equity = Risk-Free Rate + Beta × Equity Risk Premium

Where:
- Risk-Free Rate = Current 10-Year Treasury Yield
- Beta = 5-year monthly stock beta vs market index
- Equity Risk Premium = 5.0-6.0% (market standard)
```

**债务成本计算：**

```
After-Tax Cost of Debt = Pre-Tax Cost of Debt × (1 - Tax Rate)

Determine Pre-Tax Cost of Debt from:
- Credit rating (if available)
- Current yield on company bonds
- Interest expense / Total Debt from financials
```

**资本结构权重：**

```
Market Value Equity = Current Stock Price × Shares Outstanding
Net Debt = Total Debt - Cash & Equivalents
Enterprise Value = Market Cap + Net Debt

Equity Weight = Market Cap / Enterprise Value
Debt Weight = Net Debt / Enterprise Value

WACC = (Cost of Equity × Equity Weight) + (After-Tax Cost of Debt × Debt Weight)
```

**特殊情况：**
- **净现金头寸**：若现金 > 债务，则净债务为负值
  - 债务权重可能为负数
  - 加权平均资本成本将随之进行调整
- **无债务**：加权平均资本成本 = 股权成本

**常见的加权平均资本成本范围：**
- 大型稳定企业：7-9%
- 成长型企业：9-12%
- 高增长/高风险企业：12-15%

### 第7步：折现率应用（5-10年预测）

**年中假设规则：**
- 假设现金流发生在每年年中
- 折现期：0.5、1.5、2.5、3.5、4.5等
- 折现因子 = 1 / (1 + 加权平均资本成本)^折现期

**现值计算方法：**
```
For each projection year:
PV of FCF = Unlevered FCF × Discount Factor

Example (Year 1):
FCF = $1,000
WACC = 10%
Period = 0.5
Discount Factor = 1 / (1.10)^0.5 = 0.9535
PV = $1,000 × 0.9535 = $954
```

**预测期选择：**
- **5年**：适用于大多数分析场景的默认选项
- **7-10年**：适合具有较长发展前景的高增长企业
- **3年**：适用于成熟且稳定的企业

### 第8步：终值计算

**永续增长法（推荐方法）：**

```
Terminal FCF = Final Year FCF × (1 + Terminal Growth Rate)
Terminal Value = Terminal FCF / (WACC - Terminal Growth Rate)

Critical Constraint: Terminal Growth < WACC (otherwise infinite value)
```

**终端增长率选择：**
- 审慎型：2.0-2.5%（GDP增长率）
- 中等型：2.5-3.5%
- 激进型：3.5-5.0%（仅适用于市场领先者）

**不得超过以下数值**：无风险利率或长期GDP增长率

**退出倍数计算方法（备选方案）：**
```
Terminal Value = Final Year EBITDA × Exit Multiple

Where Exit Multiple comes from:
- Industry comparable trading multiples
- Precedent transaction multiples
- Typical range: 8-15x EBITDA
```

**终值现值：**
```
PV of Terminal Value = Terminal Value / (1 + WACC)^Final Period

Where Final Period accounts for timing:
5-year model with mid-year convention: Period = 4.5
```

**终值合理性检查：**
- 其数值应占企业价值的50%-70%
- 若超过75%，则模型可能过度依赖终值假设
- 若低于40%，则需检查终值假设是否过于保守

### 第9步：从企业价值到股权价值的转换

**估值汇总结构：**

```
(+) Sum of PV of Projected FCFs = $X million
(+) PV of Terminal Value = $Y million
= Enterprise Value = $Z million

(-) Net Debt [or + Net Cash if negative] = $A million
= Equity Value = $B million

÷ Diluted Shares Outstanding = C million shares
= Implied Price per Share = $XX.XX

Current Stock Price = $YY.YY
Implied Return = (Implied Price / Current Price) - 1 = XX%
```

**关键调整项：**
- **净债务 = 总债务 - 现金及现金等价物**
  - 若数值为正：从企业价值中扣除（从而降低股权价值）
  - 若为负值（即净现金）：加到企业价值中（从而提升股权价值）
- **采用稀释后股数**：包括期权、限制性股票单位以及可转换证券
- **其他调整项**（如适用）：
  - 少数股东权益
  - 养老金负债
  - 经营租赁义务

**估值输出格式：**
```csv
Valuation Component,Amount ($M)
PV Explicit FCFs,X.X
PV Terminal Value,Y.Y
Enterprise Value,Z.Z
(-) Net Debt,A.A
Equity Value,B.B
,,
Shares Outstanding (M),C.C
Implied Price per Share,$XX.XX
Current Share Price,$YY.YY
Implied Upside/(Downside),+XX%
```

### 第10步：敏感性分析

在DCF模型表的底部构建**三个敏感性表格**，用以展示在不同假设条件下的估值变化情况：

1. **加权平均资本成本与终端增长率**——反映企业价值对折现率及永续增长率的敏感度；
2. **营收增长率与息税前利润率**——体现营收增长速度与运营杠杆的影响；
3. **贝塔系数与无风险利率**——展示对股权成本各构成要素的敏感程度。

**实现方式**：这些表格为简单的二维网格（并非Excel中的“数据表”功能），每个单元格均包含相应公式。每个单元格都必须针对该特定的假设组合重新进行完整的DCF计算。关于如何使用openpyxl编程填充全部75个单元格的详细要求，请参阅“关键约束”部分。

<correct_patterns>

本节列出了构建DCF模型时需遵循的所有正确规范。

### 场景模块选择规范——请采用此方法

**每个场景的假设条件均被划分到独立的模块中：**

**核心结构要求——每个章节标题下方需包含三行内容：**

```csv
BEAR CASE ASSUMPTIONS (section header, merge cells across)
Assumption,FY1,FY2,FY3,FY4,FY5
Revenue Growth (%),12%,10%,9%,8%,7%
EBIT Margin (%),45%,44%,43%,42%,41%

BASE CASE ASSUMPTIONS (section header, merge cells across)
Assumption,FY1,FY2,FY3,FY4,FY5
Revenue Growth (%),16%,14%,12%,10%,9%
EBIT Margin (%),48%,49%,50%,51%,52%

BULL CASE ASSUMPTIONS (section header, merge cells across)
Assumption,FY1,FY2,FY3,FY4,FY5
Revenue Growth (%),20%,18%,15%,13%,11%
EBIT Margin (%),50%,51%,52%,53%,54%
```

**每个情景模块都必须包含一个列标题行**，该行应直接位于模块标题下方，用于标注预测年份（如FY2025E、FY2026E等）。若没有这一行，用户将无法判断某个假设数值对应的是哪一年。

**如何引用假设值——创建汇总列：**
1. 情景选择单元格（例如B6）中输入1表示看跌市场，2表示基准情况，3表示看涨市场；
2. 使用INDEX或OFFSET函数创建汇总列，从而从对应的情景模块中提取数据；
3. 预测公式引用该汇总列（使用规范的单元格引用格式）；
4. 每个情景模块都会包含涵盖所有预测年份的完整DCF假设值。

**推荐的汇总列设置方式（使用INDEX函数）：**
`=INDEX(B10:D10, 1, $B$\6)`

**请避免以下做法——在公式中散布过多的IF语句：**
`=IF($B$\6=1,[看跌市场模块单元格],IF($B$\6=2,[基准情况模块单元格],[看涨市场模块单元格]))`

采用汇总列的方式可以将逻辑集中处理，从而便于对模型进行审核。

### 正确的收入预测格式

**首先使用INDEX函数创建汇总列，然后在预测公式中引用该列：**

**步骤1——创建用于FY1增长情况的汇总列：**
`=INDEX([看跌市场FY1增长值]:[看涨市场FY1增长值], 1, $B$\6)`

**步骤2——收入预测公式引用该汇总列：**
`第一年收入 = D29*(1+$E$\10)`

其中：
- D29 = 上一年的收入数值；
- $E$\10 = 用于存储FY1增长情况的汇总列单元格（其中包含INDEX函数）；
- $B$\6 = 情景选择值（1=看跌市场，2=基准情况，3=看涨市场）。
**与在每个投影公式中嵌入 IF 语句相比，这种方法更为简洁**，同时也便于核查当前使用了哪些情景假设。

### 正确的自由现金流公式结构

**应使用包含 INDEX 公式的合并列，然后在自由现金流计算中引用这些列：**

**合并列法：**
```csv
Item,Formula,Reference
D&A,=E29*$E$21,$E$21 = consolidation column for D&A %
CapEx,=E29*$E$22,$E$22 = consolidation column for CapEx %
Δ NWC,=(E29-D29)*$E$23,$E$23 = consolidation column for NWC %
Unlevered FCF,=E57+E58-E60-E62,E57=NOPAT E58=D&A E60=CapEx E62=Δ NWC
```

**每个合并列单元格都包含一个 INDEX 公式**，该公式会根据案例选择器从相应的场景块中提取数据。这样一来，预测公式既简洁清晰，又便于审核。

在编写公式之前，请先确认场景块所在行位置，并设置好合并列。

### 正确的单元格注释格式

**所有硬编码的值都必须遵循以下格式：**

“来源：[系统/文档]，[日期]，[参考资料]，[如有网址则填写]”

**示例：**
```csv
Item,Source Comment
Stock price,Source: Market data script 2025-10-12 Close price
Shares outstanding,Source: 10-K FY2024 Page 45 Note 12
Historical revenue,Source: 10-K FY2024 Page 32 Consolidated Statements
Beta,Source: Market data script 2025-10-12 5-year monthly beta
Consensus estimates,Source: Management guidance Q3 2024 earnings call
```

### 正确的假设表结构

**重要提示：每个场景板块都必须包含三个结构要素：**

1. **章节标题行**（合并单元格）：例如“最坏情况假设”
2. **显示年份的列标题行**——此项为必填项，切勿省略
3. **包含假设数值的数据行**

**结构格式：**
```csv
BEAR CASE ASSUMPTIONS (section header - merge across columns A:G)
Assumption,FY1,FY2,FY3,FY4,FY5
Revenue Growth (%),X%,X%,X%,X%,X%
EBIT Margin (%),X%,X%,X%,X%,X%
Terminal Growth,X%,,,,
WACC,X%,,,,

BASE CASE ASSUMPTIONS (section header - merge across columns A:G)
Assumption,FY1,FY2,FY3,FY4,FY5
Revenue Growth (%),X%,X%,X%,X%,X%
EBIT Margin (%),X%,X%,X%,X%,X%
Terminal Growth,X%,,,,
WACC,X%,,,,

BULL CASE ASSUMPTIONS (section header - merge across columns A:G)
Assumption,FY1,FY2,FY3,FY4,FY5
Revenue Growth (%),X%,X%,X%,X%,X%
EBIT Margin (%),X%,X%,X%,X%,X%
Terminal Growth,X%,,,,
WACC,X%,,,,
```

**若不显示用于标注预测年份的列标题行（如FY2025E、FY2026E等），用户将无法判断某个假设数值对应的是哪一年。此行是必须存在的。**

**接着创建一个汇总列**（通常位于右侧的下一列），该列通过INDEX函数，根据案例选择器从选定的情景模块中提取数据。您的预测公式将引用这一汇总列。

### 正确的行规划流程

**1. 首先编写所有的标题和标签：**
```csv
Row,Content
1,[Company Name] DCF Model
2,Ticker | Date | Year End
4,Case Selector
7,KEY ASSUMPTIONS
26,Assumption headers
27-31,Growth assumptions
...,...
```

**2. 编写所有的章节分隔符及空行**

**3. 接着利用已锁定的行位置来编写公式**

**4. 公式创建后立即进行测试**

**可以将其类比为建筑工程：**
- 正确做法：先浇筑地基，再建造墙壁（结构稳固）
- 错误做法：先建造墙壁，再浇筑地基（墙壁会倒塌）

**Excel版本中的对应原则：**
- 正确做法：先添加表头，再编写公式（公式更稳定）
- 错误做法：先编写公式，再添加表头（公式会出错）

### 正确的敏感性表格实现方式

**重要提示**：这些并非Excel中的“数据表”功能。它们只是简单的网格结构，您需要使用openpyxl在这些网格中编写常规公式。没错，这意味着总共需要约75个公式（3个表格，每个表格25个单元格），但这种方式简单直接且是必需的。

**通过编程方式填充公式：**

每个敏感性表格都必须完整地填入公式，以便针对各种假设组合重新计算相应的股价。**请勿使用Excel的“数据表”功能**（该功能需要人工操作，无法通过openpyxl实现自动化）。

**实现方法——具体示例：**

**表格结构——5×5网格（奇数尺寸，基准情况位于中心）：**

如果模型的基准WACC为9.0%，基准终端增长率为3.0%，则应围绕这两个数值对称地构建坐标轴：

```csv
WACC vs Terminal Growth,  2.0%,  2.5%,  3.0%,  3.5%,  4.0%
              8.0%,       [fml], [fml], [fml], [fml], [fml]
              8.5%,       [fml], [fml], [fml], [fml], [fml]
              9.0%,       [fml], [fml], [★  ], [fml], [fml]   ← middle row = base WACC
              9.5%,       [fml], [fml], [fml], [fml], [fml]
             10.0%,       [fml], [fml], [fml], [fml], [fml]
                                   ↑
                          middle col = base terminal g
```

**★ = 中间单元格。**该单元格的公式计算结果必须与估值汇总表中显示的模型实际隐含股价完全一致。请为该单元格应用浅蓝色填充色（`#BDD7EE`）并设置加粗字体，以便在视觉上突出显示基准情况。

**坐标轴数值规则：** `axis_values = [base - 2*step, base - step, base, base + step, base + 2*step]`——数值以基准值为对称中心，奇数个数值可确保存在中间值。

**公式示例——B88单元格（WACC=8.0%，终端增长率=2.0%）：**

B88单元格中的公式应使用以下参数重新计算隐含股价：
- 来自行标题的加权平均资本成本：` $A88 `（8.0%）
- 来自列标题的终端增长率：` B $87 `（2.0%）

**推荐做法：** 参考主要的DCF计算公式，然后替换为上述参数。

**公式结构示例：**
`=([使用 $A88 作为折现率计算的FCF现值总和] + [使用 B $87 作为增长率、 $A88 作为加权平均资本成本计算的终值] - [净债务]) / [股数]`

**重要提示——必须为5×5网格中的每一个单元格（每张表格25个单元格，总计75个单元格）编写公式。**建议使用openpyxl通过循环以编程方式写入这些公式。切勿跳过此步骤或留下占位符文本。

**Python实现示例：**
```python
# Pseudocode for populating sensitivity table
for row_idx, wacc_value in enumerate(wacc_range):
    for col_idx, term_growth_value in enumerate(term_growth_range):
        # Build formula that uses wacc_value and term_growth_value
        formula = f"=<DCF recalc using {wacc_value} and {term_growth_value}>"
        ws.cell(row=start_row+row_idx, column=start_col+col_idx).value = formula
```

**在打开模型时，敏感性表格应立即生效，无需用户进行任何手动操作。**

```
// WRONG - Linear approximation
B97: =B88*(1+(0.096-0.116))    // Assumes linear relationship

// WRONG - Division shortcut
B105: =B88/(1+(E48-0.07))      // Doesn't recalculate full DCF
```

**请勿留下占位符文本：**
```
// WRONG - Placeholder note
"Note: Use Excel Data Table feature (Data → What-If Analysis → Data Table) to populate sensitivity tables."

// WRONG - Empty cells
[leaving cells blank because "this is complex"]
```

**请勿混淆相关术语：**
- ❌ “敏感性分析表需要使用 Excel 的数据表功能”（错误——那是一种我们无法使用的特定 Excel 工具）
- ✅ “敏感性分析表只是包含各单元格公式的简单表格”（正确——这正是我们要构建的内容）

**为何这些简化做法是错误的：**
- 线性近似公式实际上并不会重新计算DCF值，而只是进行简单的数学调整
- 各变量之间的关系并非线性，因此计算结果会不准确
- 占位文本需要用户手动补充
- 模型在交付时并非可直接使用状态
- 输出内容不够专业，无法直接呈现给客户
- 空单元格意味着交付物不完整

**常被用来作为拒绝理由的说法：**
“编写75个以上的公式太复杂了，我会在文档中留个提示让用户手动完成。”

**实际情况是：** 使用 Python 的 openpyxl 库结合循环结构，编写75个公式其实非常简单。每个公式的结构都相同，只需替换相应的行/列数值即可。这是交付物中不可或缺的部分。

**正确做法应是：** 在每一个敏感性分析单元格中输入公式，以便针对特定的假设组合重新计算完整的DCF值。

### 错误做法：遗漏单元格注释

**请避免以下行为：**
- 创建所有硬编码输入值却不加注释
- 以为“稍后再添加注释”
- 写下“TODO：补充数据来源”之类的提示
- 对蓝色标记的输入值不做任何说明

**为何这样做是错误的：**
- 无法追溯数据的来源
- 不符合相关技能要求
- 无法通过审计
- 后期修复会浪费大量时间

**正确做法应是：** 每创建一个硬编码值时，立即为其添加单元格注释。

### 错误：公式行引用错误

**症状：**
FCF部分引用了错误的假设行：
`D&A:  =E29*$E $34    // 正确应为 $E $21，但实际引用了错误行`
`CapEx: =E29*$E $41   // 正确应为 $E $22，但行号出现偏移`

**产生原因：**
1. 先编写公式
2. 再插入表头
3. 导致所有行引用发生偏移
4. 公式最终指向错误单元格 → 出现#REF!错误

**正确做法：** 先锁定行结构，再编写公式

### 错误：不同场景下每个假设仅使用单行

**请勿以这种方式组织假设：**
```csv
Assumption,Bear,Base,Bull
Revenue Growth FY1,10%,13%,16%
Revenue Growth FY2,9%,12%,15%
```
这种垂直布局使得难以查看每个情景中多年间的变化趋势。

**存在的问题：**
- 难以了解每个情景中各假设条件随时间的变化情况
- 难以在整个预测期内对比不同情景的假设条件
- 审查情景逻辑时不够直观

**推荐做法：**
- 为每种情景（熊市、基准、牛市）设置独立的区块
- 在每个区块内，按预测年份横向展示各项假设条件
- 这样就能将每种情景的假设条件作为一个整体更清晰地呈现出来

### 错误示例：未设置边框

**切勿提供没有边框的模型：**
- 没有区域分隔
- 所有单元格融为一体
- 难以阅读且显得不专业

**存在的问题：**
- 不适合直接呈交给客户
- 难以导航
- 看起来很业余

**推荐做法：** 为所有主要区域添加边框

### 错误示例：字体颜色不当或无颜色区分

**切勿这样做：**
- 所有文本均为黑色
- 仅使用填充色（不改变字体颜色）
- 混淆蓝色单元格与黑色单元格的用途

**存在的问题：**
- 无法区分输入数据与公式
- 无法进行审计追踪
- 违反了xlsx相关技能的要求

**推荐做法：** 所有硬编码的输入数据用蓝色显示，所有公式用黑色显示，工作表链接则用绿色显示

### 错误示例：运营费用基于毛利润计算

**切勿这样做：**
`销售与营销费用：=E33*0.15    // E33 = 毛利润（错误）`

**存在的问题：**
- 运营费用应随收入变化，而非毛利润
- 会导致利润率变化不切实际
- 不符合企业的实际运营方式
**正确写法：**
`S&M: =E29*0.15    // E29代表收入（正确）`

### 最常见的5大错误总结

1. **公式中行引用错误** → 在编写公式之前需先确定所有行的位置
2. **单元格缺少注释** → 应在创建单元格时立即添加注释，而非等到最后
3. **敏感性分析表过于简化** → 所有单元格都应使用完整的DCF重算公式，而非近似值
4. **情景分析模块引用错误** → 确保IF公式引用的分别是熊市/基准/牛市场景模块
5. **缺乏分隔线** → 应添加专业的分节线，以呈现符合客户要求的格式

此外，还需注意以下错误：

### WACC计算错误
- 资本结构中混用了账面价值与市场价值
- 错误地使用了股权贝塔值而非资产贝塔值或无杠杆贝塔值
- 对债务成本应用了错误的税率
- 无风险利率使用不当（必须采用当前10年期国债利率）
- 未对净债务与净现金状况进行适当调整

### 增长假设缺陷
- 终值增长率高于WACC（会导致估值无限增大）
- 预测增长率与历史表现不一致
- 未考虑行业增长限制
- 收入增长率与业务单元的经济模型不匹配
- 毛利率提升缺乏相应的运营依据

### 终值计算错误
- 选择了错误的增长方法（永续增长法 vs 出售倍数法）
- 终值占比超过企业价值的80%（表明过度依赖该假设）
- 终值毛利率与稳态假设不一致
- 终值的折现期限设置错误

### 现金流预测错误
- 以毛利润而非营收作为运营成本计算依据  
- 折旧与摊销费用/资本性支出的比例与业务模式不匹配  
- 流动资金变动未得到准确计算  
- 各年度税率存在不一致情况  
- 净经营资产收益率计算出现错误  

**这些错误最为常见。在开始构建任何现金流折现模型之前，请务必重新阅读本部分内容。**  

</common_mistakes>  

## Excel文件创建  

**该技能会使用`xlsx`技能来执行所有电子表格操作。** `xlsx`技能具备以下功能：  
- 标准化的公式构建规则  
- 数字格式设置规范  
- 通过`recalc.py`脚本实现公式自动重新计算  
- 全面的错误检测与验证功能  

该技能生成的所有Excel文件都必须符合`xlsx`技能的要求，包括杜绝公式错误并确保能够正确重新计算。  

## 质量评估标准  

每个现金流折现模型都应力求做到：  
1. 基于历史数据，设定**合理且现实**的营收与利润率假设  
2. 采用正确的资本资产定价模型方法，进行**恰当的资本成本计算**  
3. 提供**全面的敏感性分析**，明确显示估值范围  
4. 对终值进行**清晰明确的计算**，并附上相应的计算依据  
5. 拥有便于进行情景分析的**专业模型结构**  
6. 对所有关键假设提供**详尽透明的文档说明**  

## 输入要求  

### 最低必要输入项
1. **公司标识符**：股票代码或公司名称  
2. **增长假设**：预测期内的营收增长率（或选择市场共识值）  
3. **可选参数**：  
   - 预测期限（默认：5年）  
   - 不同情景设定（熊市/基准/牛市增长预期及利润率假设）  
   - 终值增长率（默认：2.5%-3.0%）  
   - 若未采用资本资产定价模型，则需输入特定的加权平均资本成本数值  

## Excel模型结构

### 工作表布局

需创建**两个工作表**：  

1. **DCF**——包含主要估值模型，底部附有敏感性分析结果  
2. **WACC**——用于计算资本成本  

**重要提示**：敏感性分析表格必须放在DCF工作表的底部（而非单独的工作表中），这样才能将所有估值结果集中呈现。  

### 公式重新计算（强制要求）

在创建或修改Excel模型后，必须使用`excel-author`技能中的`recalc.py`脚本来**重新计算所有公式**。

```bash
python recalc.py [path_to_excel_file] [timeout_seconds]
```

示例：
```bash
python recalc.py AAPL_DCF_Model_2025-10-12.xlsx 30
```

该脚本将执行以下操作：
- 使用 LibreOffice 重新计算所有工作表中的所有公式；
- 扫描所有单元格，检测 Excel 错误（如 #REF!、#DIV/0!、#VALUE!、#NAME?、#NULL!、#NUM!、#N/A）；
- 返回包含错误位置及出现次数的详细 JSON 数据。

**预期输出格式：**
```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {}             // Only present if errors found
}
```

**如果检测到错误**，输出结果中将包含相关详细信息：
```json
{
  "status": "errors_found",
  "total_errors": 2,
  "total_formulas": 42,
  "error_summary": {
    "#REF!": {
      "count": 2,
      "locations": ["DCF!B25", "DCF!C25"]
    }
  }
}
```

在交付模型之前，需**修正所有错误**并反复运行 recalc.py，直至状态显示为“success”。

### 格式标准

**重要提示**：请遵循 xlsx 技能中规定的公式构建规则与数字格式规范。DCF 技能则另有特定的视觉呈现标准。

**双层配色方案**：

**第一层：字体颜色（遵循 xlsx 技能的强制要求）**
- **蓝色文字（RGB: 0,0,255）**：所有硬编码输入值（股票价格、股数、历史数据及假设条件）
- **黑色文字（RGB: 0,0,0）**：所有公式与计算结果
- **绿色文字（RGB: 0,128,0）**：指向其他工作表的链接（如 WACC 工作表引用）

**第二层：填充颜色——专业蓝/灰色调（除非用户另有指定，否则默认使用此方案）**
- **保持极简风格**——仅使用蓝色和灰色作为填充色。严禁使用绿色、黄色、橙色或其他多种强调色。颜色过多的模型看起来会很业余。
- **默认填充色方案：**
  - **章节标题**：深蓝色背景（RGB：31,78,121 / `#1F4E79`），搭配白色粗体文字
  - **子标题/列标题**：浅蓝色背景（RGB：217,225,242 / `#D9E1F2`），搭配黑色粗体文字
  - **输入单元格**：浅灰色背景（RGB：242,242,242 / `#F2F2F2`），搭配蓝色字体；若追求极致极简，也可仅使用白色背景配蓝色字体
  - **计算结果单元格**：白色背景，搭配黑色字体
  - **输出/汇总行**（如每股价值、企业价值等）：中蓝色背景（RGB：189,215,238 / `#BDD7EE`），搭配黑色粗体文字
- **仅此而已——3种蓝色 + 1种灰色 + 白色。**请克制住添加更多颜色的冲动。
- 用户自定义的模板或明确的颜色偏好将始终优先于这些默认设置。

**各层颜色功能说明：**
- 输入单元格：蓝色字体 + 浅灰色填充 = “硬编码输入”
- 公式单元格：黑色字体 + 白色背景 = “计算结果”
- 工作表链接：绿色字体 + 白色背景 = “来自其他工作表的引用”
- 核心输出结果：黑色粗体字体 + 中蓝色填充 = “这是最终答案”

**字体颜色用于标识内容类型（输入/公式/链接），而填充颜色则用于指示所在位置（标题/数据/输出）。**

### 边框标准（专业外观的必备要求）

主要章节周围需设置**加粗边框**（1.5磅）：
- 关键输入项部分  
- 投资预测假设部分  
- 5年现金流预测部分  
- 终值部分  
- 估值汇总部分  
- 各敏感性分析表格  

各子部分之间的**中等宽度边框**（1磅）：  
- 公司概况与历史业绩对比  
- 增长假设与息税前利润率及自由现金流参数对比  

数据表格周围的**细线边框**（0.5磅）：  
- 不同情景假设表（看跌 | 基准 | 看涨 | 已选）  
- 历史数据与预测财务数据矩阵  

**无边框**：表格内的单个单元格（需保持整洁，便于阅读）  

**边框为必填项**——没有专业格式边框的模型无法直接呈交给客户。  

**数字格式**（遵循xlsx技能标准）：  
- **年份**：以文本字符串形式显示（例如“2024”，而非“2,024”）  
- **百分比**：`0.0%`（保留一位小数）  
- **货币**：百万级用`$,##0`格式；每股金额用`$,##0.00`格式——表头中必须明确标注单位（如“营收（百万美元）”）  
- **零值**：通过数字格式设置将所有零显示为“-”（例如`$,##0;($#,##0);-`）  
- **大数**：使用千位分隔符，格式为`#,##0`  
- **负数**：用括号表示，格式为`(#,##0)`（不可使用减号）  

**单元格注释**（所有硬编码输入项**必须**添加）：  

根据xlsx技能要求，所有硬编码值都必须附带说明其来源的单元格注释。格式如下：“来源：[系统/文档]，[日期]，[参考资料]，[如有网址请注明]”  

**重要提示**：需在创建单元格时立即添加注释，切勿延后至最后处理。  

### DCF模型表格的详细结构  

**第1部分：表头**
```csv
Row,Content
1,[Company Name] DCF Model
2,Ticker: [XXX] | Date: [Date] | Year End: [FYE]
3,Blank
4,Case Selector Cell (1=Bear 2=Base 3=Bull)
5,Case Name Display (formula: =IF([Selector]=1"Bear"IF([Selector]=2"Base""Bull")))
```

**第2节：市场数据（与案例无关）**
```csv
Item,Value
Current Stock Price,$XX.XX
Shares Outstanding (M),XX.X
Market Cap ($M),[Formula]
Net Debt ($M),XXX [or Net Cash if negative]
```

**第3节：DCF情景假设**

需为每种情景（看跌、基准、看涨）分别设置独立的假设模块，在这些模块中，与DCF模型相关的各项假设——如收入增长率、息税前利润率、税率、销售及管理费用占收入的比重、资本支出占收入的比重、净营运资本随收入变动的百分比、终端增长率以及加权平均资本成本——应按照预测年份的顺序横向排列。每个模块都必须包含节标题、显示预测年份（FY1、FY2等）的列标题行，以及数据行。具体的布局要求请参见《<correct_patterns>》章节中的“正确的假设表结构”说明。

**第4节：历史及预测财务数据**

应使用从各情景模块中提取数据的汇总列（例如“选定方案”），而非在每一行预测数据中都使用零散的IF函数。

```csv
Income Statement ($M),2020A,2021A,2022A,2023A,2024E,2025E,2026E
Revenue,XXX,XXX,XXX,XXX,[=E29*(1+$E$10)],[=F29*(1+$E$11)],[=G29*(1+$E$12)]
  % growth,XX%,XX%,XX%,XX%,[=E29/D29-1],[=F29/E29-1],[=G29/F29-1]
,,,,,,
Gross Profit,XXX,XXX,XXX,XXX,[=E29*E33],[=F29*F33],[=G29*G33]
  % margin,XX%,XX%,XX%,XX%,[=E33/E29],[=F33/F29],[=G33/G29]
,,,,,,
Operating Expenses:,,,,,,,
  S&M,XXX,XXX,XXX,XXX,[=E29*0.15],[=F29*0.14],[=G29*0.13]
  R&D,XXX,XXX,XXX,XXX,[=E29*0.12],[=F29*0.11],[=G29*0.10]
  G&A,XXX,XXX,XXX,XXX,[=E29*0.08],[=F29*0.07],[=G29*0.07]
  Total OpEx,XXX,XXX,XXX,XXX,[=E36+E37+E38],[=F36+F37+F38],[=G36+G37+G38]
,,,,,,
EBIT,XXX,XXX,XXX,XXX,[=E33-E39],[=F33-F39],[=G33-G39]
  % margin,XX%,XX%,XX%,XX%,[=E41/E29],[=F41/F29],[=G41/G29]
,,,,,,
Taxes,(XX),(XX),(XX),(XX),[=E41*$E$24],[=F41*$E$24],[=G41*$E$24]
  Tax rate,XX%,XX%,XX%,XX%,[=E43/E41],[=F43/F41],[=G43/G41]
,,,,,,
NOPAT,XXX,XXX,XXX,XXX,[=E41-E43],[=F41-F43],[=G41-G43]
```

**核心公式模式**：
- 收入增长计算：`=E29*(1+$E $10)`，其中 $E $10 为用于计算第一年增长率的汇总列
- 不推荐的方式：`=E29*(1+IF($B $6=1,$B $10,IF($B $6=2,$C $10,$D $10)))`

通过将相关逻辑集中处理，这种做法更加简洁、便于审计，同时也能有效避免公式错误。

**第5节：自由现金流计算**

**重要提示**：务必确认行引用指向正确的假设数据行。公式创建后应立即进行测试。

```csv
Cash Flow ($M),2020A,2021A,2022A,2023A,2024E,2025E,2026E
NOPAT,XXX,XXX,XXX,XXX,[=E45],[=F45],[=G45]
(+) D&A,XXX,XXX,XXX,XXX,[=E29*$E$21],[=F29*$E$21],[=G29*$E$21]
    % of Rev,XX%,XX%,XX%,XX%,[=E58/E29],[=F58/F29],[=G58/G29]
(-) CapEx,(XX),(XX),(XX),(XX),[=E29*$E$22],[=F29*$E$22],[=G29*$E$22]
    % of Rev,XX%,XX%,XX%,XX%,[=E60/E29],[=F60/F29],[=G60/G29]
(-) Δ NWC,(XX),(XX),(XX),(XX),[=(E29-D29)*$E$23],[=(F29-E29)*$E$23],[=(G29-F29)*$E$23]
    % of Δ Rev,XX%,XX%,XX%,XX%,[=E62/(E29-D29)],[=F62/(F29-E29)],[=G62/(G29-F29)]
,,,,,,
Unlevered FCF,XXX,XXX,XXX,XXX,[=E57+E58-E60-E62],[=F57+F58-F60-F62],[=G57+G58-G60-G62]
```

**行引用示例**（基于报表布局）：
- $E$$21 = 营业费用率假设值（合并列，第21行）
- $E$$22 = 资本支出率假设值（合并列，第22行）
- $E$$23 = 流动资产占比假设值（合并列，第23行）
- E29 = 当年营业收入（第29行）
- E45 = 当年税后经营利润（第45行）

**在输入公式之前**：请确认这些行号与实际报表布局一致。建议先测试一列，确认无误后再复制到其他列。

**第6节：折现与估值**
```csv
DCF Valuation,2024E,2025E,2026E,2027E,2028E,Terminal
Unlevered FCF ($M),XXX,XXX,XXX,XXX,XXX,
Period,0.5,1.5,2.5,3.5,4.5,
Discount Factor,0.XX,0.XX,0.XX,0.XX,0.XX,
PV of FCF ($M),XXX,XXX,XXX,XXX,XXX,
,,,,,,
Terminal FCF ($M),,,,,,,XXX
Terminal Value ($M),,,,,,,XXX
PV Terminal Value ($M),,,,,,,XXX
,,,,,,
Valuation Summary ($M),,,,,,
Sum of PV FCFs,XXX,,,,,
PV Terminal Value,XXX,,,,,
Enterprise Value,XXX,,,,,
(-) Net Debt,(XX),,,,,
Equity Value,XXX,,,,,
,,,,,,
Shares Outstanding (M),XX.X,,,,,
IMPLIED PRICE PER SHARE,$XX.XX,,,,,
Current Stock Price,$XX.XX,,,,,
Implied Upside/(Downside),XX%,,,,,
```

### WACC 表格结构

```csv
COST OF EQUITY CALCULATION,,
Risk-Free Rate (10Y Treasury),X.XX%,[Yellow input]
Beta (5Y monthly),X.XX,[Yellow input]
Equity Risk Premium,X.XX%,[Yellow input]
Cost of Equity,X.XX%,[Calculated blue]
,,
COST OF DEBT CALCULATION,,
Credit Rating,AA-,[Yellow input]
Pre-Tax Cost of Debt,X.XX%,[Yellow input]
Tax Rate,XX.X%,[Link to DCF sheet]
After-Tax Cost of Debt,X.XX%,[Calculated blue]
,,
CAPITAL STRUCTURE,,
Current Stock Price,$XX.XX,[Link to DCF]
Shares Outstanding (M),XX.X,[Link to DCF]
Market Capitalization ($M),"X,XXX",[Calculated]
,,
Total Debt ($M),XXX,[Yellow input]
Cash & Equivalents ($M),XXX,[Yellow input]
Net Debt ($M),XXX,[Calculated]
,,
Enterprise Value ($M),"X,XXX",[Calculated]
,,
WACC CALCULATION,Weight,Cost,Contribution
Equity,XX.X%,X.X%,X.XX%
Debt,XX.X%,X.X%,X.XX%
,,
WEIGHTED AVERAGE COST OF CAPITAL,X.XX%,[Green output]
```

**关键WACC计算公式：**
```
Market Cap = Price × Shares
Net Debt = Total Debt - Cash
Enterprise Value = Market Cap + Net Debt
Equity Weight = Market Cap / EV
Debt Weight = Net Debt / EV
WACC = (Cost of Equity × Equity Weight) + (After-tax Cost of Debt × Debt Weight)
```

### 敏感性分析（DCF表格底部）

**术语说明**：“敏感性表格”指的是具有行标题、列标题以及每个数据单元格中公式内容的简单二维网格，而非Excel中的“数据表”功能（路径：数据 → 假设分析 → 数据表）。您需要使用openpyxl在每个单元格中输入常规的Excel公式。

**位置**：DCF表格的第87行及以后（并非单独的页面）

**共三个垂直堆叠的敏感性表格**：

1. **加权平均资本成本与终端增长率**（第87-100行）——5×5网格，共25个包含公式的单元格
2. **营收增长率与息税前利润率**（第102-115行）——5×5网格，共25个包含公式的单元格
3. **贝塔系数与无风险利率**（第117-130行）——5×5网格，共25个包含公式的单元格

**需输入的公式总数：75个**（此项为必做要求，非可选）

**重要提示**：所有敏感性表格的单元格都必须通过openpyxl以编程方式填充公式，严禁使用线性近似等简化手段。不得留下占位文本或关于手动操作的说明，也绝不能以“内容过于复杂”为由让某些单元格保持空白——应使用Python循环来生成这些公式。

**表格设置：**
1. 创建包含行/列标题的表格结构（即用于测试的假设数值）。
2. 为每个数据单元格填入公式，该公式需满足以下要求：
   - 使用行标题对应的数值（例如：WACC = 9.0%）
   - 使用列标题对应的数值（例如：Terminal Growth = 3.0%）
   - 基于这些特定假设重新计算完整的DCF模型
   - 输出该情景下的预期股价
3. 交付的文件中所有单元格都必须包含可正常运行的公式。
4. 使用条件格式设置单元格样式：数值较高时显示为绿色，数值较低时显示为红色。
5. 将基准情景对应的单元格加粗显示。
6. 表格之间需留出1-2行空白。

**无需人工干预**——用户打开文件时，这些敏感性分析表格必须能够完全正常使用。

## 情景选择器实现方案

**三情景框架：**

### 谨慎情景
- 保守的收入增长预期（处于历史数据区间的较低水平）
- 利润率要么保持不变，要么出现下滑
- 更高的WACC值（风险溢价上升）
- 更低的长期增长率
- 更高的资本支出假设

### 基准情景
- 市场普遍预期或管理层给出的收入增长目标
- 基于运营杠杆效应的适度利润率提升
- 当前市场所反映的WACC值
- 与GDP增长水平相匹配的长期增长率（2.5-3.0%）
- 标准的资本支出假设

### 乐观情景
- 乐观的收入增长预期（处于预测区间的较高水平）
- 显著的利润率提升
- 更低的WACC值（风险溢价下降）
- 更高的长期增长率（3.5-5.0%）
- 较低的资本支出强度

**公式实现方式：**

**请勿在模型中随意使用嵌套的IF公式。** 相反，应创建一个汇总列，通过INDEX或OFFSET公式从对应的情景模块中提取数据。

**推荐用法（使用INDEX函数）：**
`=INDEX(B10:D10, 1, $B$$6)`，其中`B10:D10`代表熊市/基准/牛市下的数值，`1`表示行偏移量，`$,B$$6`则为情景选择单元格（1、2或3）。

**在所有预测中均引用该汇总列：**
`第一年营收：=D29*(1+$E$$10)`，此处`E$$10`即为第一年增长对应的汇总列数值。

这种做法可将情景逻辑集中管理，从而提升模型的可审计性与可维护性。

## 输出文件结构

**文件命名**：`[股票代码]_DCF_Model_[日期].xlsx`

**包含两个工作表**：
1. **DCF**——完整的模型，包含熊市/基准/牛市三种情景，页面底部还附有三张敏感性分析表（加权平均资本成本与终端增长率、营收增长率与息税前利润率、贝塔值与无风险利率）。
2. **WACC**——用于计算资本成本的表格。

**核心功能**：情景选择器（1/2/3）、包含INDEX/OFFSET公式的汇总列、彩色标注的单元格、所有输入参数旁的注释说明，以及专业风格的边框设计。

## 最佳实践

### 模型构建
1. **逐步完善**：完成一个部分后再进入下一环节。
2. **边建边测试**：输入示例数值以验证公式是否正确。
3. **保持结构统一**：相似的计算应遵循相同的格式。
4. **为复杂公式添加注释**：对特殊计算方式予以说明。
5. **内置校验机制**：在适用情况下加入求和校验与平衡校验。

### 文档编写
1. **记录所有假设**：说明关键输入参数的依据  
2. **标注数据来源**：注明每个数据点的出处  
3. **阐述方法论**：描述任何非标准化的处理方式  
4. **标明不确定性**：突出那些信息透明度较低的领域  

### 质量控制  
1. **交叉验证计算结果**：通过多种方法核验数学运算  
2. **对假设进行压力测试**：通过敏感性分析确保模型稳健性  
3. **同行评审**：请他人检查公式与逻辑  
4. **版本控制**：在项目进展过程中保存不同版本  

## 常见场景差异  

### 高速成长型科技公司  
- 更长的预测周期（7-10年）  
- 较高的初始增长率（20-30%）  
- 随时间推移利润率显著提升  
- 较高的加权平均资本成本（12-15%）  
- 需分析模型中的核心经济指标（用户数量、每用户平均收入等）  

### 成熟/稳定型公司  
- 较短的预测周期（3-5年）  
- 适度的增长率（与GDP增长水平相当，约1-3%）  
- 相对稳定的利润率  
- 较低的加权平均资本成本（7-9%）  
- 重点关注现金生成能力与资本配置策略  

### 周期性行业公司  
- 需将模型扩展至完整经济周期  
- 以周期中点作为利润率基准  
- 需考虑经济低谷与高峰两种情景  
- 根据周期性特征调整相关参数值  

### 多业务板块公司  
- 为每个业务单元分别构建DCF模型  
- 不同业务板块采用差异化的增长率与利润率  
- 采用分部加总法进行估值  
- 需评估业务协同效应  

## 故障排除  

**如果遇到错误或不合理的结果，请查阅 [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) 以获取详细的调试指南。**  

## 工作流程整合  

### 在构建DCF模型之初

1. **收集市场数据**：
   - 查找可用于获取当前市场数据的MCP服务器
   - 通过网络搜索或数据抓取方式获取股票价格、贝塔值及其他市场指标
   - 若需要特定数据，则向用户请求

2. **收集历史财务数据**：
   - 查找可用的MCP服务器（如Daloopa等）
   - 若无法通过MCP获取，则向用户请求
   - 必要时手动从10-K年度报告中提取数据

3. **按照本技能中详述的DCF方法开始构建模型**

### 模型构建期间

1. **使用openpyxl库创建Excel模型**，公式需动态生成（而非硬编码数值）
2. **遵循xlsx技能相关的规范**来设置公式及格式
3. 仅在用户提出要求或提供了特定品牌指南时，才应用填充颜色

### 模型交付前（必须完成）

1. **验证结构**：
   - 为熊市/基准市场/牛市场景设置各预测年份的假设条件
   - 配备案例选择功能，公式需正确引用对应场景块
   - DCF表格底部放置敏感性分析表（不得另建表格）
   - 字体颜色规范：输入数据用蓝色，公式用黑色，表格链接用绿色
   - 所有硬编码输入值均需添加单元格注释
   - 各主要板块周围设置专业边框

2. **重新计算公式**：运行命令 `python recalc.py model.xlsx 30`

3. **检查输出结果**：
   - 若`status`显示为“success” → 继续执行第4步
   - 若`status`显示为“errors_found” → 查看`error_summary`内容，并参阅[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)获取调试指导

4. **修正错误后再次运行recalc.py**，直至状态变为“success”

5. **抽查公式正确性**：
   - 测试一个自由现金流公式——确认其是否引用了正确的假设行
   - 更改案例选择选项——检查合并列是否同步更新
   - 确认收入计算公式引用的是合并列数据（而非嵌套的IF函数）

6. **交付模型**

### 可用的数据来源

- **MCP服务器**：如已配置，可用于获取历史财务数据（Daloopa平台）
- **网络搜索/抓取**：用于获取当前股票价格、贝塔值及市场数据
- **用户提供的数据**：历史财务报表、市场共识预期值
- **手动提取**：作为备用方案，可从SEC EDGAR数据库中获取数据

## 最终交付检查清单

在提交DCF模型之前：

**必填项：**
- 运行 `python recalc.py model.xlsx 30`，直至状态显示为“success”（即无公式错误）。
- 文件包含两个工作表：DCF（底部附有敏感性分析）以及WACC。
- 字体颜色规则：蓝色代表输入数据，黑色代表公式，绿色代表工作表链接。
- 所有硬编码的输入数据旁均配有单元格注释。
- 敏感性分析表格中已填入完整的公式。
- 各主要板块周围均有专业的边框设计。

**验证规则：**
- 运营费用需基于营业收入计算（而非毛利润）。
- 终值应占企业价值的50%至70%。
- 终值增长率须低于WACC。
- 税率应在21%至28%之间。
- 文件命名规则为：`[Ticker]_DCF_Model_[Date].xlsx`。

## 数据来源 —— 首选MCP，网络检索作为备选

下文多处提到“使用S&P Kensho MCP / Daloopa MCP / FactSet MCP”。这些均为源自原有Cowork插件环境的商业金融数据MCP服务。在Hermes系统中：
- **如果您已配置了任何结构化的金融数据MCP**（Hermes支持MCP功能，详见`native-mcp`技能），则优先使用它们来获取特定时间点的财务数据、历史交易案例及监管文件信息。
- **若未配置此类MCP**，可采取以下备选方案：
  - 对于美国市场的监管文件，可通过SEC EDGAR网站（`https://www.sec.gov/cgi-bin/browse-edgar`）使用`web_search`/`web_extract`功能进行检索；
  - 从公司官网的投资者关系页面获取新闻稿和财报材料；
  - 使用`browser_navigate`功能访问交互式数据平台；
  - 接收用户提供的数据（当上下文信息不足时需主动询问用户）。
- **严禁编造数据**。如果无法找到倍数、历史案例或监管文件编号，应将该单元格标记为`[UNSOURCED]`，并向用户显示这一情况。

## 出处标注

该智能体技能基于 Anthropic 的 Claude for Financial Services 插件套件（Apache-2.0 许可协议）开发。原版本中用于处理 Office-JS 和 Cowork 在线 Excel 文件的功能已被移除；当前版本则遵循 `excel-author` 智能体技能的规范，通过无界面方式调用 openpyxl 库来实现相应功能。原始代码地址：https://github.com/anthropics/financial-services
