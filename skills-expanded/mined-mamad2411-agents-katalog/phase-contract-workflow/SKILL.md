---
name: phase-contract-workflow
description: "Set up a Phase-Contract long-running workflow that drives an AI agent to work continuously for 5+ hours on a single project. Use when the user wants to plan a large migration, new product build, big refactor, long-form writing project, compliance remediation, or any multi-phase task that exceeds a single context window. Triggers: '让 AI 连续工作', '长任务规划', '分阶段执行', 'phase 规划', 'plan 规划', '多阶段迁移', '大型重构规划', 'long-running AI workflow', 'phase-contract', 'planctl', 'manifest + execution 双文档', '拆 phase', '规划压缩恢复', '给 AI 写 plan', '项目分阶段', '续跑规划', '合同链规划', '长任务续跑工作流'. Scaffolds plan/manifest.yaml, plan/common.md, plan/phases/, plan/execution/, a planctl scheduler script, plus synchronized agent instruction files (.github/copilot-instructions.md for Copilot, CLAUDE.md for Claude Code, AGENTS.md for Codex) so phase state is externalized and AI work can survive context compression across all three agents."
argument-hint: "(optional) target project path and short project description"
---

# Phase-Contract Workflow (长任务续跑工作流脚手架)

把任意长任务建模为**有序合同链**，让 AI 在小窗口内执行小合同、做完立刻写回外部状态，从而稳定连续工作 5+ 小时，并在上下文压缩或换会话后无损续跑。

参考完整方法论：[ai-long-running-workflow-methodology.md](./references/methodology.md)

## When to Use

**适用**：

- 中大型新产品从 0 到 1（5+ 个可独立交付的阶段）
- 框架/SDK 迁移、大版本升级（Vue2→3、Java8→21 等）
- 架构替换 / 大型重构 / 模块级重写
- 长文档工程（技术书、系列报告、课程讲义）
- 合规整改 / 安全加固（SOC2、等保、ISO 27001）
- 数据治理 / schema 重建 / 长链路 ETL 重写

**不要用**：

- 单次 bug 修复或一次性小任务（太重）
- 探索型研究（没有可预定义 phase）
- 需求高度不稳定、会频繁改写 phase 的阶段（先等需求稳定）

## Prerequisites（前置条件，必须满足）

以下前提**不满足则本 Skill 不生成任何文件**，必须先由用户处理：

1. **目标项目根目录必须是 git 工作区**。即在该目录下 `git rev-parse --is-inside-work-tree` 必须返回 `true`（worktree / submodule / 父仓库下未被 ignore 的子目录均视为合法 git 工作区）。
   - Phase-Contract 依赖 git 做 phase 级路径白名单比对、回滚与 handoff 校验。非 git 目录下 `execution/*` 的“允许改动/禁止改动”无法被客观核验，Quality Gate 会悬空，`complete` 写回的状态也无法对应任何可审计的 diff。
   - 修复方式：`cd <target> && git init && git add -A && git commit -m 'baseline'`，或把项目迁入已有 git 仓库后重试。
2. **本地有 `ruby` 可用**，版本 ≥ 2.6（`ruby -v` 验证）。planctl 是单文件 Ruby 脚本，不依赖 gem。macOS 14+ / 主流 Linux 发行版默认满足；Windows 用户推荐在 WSL 内使用。缺少 Ruby 时先由用户安装，本 Skill 不负责代安。
3. **显式 opt-out（不推荐）**：当项目确有理由不使用 git（例如临时沙盒、完全由另一套 VCS 管理），才可在调用本 Skill 前设置环境变量 `PHASE_CONTRACT_ALLOW_NON_GIT=1`，并在后续生成的 `plan/common.md` 里以风险段落明确记录此偏离及补偿措施（如何做 phase 级回滚、如何审计改动范围）。默认路径禁止走 opt-out。

## What It Produces

运行本 skill 会在目标项目里创建完整的 Phase-Contract 制品集：

