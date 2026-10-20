---
description: structure-projects 生态评审约束。审查 PR / diff / 设计文档时生效。
triggers:
  - 评审
  - 审查
  - 检查
  - 看一下
  - 代码
  - 改动
  - PR
  - review
priority: medium
alwaysApply: false
globs: "**/*.md, changes/**/*.md, docs/**/*.md, README.md, AGENTS.md, CLAUDE.md"
category: code-review
stack: structure-boot
role: reviewer
maturity: stable
related-skills:
  - expert-review
reads-before-action:
  - wiki/structure-boot/reviewer.md
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


# structure-projects 评审规则

完整规范见 `wiki/reviewer.md`。以下为关键内联规则：

## 评审顺序
1. 包名与坐标 → 2. 模块依赖方向 → 3. 工具类优先级（自定义限 infra 层） → 4. Bean 注入（构造器 > @Resource > @Autowired 谨慎） → 5. 持久化路径（RepositoryFacade + 显式 toEntity/toPo） → 6. POJO 规范（@Builder + 无参构造 + 参数 ≤ 3） → 7. 统一性（CommonException + ResultUtilSimpleImpl + ResResultVO） → 8. API 出入参（分页签名 `page(query, reqPage)` + CRUD 命名统一） → 9. 用户上下文（非控制层 MUST） → 10. 数据权限（缓存/事件用框架包装） → 11. 多租户 → 12. 安全 → 13. 版本兼容 → 14. 测试 → 15. 文档

## 硬性驳回项
- 包名混淆 `cn.structure` ↔ `cn.structured`
- DDD `application`/`domain` 直接注入 `Mapper`/`PO`
- `MybatisPlusDelegate` 未显式重写 `toEntity`/`toPo`
- 业务层抛非 `CommonException` 异常
- 控制层用 `throw` 抛业务异常（应用 `ResultUtilSimpleImpl.fail`）
- 业务异常缺 `{X}ExceptionEnum` 枚举
- POJO 缺无参构造
- 非控制层用 `SecurityUtils`/`SecurityContextHolder`（应用用户上下文）
- 缓存/事件未用框架的数据权限包装工具（跨服务消息未走 `DataScopeStreamBridge`）
- **事件**：未实现 `Event` 接口；跨服务未声明 `MESSAGE_EVENT`；绕过 `EventManager` 直连 publisher/MQ
- **Binding 消费**：`Consumer` Bean 名 ≠ `@StreamEventListener.bindingName`；`Consumer` 内直接写业务
- **Router 消费**：`@StreamRouteHandler` 签名非 `(T payload, StreamEvent<T> event)` 双参
- 自定义工具类放在非 infra 层
- 业务 SQL 手写 `WHERE tenant_id = ?`
- 从请求参数/Header 读租户 ID
- Controller 返回非 `ResResultVO<T>`
- 绕过 Starter 自行装配且无说明
- 集成测试 Mock 数据库/Redis/MQ
- 无 issue 关联的 `@Disabled` 测试
- 新功能无单测；改功能未同步测试；缺流程级集成测试；僵尸断言；测试/编译失败仍提交
- 服务间调用用 `RestTemplate`/`WebClient`/手写 HTTP（MUST 用 `@FeignClient`）
- `@FeignClient` 未声明 `fallback`/`fallbackFactory`
- 强一致性场景 fallback 静默返回兜底数据（MUST 抛 `CommonException`）
- 业务序列化用 Jackson/Gson（MUST 用 FastJSON）

## 建议性反馈
- 使用 `@Autowired` 字段注入（应优先构造器或 `@Resource`）
- 函数参数 > 3 未用包装类
- 命名不统一（`list`/`page`/`queryPage` 混用）
- Hutool 已实现却手写工具
- 绕过 Starter 重新实现

## 已知历史遗留（识别但不一定驳回）
- `cn.structured.{X}.repository.repository.*`（双 "repository"）— 修正需确认
- 旧 Controller javadoc 含 `@since JDK1.8` 但项目已 JDK 17+ —— NIT
- `UserContext.getLoneDeptIds()` 拼写错误（框架源码问题，业务使用合理，**不因此驳回业务 PR**）
- 业务用 `UserContext.get()` + `Long.parseLong(...)` 而非 `getLongUserId()` —— SHOULD-FIX，不驳回

## 反馈格式
每条反馈含：位置（`file:line`）、级别（MUST-FIX / SHOULD-FIX / NIT / QUESTION）、依据（引用规则条目）、建议（可落地）。

详细规则请读 `wiki/reviewer.md`。
