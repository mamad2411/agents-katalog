---
name: spss-syntax
description: |
  SPSS Syntax 语法生成器 — 根据分析需求自动生成可复现的 SPSS Syntax，
  支持批处理、错误排查、宏技巧、数据导入导出。
  Multilingual. Trigger: "SPSS syntax", "generate syntax", "SPSS code",
  "batch analysis", "syntax error", "自动化", "宏"。
license: MIT
compatibility: Compatible with any Agent Skills compliant tool (Claude Code, Codex, Gemini CLI, Cursor, VS Code, GitHub Copilot, Junie, Roo Code, Goose, OpenHands, Amp, etc.)
metadata:
  version: "2.0.0"
  author: Amki1209
  language: multilingual
---

# SPSS Syntax 语法生成器 v2

你是 SPSS Syntax 专家。根据用户描述的分析需求，生成规范、带注释、可直接运行的 SPSS 语法。

**Always respond in the same language the user writes in.** 支持中文、English、日本語、한국어、Español、Français、Deutsch、Português、العربية 等所有语言。SPSS Syntax 命令始终用英文（这是 SPSS 本身的要求）。

**格式规范**：
- 每个命令以句号 `.` 结尾
- `*` 开头为注释
- 命令关键字不区分大小写
- 变量名必须与数据文件中完全一致
- 每段语法前注明目的和适用场景

---

## 一、数据管理基础

### 打开 / 保存 / 导入数据

```spss
* ========== 数据文件操作 ==========.

* 打开 SPSS 数据文件.
GET FILE='C:\data\mydata.sav'.
DATASET NAME mydata.

* 保存数据文件.
SAVE OUTFILE='C:\data\cleaned.sav'
  /COMPRESSED.

* 从 Excel 导入.
GET DATA /TYPE=XLSX
  /FILE='C:\data\mydata.xlsx'
  /SHEET=name 'Sheet1'
  /CELLRANGE=FULL
  /READNAMES=ON.

* 从 CSV 导入.
GET DATA /TYPE=TXT
  /FILE='C:\data\mydata.csv'
  /DELCASE=LINE
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=
    id F5.0
    gender F1.0
    age F3.0
    score F5.2.

* 导出为 Excel.
SAVE TRANSLATE OUTFILE='C:\output\results.xlsx'
  /TYPE=XLSX
  /VERSION=12
  /MAP
  /REPLACE
  /FIELDNAMES
  /CELLS=VALUES.
```

### 变量定义与标签

```spss
* ========== 变量定义 ==========.

* 添加变量标签 (中文说明).
VARIABLE LABELS
  id '被试编号'
  gender '性别'
  age '年龄'
  edu '教育程度'
  income '月收入'
  sat1 '满意度题项1'
  sat2 '满意度题项2'
  sat3 '满意度题项3'.

* 添加值标签.
VALUE LABELS gender 1 '男' 2 '女'.
VALUE LABELS edu 1 '高中及以下' 2 '大专' 3 '本科' 4 '硕士' 5 '博士及以上'.
VALUE LABELS group 1 '实验组' 2 '对照组'.

* 设置测量层次.
VARIABLE LEVEL id gender group edu (NOMINAL).
VARIABLE LEVEL likert1 likert2 likert3 (ORDINAL).
VARIABLE LEVEL age income score (SCALE).

* 设置用户缺失值.
MISSING VALUES gender (9).
MISSING VALUES age (-1, 999).
MISSING VALUES sat1 TO sat5 (0).

* 重命名变量.
RENAME VARIABLES (old_var = new_var).
```

### 变量计算与转换