```
<project>/
├── plan/
│   ├── manifest.yaml            # 流程清单（phase 顺序 + depends_on + required_context）
│   ├── common.md                # 全局硬约束（所有 phase 必带）
│   ├── workflow.md              # 流程说明
│   ├── state.yaml               # 执行账本（脚本写入）
│   ├── handoff.md               # 压缩恢复锚点（脚本写入）
│   ├── phases/
│   │   └── phase-0-<name>.md    # 定位合同模板
│   └── execution/
│       └── phase-0-<name>.md    # 执行合同模板
├── scripts/
│   └── planctl                  # 调度脚本（Ruby，可直接执行）
├── .github/
│   └── copilot-instructions.md  # Copilot 强制层
├── CLAUDE.md                     # Claude Code 强制层（内容同上）
└── AGENTS.md                     # Codex / 通用 Agent 强制层（内容同上）
```

## Core Principles (不可违反)

| #   | 原则           | 落地动作                                                                                             |
| --- | -------------- | ---------------------------------------------------------------------------------------------------- |
| P1  | 状态外部化     | 进度写 `state.yaml`，不写 AI 记忆                                                                    |
| P2  | 调度与执行分离 | 脚本决定做什么，AI 决定怎么做                                                                        |
| P3  | 三文件上下文律 | 工作窗口只装 `common + phase + execution` 三份文档                                                   |
| P4  | 双层合同       | `phases/*` 说"是什么"，`execution/*` 说"能碰什么"                                                    |
| P5  | 依赖强制校验   | `depends_on` + `--strict` 阻断跳步                                                                   |
| P6  | 完成即写入     | `complete` 原子写回 `state.yaml` 与 `handoff.md`，缺一不进下一圈                                     |
| P7  | 固定恢复协议   | 压缩后永远三步：manifest → handoff → next                                                            |
| P8  | 里程碑外部化   | `complete` 自动 `git add/commit/push`；有 remote 时形成远端记录，无 remote 时保留本地可回滚里程碑    |
| P9  | 显式整体收尾   | 全部 phase 完成后必须跑 `planctl finalize` 输出最终仪表盘并把决策权交还人类，AI 不得自行宣告项目结束 |

## Procedure

### Step 0: 环境前置检查（阻塞门禁）

**在收集任何输入、生成任何文件之前**，先验证 Prerequisites：

1. 在目标项目根目录执行：`git -C <target> rev-parse --is-inside-work-tree`。
2. 若返回 `true` → 继续 Step 1。
3. 若返回非零或 `false`：
   - 立刻停止脚手架流程，**不要**创建 `plan/`、`scripts/planctl`、任何 agent 强制层文件。
   - 向用户输出标准指引（原样输出，不要软化）：

     > 检测到 `<target>` 不是 git 工作区。Phase-Contract Workflow 依赖 git 做 phase 级白名单比对、回滚与 handoff 校验，缺少 git 会让 phase-0 之后的每一次 `complete` 都无法被客观核验。
     >
     > 请先执行：
     >
     > ```bash
     > cd <target>
     > git init
     > git add -A
     > git commit -m 'baseline'
     > ```
     >
     > 然后重新调用本 Skill。若该项目确需不使用 git，请在调用前 export `PHASE_CONTRACT_ALLOW_NON_GIT=1` 并准备在 `plan/common.md` 里记录风险与补偿措施。

   - 等待用户决策后再重新进入 Step 1；不要提供“那我先跳过这步”之类的折中方案。

4. 若 `PHASE_CONTRACT_ALLOW_NON_GIT=1` 已显式设置，允许跳过此门禁，但必须在后续 Step 2 生成 `plan/common.md` 时强制写入“非 git 工作区偏离”风险段落（编号的独立段），明确列出：偏离原因、手动回滚方案、改动审计方式。

### Step 1: 收集输入

如果用户未指定，使用 ask-questions 工具逐项收集：

1. **项目根目录路径**（绝对路径）
2. **项目一句话定位**（写入 common.md 和 manifest）
3. **切分主维度**：按模块 / 按层次 / 按章节 / 按控制项 / 按迁移波次（必须选一，不能混用）
4. **初始 phase 列表**：phase id + 一句话标题 + depends_on（5–12 个为宜）
5. **全局硬约束**：技术栈版本、依赖禁区、质量底线、非目标（5–10 条，够锋利即可）

