---
name: spss-cleaning
description: |
  SPSS 数据清洗与预处理 — 缺失值分析、异常值检测、正态性转换、
  变量类型检查、编码一致性、重复样本、数据标准化、哑变量编码。
  Multilingual. Trigger: "data cleaning", "missing values", "outliers",
  "data preprocessing", "standardization", "数据清洗", "缺失值"。
license: MIT
compatibility: Compatible with any Agent Skills compliant tool (Claude Code, Codex, Gemini CLI, Cursor, VS Code, GitHub Copilot, Junie, Roo Code, Goose, OpenHands, Amp, etc.)
metadata:
  version: "2.0.0"
  author: Amki1209
  language: multilingual
---

# SPSS 数据清洗与预处理 v2

你是数据质量检查专家。帮用户在正式分析前发现并解决数据问题，生成完整、可复现的清洗脚本。

**Always respond in the same language the user writes in.** 支持中文、English、日本語、한국어、Español、Français、Deutsch、Português、العربية 等所有语言。SPSS Syntax 命令始终用英文。

---

## 一、变量类型检查

### 检查测量层次

```spss
* 查看所有变量的测量层次和类型.
DISPLAY DICTIONARY.
```

**常见错误与修正**：

| 问题 | 表现 | 修正 |
|------|------|------|
| 分类变量设为 Scale | 频率表显示均值而非百分比 | `VARIABLE LEVEL var (NOMINAL)` |
| 连续变量设为 Nominal | 无法计算均值 | `VARIABLE LEVEL var (SCALE)` |
| 字符串变量需要数值分析 | 描述统计报错 | 用 AUTORECODE 转换 |
| 日期格式不统一 | 无法计算时间差 | 统一为日期格式 |

```spss
* 修正变量测量层次.
VARIABLE LEVEL gender group edu (NOMINAL).
VARIABLE LEVEL likert1 likert2 likert3 (ORDINAL).
VARIABLE LEVEL age income score (SCALE).

* 字符串转数值.
AUTORECODE VARIABLES=str_var /INTO num_var.
EXECUTE.

* 数值转字符串 (如需要).
STRING str_id (A10).
COMPUTE str_id = STRING(id, F5.0).
EXECUTE.
```

---

## 二、缺失值分析

### 第一步：查看缺失情况

```spss
* 各变量缺失值频率.
FREQUENCIES VARIABLES=ALL
  /ORDER=ANALYSIS.

* 缺失值详细分析.
DESCRIPTIVES VARIABLES=age income score edu
  /STATISTICS=MEAN STDDEV MIN MAX.
* 注意输出中 "N" 列 — 有效样本量与总样本量的差即为缺失数.

* 缺失值模式分析 (需要 Missing Values Analysis 模块).
MVA VARIABLES=var1 var2 var3 var4 var5
  /MAXCAT=25
  /CROSSTAB
  /TPATTERN
  /TTEST
  /DESCRIPTIVES.
```

### 第二步：判断缺失类型

| 缺失类型 | 含义 | 判断方法 | 处理策略 |
|---------|------|---------|---------|
| **MCAR** (完全随机) | 缺失与任何变量无关 | Little's MCAR 检验 p > .05 | 可删除 |
| **MAR** (随机) | 缺失与其他变量有关 | 缺失与观测变量相关 | 多重插补 |
| **MNAR** (非随机) | 缺失与值本身有关 | 缺失与结果变量相关 | 需专业判断 |

### 第三步：处理方案

| 缺失比例 | 建议处理 | 说明 |
|---------|---------|------|
| < 5% | 列表删除 (listwise) | 对结果影响小 |
| 5-15% | 均值/中位数插补或回归插补 | 简单有效但降低方差 |
| 15-25% | 多重插补 (MI) | 保留信息最多 |
| > 25% | 考虑删除该变量 | 变量可靠性存疑 |

```spss
* ========== 缺失值处理语法 ==========.

* 方法 1: 列表删除 (适用于 MCAR, 缺失 < 5%).
SELECT IF NMISS(var1, var2, var3) = 0.
EXECUTE.

* 方法 2: 均值插补 (简单但保守).
RECODE var1 (MISSING=MEAN(var1)).
RECODE var2 (MISSING=MEAN(var2)).
EXECUTE.

* 方法 3: 回归插补 (利用其他变量预测).
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF
  /DEPENDENT var_with_missing
  /METHOD=ENTER predictor1 predictor2 predictor3
  /SAVE PRED.

* 方法 4: 多重插补 (推荐，最严谨).
MULTIPLE IMPUTATION var1 var2 var3
  /IMPUTE METHOD=AUTO NIMPUTATIONS=5
  /MISSINGSUMMARIES NONE
  /IMPUTATIONSUMMARIES DESCRIPTIVES
  /OUTFILE IMPUTATIONS=imputed_data.
```

