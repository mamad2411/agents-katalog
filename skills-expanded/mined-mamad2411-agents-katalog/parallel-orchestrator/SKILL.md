---
name: parallel-orchestrator
pack: universal
description: 主 session 拿到 task-decomposer 的 DAG 后,执行 fan-out → fan-in → 整合回路。使用 Codex 可用的并行子 agent 或多 worktree 调度方式。
when_to_use: decomposition.json 写好且用户确认后,主 session 走到"现在实施"那一步。
when_NOT_to_use: 单任务或没有并行子任务——直接走 implementer。
---

# Skill: Parallel Orchestrator

> 你(主 session)是指挥官。不要自己写代码。实施靠 `subtask-implementer`,整合靠 `merger`。
> 你的责任是正确地 fan-out / 等待 / fan-in / 决定下一轮。

## 持续推进原则

- 小步实现、测试先行、每步可验证,不等于每步都停下来等人。
- fan-out 后,各子 session 应持续开发到自己的 `verifies` 通过或遇到明确 blocker。
- 如果某个子 session 需要人工决断,只把这个子 session 标记为 `blocked`,记录 blocker 和需要人判断的问题;**不要取消或暂停同轮其它无 blocker 的子 session**。
- 主 session 继续收集其它子任务结果。只有全局方向受影响(共享契约冲突、无法自动 merge、整体验收策略需要改)时,才让主 session 停下来请求人工判断。

## 主循环

```python
dag = read_json("state/orchestration/<task-id>/decomposition.json")

for round in dag.rounds:
    round_dir = f"state/orchestration/<task-id>/round-{round.round}/"
    mkdir(round_dir)

    for sub in round.subtasks:
        write(f"{round_dir}/{sub.id}.task.md", render_architect_task(sub))

    if round.parallel:
        results = run_subtasks_in_parallel([
            {
                "agent": "subtask-implementer",
                "description": sub.id,
                "prompt": load(f"{round_dir}/{sub.id}.task.md"),
                "isolation": "worktree"
            }
            for sub in round.subtasks
        ])
    else:
        results = [
            run_subtask({
                "agent": "subtask-implementer",
                "description": sub.id,
                "prompt": load(f"{round_dir}/{sub.id}.task.md"),
                "isolation": "worktree"
            })
            for sub in round.subtasks
        ]

    for sub, res in zip(round.subtasks, results):
        write(f"{round_dir}/{sub.id}.result.md", res)

    blocked = [res for res in results if res.status == "blocked"]
    done = [res for res in results if res.status == "done"]

    # 局部 blocked 不取消其它子任务;已完成的仍然进入 fan-in 记录。
    if blocked:
        write(f"{round_dir}/blocked-report.md", summarize_blockers(blocked))

    merge_report = run_subtask({
        "agent": "merger",
        "description": f"integrate-round-{round.round}",
        "prompt": build_merger_prompt(round_dir, done)
    })

    if merge_report.has_conflicts:
        ask_user(merge_report.conflicts)
        break

    write(f"{round_dir}/round-report.md", merge_report)

write(f"state/orchestration/<task-id>/final-state.json", aggregated_state)
```

## Codex 并行方式

- 如果当前 Codex 环境提供多 agent / sub-agent 工具,在**同一轮**一次性派发所有独立子任务,等待全部返回后再整合。
- 如果当前环境没有原生多 agent 工具,用 `scripts/spawn_agent_worktree.sh <sub-id> <command...>` 为每个子任务建立隔离 worktree,再并行运行命令。
- 不管用哪种执行器,每个子任务都必须有独立 worktree 或等价隔离,否则多个写码 agent 会互相踩 git 状态、端口、数据库和锁文件。

正确(并行):

```text
同一轮一次性派发:
- subtask-implementer: oauth-google
- subtask-implementer: oauth-github
- subtask-implementer: oauth-microsoft
```

错误(串行):

```text
先等 oauth-google 完成,再派 oauth-github,再派 oauth-microsoft。
```

## sub-task 任务包格式

```markdown
# Sub-task: <id>

## 上下文
你是 N 个并行子 agent 之一,跑在 git worktree 隔离里。
父任务:<原始需求>
本子任务在 DAG 里的位置:Round <N>,与 <其他 sub-id> 并行。

## 你的 scope(只能动这些)
<sub.scope>

## 严禁触及(其他并行任务在改)
<sub.no_touch 列表>

## 验收
<sub.verifies>
做完跑这条命令,绿了再返回。

## 返回格式
返回 JSON:
{
  "status": "done" | "blocked" | "failed",
  "changed_files": [],
  "test_output": "",
  "blockers": [],
  "summary": "一句话:做了什么"
}
```

## merger 输入格式

```markdown
# Merger 任务

## 上下文
Round <N> 的 <K> 个并行子任务已完成。请整合并报告。

## 子任务产出
<sub-1.result.md 内容>
<sub-2.result.md 内容>

## 你的工作
1. cd 到主 worktree 或集成 worktree。
2. 按顺序 git merge 每个 sub 分支。
3. 每次 merge 后跑一次指定验证。
4. 任意 merge 冲突 / 测试 fail -> 立即 STOP,报告给主 session,不要尝试自动解。
5. 已标记 `blocked` 的子任务不要强行 merge;把 blocker 写进 round-report,等待主 session/人工决断。
6. 全部 OK -> 写 round-report.md 汇总,返回 has_conflicts=false。

## 严禁
- 修改任何业务代码。merger 只整合,不写。
- 跳过测试后声称 "应该没问题"。
```

## fan-out 前清单

- [ ] 每个 sub-task 都有清晰 scope + no_touch。
- [ ] 每个 sub-task 都有客观 verifies 命令。
- [ ] 本轮并行总数 < 5。超过 5 个,先拆轮。
- [ ] 用户已确认 decomposition.json。

任一不满足,回到 task-decomposer,不要硬上 fan-out。

## 反模式

- N 个 sub-agent 没有 worktree 隔离。
- 派发后用消息 1/2/3 串行调用。
- 一个子任务 blocked 就取消整轮其它子任务。
- merger 擅自修冲突。
- 同一文件被多个 sub.scope 包含。

## 反递归保护

- `subtask-implementer` 不允许再调用子 agent。
- 真有"子任务还能再分解"的情况,回主 session 决定是否加新轮。
