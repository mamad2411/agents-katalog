---
name: common-version-management
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 version-management Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/version-management.md`（完整规范）。以下为操作要点：


# 版本管理规范

> 完整规范详见 `wiki/_common/version-management.md`

## 版本格式（MUST）

`X.Y.Z` 3 段式语义化版本：

| 段位 | 名称 | 自增时机 | 示例 |
|------|------|----------|------|
| **X** | 架构版本 | 架构级别调整（模块拆分/合并、框架大版本升级） | 1 → 2 |
| **Y** | 功能版本 | 新增功能 | 1.0 → 1.1 |
| **Z** | 修复版本 | Bug 修复（每次修复必增） | 1.1.0 → 1.1.1 |

## 核心约束

- **MUST** 版本号不可重复，不可回退。
- **MUST** 每次开发前确认目标版本号（X/Y/Z 哪段自增）。
- **MUST** Y 自增时 Z 归 0；X 自增时 Y 和 Z 归 0。
- **MUST** 开发阶段使用 `{X}.{Y}.{Z}-SNAPSHOT`，发布时去掉 `-SNAPSHOT`。
- **MUST** 分支命名与版本号对应：`feat-1.2.0` 对应功能版本 `1.2.0`。
- **MUST** 发布前检查 `README.md` 是否与当前版本代码一致。
- **MUST NOT** 在 README 过期的情况下发布版本。

完整规则以 `wiki/_common/version-management.md` 为准。