写不出客观完成判定的 phase，就是切错了，当场要求用户改切分。

### Step 2: 生成骨架文件

按 [templates/](./references/templates.md) 的模板同时产出：

- `plan/manifest.yaml`：带 `compression_control`、`execution_rule`、`required_context` 三块；phase 列表展开所有 id 和 `depends_on`
- `plan/common.md`：把 Step 1 第 5 项的硬约束成文
- `plan/workflow.md`：直接复制 [references/workflow-template.md](./references/workflow-template.md)
- `plan/state.yaml`：初始空态（`version: 1 / completed_phases: [] / completion_log: []`）
- `plan/handoff.md`：初始态，标注"尚未开始任何 phase"
- `.github/copilot-instructions.md` **和** `CLAUDE.md` **和** `AGENTS.md`：三份内容完全相同，均直接复制 [references/agent-instructions-template.md](./references/agent-instructions-template.md)，把 `<PROJECT>` 替换为项目名。这三份分别被 GitHub Copilot、Claude Code、Codex（以及其他兼容 `AGENTS.md` 的 agent）在会话开头自动注入。**必须同步修改，任何单边漂移都会破坏强制层。**如项目只使用其中某一种 agent，也建议保留三份以便将来切换。

### Step 3: 安装 planctl

把 [scripts/planctl.rb](./scripts/planctl.rb) 复制到目标项目的 `scripts/planctl`，加可执行位：`chmod +x scripts/planctl`。planctl **不内置固定的中间产物名单**；这部分交给 AI 在 phase 实施中结合未跟踪文件、构建/编译/运行/测试命令输出、路径语义和“是否可从源码重新生成”自行推理。凡被判断为临时输出的路径，AI 应在 `complete` 前把精确规则写入根目录 `.gitignore`，避免 `git add -A` 把它们带进里程碑提交；凡属于真实交付物、fixture、快照基线、lockfile、必须入库的生成代码/文档，则不得误忽略。跑一次 `ruby scripts/planctl status` 自检，再跑 `ruby scripts/planctl doctor` 做一次完整体检（Ruby 版本、git 工作区、manifest 引用、state/handoff 一致性、三份 agent 指令 SHA256 比对）。

### Step 4: 生成第一批 phase 合同

- 为 `phase-0`（和用户明确想立刻启动的 phase）生成**正式**的 `phases/*` 和 `execution/*`
- 为其余 future phase 生成**成对占位合同**，使用 [references/phase-templates.md](./references/phase-templates.md) 里的 `PHASE_CONTRACT_PLACEHOLDER` 模板

不要一次把所有 future phase 都写成正式合同——那会破坏"只装 3 份文档"的不变量，也会被后续认知更新推翻；但也不要留空文件，因为 `planctl doctor` 需要验证 manifest 引用存在，而 `advance --strict` 需要在该 phase 轮到当前时识别它仍是占位合同并返回 `ACTION: promote_placeholder`。

模板见 [references/phase-templates.md](./references/phase-templates.md)。

写作铁律：

- 完成判定禁止出现"良好"、"合理"、"基本完成"等主观词
- execution 的"允许改动"必须是路径级白名单
- execution 是**围栏**而不是**脚手架**，不要写"第一步 A 第二步 B"

### Step 5: 启动并验证

在目标项目根目录运行：

```bash
ruby scripts/planctl advance --strict
```

验收三条：

1. 命令以 0 退出码返回 `ACTION: implement`、当前应执行的 phase 和其 `required_context`
2. `required_context` 恰好是三份：`common.md` + `phases/phase-0-*.md` + `execution/phase-0-*.md`
3. `plan/handoff.md` 已包含压缩恢复三步和下一 phase 指引

### Step 6: 输出使用指南

告诉用户后续每一圈的循环命令（Golden Loop）：

