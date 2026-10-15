---
name: sf-work
description: SpecForge 一键推进模式；用于用户明确要求“继续做完”“自动推进”“不要停”，但仍必须保留 gate、evidence、verification 和 archive 纪律。
---

# sf-work

## 运行目录

执行任何 `node .specforge/...` 命令或读取 `.specforge/...` 文件前，先从当前目录向上找到包含 `.specforge/` 的项目根，并在该目录执行后续命令。不要在 `frontend/`、`backend/` 等子目录直接运行相对 `.specforge/...` 命令。

一键推进模式。它不是跳过流程，而是自动循环调用正确的 `sf-*` 子技能。`sf-work` 可以减少用户手动输入，但不能替用户做产品确认、风险接受、gate 审查或缺证据批准。

自动推进的边界：可以自动执行确定性的脚本、生成模板、更新证据、运行验证；不能自动替用户选择产品范围、视觉风格、技术风险接受、上线确认或外部技能安装。

## 启动

```bash
node .specforge/core/scripts/doctor.mjs
```

## 内部技能母本

每轮自动推进前，读取 `.specforge/core/workflows/stages/status/SKILL.md` 判断当前 ready artifact，再交给对应 `sf-*` 子技能；阶段细节由子技能继续读取自己的内部母本。

## 关联标准

- `.specforge/core/standards/workflow.md`：ready artifact、required gate、scope 和停止条件。
- `.specforge/core/standards/engineering.md`：verification evidence 和高风险变更暂停。

## 循环

0. 每轮先运行：

```bash
node .specforge/core/scripts/doctor.mjs
node .specforge/core/scripts/instructions.mjs
node .specforge/core/scripts/artifact-graph-status.mjs
git status --short --untracked-files=all
```

1. 判断当前 ready artifact。
2. 先做推进安全检查：
   - gate 为 `REQUEST_CHANGES` / `REJECTED` 时，不继续下游，按 review / report 的 return path 回到修复技能。
   - requirements 前仍有 PRD 产品决策阻断时，暂停到 `sf-prd`。
   - requirements / ui_design / technical_design 前仍有用户取舍阻断时，暂停到 `sf-brainstorm`。
   - technical_design 有关键 `unknown` 时，暂停到 `sf-tech-design`。
   - technical_design 的核心决策摘要未确认、授权默认或标记 N/A 时，暂停到 `sf-tech-design`。
   - tasks 缺少核心字段，或条件字段无法覆盖 technical_design `yes` 影响面时，暂停到 `sf-tasking`。
   - implementation report、changed-files 和真实 git 状态不一致时，暂停到 `sf-implement`。
   - verification 有跳过项但没有 owner / 影响 / 重新验证条件时，暂停到 `sf-verify`。
   - wiki_sync 会产生重复 current wiki 文件，或 release / rollback 未覆盖 verification 残余风险时，暂停到 `sf-wiki` / `sf-close`。
3. 对 ready artifact 调用对应子技能：
   - requirements：先检查 `00-intake/brief.md`、可选 `brainstorm.md` 和 PRD 决策；如果存在需要用户取舍的 `[NEEDS DECISION]`，先调用 `sf-brainstorm`；如果 `PRD required: yes` 或表格中 `PRD required | yes`，且 `00-intake/prd.md` 不存在、`Decision Status` 不是 `approved-for-requirements`，或仍有 `[NEEDS PRODUCT DECISION]`，先调用 `sf-prd`；否则调用 `sf-requirements`
   - gap_report：`sf-discovery`
   - research：`sf-discovery`
   - ui_design：`sf-ui-design`
   - technical_design：`sf-tech-design`
   - tasks：`sf-tasking`
   - spec_review：`sf-spec-review`
   - implementation：`sf-implement`
   - code_review：`sf-code-review`
   - verification：`sf-verify`
   - wiki_sync：`sf-wiki`
   - closure：`sf-close`
