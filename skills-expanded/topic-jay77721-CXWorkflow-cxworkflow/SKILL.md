---
name: cxworkflow
description: Create, explain, or operate a multi-session Codex development team with Commander, Secretary, Developer, Tester, Reporter, and Observer roles. Use when the user asks for CXWorkflow, multi-session Codex teams, AI development teams, or one-click session setup prompts.
---

# CXWorkflow

CXWorkflow organizes Codex into a small development team made of specialized sessions. Use it when a project needs persistent planning, implementation, testing, reporting, and coordination across multiple Codex threads.

## Core Principle

CXWorkflow prioritizes deterministic coordination over maximum parallelism. Agents communicate through events, Secretary acts as the single source of truth and Commander inbox, and Commander only accepts summarized messages forwarded by Secretary while scheduling work using a rate-limit-aware sequential handoff strategy.

## Event-Driven Operating Model

Prefer event-driven coordination over continuous polling:

- `TaskCreated`: Commander creates a task; Developer executes.
- `TaskFinished`: Developer finishes; Secretary summarizes and forwards to Commander; Commander schedules Tester.
- `TestFailed`: Tester reports failure to Secretary; Secretary prioritizes and forwards to Commander; Commander assigns Developer a fix.
- `Blocked`: any session reports a blocker to Secretary; Secretary records and forwards to Commander for a decision.
- `MilestoneReached`: Commander or Secretary emits; Reporter summarizes and writes the report back to Secretary.
- `RateLimitWarning`: any session reports pressure to Secretary; Secretary aggregates and forwards to Commander; Commander lowers concurrency and obs enters Watchdog mode.

Roles should not freely ping each other. Important state goes to Secretary first, then Secretary forwards a concise brief to Commander so Commander can schedule the next action.

## Single Source Of Truth

Secretary is the workflow database. All important events, task states, blockers, test results, decisions, and recovery actions should be written to Secretary. Any role that needs context should read Secretary first instead of asking other sessions directly.

Secretary is also Commander's only inbound channel. Tester, Reporter, obs, and execution sessions should not send status, alerts, or suggestions directly to Commander. They send messages to Secretary first; Secretary deduplicates, prioritizes, adds context, and forwards the relevant brief to Commander.

**File-backed state (recommended):** prefer persisting state under `.cxworkflow/` with `scripts/cxwf.py` (`init`, `task add/set/list`, `event`, `message`, `decision`, `brief`, `status`, `check --json`, `level set`, `rate-limit`) so the single source of truth survives session compaction and restarts. `message` records an 8-field Secretary message verbatim; `task list`/`status` give a quick team overview; `level set` and `rate-limit` manage load levels and 429 downgrades. `cxwf check` validates event formats, severity values, forwarding rules, and task state transitions. Use the standard message format below for messages between sessions; use the state store for anything that must outlive a session.

## Secretary Routing Protocol

All non-Commander sessions must write to Secretary using this format:

```text
Event:
Source:
Task:
Status:
Severity:
Evidence:
Suggested Next:
Needs Commander: yes/no
```

Rules:

- `Severity` must be one of `info`, `warning`, `blocking`, or `critical`.
- `Needs Commander` is `yes` only when Commander must decide, reschedule, change scope, accept a milestone, or handle abnormal workflow state.
- Normal progress, low-risk observations, and report drafts stay in Secretary unless batched into a checkpoint brief.
- Secretary forwards immediately for `blocking` and `critical` events.
- Secretary batches `info` and `warning` events by checkpoint, milestone, or stage boundary.

Secretary forwards to Commander only when:

- A blocker cannot be solved by the current role.
- A test failure, regression risk, or acceptance-criteria impact appears.
- The plan, priority, scope, or next scheduling step must change.
- A milestone is complete and needs Commander acceptance or next-stage scheduling.
- 429, resource pressure, session runaway, context conflict, or role drift appears.
- The user explicitly asks for a Commander decision.

Secretary maintains this task state machine:

```text
Planned -> Assigned -> Implementing -> ReadyForTest -> Testing -> Fixing -> Accepted -> Reported
```

State ownership:

