---
name: ui-orchestrator
description: 当需要UI设计与前端开发时使用。UI设计与前端开发编排器，按需调度核心Skill与ext Skill完成从项目初始化到生产就绪的全流程。关键词：UI设计、前端开发、UI、前端、界面开发、做UI、写前端、出界面、搭页面、设计系统+前端代码。
metadata:
  module: "UI设计与前端开发"
  sub-module: "UI总指挥"
  type: "orchestrator"
  version: "7.3"
  domain_tags: ["互联网", "通用"]
  trigger_examples:
    - "做UI"
    - "写前端"
    - "出界面"
    - "搭页面"
    - "设计系统加前端代码一起做"
    - "从设计到前端全流程"
  interaction_mode: "ai_suggest_human_approve"
---

# UI设计与前端开发编排器

## 核心原则

按需执行——只运行项目需要的步骤，不执行不需要的阶段。核心阶段与ext增强阶段交替执行，ext Skill调用由编排器统一调度而非内嵌在Pipeline Skill内部。

## 执行模式

编排器支持四种执行模式，通过 `mode` 参数选择：

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `express` | 选择一个 ext Skill 直接读取 PRD 生成页面代码，最小质量检查 | 单页面/落地页/快速原型/概念验证 |
| `prototype` | 只出原型，不生成前端代码 | 需求验证阶段、多方案对比、交互逻辑对齐 |
| `full` | 完整输出前端代码，跳过探索 | 需求已确认、设计方向明确、直接进入实施 |
| `progressive` | 渐进式——先探索验证，确认后自动进入完整交付 | 大多数场景，特别是需求尚未完全验证时 |

**模式选择建议**：
- 单页面/快速出结果 → 用 `express`
- 只想快速看原型 → 用 `prototype`
- 需求和设计都已确认 → 用 `full`
- 不确定选哪个 → 用 `progressive`（默认）

### express 模式 Pipeline

```
stage-e: 生成锚点 → 设计方向快选(2-3套) → 结构化prompt → ext Skill生成 → 增强质量检查 → 输出
```

**设计引擎选择**：express 模式通过 `express_engine` 参数选择设计引擎（4选1），不同引擎有不同的设计风格和能力侧重：

| 设计引擎 | ext Skill | 风格侧重 | 适用场景 | 推荐外部工具（可选） |
|----------|-----------|---------|---------|-------------------|
| `visual`（默认） | ext-frontend-design | 视觉差异化，避免AI同质化，大胆创意 | 品牌站/落地页/创意展示 | v0.dev / Bolt / Lovable |
| `ux` | ext-ui-ux-pro-max | UX最佳实践，数据驱动推荐，行业标准 | SaaS/管理后台/电商 | v0.dev / Cursor |
| `polish` | ext-impeccable | 质量打磨，细节优化，生产级品质 | 需要高完成度的页面 | Google Stitch / Cursor |
| `motion` | ext-interaction-design | 交互动效，微交互，动态体验 | 交互密集型应用/游戏化界面 | Framer / Rive |

**选择建议**：
- 想要好看且独特 → `visual`（默认）
- 想要好用且规范 → `ux`
- 想要精致且完善 → `polish`
- 想要动感且有趣 → `motion`

**prompt 来源模式**（通过 `express_prompt_source` 参数选择）：

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `auto`（默认） | 编排器生成2-3套设计方向供用户快选，基于选中方向生成结构化prompt，传给选定的 ext Skill | 快速出结果，想要设计方向选择权 |
| `manual` | 用户自行前往推荐的外部工具官网，获取/编写 prompt，填入 `express_prompt` 参数 | 想要更精细控制设计效果 |

**manual 模式使用流程**：
1. 用户选择 `express_engine`（如 `visual`）
2. 用户选择 `express_prompt_source=manual`
3. 编排器提示用户前往推荐的外部工具官网（如 v0.dev）
4. 用户在外部工具中输入需求，获取/编写 prompt
5. 用户将 prompt 内容填入 `express_prompt` 参数
6. 编排器将 `express_prompt` 直接传给选定的 ext Skill，跳过自动 prompt 生成

**express 模式取舍**：
- ✅ 获得：极快速度、最少流程、直接出可运行代码
- ❌ 放弃：设计系统一致性、令牌驱动架构、组件库集成、质量债务追踪、PM↔UI反馈闭环

**express 模式最小质量检查**（5项，v7.2升级）：
1. WCAG AA 对比度达标
2. 无硬编码密钥/token
3. 页面可运行（npm run dev 启动成功）
4. visual_bans 合规（无 AI 同质化模式）
5. 设计锚点一致性（色彩/排版方向校验）

