---
name: devops-workflow
description: 单体多模块项目的需求开发全流程编排。状态机驱动，自动调度 discuss、arch-analyzer、team、code-reviewer 等 skill/agent，串联需求讨论到代码审查的 5 个阶段。当用户说 "devops-workflow"、"开发流程"、"需求流程"、"模块开发流程" 时触发。
---

# DevOps Workflow — 单体多模块需求开发全流程编排

## 目录约定

> 修改顶级目录时只改这里，全文及 reference 文件中的路径同步全局替换即可。

- **{讨论根目录}** = `docs/discuss/` — 需求讨论、设计、任务工单的存放根目录

状态机驱动的流程 skill：5 个开发阶段串成统一入口，按 `progress.md` 的当前状态决定下一步调度什么 agent。本文件是**路由器 + 常驻安全规则**；各步骤的执行细节按需读取 `references/`（见末尾索引）。

## 总体流程

```
1 需求讨论 → 2 分析与设计 →[★阶段3 设计审核门]→ 4 开发与逐任务审查 → 5 收尾验收 →[★阶段5 验收确认门]→ COMPLETED
  (start)     (next: analyst+ralph)  (approve)    (next: 逐任务闭环)      (next: verifier)    (approve)
                                                        │
  阶段4 逐任务闭环：⓪复杂度判断（简单/普通/复杂）
    简单（skip_cr=true）：①编码 → ②DoD → DONE
    普通：①编码 → ②DoD → ③CR扫描 →[★CR人工门(+同步design)]→ ⑤改写 → ⑥复验+回写 → DONE
    复杂：[★plan门(+同步design)]→ ①编码 → ②DoD → ③CR扫描 →[★CR人工门(+同步design)]→ ⑤改写 → ⑥复验+回写 → DONE
  ※ 阶段 4/5 发现设计/需求层缺陷 → /devops-workflow rework 按根因层级回退 + 依赖级联重做
```

四道人工门（均由 `/devops-workflow approve` 按状态分发）：**阶段3 设计审核** / **阶段4 复杂任务 plan** / **阶段4 CR 问题裁决** / **阶段5 验收问题裁决**。

## 命令速查

```
/devops-workflow use [需求ID][#里程碑]        # 设定活动上下文，之后裸命令默认作用于它（粘性，推荐）
/devops-workflow start {需求名}              # 创建需求，进入阶段 1 讨论
/devops-workflow next [需求ID]               # 执行下一阶段 / 下一个任务（省略=活动上下文）
/devops-workflow approve [需求ID]            # 确认当前人工门（阶段3设计 / 阶段4 plan / 阶段4 CR）
/devops-workflow status [需求ID]             # 查看进度（省略=活动上下文+高亮；无活动则全部）
/devops-workflow list                        # 列出未完成的需求
/devops-workflow split [需求ID] {里程碑列表}  # 把大需求拆成多个里程碑（仅大需求需要）
/devops-workflow rework [需求ID]             # 设计/实现缺陷返工：按根因层级回退并级联重做
/devops-workflow followup {已完成需求ID} [新需求名]  # 基于已完成需求发起新需求（继承设计上下文）
/devops-workflow summary [需求ID]            # 产出交付清单（DDL / Job·MQ / API）给 DBA 与前端
/devops-workflow fix {bug描述}                # 轻量 bug 修复（定位→编码→CR，不走 5 阶段）
/devops-workflow config                      # 查看/初始化/更新 .workflow-config 配置（缺失项自动补全）
```

- **需求名** = `{YYYY-MM-DD}-{简称}`（如 `2026-09-12-订单取消优化`），**需求 ID** = `{域}/{需求名}`（如 `order/2026-09-12-订单取消优化`），与目录路径 `{讨论根目录}{域}/{需求名}/` 一致
- **`#里程碑`** 仅多里程碑需求需要（如 `payment/2026-09-12-支付渠道重构#alipay`）；未 `split` 的需求是单里程碑，无需 `#`
- 命令的详细处理逻辑见 `references/commands/index.md`

### 强制前置（每个子命令执行前必须做）

1. **Preflight 检查（仅 `start`）**：执行 `start` 时先读 `references/protocols/preflight.md` 逐项检查，blocking 项未通过则终止。其他子命令不执行 preflight
2. **读取** `{讨论根目录}.workflow-active`（`cat` 或 Read）→ 若文件存在且非空，将其内容设为当前活动上下文
3. 若文件不存在且命令需要需求 ID → 走旧回退规则（唯一进行中自动选中；多个列出让选；无则提示 `start`）
4. **禁止跳过此步骤**——不得在未读取该文件的情况下声称"没有活跃的 workflow 流程"

## Agent 权限与职责分离

