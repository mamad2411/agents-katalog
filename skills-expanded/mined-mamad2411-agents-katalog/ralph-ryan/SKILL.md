---
name: ralph-ryan
description: "Ralph autonomous agent for iterative development with multi-PRD parallel support. Commands: '/ralph-ryan:prd' (create PRD), '/ralph-ryan:prep' (prepare), '/ralph-ryan:run' (execute), '/ralph-ryan:status' (overview). Triggers on: ralph prd, ralph prep, ralph run, ralph go, ralph status."
---

# Ralph Agent

Autonomous coding agent that implements user stories iteratively with **multi-PRD parallel development** support.

---

## Routing

Based on user intent, load the corresponding instruction file:

| Intent | Keywords | Action |
|--------|----------|--------|
| **PRD** | prd, create, generate, plan | Read `{baseDir}/prd.md` |
| **Prep** | prep, prepare, convert, setup | Read `{baseDir}/prep.md` |
| **Run** | run, execute, go, start | Read `{baseDir}/run.md` |
| **Status** | status, list, overview | Read `{baseDir}/status.md` |

---

## Directory Structure (Multi-PRD)

```
.claude/ralph-ryan/
├── prd-06-risk-management/          # PRD 子目录
│   ├── prd.md                       # PRD 文档
│   ├── prd.json                     # 结构化数据
│   └── progress.txt                 # 进度日志
├── prd-07-model-governance/
│   ├── prd.md
│   ├── prd.json
│   └── progress.txt
└── ...

.claude/ralph-ryan-archived/         # 已完成的 PRD
└── 2026-01-29-prd-06-risk-management/
```

**命名规范**: `prd-<slug>` 或 `<descriptive-name>`，使用 kebab-case

---

## Shared Configuration

| Item | Path |
|------|------|
| Working directory | `.claude/ralph-ryan/` |
| PRD 子目录 | `.claude/ralph-ryan/<prd-slug>/` |
| PRD markdown | `.claude/ralph-ryan/<prd-slug>/prd.md` |
| PRD JSON | `.claude/ralph-ryan/<prd-slug>/prd.json` |
| Progress log | `.claude/ralph-ryan/<prd-slug>/progress.txt` |
| Loop state | `.claude/ralph-ryan/<prd-slug>/ralph-loop.local.md` |
| Archived runs | `.claude/ralph-ryan-archived/<date>-<prd-slug>/` |

### prd.json Branch Fields

| Field | Description |
|-------|-------------|
| `branchName` | Target branch for execution |
| `baseBranch` | Base branch for creation (only if creating new branch) |

**Branch strategy (set during prep):**
- **Use current**: `branchName` = current branch, no `baseBranch`
- **New from current**: `branchName` = `ralph/<prd-slug>`, `baseBranch` = current branch
- **New from main**: `branchName` = `ralph/<prd-slug>`, `baseBranch` = `main`

---

## Quick Reference

```bash
# 查看所有 PRD 状态
/ralph-ryan:status

# 创建新 PRD (会询问 slug 名称)
/ralph-ryan:prd [describe your feature]

# 准备执行 (会列出可选 PRD)
/ralph-ryan:prep

# 执行 (会列出可选 PRD，自动循环直到完成)
/ralph-ryan:run [prd-slug] [--max-iterations N]
```

停止循环：直接 Ctrl+C 终止即可。

---

## Session Isolation

每个循环状态文件 (`ralph-loop.local.md`) 包含 `session_hash` 字段。Stop Hook 在第一次迭代时自动填入当前会话 transcript 路径的 SHA256 哈希值（16字符），确保：
- 只有启动循环的会话才能继续它
- 其他会话不会干扰正在运行的循环
- 隐私保护：不存储完整路径，只存储哈希值
- 如果其他会话尝试退出时发现有活跃循环，会提示选择：退出或接管

---

## File Tracking

每个 story 完成后，在 prd.json 中记录修改的文件：

```json
{
  "id": "US-003",
  "passes": true,
  "filesChanged": [
    "app/risk/greeks/page.tsx",
    "components/charts/greeks-heatmap.tsx"
  ]
}
```

用于：
1. 精准 commit（只提交相关文件）
2. 冲突检测（多 PRD 修改同一文件时预警）
