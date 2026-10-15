---
name: dwf-orchestrator
description: "Use when 用户要启动、继续、恢复或重启 DWF 开发工作流，或需要编排 .dwf/state.json、specs 队列、阶段推进、迭代新增/拆分/插队、待确认事项、state.json 重建。只要存在 .dwf/state.json 或用户要求按 DWF/开发工作流步骤推进，必须使用本技能。若用户只是单独要求生成需求文档、设计稿、需求分析、技术方案、实现清单或编码，且没有工作流状态/队列编排诉求，优先使用对应 dwf-xxx 子技能。触发短语包括开始项目、继续 dev-workflow、恢复工作流、重新开始、插队、拆分迭代、推进下一阶段。"
---

# dwf-orchestrator

本技能是 DWF（Dev Workflow）开发工作流的统一调度入口。它只负责读取状态、判断阶段、分派子技能、维护状态机骨架，不生成阶段文档正文，不修改项目代码。

与旧的 `dev-workflow` 一体化技能不同，本技能把流程编排和阶段实现解耦：编排层只持有状态机与路由表，阶段产出由 `dwf-requirement`、`dwf-design`、`dwf-development`、`dwf-coding` 完成。

## 加载资源

先读本文件，再按动作读取引用文件：

- 写入、修复或解释 `.dwf/state.json`、`_meta.json`、`_context.md`、`.dwf/pending/<迭代目录名>/state.json`、spec 目录骨架前，读取 `references/state-model.md`。
- 执行首次初始化、阶段推进、拆分迭代、迭代完成、新增迭代、暂停插队、重新开始、待确认事项处理、递延提醒、恢复或 `state.json` 重建前，读取 `references/orchestration-flows.md`。
- 分派到子技能时，读取并遵守对应子技能的 `SKILL.md`。子技能只处理当前阶段内容，队列结构仍由本技能控制。

<HARD-GATE>

以下规则不可违反：

1. **只编排，不实现。** 不生成 `01-需求/`、`02-设计稿/`、`03-需求分析/`、`04-技术方案/`、`05-实现清单/` 的正文内容，不修改工作区根目录下的项目代码。阶段实现必须分派给子技能。唯一例外：处理待确认事项时，可把用户的明确决策回写到对应阶段文档的“待确认项/待确认事项/待解决问题”段。
2. **每次调用先读 `state.json`。** 在分派、初始化或任何动作之前，先读取 `.dwf/state.json`（如存在），识别 `specs` 队列、`active` spec 与每项 `current_step`。`state.json` 与 `_meta.json` 分歧时以 `state.json` 为准并修正 `_meta.json`。
3. **禁止未经确认的自动推进。** 阶段文档整体确认和阶段间推进都必须有显式用户确认。若用户没有明确说“确认/通过/没问题/采用/继续推进该阶段”等等价表达，本技能必须先用 `question` 询问“是否确认当前阶段文档整体通过”；未确认前不得写 `confirmed_stages`、不得推进 `current_step`。每次推进同步更新对应 spec 的 `_meta.json` 与顶层 `updated_at`。
4. **禁止跳过阶段。** 用户说“直接写代码”“只是小 bug”不是跳过流程的理由。正确做法是分派到对应阶段，或走新增迭代、极简迭代、暂停与优先插入流程。
5. **队列变更由本技能统一控制。** spec 入队、出队、`active`/`pending`/`paused`/`done` 切换、拆分兄弟 spec、优先插入，都必须经 `question` 确认后写入 `state.json`，并同步 `_meta.json`。
6. **状态只写 `_meta.json`，不重命名 spec 目录。** 不要把 `done`、`paused` 等状态前缀加到 spec 目录名上。
7. **重新开始必须二次确认并限制删除范围。** 默认只删除 `.dwf/`。如确需删除根目录项目代码，必须先生成逐项待删清单，排除 `skills/`、`.git/`、agent 配置、文档、脚本和其它仓库维护文件，再用 `question` 让用户逐项确认；二次确认前不得删除任何文件。
8. **全程使用中文。** 除非用户明确要求其他语言，交互、`question` 选项、状态摘要、编排说明均使用中文。代码、路径、技术名词可保留英文。
9. **待确认事项由本技能统一发起。** 阶段文档中“待确认项/待确认事项/待解决问题”的逐项确认、已确认事项回写、未确认事项记录到 `.dwf/pending/<迭代目录名>/state.json`、激活 spec 前的递延提醒，全部由本技能处理；子技能不解析该段、不写待确认状态、不发起逐项 `question`。
10. **待确认事项扫描不可跳过。** 每次处理阶段推进时，即使用户已经说“继续”或“文档没问题”，也必须先读取刚确认的阶段文档并扫描待确认段。存在可解析条目时必须逐项处理；存在待确认段但不可解析时必须用 `question` 让用户选择“跳过解析推进”或“需要修改文档重整该段”。未完成本扫描前不得写 `confirmed_stages`、不得推进 `current_step`。
11. **一次触发只执行一个编排动作。** 每次触发最多完成以下一种动作：初始化并分派当前阶段、分派当前 active spec 的当前阶段、处理一次阶段推进、处理一次队列变更、处理一次恢复或重建。允许的复合动作只有：首次初始化后分派 `requirements`；新增/插队 spec 经确认后激活并分派其第一个阶段；恢复经确认后激活并分派当前阶段。不得在同一次响应中连续执行多个阶段。
12. **阶段推进后必须停下。** 子技能完成、阶段文档整体确认且待确认事项处理完后，本技能只能把 `current_step` 推进到 `affected_stages` 中的下一个阶段并同步状态，然后向用户说明下一阶段等待继续；不得自动调用下一阶段子技能。
13. **禁止批量生成阶段产物。** 本技能和被分派的子技能在工作流模式下不得一次性生成或确认 `requirements`、`design`、`breakdown`、`plans`、`todos`、`code` 中的多个阶段产物。