```bash
# 查看下一步（连续执行状态机）
ruby scripts/planctl advance --strict

# 实施该 phase 后标记完成（自动刷新 handoff、并 git add -A / commit / push 本 phase 的里程碑）
ruby scripts/planctl complete <phase-id> --summary "<做了什么>" --next-focus "<下一个 phase 要关注什么>" --continue

# complete --continue 会立刻运行 advance；若 ACTION: promote_placeholder，先补正式合同，再重跑 advance
# 当 advance 返回 ACTION: finalize 时，跑一次 finalize 收尾，不要直接收工
ruby scripts/planctl finalize
```

> 注：`complete` 已自动 `write_state` → `write_handoff_file`（均为 tmp+rename 原子写入）。`ruby scripts/planctl handoff --write` 仅作为**手动补救**：比如你手改了 `state.yaml` 但忘了别的联动刷新，或 `complete` 后 `handoff.md` 被意外编辑需要重放。正常循环不需要多这一步。

> 若 `advance --strict` 返回 `ACTION: promote_placeholder`，这不是用户确认点，而是 Golden Loop 内部待办：先把两份文件升级成正式合同，再重跑同一条 strict 命令。

**压缩恢复 / 冷启动**：新会话开场只需一条命令，替代手动读三份文件：

```bash
ruby scripts/planctl resume --strict
```

输出包含项目概览、handoff 快照和下一步 `ACTION`，足以让任意 agent 在单次读取中恢复全部上下文并继续 Golden Loop。

**仓库体检**：怀疑三份 agent 指令失步、manifest 引用断裂或 state 与 handoff 不一致时，运行：

```bash
ruby scripts/planctl doctor
```

脚本按 SHA256 比对三份 agent 指令、校验 manifest 中每个 phase 的 plan_file/execution_file 是否存在、检查 `state.yaml` 中的 phase id 是否都在 manifest 里，问题以 exit 2 退出。

并提醒三件事：

- 压缩或新会话恢复**永远且仅**三步：读 manifest → 读 handoff → 跑 `advance --strict`（或一步 `resume --strict`）
- `complete` 是写回 state + handoff + git 里程碑的原子入口；**不要**再对其补一次 `handoff --write`，未跑 `complete` 的 phase 则直接不视为完成
- `complete --continue` 之后必须立刻服从 `advance` 的下一 `ACTION`；若返回 `promote_placeholder`，先升级该 phase 的两份合同，不要停下来问用户是否继续
- 未写入 `state.yaml` 的 phase 不视为完成，不管 AI 自己说做得多好
- 当 `advance` / `complete --continue` 输出 `ACTION: finalize` 或 “All phases are completed”，下一动作不是直接对人类宣告项目结束，而是跑 `ruby scripts/planctl finalize`，把仪表盘和决策权按 Step 8 交还人类

### Step 7: 里程碑提交与推送（`complete` 自动执行）

`complete` 会在 phase 被判定完成、`state.yaml` / `handoff.md` 写回之后，自动完成以下 git 操作，用于给每个 phase 留下一次**可回溯、可回退、可审计**的里程碑记录。**AI 在 phase 实施过程中不要自己 `git commit` / `git push`**，统一交给 `complete` 一次性收尾，避免半成品提交和消息风格漂移。

自动流程：

1. 在 `git add -A` 之前，AI 先根据当前 phase 产生的未跟踪/新生成文件自行推理哪些属于构建 / 编译 / 运行 / 测试临时输出，并在需要时更新根目录 `.gitignore`。随后 planctl 再执行 `git add -A`，把 phase 产出的代码/文档、`plan/state.yaml`、`plan/handoff.md`（以及必要时新更新的 `.gitignore`）一并入栈。
2. 若暂存区为空（例如重复 `complete`）→ 跳过提交，给出 `Nothing to commit` 提示。
3. 否则以地道英文提交，格式：
   - Subject：`chore(plan): complete <phase-id> — <phase title>`（自动截断到 100 字符内）
   - Body：用户传入的 `--summary`（缺省时为通用提示语）
   - Trailers：`Phase-Id: <id>`、`Next-Focus: <...>`（来自 `--next-focus`）、`Automated-By: scripts/planctl complete`
   - 通过 `git commit -F -`（stdin）写入，完全尊重仓库的 pre-commit / commit-msg hook，不使用 `--no-verify`。
