---
name: relay-handoff-stop
description: Use when ending a session before switching tools/models, and a complete handoff snapshot must be persisted. 中文常见触发：做一次标准交接、按接力开发规则收尾、切换前先交接。
---

# Relay Handoff Stop

## 目标
结束会话前把“做了什么/没做完什么/下一步”写清楚，保证下一个模型可直接接手。

## 执行步骤
1. 更新 `progress.md` 顶部 `Latest Handoff Snapshot`：
   - Task-ID
   - Task-Name
   - Files Changed
   - Completed This Session
   - Open TODO
   - Risks/Blockers
   - Next First Command
2. 在 `修改记录_会话备忘.md` 追加一条 `Session Record`：
   - Task-ID
   - Task-Name
   - 本轮目标
   - 已完成
   - 未完成
   - 关键命令/结果
   - 下一步
3. 更新 `task_registry.md` 中相同 `Task-ID` 的行：
   - Status
   - Last Update
   - Next First Command
4. 输出一句交接摘要并停止执行。


