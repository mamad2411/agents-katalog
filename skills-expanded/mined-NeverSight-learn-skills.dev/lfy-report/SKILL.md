---
name: lfy-report
description: 报表查询技能。适用于通过 lfy-cli 的 report 品类读取陆份仪侧只读报表数据。当用户需要：(1) 查询指定销售人员当前财年的合同目标（年/季/月及是否已配置），(2) 后续在 report 下扩展的其他只读报表接口时使用此技能；具体命令与参数以本技能 references 为准。
version: 1.0.1
metadata:
  requires:
    bins: ["lfy-cli"]
  cliHelp: "lfy-cli report --help"
---

# 报表查询技能

> `lfy-cli` 是陆份仪提供的命令行程序，所有操作通过执行 `lfy-cli` 命令完成。

通过 `lfy-cli report <接口名> '<json参数>'` 与报表服务交互（需已完成 `lfy-cli init` 登录配置）。

## 注意事项

- 若命令输出以 `Error:` 开头或 JSON 中含 `error_message`，需向用户说明原因，勿伪造数据。
- 当前 **report** 品类下接口均为 **只读**，不支持通过本技能发起修改类操作。
- `sales_id` 等同 org 内技术 ID，面向业务用户展示时可优先展示 `sales_name` 等业务字段。
- 每新增一个 `report/<子命令>`，应在 `references/` 下增加对应文档，并在下方「接口列表」补充一节。

---

## 接口列表

### 销售财年合同目标 (sales_target)

```bash
lfy-cli report sales_target '{"sales_id": 123}'
```

查询指定销售在当前财年的**合同目标**（年目标 + 季/月槽位，含是否已配置）。

参见 [API 详情](references/sales_target.md)。

---

## 典型工作流

### 查询某销售的财年合同目标

**经典 query 示例：**

- 「查一下销售 ID 为 123 的本财年合同目标」
- 「张三的销售目标是多少」（需先具备或可解析出 `sales_id`）
- 「这个销售 Q2、M3 有没有设目标」
- 「我这个月的销售目标是多少」
- 「我这个季度的销售目标是多少」
- 「我这个财年的销售目标是多少」

**流程：**

1. 先确认销售人员的ID是否已知，已知的话直接进行第2步；否则先通过 `lfy-cli user get_sales '{}'` 获取销售人员名单，自动根据销售的名字匹配到对应的 sales_id，如果匹配到多个人名，需要让用户确认是哪个销售。
2. 执行 `lfy-cli report sales_target '{"sales_id": <id>}'`。
3. 若成功：结合返回中的 `year_target`、`quarterly`、`monthly` 与 `is_set` 向用户说明； `is_set` 为 `false` 时表示尚未配置该季度/月度的目标。
4. 若失败：根据终端 `Error:` 或 JSON `error_message` 说明（例如暂未设置财年目标）。

**展示结果（示例结构，非固定话术）：**

```
📊 销售目标（财年）：<sales_name>
年目标：<year_target>（<start_date> ~ <end_date>）
季度：Q1 … Q4（已配置项 is_set=true，未配置为 false）
月度：M1 … M12（同上）
```