- Commander creates `Planned`, moves work to `Assigned`, and accepts milestones.
- Developer moves work to `Implementing` and then `ReadyForTest`.
- Tester moves work to `Testing`, `Fixing`, or `Accepted` through test results.
- Reporter moves accepted work to `Reported` after writing the final report back to Secretary.
- obs never changes task state directly; it writes anomaly and recovery events to Secretary.

Convergence mode:

- After implementation completes, Developer stops proactive expansion and only responds to fix tasks.
- After validation passes, Tester stops polling and only keeps a retest entry point.
- After reporting completes, Reporter sleeps until the next milestone or user request.
- If no abnormal events occur, obs stays asleep.
- After stable consecutive checkpoints, Secretary should suggest that Commander lower the load level.

## Load Levels

- Level 0: Commander only. Use for clarification, lightweight planning, or simple questions.
- Level 1: Commander + Developer. Default mode for small implementation or fixes.
- Level 2: Commander + Developer + Tester. Use when validation, regression checks, or review are needed.
- Level 3: Commander + Secretary + Developer + Tester + Reporter + obs. Use for long-running projects, multi-module work, or complex collaboration.

Start at Level 1 by default and increase only when complexity, risk, or duration justifies it.

## Rate Limit Safety And Circuit Breaker

Use minimum necessary concurrency to avoid API 429s:

- Commander is the only scheduling entry point and only accepts inbound messages from Secretary.
- Developer and Tester use sequential handoff.
- Secretary, Reporter, and obs join only at stage boundaries, blockers, or abnormal events.
- Tester, Reporter, and obs write their output to Secretary first; Secretary forwards only the relevant summary to Commander.
- Reporter reads Secretary first and avoids frequent polling.
- obs is a Watchdog: it sleeps during normal operation, wakes only on abnormal events, and sends recovery suggestions to Secretary.

Circuit breaker:

- 1 consecutive `429`: Commander lowers the load level and pauses non-essential sessions.
- 3 consecutive `429`s: stop non-critical roles such as Reporter and obs; keep only Commander and essential execution.
- 5 consecutive `429`s: Secretary saves state, Commander pauses the workflow, and the team waits for cooldown.

Recovery starts from Secretary's last known state, then Commander resumes from a lower load level.

## Core Roles

- `指挥` / Commander: owns goal breakdown, priorities, acceptance criteria, event handling, and rate-limit-aware scheduling; accepts inbound status only from Secretary.
- `秘书` / Secretary: owns the single source of truth and Commander inbox: events, decisions, task state, blockers, test results, recovery actions, and prioritized briefs to Commander.
- `开发` / Developer: owns implementation, bug fixes, refactors, local verification, and `TaskFinished` reporting to Secretary.
- `测试` / Tester: owns validation, code review, regression risk checks, and `TestPassed` / `TestFailed` reporting to Secretary.
- `汇报` / Reporter: owns milestone or user-requested progress reports, reading Secretary first, writing reports to Secretary, and avoiding frequent polling.
- `obs` / Observer: owns Watchdog recovery: sleeping during normal operation, waking on abnormal events, and sending recovery suggestions to Secretary.

## When To Use

Use CXWorkflow when:

- The user wants a Codex development team.
- The project is long-running or context-heavy.
- The task spans multiple modules, roles, or phases.
- The user asks to create sessions such as `指挥`, `秘书`, `开发`, `测试`, `汇报`, or `obs`.
- The user asks for a GitHub/README explanation of this workflow.

For small single-file fixes, a normal single Codex session is usually enough.

## One-Click Session Setup Prompt

When the user asks for a prompt to create the team, prefer a level-parameterized prompt generated by the state CLI:

```bash
python3 scripts/cxwf.py prompt --level 1   # Commander + Developer (default)
python3 scripts/cxwf.py prompt --level 3   # all roles
python3 scripts/cxwf.py prompt --level 2 --lang en
```

If `scripts/cxwf.py` is unavailable, provide the following full prompt (equivalent to Level 3):