**轻量设计锚点**（v7.2 新增）：
express 模式虽跳过完整设计系统建立，但在 ext Skill 调用前生成轻量设计锚点（express_design_anchor），包含 register、color_direction、typography_direction、layout_direction、visual_bans，确保 ext Skill 产出有设计方向约束而非完全随机。锚点根据 express_engine 自动调整侧重（visual→非蓝紫非card-grid，ux→功能型排版+大方留白，polish→完整anti-patterns，motion→动效友好布局）。

**设计方向快选**（v7.3 新增）：
auto 模式下，锚点生成后编排器生成 2-3 套差异化设计方向描述（每套约100-200字，含色温/布局/排版/张力差异），用户快速选择后回写锚点。用户也可跳过快选直接使用默认方向（`express_skip_scheme=true`）。与 full 模式的"设计探索→人类选择"形成对应，express 版本更轻量（方向描述而非完整视觉方向）。

**结构化 Prompt**（v7.3 新增）：
原 auto 模式的 prompt 是简单拼接（PRD + 品牌规范 + 锚点），v7.3 升级为结构化 prompt——基于用户选中的设计方向 + PRD + 锚点，生成包含具体色值/字体名/布局模式/禁忌列表/功能需求的精确 prompt，替代模糊描述。manual 模式下用户 prompt 末尾自动附加锚点设计约束。

**express 模式输出**：
- 页面代码直接写入 {project_dir}/src/
- 无 output/ 元数据（无 design_brief、无 quality_debt、无 design_feedback）
- 无下游 Skill 衔接（如需 API 集成或生产就绪，需切换到 full 模式重新执行）

> 📄 详细执行计划见 [stages/stage-e.md](stages/stage-e.md)

### prototype 模式 Pipeline

```
stage-1 → stage-p
project-init → prototype-output
  核心           原型输出
```

仅执行设计系统建立和PM约束审查，输出视觉方向+约束审查结果，不生成页面代码。

**prototype 模式取舍**：
- ✅ 获得：快速验证设计方向、低成本多方案对比、交互逻辑对齐
- ❌ 放弃：页面代码、ext 增强、质量审计、API 集成、生产就绪

**prototype 模式输出**：
- 原型报告（prototype-report.md）：视觉方向概要 + 关键页面布局描述 + 组件选型摘要
- 设计系统产出（project-init.json）：视觉方向 + 设计令牌 + 组件库
- 无页面代码、无 design_brief、无 quality_debt

**与 full 模式的衔接**：prototype 完成后确认视觉方向，切换到 full 模式时从 stage-2 开始（跳过 stage-1，复用已有 project-init 产出）。

> 📄 详细执行计划见 [stages/stage-p.md](stages/stage-p.md)

### full 模式 Pipeline

```
stage-1 → stage-2 → stage-3 → stage-4 → [stage-5] → [stage-6]
```

跳过探索阶段，直接从设计系统建立开始完整交付。PM约束审查内建为 stage-1 的条件分支。

### progressive 模式 Pipeline（默认）

```
stage-1 → stage-2 → stage-3 → stage-4 → [stage-5] → [stage-6]
设计系统    增强      页面构建   增强+审计   按需        按需
```

先自由探索设计方案（内建在 stage-1 条件分支），人类确认后自动进入完整交付流程。

## 执行流程（full 模式 / progressive 模式）

```
stage-1        stage-2          stage-3        stage-4              stage-5      stage-6
project-init → ext-enhance → page-builder → ext-enhance+audit → [api-int] → [prod-ready]
  核心          增强             核心          增强+审计            按需         按需
```

| 阶段 | 名称 | Skill | 必选/按需 | 跳过条件 | 详细计划 |
|------|------|-------|---------|---------|---------|
| stage-1 | 设计系统建立 | project-init | 必选 | — | [stages/stage-1.md](stages/stage-1.md) |
| stage-2 | 设计增强+简报生成 | ext-ui-ux-pro-max, ext-impeccable, ext-frontend-design | 必选 | — | [stages/stage-2.md](stages/stage-2.md) |
| stage-3 | 页面与组件构建 | page-builder | 必选 | — | [stages/stage-3.md](stages/stage-3.md) |
| stage-4 | 页面增强+质量审计 | ext-ui-ux-pro-max, ext-impeccable, ext-interaction-design | 必选 | — | [stages/stage-4.md](stages/stage-4.md) |
| stage-5 | API集成 | api-integration | 按需 | 无后端 / 静态数据 | [stages/stage-5.md](stages/stage-5.md) |
| stage-6 | 生产就绪+优化 | production-ready, ext-impeccable | 按需 | 无需构建部署 | [stages/stage-6.md](stages/stage-6.md) |

