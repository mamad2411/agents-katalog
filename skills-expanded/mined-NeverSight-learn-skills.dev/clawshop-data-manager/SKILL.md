---
name: clawshop-data-manager
description: |
  电商选品商品库管理。自动创建并管理飞书多维表格「赛博店长-商品库」。
  功能：(1) 首次自动建表建字段 (2) 候选品入库 (3) 状态流转 (4) 搜品回填
  (5) 订单数更新 (6) 14天淘汰同步。
  触发词：商品库、候选库、bitable、选品入库、更新状态、写入候选、商品入库。
---

# 赛博店长-商品库

## 🚀 Bootstrap（每次使用前）

**Step 1：读取 token**

```bash
exec: echo $CLAWSHOP_APP_TOKEN && echo $CLAWSHOP_TABLE_ID
```

**Step 2：校验是否可用**

用读到的 token 调用 `feishu_bitable_list_fields(app_token, table_id)`：
- 返回字段列表 → ✅ 直接操作
- 报错 / token 为空 → 重新建表（见 Step 3）

**Step 3：建表（仅在校验失败时执行）**

1. 调用 `feishu_bitable_create_app(name="赛博店长-商品库")` → 获得新 app_token / table_id
2. 依次调用 `feishu_bitable_create_field` 创建 16 个字段（字段定义见 `{baseDir}/references/fields.md`）
3. 用 `gateway config.patch` 写入新 token 并重启：

```json
{
  "skills": {
    "entries": {
      "clawshop-data-manager": {
        "env": {
          "CLAWSHOP_APP_TOKEN": "new_app_token",
          "CLAWSHOP_TABLE_ID": "new_table_id"
        }
      }
    }
  }
}
```

---

## ⚙️ Feishu 账号说明

`feishu_bitable_*` 工具统一使用 `channels.feishu.accounts.default` 账号创建和读写表，这是 OpenClaw 当前行为（多账号隔离为社区少数需求，暂未修复）。无需切换账号，直接操作即可。

---

## 🚨 写入铁律

- **只用 `feishu_bitable_*` 工具**，禁止自己拼 curl
- **主字段名是「赛博店长-商品库」**，不是「商品名称」，写错会静默失败
- **禁止重复入库**：入库前先 `feishu_bitable_list_records` 查全量，商品名关键词匹配任意状态 → 跳过换品

---

## 🚫 候选状态铁律（只允许这 7 个值）

| 状态 | 写入时机 |
|------|---------|
| `⏳待评估` | 选品入库 |
| `🔄铺货中` | 搜品成功，铺货已提交 |
| `已上架` | 巡检确认在抖店在售 |
| `已出单` | 订单数 ≥ 1 |
| `已下架` | 14天0单下架 |
| `❌不符合标准` | 搜品失败/无货源 |
| `❌铺货失败` | 铺货提交后被平台过滤 |

**状态流转**：
```
⏳待评估 → 🔄铺货中 → 已上架 → 已出单（永久保留）
                   ↘ ❌铺货失败   ↘ 已下架（14天0单且订单数=0）
⏳待评估 → ❌不符合标准（搜品失败/无货源）
```
严禁写入任何其他值。

---

## 读写速查

| 操作 | 工具 | 关键参数 |
|------|------|---------|
| 读全量 | `feishu_bitable_list_records` | app_token, table_id |
| 新增记录 | `feishu_bitable_create_record` | app_token, table_id, fields |
| 更新记录 | `feishu_bitable_update_record` | app_token, table_id, record_id, fields |

token 值通过 `exec: echo $CLAWSHOP_APP_TOKEN && echo $CLAWSHOP_TABLE_ID` 获取，再传入工具调用。

---

## 详细文档

- 字段定义 + 状态说明 → `{baseDir}/references/fields.md`
- CRUD 示例 + 常见错误 → `{baseDir}/references/operations.md`
