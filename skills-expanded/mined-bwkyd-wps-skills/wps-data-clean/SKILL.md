---
name: wps-data-clean
description: >
  表格数据清洗。清理表格中的格式问题，如手机号、身份证、日期格式不统一，
  去除多余空格和重复行，支持中国特色数据格式。
  用于帮助用户清洗修复表格数据。当用户提到数据清洗、去重、格式统一时触发。
  Spreadsheet data cleaning tool.
license: MIT
user-invocable: true
argument-hint: '[清洗需求描述] [文件路径(可选)]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 表格数据清洗
  description_zh: 清理表格中的格式问题，如手机号、身份证、日期格式不统一等
  tags:
    - 数据清洗
    - WPS
    - 表格
    - openpyxl
    - 去重
  version: 1.0.2
  license: MIT
---

# WPS 数据清洗工具

一键清洗杂乱的表格数据，让脏数据变成可用数据。

## When to Use

- 表格数据有大量重复、空行、格式不统一
- 手机号、身份证号、日期格式混乱
- 需要合并/拆分单元格内容
- 从外部系统导出的数据需要整理
- 用户说"帮我清洗/整理这个表格"

## When NOT to Use

- 需要写公式 → 使用 `wps-formula`
- 需要数据分析/透视 → 使用 `wps-pivot`
- 需要图表可视化 → 使用 `wps-chart`

## 清洗能力清单

### ✅ 基础清洗

| 操作 | 说明 | 适用场景 |
|------|------|---------|
| **去重** | 按指定列删除重复行 | 导入数据有重复记录 |
| **去空行** | 删除全空行或指定列为空的行 | 数据中间有空行 |
| **去空格** | 去除首尾空格、多余空格 | 文本前后有隐藏空格 |
| **去特殊字符** | 清除不可见字符、换行符 | 从网页/PDF复制的数据 |
| **统一大小写** | 全大写/全小写/首字母大写 | 英文数据不统一 |
| **繁简转换** | 繁体中文→简体中文 | 港台数据导入 |

### ✅ 中国特色数据标准化

| 数据类型 | 清洗规则 | 示例 |
|---------|---------|------|
| **手机号** | 去空格/横杠，补+86，验证11位 | `138-1234-5678` → `13812345678` |
| **身份证号** | 去空格，验证18/15位，校验末位 | `110101 1990 0101 001X` → `11010119900101001X` |
| **日期** | 统一为 `YYYY-MM-DD` 或 `YYYY年M月D日` | `2024/3/5` `2024.03.05` → `2024-03-05` |
| **金额** | 去逗号/¥/元，统一为数值 | `¥1,234.56元` → `1234.56` |
| **性别** | 统一为 `男/女` | `M/F` `male/female` `1/0` → `男/女` |
| **省市区** | 补全省市区层级 | `朝阳区` → `北京市朝阳区` |
| **姓名** | 去空格，去称呼后缀 | `张 三先生` → `张三` |
| **邮箱** | 去空格，转小写，验证格式 | ` ABC@Gmail.COM ` → `abc@gmail.com` |

### ✅ 结构性清洗

| 操作 | 说明 |
|------|------|
| **拆分列** | 一列拆多列（如姓名→姓+名，地址→省+市+区） |
| **合并列** | 多列合一列（如姓+名→姓名） |
| **取消合并单元格** | 合并单元格→填充每个子单元格 |
| **转置** | 行列互换 |
| **宽表转长表** | 多列月份→日期+值的两列 |
| **长表转宽表** | 日期+值→多列月份 |

## 工作流程

### Step 1: 诊断数据问题

**如果用户提供了文件：**
```bash
pip install openpyxl 2>/dev/null || pip3 install openpyxl 2>/dev/null
```

读取文件并输出数据诊断报告：

```text
📊 数据诊断报告
═══════════════════════════════════
文件：[文件名]
工作表：[Sheet名]
行数：[X] 行（含表头）
列数：[X] 列

🔍 发现的问题：
┌─────────────────────────────────┐
│ ⚠️  重复行：XX 行（占比 XX%）     │
│ ⚠️  空行：XX 行                  │
│ ⚠️  A列有 XX 个空值              │
│ ⚠️  B列(手机号)格式不统一：XX 个   │
│ ⚠️  C列(日期)格式混乱：XX 个      │
│ ✅  D列(金额)格式正常             │
└─────────────────────────────────┘

📋 建议清洗操作：
1. 删除 XX 行完全重复数据
2. 删除 XX 行空行
3. 标准化手机号为11位数字
4. 统一日期格式为 YYYY-MM-DD
```