</HARD-GATE>

## 状态摘要

`.dwf/state.json` 是工作流权威来源。顶层维护有序 `specs` 队列和 `completed_specs` 历史；每个 spec 目录内的 `_meta.json` 是镜像。完整字段、示例 JSON、目录结构和台账 schema 见 `references/state-model.md`。

spec 队列状态：

| 状态 | 含义 |
|---|---|
| `pending` | 排队等待执行 |
| `active` | 当前正在执行，同一时刻最多一个 |
| `paused` | 被高优先级 spec 中断，保留进度待恢复 |
| `done` | 已完成，从 `specs` 移入 `completed_specs` |

阶段与分派目标：

| `current_step` | 阶段 | 子技能 |
|---|---|---|
| `requirements` | 需求文档待确认 | `dwf-requirement` |
| `design` | 设计稿待确认 | `dwf-design` |
| `breakdown` | 需求分析待确认 | `dwf-development` |
| `plans` | 技术方案待选择 | `dwf-development` |
| `todos` | 实现清单待确认 | `dwf-development` |
| `code` | 编码执行中或待收尾 | `dwf-coding` |

默认阶段顺序：`requirements → design → breakdown → plans → todos → code`。实际推进以当前 spec 的 `affected_stages` 为准。

## 每次触发流程

1. 读取 `.dwf/state.json`。
2. 若不存在：
   - 若 `.dwf/specs/` 也不存在，走首次初始化。
   - 若 `.dwf/specs/` 仍在，按 `references/orchestration-flows.md` 的 `state.json` 缺失重建流程恢复。
3. 若 `specs` 为空：项目处于稳定态。用户提出新变更时走新增迭代。
4. 若有 `active` spec：按其 `current_step` 分派子技能；若用户提出紧急变更，走暂停与优先插入。
5. 若无 `active` 但有 `paused` 或 `pending`：先按递延项提醒流程处理 `.dwf/pending/` 中的未确认状态，再用 `question` 让用户选择恢复 `paused` 或激活首个 `pending`。
6. 若 `active.current_step == "code"` 且实现清单全部完成并验证通过，走迭代完成。

分派子技能后，本次 orchestrator 编排动作结束。当前回合交由该子技能完成当前阶段；后续阶段必须等待用户再次确认或下一次触发后，重新读取 `state.json` 再分派。

## 分派规则

分派时把子技能视为工作流模式执行者：它读取 `state.json` 与当前 `active` spec 目录，生成或确认当前阶段内容。本技能只指定目标 spec、阶段与上下文，不替子技能写正文。

兄弟 spec（`shared_ref` 非空）执行 `breakdown`、`plans`、`todos` 时，子技能应把 `shared_ref` 指向的初始化 spec 中 `01-需求/`、`02-设计稿/` 作为只读上下文，不重新生成项目级需求和设计稿。

## 阶段推进

子技能完成当前阶段后，本技能只有在阶段文档整体已被用户显式确认时才能推进状态：

