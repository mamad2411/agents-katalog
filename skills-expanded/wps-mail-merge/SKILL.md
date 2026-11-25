---
name: wps-mail-merge
description: |
  批量套打神器。一份Word模板+一份Excel名单=自动生成100份个性化文档。
  录取通知书、邀请函、证明信、催款函……只要有模板有数据就能批量出稿。
  用于帮助用户批量生成个性化文档。当用户提到邮件合并、批量生成、套打时触发。
  Mail merge tool - template + data source = batch personalized documents.
license: MIT
user-invocable: true
argument-hint: '[模板文件] [数据源文件]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 批量套打
  description_zh: 用一份Word模板配合Excel数据，批量生成个性化文档
  tags:
    - 邮件合并
    - 批量生成
    - python-docx
    - openpyxl
    - WPS
  version: 1.0.1
  license: MIT
---

# 智能邮件合并

Excel 数据源 + Word 模板 → 批量生成几百份个性化文档。

## When to Use

- 从名单批量生成通知/邀请函/证书
- 合同模板批量填充甲乙方信息
- 工资条/薪资通知单批量生成
- 录取通知书/入职通知批量生成
- 信封/标签批量打印
- 用户说"帮我批量生成""邮件合并"

## When NOT to Use

- 只生成单份文档 → 使用 `wps-docx-writer`
- 需要创建模板本身 → 使用 `wps-template-engine`
- 需要批量处理表格数据 → 使用 `wps-data-clean`

## 工作流程

### Step 1: 准备数据源和模板

**数据源（Excel/.xlsx/.csv）：**
```text
| 姓名   | 部门   | 职位     | 入职日期     | 薪资    |
|--------|--------|---------|-------------|---------|
| 张三   | 技术部  | 工程师   | 2026-04-01  | 15000   |
| 李四   | 市场部  | 经理    | 2026-04-01  | 20000   |
```

**模板（Word/.docx）——用 `{{变量名}}` 标记：**
```text
                    入职通知书

{{姓名}} 先生/女士：

  恭喜您通过面试！现通知您于 {{入职日期}} 到 {{部门}} 报到，
担任 {{职位}} 一职，试用期月薪为人民币 {{薪资}} 元。

  请携带以下材料：...

                                    XX公司人力资源部
                                    {{日期}}
```

### Step 2: 匹配变量

自动扫描模板中的 `{{变量名}}`，与数据源列名匹配：

```text
📋 变量匹配结果
═════════════════════════════
模板变量        数据源列      状态
──────────────────────────────
{{姓名}}    →   姓名列       ✅ 匹配
{{部门}}    →   部门列       ✅ 匹配
{{职位}}    →   职位列       ✅ 匹配
{{入职日期}} →   入职日期列    ✅ 匹配
{{薪资}}    →   薪资列       ✅ 匹配
{{日期}}    →   (无匹配)     ⚠️ 将使用当前日期
══════════════════════════════
数据行数：50 行
将生成：50 份文档
```

### Step 3: 批量生成

```bash
pip install python-docx openpyxl 2>/dev/null || pip3 install python-docx openpyxl 2>/dev/null
```

```python
from docx import Document
from openpyxl import load_workbook
from datetime import datetime
import os
import re
import csv

def mail_merge(template_path, data_path, output_dir=None,
               filename_pattern='{{姓名}}', date_str=None):
    """
    邮件合并：模板 + 数据源 → 批量文档

    参数：
        template_path: Word模板路径（含{{变量}}标记）
        data_path: 数据源路径（.xlsx 或 .csv）
        output_dir: 输出目录（默认 ./merged_output/）
        filename_pattern: 输出文件名模式（可含变量）
        date_str: 日期字符串（用于{{日期}}变量）
    """
    if not output_dir:
        output_dir = './merged_output'
    os.makedirs(output_dir, exist_ok=True)

    if not date_str:
        date_str = datetime.now().strftime('%Y年%m月%d日')

    # 读取数据源
    records = []
    if data_path.endswith('.csv'):
        with open(data_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            records = list(reader)
    else:
        wb = load_workbook(data_path)
        ws = wb.active
        headers = [cell.value for cell in ws[1]]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if any(v is not None for v in row):
                record = {}
                for h, v in zip(headers, row):
                    if h:
                        record[h] = str(v) if v is not None else ''
                records.append(record)

    # 扫描模板变量
    template_doc = Document(template_path)
    template_vars = set()
    for para in template_doc.paragraphs:
        template_vars.update(re.findall(r'\{\{(.+?)\}\}', para.text))
    for table in template_doc.tables:
        for row in table.rows:
            for cell in row.cells:
                template_vars.update(re.findall(r'\{\{(.+?)\}\}', cell.text))

    generated = []
    for i, record in enumerate(records):
        doc = Document(template_path)

        # 添加内置变量
        record.setdefault('日期', date_str)
        record.setdefault('序号', str(i + 1))

        # 替换段落中的变量
        for para in doc.paragraphs:
            for var_name in template_vars:
                placeholder = '{{' + var_name + '}}'
                if placeholder in para.text:
                    # 保持格式的替换
                    for run in para.runs:
                        if placeholder in run.text:
                            run.text = run.text.replace(
                                placeholder,
                                record.get(var_name, '')
                            )

        # 替换表格中的变量
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        for var_name in template_vars:
                            placeholder = '{{' + var_name + '}}'
                            if placeholder in para.text:
                                for run in para.runs:
                                    if placeholder in run.text:
                                        run.text = run.text.replace(
                                            placeholder,
                                            record.get(var_name, '')
                                        )

        # 生成文件名
        fname = filename_pattern
        for var_name in template_vars:
            fname = fname.replace(
                '{{' + var_name + '}}',
                record.get(var_name, '')
            )
        fname = re.sub(r'[\\/:*?"<>|]', '_', fname)
        output_path = os.path.join(output_dir, f'{fname}.docx')

        doc.save(output_path)
        generated.append(output_path)

    return generated

# 使用示例
# files = mail_merge('template.docx', 'data.xlsx',
#                    filename_pattern='入职通知_{{姓名}}')
```

### Step 4: 交付

```text
✅ 批量生成完成！
═══════════════════════════════════
模板：入职通知模板.docx
数据源：新员工名单.xlsx（50条记录）
输出目录：./merged_output/

📁 生成文件：
  1. 入职通知_张三.docx
  2. 入职通知_李四.docx
  3. 入职通知_王五.docx
  ... 共 50 份

⚠️ 请抽查几份确认内容正确
```

## 高级功能

### 条件内容
模板中支持简单条件：
```text
{{#if 性别=男}}先生{{/if}}{{#if 性别=女}}女士{{/if}}
```
（通过预处理数据实现，在数据源中增加"称呼"列）

### 金额大小写
数据源中的金额自动生成大写列：
`15000` → 增加列 `薪资大写` = `壹万伍仟元整`

### 合并输出
将所有文档合并为一个PDF（方便统一打印）

## 示例

```bash
# 基本邮件合并
/wps-mail-merge 用 template.docx 和 employees.xlsx 批量生成入职通知

# 生成证书
/wps-mail-merge 从获奖名单.xlsx批量生成荣誉证书，模板是certificate.docx

# 描述需求（无现有文件）
/wps-mail-merge 帮我做一个邮件合并，通知50个客户下周的活动安排
```
