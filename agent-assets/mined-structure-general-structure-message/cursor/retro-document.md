---
description: |
triggers:
  - 反向生成文档
  - 补架构图
  - 补 ADR
  - retro document
  - 反向工程
  - 架构文档
role: architect
priority: medium
category: documentation
stack: _common
alwaysApply: false
---


# 反向文档化

> 为老项目反向生成架构文档、ADR、时序图。**可选，但推荐**。

## 前置条件

- `audit-report.md` 已完成

## 执行步骤

### 第 1 步：确定文档范围（MUST 用户确认）

```
Q1: 反向生成哪些文档？
    a) C4 架构图（系统上下文 + 容器图）
    b) ADR（关键架构决策记录）
    c) 时序图（关键业务流程）
    d) 全部
```

### 第 2 步：C4 架构图

#### 系统上下文图（Level 1）

```bash
# 扫描依赖
cat pom.xml | grep "<artifactId>"  # Java
cat package.json | grep "dependencies"  # Node
```

画出系统与外部的关系。

#### 容器图（Level 2）

```bash
# 扫描模块
tree -L 2 -d
```

画出系统内部的部署单元。

**产出**：`docs/architecture/c4-context.md` + `c4-container.md`

### 第 3 步：ADR（架构决策记录）

为关键决策反向生成 ADR：

```markdown
# ADR-001: 选择 structure-security 作为安全框架

## 状态
已采用（2024-XX-XX）

## 背景
<为什么需要这个决策>

## 决策
<选择了什么>

## 后果
### 正面
- ...
### 负面
- ...

## 替代方案
- 方案 A：...
- 方案 B：...
```

**产出**：`docs/adr/0001-*.md` / `0002-*.md` / ...

### 第 4 步：时序图（关键业务流程）

为核心业务流程画时序图：

```bash
# 找 Controller
find . -name "*Controller.java"

# 读关键方法，画出时序图
```

**产出**：`docs/flows/<flow-name>.md`

### 第 5 步：归档到 archive

```bash
# 把这些反向文档作为"初始状态"归档
mkdir -p changes/archive/0000-initial-state/docs
cp -r docs/architecture docs/adr docs/flows changes/archive/0000-initial-state/docs/
```

## 产出物

- `docs/architecture/`（C4 图）
- `docs/adr/`（ADR）
- `docs/flows/`（时序图）
- `changes/archive/0000-initial-state/docs/`（归档）

## 完成标准

- 核心模块有 C4 图
- 关键决策有 ADR
- 主要流程有时序图

## 关联

- 调用方：`legacy-onboarding`
- 前置：`codebase-audit`
- Wiki：`wiki/_common/documentation.md` `wiki/_common/architecture.md`
