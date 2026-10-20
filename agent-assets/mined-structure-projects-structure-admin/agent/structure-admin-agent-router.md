---
description: 动作路由表 - 任何动作前 MUST 先查表确定该读什么、调什么
triggers:
  - always
category: routing
stack: _common
role: router
alwaysApply: true
priority: 0
---

# 动作路由（MUST 遵守）

> 本表由安装器基于所有规则/技能元数据自动生成。
> 任何用户意图必须先在下表找到对应条目，按"必读 / 必调用 / 遵守"执行。
> 未列出场景：先 `Glob wiki/**/*.md` 找相关规范；不确定时问用户。

## 第 0 步：项目栈识别（MUST 最先执行）

开始任何工作前 MUST 先识别当前项目的技术栈：

```bash
# 通过依赖文件识别
ls wiki/                    # 看有哪些栈级 wiki 目录
cat pom.xml 2>/dev/null | grep -o "cn\.structured\|spring-boot" | head -3
cat package.json 2>/dev/null | grep -o "@structure-projects\|vue\|react\|next" | head -3
```

| 标识 | 推断栈 |
|---|---|
| `pom.xml` 含 `cn.structured` | `structure-boot` |
| `pom.xml` 含 `spring-boot-starter` 但无 `cn.structured` | `spring-boot` |
| `package.json` 含 `@structure-projects` + `vue` | `vue3` |
| `package.json` 含 `react`（无 @structure-projects） | `react` |
| `package.json` 含 `next` | `nextjs` |

识别出栈后 MUST 按以下顺序加载约束：

```
1. 栈级规则（<stack>-*.mdc）       ← 优先级最高
2. 栈级 Wiki（wiki/<stack>/*.md）  ← 必细参考
3. 栈级技能（<stack>-<action>）    ← 栈级动作
4. _common 规则（common-*.mdc）    ← 通用兜底
5. _common Wiki（wiki/_common/）   ← 通用参考
6. _common 技能                    ← 通用动作
```

**核心原则**：**栈级优先，_common 兜底**。

识别后 MUST Read：
- `wiki/<stack>/developer.md`（开发约束）
- `wiki/<stack>/components.md`（生态组件清单 + 版本约束）

**完整规则**：
- 栈识别详细规则见 `common-project-stack-detection` 规则
- 用户交互信任级别见 `common-trust-level` 规则

**禁止**：
- ❌ MUST NOT 只看 _common 规则就开始工作
- ❌ MUST NOT 凭 LLM 自带知识选技术栈版本
- ❌ MUST NOT 忽略栈级规则里的"必选组件"

无法识别栈时 MUST 问用户，禁止默认。

---


## 当前栈硬约束（MUST 遵守）

**识别栈**：`structure-boot`

本项目的硬约束（来自 `stack-constraints`）：

```yaml
structure-boot:
    spring-boot-version: "4.0.6"
    jdk: "17+"
    parent: "cn.structured:structure-dependencies:1.4.4"
    required-components:
      - structure-security
      - structure-infra
      - structure-restful-web-starter
    forbidden:
      - "Jackson / Gson"
      - "RestTemplate / WebClient"
      - "Spring Boot 3.x"
```

**禁止**：
- ❌ MUST NOT 忽略上述必选组件
- ❌ MUST NOT 使用上述 forbidden 项
- ❌ MUST NOT 凭 LLM 印象选版本（MUST 按上述版本约束）

---

## hotfix-release（SDLC: deployment，priority: critical）
- **触发词**：热修复/hotfix/紧急上线/线上bug
- **MUST 调用 skill**：`hotfix-release`

## rollback（SDLC: deployment，priority: critical）
- **触发词**：回滚/回退/撤销发布/rollback
- **MUST 调用 skill**：`rollback`

## api-design（SDLC: design，priority: high）
- **触发词**：设计接口/定 API/写 OpenAPI/定义接口
- **MUST 调用 skill**：`api-design`

## archive-change（SDLC: deployment，priority: high）
- **触发词**：归档/完成变更/结束变更/archive
- **MUST 调用 skill**：`archive-change`

## ci-gate（SDLC: ci，priority: high）
- **触发词**：提交/commit/推送/push
- **MUST 调用 skill**：`ci-gate`

## ci-pipeline-design（SDLC: ci，priority: high）
- **触发词**：写流水线/加 CI/加 CD/GitHub Actions
- **MUST 调用 skill**：`ci-pipeline-design`

## codebase-audit（SDLC: requirement，priority: high）
- **触发词**：扫描现状/代码审计/项目评估/现状分析
- **MUST 调用 skill**：`codebase-audit`

