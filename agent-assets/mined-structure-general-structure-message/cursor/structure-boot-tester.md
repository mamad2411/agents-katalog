---
description: structure-projects 生态测试约束。编写测试代码时生效。
triggers:
  - 测试
  - 写测试
  - 跑测试
  - 补测试
  - test
  - 单测
  - 集成测试
  - 测试用例
priority: medium
alwaysApply: false
globs: "**/test/**/*.java, **/*Test.java, **/*IT.java, **/*.test.ts, **/*.spec.ts, changes/**/*.md, docs/**/*.md, README.md, AGENTS.md, CLAUDE.md"
category: testing
stack: structure-boot
role: tester
maturity: stable
related-skills:
  - unit-testing
reads-before-action:
  - wiki/structure-boot/tester.md
  - wiki/_common/naming.md
when-to-use: 编辑 structure-boot 栈相关代码或文档时
when-not-to-use: 仅阅读代码不修改
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


# structure-projects 测试规则

完整规范见 `wiki/tester.md`。以下为关键内联规则：

## 测试工作流（MUST）
- 每开发一个功能 **立即** 写单元测试，**单测通过才能做下一个功能**
- 功能有修改时 **同步修改测试** 并通过
- 业务完成后写 **业务流程集成测试**（`XxxIT`），通过才算交付
- 覆盖正常+异常+边界；断言验证行为与数据（**禁止** 僵尸断言）
- **提交前**：`mvn clean test` 全部通过 + `mvn clean package -DskipTests` 编译通过

## 分层与命名
- `XxxTest` — 单元测试，不启动 Spring 上下文
- `XxxIT` — 集成测试，**必须** 用真实中间件（Testcontainers），**禁止** Mock 数据库/Redis/MQ
- Feign 跨服务调用必须有契约测试

## 生态必须覆盖
- 多租户：覆盖"租户隔离"与"无租户上下文兜底"
- 数据权限：验证行级过滤实际生效，而非仅看 200
- 统一异常：断言业务异常返回统一错误码
- 读写分离：覆盖 `@ReadDelegate` 失败回退

## Mock 边界
- 只允许 Mock 进程边界（第三方 HTTP / 外部 SaaS）
- 禁止 Mock 自己项目的 `Repository` / `Service` / `Mapper`

## 禁止
- 僵尸断言（只 `assertNotNull`）
- `Thread.sleep` 等待异步 —— 用 Awaitility
- 无 issue 关联的 `@Disabled`

详细规则请读 `wiki/tester.md`。
