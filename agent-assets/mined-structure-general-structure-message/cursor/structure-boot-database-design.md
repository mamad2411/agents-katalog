---
description: |
  当用户要求"设计表/写迁移/MyBatis/Mapper"时触发（structure-boot 栈）。
  覆盖 structure-boot 项目数据库设计的特殊约束：MyBatis-Plus + Flyway + Delegate。

triggers:
  - 设计表
  - 写迁移
  - MyBatis
  - Mapper
  - Flyway
  - 数据库
  - structure-boot 数据库

priority: high
alwaysApply: false
globs: "**/db/migration/**/*.sql, **/*Mapper.java, **/*Mapper.xml, **/*PO.java, changes/**/*.md"

category: database-design
stack: structure-boot
role: developer
maturity: stable

reads-before-action:
  - wiki/structure-boot/developer.md
  - wiki/_common/database-design.md

related-skills:
  - database-design
  - structure-boot-new-repository

when-to-use: |
  在 structure-boot 项目里设计表、写迁移、写 Mapper
when-not-to-use: |
  仅查询数据
version: "0.3.0"
since: "2026-08-13"
---

> **通用规范** (已安装于 `wiki/_common/`):
> - `wiki/_common/api-design.md`: API 设计通用原则
> - `wiki/_common/architecture.md`: 分层架构通用原则
> - `wiki/_common/cache-design.md`: 缓存设计规范
> - `wiki/_common/ci-cd-pipeline.md`: CI/CD 流水线规范
> - `wiki/_common/code-review-checklist.md`: Code Review 通用原则
> - `wiki/_common/coding-conventions.md`: 通用编码约定（coding-conventions）
> - `wiki/_common/concurrency.md`: 并发编程规范
> - `wiki/_common/database-design.md`: 数据库设计规范
> - `wiki/_common/deployment.md`: 部署规范
> - `wiki/_common/detailed-design.md`: 详细设计（LLD）规范
> - `wiki/_common/distributed-transaction.md`: 分布式事务规范
> - `wiki/_common/docker.md`: Docker 规范
> - `wiki/_common/documentation.md`: 文档管理规范
> - `wiki/_common/error-handling.md`: 错误处理公约
> - `wiki/_common/git-workflow.md`: Git 工作流（分级规范）
> - `wiki/_common/git.md`: Git 分支策略与工作流规范
> - `wiki/_common/github-workflow.md`: GitHub 工作流（gh CLI + PR + Release）
> - `wiki/_common/high-level-design.md`: 概要设计（HLD）规范
> - `wiki/_common/kubernetes.md`: Kubernetes 规范
> - `wiki/_common/legacy-onboarding.md`: 老项目接入指南
> - `wiki/_common/logging.md`: 日志规范
> - `wiki/_common/maven-publish.md`: Maven 发布规范
> - `wiki/_common/messaging.md`: 消息队列规范
> - `wiki/_common/migration-strategies.md`: 迁移策略详解
> - `wiki/_common/model-design.md`: 模型设计规范
> - `wiki/_common/naming.md`: 通用命名规范
> - `wiki/_common/npm-publish.md`: npm 发布规范
> - `wiki/_common/observability.md`: 可观测性规范
> - `wiki/_common/performance.md`: 性能优化规范
> - `wiki/_common/project-form-decision.md`: 项目形态决策指南
> - `wiki/_common/project-structure.md`: 项目结构约定
> - `wiki/_common/requirement-analysis.md`: 需求分析规范
> - `wiki/_common/security.md`: 安全基线
> - `wiki/_common/testing-strategies.md`: 测试策略
> - `wiki/_common/transaction.md`: 本地事务规范
> - `wiki/_common/version-management.md`: 版本管理规范
> 
> 在编码决策前应加载对应规范文件。


# structure-boot 数据库设计规范

> 完整规范详见 `wiki/structure-boot/developer.md` + `wiki/_common/database-design.md`

## 硬约束（MUST）

- ✅ **MUST** 用 `mybatis-plus-spring-boot4-starter`（**不是** `mybatis-plus-boot-starter`）
- ✅ **MUST** PO 含 `@TableName` / `@TableId(type=AUTO)` / `@TableLogic`
- ✅ **MUST** 用 MyBatis-Plus `Wrappers` / `LambdaQueryWrapper`（不手写 SQL）
- ✅ **MUST** 持久化用 `RepositoryFacade<Entity, ID, Delegate>` + `MybatisPlusRepositoryDelegate<Entity, PO, Long>` 模式
- ✅ **MUST** 迁移脚本在 `<module>-repository-mybatis/src/main/resources/db/migration/`
- ✅ **MUST** 迁移脚本命名 `V<major>_<minor>_<patch>__<description>.sql`
- ✅ **MUST** 表含审计字段 + 逻辑删除 + 多租户字段

## 禁止（MUST NOT）

- ❌ 手写 SQL（应用 Wrapper）
- ❌ `SELECT *`
- ❌ 在 `WHERE` 里对字段做函数操作
- ❌ 修改已发布的迁移脚本
- ❌ 在 Service / Controller 直接用 `baseMapper`（应在 Delegate 层）

## 关联

- Wiki：`wiki/structure-boot/developer.md` `wiki/_common/database-design.md`
- 技能：`database-design` / `structure-boot-new-repository`
- 规则：`common-database-design`
