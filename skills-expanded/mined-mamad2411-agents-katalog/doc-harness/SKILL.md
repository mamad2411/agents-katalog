---
name: doc-harness
description: "基于文档的项目控制：让任何 AI 智能体或人仅凭文件即可恢复工作状态——无需外部记忆。当用户需要管理长期项目、跨 session 追踪进度、context 丢失后恢复状态、多智能体协作、审计文档健康、或避免忘记上次做到哪里时使用。触发词包括 '/doc-harness init'、'/doc-harness check' 等斜杠命令，以及『帮我搭建这个项目』『我总是忘』『智能体在 session 之间会忘记』『整理项目文档』『审计这个项目』『上次我们做了什么』等。"
argument-hint: "init [项目名] [描述] | check | sync [--auto] | flush [--auto] | recall [查询] | resume [--auto]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
license: MIT
---

# Doc Harness — 基于文档的项目控制

Doc Harness 让项目仅凭文件即可恢复：任何新 agent 在上下文断裂后，读入口就能正确接手。

每个项目维护：

- **CLAUDE.md** —— 唯一权威入口：AGENT IDENTITY LOCK + 稳定锚（框架锚、铁律、底层原则）+ 操作规则。
- **AGENTS.md** —— 指向 CLAUDE.md 的薄指针（绝不过时复制）。
- **events.log** —— append-only 事件日志：历史与当前状态的**单一来源**。
- **CURRENT_STATUS.md** —— 由 `events.log` **生成的投影**（`## NOW` + 活跃工作面 + 否定台账）；绝不手工编辑。
- **FILE_INDEX.md** —— 文件目录；未注册文件是红项。
- **DOC_HARNESS_SPEC.md** —— 可选的规范参考副本。

可选：`PHILOSOPHY.md`（底层原则）、`PARKING_LOT.md`、`RUNBOOK.md`，以及跨项目 `inbox/`/`outbox/`（可另配 `MAIL_LEDGER.md`）。

核心原则：**接手优先于记录**——新 agent 必须能仅凭文件正确接手。状态变化是一条 `record` 命令；确定性工具带（`tools/`）负责验证文档体系的完整性。

## 如何调用（与 agent 无关）

下面这些命令描述的是**结果**，不是某个平台的专有功能。具体怎么触发，取决于你用的 agent：

| Agent | 怎么调用 |
|-------|---------|
| Claude Code | `/doc-harness check`（插件斜杠命令） |
| Kimi CLI | `/skill:doc-harness` 载入本 skill，然后用自然语言说「检查这个项目的文档健康」 |
| 其它 agent | 自然语言即可——「恢复这个项目」「把文档状态冲刷一下」「当初为什么选 X？」 |

本 skill 不依赖任何 agent 的专有功能：它就是 Markdown，外加一套可选的 PowerShell 工具带。

## 命令

### `/doc-harness init [项目名] [描述]`

为新项目创建文件（干净初始化或中途采纳）。
**→ 见 [init.md](init.md)。**

### `/doc-harness check`

审计健康：投影新鲜度（now_refreshed vs events.log）、未注册文件（红）、入口唯一、`events.log` 良好性、收件箱、操作规则版本、身份锁、超期结论（`conclusion_until`）、来源 class（`class=root|decision|reported`）；然后反思锚与底层原则。
**→ 见 [check.md](check.md)。**

### `/doc-harness sync [--auto]`

修复漂移：注册文件、向 `events.log` 追加缺失的状态事件、重新投影 CURRENT_STATUS、收件箱整理。`interactive`（默认）在状态变更前询问；`auto` 执行安全修复。
**→ 见 [sync.md](sync.md)。**

### `/doc-harness flush [--auto]`

压缩 / session 结束前的紧急保存：先 sync，再**强制**盘点上下文、写入并注册提取项、验证新 agent 能找到、最后**追加状态事件并重新投影**。
**→ 见 [flush.md](flush.md)。**

### `/doc-harness recall [查询]`

检索信息：第 0 层稳定锚 → 第 1 层 `## NOW`/活跃工作面 → 第 2 层 `events.log`（历史）→ 第 3 层 FILE_INDEX → 第 4 层文件。只读、带来源引用。机械 grep 用 `tools/search.ps1`。
**→ 见 [recall.md](recall.md)。**

### `/doc-harness resume [--auto]`

结构化、可验证的接手：身份 → 稳定锚 → 从 `events.log` 读当前状态（并校验新鲜）→ 先读清单 → 否定台账；再出恢复报告 + 5 问验证 + 继续/等待决策。上下文为空或用户说「恢复」时运行。
**→ 见 [resume.md](resume.md)。**

### `/doc-harness`（无参数）

检查目录：核心文件齐全 → 建议 `check`；完全没有 → 建议 `init`；部分存在 → 建议 `init` 中途采纳模式。然后显示本帮助。

## 确定性工具带（`tools/`）

纯 PowerShell、工具无关。关键入口是 `record.ps1`（一步状态变更：追加事件 + 重新投影 + conformance）。其余：`project.ps1`、`search.ps1`、`conformance.ps1`、`now-verify`、`encoding-guard`、`unregistered`、`dead-pointer`、`cite-check`、`stale-check`、`recurrence`、`nested-git-guard`、`stale-writer-guard`、`batch-register`、`telemetry`，以及邮件族（`mail-daemon`、`mail-send`、`mail-poll`、`mail-ledger`）。

**它在哪里**：工具带**就在这个 skill 目录里**（`tools/`，因此任何安装方式——插件市场、`cp -r`、Kimi CLI 复制——都会带上它），仓库根目录另存一份作为规范副本。用法是传 `-ProjectRoot <你的项目>`：

```powershell
powershell -File <本 skill 目录>/tools/record.ps1 -ProjectRoot C:\path\to\your\project -Verb close -Text "T3 evidence=docs/t3.md class=root"
```

它仍然是**可选**的，但值得知道不装它到底会弱在哪两处：(a) 把漂移变成红灯的守卫没有了；(b) 投影只能手写而不是生成——而那恰恰是 v2 想避免的那件事。

## 参考文档

- [init.md](init.md) · [check.md](check.md) · [sync.md](sync.md) · [flush.md](flush.md) · [recall.md](recall.md) · [resume.md](resume.md) · [operational_rules.md](operational_rules.md) · [spec.md](spec.md)（权威）。
