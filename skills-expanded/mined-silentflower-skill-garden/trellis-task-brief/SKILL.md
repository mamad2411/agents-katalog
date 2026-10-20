---
name: trellis-task-brief
description: "从最新 prd.md、design.md、implement.md 生成、刷新、校验并在对话中展示 Trellis 任务的 brief.md。用于 Phase 1.4 task.py start 前、planning review、用户要求任务 brief/交接摘要，或 in_progress 任务缺失/过期 brief.md 时。"
---

# Trellis 任务交接摘要

为当前任务生成或更新 `brief.md`，并把交接摘要展示在对话里。`brief.md` 是从三件套派生的交接视图，不替代 `prd.md`、`design.md`、`implement.md`。

## Auto-Loop Action 例外

调用来自 auto-loop 时，先通过 `auto_loop.py status` 与 `next` 校验真实 run 和当前 action，不从聊天摘要或 raw runtime JSON 推断授权。只有 schema 2、`profile=commit-only`、run 为 `preparing`，且 `next` 返回本任务的 `refresh_brief` 时，才使用本例外：按下方步骤读取、刷新并完整展示 Brief，然后返回 `trellis-auto-loop` 回写同名 action 并立即 `next`；不等待逐任务人工确认，也不直接执行 `task.py start`。

本例外沿用 runner 的 prepare、Open Questions、readiness 和 artifact 校验，不扩张任务或授权边界。schema 1 返回的 `refresh_brief` 同样在展示后交回 runner，由后续 `confirm_brief` action 等待人工确认。run 已停止、终态、损坏或 action/task 不匹配时不得免确认或代为推进；由 auto-loop owner 处理诊断。普通交互调用继续遵守以下确认规则。

## 核心规则

- 每次运行都重新读取最新 `prd.md`、`design.md if present`、`implement.md if present`。
- 已存在的 `brief.md` 不能作为跳过同步的理由。
- `brief.md` 必须以三件套为准覆盖旧内容；无法从三件套追溯的旧内容不能保留为事实。
- 不要在 `brief.md` 里发明三件套没有表达的新需求。必填字段缺失时写“未明确”，并提示应补充三件套；没有明确技术机制时省略 `Technical Overview`，没有具体风险时省略 `Risks`。
- `Goal` 保持一句话，`Scope` 只写本轮纳入的行为或改动对象；延期事项归入 `Non-Goals`，不另设栏目，也不把范围、方案和验收写成同义复述。
- 首次开工评审或用户明确要求查看全貌时，写回 `brief.md` 后必须展示 brief 正文，不要只给文件路径；首次批准后的同步按下方增量规则展示变化。
- 首次实施批准前必须展示完整 brief。除上方经 runner 校验的 Auto-Loop Action 例外外，默认等待用户确认后再运行 `task.py start`；只有用户明确把当前任务或最终 Brief 与“展示后直接开始 / 不用再次确认 / 视为已确认”绑定时，才可在范围未变化的前提下免除第二次确认。
- “开始做吧”“按你建议来”“可以创建任务”等普通实现或建任务意图不是 Brief 预授权，不能据此跳过确认。
- 普通交互预授权只依赖当前对话中仍然明确可见的用户表达，不建立跨会话永久偏好，也不写 session runtime；auto-loop 恢复由上方 runner 例外所有。
- `in_progress` 阶段只读取 brief 和任务材料，不例行重新生成、展示或确认；新会话或压缩恢复同样如此。首次批准后的方案变化按下方增量规则处理，用户明确要求查看时再完整展示。
- `in_progress` 阶段发现缺失 brief 时，不自动生成未经 review 的 brief；先读取三件套并建议回补。只有用户明确要求当场回补并 review 时，才继续写回 `brief.md`。
- 不要机械限制 brief 或对话展示长度；信息完整优先，不能截掉会影响实现判断的范围、约束、风险或验收条件。

## 首次确认后的方案变更

本节区分首次完整交接及批准后的方案变更，不把规划讨论中的单项决定当成首次开工批准；不新建批准状态文件或从聊天摘要猜测授权。

1. 首次规划仍在收敛时，持续同步三件套并只询问未决产品事项；收敛后完整展示一次 Brief，按首次开工规则等待确认。
2. 已确认目标、范围和验收不变的实现细节调整，简述调整并更新必要材料后继续；文档刷新本身不触发重新审批。
3. 用户明确要求 A→B，且当前指令清楚覆盖变化及其影响、没有新增待决事项时，该指令就是增量决定。先同步受影响三件套及确需更新的 Brief，展示变化说明后继续，不再询问是否确认同一调整。
4. 新增目标、范围、验收、风险或产品取舍尚未明确决定时，只展示相对已批准方案的变化、影响和待决事项，请用户决定变化部分；未决部分不实施，已确认部分不重复审批。新增权限、生产、真实数据、费用、外部或破坏性边界必须有适用授权，不借泛化调整扩大范围。
5. 增量决定后同步最新材料；planning 状态的 Brief 仍须满足存在性和新鲜度校验，但刷新不等于批准，也不取消仍需作出的决定。跨任务事项先服从 Active Task Scope Guard；已完成任务返工先服从显式 reopen。
6. 会话恢复只读取实际材料和可验证的决定，不因恢复重新确认完整 Brief。批准证据缺失时只定位并补核受影响决定；用户要求全貌时完整展示，否则不重复未变化内容。

