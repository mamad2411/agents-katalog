---
name: product-iteration-orchestrator
description: 当需要对已有产品进行功能迭代时使用。产品迭代总指挥，根据需求变更影响范围协调PM/UI/Backend子编排器的增量更新和集成交付。关键词：功能迭代、需求变更、增量更新、跨领域、产品优化、加功能、改需求、产品升级、系统升级、功能优化、新增模块、需求调整、版本迭代、功能改进、迭代开发。
metadata:
  module: "跨领域协调"
  sub-module: "产品迭代"
  type: "orchestrator"
  version: "10.0"
  domain_tags: ["通用"]
  trigger_examples:
    - "给现有产品加一个支付功能"
    - "需求改了，需要调整"
    - "产品要升级，加几个新模块"
    - "优化一下现有的功能"
    - "给系统加个新功能"
    - "需求变更了，重新评估影响"
    - "版本迭代，需要更新几个模块"
---

# 产品迭代总指挥

## 核心原则

**影响分析驱动，条件分支执行，最小变更集交付**

产品迭代与产品启动的核心区别在于：已有产品有存量代码、存量API、存量用户。迭代的关键不是全流程推进，而是精准识别变更影响范围，只执行受影响的领域编排器，避免不必要的全量重做。

## 执行步骤

1. **需求与设计**：调用design-orchestrator完成需求分析和PRD增量更新
2. **变更影响分析**：识别变更影响范围，判断API/UI/后端是否需变更
3. **后端变更**：条件执行backend-orchestrator，保持API/数据/架构统一设计审查
4. **UI变更**：条件执行UI编排器；如有后端变更，则消费backend-orchestrator产出的API契约
5. **集成对齐**：当API与UI均需变更时，校验API变更已同步到前端（类型定义/请求函数/Mock数据）、UI变更所需API端点已覆盖
6. **交付上线**：调用release-orchestrator+monitoring-orchestrator完成质量验收→发布检查→灰度发布→监控建立

## 编排协议

遵循 [orchestrator-protocol.md](../../../templates/orchestrator-protocol.md)。协议正文不再内联；阶段顺序、依赖和卡口以运行时定义为准。

### 执行方式（强制）

1. `node scripts/orchestrate.js next product-iteration-orchestrator` 获取可执行阶段
2. 按返回的 `skills` 执行子 Skill，产物写入阶段定义路径
3. `node scripts/orchestrate.js gate product-iteration-orchestrator --stage <id>` 执行阶段卡口
4. 条件阶段可跳过：`node scripts/orchestrate.js skip product-iteration-orchestrator --stage <id> --reason <text>`
5. 人类决策阶段：`node scripts/orchestrate.js approve product-iteration-orchestrator --stage <id> --by <name>`
6. 全部阶段通过后：`node scripts/orchestrate.js finalize product-iteration-orchestrator`

### Pipeline

机器可读定义（唯一权威）：[runtime/pipelines/product-iteration-orchestrator.json](../../../runtime/pipelines/product-iteration-orchestrator.json)

```yaml
pipeline: product-iteration-orchestrator
post_pipeline:
  - action: stage-summary
    output: output/phase-reports/cross-domain/product-iteration-orchestrator.md
```

阶段顺序：需求与设计 → 变更影响分析 → 后端变更（条件）→ UI 变更（条件）→ 集成对齐（条件）→ 交付上线（条件）。条件阶段使用 `trigger` 标记，由 `skip` 显式跳过并记录原因。

## 阶段执行计划

### 跨领域产物索引

本编排器不要求子Skill把产物写入 `output/cross-domain/{skill-name}/`。所有子Skill仍写入各自领域原生路径；本编排器在 `output/cross-domain/artifact-index.json` 记录阶段、skill、真实输出路径、摘要和验证状态。下方出现的跨领域路径仅表示索引引用，不表示改写子Skill输出目录。

### 阶段1：需求与设计

#### 调用 design-orchestrator

```
Skill: design-orchestrator
输入:
  用户反馈: 迭代用户反馈数据
  业务需求: 业务需求变更
  数据异常: 数据异常指标
输出: output/cross-domain/design-orchestrator/
验证: PRD人类确认通过
模式: 🤖→👤
```

### 阶段2：变更影响分析

#### 调用 change-impact-analysis

```
Skill: change-impact-analysis
输入:
  PRD变更: output/cross-domain/design-orchestrator/
输出: output/cross-domain/product-iteration-orchestrator/impact-report.md
验证: 影响矩阵覆盖所有下游产出
模式: 🤖
```

### 阶段3：后端变更（条件执行）

