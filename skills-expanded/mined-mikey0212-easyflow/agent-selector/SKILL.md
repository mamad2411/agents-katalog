---
name: agent-selector
description: 在 subagent 派发前扫描项目级 agent 目录、按阶段关键词推荐、让用户选择，结果落盘防腐化
---

# agent-selector

## 调用方契约（必经之路）

**任何派发点 skill 在做 subagent 派发动作之前，必须先 `use_skill("easy-flow:agent-selector")` 并等待返回。**

"派发动作"包括但不限于：

- 通过宿主原生 Task / AgentTool 直接派发 subagent
- 任何"让另一个 LLM context 接手某项工作"的动作

> **全局禁令(HARD STOP H13)**:任何 skill **禁止**调用 `superpowers:subagent-driven-development` 与 `superpowers:executing-plans` 这两个派发驱动器。所有 subagent 派发统一由主代理使用宿主原生 Task / AgentTool 完成,selector 只决定"用哪个 agent 文件 / 走默认 subagent / inline 不派发"三类语义之一。
>
> 注:`superpowers:brainstorming`、`superpowers:test-driven-development` 等被动方法论 skill **不在禁令范围**——它们不派发 subagent,只是给主代理或 subagent 提供检查清单与思路,可继续使用。

**禁止**主代理"觉得需求清晰、selector 多余"就跳过本步——这会剥夺用户对 subagent 选择的可见性与控制权。

### 当前已注册派发点

| dispatch_point_id | 调用方 skill | 用途 |
|---|---|---|
| `design.brainstorm` | `design` | brainstorming subagent |
| `lock.plan-review` | `plan-review` | 主评审 subagent |
| `build.implementer` | `build` | 执行 `/opsx:apply` 的实施 subagent（一次选定，全程复用） |
| `audit.scorer-driver` | `audit`（如适用） | 审计驱动 subagent |

### 跳过自检（违规即停）

派发点 skill 中若即将做派发动作而本 skill 尚未被调用，**必须**立即停止并输出：

> "[easy-flow] 阻断：派发点 `<dispatch_point_id>` 必须先调用 easy-flow:agent-selector，不得跳过 Agent Selection。"

然后回到 Agent Selection 步骤重新走完，再继续派发。

## 调用方式

被派发点 skill 以内嵌指令调用。派发点传入 `dispatch_point_id`（如 `build.implementer`），selector 返回结论。

**关键约束**：每次派发前必须从磁盘重读缓存——禁止依赖主 agent 内存中的"上次选择结果"。

## 输入

| 参数 | 类型 | 说明 |
|---|---|---|
| `dispatch_point_id` | string | 派发点标识符（先 `read_file ./policies/description-keyword-rules.md`） |

## 输出

| 返回值 | 含义 | 调用方应执行 |
|---|---|---|
| agent 文件路径(string,相对 repo 根) | 用户从扫描结果中选定一个项目级 agent | 主代理用宿主原生 Task / AgentTool,以该路径作为 `subagent_path` 派发 subagent |
| `"default-subagent"` | 用户选 D — 不指定 agent 文件 | 主代理用宿主原生 subagent 能力派发,由宿主默认行为接管 |
| `"inline"` | 用户选 I 或取消 / 未识别输入 | 主代理在自己会话内 inline 执行后续命令,不派发任何 subagent |

> **`null` 不是合法返回值。** 禁止在未通过 `ask_followup_question` 展示菜单并收到用户输入的情况下返回任何值。selector 必须弹菜单、等用户选、再返回三态之一。

## 完整流程

```
[1] 读盘：.harness/.cache/sessions/$PPID.id → current_session_id
    - 文件缺失 → 生成临时 session_id 写入 sessions/$PPID.id + 输出警告

[2] 读盘：.harness/.cache/agent-selection.json → cache
    - 文件缺失 / JSON 不可解析 → cache = 空

[3] 比对 cache.session_id 与 current_session_id
    - 不一致 → cache 视为空
    - 一致 → 查 cache.selections[dispatch_point_id]
      - 存在且 remember=true → 校验 agent 文件存在性(若 agent 是路径) → 直接返回
      - 存在但 remember=false → **不复用**,进入完整流程(单次选择不缓存跨调用)
      - 不存在 → 继续

[4] 扫描项目级 agent 目录：

    [4.0] 确定扫描根 main_repo_root（**绝对路径，主仓优先**）：

        ```bash
        main_repo_root="$(git rev-parse --show-toplevel)"
        ```

        `--show-toplevel` 始终返回绝对路径。在 worktree 内返回 worktree 根(`.claude/` 等宿主目录可能不存在——这是预期行为,扫描为空时弹精简菜单)。
        **禁止使用** `dirname "$(git rev-parse --git-common-dir)"`——它在主仓内返回相对路径 `.`,依赖 cwd 正确才能工作。

    [4.1] 扫描以下三个目录（基于 main_repo_root，不基于当前 cwd）：
        - <main_repo_root>/.agents/
        - <main_repo_root>/.codebuddy/agents/
        - <main_repo_root>/.claude/agents/
        三个目录全扫，结果合并去重。跳过无 frontmatter description 字段的文件。

    设计依据：agent 定义是**项目级共享配置**，多个 worktree（即多个 feature 分支）应共享主仓的同一份 agent 定义；且 .claude/ .codebuddy/ 等宿主目录通常不入仓，git worktree 不会复制这些 untracked 目录到新工作树，导致 worktree 内扫描结果为空。

[5] `read_file ./policies/description-keyword-rules.md` 并按 dispatch_point_id 对应的关键词做匹配
    - 命中关键词 → 归入"推荐"组
    - 未命中 → 归入"通用"组
    - **候选总数 = 推荐 + 通用**（即所有扫描到的含 description 的 .md 文件合计,不是"关键词匹配数"）

[6] `read_file ./policies/menu-presentation.md` 并按其展示菜单——**禁止跳过,禁止不弹菜单就返回**
    - 候选 ≥1(有任何 .md 文件被扫描到,无论匹不匹配关键词) → 弹标准菜单(推荐组 + 通用组 + D + I + R),等待用户选择
    - 候选 = 0(三个目录全空 / 全无 .md / 全无 description) → 弹精简菜单(仅 D + I + R)
    - **两种情况都必须通过 ask_followup_question 弹菜单并等待用户输入后才能返回**
    - 用户输入未识别字符 / 空回车 / 取消 → 视同 I,返回 `"inline"`

[7] `read_file ./policies/session-memory-protocol.md` 并按其写回 cache

[8] 返回三态之一:agent 路径(string) / `"default-subagent"` / `"inline"`
```

## 扫描目录（仅项目级）

```
<main_repo_root>/.agents/
<main_repo_root>/.codebuddy/agents/
<main_repo_root>/.claude/agents/
```

`main_repo_root` 解析：`main_repo_root="$(git rev-parse --show-toplevel)"`(绝对路径)。详见 `read_file adapters/agent-directory-probe.md`。

扫描逻辑：列出目录下所有 `*.md` 文件，对每个文件读取前 5 行寻找 `description:` 行（纯文本扫描，不依赖 YAML 解析器）。

## Policies

| Policy | 路径 | 职责 |
|---|---|---|
| 关键词规则 | `./policies/description-keyword-rules.md` | 派发点 → 关键词映射表 |
| 缓存协议 | `./policies/session-memory-protocol.md` | 读/写/失效/兜底完整规则 |
| 菜单展示 | `./policies/menu-presentation.md` | 文案、排序、选项规范 |
