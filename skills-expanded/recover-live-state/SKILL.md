---
name: recover-live-state
description: 从仓库证据恢复当前 Slay the Spire 2 live run，而不是依赖聊天历史。
---

# 恢复当前 live run

适用场景：先判断**当前真实 live 状态**，再决定下一步动作。

## 阅读顺序

1. `AGENTS.md`
2. `README.md`
3. `STARTUP.md`
4. `data\python-runtime\runtime-status.json`
5. `data\python-runtime\runs\` 下最新 run
6. `data\live\latest-standalone-player-step.json`
7. `data\live\standalone-player-step-history.jsonl`
8. `data\python-runtime\knowledge\lessons.json`
9. `data\python-runtime\knowledge\playbook.json`

## 输出

- 当前 live scene
- 当前 floor
- 最近的真实阻塞点
- 是游戏重开了还是只是 standalone loop 重启了
- 下一步最有价值的动作

## 约束

- 优先相信最新 live 证据，而不是旧 summary。
- 不要只看 step counter 就判断重开。
- 如果 `continue_run` 健康可用，优先把它视为恢复路径。