| 阶段 | 执行方式 | 权限 |
|------|---------|------|
| 2 模块分析 | `arch-analyzer` 或 `analyst` | 只读 |
| 4 任务详细设计（仅复杂任务） | `architect` / `planner` | 只读（只设计不写码）|
| 4 编码 | `executor`（并行 `team`/串行单个，Claude 判断） | 读写 |
| 4 CR 扫描（逐任务） | 单个 `code-reviewer` | 只读（只产清单不改码）|
| 4 改写（逐任务） | 单个 `executor` | 读写（只改已采纳项）|
| 5 收尾验收 | `verifier` | 只读 |

人工门：阶段3 设计审核、阶段4 plan 确认、阶段4 CR 裁决、阶段5 验收问题裁决。

---

## 关键不变量（必须遵守，不随阶段文件加载与否而改变）

1. **子 agent 返回 ≠ 流程推进（防卡死）**：每次子 agent 返回后，主 Agent **必须立刻**：① 读取其产出文件（不以子 agent 的返回文本为准）→ ② 回写 progress.md 对应状态 → ③ 向用户输出结果摘要 + **明确的下一步指令**（该 approve 还是 next）。**绝不允许因为"子 agent 说完了"就静默结束本轮而不给提示。**
2. **审查/验收问题人工门**：code-reviewer 和 verifier 只产出问题清单，**绝不直接改代码**；扫出的问题必须经人工逐条裁决并 `/devops-workflow approve` 后，才由另一个 executor 改写。零问题也要输出提示，不许静默卡住。
3. **编码与审查分两轮**：编码、CR、改写各自独立 agent，CR 与编码不共享上下文，禁止同上下文自审。
4. **进度即时回写（阻塞步骤）**：任务每次状态流转都必须即时写回 progress.md + dev-tasks.md；回写未完成不得推进下一个任务。
5. **设计分两层 + 三级复杂度**：design-consensus = 共识/契约层；复杂任务走任务级 plan/LLD（阶段4 编码前出，人工 approve 后才编码）。简单任务在 `simple_task_skip_cr=true` 时跳过 CR 门（详见 `protocols/automation.md`）。
6. **未决项不许悬空**：design-consensus 的 `待确认/TODO` 必须登记成表并有处置。
7. **设计/需求层缺陷走 rework**：CR 改写只解决"设计对、改当前任务小问题"；牵动设计或多任务用 `/devops-workflow rework`。
8. **人工门只认 `/devops-workflow approve`**：用户的任何其他消息都**不等于** approve，绝不推断审批意图。
9. **design-consensus 同步（防设计漂移）**：阶段 4 中 plan 确认后和 CR 裁决 MODIFIED 后，如果调整了契约，**必须同步回写** design-consensus.md。
10. **rework 必须走返工协议（禁止跳步）**：必须读 `commands/rework.md` → 与用户确认 → 判定根因层级 → 按流程执行。**绝不允许**跳过确认步骤。
11. **所有 agent prompt 必须含 Bash 静态分析约束**：禁止 for/while/if/case/here-doc/嵌套 `$()`。产出物只落项目内 `.task/`，禁止写 home 或仓库外。

---

## references 索引（按需读取，别一次性全载）

| 当你要做 | 先读 |
|---------|------|
| **任何命令执行前（最先）** | `references/protocols/preflight.md` |
| 写/更新 progress.md、初始化任务目录、查状态枚举 | `references/protocols/templates.md` |
| 执行任意 `/devops-workflow` 子命令（路由入口） | `references/commands/index.md` |
| 自动化协议（auto_advance / auto_accept_pass 等） | `references/protocols/automation.md` |
| 任务编号规则、产出物命名、项目约定 | `references/protocols/conventions.md` |
| **阶段执行** | |
| 阶段 1 需求讨论（start + devops-discuss） | `references/stages/stage-1-discuss.md` |
| 阶段 2 分析与设计（analyst/ralph + design-consensus） | `references/stages/stage-2-design.md` |
| 阶段 3 设计审核清单门 | `references/stages/stage-3-review.md` |
| 阶段 4 开发（总则 + 并行判断 + 编码 + 复验回写） | `references/stages/stage-4.0-dev.md` |
| 阶段 4 复杂任务 plan（复杂度判断 + plan 产出 + 同步） | `references/stages/stage-4.1-plan.md` |
| 阶段 4 CR 扫描与裁决（CR + 人工门 + 同步 + 改写） | `references/stages/stage-4.2-cr.md` |
| 阶段 5 收尾验收 + 异常处理 | `references/stages/stage-5-accept.md` |
| **独立命令** | |
| `/devops-workflow fix` 轻量 bug 修复 | `references/commands/fix.md` |
| `/devops-workflow rework` 返工 | `references/commands/rework.md` |
| `/devops-workflow followup` 基于已完成需求发起新需求 | `references/commands/followup.md` |
| `/devops-workflow config` 初始化/合并流程配置 | `references/commands/config.md` |
| `/devops-workflow summary` 产出交付清单（DDL/Job·MQ/API） | `references/commands/summary.md` |

> **执行某阶段/命令前，必须先读对应 reference 文件**再行动——凭记忆执行易漏步、易卡死。
