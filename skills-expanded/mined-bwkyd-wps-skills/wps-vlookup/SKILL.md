---
name: wps-vlookup
description: |
  VLOOKUP助手。帮你写VLOOKUP/INDEX-MATCH/XLOOKUP公式，
  排查#N/A等常见错误，选择最合适的查找方案。
  用于帮助用户解决表格查找匹配问题。当用户提到VLOOKUP、查找、匹配、#N/A时触发。
  VLOOKUP formula assistant.
license: MIT
user-invocable: true
argument-hint: '[查找需求描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: VLOOKUP助手
  description_zh: 帮你写VLOOKUP公式，排查#N/A等常见错误
  tags:
    - VLOOKUP
    - 查找
    - 匹配
    - 公式
    - WPS
  version: 1.0.2
  license: MIT
---

# VLOOKUP/查找匹配专家

解决WPS表格中**最高频的痛点** — 数据查找与匹配。

> 据统计，VLOOKUP相关问题占WPS求助帖的35%以上。

## When to Use

- 需要从一张表查找另一张表的数据
- VLOOKUP返回#N/A、#REF!等错误
- 需要多条件查找/反向查找/多列返回
- 用户说"帮我写个VLOOKUP""两张表怎么关联"

## When NOT to Use

- 通用公式问题 → 使用 `wps-formula`
- 数据透视分析 → 使用 `wps-pivot`

## 查找场景速查

### 场景1：基础正向查找（最常见）

```text
需求：根据工号查姓名
公式：=VLOOKUP(A2, 员工表!A:C, 3, FALSE)

参数解释：
  A2        → 要查找的值（工号）
  员工表!A:C → 查找范围（工号在第1列）
  3         → 返回第3列（姓名）
  FALSE     → 精确匹配（99%的情况用FALSE）
```

### 场景2：反向查找（VLOOKUP做不到）

```text
需求：根据姓名查工号（姓名在右边，工号在左边）
方案A - INDEX+MATCH（推荐）：
=INDEX(A:A, MATCH(D2, C:C, 0))

方案B - XLOOKUP（WPS 2021+）：
=XLOOKUP(D2, C:C, A:A)
```

### 场景3：多条件查找

```text
需求：根据"部门+姓名"查找工资
方案 - INDEX+MATCH+数组：
=INDEX(C:C, MATCH(1, (A:A=E2)*(B:B=F2), 0))
（Ctrl+Shift+Enter 数组公式）

方案 - 辅助列：
辅助列公式：=A2&"|"&B2
然后VLOOKUP查找 E2&"|"&F2
```

### 场景4：模糊匹配/近似查找

```text
需求：根据成绩查等级（60→及格，80→良好，90→优秀）
公式：=VLOOKUP(A2, 等级表, 2, TRUE)
注意：等级表第一列必须升序排列！

等级表：
  0   不及格
  60  及格
  80  良好
  90  优秀
```

### 场景5：跨工作簿查找

```text
=VLOOKUP(A2, '[数据源.xlsx]Sheet1'!A:D, 3, FALSE)
注意：源文件必须打开，否则需要写完整路径
```

### 场景6：一次返回多列

```text
需求：查找后返回多个字段
方案 - VLOOKUP+COLUMN：
=VLOOKUP($A2, 数据!$A:$F, COLUMN(B1), FALSE)
向右拖动自动递增列号

方案 - XLOOKUP返回数组（WPS 2021+）：
=XLOOKUP(A2, 数据!A:A, 数据!B:F)
一次返回B到F所有列
```

## #N/A 错误诊断

```text
VLOOKUP返回#N/A？按这个顺序排查：

1️⃣ 数据类型不一致（最常见！）
   症状：明明有这个值但就是找不到
   原因：查找值是文本"001"，表里是数字1
   修复：=VLOOKUP(VALUE(A2), ...) 或 =VLOOKUP(TEXT(A2,"000"), ...)

2️⃣ 有隐藏空格
   症状：肉眼看一样但匹配不上
   检测：=LEN(A2) 看长度是否异常
   修复：=VLOOKUP(TRIM(CLEAN(A2)), ...)

3️⃣ 查找列不在第一列
   症状：范围选错了
   修复：调整范围让查找值在第一列，或改用INDEX+MATCH

4️⃣ 第4参数写了TRUE或省略
   症状：返回错误的值
   修复：改为FALSE（精确匹配）

5️⃣ 查找范围有合并单元格
   症状：只有合并区域第一行能匹配
   修复：先取消合并 → 填充空值 → 再查找
```

## 工作流程

### Step 1: 理解查找需求

确认以下信息：
- **查找什么**：用什么值去查（如工号、姓名）
- **从哪里查**：数据源在哪个表/文件
- **返回什么**：需要取回哪些字段
- **特殊要求**：多条件？模糊匹配？反向？

### Step 2: 选择最佳方案

```text
┌─ 正向查找（查找列在最左）
│  └─ 单条件 → VLOOKUP
│  └─ 多条件 → 辅助列+VLOOKUP 或 INDEX+MATCH
│
├─ 反向查找（查找列在右侧）
│  └─ INDEX+MATCH 或 XLOOKUP
│
├─ 多列返回
│  └─ VLOOKUP+COLUMN 或 XLOOKUP
│
└─ 近似/区间匹配
   └─ VLOOKUP(TRUE) 或 IFS
```

### Step 3: 生成公式并说明

提供：
1. 完整公式（可直接粘贴使用）
2. 参数逐项说明
3. 注意事项（数据类型、排序要求等）
4. 如遇错误的排查步骤

### Step 4: 提供JSA批量方案（可选）

如果查找量大或需要自动化：

```javascript
// JSA: 批量VLOOKUP填充
function BatchLookup() {
    var ws = Application.ActiveSheet;
    var lookupSheet = Application.Sheets("数据源");
    var lastRow = ws.Cells(ws.Rows.Count, 1).End(-4162).Row; // xlUp

    for (var i = 2; i <= lastRow; i++) {
        var key = ws.Cells(i, 1).Value2; // A列查找值
        // 在数据源A列查找，返回C列
        var found = lookupSheet.Range("A:A").Find(key, undefined,
            -4163, 1); // xlValues, xlWhole
        if (found) {
            ws.Cells(i, 5).Value2 = lookupSheet.Cells(found.Row, 3).Value2;
        } else {
            ws.Cells(i, 5).Value2 = "未找到";
        }
    }
    Application.alert("批量查找完成！共处理 " + (lastRow - 1) + " 行");
}
```

## VLOOKUP vs INDEX-MATCH vs XLOOKUP

| 特性 | VLOOKUP | INDEX+MATCH | XLOOKUP |
|------|---------|-------------|---------|
| 反向查找 | 不支持 | 支持 | 支持 |
| 插入列不影响 | 会错位 | 不受影响 | 不受影响 |
| 多条件 | 需辅助列 | 原生支持 | 原生支持 |
| 默认匹配 | 近似(TRUE) | 精确(0) | 精确 |
| WPS兼容 | 所有版本 | 所有版本 | 2021+ |
| 性能 | 一般 | 较好 | 最好 |
| 学习难度 | 简单 | 中等 | 简单 |

## 示例

```bash
# 基础查找
/wps-vlookup 我有两张表，A表有工号和姓名，B表有工号和工资，怎么把工资匹配到A表

# 错误修复
/wps-vlookup VLOOKUP老是返回#N/A，明明数据都有

# 多条件
/wps-vlookup 根据部门和月份两个条件查找销售额
```
