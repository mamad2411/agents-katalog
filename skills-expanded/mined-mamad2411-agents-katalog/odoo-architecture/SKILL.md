---
name: odoo-architecture-skill
description: Odoo 技术架构详解，包括三层架构、模块化设计、ORM 框架、数据库结构、模块开发规范。使用本 Skill 当需要进行 Odoo 定制开发、模块设计、性能优化、系统集成或技术选型时。
---

# Odoo 技术架构 Skill

## 快速导航

| 主题 | 参考文档 |
|------|----------|
| [三层架构](references/three-tier-architecture.md) | 表现层、逻辑层、数据层详解 |
| [模块化设计](references/modular-design.md) | 模块结构、依赖管理、Manifest |
| [ORM 框架](references/orm-framework.md) | 模型定义、字段类型、关系映射 |
| [数据库结构](references/database-schema.md) | PostgreSQL 表结构、索引优化 |
| [模块开发](references/module-development.md) | 开发规范、最佳实践、调试技巧 |

---

## 架构概览

Odoo 采用**三层架构**设计，实现关注点分离和高度可扩展性。

```
┌─────────────────────────────────────────┐
│         表现层 (Presentation)           │
│    HTML5 + CSS + JavaScript (OWL)       │
├─────────────────────────────────────────┤
│          逻辑层 (Business Logic)        │
│         Python (Odoo Framework)         │
├─────────────────────────────────────────┤
│           数据层 (Data)                 │
│         PostgreSQL (RDBMS)              │
└─────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **表现层** | HTML5, CSS3, JavaScript | 前端界面 |
| **前端框架** | OWL (Odoo Web Library) | 自研组件框架 (v15+) |
| **逻辑层** | Python 3.8+ | 业务逻辑 |
| **数据层** | PostgreSQL 12+ | 关系数据库 |
| **通信协议** | XML-RPC, JSON-RPC | 外部 API |
| **Web 服务器** | Werkzeug | Python WSGI |

---

## 三层架构详解

### 1. 表现层 (Presentation Tier)

**职责**: 用户界面展示和交互

**技术组成**:
- **HTML5/CSS3**: 页面结构和样式
- **OWL 框架**: 组件化开发（v15+）
- **QWeb**: 模板引擎
- **JavaScript**: 客户端逻辑

**关键特性**:
- 响应式设计
- 实时通信（WebSocket）
- 组件化架构
- 客户端验证

> **OWL 框架**: Odoo 自研的前端框架，类似于 React/Vue，提供组件系统、状态管理和虚拟 DOM。

### 2. 逻辑层 (Logic Tier)

**职责**: 业务逻辑处理

**技术组成**:
- **Python**: 主要编程语言
- **Odoo ORM**: 对象关系映射
- **业务对象**: 模型定义
- **控制器**: HTTP 路由处理
- **工作流引擎**: 自动化流程

**关键特性**:
- 模块化设计
- ORM 自动映射
- 继承机制
- 自动化工作流
- 安全权限控制

### 3. 数据层 (Data Tier)

**职责**: 数据存储和管理

**技术组成**:
- **PostgreSQL**: 关系数据库
- **ORM 映射**: Python 类 ↔ 数据库表
- **索引优化**: 查询性能
- **事务管理**: ACID 合规

**关键特性**:
- 自动表结构生成
- 关系映射（一对多、多对多）
- 计算字段
- 存储字段
- 数据库迁移

---

## 模块化设计

### 模块概念

Odoo 的所有功能都打包为**模块**（Modules），也称为**插件**（Addons）。

**模块类型**:
- **App 模块**: 主要功能模块（带图标，用户可见）
- **技术模块**: 依赖模块（无图标，后台支持）

### 模块目录结构

```
my_module/
├── __init__.py              # Python 包初始化
├── __manifest__.py          # 模块清单（必需）
├── models/                  # 数据模型
│   ├── __init__.py
│   ├── sale_order.py
│   └── product.py
├── controllers/             # HTTP 控制器
│   ├── __init__.py
│   └── main.py
├── views/                   # XML 视图
│   ├── menus.xml
│   └── views.xml
├── security/                # 安全配置
│   └── ir.model.access.csv
├── data/                    # 数据文件
│   └── demo_data.xml
├── static/                  # 静态资源
│   ├── src/
│   │   ├── css/
│   │   ├── js/
│   │   └── xml/
│   └── description/
│       └── icon.png
├── wizard/                  # 向导
│   ├── __init__.py
│   └── wizard_view.xml
├── report/                  # 报表
│   └── report.xml
└── tests/                   # 测试
    └── test_module.py
