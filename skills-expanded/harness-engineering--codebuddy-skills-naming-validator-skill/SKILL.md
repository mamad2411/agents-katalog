---
name: naming-validator
description: 命名规范校验——函数 / 变量 / 文件 / 接口 / 错误码 / 表名 / 分支等命名是否符合团队规范。
allowed-tools: Read, Bash, Grep
---

# Skill: naming-validator

> 原文 §8.3 规范查询类。命名是"低成本对齐"的最佳入口。

## 规则源

`context/team/coding-style.md`（团队级）+ `context/project/{p}/coding-style.md`（项目级覆盖）。

## 默认规则集（团队若未自定义，使用这套）

| 对象 | 规则 | 示例 |
|---|---|---|
| Go 函数 | UpperCamelCase 导出 / lowerCamelCase 内部 | `GrantCoupon` / `grantCoupon` |
| Go 变量 | lowerCamelCase | `userID` (不是 `userId`) |
| 文件 | snake_case.go | `coupon_grant.go` |
| 接口 path | `kebab-case` | `/coupon/grant-by-tag` |
| 错误码 | 6 位整数，按规范分段 | `4010001` |
| MySQL 表 | `snake_case` 单数 | `coupon_grant_task` |
| MySQL 字段 | `snake_case` | `tag_rule_json` |
| Git 分支 | `feature/T12345-coupon-tag` | 见 git-conventions |
| FT 编号 | `FT-001`, `FT-002` | 不能省零 |

## 工作流

输入文件路径或 diff → 逐条提取命名 → 匹配规则 → 输出违规列表。

```
=== Naming Validation: coupon_grant.go ===

✓ 文件名：coupon_grant.go
✓ 函数：GrantByTag (导出，UpperCamelCase)
❌ 变量：UserId → 应为 userID（Go 习惯：ID/URL/JSON 等首字母缩写应全大写）
❌ 错误码：401001 → 位数错误，应为 6 位
✓ 接口 path：/coupon/grantByTag → 建议改 /coupon/grant-by-tag（kebab-case）
```

## 与 coding-style.md 的优先级

项目级覆盖团队级（详见 AGENTS.md §10）。

## 协作

- 被 `auxiliary-checker` Agent 调用（review 维度⑧）
- 被 `feature-implementer` 在 commit 前自检