#### 调用 backend-orchestrator

```
Skill: backend-orchestrator
输入:
  PRD变更: artifact-index.json → design-orchestrator → output/pm-design/design-prd/
  change-impact: artifact-index.json → change-impact-analysis
  project_dir: 用户提供（已有项目目录路径）
输出: output/backend-architecture/ + output/backend-data-architecture/ + output/backend-api-design/ + output/backend-design-review/
验证: 后端统一设计审查通过 + 变更兼容性已确认 + 实现审查通过
模式: 🤖→👤
```

### 阶段5：UI变更（条件执行）

#### 调用 ui-orchestrator

```
Skill: ui-orchestrator
输入:
  mode: full（产品迭代场景，需求变更已由上游design-orchestrator确认，跳过探索阶段）
  PRD变更: artifact-index.json → design-orchestrator → output/pm-design/design-prd/
  API变更输出: artifact-index.json → backend-orchestrator → output/backend-api-design/api-design-spec/openapi.yaml
  目标语言: 用户提供（默认zh-CN）
  project_dir: 用户提供（已有项目目录路径）
输出: output/ui-project-init/ + output/ui-frontend/ + output/ui-frontend-integration/
验证: 前端代码审查通过，前后端联调通过
模式: 🤖→👤
```

### 阶段4：集成对齐（条件执行）

当API与UI均需变更时，编排器读取 `artifact-index.json` 中的后端API变更与前端UI变更产出，执行跨领域对齐检查：

```
动作: API/UI变更对齐检查
输入:
  API变更契约: artifact-index.json → backend-orchestrator → output/backend-api-design/api-design-spec/openapi.yaml
  UI页面数据需求: artifact-index.json → ui-orchestrator → output/ui-frontend/page-builder/pages.json
  变更影响报告: output/cross-domain/product-iteration-orchestrator/impact-report.md
输出: output/cross-domain/integration-alignment.json
验证: API变更已同步到前端（类型定义/请求函数/Mock数据），UI变更所需API端点已覆盖，未对齐项=0
模式: 🤖→👤
```

#### 对齐检查规则

| 检查维度 | 检查项 | 通过标准 |
|----------|--------|----------|
| API→前端同步 | 新增/修改的API端点，前端TypeScript类型定义是否已更新 | 所有变更端点均有对应类型定义 |
| API→前端同步 | 新增/修改的API端点，前端请求函数（API Service层）是否已添加/更新 | 所有变更端点均有对应请求函数 |
| API→前端同步 | 新增/修改的API端点，前端Mock数据是否已同步更新 | Mock数据结构与最新API响应结构一致 |
| 前端→API覆盖 | UI新增页面/组件所需的数据，是否有对应的API端点提供 | 所有UI数据需求均有API端点覆盖 |
| 前端→API覆盖 | UI变更涉及的API调用，是否与最新API契约一致（路径/参数/响应结构） | 无过期的API调用 |
| 废弃项清理 | 已废弃的API端点，前端是否已移除相关调用 | 无前端调用指向已废弃端点 |
| 废弃项清理 | 已移除的前端页面/组件，后端是否仍存在仅被其调用的冗余API | 无冗余API端点 |

#### 门禁标准

- **未对齐项 = 0**：上述所有检查项全部通过
- 对齐检查结果写入 `integration-alignment.json`，包含：已对齐项列表、未对齐项列表（含差异描述和建议修复方向）、整体对齐率
- 未对齐项不为0时，根据差异描述回退到对应编排器修复：API侧缺失→回退backend-orchestrator，前端侧缺失→回退ui-orchestrator

### 阶段6：交付上线

#### 调用 release-orchestrator

```
Skill: release-orchestrator
输入:
  变更部分输出: output/cross-domain/
  集成输出: output/cross-domain/ui-orchestrator/
输出: output/cross-domain/release-orchestrator/
验证: P0问题=0，灰度发布通过
模式: 🤖→👤
```

#### 调用 monitoring-orchestrator

```
Skill: monitoring-orchestrator
输入:
  发布产物: output/cross-domain/release-orchestrator/
  指标体系: output/cross-domain/metrics-orchestrator/（可选）
输出: output/cross-domain/monitoring-orchestrator/
验证: 监控预警体系已建立
模式: 🤖→👤
```

### 附加调度（按需触发）

| 触发事件 | 调度动作 |
|----------|----------|
| 需要数据支撑决策 | → analysis-orchestrator（在design-orchestrator之前执行） |
| 需要A/B验证 | → experiment-orchestrator（在交付上线之前执行） |
| 需要项目管理支撑 | → agile-orchestrator（贯穿全程） |
| 迭代效果评估 | → analysis-orchestrator（在交付上线之后执行） |

