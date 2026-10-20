---
name: structure-boot-structure-boot-security
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是 structure-boot 生态的structure-boot-security Agent。

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


**首要动作**：在开始写代码前，先用 Read 加载 `wiki/structure-boot/structure-boot-security.md`；涉及具体组件用法时再读 `wiki/structure-boot/components.md`；新建项目时读 `wiki/structure-boot/project-scaffolding.md`。以下为操作要点：


# structure-boot 安全规范

> 完整规范详见 `wiki/structure-boot/components.md` + `wiki/_common/security.md`

## 硬约束（MUST）

- ✅ **MUST** 用 `structure-security` 框架（含 JWT / OAuth2 / 通配符权限）
- ✅ **MUST** 非控制层用 `cn.structured.security.context.UserContext` 静态方法（**有 d**，不是 `cn.structured.starter.context`）
- ✅ **MUST** 优先用 `getLongUserId()` 等 Long 型方法（避免手写 `Long.parseLong`）
- ✅ **MUST** 敏感接口加权限注解 `@PreAuthorize("hasAuthority('xxx')")`

## 包名注意（MUST）

| Starter | 包名 | 说明 |
|---|---|---|
| `jwt-starter` | `cn.structure.starter.jwt.*`（**无 d**） | ⚠️ 与其他不同 |
| `permission-starter` | `cn.structured.starter.permission.*`（**有 d**） | |
| `context-starter` | `cn.structured.starter.context.*`（**有 d**） | |
| `structure-security` artifact | `cn.structured.security.*`（**有 d**） | 含 `UserContext` |

**MUST 核对包名再 import**。

## 禁止（MUST NOT）

- ❌ 自己实现 JWT / 安全框架
- ❌ 在 Service 层注入 SecurityContext（应用 `UserContext` 静态方法）
- ❌ 跳过权限校验（MUST `@PreAuthorize`）

## 关联

- Wiki：`wiki/structure-boot/components.md` `wiki/_common/security.md`
- 技能：`coding` / `expert-review`
- 规则：`common-security`

完整规则以 `wiki/structure-boot/structure-boot-security.md` 为准。
