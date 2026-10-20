---
description: |
triggers:
  - 拆分模块
  - 微服务划分
  - DDD 设计
  - 模块划分
  - 服务拆分
  - 拆服务
  - bounded context
  - 领域划分
  - 模块依赖
role: architect
priority: high
category: architecture
stack: _common
alwaysApply: false
---


# 模块拆分（DDD / 微服务）

> 按 DDD 或单体规范拆分模块。**MUST 先识别 bounded context，禁止凭直觉拆分**。

## 前置条件

- 已有变更提案（`changes/proposals/<current>/proposal.md`）
- 明确项目形态（DDD 7+1 / 单体 4 模块）

## 执行步骤

### 第 1 步：识别 Bounded Context（MUST）

通过业务分析识别限界上下文：

```
业务领域
   ├─ 用户上下文（User Context）：用户 / 组织 / 角色 / 权限
   ├─ 订单上下文（Order Context）：订单 / 订单项 / 支付
   ├─ 商品上下文（Product Context）：商品 / 类目 / 库存
   └─ ...
```

**关键问题**（MUST 与用户确认）：
- 业务边界在哪里？
- 哪些概念属于同一上下文？
- 上下文之间如何通信（同步 / 异步 / 共享数据库）？

### 第 2 步：确定拆分粒度

| 粒度 | 说明 | 适用 |
|---|---|---|
| **粗粒度** | 1 个上下文 = 1 个服务 | 小型项目 |
| **中粒度** ⭐ | 1 个上下文 = 1 个服务，内部 7+1 模块 | 中型项目（推荐） |
| **细粒度** | 1 个上下文拆为多个服务 | 大型项目 |

### 第 3 步：生成模块结构

#### DDD 7+1 多模块（推荐用于新业务中心）

```
structure-{X}/
├── structure-{X}-dependencies/        # 父 POM
├── structure-{X}-common/              # DTO / VO / Query / enums / exception
├── structure-{X}-domain/              # Entity / Repository 接口 / DomainService
├── structure-{X}-infra/               # RepositoryImpl / RepositoryDelegate
├── structure-{X}-repository-mybatis/  # PO / Mapper / MybatisPlusDelegate / Flyway
├── structure-{X}-application/         # I{X}Service / {X}ServiceImpl / {X}Assembler
├── structure-{X}-interfaces/          # Controller（api/ + open/）
└── structure-{X}-boot/                # 启动类 + application.yaml
```

**模块依赖方向**（MUST 遵守）：
```
common → domain → infra → repository-mybatis
                     ↑
application → domain + infra
interfaces → application
boot → all
```

#### 单体 4 模块（老项目 / 小型项目）

```
structure-{X}/
├── {X}-api/           # 接口定义（DTO / VO / Feign 客户端）
├── {X}-biz/           # 业务实现（Service / Manager）
├── {X}-common/        # 通用类（Utils / Constants）
└── {X}-dependencies/  # 父 POM
```

### 第 4 步：生成模块依赖图

用 mermaid 或 markdown 表格说明模块依赖关系：

```markdown
## 模块依赖图

| 模块 | 依赖 | 被依赖 | 职责 |
|---|---|---|---|
| common | 无 | domain, infra, application, interfaces | DTO/VO/枚举/异常 |
| domain | common | infra, application | 领域模型 + 领域服务 |
| infra | domain, common | application | 仓储实现防腐层 |
| repository-mybatis | domain, common | infra | MyBatis 持久化 |
| application | domain, infra | interfaces | 应用服务 |
| interfaces | application | boot | 控制器 |
| boot | all | — | 启动 |
```

### 第 5 步：定义模块间依赖规则

MUST 明确：
- **允许**：`application → domain`，`interfaces → application`
- **禁止**：`domain → infra`，`domain → application`，`interfaces → domain`
- **禁止**：跨服务的直接数据库访问（MUST 通过 API / Feign）

### 第 6 步：写入 design.md

把模块拆分结果写入 `changes/proposals/<current>/design.md`：

```markdown
## 模块拆分

### Bounded Context
<识别结果>

### 模块结构
<目录树>

### 模块依赖
<依赖图>

### 关键决策
<决策 1 / 决策 2 / ...>
```

## 产出物

- 模块依赖图
- 每个模块的职责说明
- 模块间依赖规则
- design.md 更新

## 完成标准

- bounded context 经用户确认
- 模块结构符合 DDD 7+1 或单体 4 模块规范
- 依赖方向无循环
- 依赖规则明确

## 关联

- 前置：`requirement-analysis`
- 后续：`scaffold-project`（按拆分结果初始化项目）或 `coding`
- Wiki：`wiki/_common/architecture.md` `wiki/<stack>/ddd-patterns.md`
