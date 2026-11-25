---
name: invoice-organizer
description: 通过读取杂乱的文件、提取关键信息、一致地重命名并将它们分类到逻辑文件夹中，自动组织税务准备的发票和收据。将数小时的手动记账转变为数分钟的自动组织。
---

# 发票组织器

此技能将混乱的发票、收据和财务文档文件夹转变为干净、税务就绪的归档系统，无需手动操作。

## 何时使用此技能

- 准备报税季并需要有组织的记录
- 管理多个供应商的业务支出
- 整理杂乱文件夹或电子邮件下载中的收据
- 为持续记账设置自动发票归档
- 按年份或类别归档财务记录
- 核对费用以进行报销
- 为会计师准备文档

## 此技能做什么

1. **读取发票内容**: 从 PDF、图像和文档中提取信息：
   - 供应商/公司名称
   - 发票号码
   - 日期
   - 金额
   - 产品或服务描述
   - 付款方式

2. **一致地重命名文件**: 创建标准化文件名：
   - 格式: `YYYY-MM-DD Vendor - Invoice - ProductOrService.pdf`
   - 示例: `2024-03-15 Adobe - Invoice - Creative Cloud.pdf`

3. **按类别组织**: 分类到逻辑文件夹中：
   - 按供应商
   - 按费用类别 (软件、办公、差旅等)
   - 按时间段 (年、季度、月)
   - 按税务类别 (可抵扣、个人等)

4. **处理多种格式**: 适用于：
   - PDF 发票
   - 扫描的收据 (JPG, PNG)
   - 电子邮件附件
   - 截图
   - 银行对账单

5. **保留原件**: 在整理副本的同时保留原始文件

## 如何使用

### 基本用法

导航到您杂乱的发票文件夹：
```
cd ~/Desktop/receipts-to-sort
```

然后询问 Claude Code：
```
Organize these invoices for taxes
```

或者更具体地：
```
Read all invoices in this folder, rename them to 
"YYYY-MM-DD Vendor - Invoice - Product.pdf" format, 
and organize them by vendor
```

### 高级组织

```
Organize these invoices:
1. Extract date, vendor, and description from each file
2. Rename to standard format
3. Sort into folders by expense category (Software, Office, Travel, etc.)
4. Create a CSV spreadsheet with all invoice details for my accountant
```

## 说明

当用户请求发票组织时：

1. **扫描文件夹**
   
   识别所有发票文件：
   ```bash
   # 查找所有发票相关文件
   find . -type f \( -name "*.pdf" -o -name "*.jpg" -o -name "*.png" \) -print
   ```
   
   报告发现：
   - 文件总数
   - 文件类型
   - 日期范围 (如果可以从名称中辨别)
   - 当前组织 (或缺乏组织)

2. **从每个文件中提取信息**
   
   对于每张发票，提取：
   
   **从 PDF 发票**:
   - 使用文本提取读取发票内容
   - 寻找常见模式:
     - "Invoice Date:", "Date:", "Issued:"
     - "Invoice #:", "Invoice Number:"
     - 公司名称 (通常在顶部)
     - "Amount Due:", "Total:", "Amount:"
     - "Description:", "Service:", "Product:"
   
   **从图像收据**:
   - 从图像中读取可见文本
   - 识别供应商名称 (通常在顶部)
   - 寻找日期 (常见格式)
   - 找到总金额
   
   **不清晰文件的回退**:
   - 使用文件名线索
   - 检查文件创建/修改日期
   - 如果关键信息缺失，标记为手动审查

3. **确定组织策略**
   
   如果未指定，询问用户偏好：
   
   ```markdown
   I found [X] invoices from [date range].
   
   How would you like them organized?
   
   1. **By Vendor** (Adobe/, Amazon/, Stripe/, etc.)
   2. **By Category** (Software/, Office Supplies/, Travel/, etc.)
   3. **By Date** (2024/Q1/, 2024/Q2/, etc.)
   4. **By Tax Category** (Deductible/, Personal/, etc.)
   5. **Custom** (describe your structure)
   
   Or I can use a default structure: Year/Category/Vendor
   ```

