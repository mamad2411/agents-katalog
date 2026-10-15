---
name: prdkit-prd-create
description: 当用户提出写 PRD、起 PRD、生成需求文档、整理产品方案、补产品文档、输出高/中/低复杂度需求文档时使用。该 skill 采用两阶段流程：第一阶段检查 prdkit 项目状态、扫描上下文、完成产品定型与复杂度判断、通过结构化提问补齐信息，并将方案稿写入 draft/reference/<title>-prd-plan.md；第二阶段仅在用户确认方案稿后，调用 prdkit prd create --from-plan 生成 workspace/prds 下的正式 PRD 初稿，再按复杂度和产品类型补齐正式内容。
allowed-tools:
  - Read
  - Grep
  - Glob
  - LS
  - AskQuestion
  - Bash(command -v prdkit)
  - Bash(prdkit info*)
  - Bash(prdkit init*)
  - Bash(prdkit prd create*)
  - Bash(prdkit prd list*)
  - Edit
  - MultiEdit
  - Write
---

# 创建复杂度感知 PRD

## 目标

为 `prdkit` 项目生成一套“先方案、后正式稿”的 PRD 工作流：

1. 第一阶段只写 `draft/reference/<title>-prd-plan.md`
2. 第二阶段在用户确认后，才写 `workspace/prds/<title>-prd.md`
3. 正式 PRD 既受复杂度等级影响，也受产品类型影响

## 渐进加载原则

不要预读全部参考资料。按阶段加载：

1. 阶段 0 只加载：
   - [references/framework/complexity-assessment.md](references/framework/complexity-assessment.md)
   - [references/appendices/product-typing.md](references/appendices/product-typing.md)
2. 阶段 1 写方案稿时补充：
   - [references/question-bank.md](references/question-bank.md)
   - [references/plan-template.md](references/plan-template.md)
   - [references/chapters/chapter-generation.md](references/chapters/chapter-generation.md)
3. 阶段 2 写正式稿时补充：
   - [references/final-prd-sections.md](references/final-prd-sections.md)
   - [references/appendices/selfcheck.md](references/appendices/selfcheck.md)

## 工作流程

### 阶段 0：项目检查、产品定型、复杂度判断

1. 从项目根目录开始，先检查 `prdkit` 和项目状态：
   - `command -v prdkit`
   - `prdkit info`
2. 如果缺少 `prdkit` 命令，先安装 CLI；如果当前目录不是 `prdkit` 项目，先完成 `prdkit init`。
3. 在提问前先扫描上下文：
   - `context/`
   - `draft/`
   - `workspace/prds/`
   - `workspace/discussions/`
4. 结合 [references/appendices/product-typing.md](references/appendices/product-typing.md) 先推断产品定型：
   - 商业属性：商业化产品 / 企业自研系统
   - 功能类型：业务型管理软件 / 工具型软件 / 交易型平台 / 基础服务型
5. 用一句话向用户确认产品定型：
   - `根据目前上下文，我先按【企业自研系统 × 业务型管理软件】理解，后续会据此调整 PRD 章节侧重点。`
6. 再结合 [references/framework/complexity-assessment.md](references/framework/complexity-assessment.md) 做复杂度判断：
   - 先用一句话从用户视角描述变更
   - 再走 L1-L4 决策树
   - 边界模糊时用辅助信号消歧
7. 向用户确认复杂度等级：
   - `根据描述，这是一个 L3（模块级）需求，我会按标准 PRD 体量组织方案稿。`

### 阶段 1：生成 PRD 方案稿

8. 使用 [references/question-bank.md](references/question-bank.md) 提 3-4 个高信息密度问题，优先补齐：
   - 背景和业务问题
   - 角色与关键场景
   - 范围边界
   - 数据、依赖、风险、验收
9. 结合 [references/chapters/chapter-generation.md](references/chapters/chapter-generation.md) 决定章节适配策略：
   - 低复杂度保留核心章节
   - 高复杂度增加流程、依赖、权限、上线与回滚、自检
   - 按产品类型调整内容重心
10. 按 [references/plan-template.md](references/plan-template.md) 生成并保存：
   - `draft/reference/<title>-prd-plan.md`
11. 方案稿里必须写清：
   - 产品定型及原因
   - 复杂度等级及原因
   - 推荐章节与章节策略
   - 已确认信息
   - 当前假设
   - 待确认 / 开放问题
   - 第二阶段执行命令
12. 第一阶段结束后必须停止，等待用户确认。

### 阶段 2：生成正式 PRD

13. 只有在用户明确确认方案稿后，才能进入第二阶段。
14. 执行：

```bash
prdkit prd create "<title>" --from-plan ./draft/reference/<title>-prd-plan.md
```

15. 根据复杂度等级和产品类型补齐 `workspace/prds/` 下正式 PRD：
   - L1/L2：保持轻量，但必须完整覆盖背景、目标、范围、需求、风险、验收
   - L3/L4：必须完整覆盖角色、流程、依赖、风险、验收、里程碑
   - 商业化产品：补充商业目标、市场/客户视角
   - 企业自研系统：补充 ROI、效率、内部推广与采纳视角
   - 交易型 / 业务型：补充流程、状态、角色权限
   - 基础服务型：补充 API、调用链路、隔离和稳定性
16. 对 L3/L4，正式输出前必须执行 [references/appendices/selfcheck.md](references/appendices/selfcheck.md) 中的高复杂度自检：
   - 边界条件是否清楚
   - 外部依赖是否清楚
   - 异常流是否清楚
   - 验收标准是否可执行
   - 文末是否附待完善清单
17. 完成后向用户说明正式文档路径，以及后续可继续拆原型、补标记、推进评审。

## 输出约束

- 任何 PRD 生成默认先写方案稿，再写正式稿
- 方案稿路径固定为 `draft/reference/<title>-prd-plan.md`
- 正式 PRD 路径固定为 `workspace/prds/`
- 不要跳过产品定型
- 不要跳过复杂度判断
- 不要在用户未确认方案稿前直接写正式 PRD