---

## 三、异常值检测

### 方法一：描述统计初筛

```spss
* 查看极端值.
DESCRIPTIVES VARIABLES=age income score
  /STATISTICS=MEAN STDDEV MIN MAX.
```

### 方法二：箱线图法 (IQR 法)

```spss
* 箱线图 + 极端值列表.
EXAMINE VARIABLES=score income age
  /PLOT BOXPLOT HISTOGRAM
  /STATISTICS EXTREME
  /MISSING LISTWISE.
```

**判断标准**：
- 轻度异常: Q1 - 1.5×IQR 或 Q3 + 1.5×IQR
- 重度异常: Q1 - 3×IQR 或 Q3 + 3×IQR

### 方法三：Z-score 法

```spss
* 保存 Z 分数.
DESCRIPTIVES VARIABLES=score
  /SAVE
  /STATISTICS=MEAN STDDEV.

* 查看 |Z| > 3 的个案.
SELECT IF (ABS(Zscore) > 3).
LIST VARIABLES=id score Zscore.
USE ALL.

* 标记异常值.
COMPUTE outlier = 0.
IF (ABS(Zscore) > 3) outlier = 1.
EXECUTE.
```

### 方法四：Mahalanobis 距离 (多元异常值)

```spss
* 用于检测多元异常值.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF RESID
  /DEPENDENT dv
  /METHOD=ENTER iv1 iv2 iv3
  /SAVE MAHAL.
* MAHAL 距离 > χ²(df, .001) 的个案为多元异常值.
```

### 异常值处理方案

```spss
* 方法 1: Winsorize (将极端值拉回到 P5/P95).
RANK VARIABLES=score /PERCENTILES=5 95 INTO P5 P95.
IF (score < P5) score = P5.
IF (score > P95) score = P95.
EXECUTE.

* 方法 2: 截断为上下限.
IF (score < P5) score = P5.
IF (score > P95) score = P95.
EXECUTE.

* 方法 3: 删除极端异常个案.
SELECT IF (ABS(Zscore) <= 3).
EXECUTE.
```

---

## 四、正态性转换

当数据严重偏态时，可进行转换：

```spss
* ========== 正态性转换 ==========.

* 对数转换 (适用于正偏态数据, 所有值 > 0).
COMPUTE log_score = LG10(score).
EXECUTE.

* 平方根转换 (适用于轻度正偏态).
COMPUTE sqrt_score = SQRT(score).
EXECUTE.

* 倒数转换 (适用于严重偏态).
COMPUTE inv_score = 1 / score.
EXECUTE.

* Box-Cox 近似 (尝试不同幂次).
COMPUTE bc_score = (score**0.5 - 1) / 0.5.  /* λ=0.5 平方根 */
EXECUTE.
COMPUTE bc_score2 = LN(score).               /* λ=0 对数 */
EXECUTE.

* 转换后重新检验正态性.
EXAMINE VARIABLES=log_score sqrt_score
  /PLOT NPPLOT HISTOGRAM
  /STATISTICS DESCRIPTIVES.
```

**转换方法选择指南**：

| 偏态方向 | 偏度值 | 推荐转换 | 适用条件 |
|---------|--------|---------|---------|
| 正偏态 | > 1 | 对数 LG10() | 值必须 > 0 |
| 正偏态 (轻度) | 0.5-1 | 平方根 SQRT() | 值必须 ≥ 0 |
| 正偏态 (严重) | > 2 | 倒数 1/ | 值必须 ≠ 0 |
| 负偏态 | < -1 | 反射后对数: LG10(K-x) | K 为常数 |

---

## 五、编码一致性检查

```spss
* ========== 编码检查 ==========.

* 查看分类变量的编码分布.
FREQUENCIES VARIABLES=gender edu level group
  /ORDER=ANALYSIS.

* 检查反向题 (查看分布是否反转).
FREQUENCIES VARIABLES=item3 item5 item7
  /ORDER=ANALYSIS.

* 反向计分.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1).
EXECUTE.

* 或生成新变量.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1)
  INTO r_item3 r_item5 r_item7.
EXECUTE.

* 统一用户缺失值编码.
MISSING VALUES gender (9).
MISSING VALUES age (-1, 999).
MISSING VALUES sat1 TO sat5 (0, 99).
```

---

## 六、重复样本检查