4. **创建标准化文件名**
   
   对于每张发票，创建遵循此模式的文件名：
   
   ```
   YYYY-MM-DD Vendor - Invoice - Description.ext
   ```
   
   示例：
   - `2024-03-15 Adobe - Invoice - Creative Cloud.pdf`
   - `2024-01-10 Amazon - Receipt - Office Supplies.pdf`
   - `2023-12-01 Stripe - Invoice - Monthly Payment Processing.pdf`
   
   **文件名最佳实践**:
   - 移除除连字符外的特殊字符
   - 正确大写供应商名称
   - 保持描述简洁但有意义
   - 使用一致的日期格式 (YYYY-MM-DD) 进行排序
   - 保留原始文件扩展名

5. **执行组织**
   
   在移动文件之前，显示计划：
   
   ```markdown
   # 组织计划
   
   ## 提议结构
   ```
   Invoices/
   ├── 2023/
   │   ├── Software/
   │   │   ├── Adobe/
   │   │   └── Microsoft/
   │   ├── Services/
   │   └── Office/
   └── 2024/
       ├── Software/
       ├── Services/
       └── Office/
   ```
   
   ## 示例更改
   
   Before: `invoice_adobe_march.pdf`
   After: `2024-03-15 Adobe - Invoice - Creative Cloud.pdf`
   Location: `Invoices/2024/Software/Adobe/`
   
   Before: `IMG_2847.jpg`
   After: `2024-02-10 Staples - Receipt - Office Supplies.jpg`
   Location: `Invoices/2024/Office/Staples/`
   
   Process [X] files? (yes/no)
   ```
   
   批准后：
   ```bash
   # 创建文件夹结构
   mkdir -p "Invoices/2024/Software/Adobe"
   
   # 复制 (不移动) 以保留原件
   cp "original.pdf" "Invoices/2024/Software/Adobe/2024-03-15 Adobe - Invoice - Creative Cloud.pdf"
   
   # 或者如果用户更喜欢移动
   mv "original.pdf" "new/path/standardized-name.pdf"
   ```

6. **生成摘要报告**
   
   创建一个包含所有发票详情的 CSV 文件：
   
   ```csv
   Date,Vendor,Invoice Number,Description,Amount,Category,File Path
   2024-03-15,Adobe,INV-12345,Creative Cloud,52.99,Software,Invoices/2024/Software/Adobe/2024-03-15 Adobe - Invoice - Creative Cloud.pdf
   2024-03-10,Amazon,123-4567890-1234567,Office Supplies,127.45,Office,Invoices/2024/Office/Amazon/2024-03-10 Amazon - Receipt - Office Supplies.pdf
   ...
   ```
   
   此 CSV 用于：
   - 导入会计软件
   - 与会计师共享
   - 费用跟踪和报告
   - 税务准备

7. **提供完成摘要**
   
   ```markdown
   # 组织完成! 📊
   
   ## 摘要
   - **已处理**: [X] invoices
   - **日期范围**: [earliest] to [latest]
   - **总金额**: $[sum] (if amounts extracted)
   - **供应商**: [Y] unique vendors
   
   ## 新结构
   ```
   Invoices/
   ├── 2024/ (45 files)
   │   ├── Software/ (23 files)
   │   ├── Services/ (12 files)
   │   └── Office/ (10 files)
   └── 2023/ (12 files)
   ```
   
   ## 创建的文件
   - `/Invoices/` - Organized invoices
   - `/Invoices/invoice-summary.csv` - Spreadsheet for accounting
   - `/Invoices/originals/` - Original files (if copied)
   
   ## 需要审查的文件
   [List any files where information couldn't be extracted completely]
   
   ## 下一步
   1. 审查 `invoice-summary.csv` 文件
   2. 检查 "Needs Review" 文件夹中的文件
   3. 将 CSV 导入您的会计软件
   4. 为未来发票设置自动组织
   
   税务季准备就绪！ 🎉
   ```

## 示例

### 示例 1: 税务准备 (来自 Martin Merschroth)

**用户**: "I have a messy folder of invoices for taxes. Sort them and rename properly."

**过程**:
1. 扫描文件夹：发现 147 个 PDF 和图像
2. 读取每张发票以提取：
   - 日期
   - 供应商名称
   - 发票号码
   - 产品/服务描述
3. 重命名所有文件： `YYYY-MM-DD Vendor - Invoice - Product.pdf`
4. 组织到： `2024/Software/`, `2024/Travel/`, 等
5. 为会计师创建 `invoice-summary.csv`
6. 结果：数分钟内完成税务就绪的有组织发票