## coding（SDLC: coding，priority: high）
- **触发词**：按提案/开始编码/写代码/实现
- **MUST 调用 skill**：`coding`

## create-feature（SDLC: support，priority: high）
- **触发词**：新建特性/新增特性/新建子目录/新增子目录
- **MUST 调用 skill**：`create-feature`

## database-design（SDLC: design，priority: high）
- **触发词**：设计表/加字段/写迁移/改表结构
- **MUST 调用 skill**：`database-design`

## debug-issue（SDLC: support，priority: high）
- **触发词**：报错/异常/不工作/有问题
- **MUST 调用 skill**：`debug-issue`

## deployment-verification（SDLC: deployment，priority: high）
- **触发词**：部署/上线/发版/deploy
- **MUST 调用 skill**：`deployment-verification`

## detailed-design（SDLC: design，priority: high）
- **触发词**：详细设计/LLD/类图/接口设计
- **MUST 调用 skill**：`detailed-design`

## docker-compose-design（SDLC: ci，priority: high）
- **触发词**：写 docker-compose/编排服务/编写部署文件/docker compose
- **MUST 调用 skill**：`docker-compose-design`

## dockerfile-writing（SDLC: ci，priority: high）
- **触发词**：写 Dockerfile/Docker 化/容器化/写 dockerfile
- **MUST 调用 skill**：`dockerfile-writing`

## expert-review（SDLC: review，priority: high）
- **触发词**：评审/看一下/检查/审查
- **MUST 调用 skill**：`expert-review`

## gh-pr-workflow（SDLC: ci，priority: high）
- **触发词**：提 PR/创建 PR/请求评审/合并 PR
- **MUST 调用 skill**：`gh-pr-workflow`

## gh-release（SDLC: deployment，priority: high）
- **触发词**：打 tag/发 Release/发布版本/GitHub Release
- **MUST 调用 skill**：`gh-release`

## git-commit（SDLC: coding，priority: high）
- **触发词**：commit/提交/提交代码/总结变更
- **MUST 调用 skill**：`git-commit`

## git-workflow-decision（SDLC: support，priority: high）
- **触发词**：开始新任务/创建分支/新建功能/拉分支
- **MUST 调用 skill**：`git-workflow-decision`

## high-level-design（SDLC: design，priority: high）
- **触发词**：概要设计/HLD/架构设计/系统设计
- **MUST 调用 skill**：`high-level-design`

## integration-testing（SDLC: testing，priority: high）
- **触发词**：集成测试/IT/跨模块测试/Testcontainers
- **MUST 调用 skill**：`integration-testing`

## k8s-deployment（SDLC: deployment，priority: high）
- **触发词**：K8s/k8s 部署/编写 manifest/Deployment
- **MUST 调用 skill**：`k8s-deployment`

## k8s-verification（SDLC: deployment，priority: high）
- **触发词**：验证 K8s/K8s 状态/K8s 健康检查/检查部署
- **MUST 调用 skill**：`k8s-verification`

## legacy-onboarding（SDLC: requirement，priority: high）
- **触发词**：接入老项目/老项目改造/项目迁移/规范接入
- **MUST 调用 skill**：`legacy-onboarding`

## maven-publish（SDLC: deployment，priority: high）
- **触发词**：发布 Maven/发 maven/maven deploy/Maven Central
- **MUST 调用 skill**：`maven-publish`

## migration-planning（SDLC: requirement，priority: high）
- **触发词**：制定迁移计划/规划迁移/迁移策略/migration planning
- **MUST 调用 skill**：`migration-planning`

## model-design（SDLC: design，priority: high）
- **触发词**：设计模型/建表/设计实体/加字段
- **MUST 调用 skill**：`model-design`

## module-decomposition（SDLC: design，priority: high）
- **触发词**：拆分模块/微服务划分/DDD 设计/模块划分
- **MUST 调用 skill**：`module-decomposition`

## npm-publish（SDLC: deployment，priority: high）
- **触发词**：发布 npm/发 npm/npm publish/npm 发布
- **MUST 调用 skill**：`npm-publish`

## requirement-analysis（SDLC: requirement，priority: high）
- **触发词**：需求/新需求/功能/新功能
- **MUST 调用 skill**：`requirement-analysis`

## review-fix-loop（SDLC: review，priority: high）
- **触发词**：修复评审问题/处理 review/修复 MUST fix/复评
- **MUST 调用 skill**：`review-fix-loop`

