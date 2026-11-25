---
name: wps-template-engine
description: |
  文档模板批量填充。在Word模板里写{{姓名}}{{金额}}这样的变量标记，
  配合Excel/CSV数据源一键批量生成。支持条件判断、循环、金额大写转换，比邮件合并更强大。
  用于帮助用户构建文档模板体系。当用户提到模板、变量、占位符、批量填充时触发。
  Document template engine with {{variable}} placeholders and batch rendering.
license: MIT
user-invocable: true
argument-hint: '[模板需求描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 模板批量填充
  description_zh: 在Word模板中设置变量，配合Excel数据批量生成文档
  tags:
    - 模板
    - 自动化
    - python-docx
    - 变量
    - WPS
  version: 1.0.1
  license: MIT
---

# 文档模板引擎

创建带 `{{变量}}` 的 Word 模板 → 从数据源自动填充 → 批量生成文档。

> 邮件合并的**升级版**：支持条件逻辑、循环、表格动态行、嵌套变量。

## When to Use

- 需要创建可复用的文档模板
- 需要从数据源批量填充文档
- 需要比邮件合并更强大的模板功能
- 用户说"帮我做一个模板""文档自动化"

## When NOT to Use

- 简单的邮件合并（无高级功能） → 使用 `wps-mail-merge`
- 一次性文档生成 → 使用 `wps-docx-writer`

## 模板语法

### 基础变量
```text
{{变量名}}           → 替换为数据值
{{公司名称}}         → "XX科技有限公司"
{{合同金额}}         → "100,000.00"
```

### 日期/格式化
```text
{{今日日期}}         → 自动填充当前日期
{{日期|YYYY年M月D日}} → 格式化日期
{{金额|大写}}        → 自动转金额大写
{{金额|千分位}}      → 添加千位分隔符
```

### 条件逻辑
```text
{{#if 性别=男}}先生{{/if}}
{{#if 性别=女}}女士{{/if}}
{{#if 金额>10000}}需要总经理审批{{/if}}
{{#if 部门=技术部}}技术考核标准如下...{{/if}}
```

### 循环（表格动态行）
```text
| 序号 | 品名 | 数量 | 单价 | 金额 |
{{#each 商品列表}}
| {{序号}} | {{品名}} | {{数量}} | {{单价}} | {{小计}} |
{{/each}}
| 合计 |  |  |  | {{总金额}} |
```

### 内置变量
```text
{{__TODAY__}}        → 当前日期 YYYY-MM-DD
{{__TODAY_CN__}}     → 当前日期 YYYY年M月D日
{{__NOW__}}          → 当前时间 HH:MM
{{__INDEX__}}        → 当前记录序号（批量生成时）
{{__TOTAL__}}        → 总记录数
```

## 工作流程

### Step 1: 决定路径

```text
用户需要什么？
│
├─ 创建新模板 → Step 2A: 设计模板
│
├─ 用已有模板填充 → Step 2B: 数据填充
│
└─ 两者都要 → 先2A再2B
```

### Step 2A: 设计模板

1. 理解用户的文档类型和变量需求
2. 设计模板结构和变量标记
3. 生成带 `{{变量}}` 的 .docx 模板文件
4. 生成配套的数据模板（.xlsx），列名对应变量名

### Step 2B: 数据填充

