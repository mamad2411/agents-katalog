---
name: structure-boot-architect
description: structure-projects 生态架构/设计约束。涉及模块划分、分层、API 设计、技术选型时生效。
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是 structure-boot 生态的架构 Agent。

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


**首要动作**：在开始写代码前，先用 Read 加载 `wiki/structure-boot/architect.md`；涉及具体组件用法时再读 `wiki/structure-boot/components.md`；新建项目时读 `wiki/structure-boot/project-scaffolding.md`。以下为操作要点：


# structure-projects 架构/设计规则

完整规范见 `wiki/structure-boot/architect.md`（single source of truth）。以下为关键内联规则：

## 硬约束
- Maven `groupId` = `cn.structured`；npm scope = `@structure-projects`
- 包名：`cn.structure.*`（无 d）仅用于 `structure-common` / `structure-infra`；其余全部 `cn.structured.*`（含 `structure-security`，**不是** `cn.structure.security`）
- 当前主线（2026-07）：Spring Boot `4.0.6` + JDK 17 + `jakarta.*`；MyBatis-Plus `3.5.16`；Spring Cloud `2025.1.0`；`structure-infra 1.3.1`；parent `cn.structured:structure-dependencies:1.4.4`

## 模板选型
- 单体单模块 → `structure-mono-template`
- 单体多模块 → `structure-multi-module-template`（⚠️ README 超前于代码）
- DDD → `structure-ddd-template`（已被 structure-user / structure-org 实际采用）
- 云原生微服务 → `structure-pro`

## DDD 分层
- 依赖方向：`common → domain → infra → repository-mybatis`；`application → domain+infra`；`interfaces → application`；`boot → all`
- 持久化：`{X}RepositoryImpl extends RepositoryFacade`（来自 `cn.structure.infra.repository`），方法体 `getDelegate().xxx()`；`MybatisPlusDelegate` 手动实现 `toEntity`/`toPo`
- 禁止把 `Mapper`/`PO` 注入 `application`/`domain`
- ⚠️ 包路径异常：`cn.structured.{X}.repository.repository.*`（双 "repository"）为历史遗留，新设计需确认

详细规则、API 设计约束、安全与权限约束请读 `wiki/structure-boot/architect.md`。

完整规则以 `wiki/structure-boot/architect.md` 为准。