4. `git push`：若仓库已配置 remote，则优先用当前分支的 upstream；若无 upstream，则回退到 `git push -u origin HEAD`（没有 `origin` 时使用第一个可用 remote）。若仓库尚未配置任何 remote，则**跳过 push 并继续执行**，只打印 warning，phase 仍视为已完成。
5. 失败不回滚：`state.yaml` 已经记录完成。无 remote、push 失败或 commit/push 其他异常都只输出 warning，让用户手动处置，不会把已完成的 phase 标回未完成，也不应因此中止后续 phase 规划与执行。

环境变量（仅用于特殊场景，默认**不要**设置）：

- `PHASE_CONTRACT_SKIP_PUSH=1`：只做本地 commit，不推送（离线或保密分支）。
- `PHASE_CONTRACT_SKIP_COMMIT=1`：同时跳过 commit 与 push（极端情况下排障用）。
- `PHASE_CONTRACT_ALLOW_NON_GIT=1`：非 git 工作区模式，`complete` 的 git 收尾整体不执行。

典型输出：

```text
Marked complete: phase-0-scaffold
Updated state file: plan/state.yaml
Updated handoff file: plan/handoff.md
[main 33b5258] chore(plan): complete phase-0-scaffold — bootstrap plan artifacts
[planctl] Committed milestone: phase-0-scaffold
To git@github.com:acme/widget.git
   c6a54d1..33b5258  main -> main
```

### Step 8: 整体收尾（`planctl finalize`）

每一份 plan 在“最后一个 phase 也跑完 `complete`”之后，**还差一步**才算真正结束：跑一次 `ruby scripts/planctl finalize`，把全部状态聚合成最终执行仪表盘并把决策权交还人类。这一步是 Skill 的最后一公里，不是可选优化。

触发条件（满足任一即进入收尾）：

- `complete` 的输出里出现 `All phases are completed. No remaining work.`
- `advance` 或 `complete --continue` 的输出里出现 `ACTION: finalize`

AI 必须立刻执行的动作（连续执行，不需要用户确认）：

```bash
ruby scripts/planctl finalize
```

`finalize` 仅在 `state.yaml` 已包含 manifest 中全部 phase 时才会运行，否则以 exit 2 拒绝（防止半成品 plan 被误收尾）。它一次性聚合：

1. **项目总览**：phase 总数 / 完成数、首末完成时间戳、累计 elapsed。
2. **Phase 台账**：每个 phase 的 id、标题、completed_at、summary、next_focus，以及 `git log --grep "Phase-Id: <id>"` 找到的里程碑 commit SHA。找不到的 phase 会被显式标出，提示人工对账。
3. **仓库状态**：当前分支、upstream、ahead/behind、工作树是否干净、未提交文件清单（截断到前 10 条）、配置的 remotes、最近一次 commit。
4. **Health 检查**：manifest → plan_file/execution_file 引用是否还存在、`state.yaml` 中的 phase id 是否都在 manifest 里、三份 agent 指令（Copilot / CLAUDE / AGENTS）是否仍然 SHA256 一致。issue 与 note 分开列。
5. **Recommended human next steps**：基于上面四块自动推导，例如有未推送 commit 就提示 `git push`、没有 remote 就提示先 `git remote add origin`、有 phase 缺 summary 就提示补叙述，并附上一组**通用收尾动作**（端到端验收、人类 code review、决定是否打 release tag、归档 `plan/`、写对外交付说明、把发版/维护决策交还人类）。

拿到 finalize 输出后，AI **必须再做一次深入审视**，不要原样转发：

