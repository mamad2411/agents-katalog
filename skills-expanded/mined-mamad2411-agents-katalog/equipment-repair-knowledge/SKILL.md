---
name: equipment-repair-knowledge
description: 门店设备维修管理本体知识与工具使用策略
type: domain_knowledge
---

# 门店设备维修管理

## 本体（4 Object / 4 Link）
- **Object**: Equipment、RepairTicket、Technician、Vendor
- 读实体用 `query_entity`，遍历关系用 `traverse_relation`。
- 维修工单列表用专属工具 `query_repair_tickets`。

## 状态
- Equipment.status：normal / in_repair / scrapped
- RepairTicket.status：reported / diagnosed / assigned / repairing / resolved / cancelled

状态迁移只能经 Action，不可直接改写。

## 无折扣概念
本 vertical 无折扣/数值规则。维修费用（parts_cost / labor_cost）在 complete_repair 时按实际填写，单位元。