**阶段合并说明**（v7.0 相比 v6.0 的精简）：
- Stage 0/0.5（设计探索/约束对齐）→ 合并为 stage-1 的条件分支（mode=progressive 时执行）
- Stage 1.5（PM约束审查）→ 合并为 stage-1 的条件分支（有PM输入时执行）
- Stage 4 的 ext-frontend-design 调用 → 移除（stage-2 已调用，产出通过 design_brief.json 消费）
- Stage 5（质量审计）→ 合并到 stage-4（增强+审计一体化）
- Stage 7+8（生产就绪+生产优化）→ 合并为 stage-6

## 编排协议

遵循 [orchestrator-protocol.md](../../../templates/orchestrator-protocol.md)。协议正文不再内联；阶段顺序、依赖和卡口以运行时定义为准。

### 执行方式（强制）

1. `node scripts/orchestrate.js init ui-orchestrator --mode <express|prototype|full|progressive>` 初始化执行模式
2. `node scripts/orchestrate.js next ui-orchestrator` 获取当前模式下的可执行阶段
3. 按返回的 `skills` 执行子 Skill，产物写入阶段定义路径
4. `node scripts/orchestrate.js gate ui-orchestrator --stage <id>` 执行阶段卡口
5. 人类决策阶段：`node scripts/orchestrate.js approve ui-orchestrator --stage <id> --by <name>`
6. 全部阶段通过后：`node scripts/orchestrate.js finalize ui-orchestrator`

### 断点续执行

执行状态由运行时写入 `output/.runtime/ui-orchestrator/state.json`。中断后再次执行 `next` 即可从第一个可执行阶段恢复；无需手工维护检查点文件。阶段失败会保留在 state 中，重试时 `next` 会返回 `resumed: true`。

## Pipeline

机器可读定义（唯一权威）：[runtime/pipelines/ui-orchestrator.json](../../../runtime/pipelines/ui-orchestrator.json)

```yaml
pipeline: ui-orchestrator
post_pipeline:
  - action: stage-summary
    output: output/phase-reports/ui/ui-orchestrator.md
```

| 模式 | 阶段 | 跳过条件 |
|------|------|---------|
| `express` | stage-e | 仅快速生成，不进入完整流程 |
| `prototype` | stage-1 → stage-p | 只出原型，不生成页面代码 |
| `full` / `progressive` | stage-1 → stage-2 → stage-3 → stage-4 → [stage-5] → [stage-6] | stage-5/6 按需跳过 |

各阶段的详细执行计划见 `stages/stage-*.md`；卡口规则由 JSON 定义中的 `gate.checks` 执行。

## 阶段执行计划

### 项目信息收集

| 输入项 | 来源 | 必选 |
|--------|------|------|
| mode | 用户提供（默认progressive） | 否 |
| express_engine | 用户提供（默认visual，仅mode=express时生效） | 否 |
| express_prompt_source | 用户提供（默认auto，仅mode=express时生效） | 否 |
| express_prompt | 用户提供（仅express_prompt_source=manual时必填） | 否 |
| express_skip_scheme | 用户提供（默认false，仅mode=express且express_prompt_source=auto时生效，跳过设计方向快选） | 否 |
| 品牌规范 | 用户提供 / output/pm-strategy/positioning-strategy/positioning-strategy.json | 是 |
| 产品定位 | output/pm-strategy/positioning-strategy/positioning-strategy.json | 否 |
| 目标平台 | 用户提供 | 是 |
| 目标语言 | 用户提供（默认zh-CN） | 是 |
| project_name | 用户提供 | 是 |
| project_dir | 用户提供 | 是 |
| framework | 用户提供（React/Vue/Svelte/Next.js/Nuxt.js） | 是 |
| 组件库偏好 | 用户提供 | 否 |
| 后端集成需求 | 用户提供（有/无） | 是 |
| 部署需求 | 用户提供（有/无） | 是 |

输出: 项目信息汇总 + 阶段执行计划（根据 mode 确定哪些阶段执行/跳过）
⏸ 人类确认项目信息、执行模式和执行计划

### 各阶段详细计划