- 通读 `manifest.yaml` / `state.yaml` / `handoff.md` 与最近 N 条里程碑 commit，验证仪表盘里的 phase ledger、git 状态、health 与仓库实情吻合。
- 把通用建议翻译成本项目的具体动作（带命令、目标分支、潜在审阅者、时限），区分“立即必须”、“短期推进”、“可选优化”。
- 找出 finalize 没显式说但客观存在的风险：例如某条 summary 与 diff 不一致、某条建议在本项目语境下不适用、health notes 中的轻警告是否需要升级为 issue。

最后必须以**最终执行仪表盘**形式向人类汇报，并显式把以下决策点交还人类（**AI 不得自行执行**）：

- 是否上线 / 发版 / 对外公布
- 是否对成果打 release tag（`git tag -a vX.Y.Z`、是否 `git push --tags`）
- 是否归档 `plan/`（`git mv plan plan-archive-<date>`）后开启下一项规划，或保留作为长期档案
- 是否安排长期维护、轮值或回归测试
- 是否需要安全 / 合规 / 法务审阅

在人类未明确指示之前，AI 不得 `git tag` / 推 tag / 删除或移动 `plan/` / 重跑本 Skill 脚手架 / 继续修改 `state.yaml`。若 finalize 的 health 报告了 issue，按 Step 7 的"中止条件"逻辑先汇报由人类决定是先修问题再收尾还是接受现状收尾。重复 `finalize` 无副作用但应避免当 status 用。

## Decision Points

**phase 数 > 12**：当场要求重切，或引入 `epic` 分组层（见 [references/methodology.md §7.1](./references/methodology.md)）。

**依赖成环**：直接判定切错，重构 phase 边界。任何循环依赖都不合法。

**common.md 写到第 15 条还刹不住**：区分"约束"（永恒不变）和"策略"（可能变化），把后者下放到具体 phase。

**用户说"phase 文档 AI 帮我全写了吧"**：只把 phase-0（和准备立刻启动的 phase）写成正式合同；future phase 先保留占位合同。manifest 和 common 必须由用户主导，否则 AI 拟合会把全局带偏。

**`advance --strict` 指向的新 phase 仍是占位合同**：这不是 blocker，也不是用户确认点。`advance` 会返回 `ACTION: promote_placeholder`；先把该 phase 的 `phases/*.md` 和 `execution/*.md` 同步升级成正式合同，再 rerun 同一条 strict 命令；返回 `ACTION: implement` 前不得开始实现。

**用户已有 phase 结构但没有 planctl 体系**：跳过 Step 1.3–1.4，仅生成基础设施（manifest、common、workflow、planctl、三份 agent 指令），把已有 phase 文档纳入 manifest。

**某个 phase 做坏了需要回退**：运行 `ruby scripts/planctl revert <phase-id>`。默认 `--mode revert` 用 `git revert` 保留历史（安全，可推送）；`--mode reset` 用 `git reset --hard` 重写历史（仅限私有分支，脚本不自动 push）。脚本会自动从 `state.yaml` 移除该 phase、在 completion_log 追加 `reverted_at` 条目、并以 `chore(plan): revert <phase-id>` 提交 ledger。若该 phase 还有**已完成的下游依赖**，脚本会拒绝回退，必须按逆序先回退下游。

**AI 在 phase 间越界改文件**：在 `manifest.yaml` 的 `execution_rule` 下加 `enforce_allowed_paths: true`，并给每个 phase 填 `allowed_paths:` glob 白名单（见 [references/templates.md](./references/templates.md)）。开启后 `complete` 会在写回 state 之前把 `git diff --cached` 与白名单比对，越界路径直接 abort 且**不更新 state.yaml**，phase 保持未完成。临时关掉走 `enforce_allowed_paths: false`（仅警告）或 `PHASE_CONTRACT_ENFORCE_PATHS=1` 覆盖。

**新会话冷启动 / 上下文压缩后续跑**：运行 `ruby scripts/planctl resume --strict` 或 `ruby scripts/planctl advance --strict`。一次性打印项目概览、handoff 快照和下一 phase 的完整结果，等价于手动读 `manifest` + `handoff` + 跑状态机。

