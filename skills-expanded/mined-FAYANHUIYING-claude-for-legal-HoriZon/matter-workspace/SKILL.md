---
name: matter-workspace
description: >
  管理事项工作区——新建、列表、切换、关闭或脱离（实务级）。使一个客户或委托的
  上下文与其他所有客户隔离。当多客户执业者说"新建事项""切换事项""列出事项"
  "关闭事项"，或其他技能需要知道当前在哪个事项中工作时使用。
argument-hint: "<new | list | switch | close | none> [slug]"
---

# /matter-workspace

执业者跨多个客户与事项工作。事项工作区使一个客户或委托的上下文与其他所有客户、委托相互隔离。本技能管理这些工作区。

## 子命令

- `/ip-legal:matter-workspace new <slug>` —— 新建事项，运行简短立项登记，写入 `matter.md`
- `/ip-legal:matter-workspace list` —— 列出事项及状态，标记活跃事项
- `/ip-legal:matter-workspace switch <slug>` —— 设定当前活跃事项
- `/ip-legal:matter-workspace close <slug>` —— 归档（移至 `matters/_archived/`，绝不删除）
- `/ip-legal:matter-workspace none` —— 脱离活跃事项，仅在实务级上下文工作

## 操作指引

1. 读取 `~/.claude/plugins/config/claude-for-legal-horizon/ip-legal/CLAUDE.md`，确认 `## 事项工作区` 已填充。若 `启用` 为 `✗`：告诉用户"事项工作区已关闭——单客户/内部法务场景自动以实务级上下文工作。若你实际跨多个客户执业，重跑 `/ip-legal:cold-start-interview --redo` 并选择私人执业设置。" 不要报错——关闭是预期状态。
2. 按 `$ARGUMENTS` 首词分派：
   - `new` → 立项登记访谈，写 `~/.claude/plugins/config/claude-for-legal-horizon/ip-legal/matters/<slug>/matter.md`，初始化 `history.md` 与 `notes.md`
   - `list` → 枚举 `matters/*/matter.md`，打表，`*` 标活跃；`_archived/*` 单列
   - `switch` → 更新实务级 CLAUDE.md 的 `当前事项：` 行（唯一权威来源，无单独状态文件）
   - `close` → `history.md` 记关闭日期，移至 `_archived/<slug>/`；若关的是活跃事项，`当前事项：` 设回 `无`
   - `none` → `当前事项：` 设为 `无 —— 仅实务级上下文`
3. 写入前向用户展示将要变更的内容并确认。

## 存储布局

```
~/.claude/plugins/config/claude-for-legal-horizon/ip-legal/
├── CLAUDE.md                       # 实务级实务画像
└── matters/
    ├── <slug>/
    │   ├── matter.md               # 客户、相对方、事项类型、关键事实、覆盖项
    │   ├── history.md              # 带日期的事件日志（仅追加，最新在上）
    │   ├── notes.md                # 自由格式工作笔记
    │   └── outputs/                # 本事项的技能输出
    └── _archived/<slug>/           # 已关闭事项——可读但非活跃
```

slug 用小写加连字符。示例：`acme-shangbiao-qinquan`（商标侵权分析）、`zenith-fto`（专利 FTO）。

## `new <slug>` 立项登记

1. 确认 slug 在活跃与归档中均不存在；重复则请另选。
2. 登记访谈：
   - **客户**（我方代理的一方）与**相对方**
   - **事项类型**：商标 | 专利/FTO | 著作权 | 商业秘密 | 侵权分析 | 其他
   - **保密级别**（标准 | 加强 | 隔离团队）
   - **关键事实**（2-5 句：涉及什么、利益方是谁、争点何在）
   - **事项特定覆盖项**（偏离实务级画像之处，例如「本客户为被诉方——分析以不侵权抗辩与无效路径优先」）
   - **关联事项**（相关 slug）
3. 写入 `matter.md`（含工作成果页眉，按 `## 使用者角色` 选择）；初始化 `history.md`（一条"立项"记录）与空 `notes.md`。
4. **不要**自动切换。问："要现在切换到 `<slug>` 吗？"

## 跨事项上下文

实务级 CLAUDE.md 的 `跨事项上下文：` 开关为 `关闭`（默认）时，在事项 A 工作的技能对事项 B 的文件**绝不读取**，绝无例外。一个客户的技术方案、申请策略与侵权弱点绝不能泄入另一个客户——同领域多客户时是利益冲突高发区。

为 `开启` 时，仅在用户明确要求时方可跨事项读取（如"对照过去五个同类事项比较立场"）；即便开启，默认仍只加载活跃事项。

应跨事项沉淀的经验写到实务级 CLAUDE.md，不写到事项文件夹。

## 本技能不做的事

- **不运行利益冲突检查**——那是执业者/律所的职责；立项登记只记录用户申报的内容。
- **不强制留存**——关闭即归档，不删除；留存政策不在本技能范围。
- **不自动路由输出**——实质技能决定写什么；本技能只告诉它哪个文件夹活跃。
