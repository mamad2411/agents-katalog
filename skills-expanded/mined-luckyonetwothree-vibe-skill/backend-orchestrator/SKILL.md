---
name: backend-orchestrator
description: 当需要完成后端从设计到代码实现的全流程时使用。后端全流程指挥官，协调"先全量设计、再统一实现"的两阶段流程：设计阶段按架构→数据→API顺序产出设计规范，经统一设计审查后，实现阶段按数据→API→架构顺序生成可运行代码。关键词：后端全流程、后端开发、后端设计+实现、后端整体方案。
metadata:
  module: "后端架构与开发"
  sub-module: "全流程编排"
  type: "orchestrator"
  version: "5.0"
  domain_tags: ["电商", "SaaS", "金融", "通用"]
  trigger_examples:
    - "完成后端开发全流程"
    - "从设计到代码一步到位"
    - "后端整体方案设计和实现"
    - "后端从零开始搭建"
---

# 后端全流程指挥官

## Code Write Boundary

Follow [Engineering Boundary Protocol](../../templates/engineering-boundary-protocol.md) or the equivalent relative path from this skill.

1. Scan first: identify framework, package manager, module layout, ORM, migration tool, validation library, auth middleware, and test conventions before implementation.
2. Target scope: declare exact files/directories to create or modify; generated code must stay inside the target module unless integration files are explicitly required.
3. No overwrite: preserve existing business logic, routes, models, migrations, configs, and tests unless the user explicitly asks for replacement.
4. Consistency checks: verify OpenAPI, controller/service signatures, DTO/schema validation, ER model, migrations, repositories, and auth rules are aligned.
5. Migration safety: generated migrations must be additive by default; destructive data changes require explicit human confirmation.
6. Implementation report: list created/modified files, skipped files, checks run, failed checks, and residual risks.

## 核心原则

架构约束先行，数据驱动契约，设计审查闭环，实现步步可编译。

1. **架构约束先行**：架构决策从根本上影响数据模型和API设计，必须最先确定
2. **数据驱动契约**：API契约基于已确认的数据模型设计，字段定义有据可依
3. **先全量设计再统一实现**：设计阶段只产出文档，三份设计交叉验证后统一审查，避免设计冲突导致代码返工
4. **实现步步可编译**：实现阶段按数据→API→架构顺序，每步产出都可独立编译运行

## 执行步骤

1. **设计阶段串行**：架构→数据→API，后一步消费前一步产出
2. **统一设计审查**：编排器读取三份设计产出执行交叉验证，确保一致性后人类统一确认
3. **实现阶段串行**：数据→API→架构，每步可编译
4. **最终验证**：项目可启动，健康检查通过

## 编排协议

遵循 [orchestrator-protocol.md](../../../templates/orchestrator-protocol.md)。协议正文不再内联；阶段顺序、依赖和卡口以运行时定义为准。

### 执行方式（强制）

1. `node scripts/orchestrate.js next backend-orchestrator` 获取可执行阶段
2. 按返回的 `skills` 执行子 Skill，产物写入阶段定义路径
3. `node scripts/orchestrate.js gate backend-orchestrator --stage <id>` 执行阶段卡口
4. 人类决策阶段：`node scripts/orchestrate.js approve backend-orchestrator --stage <id> --by <name>`
5. 全部阶段通过后：`node scripts/orchestrate.js finalize backend-orchestrator`

### Pipeline 定义

机器可读定义（唯一权威）：[runtime/pipelines/backend-orchestrator.json](../../../runtime/pipelines/backend-orchestrator.json)

```yaml
pipeline: backend-orchestrator
post_pipeline:
  - action: stage-summary
    output: output/phase-reports/backend/backend-orchestrator.md
```

阶段顺序：架构设计 → 数据架构设计 → API 设计 → 统一设计审查 → 数据层实现 → API 层实现 → 架构层实现 → 阶段总结。卡口规则由 `runtime/pipelines/backend-orchestrator.json` 的 `gate.checks` 执行，包含文件存在性、JSON Schema 实例校验与人类审批。

## 阶段执行计划

### 阶段A：全量设计

#### A1：架构设计 → 调用 backend-architecture-spec