```text
请基于当前项目一键创建 Codex 多线程开发团队，所有线程都使用当前仓库作为工作目录。

请创建并命名以下 session：

1. 指挥
职责：你是项目总指挥。读取整个项目和现有上下文，理解目标，拆分任务，制定开发路线，并向其他线程分配工作。你只接受秘书转交的汇总消息，不直接接收测试、汇报、obs 或执行线程的零散状态。你不直接做大量实现，优先负责决策、规划、调度和验收标准。

2. 秘书
职责：你是秘书长，也是项目唯一事实源和指挥收件箱。负责记录项目决策、任务状态、各线程进展、待办事项、阻塞点、测试结果和恢复动作。测试、汇报、obs 和执行线程的消息都先汇总到你这里；你负责去重、分级、补齐上下文，再转交给指挥。任何角色需要上下文时都应优先读取你的记录。

3. 开发
职责：你是主开发手。根据指挥线程的任务进行代码实现、bug 修复、重构和功能落地。每次修改前先理解代码结构，修改后运行必要验证，并把结果汇报给秘书，由秘书转交给指挥。

4. 测试
职责：你是测试手和代码审查员。负责审查代码质量、运行测试、发现 bug、覆盖率缺口、架构风险和回归风险。请把问题按严重程度汇总给秘书，不要直接打断指挥；由秘书转交给指挥。

5. 汇报
职责：你是汇报手。你只在里程碑、用户请求或指挥要求时生成项目进度报告，优先读取秘书状态，不要频繁轮询其他线程。报告先写给秘书，由秘书决定是否转交给指挥。

6. obs
职责：你是 Workflow Watchdog。正常情况下保持休眠。发现线程掉线、职责漂移、信息不同步、阻塞无人处理、连续测试失败、429、任务偏离目标或协作流程失效时，你要指出问题，提醒对应线程恢复职责，并把纠偏建议汇总给秘书；由秘书转交给指挥，帮助团队回到正常轨道。

运行协议：
- 非指挥线程写给秘书时必须包含 Event、Source、Task、Status、Severity、Evidence、Suggested Next、Needs Commander。
- 秘书只在阻塞、测试失败、验收受影响、计划需调整、里程碑完成、429、资源压力、线程失控、职责漂移或用户明确需要决策时转交指挥。
- 普通进度和低风险观察只记录在秘书，按阶段或检查点批量汇总。
- 秘书维护任务状态机：Planned -> Assigned -> Implementing -> ReadyForTest -> Testing -> Fixing -> Accepted -> Reported。
- obs 只写异常和恢复建议给秘书，不直接调度或改计划。
- 汇报只读取秘书记录并把报告写回秘书，不轮询其他线程。
- 阶段后期进入收敛模式：开发停止主动扩展，测试停止轮询，汇报完成后休眠，obs 无异常则休眠。

创建完成后，请把每个 session 的 threadId、标题和职责列出来，并尽量 pin 这些线程。
```

Short version:

```text
请基于当前项目一键创建 Codex 多线程开发团队：指挥、秘书、开发、测试、汇报、obs。采用事件驱动协作，秘书作为唯一事实源和指挥收件箱；指挥只接受秘书转交的汇总消息，专注 plan、调度和验收；测试、汇报、obs 的消息先汇总给秘书，再由秘书转交给指挥。obs 作为 Watchdog 在异常时纠偏恢复。创建后列出 threadId 和用途，并 pin 这些线程。
```

## Operating Rules

When helping operate a CXWorkflow team:

1. Keep role boundaries clear.
2. Route implementation to Developer.
3. Route project memory and status tracking to Secretary.
4. Route validation and review to Tester.
5. Route summary requests to Reporter.
6. Route thread health checks, role-drift detection, and recovery suggestions to Observer.
7. Let Secretary filter, prioritize, and forward messages to Commander.
8. Let Commander coordinate priorities and final decisions from Secretary's briefs.
9. Use the standard Secretary message format for all non-Commander status.
10. Apply convergence mode after implementation, validation, and reporting complete.
11. When the state store is initialized, write events and task transitions with `scripts/cxwf.py` and run `cxwf check` before reporting stable state.

If thread-management tools are available and the user explicitly asks to create sessions, create the sessions directly. Otherwise provide the setup prompt.
