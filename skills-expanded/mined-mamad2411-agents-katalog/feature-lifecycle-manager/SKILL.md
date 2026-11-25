---
name: feature-lifecycle-manager
description: 管理单个 feature（FT-*）的生命周期：pending → in_progress → done。维护 features.json，触发对应 Agent。
allowed-tools: Read, Write, Edit, Bash, Task
---

# Skill: feature-lifecycle-manager

> 在 `managing-requirement-lifecycle` 之下的"feature 粒度"调度。原文 §8.3。

## 触发

- `/req-task:start`、`/req-task:done` 等命令
- `code-review-preparer` 完成 8 维 review 后调用，决定是否标 done

## feature 状态机

```
pending ──▶ in_progress ──▶ done
                │
                └──▶ blocked（review 卡住）
                │
                └──▶ cancelled（需求变更/废弃）
```

| 转移 | 条件 | 谁触发 |
|---|---|---|
| pending → in_progress | 用户 `/req-task:start FT-001` | feature-lifecycle-manager |
| in_progress → done | 8 维 review 全 PASS + commit 含 (FT-id) | code-review-preparer |
| in_progress → blocked | 任一维 review 为 FAIL | code-review-preparer |
| blocked → in_progress | 用户修复后重新触发 review | feature-lifecycle-manager |
| any → cancelled | 用户显式 `/req-task:cancel FT-001` | feature-lifecycle-manager |

## 写入约束

- 写 `features.json` 时必须保持 JSON 合法（用 `JSON.parse + JSON.stringify` 而不是字符串替换）
- 状态变更必须更新 `state_history`（追加而不是覆盖）

## features.json 扩展字段（v1 兼容）

```json
{
  "id": "FT-001",
  "status": "in_progress",
  "state_history": [
    { "to": "pending", "ts": "2026-05-28T08:00:00Z" },
    { "to": "in_progress", "ts": "2026-05-28T10:30:00Z", "by": "koka" }
  ],
  "assignee": "koka",
  "started_at": "2026-05-28T10:30:00Z",
  "completed_at": null
}
```

## 与 managing-requirement-lifecycle 的边界

- managing-requirement-lifecycle 管"阶段"
- 本 Skill 管"feature 任务"
- 阶段 4.4 内的细粒度状态都由本 Skill 维护，4.4 完成判定（所有 features 为 done）由 lifecycle Skill 跑
