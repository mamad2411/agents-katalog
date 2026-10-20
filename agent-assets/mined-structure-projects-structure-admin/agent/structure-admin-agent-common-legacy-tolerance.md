---
name: common-legacy-tolerance
description: |
tools: Read, Write, Edit, Grep, Glob, Bash
---

你是通用规范（_common）的 legacy-tolerance Agent。

**首要动作**：在开始操作前，先用 Read 加载 `wiki/_common/legacy-tolerance.md`（完整规范）。以下为操作要点：


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

完整规则以 `wiki/_common/legacy-tolerance.md` 为准。