```python
from docx import Document
from openpyxl import load_workbook
import re
import os
import csv
from datetime import datetime

class TemplateEngine:
    """文档模板引擎"""

    BUILTIN_VARS = {
        '__TODAY__': lambda: datetime.now().strftime('%Y-%m-%d'),
        '__TODAY_CN__': lambda: datetime.now().strftime('%Y年%m月%d日'),
        '__NOW__': lambda: datetime.now().strftime('%H:%M'),
    }

    def __init__(self, template_path):
        self.template_path = template_path
        self.vars_found = set()
        self._scan_variables()

    def _scan_variables(self):
        """扫描模板中的所有变量"""
        doc = Document(self.template_path)
        for para in doc.paragraphs:
            self.vars_found.update(re.findall(r'\{\{(.+?)\}\}', para.text))
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        self.vars_found.update(
                            re.findall(r'\{\{(.+?)\}\}', para.text))

    def get_variables(self):
        """返回模板中使用的变量列表"""
        return sorted(self.vars_found)

    def render(self, data, output_path):
        """用数据渲染模板"""
        doc = Document(self.template_path)

        # 注入内置变量
        for key, func in self.BUILTIN_VARS.items():
            data.setdefault(key, func())

        # 格式化处理
        processed = {}
        for key, value in data.items():
            processed[key] = str(value) if value is not None else ''
            # 金额大写
            if key + '|大写' in str(self.vars_found):
                processed[key + '|大写'] = self._amount_to_cn(value)
            # 千分位
            if key + '|千分位' in str(self.vars_found):
                try:
                    processed[key + '|千分位'] = f'{float(value):,.2f}'
                except (ValueError, TypeError):
                    processed[key + '|千分位'] = str(value)

        # 替换段落
        for para in doc.paragraphs:
            self._replace_in_paragraph(para, processed)

        # 替换表格
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        self._replace_in_paragraph(para, processed)

        doc.save(output_path)
        return os.path.abspath(output_path)

    def _replace_in_paragraph(self, para, data):
        """替换段落中的变量（保持格式）"""
        full_text = para.text
        if '{{' not in full_text:
            return

        for var_name, value in data.items():
            placeholder = '{{' + var_name + '}}'
            if placeholder in full_text:
                for run in para.runs:
                    if placeholder in run.text:
                        run.text = run.text.replace(placeholder, value)
                full_text = para.text

    def batch_render(self, records, output_dir,
                     filename_pattern='doc_{{__INDEX__}}'):
        """批量渲染"""
        os.makedirs(output_dir, exist_ok=True)
        generated = []

        for i, record in enumerate(records):
            record['__INDEX__'] = str(i + 1)
            record['__TOTAL__'] = str(len(records))

            fname = filename_pattern
            for key, value in record.items():
                fname = fname.replace('{{' + key + '}}', str(value))
            fname = re.sub(r'[\\/:*?"<>|]', '_', fname)

            output_path = os.path.join(output_dir, f'{fname}.docx')
            self.render(record, output_path)
            generated.append(output_path)

        return generated

    @staticmethod
    def _amount_to_cn(amount):
        """金额转中文大写"""
        try:
            num = float(amount)
        except (ValueError, TypeError):
            return str(amount)
        units = ['', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿']
        digits = '零壹贰叁肆伍陆柒捌玖'
        integer = int(abs(num))
        decimal = round(abs(num) - integer, 2)

        if integer == 0:
            result = '零元'
        else:
            s = str(integer)
            result = ''
            for i, d in enumerate(reversed(s)):
                if int(d) != 0:
                    result = digits[int(d)] + units[i] + result
                else:
                    if not result.startswith('零'):
                        result = '零' + result
            result = result.rstrip('零') + '元'

        jiao = int(decimal * 10) % 10
        fen = int(decimal * 100) % 10
        if jiao == 0 and fen == 0:
            result += '整'
        else:
            if jiao > 0:
                result += digits[jiao] + '角'
            if fen > 0:
                result += digits[fen] + '分'

        return ('负' if num < 0 else '') + result
```

### Step 3: 交付

1. 生成模板文件（.docx）和数据模板（.xlsx）
2. 或直接输出填充后的文档
3. 显示变量匹配状态

## 示例

```bash
# 创建模板
/wps-template-engine 帮我做一个报价单模板，包含客户名称、产品列表、总价

# 填充模板
/wps-template-engine 用 data.xlsx 填充 quote_template.docx

# 批量生成
/wps-template-engine 用员工名单批量生成工资条，模板是salary_template.docx
```
