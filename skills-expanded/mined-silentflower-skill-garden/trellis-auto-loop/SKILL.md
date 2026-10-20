---
name: trellis-auto-loop
description: "启动、恢复和推进 Trellis 自动任务循环。用于用户明确要求 auto loop、自动跑任务、/goal 类似流程、一次跑多个任务、继续自动 run、查看/停止 auto-loop，或压缩恢复后需要执行 .trellis/scripts/auto_loop.py next 获取 runner action。"
---

# Trellis Auto Loop

用 `.trellis/scripts/auto_loop.py` 驱动批量无人值守任务。runner 是状态、manifest、hash、依赖和预算的权威；本 skill 只判断语义边界并执行 runner 返回的 action。

## Run Contract

- 仅在用户明确要求 auto-loop、自动跑到底、goal-like 或继续既有 run 时使用；普通实现请求不能自动升级。
- 用户发出启动指令即授权本次 `commit-only` run。prepare 完成后不再确认 manifest，也不逐任务执行 `confirm_brief`。
- 新 run 先 prepare 全部显式任务，Open Questions 全部收敛后才进入 running。running 中不再询问 route、planning 或普通 Check-All 停止边界。
- 每个 action 完成后，必须用同名 `record --action ...` 精确回写；record 成功后立即 `next`。不得根据聊天摘要手改 runtime 或跳步。
- `record` 返回 `status=retryable` 时不得运行 `next`，必须按返回指令在同一个 outstanding action 内纠正并重录；恢复诊断的 owner 见下方 Action 内恢复。
- 本地提交是自动终点。不得 push、merge、release 或 deploy；runner 在 item 本地提交成功后原子写入 `progress`、`status=completed`、`completedAt` 与确定性 `closeout`。`closed` 立即退出活跃视图，物理 GC 由后续 SessionStart 处理。
- 任务顺序只决定稳定调度顺序，不隐含依赖。依赖必须通过 `--depends-on dependent=dependency` 明确传入或由 planning artifacts 明确声明。
- 任务级失败只阻塞自身及显式依赖项；独立任务继续。fix/recheck、planning repair 与安全的 commit-only repair 各最多 3 轮，队列结束后不自动执行第二遍恢复扫描。
- schema 1 runtime 继续按 runner 返回的旧 action 恢复，包括 outstanding `confirm_brief`；不要把旧 run 改写成 schema 2。

启动或恢复前静默清除交互式 pre-check hold；miss、task mismatch 或损坏诊断不阻断 runner：

```bash
python3 ./.trellis/scripts/pre_check_state.py clear
```

## Start

任务列表必须显式。用户只说当前任务时，先用 `task.py current --source` 解析。启动前进入 `trellis-route` 的“auto-loop 启动前选模例外”：对队列任务只读解析 implement/check，复用匹配任务的 session 决定或个人默认，只询问未决 target。临时选择才传 runner 参数，明确请求的个人默认由 `write-pref` 保存；不提前写 task route decision、绑定任务或实施。

模式确定后同轮回到本 skill，执行下方 start + next，先完成 runner 的 prepare；不得套用普通 route 的选完立即实施，也不等待用户回复“继续”。只有 runner 返回 `run_implement` / `run_check_all` 等运行 action 后才按对应 route 实际执行。

```bash
python3 ./.trellis/scripts/auto_loop.py start \
  --tasks <task> [<task> ...] \
  [--depends-on <dependent>=<dependency>] \
  --profile commit-only \
  [--check-depth auto|light|full] \
  [--route-implement inline|subagent] \
  [--route-check check-all-inline|check-all-subagent]
python3 ./.trellis/scripts/auto_loop.py next
```

默认 check depth 为 `auto`。light/full 只是 Check-All 请求深度，不是 route mode；hard-full 风险仍由 Check-All 升级。

用户一次选择全 Inline/Subagent 时可同时映射两个 route：

