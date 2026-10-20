---
description: 当用户询问数据库内容、用户数据、存档、背包道具、角色解锁/等级/经验/装备、理智账本等游戏数据相关问题时应用此规则。
alwaysApply: false
---

当用户需要查询、分析或修改游戏数据库时，优先使用 `database-server/db_query.py`。

数据库路径：`database-server/data/database.sqlite`

可用命令：
- `python database-server/db_query.py counts` — 各表数据量
- `python database-server/db_query.py users [user_id]` — 查询用户
- `python database-server/db_query.py inventory <user_id> [item_id]` — 查询背包（来源于 `saves.data` 的 `inventory`）
- `python database-server/db_query.py save <user_id> [slot_id]` — 查看存档完整 JSON
- `python database-server/db_query.py unlocks <user_id> [slot_id] [character_id]` — 查询角色解锁状态
- `python database-server/db_query.py progress <user_id> [slot_id] [character_id]` — 查询角色等级/经验
- `python database-server/db_query.py equipment <user_id> [slot_id] [character_id]` — 查询角色装备
- `python database-server/db_query.py character <user_id> <slot_id> [character_id]` — 查询角色总览（解锁+等级经验+装备）
- `python database-server/db_query.py sanity <user_id> [limit]` — 查询理智账本最近明细
- `python database-server/db_query.py balance [user_id]` — 查询理智余额
- `python database-server/db_query.py sql "<SELECT ...>"` — 执行任意 SQL 查询

## 时间字段输出规范（强制）

时间戳字段（如 `created_at`、`updated_at`）均为毫秒级 Unix 时间戳。查询时间相关信息时，必须：
1. 在 SQL 中使用 `datetime(field/1000, 'unixepoch', '+8 hours')` 转换；
2. 输出为「年月日时分秒」格式（示例：`2026-03-01 01:21:37`）。

---

## 角色数据查询规范

新增角色数据表：
- `character_unlocks`：角色解锁/行为接受度
- `character_progress`：角色等级与经验
- `character_equipment`：角色装备（`weapon_id`/`armor_id`/`accessory1_id`/`accessory2_id`）

注意：
- 这三张表主维度均为 `(user_id, slot_id, character_id)`。
- 装备空栏位统一为 `NULL`。

### 常用查询模板

```sql
-- 查询某用户某存档的角色解锁状态
SELECT character_id,
       accept_battle_party,
       accept_flirt_topic,
       accept_nsfw_topic,
       accept_physical_contact,
       accept_indirect_sexual,
       accept_become_lover,
       accept_direct_sexual,
       accept_sexual_partner,
       accept_public_exposure,
       accept_public_sexual,
       accept_group_sexual,
       accept_prostitution,
       accept_sexual_slavery,
       accept_bathing_together,
       accept_player_massage,
       accept_character_massage,
       datetime(updated_at/1000, 'unixepoch', '+8 hours') AS updated_at
FROM character_unlocks
WHERE user_id = ? AND slot_id = ?
ORDER BY character_id;

-- 查询某用户某存档的角色等级/经验
SELECT character_id,
       level,
       exp,
       datetime(updated_at/1000, 'unixepoch', '+8 hours') AS updated_at
FROM character_progress
WHERE user_id = ? AND slot_id = ?
ORDER BY character_id;

-- 查询某用户某存档的角色装备
SELECT character_id,
       weapon_id,
       armor_id,
       accessory1_id,
       accessory2_id,
       datetime(updated_at/1000, 'unixepoch', '+8 hours') AS updated_at
FROM character_equipment
WHERE user_id = ? AND slot_id = ?
ORDER BY character_id;

-- 联表查看某用户某存档的角色总览（解锁+等级经验+装备）
SELECT p.character_id,
       p.level,
       p.exp,
       e.weapon_id,
       e.armor_id,
       e.accessory1_id,
       e.accessory2_id,
       u.accept_battle_party,
       u.accept_become_lover,
       datetime(p.updated_at/1000, 'unixepoch', '+8 hours') AS progress_time,
       datetime(e.updated_at/1000, 'unixepoch', '+8 hours') AS equip_time,
       datetime(u.updated_at/1000, 'unixepoch', '+8 hours') AS unlock_time
FROM character_progress p
LEFT JOIN character_equipment e
  ON p.user_id = e.user_id AND p.slot_id = e.slot_id AND p.character_id = e.character_id
LEFT JOIN character_unlocks u
  ON p.user_id = u.user_id AND p.slot_id = u.slot_id AND p.character_id = u.character_id
WHERE p.user_id = ? AND p.slot_id = ?
ORDER BY p.character_id;
```

---

## 理智账本（sanity_ledger）查询规范

表结构：
- `id` — 自增主键
- `user_id` — 用户 ID（不关联 users 表，删除用户不影响此表）
- `type` — 记录类型（见下方枚举）
- `amount` — 负数=消耗，正数=充值/收入
- `description` — 备注（如角色 ID、操作说明）
- `client_ip` — 客户端真实 IP
- `created_at` — 毫秒时间戳

已定义 `type` 枚举：
- `ai_memory` — 对话记忆写入（`amount` = 该条消息字符数的负值）
- `ai_summary` — 摘要压缩（`amount` = 被压缩消息字符数合计的负值）
- `recharge` — 用户付费充值（正值）

常用查询模板：

```sql
-- 查询某用户余额（所有 amount 求和）
SELECT user_id, SUM(amount) AS balance
FROM sanity_ledger
WHERE user_id = ?;

-- 查询某用户最近明细（带北京时间）
SELECT type,
       amount,
       description,
       client_ip,
       datetime(created_at/1000, 'unixepoch', '+8 hours') AS time
FROM sanity_ledger
WHERE user_id = ?
ORDER BY created_at DESC
LIMIT 20;

-- 按 type 统计全局消耗分布
SELECT type,
       COUNT(*) AS count,
       SUM(ABS(amount)) AS total_chars,
       CAST(AVG(ABS(amount)) AS INTEGER) AS avg_chars
FROM sanity_ledger
GROUP BY type;

-- 查询所有用户累计消耗排行
SELECT user_id,
       SUM(ABS(amount)) AS total_consumed
FROM sanity_ledger
WHERE amount < 0
GROUP BY user_id
ORDER BY total_consumed DESC
LIMIT 20;

-- 按天统计全局字符写入量（北京时间）
SELECT date(created_at/1000, 'unixepoch', '+8 hours') AS day,
       COUNT(*) AS records,
       SUM(ABS(amount)) AS total_chars
FROM sanity_ledger
WHERE amount < 0
GROUP BY day
ORDER BY day DESC;
```