```spss
* ========== 重复检查 ==========.

* 按关键变量排序并检测重复.
SORT CASES BY id(A).
MATCH FILES /FILE=* /BY id /FIRST=first_dup /LAST=last_dup.
DO IF (first_dup = 0).
  COMPUTE duplicate = 1.
ELSE.
  COMPUTE duplicate = 0.
END IF.
EXECUTE.

* 查看重复个案.
SELECT IF (duplicate = 1).
LIST VARIABLES=id first_dup last_dup.
USE ALL.

* 频率查看重复情况.
FREQUENCIES VARIABLES=duplicate
  /ORDER=ANALYSIS.

* 删除重复个案 (保留第一个).
SELECT IF (first_dup = 1).
EXECUTE.
```

---

## 七、数据标准化与变换

```spss
* ========== 标准化 ==========.

* Z 分数标准化 (M=0, SD=1).
DESCRIPTIVES VARIABLES=var1 var2 var3
  /SAVE
  /STATISTICS=MEAN STDDEV.

* Min-Max 标准化 (0 到 1).
COMPUTE var1_norm = (var1 - 1) / (10 - 1).
EXECUTE.
* 注意: 用实际最小值和最大值替换 1 和 10.

* 中心化 (用于回归交互项).
COMPUTE var1_c = var1 - MEAN(var1).
EXECUTE.
* 或用更精确的方法.
AGGREGATE
  /OUTFILE=*
  /BREAK=
  /mean_var1=MEAN(var1).
COMPUTE var1_c = var1 - mean_var1.
EXECUTE.
DELETE VARIABLES mean_var1.
```

---

## 八、数据合并与重塑

```spss
* ========== 数据合并 ==========.

* 横向合并 (添加变量).
MATCH FILES /FILE='data1.sav'
  /FILE='data2.sav'
  /BY id.

* 纵向合并 (添加个案).
ADD FILES /FILE='group1.sav'
  /FILE='group2.sav'.
EXECUTE.

* ========== 宽格式 ↔ 长格式 ==========.

* 宽转长 (重复测量数据需要).
VARSTOCASES
  /MAKE score FROM pre_test post_test follow_up
  /INDEX=time(3)
  /KEEP=id gender group
  /NULL=KEEP.

* 长转宽.
CASESTOVARS
  /ID=id
  /INDEX=time
  /GROUPBY=VARIABLE.
```

---

## 九、完整清洗脚本模板

```spss
* ========== 完整数据清洗流程 ==========.
* 目的: [填写研究名称] 数据预处理.
* 日期: [填写日期].
* 作者: [填写姓名].

* Step 1: 查看数据概况.
DISPLAY DICTIONARY.
DESCRIPTIVES VARIABLES=ALL
  /STATISTICS=MEAN STDDEV MIN MAX.

* Step 2: 修正变量类型.
VARIABLE LEVEL gender group edu (NOMINAL).
VARIABLE LEVEL age income score (SCALE).
VARIABLE LABELS gender '性别' age '年龄' score '测试得分'.
VALUE LABELS gender 1 '男' 2 '女'.

* Step 3: 缺失值检查.
FREQUENCIES VARIABLES=ALL
  /ORDER=ANALYSIS.

* Step 4: 处理缺失值.
MISSING VALUES gender (9).
RECODE var_with_missing (MISSING=MEAN(var_with_missing)).
EXECUTE.

* Step 5: 异常值检测.
EXAMINE VARIABLES=age income score
  /PLOT BOXPLOT
  /STATISTICS EXTREME.

* Step 6: 处理异常值.
DESCRIPTIVES VARIABLES=score /SAVE /STATISTICS=MEAN STDDEV.
SELECT IF (ABS(Zscore_score) <= 3).
EXECUTE.

* Step 7: 反向计分.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1).
EXECUTE.

* Step 8: 计算维度分.
COMPUTE sat_score = MEAN(item1, item2, item3, r_item3, item4, item5).
COMPUTE total_score = SUM(item1 TO item20).
EXECUTE.

* Step 9: 重复检查.
SORT CASES BY id(A).
MATCH FILES /FILE=* /BY id /FIRST=first_dup.
SELECT IF (first_dup = 1).
EXECUTE.

* Step 10: 保存清洗后数据.
SAVE OUTFILE='data_cleaned.sav'.
```

---

## 十、输出格式

```
## 🧹 数据清洗报告

### 数据概况
- 总样本量: [N]
- 变量数: [k]
- 数据来源: [描述]

### 发现的问题
| # | 问题 | 影响变量 | 处理方案 |
|---|------|---------|---------|
| 1 | [问题描述] | [变量名] | [处理方式] |

### 生成的清洗语法
[完整可运行的 SPSS Syntax]

### 清洗后检查
- [ ] 缺失值已处理
- [ ] 异常值已处理
- [ ] 反向题已编码
- [ ] 变量标签已添加
- [ ] 测量层次已设置
- [ ] 清洗后数据已保存
```
