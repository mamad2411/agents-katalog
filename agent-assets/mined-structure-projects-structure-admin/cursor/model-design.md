---
description: |
triggers:
  - 设计模型
  - 建表
  - 设计实体
  - 加字段
  - 设计 DTO
  - 设计 VO
  - 设计表
  - 设计用户表
  - model
  - entity
  - table
  - DTO
  - VO
role: architect
priority: high
category: model-design
stack: _common
alwaysApply: false
---


# 模型设计

> 按 DDD Entity/PO/DTO/VO 分层规范设计模型。**MUST 区分四层模型，禁止混用**。

## 前置条件

- 变更提案存在
- 已识别项目栈（DDD / 单体）

## 执行步骤

### 第 1 步：识别模型边界

**MUST 与用户确认**：
- 这个模型属于哪个 bounded context？
- 哪些字段属于本模型，哪些属于关联模型？
- 是一对一 / 一对多 / 多对多关系？

### 第 2 步：设计数据表（PO 对应）

```sql
CREATE TABLE `user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` VARCHAR(64) NOT NULL COMMENT '用户名',
  `email` VARCHAR(128) COMMENT '邮箱',
  `tenant_id` BIGINT NOT NULL COMMENT '租户 ID',
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_deleted` TINYINT NOT NULL DEFAULT 0 COMMENT '逻辑删除',
  PRIMARY KEY (`id`),
  KEY `idx_username` (`username`),
  KEY `idx_tenant_id` (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
```

**关键约束**：
- 表名 MUST `lower_snake_case`
- 字段名 MUST `lower_snake_case`
- MUST 含审计字段（`create_time` / `update_time` / `is_deleted` / `tenant_id`）
- MUST 有合适索引

### 第 3 步：设计四层模型

#### Entity（领域实体）
- 位置：`{X}-domain` 模块
- 命名：`{X}Entity`
- 示例：`UserEntity`
- 说明：业务领域模型，不含持久化注解

#### PO（持久化对象）
- 位置：`{X}-repository-mybatis` 模块
- 命名：`{X}PO`
- 示例：`UserPO`
- 说明：数据库表映射，含 `@TableName` / `@TableId` / `@TableLogic` 等 MyBatis-Plus 注解

#### DTO（数据传输对象）
- 位置：`{X}-common` 模块
- 命名：`{X}DTO`
- 示例：`UserDTO`
- 说明：服务间传输（Feign 调用）

#### VO（视图对象）
- 位置：`{X}-common` 模块
- 命名：`{X}VO`
- 示例：`UserVO`
- 说明：返回给前端的视图

#### Query（查询对象）
- 位置：`{X}-common` 模块
- 命名：`{X}Query`
- 示例：`UserQuery`
- 说明：分页 / 条件查询

### 第 4 步：生成代码骨架

按 `wiki/<stack>/developer.md` 中的代码模板生成。

### 第 5 步：生成 Flyway 迁移脚本

```
db/migration/V1_2_0__add_user_table.sql
```

## 产出物

- 模型设计文档（融入 proposal 或单独 model.md）
- 数据表 DDL
- Flyway 迁移脚本
- Entity / PO / DTO / VO / Query 类骨架

## 完成标准

- 模型边界经用户确认
- 表设计含所有审计字段
- 四层模型（Entity/PO/DTO/VO/Query）齐全
- 命名符合规范

## 关联

- 前置：`requirement-analysis`
- 后续：`coding`（按模型编码）
- Wiki：`wiki/_common/model-design.md` `wiki/_common/database-design.md`
