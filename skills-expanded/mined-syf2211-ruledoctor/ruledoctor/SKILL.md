---
name: ruledoctor
description: >-
  Use when the project has rule files (CLAUDE.md, AGENTS.md, .cursorrules, CONTRIBUTING.md,
  .github/copilot-instructions.md, .cursor/rules) or .ruledoctor.json required_reads;
  before git push, deploy, bulk delete, or when context was compacted.
  Read listed rules and required_reads first; refuse violations; re-read after long sessions.
  Default user message: files read + 3 hard constraints only unless user asks for full summary.
---

# RuleDoctor — 项目规则优先

## 三层分工（向用户说明时用）

| 层 | 作用 |
|----|------|
| **本 Skill** | 提醒你先读规则、拒绝违禁操作、压缩后重读（**软约束**） |
| **CLI `ruledoctor`** | 用户要求时，用本地会话日志做**事后核对** |
| **Hook（`ruledoctor setup`）** | 在 **Bash 执行前**硬拦截部分命令；SessionStart/压缩后注入规则摘要；CLI 可用时结束出报告 |

读规则 ≠ 一定遵守。**「必须用中文、要汇报、要写验证」** 靠本 Skill + 项目规则（软约束）；**只有能写成明确 shell 命令规则的危险操作** 才适合 Hook 硬拦。人话说明：[Hook 是什么？](https://github.com/syf2211/ruledoctor/blob/main/docs/Hook是什么.md)

---

## 何时启用

- 存在根规则文件或 `.cursor/rules/`，或 `.ruledoctor.json` 里有 `required_reads`
- 用户要 push、部署、大批量删除
- 用户说上下文被压缩、忘了规则

---

## 规则文件从哪来（不要扫全仓库）

1. **自动认的根文件**（存在则读）：`CLAUDE.md`、`AGENTS.md`、`.cursorrules`、`CONTRIBUTING.md`、`.github/copilot-instructions.md`、`.cursor/rules/*.{md,mdc}`
2. **必读清单**（只读列表里的路径）：项目根 `.ruledoctor.json` → `required_reads` 数组，例如：
   ```json
   "required_reads": ["docs/agent_workflow_protocol.md", "README.md"]
   ```
   `README.md` 只有写进清单才强制 Read，不会默认扫全库。忽略绝对路径、`..` 逃逸和指向项目外的 symlink。

---

## 触发后做什么

### 1. 读取（工具调用）

- Glob/Read：上面「自动认」+ `required_reads` 里每一项（文件必须存在）。

### 2. 对用户的开场（两层输出，避免念经）

**默认只说：**

- 已 Read 的文件名列表（含 `required_reads`）
- **最多 3 条**本场硬约束（一句话一条）

**仅当用户说「展开规则 / 完整摘要 / 列出全部」时**，再发更长摘要。

### 3. 动手前

- 将违反硬约束的命令 → **不执行**，说明**哪一条**、**建议替代**。
- 默认拒绝：`git push` 搭配 `--force` / `-f` / `--force-with-lease`、`rm -rf /`、提交密钥。

### 4. 长对话 / 压缩后

- 重新 Read 规则文件 + `required_reads` 项；默认仍用「文件列表 + 3 条硬约束」汇报。

### 5. 仅当用户要「体检 / 报告」

```bash
ruledoctor --cwd "<项目根>" --last-session
```

若本机没有 `ruledoctor` CLI，不要直接 `npx ruledoctor`；说明 CLI/Hook 是可选增强，并让用户按仓库文档 clone、build 后再运行报告。

---

## 安装

`~/.claude/skills/ruledoctor/` · `~/.codex/skills/ruledoctor/` · Cursor：`~/.cursor/skills/ruledoctor/`

仓库：https://github.com/syf2211/ruledoctor （`skills/ruledoctor`）

用户文档：https://github.com/syf2211/ruledoctor/blob/main/docs/用户指南.md