| 阶段 | 详细计划文件 | 核心输入 | 核心输出 |
|------|------------|---------|---------|
| Stage-E | [stages/stage-e.md](stages/stage-e.md) | PRD+品牌规范+express_engine | 可运行项目 |
| Stage-P | [stages/stage-p.md](stages/stage-p.md) | visual_direction+tokens | prototype-report.md |
| Stage 1 | [stages/stage-1.md](stages/stage-1.md) | 品牌规范+PRD | project-init.json+PRODUCT.md+DESIGN.md |
| Stage 2 | [stages/stage-2.md](stages/stage-2.md) | visual_direction+tokens | design_brief.json+page_manifest.json+回写后的project-init.json |
| Stage 3 | [stages/stage-3.md](stages/stage-3.md) | design_brief+page_manifest | pages.json+页面代码+design_feedback.json+quality_debt.json |
| Stage 4 | [stages/stage-4.md](stages/stage-4.md) | 页面代码+design_brief.json+visual_review_result | 增强后代码+quality_score+quality_debt.json更新 |
| Stage 5 | [stages/stage-5.md](stages/stage-5.md) | API契约+pages.json | api-integration.json+请求层代码 |
| Stage 6 | [stages/stage-6.md](stages/stage-6.md) | 前端代码+quality_debt | 构建产物+测试+优化 |

### Schema 定义

| Schema | 文件 | 用途 |
|--------|------|------|
| checkpoint | [schemas/checkpoint.json](schemas/checkpoint.json) | 断点续执行检查点 |
| constraint-review | [schemas/constraint-review.json](schemas/constraint-review.json) | PM约束审查结果（Stage 1 条件分支B） |
| design-brief | [schemas/design-brief.json](schemas/design-brief.json) | 可执行设计规范（Stage 2 → Stage 3） |
| page-manifest | [schemas/page-manifest.json](schemas/page-manifest.json) | 页面清单（防止页面遗漏） |
| prototype-report | [schemas/prototype-report.json](schemas/prototype-report.json) | 原型报告（prototype模式输出） |
| quality-debt | [schemas/quality-debt.json](schemas/quality-debt.json) | 质量债务追踪 |

### 阶段总结（post_pipeline）

所有子Skill执行完成后，必须生成阶段总结文档，写入 `output/phase-reports/ui/ui-orchestrator.md`，包含以下6项结构（均不可为空）：

1. **执行概览**：编排器名称与版本、执行时间、子Skill执行状态（成功/失败/降级）
2. **关键发现**：每个子Skill的核心输出摘要（1-3条）、跨子Skill的交叉洞察
3. **决策记录**：人类决策点及决策结果、AI自动决策及依据
4. **产出清单**：所有输出文件路径及内容摘要、产出质量评估（是否通过验证）
5. **风险与待办**：未通过验证的项、降级执行的项、建议后续跟进的事项
6. **下游衔接**：本编排器产出可被哪些下游编排器消费、推荐的下一步编排器

| 参数 | 值 |
|------|-----|
| 子Skill输出路径 | output/ui-frontend/ |
| 总结输出路径 | output/phase-reports/ui/ui-orchestrator.md |
| 审批记录路径 | output/approvals/{orchestrator-name}/{stage-id}.approval.json |
| ext增强记录 | 本轮执行中的ext Skill调用结果摘要 |

下游衔接:
  primary: release-orchestrator（UI开发完成后，进入质量验收和发布流程）
  alternatives:
    - target: api-integration
      reason: 后端API已就绪，需要前后端联调集成
      condition: 有后端API但尚未集成时
    - target: monitoring-orchestrator
      reason: UI上线后建立前端性能和用户体验监控
      condition: 前端已部署需要持续监控时

## 阶段卡口

编排器的阶段卡口只校验以下3类条件，不深入子Skill内部字段：

| 卡口类型 | 校验内容 | 示例 |
|----------|----------|------|
| 输出存在性 | 输出文件已生成且非空 | "api-design-spec输出文件已生成" |
| 顶层结构完整性 | JSON顶层必填字段存在 | "prd.json包含features/pages/entities" |
| 人类决策确认 | 关键决策点已获人类确认 | "设计审查人类确认通过" |

| 卡口 | 条件 | 未通过处理 |
|------|------|------------|
| 阶段总结已生成 | output/phase-reports/ui/ui-orchestrator.md 已生成且6项结构均非空 | 补充缺失结构项后重新生成 |
| stage-e/1 完成 | 项目初始化+约束审查产出完整 | 修复后重试 |
| stage-2 完成 | design_brief.json + 回写验证通过 | 回写验证失败按异常处理 |
| stage-3 完成 | pages.json 生成 + 视觉审查完成 | P0问题必须修复 |
| stage-4 完成 | quality_debt.json 更新 + quality_score≥75 | 修复后重新审计 |
| stage-6 完成 | production_ready.json 生成 | 修复后重试 |