### 阶段总结（post_pipeline）

所有子Skill执行完成后，必须生成阶段总结文档，写入 `output/phase-reports/cross-domain/product-iteration-orchestrator.md`，包含以下6项结构（均不可为空）：

1. **执行概览**：编排器名称与版本、执行时间、子Skill执行状态（成功/失败/降级）
2. **关键发现**：每个子Skill的核心输出摘要（1-3条）、跨子Skill的交叉洞察
3. **决策记录**：人类决策点及决策结果、AI自动决策及依据
4. **产出清单**：所有输出文件路径及内容摘要、产出质量评估（是否通过验证）
5. **风险与待办**：未通过验证的项、降级执行的项、建议后续跟进的事项
6. **下游衔接**：本编排器产出可被哪些下游编排器消费、推荐的下一步编排器

| 参数 | 值 |
|------|-----|
| 子Skill输出路径 | output/cross-domain/ |
| 总结输出路径 | output/phase-reports/cross-domain/product-iteration-orchestrator.md |
| 审批记录路径 | output/approvals/{orchestrator-name}/{stage-id}.approval.json |

下游衔接:
  primary: monitoring-orchestrator（迭代发布后进入持续监控）
  alternatives:
    - target: product-iteration-orchestrator
      reason: 继续下一轮迭代
      condition: 有新的迭代需求时
    - target: growth-orchestrator
      reason: 迭代涉及增长功能
      condition: 迭代包含获客/激活/留存/变现相关功能时
    - target: agile-orchestrator
      reason: 进入下一Sprint规划
      condition: 采用敏捷开发模式时
  special_cases: []

## 阶段卡口

| 卡口 | 条件 | 未通过处理 |
|------|------|------------|
| PRD确认 | PRD人类确认通过 | 补充需求细节 |
| 影响范围确认 | change-impact输出文件已生成且非空 | 补充缺失的下游影响项 |
| API变更确认 | api-design-orchestrator输出文件已生成且非空 | 调整API设计 |
| 后端审查通过 | backend-review输出文件已生成且非空 | 修复P0问题 |
| UI集成验证 | ui-integration输出文件已生成且非空 | 修复集成问题 |
| 集成对齐 | integration-alignment.json已生成且未对齐项=0 | 回退到backend-orchestrator或ui-orchestrator修复对齐差异 |
| 交付上线 | release输出文件已生成且非空 | 修复阻断问题后重新验证 |
| 阶段总结已生成 | output/phase-reports/cross-domain/product-iteration-orchestrator.md 已生成且6项结构均非空 | 补充缺失结构项后重新生成 |

## 人类决策点

| 决策点 | 触发条件 | 决策内容 |
|--------|----------|----------|
| PRD确认 | design-orchestrator完成 | 确认PRD变更可分发到受影响领域 |
| 影响范围确认 | change-impact-analysis完成 | 确认哪些领域需要变更，是否有遗漏 |
| 对齐冲突裁决 | 集成对齐阶段发现API与前端不一致 | 决策API侧改还是前端侧改 |
| 发布决策 | 交付上线阶段完成 | 确认是否发布 |

## 异常处理

| 异常类型 | 处理策略 |
|----------|----------|
| 需求范围蔓延 | 标注超出范围的需求，人类决策是否纳入本期迭代 |
| PRD变更影响未评估领域 | 自动扫描所有领域编排器的输入依赖，补全遗漏的影响 |
| API向后不兼容 | 标注破坏性变更，必须提供兼容方案或版本升级策略 |
| 回归测试失败 | 回退到变更前的代码版本，标注"迭代阻塞" |
| 变更范围超出预期 | 暂停执行，人类决策是否拆分为多期迭代 |
| 纯UI变更但设计令牌需调整 | 由ui-orchestrator统一处理设计令牌更新与前端开发 |
| 纯后端变更但影响已有API | 必须执行api-design-orchestrator评估API兼容性 |
| API变更未同步到前端 | 集成对齐阶段检出未同步项，回退到ui-orchestrator补充类型定义/请求函数/Mock数据 |
| UI变更缺少API端点支撑 | 集成对齐阶段检出未覆盖端点，回退到backend-orchestrator补充API设计 |
| 对齐检查回退多次仍未通过 | 暂停编排，人类裁决冲突方向，标注"对齐阻塞" |
| 阶段总结生成失败 | 基于已完成的子Skill输出生成部分总结，缺失项标注"数据缺失"，不阻塞编排完成 |