- Inline：`--route-implement inline --route-check check-all-inline`
- Subagent：`--route-implement subagent --route-check check-all-subagent`

runner 在 start 时检查任务存在性、task status、staged/conflict/未完成 Git 集成，并捕获主仓及已初始化子仓的 dirty baseline。全局安全错误不得通过 `--force` 绕过。

## Prepare Actions

prepare action 必须先完成并 record，runner 才会继续扫描整个队列。

| action | 主 agent 行为 | record |
| --- | --- | --- |
| `classify_dirty_baseline` | 把每个 `repository::path` 精确归到一个任务的 owned dirty，或归为 protected-retained；不猜测归属 | `record --action classify_dirty_baseline --result ok [--owned-dirty <task>=<repository>::<path>] [--protected-retained <repository>::<path>]` |
| `resolve_open_questions` | 使用 `trellis-brainstorm` 一次引导人工回答一个问题，并更新对应 planning artifacts；AI 不得代答、删除、改写或勾选 | 全部问题消失后 `record --action resolve_open_questions --result ok` |
| `review_planning_readiness` | 读取 action 绑定的 artifacts，按 Brainstorm Quality Bar 判断 `ready|repairable|blocking` | `record --action review_planning_readiness --result ok --readiness-verdict ready|repairable --summary "..."`；blocking 用 `--result blocked` |
| `run_planning_repair` | 仅按现有需求、代码、spec 和仓库证据修复 planning；不得处理 Open Questions 或高风险事项 | `record --action run_planning_repair --result ok --summary "..."` |
| `refresh_brief` | 使用 `trellis-task-brief` 刷新派生的 `brief.md`，无需再次让用户确认 | `record --action refresh_brief --result ok` |

`resolve_open_questions` 是整队列门禁：任一任务仍有 `- [ ]` 或历史裸列表时，run 保持 `awaiting_input`，不得先执行其它任务。`- [x]`、空章节或无章节不阻塞。

readiness 的 `repairable` 仅适用于不改变目标、可由仓库证据确定的问题，例如验收不可测试、design/implement 不完整或 context 未整理。达到 3 轮、需要产品选择或越过风险黑名单时返回 blocking。

## Autonomous Decisions

满足任务目标内、仅影响本地代码、可逆且可验证时，AI可自主选择推荐方案。作出选择后必须先记录，再继续修改或 record；会修改 planning/handoff 时，`--task-file` 或完整 `--file` 必须列出全部目标 artifact：

```bash
python3 ./.trellis/scripts/auto_loop.py decide \
  --task <task> \
  --topic "<主题>" \
  --option "<候选>" [--option "<候选>" ...] \
  --choice "<选择>" \
  --summary "<依据摘要>" \
  [--evidence "<证据>" ...] \
  --risk low|medium \
  --confidence low|medium|high \
  [--requirement <id> ...] [--task-file <name> ...] [--file <repository>::<path> ...] \
  [--verification "<验证摘要>"]
```

决策写入 runtime 摘要和任务 `decisions.jsonl`，只保存结论与证据，不保存思维链。下一次同任务 action record 会消费该决策：列明的 planning/handoff 变化生成绑定 decision ID 的 manifest revision；Check record 中其它变化进入有限自纠，其它 action 的确定路径错误先进入恢复诊断，未知或越界漂移仍按 `artifact-drift` 阻塞。

以下事项不得用 `decide`，必须 blocked：

- 不可逆真实数据修改。
- 扩大权限或降低安全、隐私保护。
- 公开 API 或数据格式破坏性变更。
- 费用、生产环境或外部系统影响。
- push、merge、release、deploy、物理 GC 或其它外部副作用。
- 明显改变任务目标或业务规则且仓库没有倾向证据。
- `Open Questions` 中人工保留的任何选择。

## Action 内恢复

`next` 保留原 action 和文档基线，不消费 pending。收到 `artifact-recovery-required` 或 `artifact-recovery-failed` 时，必须读取 [恢复协议](references/artifact-recovery.md)，同轮完成诊断、纠正、`reconcile` 校验并继续原 action。初次诊断不计数，最多三次实际纠正，第三次仍可成功；不要求用户回复“继续”。