```spss
* ========== 变量计算 ==========.

* 计算新变量.
COMPUTE total_score = SUM(item1 TO item10).
COMPUTE mean_score = MEAN(item1 TO item10).
COMPUTE ratio = income / family_size.
EXECUTE.

* 条件计算.
IF (age < 18) age_group = 1.
IF (age >= 18 & age < 30) age_group = 2.
IF (age >= 30 & age < 50) age_group = 3.
IF (age >= 50) age_group = 4.
EXECUTE.

* 反向计分.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1).
EXECUTE.

* 或保留原变量，生成新变量.
RECODE item3 item5 item7 (1=5)(2=4)(3=3)(4=2)(5=1)
  INTO r_item3 r_item5 r_item7.
EXECUTE.

* 重编码为分类变量.
RECODE score (LOWEST THRU 59=1)(60 THRU 79=2)(80 THRU HIGHEST=3)
  INTO score_level.
VALUE LABELS score_level 1 '不及格' 2 '及格' 3 '优秀'.
EXECUTE.

* 标准化 (Z 分数).
DESCRIPTIVES VARIABLES=score1 score2 score3
  /SAVE
  /STATISTICS=MEAN STDDEV.

* 数据标准化 (Min-Max 到 0-1).
COMPUTE score_norm = (score - 0) / (100 - 0).
EXECUTE.

* 虚拟变量编码 (为回归分析准备).
RECODE edu (1=0)(2=0)(3=1)(4=0)(5=0) INTO edu_ba.
RECODE edu (1=0)(2=0)(3=0)(4=1)(5=0) INTO edu_ma.
EXECUTE.
* 注意: 参照组 (如 edu=5 博士) 不需要创建虚拟变量.
```

### 个案选择与筛选

```spss
* ========== 个案管理 ==========.

* 按条件选择个案.
USE ALL.
FILTER BY gender.
EXECUTE.

* 按范围选择.
SELECT IF (age >= 18 AND age <= 65).
EXECUTE.

* 取消选择，恢复全部个案.
USE ALL.
FILTER OFF.

* 加权个案 (适用于汇总数据).
WEIGHT BY freq_var.

* 拆分文件: 按组分别执行后续分析.
SORT CASES BY group.
SPLIT FILE LAYERED BY group.

* 取消拆分.
SPLIT FILE OFF.

* 删除个案.
SELECT IF (id ~= 999).
EXECUTE.
```

---

## 二、描述统计

```spss
* ========== 描述统计 ==========.

* 频率分析 (分类变量).
FREQUENCIES VARIABLES=gender edu group
  /BARCHART FREQ PERCENT
  /ORDER=ANALYSIS.

* 描述统计 (连续变量).
DESCRIPTIVES VARIABLES=age income score
  /STATISTICS=MEAN STDDEV MIN MAX SKEWNESS KURTOSIS.

* 探索性分析 (含正态性检验和箱线图).
EXAMINE VARIABLES=score BY group
  /PLOT BOXPLOT HISTOGRAM NPPLOT
  /COMPARE GROUPS
  /STATISTICS DESCRIPTIVES EXTREME
  /CINTERVAL 95
  /MISSING LISTWISE
  /NOTOTAL.

* 交叉表.
CROSSTABS
  /TABLES=gender BY edu
  /FORMAT=AVALUE TABLES
  /STATISTICS=CHISQ CC PHI
  /CELLS=COUNT ROW COLUMN TOTAL EXPECTED
  /COUNT ROUND CELL
  /BARCHART.
```

---

## 三、比较均值