1. 判断用户输入或 `question` 结果是否已经明确确认当前阶段文档整体通过；没有则先用 `question` 请求确认，未确认时停下，不写任何阶段状态。
2. 读取刚确认的阶段文档，检查是否存在非空“待确认项/待确认事项/待解决问题”段；存在则由本技能进入待确认事项逐项确认循环。
3. 待确认事项处理完后，将当前阶段加入 `confirmed_stages`。
4. 按 `affected_stages` 中的顺序把 `current_step` 推进到下一阶段。
5. 同步更新 `state.json` 中的 spec 项、对应 `_meta.json`、顶层 `updated_at`。
6. 停止本次编排，向用户说明下一阶段已就绪；等待用户下一次继续或确认后再分派下一阶段。

特殊规则：

- 跳过设计稿时，把 `design_skipped` 设为 `true`，从 `affected_stages` 移除 `design`，并直接进入下一个受影响阶段。
- `plans` 阶段必须由 `dwf-development` 给出至少两个方案，并通过 `question` 让用户选择，选定值写入 `selected_plan`。
- 初始化 spec 的 `breakdown` 确认后，若需求覆盖多个页面或复杂模块，必须用 `question` 询问是否拆分兄弟 spec。
- 推进到 `code` 并完成编码验证后，进入迭代完成流程。

## 队列操作

执行以下操作前必须读取 `references/orchestration-flows.md` 的对应章节：

- **首次初始化**：创建 `.dwf/`、`.dwf/specs/`、首个 `{date}-{seq}-feat-项目初始化` spec 骨架、初始 `state.json` 与 `_meta.json`，然后分派 `dwf-requirement`。不创建空待确认状态；首次出现未确认事项时再创建 `.dwf/pending/<迭代目录名>/state.json`。
- **拆分迭代**：只在初始化 spec 的 `breakdown` 已确认且用户同意后执行。兄弟 spec 写 `shared_ref` 与 `_context.md`，入队为 `pending`，执行顺序经 `question` 确认。
- **迭代完成**：将 active spec 标为 `done`，同步 `_meta.json`，从 `specs` 移入 `completed_specs`，递增 `iteration_count`，再决定是否激活下一个 spec。
- **新增迭代**：项目稳定或编码阶段收到新变更时，确认 spec 名、`affected_stages`、目录骨架与队列位置。
- **暂停与优先插入**：紧急需求中断当前 active 前，必须用 `question` 确认；原 spec 改为 `paused`，新 spec 插到队列头并设为 `active`。
- **重新开始**：必须完成二次风险确认后才可删除 `.dwf/`；根目录项目代码只有在用户逐项确认待删清单后才可删除，再回到首次初始化。

## 待确认事项

阶段推进前，本技能必须读取刚确认阶段文档并解析标题 `## 待确认项`、`## 待确认事项` 或 `## 待解决问题`，列表项匹配 `^-\s+`。逐项用 `question` 让用户选择“已解决，给出答案”“跳过，留待后续迭代”“已在文档中直接修改”。这一步不能因为用户说“继续”或“文档没问题”而省略。

处理规则：

- 用户已确认或已在文档中修改：把用户决策回写到对应阶段文档的待确认段，不写入 `.dwf/pending/`。
- 用户跳过或未确认：写入 `.dwf/pending/<迭代目录名>/state.json` 中对应阶段数组。每个文件含 `requirements`、`design`、`breakdown`、`plans`、`todos` 五个数组字段。
- 任意 spec 即将转为 `active` 前，先扫描 `.dwf/pending/*/state.json` 中的未确认项；若存在，用 `question` 提醒用户选择逐项处理、全部继续递延或只处理来自本 spec 的项。完整状态结构和流程见两个引用文件。

## 恢复

会话中断后再次触发本技能时，不重新初始化。读取 `state.json` 后：

- 有 `active`：按其 `current_step` 分派对应子技能。
- 无 `active` 但有 `paused`：用 `question` 让用户选择恢复哪个。
- 只有 `pending`：激活首个 `pending` 前先处理递延项提醒。
- 队列为空：项目稳定，等待新变更。

每次恢复写回前，把当前 spec 的 `_meta.json` 与 `state.json.specs` 对齐。

## 完成前检查

结束前确认：

- 已先读取 `.dwf/state.json`，并识别当前队列状态。
- 没有生成阶段文档正文或项目代码。
- 所有阶段推进、队列变更、拆分、插队、重新开始均经 `question` 确认。
- `state.json`、对应 `_meta.json`、顶层 `updated_at` 已同步。
- spec 目录没有被重命名为带状态前缀。
- 待确认事项回写、`.dwf/pending/` 未确认状态与递延提醒已按规则处理。
- 与用户的交互和 `question` 内容均为中文。