4. 每完成一个 gate 或阶段后再次运行 doctor、`instructions.mjs`、`artifact-graph-status.mjs` 和 `git status --short --untracked-files=all`。
5. ready artifact 进入 `closure` 后交给 `sf-close`，由 `sf-close` 负责 release、rollback、archive dry-run 和 archive。
6. archive 成功后停止，并输出已完成 artifact、gate、验证和归档路径。

## 机器检查纪律

`sf-work` 的“不跳过 gate”不能只靠口头承诺。每一轮推进都要使用工具脚本确认状态：

```bash
node .specforge/core/scripts/doctor.mjs
node .specforge/core/scripts/instructions.mjs
node .specforge/core/scripts/artifact-graph-status.mjs
```

遇到 gate artifact 时，必须先生成对应 evidence 文件，再由对应子技能按自己的审查规则调用：

```bash
node .specforge/core/scripts/gate.mjs <gate> APPROVED --evidence <path>
```

如果 `instructions.mjs` 显示依赖未满足、gate 不是 `APPROVED`、artifact 是 `blocked` / `partial`，或者 doctor 失败，必须停止并说明阻断原因。不要通过手写总结替代 gate evidence。

每轮推进都要更新或检查对应 artifact 文件；如果子技能只能给建议，不能产出完整证据，`sf-work` 必须暂停让用户决策。

Gate artifact 允许自动生成草稿，但不允许“空模板批准”。批准前必须满足对应子技能完成标准：

- spec_review：无 P0 / P1，technical_design 影响面、tasks `_Impact:_` 和 verification 计划一致。
- code_review：真实 diff、changed-files、implementation report、tasks `_Impact:_` 四者一致。
- verification：风险驱动验证计划有证据，跳过项有 owner、影响和重新验证条件。
- wiki_sync：长期事实已写入唯一 current wiki 文件，或 N/A 理由具体可信。

## 必须暂停

- 出现 `[NEEDS CLARIFICATION]`。
- 当前 work item 是 `standard` / `feature` / `issue` 但 brief 缺少代码探索、外部研究 / 跳过理由、澄清记录或分析综合。
- feature / standard 的 brief 标记需要 PRD，但 `00-intake/prd.md` 不存在、`Decision Status` 不是 `approved-for-requirements`，或仍有产品决策阻塞。
- 产品、页面、全栈应用的功能候选池、MVP 组合、体验方向或关键技术路线尚未被用户确认。
- 有用户可见页面但缺少页面地图、线稿 / 原型、视觉风格确认或交互状态。
- 技术栈、组件库、编辑器、数据层或测试方案没有 profile / 取舍理由。
- technical design 初稿后的核心决策摘要没有用户确认、授权默认或明确 N/A。
- spec_review / code_review 发现 P0 / P1 阻断项。
- 任一 gate 为 `REQUEST_CHANGES` / `REJECTED`，且尚未按 return path 修复。
- `technical-design.md#0` 存在关键 `unknown`，或 tasks 缺少核心字段 / 适用条件字段。
- implementation report / changed-files / 真实 git diff 不一致。
- verification 缺关键证据、只测 happy path，或跳过项没有 owner / 影响 / 重新验证条件。
- wiki_sync 会产生重复 current 文件，或 release / rollback 没有覆盖 verification 残余风险。
- gate 需要用户判断、产品取舍、风险接受或上线确认。
- doctor、validate、selftest 失败。
- 变更触及生产发布、安全、权限、数据迁移或高风险外部影响。
- 需要安装依赖、访问网络、执行破坏性命令但未获确认。
- `sf-close` 提示需要同步安装到 Codex / Claude Code / cc-switch / Trae CN；该动作必须单独等待用户明确要求。

## 完成标准

- work item 归档。
- `node .specforge/core/scripts/validate-structure.mjs` 通过。
- 最终说明完成了哪些 artifact、哪些 gate、验证结果。
- 不存在未记录的 wiki / release / rollback 缺口。

## 不做

- 不为了“自动推进”跳过审查。
- 不隐瞒测试失败或未验证状态。
- 不自动安装 / 同步 Agent 技能副本到外部工具。