### 示例 2: 每月费用核对

**用户**: "Organize my business receipts from last month by category."

**输出**:
```markdown
# 2024 年 3 月收据已组织

## 按类别
- Software & Tools: $847.32 (12 invoices)
- Office Supplies: $234.18 (8 receipts)
- Travel & Meals: $1,456.90 (15 receipts)
- Professional Services: $2,500.00 (3 invoices)

Total: $5,038.40

所有收据已重命名并归档在：
`Business-Receipts/2024/03-March/[Category]/`

CSV 导出: `march-2024-expenses.csv`
```

### 示例 3: 多年归档

**用户**: "I have 3 years of random invoices. Organize them by year, then by vendor."

**输出**: 创建结构：
```
Invoices/
├── 2022/
│   ├── Adobe/
│   ├── Amazon/
│   └── ...
├── 2023/
│   ├── Adobe/
│   ├── Amazon/
│   └── ...
└── 2024/
│   ├── Adobe/
│   ├── Amazon/
│   └── ...
```

每个文件都正确重命名，带有日期和描述。

### 示例 4: 电子邮件下载清理

**用户**: "I download invoices from Gmail. They're all named 'invoice.pdf', 'invoice(1).pdf', etc. Fix this mess."

**输出**:
```markdown
发现 89 个文件都名为 "invoice*.pdf"

正在读取每个文件以提取真实信息...

重命名示例:
- invoice.pdf → 2024-03-15 Shopify - Invoice - Monthly Subscription.pdf
- invoice(1).pdf → 2024-03-14 Google - Invoice - Workspace.pdf
- invoice(2).pdf → 2024-03-10 Netlify - Invoice - Pro Plan.pdf

所有文件已重命名并按供应商组织。
```

## 常见组织模式

### 按供应商 (简单)
```
Invoices/
├── Adobe/
├── Amazon/
├── Google/
└── Microsoft/
```

### 按年份和类别 (税务友好)
```
Invoices/
├── 2023/
│   ├── Software/
│   ├── Hardware/
│   ├── Services/
│   └── Travel/
└── 2024/
    └── ...
```

### 按季度 (详细跟踪)
```
Invoices/
├── 2024/
│   ├── Q1/
│   │   ├── Software/
│   │   ├── Office/
│   │   └── Travel/
│   └── Q2/
│       └── ...
```

### 按税务类别 (会计师就绪)
```
Invoices/
├── Deductible/
│   ├── Software/
│   ├── Office/
│   └── Professional-Services/
├── Partially-Deductible/
│   └── Meals-Travel/
└── Personal/
```

## 自动化设置

对于持续组织：

```
Create a script that watches my ~/Downloads/invoices folder 
and auto-organizes any new invoice files using our standard 
naming and folder structure.
```

这将创建一个持久解决方案，在发票到达时对其进行组织。

## 专业提示

1. **扫描电子邮件为 PDF**: 先使用预览或类似工具将电子邮件发票保存为 PDF
2. **一致下载**: 将所有发票保存到一个文件夹以进行批量处理
3. **每月例程**: 每月组织发票，而不是每年
4. **备份原件**: 在重新组织之前保留原始文件
5. **在 CSV 中包含金额**: 用于预算跟踪
6. **按可抵扣性标记**: 注明哪些费用是可免税的
7. **保留收据 7 年**: 标准审计期

## 处理特殊情况

### 缺失信息
如果无法提取日期/供应商：
- 标记文件以供手动审查
- 使用文件修改日期作为回退
- 创建 "Needs-Review/" 文件夹

### 重复发票
如果同一发票出现多次：
- 比较文件哈希
- 保留最高质量版本
- 在摘要中注明重复项

### 多页发票
对于拆分在多个文件中的发票：
- 如果需要合并 PDF
- 对部分使用一致命名
- 在 CSV 中注明发票是否拆分

### 非标准格式
对于不寻常的收据格式：
- 提取可能的内容
- 标准化您可以的内容
- 如果关键信息缺失，标记为审查

## 相关用例

- 创建费用报表以进行报销
- 组织银行对账单
- 管理供应商合同
- 归档旧财务记录
- 为审计做准备
- 跟踪订阅成本随时间的变化