```spss
* ========== t 检验 ==========.

* 单样本 t 检验 (与已知值比较).
T-TEST
  /TESTVAL=50
  /VARIABLES=score
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

* 独立样本 t 检验.
T-TEST GROUPS=group(1 2)
  /VARIABLES=score
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

* 配对样本 t 检验.
T-TEST PAIRS=pre_test WITH post_test (PAIRED)
  /ES DISPLAY(TRUE)
  /CRITERIA=CI(.95).

* ========== ANOVA ==========.

* 单因素 ANOVA.
ONEWAY score BY group
  /STATISTICS DESCRIPTIVES HOMOGENEITY WELCH
  /PLOT MEANS
  /MISSING ANALYSIS
  /POSTHOC=TUKEY BONFERRONI ALPHA(0.05).

* 双因素 ANOVA.
UNIANOVA score BY factorA factorB
  /METHOD=SSTYPE(3)
  /INTERCEPT=INCLUDE
  /POSTHOC=factorA factorB(TUKEY)
  /PLOT=PROFILE(factorA*factorB) TYPE=LINE ERRORBAR=CI MEANREFERENCE=NO
  /PRINT=ETASQ DESCRIPTIVE HOMOGENEITY
  /CRITERIA=ALPHA(.05)
  /DESIGN=factorA factorB factorA*factorB.

* 重复测量 ANOVA.
GLM time1 time2 time3
  /WSFACTOR=time 3 Polynomial
  /MEASURE=score
  /POSTHOC=time(BONFERRONI)
  /PLOT=PROFILE(time) TYPE=LINE ERRORBAR=CI MEANREFERENCE=NO
  /PRINT=ETASQ DESCRIPTIVE
  /WSDESIGN=time.

* ========== 非参数检验 ==========.

* Mann-Whitney U (两独立样本).
NPTESTS
  /INDEPENDENT TEST (score) GROUP (group) MANN_WHITNEY
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.

* Kruskal-Wallis (多独立样本).
NPTESTS
  /INDEPENDENT TEST (score) GROUP (group) KRUSKAL_WALLIS(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.

* Wilcoxon (两配对样本).
NPTESTS
  /RELATED TEST(pre_test post_test) WILCOXON
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.

* Friedman (多配对样本).
NPTESTS
  /RELATED TEST(time1 time2 time3) FRIEDMAN(COMPARE=PAIRWISE)
  /MISSING SCOPE=ANALYSIS USERMISSING=EXCLUDE.

* McNemar (配对分类变量).
NPAR TESTS
  /MCNEMAR=before WITH after (PAIRED).
```

---

## 四、相关分析

```spss
* ========== 相关分析 ==========.

* Pearson 相关.
CORRELATIONS
  /VARIABLES=var1 var2 var3 var4
  /PRINT=TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.

* Spearman 秩相关.
NONPAR CORR
  /VARIABLES=var1 var2 var3 var4
  /PRINT=SPEARMAN TWOTAIL NOSIG FULL
  /MISSING=PAIRWISE.

* 偏相关 (控制第三变量).
PARTIAL CORR
  /VARIABLES=var1 var2 BY control_var
  /SIGNIFICANCE=TWOTAIL
  /MISSING=LISTWISE.
```

---

## 五、回归分析

```spss
* ========== 线性回归 ==========.

* 简单线性回归.
REGRESSION
  /DESCRIPTIVES MEAN STDDEV CORR SIG N
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS CI(95) R ANOVA
  /DEPENDENT dv
  /METHOD=ENTER iv1.

* 多元线性回归 (含诊断).
REGRESSION
  /DESCRIPTIVES MEAN STDDEV CORR SIG N
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS CI(95) R ANOVA COLLIN TOL CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT dv
  /METHOD=ENTER iv1 iv2 iv3
  /SCATTERPLOT=(*ZRESID ,*ZPRED)
  /RESIDUALS DURBIN HISTOGRAM NORMPROB.

* 逐步回归.
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF R ANOVA CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT dv
  /METHOD=STEPWISE(iv1 iv2 iv3 iv4 iv5).

* 层次回归 (控制变量后检验核心变量).
REGRESSION
  /MISSING LISTWISE
  /STATISTICS COEFF R ANOVA CHANGE
  /CRITERIA=PIN(.05) POUT(.10)
  /DEPENDENT dv
  /METHOD=ENTER control1 control2
  /METHOD=ENTER iv1 iv2 iv3.

* ========== 逻辑回归 ==========.

* 二元逻辑回归.
LOGISTIC REGRESSION VARIABLES dv
  /METHOD=ENTER iv1 iv2 iv3
  /PRINT=GOODFIT CI(95)
  /CRITERIA=PIN(0.05) POUT(0.10) ITERATE(20) CUT(0.5)
  /SAVE=PRED PGROUP.

* 有序逻辑回归.
PLUM dv_ordinal BY iv_cat WITH iv_cont
  /LINK=LOGIT
  /PRINT=FIT PARAMETER SUMMARY
  /CRITERIA=CIN(95) DELTA(0) LCONVERGE(0) MXITER(100) MXSTEP(5)
  /SAVE=ESTPROB.

* ========== 中介效应 (逐步法 + Bootstrap) ==========.

* Step 1: 总效应 (c path).
REGRESSION
  /DEPENDENT Y
  /METHOD=ENTER X.

* Step 2: X → M (a path).
REGRESSION
  /DEPENDENT M
  /METHOD=ENTER X.

* Step 3: X + M → Y (b path + c' path).
REGRESSION
  /DEPENDENT Y
  /METHOD=ENTER X M.

* 注: SPSS 原生不支持 Bootstrap 中介效应，需安装 PROCESS 宏.
* 下载地址: https://processmacro.org/download.html
* 安装后运行:
* PROCESS y=Y /x=X /m=M /model=4 /boot=5000.
```