```
Skill: backend-architecture-spec
输入:
  PRD: output/pm-design/design-prd/prd.md
  PRD结构化数据: output/pm-design/design-prd/prd.json
  业务规模: 用户提供
  技术约束: 用户提供（可选）
输出: output/backend-architecture/backend-architecture-spec/
关键产出:
  - architecture_decision.json — 架构方案+拓扑图
  - service_design.json — 服务划分+限界上下文
  - service_data_ownership.json — 服务数据归属（供data-architecture-spec消费）
  - tech_stack_decision.json — 技术栈决策（供所有impl Skill统一消费）
  - adr.json — 架构决策记录
  - review_report.json — 审查问题清单
  - tech_debt_register.json — 技术债登记册
验证: 输出文件已生成且非空
模式: 🤖→👤
```

⏸ **架构设计审查卡口**

#### A2：数据架构设计 → 调用 data-architecture-spec

```
Skill: data-architecture-spec
输入:
  PRD: output/pm-design/design-prd/prd.md
  PRD结构化数据: output/pm-design/design-prd/prd.json
  架构方案: output/backend-architecture/backend-architecture-spec/architecture_decision.json
  服务数据归属: output/backend-architecture/backend-architecture-spec/service_data_ownership.json
  技术栈决策: output/backend-architecture/backend-architecture-spec/tech_stack_decision.json
  数据量预估: 用户提供（可选）
  并发量预估: 用户提供（可选）
  当前Schema: 用户提供（可选）
输出: output/backend-data-architecture/data-architecture-spec/
关键产出:
  - data_dictionary.json — 业务数据字典
  - er_model.json — ER模型+DDL+索引策略
  - cache_strategy.json — 缓存方案
  - migration_plan.json — 迁移方案（增量项目）
验证: 输出文件已生成且非空
模式: 🤖→👤
```

⏸ **数据架构设计审查卡口**

#### A3：API设计 → 调用 api-design-spec

```
Skill: api-design-spec
输入:
  PRD: output/pm-design/design-prd/prd.md
  PRD结构化数据: output/pm-design/design-prd/prd.json
  数据模型: output/backend-data-architecture/data-architecture-spec/er_model.json
  业务数据字典: output/backend-data-architecture/data-architecture-spec/data_dictionary.json（可选）
  架构方案: output/backend-architecture/backend-architecture-spec/architecture_decision.json
  服务设计: output/backend-architecture/backend-architecture-spec/service_design.json
  技术栈决策: output/backend-architecture/backend-architecture-spec/tech_stack_decision.json（可选）
  业务流程: output/pm-design/design-userflow/userflow.json（可选）
  安全等级: 用户提供
  合规要求: 用户提供（可选）
  多租户需求: 用户提供（可选）
  前端页面数据需求: output/ui-frontend/page-builder/pages.json（可选）
输出: output/backend-api-design/api-design-spec/
关键产出:
  - openapi.yaml — OpenAPI 3.0规范
  - security-policy.json — 安全策略
  - auth-scheme.json — 认证鉴权方案
  - compliance-checklist.json — 合规检查清单
  - api-coverage.json — PRD/前端对齐覆盖报告
验证: 输出文件已生成且非空
模式: 🤖→👤
```

#### A4：统一设计审查 → 编排器执行交叉验证

三份设计产出完成后，编排器读取三份产出执行跨子Skill交叉验证：

```
动作: 统一设计审查（编排器协调职责）
输入:
  架构方案: output/backend-architecture/backend-architecture-spec/architecture_decision.json
  服务设计: output/backend-architecture/backend-architecture-spec/service_design.json
  技术栈决策: output/backend-architecture/backend-architecture-spec/tech_stack_decision.json
  ER模型: output/backend-data-architecture/data-architecture-spec/er_model.json
  缓存策略: output/backend-data-architecture/data-architecture-spec/cache_strategy.json
  OpenAPI规范: output/backend-api-design/api-design-spec/openapi.yaml
输出: output/backend-design-review/review-report.json
验证规则:
  - API资源↔ER模型对齐：每个API资源有对应ER模型实体，API字段100%有Model字段支撑
  - API分组↔服务边界一致：API按限界上下文分组，与服务设计一致
  - 技术栈一致性：三个设计产出引用的技术栈统一
  - 缓存策略↔API访问模式对齐：高频API有对应缓存策略
  - 数据归属↔API归属一致：API资源归属的服务与数据归属的服务一致
验证: 交叉验证全部通过 + 人类统一确认
模式: 🤖→👤
```

