---
name: pdf-member
version: 1.0.0
description: "pdf-cli 会员模块：会员信息、权益查询、价格配置、订单管理、兑换码。当用户需要查看会员等级、权益、价格、订单或兑换会员码时使用。"
metadata:
  requires:
    bins: ["pdf-cli"]
  cliHelp: "pdf-cli member --help"
---

# member

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../pdf-shared/SKILL.md`](../pdf-shared/SKILL.md)，其中包含认证、配置、错误处理**

## 命令概览

| 命令 | 说明 | 需要登录 |
|------|------|----------|
| [`info`](references/pdf-member-info.md) | 查看会员配置信息 | 是 |
| [`rights`](references/pdf-member-rights.md) | 查看各等级会员权益 | 是 |
| [`pricing`](references/pdf-member-pricing.md) | 查看价格配置 | 是 |
| [`order list`](references/pdf-member-order.md) | 查看订单列表 | 是 |
| [`order get`](references/pdf-member-order.md) | 查看订单详情 | 是 |
| [`redeem`](references/pdf-member-redeem.md) | 兑换会员码 | 是 |

## 快速开始

```bash
# 查看会员权益
pdf-cli member rights

# 查看价格
pdf-cli member pricing

# 查看订单
pdf-cli member order list

# 兑换会员码
pdf-cli member redeem --code <兑换码>
```
