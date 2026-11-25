---
name: wps-formula
description: |
  表格公式助手。描述你的计算需求，帮你写出对应的WPS表格公式，
  VLOOKUP、SUMIF、IF嵌套都支持，还说明WPS和Excel的兼容差异。
  用于帮助用户生成WPS表格公式。当用户提到公式、函数、怎么算时触发。
  WPS spreadsheet formula assistant.
license: MIT
user-invocable: true
argument-hint: '[用中文描述你想算什么]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 表格公式助手
  description_zh: 描述你的计算需求，帮你写出对应的WPS表格公式
  tags:
    - WPS
    - 公式
    - 函数
    - 表格
    - Excel
  version: 1.0.3
  license: MIT
---

# WPS 公式专家

用中文描述你想算什么 → 自动生成 WPS 表格公式。

> **核心原则：生成的公式必须在 WPS 表格中可直接使用。注意 WPS 与 Excel 的函数差异。**

## When to Use

- 用户不知道该用什么函数
- 用户需要复杂的嵌套公式
- 用户遇到公式错误（#VALUE!, #REF!, #N/A等）
- 用户需要从自然语言描述转换为公式
- 用户问"怎么用公式实现XXX"

## When NOT to Use

- 用户需要编写WPS宏脚本 → 使用 `wps-jsa-macro`
- 用户需要数据清洗（去重/去空）→ 使用 `wps-data-clean`
- 用户需要创建数据透视表 → 使用 `wps-pivot`

## 工作流程

### Step 1: 理解需求

确认：
- **数据位置**：数据在哪些单元格/列？（如"A列是姓名，B列是销售额"）
- **计算目标**：想得到什么结果？
- **特殊条件**：是否有筛选条件、多条件、跨表引用？

### Step 2: 生成公式

**输出格式必须包含：**

```text
📌 公式：
=YOUR_FORMULA_HERE

📝 说明：
- 逐段解释公式的每个部分
- 指出关键函数的作用

📋 使用方法：
- 在哪个单元格输入
- 是否需要下拉填充
- 注意事项

⚠️ 注意：
- WPS兼容性提醒（如有）
- 常见陷阱
```

### Step 3: 公式调试（如遇到错误）

用户反馈错误时，按此流程排查：

```text
#VALUE!  → 数据类型不匹配（文本vs数字），检查是否有空格或隐藏字符
#REF!    → 引用的单元格被删除或超出范围
#N/A     → 查找函数未找到匹配值，检查查找值是否完全一致
#NAME?   → 函数名拼写错误或WPS不支持该函数
#DIV/0!  → 除数为零，用IFERROR包裹
#NUM!    → 数值参数无效
循环引用  → 公式直接或间接引用了自身所在单元格
```

## WPS 函数速查（按场景分类）

### 查找匹配（最高频！）

| 场景 | 推荐公式 | 示例 |
|------|---------|------|
| 精确查找 | `VLOOKUP` | `=VLOOKUP(A2,Sheet2!A:C,3,0)` |
| 左向查找 | `INDEX+MATCH` | `=INDEX(A:A,MATCH(D2,C:C,0))` |
| 多条件查找 | `INDEX+MATCH嵌套` | `=INDEX(D:D,MATCH(1,(A:A=F2)*(B:B=G2),0))` ⚠️需Ctrl+Shift+Enter |
| 模糊匹配 | `VLOOKUP通配符` | `=VLOOKUP("*"&A2&"*",B:C,2,0)` |
| 存在性检查 | `COUNTIF` | `=IF(COUNTIF(B:B,A2)>0,"有","无")` |

### 条件统计

| 场景 | 推荐公式 | 示例 |
|------|---------|------|
| 单条件求和 | `SUMIF` | `=SUMIF(A:A,"销售部",B:B)` |
| 多条件求和 | `SUMIFS` | `=SUMIFS(C:C,A:A,"销售部",B:B,">1000")` |
| 单条件计数 | `COUNTIF` | `=COUNTIF(A:A,"合格")` |
| 多条件计数 | `COUNTIFS` | `=COUNTIFS(A:A,"男",B:B,">=90")` |
| 条件平均 | `AVERAGEIF` | `=AVERAGEIF(A:A,"A班",B:B)` |
| 条件最大 | `MAXIFS` | `=MAXIFS(B:B,A:A,"销售部")` ⚠️WPS2019+ |

### 文本处理

| 场景 | 推荐公式 | 示例 |
|------|---------|------|
| 提取前N字符 | `LEFT` | `=LEFT(A2,3)` |
| 提取后N字符 | `RIGHT` | `=RIGHT(A2,4)` |
| 提取中间 | `MID` | `=MID(A2,4,8)` 从第4位取8个字符 |
| 查找位置 | `FIND/SEARCH` | `=FIND("@",A2)` FIND区分大小写 |
| 替换 | `SUBSTITUTE` | `=SUBSTITUTE(A2," ","")` 去空格 |
| 合并文本 | `CONCATENATE/&` | `=A2&"-"&B2` |
| 文本转数字 | `VALUE` | `=VALUE(A2)` |
| 数字转文本 | `TEXT` | `=TEXT(A2,"0.00")` |
| 去首尾空格 | `TRIM` | `=TRIM(A2)` |
| 提取中文 | 正则不支持 | 用VBA/JSA替代 |

