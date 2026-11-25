---
name: using-wakita
description: 任务分级与子智能体调度规范。先查 spec → 分级 → 思考（是否开启头脑风暴） → 写 spec → Plan → builder → auditor → 标记完成。禁止未经分级直接开干。
user-invocable: True
---

<SUBAGENT-STOP>
如果你是作为子智能体被派出来执行某个具体任务，跳过本 skill。
</SUBAGENT-STOP>

# Using Wakita

## 角色

| 角色 | 职责 |
|------|------|
| **MasterAgent（你）** | 架构决策、spec 编写、Plan 制定、小任务直接执行 |
| **wakita-scout** | 只读探索代码结构，输出文件:行号报告 |
| **wakita-builder** | 按 Spec/Plan 严格实现 + 自验证，不决策 |
| **wakita-auditor** | 对照规范审查代码，输出文件:行号问题清单 |

**两条线**：spec（`docs/specs/`，留档） + plan（EnterPlanMode，一次性执行文件）。

**高风险集合**：安全、认证、支付、DB Schema、数据模型、对外 API 契约变更 → 触发即 **auditor 强制**，不受任务级别影响。

## 决策树

```
用户需求
  → 查 docs/specs/（先读前30行判断匹配）
  → 分级（三轴合成）
     小 → 直接干
     中/大 → 需求模糊 → brainstorm → 写 spec；需求清晰 → 直接写 spec
  → Plan：大任务必走 EnterPlanMode，中任务可选，小任务不走
  → 执行：小(直接) / 中(scout → MasterAgent实现 → auditor) / 大(scout → builder → auditor)
  → auditor success → 标记完成
```

---

## 第一步：查 spec

```bash
ls docs/specs/
```

**先读前 30 行**（metadata + 摘要 + 背景）判断是否相关，不匹配则跳过。

| spec 状态 | 处理 |
|-----------|------|
| `待实现` + 匹配 | 读技术要点部分 → 进入分级 |
| `开发完成` | 提醒用户。如要修改，开新 spec |
| `废弃` | 询问是否重新启用 |
| 不存在 | 中/大任务后续写 spec，小任务不需要 |

---

## 第二步：分级（三轴合成）

**轴 A — 影响范围（基准级）**：小(1-2文件) / 中(3-5文件,单模块) / 大(6+文件,跨模块,新功能,改数据模型)

**轴 B — 熟悉度（最多调一级）**：本次会话刚写过→降一级 / 从未读过→升一级

**轴 C — 风险度（最多调一级）**：纯UI/文案→降一级 / 改DB Schema/API契约/涉安全支付→升一级

**合成规则**：
1. 以轴 A 定基准级，轴 B、轴 C 各最多调整一级。
2. 多轴冲突时升级优先于降级（取更保守的级别）。
3. 触发高风险集合 → auditor 强制，与最终级别无关。

不确定时**微探**确认（一次 grep 看影响面）。

---

## 第三步：brainstorm（需求模糊时）

判断标准：「做一个导出功能」→ 模糊，需要 brainstorm；「给订单表加 status 字段(pending/processing/done)」→ 清晰，跳过。

加载 `brainstorm` skill 发散讨论。讨论留在上下文，不写盘。

---

## 第四步：写入 spec

输出到 `docs/specs/<feature-name>.md`，正文 **≤ 120 行**。前 30 行必须含 metadata + 摘要 + 背景。

````markdown
# <功能名称>

**日期**: YYYY-MM-DD
**状态**: 待实现
**关联**: （无则省略）

## 摘要
（3-5行：做什么、为什么、怎么做。快速扫描入口。）

## 背景与目标
- 问题 / 用户 / 成功标准

## 方案
- 选定的方案及理由、关键架构决策
- （ASCII 架构图，如有）

## 技术要点 ★
（spec → Plan 的桥接层，builder 执行的依据）

### 涉及文件
- `path/to/file.go:120-150` — 说明
- `path/to/new_file.go` — 新增，说明

### 数据结构
```go
type XxxRequest struct { ... }
```

### 关键约束
- 超时/编码/并发/兼容性 等硬性要求
- 每条约 1 行

## 备选方案
| 方案 | 优势 | 劣势 | 落选原因 |
|------|------|------|----------|

## 影响范围
- 涉及模块 / 风险 / 依赖

## 待确认
- [ ] 待确认项
````

---

## 第五步：Plan（EnterPlanMode）

大任务必须走，中任务可选，小任务不需要。

Plan 内容：改动文件+行号、每步实现目标、验证命令。一次性文件，执行完丢弃。

---

## 第六步：执行

| 级别 | 流程 |
|------|------|
| **小** | MasterAgent直接 Read/Edit/Write → 自检。触发高风险集合 → 至少过 auditor |
| **中** | scout 探索 → MasterAgent实现 → auditor 审查 |
| **大** | scout 探索 → builder 按 Plan 实现+自验证 → auditor 审查 |

