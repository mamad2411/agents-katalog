---
name: lfy-base
description: 客户编辑场景基础数据（下拉选项）。当用户需要获取客户状态、标签、区域、行业的可选 id 列表用于修改客户信息时使用；通过 lfy-cli base get_options，property 仅四类；API 上 cli 可省略（默认 false）；Agent 示例仍推荐 cli=true。
version: 1.0.4
metadata:
  requires:
    bins: ["lfy-cli"]
  cliHelp: "lfy-cli base --help"
---

# 基础下拉选项技能（客户字段）

> 示例里 **`cli` 一般为 `true`**（仅 `id`、`name`，无 `color`，适合 Agent）。**不传 `cli` 或 `cli:false`**（默认）时每项 **必有 `color` 键**（值可为 `""`）。

通过 `lfy-cli base get_options '<json>'` 获取下拉数据；需已完成 `lfy-cli init`（与其它品类相同自动注入凭证）。

## property 取值（仅此四种）

| property | 含义 |
|----------|------|
| `customer_status` | 客户状态 |
| `customer_tags` | 客户标签 |
| `customer_region` | 区域 |
| `customer_industry` | 行业 |

## 命令示例

客户状态（将 `<customer_id>` 换成真实客户 id）：

```bash
lfy-cli base get_options '{"object_id": <customer_id>, "property": "customer_status", "cli": true}'
```

区域：

```bash
lfy-cli base get_options '{"object_id": <customer_id>, "property": "customer_region", "cli": true}'
```

行业：

```bash
lfy-cli base get_options '{"object_id": <customer_id>, "property": "customer_industry", "cli": true}'
```

标签：

```bash
lfy-cli base get_options '{"object_id": <customer_id>, "property": "customer_tags", "cli": true}'
```

## 返回与错误

- 成功：`result` 为选项数组。**省略 `cli` 或 `cli:false`**：每项 **`id`、`name`、`color`**（`color` 必有键）；**`cli:true`**：每项仅 **`id`、`name`**（无 `color` 字段）。
- `object_id` 传 `0`：返回空数组（不查客户）。
- 终端若出现 `Error: 当前客户信息不存在`（对应接口业务码 `4004`）：客户不存在、未激活或无效上下文的客户 id。
- `property` 拼写错误：错误文案含「无效，支持 customer_status,customer_tags,customer_region,customer_industry」。

## 与客户技能的衔接

### `customer_id`（即 JSON 里的 `object_id`）从哪来

- **最常见**：手头只有公司名称/关键字时，先用客户搜索，`result` 里每条有 **`customer_id`**，任选一条作为 `object_id`：

```bash
lfy-cli customer search '{"keywords": "<名称或关键字片段>"}'
```

- **已知 id**：会话、工单、CRM 链接、或其它工具已给出数字 id，可直接用作 `object_id`。
- **列表/详情里已有**：若在走 `customer get_list`、`get_details` 等流程，响应里的客户主键同为 **`customer_id`**，与这里 `object_id` 含义一致。

下拉选项里各字段的 **`id`** 如何用（写回客户），见 **`lfy-customer`** 技能正文与 references。
