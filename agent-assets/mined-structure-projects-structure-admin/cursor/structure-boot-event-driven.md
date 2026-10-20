---
description: |
  当用户要求"发消息/事件驱动/Event/Stream"时触发（structure-boot 栈）。
  覆盖 structure-boot 项目事件驱动的特殊约束：EventManager + StreamEvent + 数据权限。

triggers:
  - 发消息
  - 事件驱动
  - Event
  - Stream
  - EventManager
  - StreamEvent
  - 消息队列
  - structure-boot 事件

priority: high
alwaysApply: false
globs: "**/*Event*.java, **/*Listener*.java, **/*Handler*.java, changes/**/*.md"

category: event-driven
stack: structure-boot
role: developer
maturity: stable

reads-before-action:
  - wiki/structure-boot/developer.md
  - wiki/structure-boot/components.md

related-skills:
  - coding

when-to-use: |
  在 structure-boot 项目里发布 / 消费事件
when-not-to-use: |
  仅阅读事件代码
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


# structure-boot 事件驱动规范

> 完整规范详见 `wiki/structure-boot/components.md`

## 硬约束（MUST）

### 发布

- ✅ **MUST** 实现 `cn.structure.infra.event.Event` 接口
- ✅ **MUST** 用 `EventManager.publish(event)` 发布
- ✅ **MUST** 跨服务事件用 `MESSAGE_EVENT`（走 `DataScopeStreamBridge` 数据权限包装）

### 消费

**Spring 事件（本 JVM）**：
- ✅ **MUST** 用 `@EventListener` 或 `@TransactionalEventListener`

**Binding 模型（跨服务推荐）**：
- ✅ **MUST** `Consumer<Message<T>>` Bean 名 = `@StreamEventListener.bindingName`
- ✅ **MUST** `Consumer` 内只 `dispatch(...)`
- ✅ **MUST** 多状态用 `condition` SpEL（`#event.xxx`）

**Router 模型**：
- ✅ **MUST** 用 `StreamEvent<T>` 信封 + `@StreamRouteHandler(eventType, businessType, condition)`
- ✅ **MUST** 签名 `(T payload, StreamEvent<T> event)` 双参

## 禁止（MUST NOT）

- ❌ 跨服务直接发 Spring 事件（应用 MESSAGE_EVENT）
- ❌ 跳过 `DataScopeStreamBridge`（失去数据权限包装）
- ❌ 在 `Consumer` 里写业务逻辑（应 dispatch 给具体 handler）

## 关联

- Wiki：`wiki/structure-boot/components.md`
- 技能：`coding`
- 规则：`structure-boot-cache`（DataScope 相关）