⏸ **统一设计审查卡口**：交叉验证全部通过 + 人类统一确认 → 不一致项修正后重新审查

### 阶段B：统一实现

#### B1：数据层实现 → 调用 data-architecture-impl

```
Skill: data-architecture-impl
输入:
  ER模型: output/backend-data-architecture/data-architecture-spec/er_model.json
  缓存策略: output/backend-data-architecture/data-architecture-spec/cache_strategy.json
  迁移方案: output/backend-data-architecture/data-architecture-spec/migration_plan.json（可选）
  API契约: output/backend-api-design/api-design-spec/openapi.yaml（可选，用于API对齐检查）
  技术栈决策: output/backend-architecture/backend-architecture-spec/tech_stack_decision.json
  project_dir: 用户提供
输出: 代码写入 {project_dir}/src/ + 元数据 output/backend-data-architecture/data-architecture-impl/
验证: 输出文件已生成且非空
模式: 🤖→👤
```

#### B2：API层实现 → 调用 api-design-impl

```
Skill: api-design-impl
输入:
  OpenAPI规范: output/backend-api-design/api-design-spec/openapi.yaml
  安全策略: output/backend-api-design/api-design-spec/security-policy.json
  认证鉴权方案: output/backend-api-design/api-design-spec/auth-scheme.json
  合规检查清单: output/backend-api-design/api-design-spec/compliance-checklist.json（可选）
  PRD: output/pm-design/design-prd/prd.md
  PRD结构化数据: output/pm-design/design-prd/prd.json
  数据模型: output/backend-data-architecture/data-architecture-spec/er_model.json
  数据层实现报告: output/backend-data-architecture/data-architecture-impl/impl-report.json
  前端页面数据需求: output/ui-frontend/page-builder/pages.json（可选）
  技术栈决策: output/backend-architecture/backend-architecture-spec/tech_stack_decision.json
  project_dir: 用户提供
输出: 代码写入 {project_dir}/src/ + 元数据 output/backend-api-design/api-design-impl/
验证: 输出文件已生成且非空
模式: 🤖→👤
```

#### B3：架构层实现 → 调用 backend-architecture-impl

```
Skill: backend-architecture-impl
输入:
  架构方案: output/backend-architecture/backend-architecture-spec/architecture_decision.json
  服务设计: output/backend-architecture/backend-architecture-spec/service_design.json
  ADR: output/backend-architecture/backend-architecture-spec/adr.json
  审查报告: output/backend-architecture/backend-architecture-spec/review_report.json（可选）
  技术债登记册: output/backend-architecture/backend-architecture-spec/tech_debt_register.json（可选）
  API契约: output/backend-api-design/api-design-spec/openapi.yaml
  数据模型: output/backend-data-architecture/data-architecture-spec/er_model.json
  缓存策略: output/backend-data-architecture/data-architecture-spec/cache_strategy.json（可选）
  技术栈决策: output/backend-architecture/backend-architecture-spec/tech_stack_decision.json
  project_dir: 用户提供
输出: 代码写入 {project_dir}/ + 元数据 output/backend-architecture/backend-architecture-impl/
验证: 输出文件已生成且非空
模式: 🤖→👤
```

### 阶段总结（post_pipeline）

所有子Skill执行完成后，必须生成阶段总结文档，写入 `output/phase-reports/backend/backend-orchestrator.md`，包含以下6项结构（均不可为空）：

1. **执行概览**：编排器名称与版本、执行时间、子Skill执行状态（成功/失败/降级）
2. **关键发现**：每个子Skill的核心输出摘要（1-3条）、跨子Skill的交叉洞察
3. **决策记录**：人类决策点及决策结果、AI自动决策及依据
4. **产出清单**：所有输出文件路径及内容摘要、产出质量评估（是否通过验证）
5. **风险与待办**：未通过验证的项、降级执行的项、建议后续跟进的事项
6. **下游衔接**：本编排器产出可被哪些下游编排器消费、推荐的下一步编排器

