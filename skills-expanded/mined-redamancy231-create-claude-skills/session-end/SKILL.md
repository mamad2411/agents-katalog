---
name: session-end
description: '[流程:交接] Standardized session handoff executor per AI collaboration framework §9.3. Runs Session Start checklist (verify CLAUDE.md/memory loaded, check memory staleness >30d, load project status, confirm environment) and Session End checklist (update project_status.md, write standardized Next Steps with priority+dependencies, capture cross-task lessons to memory/, flag Retrospect candidates). Use when ending a substantive work session, before context switching, or when invoked as /session-end. Do NOT use for quick Q&A or trivial turns — only sessions that produced or changed project state. Manual invocation only, not automated via Stop hook.'
allowed-tools: Read, Write, Edit, Bash(git:*), Bash(python:*), Glob, Grep
source: self
source_type: self
license: "CC-BY-4.0"
verified_by: "GPT-5.5, DeepSeek-V4-Pro, Kimi-K2.7, Qwen3.7-Max, GLM-5.2"
---

# Session End（会话交接标准化执行器）

> 框架 §9.3 跨层关切 — 确保跨会话状态可恢复。手动调用，不用 Stop hook。
> **Scope**：user scope（跨项目通用）。

## 快速参考（路由表）

| 场景 | 执行 |
|------|------|
| 结束产生项目状态变更的会话 | Session End 完整双清单 → [Start](reference/session-start-checklist.md) + [End](reference/session-end-checklist.md) |
| 同会话内第二次及之后调用 | 仅 Session End 清单（跳过 Session Start 复核） |
| 快速问答/纯信息查询（<5 轮） | 不触发 |
| 中断恢复（auto-compact 打断） | → 按下方「中断恢复」规则 |
| 详细检查项/教训/关系/判据 | → 见下方「参考文件」 |

## 共享文件所有权

| 文件 | 本 Skill 角色 | 其他写入者 | 约束 |
|------|-------------|-----------|------|
| `project_status.md` | **主写入者**（固定四段结构更新） | 无（其他 Skill 只读） | 更新后须检查对应 memory 文件一致性 |
| `reference_files.md` | **主维护者**（追加/标记删除） | 无 | 不含临时文件/中间产物 |
| `CHANGELOG.md` | **主写入者**（登记本会话实质变更） | 无 | 每次实质变更同步登记一行（最新在上），不等提醒；无实质变更则勾选注明 |
| `memory/*.md`（本项目） | **写入者**（跨任务教训） | session-end 自身 | 日期新鲜≠内容准确，须交叉比对 |
| `_reviews/retrospect_*.md` | **写入者**（新发现 → Retrospect） | 无 | 仅方法论/流程/工具层面发现 |

## 触发分级

**应触发（执行完整双清单）**：结束产生/修改了项目状态的会话；上下文切换前；用户显式调用 `/session-end`；长会话（>30 轮有意义交互）。

**不应触发**：快速问答（<5 轮、未修改文件）、纯信息查询、已批准项目内单文件微调。

**判定问句**："本会话是否产生了需要下一会话知道的状态变更？" 是→执行；否→跳过。

## 中断恢复

长会话可能触发 auto-compact 打断清单执行。被打断后：
- 已完成的清单项通过 git diff / 文件时间戳 / 对话上下文确认后跳过，不重复执行
- 不确定是否完成的项重新执行（幂等操作无副作用）
- 如中断前已开始写入文件 → 先检查文件当前状态再继续追加，避免重复段

## 参考文件

| 文件 | 内容 |
|------|------|
| [reference/session-start-checklist.md](reference/session-start-checklist.md) | Session Start 检查清单（7 项） |
| [reference/session-end-checklist.md](reference/session-end-checklist.md) | Session End 检查清单（5 子模块） |
| [reference/lessons.md](reference/lessons.md) | 反例/教训表 |
| [reference/skill-relationships.md](reference/skill-relationships.md) | 与互补 Skill 的关系 |
| [reference/death-criteria.md](reference/death-criteria.md) | 本 Skill 的死亡判据 |
| [templates/next-steps-format.md](templates/next-steps-format.md) | Next Steps 标准化格式 |
| [scripts/check-memory-staleness.py](scripts/check-memory-staleness.py) | memory 时效性检查脚本 |