builder **不决策**。Plan/spec 有问题它报告，MasterAgent决策后修正。

---

## 第七步：标记完成

auditor `success` 后：
- **有 spec**：Edit spec 文件，`**状态**: 待实现` → `**状态**: 开发完成`，追加 `**完成日期**: YYYY-MM-DD`
- **无 spec**（小任务触发高风险集合的情形）：向用户汇报验证结论即可；若改动后续可能被复用/追溯，升级为中任务补最小 spec

---

## 子智能体调用

```markdown
派 wakita-scout 探索 xxx，定位相关文件+调用链，输出带文件:行号的报告

派 wakita-builder 按以下 Plan 实现：
[改动文件/行号/目标代码/验证命令]

派 wakita-auditor 审查最近改动，对照项目规范
```

---

## 结果回传协议

子智能体末尾必须附「结果回传」，模板：

```
**状态**: success | partial | failed
**摘要**: 1-2行结论
**位置**: 文件:行号（改动/问题定位，无则省略）
**阻塞项**: （partial/failed 必填）
**根因**: （failed 必填）
**下一步建议**: （partial/failed 必填）
**误报**: true | false（仅 auditor）
```

MasterAgent必须读 `状态` 字段：

| 状态 | 处理 |
|------|------|
| `success` | 推进下一步（auditor success → 标记完成） |
| `partial` | **不得当 success**。读阻塞项和下一步建议，决定补派或人工介入 |
| `failed` | 读根因，解决阻塞项后重派，不得同样方式重试 |

---

## 硬约束

1. **先查 spec 再动手**。已有 spec 则对齐。
2. **先分级，不跳步**。不确定时微探。
3. **中/大任务写 spec**。无 spec 不写代码。
4. **大任务走 Plan**。不跳 EnterPlanMode。
5. **auditor 通过必须标记完成**：有 spec 标 spec，无 spec 记验证结论。
6. **auditor 发现的问题必须修**。除非 auditor 标记误报。
7. **builder 不决策**。Plan 有问题它报告，MasterAgent决策。
8. **高风险集合 → auditor 强制**，不管什么级别。

**常见借口**：「小改动直接改」→ 不熟的文件先微探 / 「Plan 太麻烦」→ 中/大任务没 Plan 容易跑偏 / 「不用写 spec，代码就是文档」→ 三个月后自己也看不懂。

---

## 模型切换

派子智能体前，先检测 `~/.zcode/agents/` 下是否已生成三个 agent 文件（wakita-scout / wakita-builder / wakita-auditor）。**未生成时提醒用户先运行 `/subagent-create` 交互式生成，不要直接调度**（会提示 agent 不存在）。后续切换模型/思考强度（thoughtLevel）也用 `/subagent-create`。写入后需重开会话生效。

## Codex 环境

在 **Codex**（桌面 App / CLI）下运行本工作流时，ZCode 的 `/subagent-create` 与 `~/.zcode/agents/` **不适用**（协议不兼容，原因见 `docs/codex-子智能体方案.md`）。改用：

1. **首次生成**：运行 `python plugins/wakita-governance/scripts/inject-codex-agents.py --apply`，把 scout/builder/auditor 渲染为 `~/.codex/agents/wakita-*.toml`（Codex 原生 TOML agent），并安装命令提示词到 `~/.codex/prompts/`。
2. **调遣方式**：对话中 `@wakita-scout` / `@wakita-builder` / `@wakita-auditor`，或用 Codex 的 spawn/multi-agent 工具按同样角色提示派发；**分级与调度流程不变**（小→直接干，中→scout→MasterAgent 实现→auditor，大→scout→builder→auditor）。
3. **命令等价物**：Codex CLI 中 `/wakita-subagent-create`（生成/切换）、`/wakita-audit`（审计日志）、`/wakita-lock`（保护清单）为 ZCode 版命令的替代提示词。
   - ⚠️ 官方已标记自定义提示词 deprecated，且只在 Codex CLI / IDE 扩展中显示；**桌面 App 不显示 `/wakita-*`**，直接用自然语言让主智能体执行对应脚本，或调遣 `@wakita-*` agent。
4. **hooks 现状**：Codex 经插件 `hooks.json` 加载本插件的 PreToolUse/PostToolUse/UserPromptSubmit（首次需在 Codex 中信任，见 `~/.codex/config.toml` 的 `[hooks.state]`）。危险拦截/审计留痕/规范注入在 Codex 下**同样生效**；但运行数据（`audit.log`、`rules.protected.json`）写入**插件缓存副本**（`~/.codex/plugins/cache/wakita-plugins/wakita-governance/<版本>/hooks/`），`/wakita-audit`、`/wakita-lock` 提示词已按此路径读写。

---

## 验证工具

| 类型 | 工具 | 谁跑 |
|------|------|------|
| 只报错不改文件 | `pytest` `mypy` `npm run build` `eslint` | builder |
| 会改文件 | `black` `isort` `prettier` | 仅 MasterAgent |