## scaffold-project（SDLC: requirement，priority: high）
- **触发词**：初始化项目/新建项目/搭建项目/创建工程
- **MUST 调用 skill**：`scaffold-project`

## unit-testing（SDLC: testing，priority: high）
- **触发词**：写测试/补测试/跑测试/单测
- **MUST 调用 skill**：`unit-testing`

## iac-terraform（SDLC: support，priority: low）
- **触发词**：Terraform/IaC/基础设施即代码/云资源编排
- **MUST 调用 skill**：`iac-terraform`

## sandbox-usage（SDLC: support，priority: low）
- **触发词**：沙箱/e2b/agentsphere/opensandbox
- **MUST 调用 skill**：`sandbox-usage`

## api-documentation（SDLC: support，priority: medium）
- **触发词**：生成 API 文档/Swagger 文档/OpenAPI 文档/API 文档
- **MUST 调用 skill**：`api-documentation`

## changelog-generation（SDLC: support，priority: medium）
- **触发词**：生成 changelog/写变更日志/补 changelog/changelog
- **MUST 调用 skill**：`changelog-generation`

## database-migration-cd（SDLC: deployment，priority: medium）
- **触发词**：数据库迁移/Flyway/数据库变更/数据库 CD
- **MUST 调用 skill**：`database-migration-cd`

## docker-cli（SDLC: support，priority: medium）
- **触发词**：docker/docker 命令/docker 构建/docker 运行
- **MUST 调用 skill**：`docker-cli`

## e2e-testing（SDLC: testing，priority: medium）
- **触发词**：E2E 测试/端到端测试/Playwright/Cypress
- **MUST 调用 skill**：`e2e-testing`

## helm-ops（SDLC: support，priority: medium）
- **触发词**：helm/helm 安装/helm 升级/helm 回滚
- **MUST 调用 skill**：`helm-ops`

## jenkins-pipeline（SDLC: ci，priority: medium）
- **触发词**：Jenkins/Jenkinsfile/Jenkins 流水线/Jenkins 构建
- **MUST 调用 skill**：`jenkins-pipeline`

## kubectl-ops（SDLC: support，priority: medium）
- **触发词**：kubectl/k8s/k8s 操作/查看 pod
- **MUST 调用 skill**：`kubectl-ops`

## log-analysis（SDLC: support，priority: medium）
- **触发词**：分析日志/查日志/日志排查/log analysis
- **MUST 调用 skill**：`log-analysis`

## monitoring-setup（SDLC: deployment，priority: medium）
- **触发词**：配置监控/接入 Prometheus/配置告警/Grafana
- **MUST 调用 skill**：`monitoring-setup`

## performance-testing（SDLC: testing，priority: medium）
- **触发词**：性能测试/压力测试/负载测试/JMeter
- **MUST 调用 skill**：`performance-testing`

## performance-tuning（SDLC: support，priority: medium）
- **触发词**：性能调优/性能优化/接口太慢/系统太慢
- **MUST 调用 skill**：`performance-tuning`

## retro-document（SDLC: requirement，priority: medium）
- **触发词**：反向生成文档/补架构图/补 ADR/retro document
- **MUST 调用 skill**：`retro-document`

## security-audit（SDLC: review，priority: medium）
- **触发词**：安全审计/安全扫描/安全检查/security audit
- **MUST 调用 skill**：`security-audit`

## yunxiao-pipeline（SDLC: ci，priority: medium）
- **触发词**：云效/阿里云效/云效流水线/yunxiao
- **MUST 调用 skill**：`yunxiao-pipeline`

## api-design（role: developer，priority: high）
- **触发词**：设计 API/新建接口/Feign
- **遵守规则**：`common-api-design` 或 `<stack>-developer`

## cache-design（role: developer，priority: high）
- **触发词**：缓存/Redis/分布式锁
- **遵守规则**：`common-cache-design` 或 `<stack>-developer`

## database-design（role: developer，priority: high）
- **触发词**：设计表/写迁移/MyBatis
- **遵守规则**：`common-database-design` 或 `<stack>-developer`

## error-handling（role: common，priority: high）
- **触发词**：异常处理/错误码/抛异常
- **遵守规则**：`common-error-handling` 或 `<stack>-common`

## event-driven（role: developer，priority: high）
- **触发词**：发消息/事件驱动/Event
- **遵守规则**：`common-event-driven` 或 `<stack>-developer`

## git（role: common，priority: high）
- **触发词**：commit/提交/push
- **遵守规则**：`common-git` 或 `<stack>-common`

