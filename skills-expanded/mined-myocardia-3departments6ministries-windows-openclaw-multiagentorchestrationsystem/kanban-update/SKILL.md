---
name: kanban_update
description: 三省六部看板任务更新工具。用于读取和更新看板上的任务状态、流转记录、进展汇报、子任务等。所有 Agent 必须掌握此技能。
---

# kanban_update — 看板任务操作

## 路径

- **看板脚本**: `~/.openclaw/workspace/skills/edict-main/scripts/kanban_update.py`
- **任务数据**: `~/.openclaw/workspace/skills/edict-main/data/tasks_source.json`

## 读取任务

用 `read` 工具或 `exec` 读取 tasks_source.json，找到你的 task_id 对应的任务。

## 更新状态

```bash
python ~/.openclaw/workspace/skills/edict-main/scripts/kanban_update.py state <task_id> <new_state> "备注"
```

状态值: `Taizi` `Zhongshu` `Menxia` `Assigned` `Doing` `Review` `Done` `Blocked`

## 添加流转记录

```bash
python ~/.openclaw/workspace/skills/edict-main/scripts/kanban_update.py flow <task_id> "来源部门" "目标部门" "remark"
```

## 完成任务

```bash
python ~/.openclaw/workspace/skills/edict-main/scripts/kanban_update.py done <task_id> "输出路径" "摘要"
```

## 子任务管理

```bash
python ~/.openclaw/workspace/skills/edict-main/scripts/kanban_update.py todo <task_id> <todo_id> "标题" <status>
```

status: `not-started` | `in-progress` | `completed`

## 实时进展汇报（频率不限，越频繁越好）

```bash
python ~/.openclaw/workspace/skills/edict-main/scripts/kanban_update.py progress <task_id> "进展描述" "子任务1|子任务2"
```

## 状态流转

```
皇上 → 太子(Taizi) → 中书省(Zhongshu) → 门下省(Menxia) → 尚书省(Assigned) → 六部(Doing) → 审查(Review) → 完成(Done)
```

## ⚠️ 规则

1. 收到派发消息后，先读 tasks_source.json 查看任务详情
2. 不要重复创建已有的任务
3. 每完成重要步骤用 `progress` 上报
4. 状态变更用 `state` 更新看板
5. 完成用 `done` 标记
