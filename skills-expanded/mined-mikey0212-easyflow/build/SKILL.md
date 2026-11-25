---
name: build
description: "用户触发 /ezfl:build 或要求实施 / 执行 tasks.md 时必须使用本 skill。选定 implementer subagent，由该 subagent 在自己的会话内执行 /opsx:apply——主代理禁止直接编写实现代码。"
---

# build

<HARD-GATE>
禁止主代理在自己会话内直接编写实现代码。禁止在 Step 1（通过 easy-flow:agent-selector 完成 Agent Selection）之前调用 /opsx:apply。/opsx:apply 必须由 implementer subagent 执行，而非主代理；subagent 启动 prompt 中必须注入 Constitution C 约束。
</HARD-GATE>

**启动时必须先输出**：`[easy-flow] 进入阶段: build — 使用 easy-flow:build skill。`

## 遵守的 Hard Stops

本 skill 遵守 `hard-stops.md` 中的：
- **H8**（状态行输出）：每个 Step 入口输出 `[easy-flow] 进入 build Step <N>: <动作>` 等可见状态行
- **H10**（agent-selector 前置）：Step 1 必须先调 `easy-flow:agent-selector`，启动 implementer subagent 前不得跳过 Agent Selection
- **H13**（禁用 superpowers 派发驱动器）：Step 1 返回 `"inline"` 时必须由主代理 inline 跑 `/opsx:apply`,绝不回退到 `superpowers:subagent-driven-development` / `:executing-plans`

## 流程

按以下顺序**逐步**执行，每一步未完成不得进入下一步：

### Step 0：定位 change_id

读取 `.harness/workflow.yaml: active_changes`，筛选 `phase=build` 的 entry：
- **唯一匹配**：取其 `change_id`
- **多个匹配**：用 `ask_followup_question` 让用户选择
- **零匹配**：阻断，提示"未找到 design 阶段的 active change，请先执行 /ezfl:design"

### Step 1：Agent Selection — implementer（必经，不得跳过）

**【硬约束】** 在启动 implementer subagent 之前，**必须**先：

1. `use_skill("easy-flow:agent-selector")`
2. 输入 `dispatch_point_id = "build.implementer"`
3. 等待返回三态之一(见 selector SKILL.md "输出"节):
   - **agent 文件路径(string)** — 用户从扫描结果中选定一个项目级 agent
   - **`"default-subagent"`** — 用户选 D,主代理用宿主原生 subagent 能力派发,不指定 agent 文件
   - **`"inline"`** — 用户选 I 或取消,主代理在自己会话内 inline 执行,不派发 subagent

返回值用于本次 build 的 implementer 派发(见 Step 2):

- 返回 agent 路径 → 主代理用宿主原生 Task / AgentTool,以该路径作为 `subagent_path` 派发
- 返回 `"default-subagent"` → 主代理用宿主原生 subagent 能力派发,不指定 agent 文件
- 返回 `"inline"` → 主代理在自己会话内 inline 执行 `/opsx:apply`(注入点 C 由主代理负责)
- 宿主无 subagent 能力 → **强制退化为 `"inline"`**:跳过 Step 2 的 subagent 启动,直接由主代理执行 `/opsx:apply`

跳过自检：若即将启动 implementer / 调用 `/opsx:apply` / 派发实施 subagent / 主代理直接编写实现代码而 Step 1 未完成，立刻停下输出 `[easy-flow] 阻断：build 阶段启动 implementer / 调用 /opsx:apply 之前必须先调用 easy-flow:agent-selector（dispatch_point_id=build.implementer），不得跳过 Agent Selection。` 后回到 Step 1。

### Step 2：按 selector 三态分支执行 `/opsx:apply`

**组装启动 prompt**：`read_file $PLUGIN_ROOT/skills/build/assets/implementer-prompt.md` 取 prompt 模板原文（含三段：任务 / Constitution 注入点 C / 返回契约），把模板中的占位符 `<change_id 或省略>` 用 Step 0 定位结果替换（trivial 路径下保持 `<省略>` 含义即整个方括号删掉，让 apply 自行推断）；其它 `<N.M>` / `<...>` 等占位符是 subagent 运行时自填，**保持原样**不要替换。

按 Step 1 返回值分三个分支:

#### 2.A — 返回 agent 文件路径(string)

主代理通过宿主原生 Task / AgentTool 派发 subagent:
- `subagent_path` = Step 1 返回的 agent 路径
- `prompt` = 上一步组装的启动 prompt

主代理在 subagent 运行期间**不得干预**,只接收最终汇报。

#### 2.B — 返回 `"default-subagent"`

主代理通过宿主原生 Task / AgentTool 派发 subagent,**不指定 `subagent_path`**(由宿主默认 subagent 接管):
- `prompt` = 上一步组装的启动 prompt

主代理在 subagent 运行期间**不得干预**,只接收最终汇报。

#### 2.C — 返回 `"inline"`(主代理 inline 执行)

主代理在自己的会话内执行 — 不派发任何 subagent:
1. 先输出本次 build 适用的 Constitution 原则清单(注入点 C 的 inline 形态);
2. 调用 `/opsx:apply [<change_id>]`,等待完成;
3. apply 内每个 task 实施前由主代理输出 `[Constitution C] Task <N.M>: 适用原则 = ...`(注入点 C 的强制条款,主代理自负其责)。

### Step 3：出口校验

`/opsx:apply` 返回（或 subagent 返回汇报）后，校验：

1. `tasks.md` 中所有任务 checkbox 已勾选完成（`- [x]`）——**存在任何 `- [ ]` 即视为未完成**
2. apply 输出 `Implementation Complete` 摘要（参考 `apply-change.ts` 输出格式）
3. 主代理未直接编写实现代码（违反 Step 1 跳过自检即视为流程失败）

**硬阻断(任一项不满足 → 禁止标记 build.status=completed)**:

- 校验 1 不通过(有 `- [ ]`) → **阻断**,输出 `[easy-flow] 阻断：tasks.md 存在未完成任务,禁止标记 build 完成。` + 列出未完成 task 编号,等待用户指示(继续实施 / 手动标记 / 放弃)
- 校验 2 不通过(apply paused/errored) → **阻断**,呈现 pause 原因与可选项,等待用户指示
- 校验 3 不通过 → **阻断**,流程视为失败
- **全部通过** → 提交 worktree 内改动后标记完成:

```bash
cd "$WORKTREE_PATH"
git add -A && git commit -m "feat($change_id): implementation complete"
```

写 `build.status: completed` 到 state.yaml,输出 `[easy-flow] build 完成，下一步建议执行 /ezfl:audit`

## Constitution 注入点 C

- 由 implementer subagent(2.A / 2.B 分支)在执行每个 task 前输出 `[Constitution C] Task <N.M>: 适用原则 = ...`
- 主代理在 Step 2 组装 prompt 时把本约束作为强制条款注入 subagent 启动 prompt
- 走 2.C 主代理 inline 时,由主代理在执行 apply 前一次性输出本次 build 的原则清单作为 inline 形态,并在每个 task 前补输 `[Constitution C] Task <N.M>: ...`