## Running Actions

| action | 主 agent 行为 | 成功 record |
| --- | --- | --- |
| `start_task` | 执行 action 返回的 `task.py start ...` | `record --action start_task --result ok` |
| `run_implement` | 进入 Phase 2.1，复用 manifest/当前任务 implement route | `record --action run_implement --result ok --route-mode <mode> --route-source <source>` |
| `run_check_all` | 进入 Phase 2.2，按 requested depth 执行统一 Check-All | `record --action run_check_all --result ok --route-mode <mode> --route-source <source> --effective-check-depth light|full --check-depth-reason "..." [--doc-remediation-file <repository>::<path> ...]` |
| `run_fix` | 根据 `last_failure` 修复并复用 implement route | `record --action run_fix --result ok --route-mode <mode> --route-source <source>` |
| `run_recheck` | 复用 check route，且不得低于 `minimum_check_depth` | 同 `run_check_all`，action 改为 `run_recheck` |
| `run_spec_update` | 执行 `trellis-update-spec` | `no-op|written` 用 ok；`needs-review` 用 blocked + `spec-needs-review` |
| `commit_only` | 复用 `trellis-push` 内部多仓精确本地提交能力，不 push | `record --action commit_only --result ok --commit <primary-or-last-hash> [--repo-commit <repository>::<hash> ...] --files <exact...> --commit-message "..."` |

失败或越权时必须回写，runner 决定重试、blocked 或继续队列：

```bash
python3 ./.trellis/scripts/auto_loop.py record \
  --action <action> --result failed|blocked \
  --failure-type <type> --summary "<摘要>" \
  [--repo-commit <repository>::<hash> ...] \
  [--files <repository>::<path> ...]
python3 ./.trellis/scripts/auto_loop.py next
```

Check-All 的 ok/failed/blocked 都要带实际 effective depth 与原因。validated auto-loop 不进入普通 Post-Check Stop Gate；检查完成后立即 `record + next`。

Check-All 自动修复当前任务 `implement.md` 或 `brief.md` 时，每个实际变化文件都要用重复的 `--doc-remediation-file` 精确声明；声明集合必须与 action 发出后的真实变化完全一致。`prd.md`、`design.md`、其它任务和其它仓库文件不得使用该参数。

若 Check record 返回 `status=retryable reason=artifact-drift`：

1. 不运行 `next`，保留 runner 返回的 outstanding action。
2. 若是本 action 的误改，撤回误改后用原 action 重录。
3. 若是合法 `implement.md` / `brief.md` DOC 修复，补齐精确 `--doc-remediation-file` 后重录。
4. 若无法安全归因，使用原 action、`--result blocked --failure-type artifact-drift` 重录并停止。

同一 Check action 最多允许 3 次 retryable 自纠，第 4 次进入 terminal blocked。实现、spec update、commit-only 等其它 action 的 artifact drift 不使用该预算；commit-only 只有下方明确的 `commit-repairable` 本地失败可以使用独立三轮预算。

## Commit-Only

收到 `commit_only` 后：

