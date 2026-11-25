---
name: dummy-dataset
description: "生成用于测试的逼真模拟数据集,支持自定义列、约束条件和输出格式(CSV、JSON、SQL、Python 脚本)。适用于创建测试数据、构建模拟数据集,或为开发和演示生成示例数据。"
---
# 模拟数据集生成

生成用于测试的逼真模拟数据集,支持自定义列、约束条件和输出格式(CSV、JSON、SQL、Python 脚本)。可直接产出可执行脚本或数据文件,开箱即用。

**适用场景:** 创建测试数据、生成示例数据集、为开发构建逼真的模拟数据,或填充测试环境。

**参数:**
- `$PRODUCT`:产品或系统名称
- `$DATASET_TYPE`:数据类型(如客户反馈、交易记录、用户档案)
- `$ROWS`:要生成的行数(默认:100)
- `$COLUMNS`:需要包含的具体列或字段
- `$FORMAT`:输出格式(CSV、JSON、SQL、Python 脚本)
- `$CONSTRAINTS`:额外的约束条件或业务规则

## 分步流程

1. **确定数据集类型** - 理解数据所属的业务领域
2. **定义列规格** - 列名、数据类型和取值范围
3. **确定行数** - 需要多少条样本记录
4. **选择输出格式** - CSV、JSON、SQL INSERT 或 Python 脚本
5. **应用真实模式** - 确保数据看起来真实且有效
6. **加入业务约束** - 遵守业务逻辑和数据关系
7. **生成或编写数据脚本** - 产出可执行的输出
8. **校验输出** - 确保数据质量和完整性

## 模板:Python 脚本输出

```python
import csv
import json
from datetime import datetime, timedelta
import random

# Configuration
ROWS = $ROWS
FILENAME = "$DATASET_TYPE.csv"

# Column definitions with realistic value generators
columns = {
    "id": "auto-increment",
    "name": "first_last_name",
    "email": "email",
    "created_at": "timestamp",
    # Add more columns...
}

def generate_dataset():
    """Generate realistic dummy dataset"""
    data = []
    for i in range(1, ROWS + 1):
        record = {
            "id": f"U{i:06d}",
            # Generate values based on column definitions
        }
        data.append(record)
    return data

def save_as_csv(data, filename):
    """Save dataset as CSV"""
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    dataset = generate_dataset()
    save_as_csv(dataset, FILENAME)
    print(f"Generated {len(dataset)} records in {FILENAME}")
```

## 数据集规格示例

**数据集类型:** 客户反馈

**列:**
- feedback_id(自增,U001、U002...)
- customer_name(逼真的姓名)
- email(合法的邮箱格式)
- feedback_date(最近 90 天内的日期)
- rating(1-5 星)
- category(Bug、Feature Request、Complaint、Praise)
- text(逼真的反馈内容)
- product(electronics、clothing、home)

**约束条件:**
- 评分倾斜分布:40% 5 星、30% 4 星、20% 3 星、10% 1-2 星
- Bug 类仅出现在 1-3 星评分中
- Feature Request 类仅出现在 3-5 星评分中
- 邮箱域名要真实(gmail、yahoo、company.com)

## 交付物

- 可直接执行的 Python 脚本或直接可用的数据文件
- 带有正确表头和格式的 CSV 文件
- 结构与类型合法的 JSON 文件
- 用于填充数据库的 SQL INSERT 语句
- 数据校验与约束合规
- 逼真且符合业务场景的取值
- 数据生成逻辑的说明文档
- 数据集使用的快速上手指引

## 输出格式

**CSV:** 扁平的表格格式,便于导入电子表格和数据库

**JSON:** 嵌套结构,适合 API 和 NoSQL 数据库

**SQL:** INSERT 语句,可直接在关系型数据库上执行

**Python 脚本:** 可执行的生成器,适合自定义或大规模数据集