## 执行步骤

以下步骤服务首次完整交接。已有首次批准或处于 `in_progress` 时，先按上节处理本次增量和文档同步，再返回当前 workflow 阶段；不要重复套用首次展示/批准流程。缺失 Brief 仍沿用上述回补规则。

1. 确定任务目录：
   - 用户给了任务路径时使用该路径。
   - 否则运行 `python3 ./.trellis/scripts/task.py current --source`，读取 `Current task:`。
2. 读取任务状态：
   - 读取 `<task>/task.json` 的 `status`。
   - 如果 `status` 是 `in_progress` 且 `<task>/brief.md` 不存在，并且用户没有明确要求“回补 / backfill / 重新生成并 review brief”，则只读取三件套、说明 brief 缺失、建议回补，不写 `brief.md`。
3. 读取任务文件：
   - 必读：`prd.md`。
   - 存在则读：`design.md`、`implement.md`。
4. 判断当前对话是否存在有效预授权：
   - 若命中上方 Auto-Loop Action 例外，按 runner 授权处理；以下条件只约束普通交互预授权。
   - 必须由用户明确指向当前任务或最终 Brief，并明确表示展示后直接开始、不用再次确认或视为已确认。
   - 普通实现意图、任务创建授权、旧任务确认或无法确定指向的表达均按“无预授权”处理。
   - 若最终内容扩大范围、仍有未解决 Open Questions，或新增权限、安全、隐私、生产、费用、真实数据、破坏性公开契约、外部系统边界，则预授权失效。
5. 从最新三件套提取：
   - `Goal`：任务目标一句话。
   - `Scope`：本轮纳入的行为或改动对象；不重复技术原理、取舍或验收。
   - `Non-Goals`：明确不做或延后的范围。
   - `Technical Overview`：来源材料已明确技术机制时，简述触发入口、主要处理或数据流、关键校验或状态变化及结果；不复制完整设计或实施步骤，没有依据时省略整节。
   - `Context & Decisions`：影响实施判断的既有事实、关键文件或模块、入口、硬约束，以及已收敛且会改变产品行为、范围、UX、兼容性、风险或核心架构的取舍及原因；不复制完整决策台账，也不重复概览中的流程。
   - `Risks`：仍需在实现或验证中关注的具体风险；没有内容时省略整节。
   - `Acceptance`：主要可验证的验收标准；负向范围声明仅在需要回归验证时保留。
   - `Next Step`：只写进入下一阶段后的一个直接动作，不展开完整实施计划。
6. 写回 `<task>/brief.md`。如果文件已存在，仍用最新三件套派生内容覆盖旧正文。
7. 在对话中展示 brief 正文，并说明来源文件：
   - 经校验的 auto-loop `refresh_brief`：展示后返回 runner，不进入下方交互分支；schema 1 的确认由后续 action 所有。
   - 无有效预授权：展示后结束当前回合，等待用户确认。
   - 有有效预授权：先完整展示，再在同一回合返回主 workflow 执行 `task.py start`，不得省略展示步骤。

## 模板

```markdown
# Brief — <任务标题>

## Goal

- <一句话说明任务目标>

## Scope

- <本轮纳入的行为或改动对象，不复述原理、取舍或验收>

## Non-Goals

- <本轮明确不做或延后的事情>

## Technical Overview

- <仅在规划材料明确技术机制时，概述入口、处理流、关键校验和结果；否则省略整节>

## Context & Decisions

- <影响实施的既有事实、入口、约束，以及关键取舍与原因，不复述流程>

## Risks

- <仅在存在具体风险时生成；否则省略整个 section>

## Acceptance

- <主要验收标准>

## Next Step

- <进入实现后的下一步>
```

## 展示格式

Phase 1.4 review 前：

```markdown
任务交接摘要已更新：<task>/brief.md

<brief.md 正文>

请确认上述 brief；确认后才运行 `task.py start <task>`。
```

存在有效预授权时：

```markdown
任务交接摘要已更新：<task>/brief.md

<brief.md 正文>

已按你对当前 Brief 的明确预授权完成复核；范围未扩大、无未解决问题，继续启动任务。
```

规划评审或用户明确要求查看时，完整展示 `brief.md` 正文，不压缩、不摘录、不改写字段结构，保留 Non-Goals、技术概览（若有）、关键决定和验收条件。

## 不要做

- 不要在完整展示 brief 之前执行 `task.py start`；启动仍由主 workflow 执行。
- 不要把普通实现意图解释成免确认授权。
- 不要把一次预授权扩展为后续任务或其它高风险操作的长期授权。
- 不要修改三件套来迎合 brief。
- 不要把 `brief.md` 当作第四件套扩写。
- 不要只因为 `brief.md` 已存在就跳过更新。
- 不要只输出“已写入 brief.md”而不展示正文。
