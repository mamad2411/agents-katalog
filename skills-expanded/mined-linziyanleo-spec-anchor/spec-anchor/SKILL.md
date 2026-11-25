---
name: spec-anchor
description: "工程上下文管理技能，服务于含有 anchor.yaml 或 .specanchor/ 的项目。在实质性代码修改、代码审查、Spec/上下文管理、对齐检查、交接、发现记录或沉淀工作前，加载编码标准、模块合约和活跃任务——这些约束在代码本身中看不到。是否加载与改动规模成比例：琐碎/局部改动（typo、注释、日志、格式化）或纯只读机械操作可跳过。当用户提到 spec-anchor、specanchor 脚本、Spec 管理、上下文装配、对齐检查、boot 流程、Assembly Trace 等概念时也应调用本技能。"
allowed-tools:
  - Bash
  - Read
---

<LOADING-GUIDANCE>
Applies only when this project has `anchor.yaml` or `.specanchor/`.
For substantive code changes or reviews that touch spec-governed modules, load SpecAnchor context first — Specs contain constraints not visible in code alone.
Scale loading to task scope using judgment: trivial/localized edits (typos, comments, log lines, formatting) and read-only mechanical operations (grep, find, git log, running tests) do not require SpecAnchor boot.
If the user explicitly mentions spec-anchor or specanchor scripts but the CWD lacks `anchor.yaml`/`.specanchor/`, skip boot but still use this skill's knowledge to assist — read script files via `$SA_SKILL_DIR/scripts/` or locate them with `find`.
</LOADING-GUIDANCE>

# SpecAnchor

> SpecAnchor compiles bounded, auditable, sedimentable engineering context for coding agents. It does not own the agent loop.
>
> SpecAnchor 为 AI coding agent 编译有边界、可审计、可沉淀的工程上下文。它不拥有 agent 执行循环。

Spec 是 cold context 来源之一，代码是船，**Context Bundle 是 SpecAnchor 的核心交付物**。SpecAnchor 把工作记忆显式分为四类产物——Spec / Decision / Evidence / Finding——按 inclusion / budget / freshness / staleness 装配成 Bundle 交给 agent。Agent 在执行中产生的新发现回写为 Finding，经 Sediment Proposal 由人 batch review 后才进入长期 Spec。跨 session 通过 `specanchor_handoff` 导出 handoff packet 重启。

主 `SKILL.md` 只负责入口和 boot；详细协议下沉到 `references/`：

- Context utilities：`references/agents/context-utilities.md`
- Workflow gates：`references/workflow-gates.md`
- Command quickref：`references/commands-quickref.md`
- Reference index：`references/reference-index.md`

## Script Invocation

Skill 脚本位于 Skill 根目录的 `scripts/` 下，运行时必须站在用户项目根目录。

```bash
# $SA_SKILL_DIR = SKILL.md 所在目录
SPECANCHOR_SKILL_DIR="$SA_SKILL_DIR" bash "$SA_SKILL_DIR/scripts/<script-name>.sh" [args]
```

Keep long options as a single shell argument: use `--format=summary`, never `-- format=summary`.

## 工作流程

1. **Boot** — 运行 `specanchor-boot.sh` 加载项目配置、模块结构和活跃任务（详见 Boot Requirement）
2. **输出 Assembly Trace** — Boot 完成后立即输出 Global/Module 加载状态（详见 Assembly Trace）
3. **按需装配** — 深入特定模块时运行 `specanchor-assemble.sh --files=... --intent=...`（详见 Loading Strategy）
4. **执行编码任务** — 基于已加载的 Spec 约束进行代码分析或修改
5. **对齐检查** — 编码完成后对比变更与 Module Spec 契约（详见 Post-Coding Chain）
6. **记录发现** — 若发现新事实、矛盾或漂移，通过 `specanchor-finding.sh` 记录
7. **评估沉淀** — 若发现 Spec 漂移，起草 Sediment Proposal 将热上下文回流为冷 Spec

步骤 1-2 在 session 开始时执行一次；步骤 3-7 在每个编码任务中按需循环。

## Boot Requirement

**当任务需要 SpecAnchor 上下文时，Boot 是第一步——实质性代码分析/修改前先 boot；琐碎或纯只读操作可跳过。** 判定需要后先运行：

```bash
SPECANCHOR_SKILL_DIR="$SA_SKILL_DIR" bash "$SA_SKILL_DIR/scripts/specanchor-boot.sh"
```

- `--format=summary`：人类可读摘要
- `--format=full`：额外附带 Global Spec 正文
- `--format=json`：机器可读 JSON

Boot 完成后立即输出 Assembly Trace（见下节），然后再进入任何代码分析或修改。

