---
description: |
triggers:
  - 接入老项目
  - 老项目改造
  - 项目迁移
  - 规范接入
  - 现状审计
  - 老项目
  - legacy
  - migration
  - onboarding
  - 重构
role: architect
priority: high
category: requirement
stack: _common
alwaysApply: false
---


# 老项目接入（Legacy Onboarding）

> 老项目接入本规范的**核心技能**。
> 串联完整流程：**codebase-audit → migration-planning → retro-document（可选）→ 进入正常 SDLC**。

## 前置条件

- 已有项目（含源代码 + git 历史）
- 未接入本规范（无 `changes/` 目录或刚通过 `--only-changes` 初始化）

## 双流程区分

| 项目类型 | 流程 |
|---|---|
| **全新项目** | 用 `scaffold-project` |
| **老项目接入** | 用本技能 `legacy-onboarding` |
| **已有项目普通变更** | 用 `requirement-analysis` |

## 执行步骤

### 第 1 步：现状审计（调用 codebase-audit）

扫描项目现状：
- 代码结构
- 规范符合性（命名 / 分支 / commit / 架构分层 / 异常 / 日志 / API / 安全）
- 测试覆盖率
- CI/CD
- 文档完整度

**产出**：`changes/proposals/0000-legacy-onboarding/audit-report.md`

详见 `codebase-audit` 技能。

### 第 2 步：制定迁移计划（调用 migration-planning）

**MUST 与用户确认**：

```
Q1: 改造范围？
    a) 全部（一次性迁移）
    b) 部分（仅新代码按新规范）
    c) 渐进（接触到的老代码顺手改）

Q2: 迁移策略？
    a) 冻结（老代码不动，仅新代码按新规范）
    b) 渐进改造（Boy Scout Rule，推荐）
    c) Strangler Fig（新功能在新模块，老功能逐步替换）
    d) 整体重写（极少推荐）

Q3: 阶段规划？
    M1: <范围 + 完成标准>
    M2: ...
```

**产出**：`changes/proposals/0000-legacy-onboarding/proposal.md` + `tasks.md`

详见 `migration-planning` 技能。

### 第 3 步：初始化四层结构

如果尚未初始化：

```bash
# 安装规则
./install.sh -t <project> -s <stack> -w <tools> -c

# 创建 0000-legacy-onboarding 提案
mkdir -p changes/proposals/0000-legacy-onboarding
```

### 第 4 步：（可选）反向文档化（调用 retro-document）

为核心模块反向生成：
- 架构文档（C4）
- 关键决策的 ADR
- 主要流程的时序图

**产出**：`docs/architecture/` 或 `docs/adr/`

详见 `retro-document` 技能。

### 第 5 步：进入正常 SDLC

```
新需求 → requirement-analysis（正常流程）
老代码改造 → migration-proposal → coding
老代码维护 → 适用 common-legacy-tolerance 规则
```

## 老代码处理策略

| 策略 | 说明 | 适用 |
|---|---|---|
| **冻结** | 老代码不动，只新代码按新规范 | 稳定老项目 |
| **渐进改造** ⭐ | 接触到的老代码顺手改（Boy Scout Rule） | 持续维护项目 |
| **Strangler Fig** | 新功能在新模块，老功能逐步替换 | 大型重构 |
| **整体重写** | 一次性重写 | 极少推荐 |

## 关键约束

- ✅ **MUST** 先做现状审计（codebase-audit）
- ✅ **MUST** 迁移策略经用户确认
- ✅ **MUST** 从接入点开始记 changelog（不强制补历史）
- ❌ **MUST NOT** 大面积重写老代码（应用渐进改造）
- ❌ **MUST NOT** 强制老代码立即补测试（新改动必须带测试）

## 产出物

- `changes/proposals/0000-legacy-onboarding/audit-report.md`
- `changes/proposals/0000-legacy-onboarding/proposal.md`
- `changes/proposals/0000-legacy-onboarding/tasks.md`
- （可选）架构文档 / ADR

## 完成标准

- audit-report.md 完成
- 迁移提案经用户确认
- 四层结构初始化完成
- 进入正常 SDLC

## 关联

- 子技能：`codebase-audit` / `migration-planning` / `retro-document`
- 后续：`requirement-analysis`（正常流程）
- Wiki：`wiki/_common/legacy-onboarding.md` `wiki/_common/migration-strategies.md`
- 规则：`common-legacy-tolerance`
