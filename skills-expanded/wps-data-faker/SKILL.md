---
name: wps-data-faker
description: |
  模拟数据生成。需要测试数据？一键生成逼真的中国式假数据：张伟、138xxxx1234、
  身份证号（含校验位）、北京市朝阳区xx路。填充模板、测试系统、做演示文档都好用。
  用于帮助用户生成测试数据。当用户提到测试数据、假数据、模拟数据时触发。
  Generates realistic Chinese test data - names, phones, IDs, addresses.
license: MIT
user-invocable: true
argument-hint: '[字段列表] [数量]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 模拟数据生成
  description_zh: 生成中国式模拟数据，包括姓名、手机号、身份证、地址等
  tags:
    - 测试数据
    - 模拟
    - 假数据
    - Excel
    - WPS
  version: 1.0.1
  license: MIT
---

# 测试数据生成器

指定字段 → 生成逼真的中国式测试数据。填充模板、测试系统的利器。

> 再也不用手动编造"张三李四王五"了。

## When to Use

- 需要测试数据填充Excel/表格
- 文档模板需要示例数据
- 系统测试需要批量数据
- 演示文档需要逼真样例
- 用户说"帮我造点测试数据""生成假数据"

## When NOT to Use

- 真实数据清洗 → 使用 `wps-data-clean`
- 数据分析 → 使用 `wps-pivot`

## 支持的字段类型

| 字段 | 示例 | 说明 |
|------|------|------|
| 姓名 | 张伟、李芳 | 常见姓+名组合 |
| 性别 | 男、女 | 与姓名匹配 |
| 年龄 | 25-55 | 可指定范围 |
| 手机号 | 138xxxx1234 | 合规号段 |
| 身份证号 | 110105199001011234 | 含校验位 |
| 邮箱 | zhangwei@qq.com | 常见邮箱后缀 |
| 地址 | 北京市朝阳区xx路xx号 | 真实地名 |
| 公司名 | XX科技有限公司 | 行业+类型组合 |
| 部门 | 技术部、销售部 | 常见部门 |
| 职位 | 经理、工程师 | 与部门匹配 |
| 日期 | 2025-01-15 | 可指定范围 |
| 金额 | 1,234.56 | 可指定范围 |
| 工号 | EMP001 | 自定义前缀 |

## 工作流程

### Step 1: 确认数据需求

- 需要哪些字段
- 生成多少条
- 输出格式（Excel/CSV）
- 特殊约束（如年龄范围、地区限定）

### Step 2: 生成数据

