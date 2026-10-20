---
description: |
  老代码容忍规则 - 当用户在老项目工作时 MUST 遵守。
  禁止大面积重写老代码；渐进改进；保持行为兼容。
  新代码按新规范，老代码渐进改造。

triggers:
  - 老代码
  - 遗留代码
  - legacy
  - 旧代码
  - 老项目
  - 重构

priority: high
alwaysApply: false
globs: "**/*.java, **/*.ts, **/*.vue, changes/**/*.md"

category: legacy-tolerance
stack: _common
role: common
maturity: complete

reads-before-action:
  - wiki/_common/legacy-onboarding.md
  - wiki/_common/migration-strategies.md

related-skills:
  - legacy-onboarding
  - migration-planning

when-to-use: |
  在老项目工作，处理既有代码
when-not-to-use: |
  全新项目
version: "0.3.0"
since: "2026-08-13"
---

# 老代码容忍规则

> 完整规范详见 `wiki/_common/legacy-onboarding.md` + `wiki/_common/migration-strategies.md`

## 核心原则

**新代码按新规范，老代码渐进改造**。

## 硬约束（MUST）

- ✅ **MUST** 新代码按新规范
- ✅ **MUST** 修改老代码时顺手改造（Boy Scout Rule）
- ✅ **MUST** 保持行为兼容（不破坏现有 API / 数据）
- ✅ **MUST** 改造老代码 MUST 先有测试覆盖

## 禁止（MUST NOT）

- ❌ 大面积重写老代码（应用渐进改造）
- ❌ 强制老代码立即补测试（新改动必须带测试）
- ❌ 在同一文件内混用两种规范
- ❌ 因为"老代码不规范"就拒绝改 bug
- ❌ 一次性重写整个模块（除极少见的小项目）

## 双规范并存期约定

| 维度 | 新代码 | 老代码 |
|---|---|---|
| 位置 | 新建模块 / 新文件 | 现有文件 |
| 规范 | 新规范 | 保持现有 |
| 测试 | MUST 有 | 不强制 |
| 文档 | MUST 有 | 不强制 |

## 关联

- Wiki：`wiki/_common/legacy-onboarding.md` `wiki/_common/migration-strategies.md`
- 技能：`legacy-onboarding` / `migration-planning`
