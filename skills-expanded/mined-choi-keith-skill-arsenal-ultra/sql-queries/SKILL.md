---
name: sql-queries
description: "根据自然语言描述生成 SQL 查询。支持 BigQuery、PostgreSQL、MySQL 及其他方言。可从上传的图表或文档中读取数据库 schema。适用于编写 SQL、构建数据报表、探索数据库,或将业务问题转化为查询。"
---

# SQL 查询生成器

## 目的
将自然语言需求转化为跨多种数据库平台的优化 SQL 查询。该技能帮助产品经理、分析师和工程师无需手工编写语法即可生成准确的查询。

## 工作原理

### 第 1 步:理解数据库 Schema
- 如果你提供 schema 文件(SQL、文档或图表描述),我会读取并分析它
- 提取表名、列定义、数据类型和关联关系
- 识别主键、外键和索引策略

### 第 2 步:处理你的请求
- 明确你需要检索或分析的确切数据
- 确认 SQL 方言(BigQuery、PostgreSQL、MySQL、Snowflake 等)
- 询问任何额外需求(过滤条件、聚合方式、排序)

### 第 3 步:生成优化查询
- 编写充分利用数据库结构的高效 SQL
- 为复杂逻辑添加注释说明
- 针对大数据集提供性能考量
- 如适用,提供备选方案

### 第 4 步:解释与测试
- 用通俗易懂的语言解释查询逻辑
- 建议如何测试或验证结果
- 提供性能优化建议
- 如需要,生成测试脚本或示例数据

## 使用示例

**示例 1:基于 Schema 文件查询**
```
上传你的 database_schema.sql 文件,然后说:
"生成一个查询,找出过去 30 天内注册
且至少有 5 个活跃会话的用户"
```

**示例 2:基于图表描述查询**
```
"这是我的数据库:Users 表 (id, email, created_at),Sessions 表
(id, user_id, timestamp, duration)。生成一个查询,计算 2026 年 1 月
每位用户的平均会话时长。"
```

**示例 3:复杂分析查询**
```
"创建一个 BigQuery 查询,按地区和客户层级分析我们的收入,
并包含同比增长率。"
```

## 核心能力

- **多方言支持**:支持 BigQuery、PostgreSQL、MySQL、Snowflake、SQL Server
- **文件读取**:读取 schema 文件、SQL 转储文件和数据文档
- **查询优化**:建议索引、分区和性能改进方案
- **解释说明**:拆解查询逻辑,便于学习和撰写文档
- **测试**:可生成测试查询和示例数据脚本
- **脚本执行**:为你的数据库创建可执行的 SQL 脚本

## 获得最佳结果的建议

1. **提供背景**:分享你的数据库 schema 或结构
2. **描述具体**:清楚说明需要什么数据以及过滤条件
3. **注明数据库**:指明你使用的 SQL 方言
4. **包含约束**:说明数据量、时间范围和性能要求
5. **明确格式**:如需特定输出,说明查询结果的格式要求

## 输出格式

你将收到:
- **SQL 查询**:可直接用于生产环境、带注释的 SQL 代码
- **解释说明**:查询的作用和工作原理
- **性能说明**:优化建议和注意事项
- **测试脚本**(如有要求):示例数据和验证查询

---

### 延伸阅读

- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [How to Become a Technology-Literate PM](https://www.productcompass.pm/p/how-to-become-a-technology-literate)