1. 用 `status` 确认 active run、profile、outstanding action 和 task 一致。
2. 调用 `trellis-push` 内部 `commit-only`，由它根据任务 artifacts、项目 SOP/spec、受版本控制脚本和可验证 Git/submodule 关系，从当前真实 Git 状态生成有序 `commit -> generate -> commit` 链。不得仅因多个仓库、submodule pin 或证据充分的本地生成命令返回 `multi-repo-commit-boundary`。
3. 仓库发现、证据冲突处理、生成入口校验、exact/retained 归属和逐步 Git 预检都由 `trellis-push` 负责；本 skill 不另行猜测依赖、拼接命令或绕过其计划。只有本地生成入口确定性、可重复、受版本控制且无外部副作用，并且计划外 dirty、retained、staged、分支和 HEAD 都满足其安全契约时才继续。
4. 按 `trellis-push` 的计划精确提交和运行生成入口。不得裸 `git add .`、`git add -A`、push、按时间差猜归属或撤销已经成功的本地 commit。
5. 确定性生成失败、生成结果尚未收敛或可重新规划的本地预检失败时，用 `--result failed --failure-type commit-repairable` 回写全部已完成 `--repo-commit`，然后立即 `next`。runner 前 3 次会重新发出同一个 action；每次都从真实 Git 状态重建计划，验证并跳过已完成提交，安全重跑生成，后续仓 clean 时跳过空提交。第 4 次失败进入 `commit-repair-budget-exhausted`。
6. 全部完成后，用主仓或最后提交传 `--commit`，并为每个已完成仓库重复传入 `--repo-commit <repositories[].root>::<hash>`；同时传 `--files`、`--retained-files` 和 `--commit-message`，record 成功后立即 next。

`commit-repairable` 只用于继续执行仍然安全的本地确定性链。外部副作用风险或任何 Git 安全边界问题必须用 `blocked` 或非 repairable `failed` 立即结束当前项。部分成功提交跨 retry/resume 保留，不回滚、不 amend、不重复创建。

`decisions.jsonl` 属于当前任务文件，发生决策时应进入该任务最终精确提交。runner 在 item 本地提交成功后把 `task.json.status` 写为 `completed` 并补 `completedAt`；只允许 `in_progress -> completed` 这一个跃迁，既有 `completedAt` 保持不变。这是本地完成态，不代表已归档。

## Resume, Retry, Stop

```bash
python3 ./.trellis/scripts/auto_loop.py resume
python3 ./.trellis/scripts/auto_loop.py next

python3 ./.trellis/scripts/auto_loop.py retry-blocked \
  [--run-id <run-id>] [--task <task>] [--all] \
  [--check-depth auto|light|full]
python3 ./.trellis/scripts/auto_loop.py next

python3 ./.trellis/scripts/auto_loop.py status [--verbose]
python3 ./.trellis/scripts/auto_loop.py stop --reason "<原因>"
```

默认使用紧凑输出；只有诊断 manifest、dirty、漂移、依赖链或决策详情时加 `--verbose`。`retryable` 不是终态，由 agent 按对应通道在同一 outstanding action 内立即自纠；`completed_with_blocked` 才是本次 run 的可审计终态，后续恢复由用户显式调用 `retry-blocked`。

## Run 收尾交接

队列到达终态后必须根据 `next`、`record` 或 `status` 的摘要报告真实结果：

- `completed_tasks`：逐项报告 commit 与 `close_result`；`closed` 无额外收尾动作，`blocked` 必须连同 `close_blockers` 交接。
- `blocked_tasks`：报告阻塞原因与可恢复入口，不把 run 终态说成全部成功。
- `parent_tasks_outside_queue`：仅说明未纳入本次队列的父任务；父任务仍按自身范围和验收条件独立推进。

run 期间新建的后补子任务不在冻结队列内，runner 不追踪；发现时按普通任务单独推进，不得手改 runtime 塞进当前 run。物理 GC 不属于 run 收尾。

## 禁止事项

- 不手写 `.trellis/.runtime/auto-loop/*.json`，不提交 runtime 或 `.route-prefs.tmp`。
- 不覆盖、暂存或提交 protected-retained 文件；发生路径冲突只阻塞涉及任务。
- 不用 `start --force` 代替 `retry-blocked`。
- `record` 返回 `retryable` 后不得调用 `next` 或重新发起 action。
- 不忽略 `close_result`：只有 `closed` 才表示确定性 Close 成功，`blocked` 必须保留结构化阻塞项。
- 不在 run 收尾执行物理 GC，也不为已关闭任务制造额外收尾命令。
- 不在无人值守执行中替用户回答 Open Questions。
