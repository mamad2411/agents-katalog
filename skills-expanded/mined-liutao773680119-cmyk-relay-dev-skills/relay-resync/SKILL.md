---
name: relay-resync
description: Use when context drifts, outputs conflict with the current phase, or an interrupted session must be realigned. 中文常见触发：重新同步当前任务、上下文漂移了、重新按接力规则对齐。
---

# Relay Re-sync

## 使用时机
- 模型疑似遗忘上下文
- 输出与当前阶段明显不一致
- 切换工具后出现执行偏移

## 执行步骤
1. 重新按顺序读取：
   - `AGENTS.md`
   - `task_registry.md`
   - `progress.md`
   - `task_plan.md`
   - `findings.md`
   - `修改记录_会话备忘.md`
2. 默认先做摘要恢复：
   - 锁定当前 `Task-ID`
   - 先读 `Latest Handoff Snapshot`
   - 再读当前任务相关段与最近 1-3 条会话记录
3. 重新输出：
   - Task-ID / Task-Name
   - Active Goal
   - Current Phase
   - Next First Command
   - Open TODO Top3
4. 与用户确认“是否按 Next First Command 继续执行”。