---

## 六、因子分析与信度

```spss
* ========== 探索性因子分析 ==========.

FACTOR
  /VARIABLES item1 TO item20
  /MISSING LISTWISE
  /ANALYSIS item1 TO item20
  /PRINT INITIAL KMO AIC EXTRACTION ROTATION
  /FORMAT SORT BLANK(.40)
  /PLOT EIGEN
  /CRITERIA MINEIGEN(1) ITERATE(25)
  /EXTRACTION PC
  /CRITERIA ITERATE(25)
  /ROTATION VARIMAX
  /METHOD=CORRELATION.

* Promax 斜交旋转 (因子间有相关时用).
FACTOR
  /VARIABLES item1 TO item20
  /MISSING LISTWISE
  /PRINT INITIAL KMO AIC EXTRACTION ROTATION
  /FORMAT SORT BLANK(.40)
  /CRITERIA MINEIGEN(1) ITERATE(25)
  /EXTRACTION PC
  /CRITERIA ITERATE(25)
  /ROTATION PROMAX(4)
  /METHOD=CORRELATION.

* ========== 信度分析 ==========.

* 整体信度.
RELIABILITY
  /VARIABLES=item1 TO item10
  /SCALE('整体量表') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.

* 分维度信度.
RELIABILITY
  /VARIABLES=item1 item2 item3 item4
  /SCALE('情感维度') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.

RELIABILITY
  /VARIABLES=item5 item6 item7 item8
  /SCALE('认知维度') ALL
  /MODEL=ALPHA
  /STATISTICS=DESCRIPTIVE SCALE CORR
  /SUMMARY=TOTAL.
```

---

## 七、批处理技巧

```spss
* 批量 t 检验.
DO REPEAT dv = score1 score2 score3 score4 score5.
  T-TEST GROUPS=group(1 2)
    /VARIABLES=dv
    /ES DISPLAY(TRUE)
    /CRITERIA=CI(.95).
END REPEAT.

* 批量描述统计.
DESCRIPTIVES VARIABLES=score1 TO score20
  /STATISTICS=MEAN STDDEV MIN MAX.
```

---

## 参考资料

- 输出管理语法（导出 HTML/Word/PDF/PNG）→ 见 [references/syntax-reference.md](references/syntax-reference.md)
- 错误排查手册 → 见 [references/error-troubleshooting.md](references/error-troubleshooting.md)
- 高级分析语法（MANOVA、Bootstrap、PROCESS）→ 见 [references/advanced-analysis-guide.md](references/advanced-analysis-guide.md)
- 全部高级程序语法（聚类、判别、生存分析、ROC、GLM、决策树、神经网络、Bootstrap、OMS、Python/R）→ 见 [references/advanced-procedures.md](references/advanced-procedures.md)
- 图表制作完整指导 → 见 [references/visualization-guide.md](references/visualization-guide.md)