### 日期时间

| 场景 | 推荐公式 | 示例 |
|------|---------|------|
| 今天日期 | `TODAY` | `=TODAY()` |
| 两日期间隔 | 直接相减 | `=B2-A2` 结果为天数 |
| 计算年龄 | `DATEDIF` | `=DATEDIF(A2,TODAY(),"Y")` |
| 提取年/月/日 | `YEAR/MONTH/DAY` | `=YEAR(A2)` |
| 工作日计算 | `NETWORKDAYS` | `=NETWORKDAYS(A2,B2)` |
| 月末日期 | `EOMONTH` | `=EOMONTH(A2,0)` 当月末 |
| 日期格式化 | `TEXT` | `=TEXT(A2,"YYYY年M月D日")` |

### 逻辑判断

| 场景 | 推荐公式 | 示例 |
|------|---------|------|
| 单条件判断 | `IF` | `=IF(A2>=60,"及格","不及格")` |
| 多层判断 | `IFS`或嵌套IF | `=IFS(A2>=90,"优",A2>=60,"及格",TRUE,"不及格")` |
| 错误处理 | `IFERROR` | `=IFERROR(VLOOKUP(...),"未找到")` |
| 多条件与 | `AND` | `=IF(AND(A2>0,B2>0),"有效","无效")` |
| 多条件或 | `OR` | `=IF(OR(A2="经理",A2="总监"),"管理层","普通")` |

### 数组公式（Ctrl+Shift+Enter）

```text
⚠️ WPS中数组公式需要按 Ctrl+Shift+Enter 确认，公式两端会显示{}

常用数组公式：
- 多条件查找：=INDEX(D:D,MATCH(1,(A:A=F2)*(B:B=G2),0))
- 条件去重计数：=SUMPRODUCT(1/COUNTIF(A2:A100,A2:A100))
- 多列求和：=SUMPRODUCT((A2:A100="条件")*B2:B100*C2:C100)
```

## WPS 与 Excel 函数差异

| 函数 | Excel | WPS | 说明 |
|------|-------|-----|------|
| `XLOOKUP` | Excel 365+ | WPS 2021+ | 旧版WPS不支持，用INDEX+MATCH替代 |
| `MAXIFS/MINIFS` | Excel 2019+ | WPS 2019+ | 旧版用MAX(IF())数组公式替代 |
| `IFS` | Excel 2019+ | WPS 2019+ | 旧版用嵌套IF替代 |
| `CONCAT` | Excel 2019+ | WPS 2019+ | 旧版用CONCATENATE |
| `TEXTJOIN` | Excel 2019+ | WPS 2019+ | 旧版无直接替代 |
| `UNIQUE` | Excel 365 | 部分WPS支持 | 建议用高级筛选或JSA宏替代 |
| `FILTER` | Excel 365 | 部分WPS支持 | 建议用高级筛选替代 |
| `SORT` | Excel 365 | 部分WPS支持 | 建议用排序功能替代 |
| `LET` | Excel 365 | 不支持 | 无法使用 |
| `LAMBDA` | Excel 365 | 不支持 | 无法使用 |

> **安全策略：** 默认使用兼容性最好的函数（VLOOKUP而非XLOOKUP），除非用户明确使用新版WPS。

## 金额大小写转换公式

这是中国财务场景的超高频需求：

```text
=IF(A1<0,"负","")&IF(INT(A1)=0,"零",
TEXT(INT(ABS(A1)),"[DBNum2]")&"元")&
IF(INT(ABS(A1)*10)-INT(ABS(A1))*10=0,
IF(INT(ABS(A1)*100)-INT(ABS(A1)*10)*10=0,"整","零"),
MID("壹贰叁肆伍陆柒捌玖",INT(ABS(A1)*10)-INT(ABS(A1))*10,1)&"角")&
IF(INT(ABS(A1)*100)-INT(ABS(A1)*10)*10=0,"",
MID("壹贰叁肆伍陆柒捌玖",INT(ABS(A1)*100)-INT(ABS(A1)*10)*10,1)&"分")
```

## 示例

```bash
# 自然语言→公式
/wps-formula 我想统计A列中"销售部"对应的B列金额总和

# 复杂需求
/wps-formula A列是姓名B列是部门C列是销售额，帮我找出每个部门销售额最高的人

# 错误修复
/wps-formula 我的VLOOKUP返回#N/A，查找值在A列，数据在Sheet2的A到D列
```

## 参考

函数详细分类见 [reference/formula-categories.md](reference/formula-categories.md)。
中文排版通用规范见 [../shared/chinese-typesetting.md](../shared/chinese-typesetting.md)。