```python
import random
import string
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
import os

class ChineseFaker:
    """中国式测试数据生成器"""

    SURNAMES = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    MALE_NAMES = ['伟', '强', '磊', '军', '勇', '杰', '涛', '明', '超', '华',
                  '志强', '建国', '建华', '国强', '文彬', '浩然', '宇航', '子轩']
    FEMALE_NAMES = ['芳', '娜', '敏', '静', '丽', '婷', '雪', '慧', '莹', '倩',
                    '秀英', '玉兰', '淑芬', '美玲', '雨萱', '欣怡', '诗涵']
    CITIES = ['北京市', '上海市', '广州市', '深圳市', '杭州市', '成都市',
              '武汉市', '南京市', '重庆市', '西安市', '苏州市', '天津市']
    DISTRICTS = ['朝阳区', '海淀区', '浦东新区', '南山区', '西湖区',
                 '武侯区', '江岸区', '玄武区', '渝中区', '雁塔区']
    COMPANIES = ['科技', '信息', '网络', '智能', '数据', '云计算', '教育',
                 '医疗', '金融', '咨询']
    COMPANY_SUFFIX = ['有限公司', '股份有限公司', '集团', '科技有限公司']
    DEPARTMENTS = ['技术部', '销售部', '市场部', '人力资源部', '财务部',
                   '行政部', '产品部', '运营部', '客服部', '法务部']
    POSITIONS = {
        '技术部': ['高级工程师', '工程师', '架构师', '技术经理', '开发主管'],
        '销售部': ['销售经理', '销售主管', '客户经理', '销售代表'],
        '市场部': ['市场经理', '品牌主管', '市场专员', '策划经理'],
    }
    PHONE_PREFIXES = ['130','131','132','133','134','135','136','137','138',
                      '139','150','151','152','153','155','156','157','158',
                      '159','170','176','177','178','180','181','182','183',
                      '185','186','187','188','189']

    def name(self, gender=None):
        g = gender or random.choice(['男', '女'])
        surname = random.choice(list(self.SURNAMES))
        given = random.choice(self.MALE_NAMES if g == '男' else self.FEMALE_NAMES)
        return surname + given, g

    def phone(self):
        return random.choice(self.PHONE_PREFIXES) + ''.join(
            random.choices('0123456789', k=8))

    def id_card(self, birth_year=None):
        area = random.choice(['110105', '310101', '440305', '330102',
                               '510107', '420102', '320102', '500103'])
        year = birth_year or random.randint(1970, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        seq = f'{random.randint(1,999):03d}'
        base = f'{area}{year}{month:02d}{day:02d}{seq}'
        # 校验位
        weights = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
        check = '10X98765432'
        s = sum(int(base[i]) * weights[i] for i in range(17))
        return base + check[s % 11]

    def email(self, name_pinyin=None):
        prefix = name_pinyin or ''.join(random.choices(string.ascii_lowercase, k=6))
        domain = random.choice(['qq.com', '163.com', '126.com',
                                'gmail.com', 'outlook.com', 'sina.com'])
        return f'{prefix}{random.randint(1,999)}@{domain}'

    def address(self):
        city = random.choice(self.CITIES)
        district = random.choice(self.DISTRICTS)
        road = f'{"".join(random.choices(list("东西南北中和平建设人民解放"),k=2))}路'
        num = random.randint(1, 200)
        return f'{city}{district}{road}{num}号'

    def company(self):
        city = random.choice(self.CITIES).replace('市', '')
        industry = random.choice(self.COMPANIES)
        suffix = random.choice(self.COMPANY_SUFFIX)
        return f'{city}{industry}{suffix}'

    def amount(self, min_val=100, max_val=100000):
        return round(random.uniform(min_val, max_val), 2)

    def date(self, start='2024-01-01', end='2026-12-31'):
        s = datetime.strptime(start, '%Y-%m-%d')
        e = datetime.strptime(end, '%Y-%m-%d')
        delta = (e - s).days
        d = s + timedelta(days=random.randint(0, delta))
        return d.strftime('%Y-%m-%d')


def generate_test_data(fields, count, output_path=None):
    """生成测试数据Excel"""
    faker = ChineseFaker()
    wb = Workbook()
    ws = wb.active
    ws.title = "测试数据"

    # 表头
    header_fill = PatternFill('solid', fgColor='2C3E50')
    header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
    for col, field in enumerate(fields, 1):
        cell = ws.cell(row=1, column=col, value=field)
        cell.font = header_font
        cell.fill = header_fill

    # 生成数据
    for row in range(2, count + 2):
        name, gender = faker.name()
        for col, field in enumerate(fields, 1):
            if field == '姓名':
                ws.cell(row=row, column=col, value=name)
            elif field == '性别':
                ws.cell(row=row, column=col, value=gender)
            elif field == '手机号':
                ws.cell(row=row, column=col, value=faker.phone())
            elif field == '身份证号':
                ws.cell(row=row, column=col, value=faker.id_card())
            elif field == '邮箱':
                ws.cell(row=row, column=col, value=faker.email())
            elif field == '地址':
                ws.cell(row=row, column=col, value=faker.address())
            elif field == '公司':
                ws.cell(row=row, column=col, value=faker.company())
            elif field == '部门':
                ws.cell(row=row, column=col, value=random.choice(
                    ChineseFaker.DEPARTMENTS))
            elif field == '金额':
                ws.cell(row=row, column=col, value=faker.amount())
            elif field == '日期':
                ws.cell(row=row, column=col, value=faker.date())
            elif field == '工号':
                ws.cell(row=row, column=col, value=f'EMP{row-1:04d}')

    if not output_path:
        output_path = f'测试数据_{count}条.xlsx'
    wb.save(output_path)
    return os.path.abspath(output_path)
```

### Step 3: 交付

1. 生成Excel文件
2. 说明数据为虚构，不含真实个人信息
3. 身份证号含正确校验位（但地区码为测试用）

## 示例

```bash
# 生成员工数据
/wps-data-faker 生成100条员工测试数据，包含姓名、手机号、部门、工号

# 指定字段
/wps-data-faker 50条数据：姓名、身份证号、地址、公司名

# 填充模板
/wps-data-faker 给合同模板生成10组测试数据
```