## 人类决策点

| 决策点 | 触发条件 | 决策内容 |
|--------|----------|----------|
| 执行模式确认 | 项目信息收集完成时 | 确认执行模式（express/prototype/full/progressive） |
| 设计方向快选 | stage-e，express_prompt_source=auto且express_skip_scheme=false | 从2-3套设计方向中选择1套或融合多套 |
| 页面清单完整性确认 | stage-3，无PM输入时 | 确认页面清单是否完整覆盖所有需求页面 |
| 探索方案选择 | stage-1条件分支A后，mode=progressive | 选择探索方案或融合多个方案 |
| 约束对齐确认 | stage-1条件分支A续后，mode=progressive | 确认约束对齐结果和设计决策 |
| 视觉方向确认 | stage-1后，stage-2前 | 确认核心视觉方向和品牌色 |
| PM约束审查确认 | stage-1条件分支B后，critical级别finding存在时 | 确认约束审查中的critical发现 |
| 设计系统增强确认 | stage-2后，stage-3前 | 确认ext增强结果；回写验证V5发现visual_direction语义矛盾时确认处理方式 |
| 页面方案确认 | stage-3后，stage-4前 | 确认页面布局和组件 |
| 视觉审查确认 | stage-3后，stage-4前，强制视觉审查完成时 | 确认视觉审查结果，低分维度决定是否回退stage-2 |
| PM反馈确认 | stage-3后，design_feedback.json存在时 | 确认是否接受UI→PM的反馈建议 |
| 质量审计确认 | stage-4后，quality_score<75或偏科时 | 确认是否放行 |
| 发布决策 | stage-6后 | 确认是否发布 |

## 异常处理

**质量债务追踪**：所有降级、标注"待修复"、"待确认"的问题统一写入 `output/ui-frontend/page-builder/quality_debt.json`，确保降级问题不被遗忘。

**quality_debt.json Schema**：见 [schemas/quality-debt.json](schemas/quality-debt.json)

**债务管理规则**：
- 每个降级/标注项产生一条 debt_item
- stage-6（生产就绪+优化）执行前汇总检查 quality_debt.json
- critical severity 的 open 债务 → 🛑 阻断执行，必须修复后才能继续
- high severity 的 open 债务 → ⏸ 人类确认是否继续
- medium severity 的 open 债务 → 标注在阶段总结中
- low severity 的 open 债务 → 记录但不阻塞

| 异常类型 | 处理策略 | 债务记录 |
|----------|----------|----------|
| 项目信息不足 | 提示用户补充，必选项缺失不可继续 | — |
| stage-e 失败 | 修复致命问题后重试，3次后建议切换到 full 模式 | — |
| stage-e manual模式用户无法获取prompt | 提供两个选项：①切换auto模式（含设计方向快选）②切换full模式 | — |
| stage-1 失败 | 修复后重试，不可跳过 | — |
| stage-1 visual_direction一致性校验矛盾 | 阻断级(❌)：必须修复后重试；警告级(⚠️)：标注+⏸人类确认 | 警告级→medium |
| stage-2 核心增强失败 | ext-frontend-design/ext-ui-ux-pro-max失败→阻断stage-3；colorize/typeset失败→标注不阻断 | colorize/typeset失败→medium |
| stage-2 回写验证失败 | V1(JSON解析)→回滚使用原始令牌；V2(WCAG)→调整色值；V3(tokens不同步)→以json为准重新生成css；V4(硬编码)→移除替换；V5(语义矛盾)→⏸人类确认 | V1-V4自动修复→low |
| stage-3 P0问题 | 必须修复，不可跳过 | — |
| stage-3 视觉审查平均分≤2.5 | ⏸ 人类决定：回退stage-2重新生成design_brief，或继续进入stage-4增强修复 | 继续进入stage-4→high |
| stage-4 quality_score<75 | 修复后重新audit+critique，最多3次闭环，3次后⏸人类确认 | 3次后仍不达标→high |
| stage-4 单项偏科(audit<60或critique<55) | 标注"偏科风险"，⏸人类确认 | medium |
| stage-4 ext-impeccable未部署 | 使用内建自评分数，gate门槛降为60 | medium |
| stage-5 api-integration 失败 | 标注"待重试"，不阻塞stage-6 | medium |
| stage-6 构建失败 | 修复后重试 | — |
| stage-6 ext调用失败 | 标注待优化项，不阻塞 | low |
| 阶段总结生成失败 | 基于已完成的输出生成部分总结 |