**怀疑 state/agent 指令失同步**：运行 `ruby scripts/planctl doctor`。按 SHA256 对比 `.github/copilot-instructions.md`、`CLAUDE.md`、`AGENTS.md` 三份指令是否字节一致，校验 manifest 引用、state 与 handoff 的一致性；发现问题以 exit 2 退出。

**最后一个 phase 也跑完 `complete` 了**：不要直接对用户宣告“项目完成”。立刻按 Step 8 跑 `ruby scripts/planctl finalize`，把仪表盘汇报给人类并显式把发版 / 打 tag / 归档 `plan/` / 安排维护等决策点交还。`finalize` 在 phase 未全部完成时会 exit 2 拒绝运行，所以它本身就是“是否真正可以收尾”的判定门。

## Quality Gates

生成完成后逐项核对：

- [ ] 目标项目根目录是 git 工作区（`git rev-parse --is-inside-work-tree` 为 `true`），或已显式设置 `PHASE_CONTRACT_ALLOW_NON_GIT=1` 且 `plan/common.md` 含偏离风险段
- [ ] `manifest.yaml` 的 `phases[].required_context` 恰好三项（common + plan + execution）
- [ ] `manifest.yaml` 的 `compression_control.rules` 明确禁止一次性加载全部 phase 文档
- [ ] `common.md` 只包含永远不变的约束，无实施步骤
- [ ] `phases/phase-0-*.md` 的"完成判定"全部为客观可勾选项
- [ ] `execution/phase-0-*.md` 的"允许改动"是路径白名单而非能力描述
- [ ] `phase-0`（和任何准备立刻启动的 phase）使用正式合同；尚未进入的 future phase 使用带 `PHASE_CONTRACT_PLACEHOLDER` 的成对占位合同，且哨兵位于文件前 40 行
- [ ] `execution/phase-0-*.md` 包含"执行裁决规则"一票否决条款
- [ ] `.github/copilot-instructions.md`、`CLAUDE.md`、`AGENTS.md` 三份内容完全一致，均包含 10 条硬约束（见 [references/methodology.md §9](./references/methodology.md)）
- [ ] 三份 agent 指令**不得引入 agent-specific 段落**（任何"仅 Claude 看"、"仅 Copilot 看"的差异都会让 `planctl doctor` 的 SHA256 比对报错）；若确需差异，改为在 `plan/common.md` 里用"按 agent 区分"的小节承载
- [ ] `scripts/planctl` 可执行，`ruby scripts/planctl status` 跑通
- [ ] `planctl advance --strict` 返回 `ACTION: implement`、phase-0 且 required_context 为三份
- [ ] 当某个 future phase 仍是占位合同且它变成 current phase 时，`planctl advance --strict` 会返回 `ACTION: promote_placeholder`，直到两份合同被升级
- [ ] 首次 `complete` 前若仓库已出现未跟踪中间产物，AI 已基于可再生性、交付边界与项目约定自行判断并更新根目录 `.gitignore`，且不会把这些产物带进里程碑提交
- [ ] 若目标项目已配置 `git remote`，其当前分支可推送；若暂时无 remote，已在对用户的交付说明里明确说明：后续 `complete` 将仅本地 commit、跳过 push，但**不阻塞**继续执行后续任务
- [ ] `scripts/planctl finalize` 在 phase 尚未全部完成时以 exit 2 拒绝运行；当且仅当 `state.yaml` 包含全部 manifest phase 时才打印仪表盘
- [ ] 三份 agent 指令均含 §十二「整体收尾规约（Finalization）」，且禁止行为里明确不得跳过 `finalize` 自行宣告项目结束

## References

- [完整方法论（Phase-Contract Workflow）](./references/methodology.md)
- [manifest / common / state / handoff 模板](./references/templates.md)
- [phase 定位合同 + 执行合同模板](./references/phase-templates.md)
- [plan/workflow.md 模板](./references/workflow-template.md)
- [Agent 强制层模板（Copilot / Claude Code / Codex 通用）](./references/agent-instructions-template.md)
- [planctl 调度脚本](./scripts/planctl.rb)