| 参数 | 值 |
|------|-----|
| 子Skill输出路径 | output/backend-architecture/ + output/backend-data-architecture/ + output/backend-api-design/ + output/backend-design-review/ |
| 总结输出路径 | output/phase-reports/backend/backend-orchestrator.md |
| 审批记录路径 | output/approvals/{orchestrator-name}/{stage-id}.approval.json |

下游衔接:
  primary: release-orchestrator（后端全流程完成后，进入质量验收和发布流程）
  alternatives:
    - target: ui-orchestrator
      reason: 后端就绪后启动UI前端开发与集成
      condition: 前端尚未开发+需要后端API支撑时
  special_cases:
    - target: api-design-spec
      reason: 仅需补充API设计，无需完整后端流程
      condition: 架构和数据层已就绪，仅需API设计时，无需完整编排流

## 阶段卡口

| 卡口 | 条件 | 未通过处理 |
|------|------|------------|
| 架构设计完成 | backend-architecture-spec输出文件已生成且非空 + 人类审查通过 | 缺失项必须补充 |
| 数据架构设计完成 | data-architecture-spec输出文件已生成且非空 + 人类审查通过 | 缺失项必须补充 |
| API设计完成 | api-design-spec输出文件已生成且非空 + 人类审查通过 | 缺失项必须补充 |
| 统一设计审查通过 | 交叉验证全部通过 + 人类统一确认 | 不一致项修正后重新审查 |
| 数据层实现完成 | data-architecture-impl输出文件已生成且非空 + 人类确认通过 | 缺失项补充后重新验证 |
| API层实现完成 | api-design-impl输出文件已生成且非空 + 人类确认通过 | 缺失项补充后重新验证 |
| 架构层实现完成 | backend-architecture-impl输出文件已生成且非空 + 人类确认通过 | 缺失项补充后重新验证 |
| 阶段总结已生成 | output/phase-reports/backend/backend-orchestrator.md 已生成且6项结构均非空 | 补充缺失结构项后重新生成 |

## 人类决策点

| 决策点 | 触发条件 | 决策内容 |
|--------|----------|----------|
| 架构模式选择 | backend-architecture-spec执行时 | 单体/微服务/Serverless，人类最终确认 |
| 服务拆分粒度 | backend-architecture-spec执行时 | 拆分过细增加复杂度，拆分过粗失去灵活性 |
| 技术栈确认 | backend-architecture-spec执行时 | 确认统一技术栈决策，影响后续所有实现 |
| 范式vs反范式 | data-architecture-spec执行时 | 读写比决定，人类确认平衡点 |
| 缓存一致性级别 | data-architecture-spec执行时 | 强一致vs最终一致，人类确认 |
| API风格选择 | api-design-spec执行时 | RESTful vs GraphQL，人类确认 |
| 安全等级确认 | api-design-spec执行时 | 标准vs高安全，影响限流/加密/审计策略 |
| 统一设计审查确认 | 三份设计完成后 | 审查三份设计的一致性，确认后才进入实现 |
| 数据迁移执行确认 | data-architecture-impl输出完成 | 迁移方案和回滚脚本生成完成，人类确认是否执行迁移 |
| 架构就绪确认 | backend-architecture-impl审查通过后 | 代码实现完成，人类确认架构可进入开发 |

## 异常处理

| 异常类型 | 处理策略 |
|----------|----------|
| 架构模式争议 | 提供单体+微服务双方案对比，人类决策 |
| 服务循环依赖 | 自动检测并告警，必须消除后才能进入审查 |
| 数据模型与API冲突 | 统一设计审查阶段解决，以数据模型为准调整API |
| 设计审查不通过 | 根据人类修改意见调整设计，重新审查 |
| 代码自审P0问题 | 自动修复后重新自审，无法修复则阻塞输出 |
| 阶段总结生成失败 | 基于已完成的子Skill输出生成部分总结，缺失项标注"数据缺失"，不阻塞编排完成 |