### Step 2: 确认清洗方案

向用户展示诊断报告，确认要执行的清洗操作。

### Step 3: 执行清洗

**根据场景选择技术路线：**

| 场景 | 技术路线 | 输出 |
|------|---------|------|
| 有 .xlsx 文件在磁盘上 | **openpyxl脚本** | 清洗后的新 .xlsx 文件 |
| 用户在WPS中打开了表格 | **JSA宏** | 粘贴到WPS宏编辑器运行 |
| 仅描述需求，无文件 | **JSA宏模板** | .js文件供用户使用 |

**openpyxl 清洗脚本模式：**

```python
import openpyxl
import re
from copy import copy

def clean_spreadsheet(input_path, output_path=None):
    wb = openpyxl.load_workbook(input_path)
    ws = wb.active

    if not output_path:
        output_path = input_path.replace('.xlsx', '_cleaned.xlsx')

    stats = {'removed_duplicates': 0, 'removed_blanks': 0,
             'fixed_phones': 0, 'fixed_dates': 0}

    # === 去重 ===
    seen = set()
    rows_to_delete = []
    for row_idx in range(2, ws.max_row + 1):  # 跳过表头
        row_data = tuple(ws.cell(row=row_idx, column=c).value
                        for c in range(1, ws.max_column + 1))
        if row_data in seen:
            rows_to_delete.append(row_idx)
            stats['removed_duplicates'] += 1
        else:
            seen.add(row_data)

    # 从后往前删除（避免索引偏移）
    for row_idx in reversed(rows_to_delete):
        ws.delete_rows(row_idx)

    # === 去空行 ===
    rows_to_delete = []
    for row_idx in range(2, ws.max_row + 1):
        if all(ws.cell(row=row_idx, column=c).value is None
               for c in range(1, ws.max_column + 1)):
            rows_to_delete.append(row_idx)
            stats['removed_blanks'] += 1
    for row_idx in reversed(rows_to_delete):
        ws.delete_rows(row_idx)

    # === 清洗各列 ===
    # 根据实际列内容动态清洗

    wb.save(output_path)
    return output_path, stats
```

**手机号标准化函数：**
```python
def clean_phone(value):
    """标准化中国大陆手机号"""
    if value is None:
        return value
    s = re.sub(r'[\s\-\+\(\)（）]', '', str(value))
    s = re.sub(r'^86', '', s)
    s = re.sub(r'^\+86', '', s)
    if re.match(r'^1[3-9]\d{9}$', s):
        return s
    return str(value)  # 无法识别的保留原值
```

**身份证号标准化函数：**
```python
def clean_id_card(value):
    """标准化身份证号"""
    if value is None:
        return value
    s = re.sub(r'\s', '', str(value)).upper()
    if re.match(r'^\d{17}[\dX]$', s):
        return s
    if re.match(r'^\d{15}$', s):
        return s  # 一代身份证
    return str(value)
```

**日期标准化函数：**
```python
def clean_date(value, output_format='%Y-%m-%d'):
    """统一日期格式"""
    if value is None:
        return value
    if isinstance(value, datetime):
        return value.strftime(output_format)
    s = str(value).strip()
    formats = [
        '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d',
        '%Y年%m月%d日', '%d/%m/%Y', '%m/%d/%Y',
        '%Y%m%d', '%d-%m-%Y',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt).strftime(output_format)
        except ValueError:
            continue
    return s  # 无法解析的保留原值
```

### Step 4: 输出结果

```text
✅ 清洗完成！
═══════════════════════════════════
输入文件：data.xlsx（1000行）
输出文件：data_cleaned.xlsx（856行）

📊 清洗统计：
  🗑️ 删除重复行：89 行
  🗑️ 删除空行：55 行
  📱 修复手机号：123 个
  📅 修复日期格式：67 个
  ✂️ 去除首尾空格：234 个

⚠️ 请用WPS打开 data_cleaned.xlsx 确认结果
```

## 示例

```bash
# 清洗指定文件
/wps-data-clean 清洗 sales_data.xlsx，去重并标准化手机号

# 生成清洗宏（在WPS中运行）
/wps-data-clean 写一个JSA宏，去除当前表格中的所有空行和重复行

# 描述需求
/wps-data-clean 我有一个客户表，手机号格式混乱（有的带横杠有的带+86），帮我统一
```

## 参考

中国数据格式标准见 [reference/cn-data-formats.md](reference/cn-data-formats.md)。