```

### 模块清单 (Manifest)

```python
# __manifest__.py
{
    'name': 'My Module',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Module summary',
    'description': """
        Detailed description
        of the module
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': ['base', 'sale'],  # 依赖模块
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/menus.xml',
        'data/demo_data.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,  # 是否为 App
    'auto_install': False,
}
```

---

## ORM 框架

### 模型定义

```python
from odoo import models, fields, api

class SaleOrder(models.Model):
    _name = 'sale.order'
    _description = 'Sales Order'
    _inherit = ['mail.thread']  # 继承混入
    _order = 'date_order desc'  # 默认排序
    _rec_name = 'name'  # 显示字段
    
    # 基础字段
    name = fields.Char(string='Reference', required=True)
    date_order = fields.Datetime(string='Order Date')
    amount_total = fields.Monetary(string='Total')
    
    # 关系字段
    partner_id = fields.Many2one('res.partner', string='Customer')
    order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines')
    
    # 计算字段
    amount_untaxed = fields.Monetary(compute='_compute_amounts')
    
    @api.depends('order_line.price_total')
    def _compute_amounts(self):
        for order in self:
            order.amount_untaxed = sum(line.price_subtotal for line in order.order_line)
```

### 字段类型

| 类型 | 字段类 | 说明 |
|------|--------|------|
| 文本 | Char, Text, Html | 字符串、长文本、HTML |
| 数值 | Integer, Float, Monetary | 整数、浮点、货币 |
| 日期 | Date, Datetime | 日期、日期时间 |
| 布尔 | Boolean | True/False |
| 选择 | Selection | 下拉选项 |
| 关系 | Many2one, One2many, Many2many | 关联关系 |
| 二进制 | Binary | 文件附件 |
| 计算 | Compute | 动态计算 |

---

## 数据库结构

### 表命名规则

- 模型名 `sale.order` → 表名 `sale_order`
- 自动添加字段：`id`, `create_uid`, `create_date`, `write_uid`, `write_date`

### 自动字段

```sql
-- 每个表自动包含
id              SERIAL PRIMARY KEY
create_uid      INTEGER REFERENCES res_users(id)
create_date     TIMESTAMP
write_uid       INTEGER REFERENCES res_users(id)
write_date      TIMESTAMP
```

### 关系映射

```python
# Many2one (外键)
partner_id = fields.Many2one('res.partner')
# → partner_id INTEGER REFERENCES res_partner(id)

# One2many (反向关系，不创建列)
order_line = fields.One2many('sale.order.line', 'order_id')
# → 在 sale_order_line 表创建 order_id 列

# Many2many (关联表)
tag_ids = fields.Many2many('sale.tag')
# → 创建 sale_order_sale_tag_rel 关联表
```

---

## 安全机制

### 访问控制列表 (ACL)

```csv
# security/ir.model.access.csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_sale_order_user,sale.order.user,model_sale_order,base.group_user,1,1,1,0
access_sale_order_manager,sale.order.manager,model_sale_order,sales_team.group_sale_manager,1,1,1,1
```

### 记录规则

```xml
<record id="sale_order_user_rule" model="ir.rule">
    <field name="name">User: see only own orders</field>
    <field name="model_id" ref="model_sale_order"/>
    <field name="domain_force">[('user_id','=',user.id)]</field>
    <field name="groups" eval="[(4, ref('base.group_user'))]"/>
</record>
```

---

## 继承机制

### 模型继承

```python
# 方式 1: 扩展现有模型
class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    
    custom_field = fields.Char(string='Custom Field')

# 方式 2: 原型继承（Python 类）
class MyModel(ParentModel):
    _name = 'my.model'
    _inherit = 'parent.model'
```

### 视图继承

```xml
<!-- 使用 XPath 扩展现有视图 -->
<record id="view_order_form_inherit" model="ir.ui.view">
    <field name="name">sale.order.form.inherit</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='partner_id']" position="after">
            <field name="custom_field"/>
        </xpath>
    </field>
</record>
```

---

## 开发规范

### 代码规范

- 遵循 PEP 8
- 使用 Odoo lint 工具检查
- 模型名使用小写 + 点分隔（`sale.order`）
- 字段名使用下划线分隔（`order_date`）
- 类名使用驼峰（`SaleOrder`）

### 性能优化

- 使用 `@api.depends` 而非 `@api.onchange`
- 避免在循环中执行数据库查询
- 使用 `read_group` 进行聚合查询
- 为常用查询字段添加索引

### 调试技巧

```python
# 日志记录
from odoo import _
_logger.info('Message: %s', value)
_logger.warning('Warning: %s', value)
_logger.error('Error: %s', value)

# 调试模式
# 启动时添加 --dev=all

# ORM 调试
# self.env.cr.execute("SELECT * FROM sale_order")
# print(self.env.cr.dictfetchall())
```

---

## 相关 Skill

- [odoo-introduction-skill](../odoo-introduction-skill/SKILL.md) - Odoo 简介
- [odoo-api-skill](../odoo-api-skill/SKILL.md) - API 集成
- [odoo-accounting-skill](../odoo-accounting-skill/SKILL.md) - 财务会计

---

## 使用示例

### 场景 1: 创建新模块

```
用户：我需要创建一个自定义模块来管理客户反馈

Agent:
1. 加载 odoo-architecture-skill
2. 查看"模块目录结构"
3. 创建模块框架
4. 定义数据模型
5. 配置视图和菜单
```

### 场景 2: 扩展现有模块

```
用户：如何在销售订单中添加自定义字段？

Agent:
1. 加载 odoo-architecture-skill
2. 查看"继承机制"
3. 使用 _inherit 扩展模型
4. 使用 XPath 扩展视图
5. 配置安全权限
```

### 场景 3: 性能优化

```
用户：我的模块查询很慢，如何优化？

Agent:
1. 加载 odoo-architecture-skill
2. 查看"开发规范 → 性能优化"
3. 检查是否有 N+1 查询
4. 建议添加索引
5. 使用 read_group 优化聚合
```

---

*Skill 版本：v1.0*
*支持 Odoo 版本：17.0 - 18.0*
*最后更新：2026-04-12*