**Boot 是 session-start / preflight，同一 session 原则上只运行一次。** 同 session 内后续的上下文需求不要重复 boot——改用 targeted `specanchor-assemble.sh --files=...`（见 Loading Strategy）。

## Assembly Trace

**Boot 完成后必须立即输出 Assembly Trace，格式如下：**

```text
Assembly Trace:
  - Global: summary|full|none|skipped -> <files or reason>
  - Module: full|summary|deferred|sources-only|none -> <files or reason>
```

Assembly Trace 是 boot 的可视确认——没有它，用户无法验证上下文已正确加载。完整规则见 `references/assembly-trace.md`。

## Loading Strategy

- `full`：始终加载 `anchor.yaml` + 全部 Global Spec；Module Spec 按需加载。
- `parasitic`：只加载 `anchor.yaml` 与外部 `sources`；不创建 full-only Spec。
- 需要判断该读哪些模块时，优先看 boot 输出的 `Available Commands:` / `Available Modules:` 段；boot 不可用时 fallback 到 `references/commands-quickref.md`。
- 复杂编码任务应在 boot 之后运行 `specanchor-assemble.sh --files=... --intent=...`，先拿到 bounded read plan，再进入编辑。

## Post-Coding Chain（编码后检查）

**完成实质性代码修改后，依次执行以下检查链（改动规模越大越应完整执行；琐碎/局部改动可按需简化或跳过）：**

1. **对齐检查（Alignment Check）** — 触及 Spec 治理模块的改动应按下述**决策树**挑合适入口执行。verdict tools 与 read-plan tools 分工明确：verdict 走 `check`，read-plan 走 `assemble`。

    | 手上有什么 | 入口 | 说明 |
    |---|---|---|
    | 一组改动文件路径 | `specanchor-check.sh files <path...>` | Post-coding verdict 超集：coverage + module freshness + optional task alignment，输出 `overall: pass\|warning\|fail` |
    | 具体 task spec | `specanchor-check.sh task <spec-file>` 或 `check files <path...> --task-spec=<path>` | 前者判定 committed-diff vs plan；后者做 candidate-only 弱声明 |
    | 只想知道是否被 Module Spec 覆盖 | `specanchor-check.sh coverage <path...>` | 纯覆盖查询（不含 freshness / task diff） |
    | 需要 bounded context bundle | `specanchor-assemble.sh --files=... --intent=...` | **read-plan 工具**，不产 verdict；输出含 `Uncovered Targets` 段列出未覆盖路径 |
    | assemble 超时 / 缺覆盖 | 显式报告 "partial context"，不要伪造 verdict | 缺 module spec 时创建 Task Spec 或跑 `specanchor_infer`，不要凭空发明业务规则 |

    - `check files --format=json` 输出 `specanchor.check.v1` envelope（top-level `schema_version` / `mode` / `status` / `inputs` / `warnings` / `verdict`）。
    - **不要用 assemble 的读文件列表当作 verdict**——它只回答"该读什么"，不回答"是否对齐"。
2. **记录发现（Record Findings）** — 若发现新事实、矛盾、风险或 Spec 漂移，通过以下命令记录：`SPECANCHOR_SKILL_DIR="$SA_SKILL_DIR" bash "$SA_SKILL_DIR/scripts/specanchor-finding.sh" new --topic=<slug> --summary=<单行摘要>`。无新发现则跳过。
3. **评估沉淀（Evaluate Sediment）** — 若发现揭示了 Spec 漂移或缺失约束，起草 Sediment Proposal（`references/concepts/sediment-proposal.md`）将热上下文回流为冷 Spec。无漂移则跳过。

## Error Handling & Exit Conditions

**脚本失败时：**
- Boot 脚本失败（exit ≠ 0）：报告错误信息给用户，不重试超过 2 次。若连续 2 次失败，fallback 到手动读取 `anchor.yaml` + `.specanchor/spec-index.md` 获取最小上下文。
- Assemble 脚本失败：向用户说明失败原因，回退到 boot 输出的 Available Modules 信息，不做超过 3 次重试。

**迭代上限：**
- Post-Coding Chain 的 Alignment Check 若发现不一致，修复后最多再检查 2 轮（共 3 轮）。超过 3 轮仍不通过，停止并报告剩余问题给用户决策。
- Finding 记录和 Sediment Proposal 不做循环——每个发现记录一次即可。

**降级策略：**
- 若 skill 脚本路径不可达（$SA_SKILL_DIR 无效），跳过脚本依赖的步骤，直接读 `.specanchor/` 下的文件作为上下文。
- 若项目无 `anchor.yaml` 且无 `.specanchor/`，skill 不激活——这是预期行为，不视为错误。