## legacy-tolerance（role: common，priority: high）
- **触发词**：老代码/遗留代码/legacy
- **遵守规则**：`common-legacy-tolerance` 或 `<stack>-common`

## model-design（role: developer，priority: high）
- **触发词**：新建实体/设计模型/Entity
- **遵守规则**：`common-model-design` 或 `<stack>-developer`

## multi-tenant（role: developer，priority: high）
- **触发词**：多租户/tenant/TenantContext
- **遵守规则**：`common-multi-tenant` 或 `<stack>-developer`

## naming（role: common，priority: high）
- **触发词**：命名/起名/变量
- **遵守规则**：`common-naming` 或 `<stack>-common`

## project-structure（role: common，priority: high）
- **触发词**：开始工作/任何任务/初始化
- **遵守规则**：`common-project-structure` 或 `<stack>-common`

## security（role: common，priority: high）
- **触发词**：认证/授权/JWT
- **遵守规则**：`common-security` 或 `<stack>-common`

## security（role: developer，priority: high）
- **触发词**：认证/授权/JWT
- **遵守规则**：`common-security` 或 `<stack>-developer`

## api-design（role: common，priority: medium）
- **触发词**：设计 API/新建接口/RESTful
- **遵守规则**：`common-api-design` 或 `<stack>-common`

## architecture（role: architect，priority: medium）
- **触发词**：设计/架构/拆服务
- **遵守规则**：`common-architecture` 或 `<stack>-architect`

## architecture（role: developer，priority: medium）
- **触发词**：写代码/新增/实现
- **遵守规则**：`common-architecture` 或 `<stack>-developer`

## cache-design（role: common，priority: medium）
- **触发词**：缓存/cache/redis
- **遵守规则**：`common-cache-design` 或 `<stack>-common`

## code-review（role: reviewer，priority: medium）
- **触发词**：评审/审查/检查
- **遵守规则**：`common-code-review` 或 `<stack>-reviewer`

## concurrency（role: common，priority: medium）
- **触发词**：并发/线程池/异步
- **遵守规则**：`common-concurrency` 或 `<stack>-common`

## database-design（role: common，priority: medium）
- **触发词**：设计表/加字段/写迁移
- **遵守规则**：`common-database-design` 或 `<stack>-common`

## documentation（role: common，priority: medium）
- **触发词**：文档/README/注释
- **遵守规则**：`common-documentation` 或 `<stack>-common`

## logging（role: common，priority: medium）
- **触发词**：写日志/加日志/日志规范
- **遵守规则**：`common-logging` 或 `<stack>-common`

## messaging（role: common，priority: medium）
- **触发词**：发消息/写 MQ/消息队列
- **遵守规则**：`common-messaging` 或 `<stack>-common`

## model-design（role: common，priority: medium）
- **触发词**：新建实体/设计模型/建表
- **遵守规则**：`common-model-design` 或 `<stack>-common`

## performance（role: common，priority: medium）
- **触发词**：性能优化/慢查询/N+1
- **遵守规则**：`common-performance` 或 `<stack>-common`

## project-structure（role: common，priority: medium）
- **触发词**：项目结构/目录结构/新建项目
- **遵守规则**：`common-project-structure` 或 `<stack>-common`

## testing（role: common，priority: medium）
- **触发词**：写测试/跑测试/测试覆盖率
- **遵守规则**：`common-testing` 或 `<stack>-common`

## testing（role: tester，priority: medium）
- **触发词**：测试/写测试/跑测试
- **遵守规则**：`common-testing` 或 `<stack>-tester`

## transaction（role: common，priority: medium）
- **触发词**：事务/Transactional/事务传播
- **遵守规则**：`common-transaction` 或 `<stack>-common`

## version-management（role: common，priority: medium）
- **触发词**：版本/version/tag
- **遵守规则**：`common-version-management` 或 `<stack>-common`

## 未列出场景

如果上述路由表没有覆盖你的场景：

1. 先 `Glob wiki/**/*.md` 找到相关规范文档
2. 再 `Glob changes/proposals/*/` 看是否有进行中的变更
3. 仍不确定时 **MUST 问用户**，不要自作主张

## 关键约束（MUST 遵守）

- **任何编码动作 MUST 先有变更提案**（`changes/proposals/<id>/proposal.md`）
- **任何提交动作 MUST 走 `ci-gate` 技能**，禁止裸 `git commit`
- **任何部署动作 MUST 走 `deployment-verification` 技能**，禁止直接操作生产
- **生产环境操作 MUST 用户确认**（部署、回滚、删除等）
- **任何工作开始前 MUST 先识别项目栈**（见上方"第 0 步"）
