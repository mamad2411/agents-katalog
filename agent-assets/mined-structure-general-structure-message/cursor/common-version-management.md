---
description: |
  当用户要求"升版本/改版本号/打 tag/发版/修改 pom.xml/package.json 版本"时触发。
  覆盖 3 段式语义化版本管理规范、SNAPSHOT 流程、版本与分支对应关系。

triggers:
  - 版本
  - version
  - tag
  - 发版
  - 升级
  - 版本号
  - SNAPSHOT
  - release

priority: medium
alwaysApply: false
globs: "**/pom.xml, **/build.gradle, **/package.json, **/*.toml, **/README.md"

category: version-management
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/version-management.md

related-skills:
  - release-version
  - ci-gate
  - deployment-verification

when-to-use: |
  递增版本号、修改 pom.xml/build.gradle/package.json 版本字段、打 tag、发布版本前
when-not-to-use: |
  仅查看当前版本号
version: "0.3.0"
since: "2026-08-13"
---

# 版本管理规范

> 完整规范详见 `wiki/version-management.md`

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
