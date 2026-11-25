---
name: wps-conditional-format
description: |
  表格自动变色。想让低于60分的自动变红？想加个进度条效果？想要红绿灯图标？
  帮你设置条件格式，数据条、色阶、图标集、重复值高亮，还提供JSA宏代码。
  用于帮助用户设置表格条件格式。当用户提到条件格式、自动变色、数据条、红绿灯时触发。
  Conditional formatting expert - data bars, color scales, icon sets, and rules.
license: MIT
user-invocable: true
argument-hint: '[格式需求描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 条件格式设置
  description_zh: 设置表格条件格式，比如不及格标红、数据条、图标集等
  tags:
    - 条件格式
    - 高亮
    - 数据条
    - Excel
    - WPS
  version: 1.0.1
  license: MIT
---

# 条件格式专家

让数据自动变色、加图标、显示数据条。一看就懂。

> "领导要的那种红绿灯效果，就是条件格式。"

## When to Use

- 数据自动变色（如负数变红）
- 进度条/数据条效果
- 红绿灯/图标集
- 重复值高亮
- 用户说"怎么让数据自动变色""加个红绿灯"

## When NOT to Use

- 图表可视化 → 使用 `wps-chart`
- 公式问题 → 使用 `wps-formula`

## 常用条件格式场景

### 场景1：数值范围变色

```text
需求：成绩≥90绿色，60-89正常，<60红色

openpyxl方式：
```

```python
from openpyxl import load_workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

wb = load_workbook('scores.xlsx')
ws = wb.active

red = PatternFill(start_color='FF6B6B', end_color='FF6B6B', fill_type='solid')
green = PatternFill(start_color='51CF66', end_color='51CF66', fill_type='solid')
yellow = PatternFill(start_color='FFD43B', end_color='FFD43B', fill_type='solid')

ws.conditional_formatting.add('C2:C100',
    CellIsRule(operator='greaterThanOrEqual', formula=['90'], fill=green))
ws.conditional_formatting.add('C2:C100',
    CellIsRule(operator='lessThan', formula=['60'], fill=red))

wb.save('scores_formatted.xlsx')
```

```text
JSA宏方式：
```

```javascript
function HighlightScores() {
    var ws = Application.ActiveSheet;
    var range = ws.Range("C2:C100");
    range.FormatConditions.Delete(); // 清除旧规则

    // >=90 绿色
    var fc1 = range.FormatConditions.Add(1, 5, "90"); // xlCellValue, xlGreaterEqual
    fc1.Interior.Color = 0x66CF51; // BGR绿色

    // <60 红色
    var fc2 = range.FormatConditions.Add(1, 6, "60"); // xlCellValue, xlLess
    fc2.Interior.Color = 0x6B6BFF; // BGR红色

    Application.alert("条件格式已设置！");
}
```

### 场景2：数据条（进度条效果）

```python
from openpyxl.formatting.rule import DataBarRule

ws.conditional_formatting.add('D2:D50',
    DataBarRule(start_type='min', end_type='max',
               color='3498DB', showValue=True))
```

```javascript
// JSA: 添加数据条
function AddDataBar() {
    var range = Application.ActiveSheet.Range("D2:D50");
    range.FormatConditions.Delete();
    range.FormatConditions.AddDatabar();
    var db = range.FormatConditions.Item(1);
    db.BarColor.Color = 0xDB9834; // BGR蓝色
}
```

### 场景3：重复值高亮

```python
from openpyxl.formatting.rule import FormulaRule

ws.conditional_formatting.add('A2:A100',
    FormulaRule(formula=['COUNTIF($A$2:$A$100,A2)>1'],
               fill=PatternFill('solid', fgColor='FFD43B')))
```

```javascript
// JSA: 高亮重复值
function HighlightDuplicates() {
    var range = Application.ActiveSheet.Range("A2:A100");
    range.FormatConditions.Delete();
    var fc = range.FormatConditions.AddUniqueValues();
    fc.DupeUnique = 1; // xlDuplicate
    fc.Interior.Color = 0x3BD4FF; // BGR黄色
}
```

### 场景4：图标集（红绿灯）

```javascript
// JSA: 红绿灯图标集
function AddTrafficLights() {
    var range = Application.ActiveSheet.Range("E2:E50");
    range.FormatConditions.Delete();
    var fc = range.FormatConditions.AddIconSetCondition();
    fc.IconSet = Application.ActiveWorkbook.IconSets(1); // 红绿灯
    // 自定义阈值
    fc.IconCriteria(2).Value = 60;
    fc.IconCriteria(3).Value = 90;
}
```

### 场景5：隔行变色（斑马纹）

```python
from openpyxl.formatting.rule import FormulaRule

stripe = PatternFill('solid', fgColor='F0F4F8')
ws.conditional_formatting.add('A2:G100',
    FormulaRule(formula=['MOD(ROW(),2)=0'], fill=stripe))
```

## 条件格式速查表

| 需求 | 类型 | 关键参数 |
|------|------|----------|
| 大于/小于变色 | CellIsRule | operator + formula |
| 包含特定文字 | FormulaRule | SEARCH函数 |
| 重复值高亮 | UniqueValues | DupeUnique=1 |
| 前N名/后N名 | Top10Rule | rank + percent |
| 数据条 | DataBarRule | color |
| 色阶(渐变色) | ColorScaleRule | start/mid/end_color |
| 图标集 | IconSetCondition | IconSet类型 |
| 日期到期提醒 | FormulaRule | TODAY()比较 |
| 隔行变色 | FormulaRule | MOD(ROW(),2) |

## 工作流程

### Step 1: 理解需求
确认要格式化的范围和条件

### Step 2: 选择方案
- openpyxl → 生成新文件
- JSA宏 → 在WPS中直接运行

### Step 3: 生成代码并说明

### Step 4: 交付
1. 提供代码（二选一或两种都给）
2. 说明如何修改阈值和颜色
3. 注意事项（规则优先级、性能影响）

## 示例

```bash
# 数值变色
/wps-conditional-format 让销售额低于目标的变红色，超过的变绿色

# 数据条
/wps-conditional-format 给完成率列加个进度条效果

# 重复值
/wps-conditional-format 帮我找出A列有哪些重复的数据
```
