---
name: relay-start
description: Use when starting a new session or taking over from another model, and context must be reconstructed before execution. 中文常见触发：接手这个项目、按接力开发规则来、开始按接力流程接手当前项目。
---

# Relay Start

## 目标
让新会话或接力会话在 30 秒内恢复上下文并进入执行。

## 执行步骤
1. 按顺序读取：
   - `AGENTS.md`
   - `task_registry.md`
   - `progress.md`
   - `task_plan.md`
   - `findings.md`
   - `修改记录_会话备忘.md`
2. 默认采用“摘要优先、按需深读”：
   - `AGENTS.md` 全文读取
   - `task_registry.md` 先读当前活跃 `Task-ID` 行
   - `progress.md` 先读顶部 `Latest Handoff Snapshot`
   - `task_plan.md` / `findings.md` 先读当前任务相关段
   - `修改记录_会话备忘.md` 先读最近 1-3 条相关记录
   - 仅在用户明确要求、上下文冲突或无法恢复任务时再扩大读取范围
3. 先锁定或创建一个 `Task-ID`，并声明 `Task-Name`。
4. 输出 `Session Context`：
   - Developer/Branch(or No-Git)
   - Task-ID / Task-Name
   - Active Goal
   - Current Phase
   - Next First Command
   - Open TODO Top3
5. 执行启动检查：
   - `Get-Location`
   - `Get-ChildItem -Force`
   - `if (Test-Path .git) { git status --short } else { 'NO_GIT_REPO' }`
   - `python -V`
6. 执行 `Next First Command` 并继续当前任务。


