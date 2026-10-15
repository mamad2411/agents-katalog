---
name: fullstack-dev-flow
description: 全栈项目开发流程管理。初始化开发团队，按照 调研需求→评审需求→设计方案→编写代码→测试代码→部署运行 的标准流程进行开发。自动创建项目开发日志目录，维护 todolist，每个任务独立文件夹存储方案文档。
metadata:
  author: evan
  version: "1.0.0"
  domain: project-management
  triggers: 全栈开发, 项目初始化, 开发流程, 团队协作, 前后端项目, 新项目, 开发日志, 任务管理, init project, new project, start development, dev flow, task management, sprint planning
  role: project-manager
  scope: development-workflow
  output-format: mixed
  globs:
    - "**/dev-logs/**"
    - "**/todolist.md"
---

# 全栈项目开发流程管理

项目开发全流程管理 skill，覆盖从需求调研到部署上线的完整生命周期。通过结构化的开发日志和任务文档，确保每个 AI agent 都能快速理解上下文并高效协作。

## When to Use This Skill

- 用户要启动一个新的前后端项目
- 用户说"初始化项目"、"新建项目"、"开始开发"
- 用户需要按流程管理开发任务
- 用户提到"开发日志"、"任务管理"、"团队协作"
- 用户要求按 调研→评审→设计→编码→测试→部署 流程工作

## 核心开发流程

```
1. 调研需求 (Research)     → 收集和分析需求，输出需求文档
2. 评审需求 (Review)       → 评审需求可行性，确认优先级和范围
3. 设计方案 (Design)       → 技术方案设计，架构设计，API 设计
4. 编写代码 (Implement)    → 按方案编码实现
5. 测试代码 (Test)         → 单元测试、集成测试、E2E 测试
6. 部署运行 (Deploy)       → 构建、部署、验证上线
```

## 项目目录结构

当用户启动新项目时，在项目根目录创建以下开发日志结构：

```
dev-logs/                          # 开发日志根目录
├── todolist.md                    # 全局任务清单（核心索引文件）
├── project-overview.md            # 项目概览（技术栈、架构、团队）
├── TASK-001-<任务名>/             # 每个任务一个独立文件夹
│   ├── requirement.md             # 需求文档
│   ├── design.md                  # 设计方案
│   ├── implementation.md          # 实现记录（关键决策、代码路径）
│   ├── test-plan.md               # 测试计划与结果
│   └── changelog.md               # 变更日志
├── TASK-002-<任务名>/
│   └── ...
└── archive/                       # 已完成任务归档
```

## 初始化流程

当用户要求初始化项目时，执行以下步骤：

### Step 1: 收集项目信息

向用户确认以下信息：
- 项目名称和简要描述
- 技术栈选择（前端框架、后端框架、数据库等）
- 主要功能模块划分
- 团队角色需求（前端、后端、测试等）

### Step 2: 创建开发日志目录

```bash
mkdir -p dev-logs/archive
```

### Step 3: 创建 todolist.md

todolist.md 是整个项目的核心索引文件，格式如下：

```markdown
# 项目名称 - 任务清单

> 最后更新: YYYY-MM-DD

## 项目信息
- 技术栈: xxx
- 仓库地址: xxx

## 任务状态说明
- [ ] 待开始 | [~] 进行中 | [x] 已完成 | [-] 已取消

## 任务列表

| ID | 任务名称 | 阶段 | 状态 | 负责人 | 文档路径 | 备注 |
|----|---------|------|------|--------|---------|------|
| TASK-001 | xxx | 调研 | [ ] | - | `TASK-001-xxx/` | - |
```

### Step 4: 创建 project-overview.md

记录项目整体信息，包括：
- 项目背景和目标
- 技术架构图（文字描述）
- 技术栈详情
- 目录结构约定
- 开发规范和约定

### Step 5: 初始化团队

根据项目需求，建议创建以下 agent 角色：

| 角色 | 职责 | 建议 subagent_type |
|------|------|-------------------|
| 需求分析师 | 需求调研、文档编写 | general-purpose |
| 架构师 | 技术方案设计、架构评审 | Plan |
| 前端开发 | 前端编码实现 | general-purpose |
| 后端开发 | 后端编码实现 | general-purpose |
| 测试工程师 | 测试用例编写、执行测试 | general-purpose |

## 任务生命周期管理

### 创建新任务

1. 在 todolist.md 中添加任务条目
2. 创建任务文件夹 `dev-logs/TASK-XXX-<任务名>/`
3. 创建 requirement.md 记录需求

```bash
mkdir -p dev-logs/TASK-XXX-<任务名>
```

### 任务阶段流转

每个任务按以下阶段流转，每个阶段完成后更新 todolist.md 中的阶段字段：

#### 1. 调研需求阶段
- 创建/更新 `requirement.md`
- 内容：需求背景、用户故事、验收标准、边界条件
- 完成标志：需求文档评审通过

#### 2. 评审需求阶段
- 在 `requirement.md` 中追加评审记录
- 内容：可行性分析、风险点、工作量评估、优先级确认
- 完成标志：需求确认，无阻塞问题

#### 3. 设计方案阶段
- 创建/更新 `design.md`
- 内容：技术方案、数据模型、API 设计、前端组件设计、依赖关系
- 完成标志：方案评审通过

#### 4. 编写代码阶段
- 创建/更新 `implementation.md`
- 内容：实现思路、关键代码路径、重要决策记录、遇到的问题及解决方案
- 完成标志：代码编写完成，自测通过

#### 5. 测试代码阶段
- 创建/更新 `test-plan.md`
- 内容：测试用例、测试结果、bug 记录、覆盖率报告
- 完成标志：所有测试通过

#### 6. 部署运行阶段
- 更新 `changelog.md`
- 内容：部署步骤、环境配置、上线验证清单、回滚方案
- 完成标志：线上验证通过

### 完成任务

1. 更新 todolist.md 状态为 `[x]`
2. 将任务文件夹移动到 `dev-logs/archive/`（可选）

## AI Agent 协作规范

### 接手任务时

每个 AI agent 在开始工作前必须：

1. 读取 `dev-logs/todolist.md` 了解全局进度
2. 进入对应任务文件夹，阅读所有已有文档
3. 理解当前任务所处阶段
4. 在对应阶段文档中记录工作开始

### 工作过程中

- 及时更新任务文档，记录关键决策和变更
- 遇到阻塞问题记录在文档中，标注 `[BLOCKED]`
- 完成阶段性工作后更新 todolist.md

### 交接任务时

- 确保所有文档是最新状态
- 在 implementation.md 中记录未完成事项，标注 `[TODO]`
- 更新 todolist.md 中的状态和备注

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| todolist 模板 | `references/todolist-template.md` | 初始化项目时 |
| 项目概览模板 | `references/project-overview-template.md` | 初始化项目时 |
| 需求文档模板 | `references/requirement-template.md` | 创建新任务时 |
| 设计文档模板 | `references/design-template.md` | 进入设计阶段时 |
| 实现记录模板 | `references/implementation-template.md` | 进入编码阶段时 |
| 测试计划模板 | `references/test-plan-template.md` | 进入测试阶段时 |
| 变更日志模板 | `references/changelog-template.md` | 部署阶段或任务完成时 |

## Constraints

### MUST DO
- 每个任务必须有独立文件夹和完整文档
- todolist.md 必须保持实时更新
- 阶段流转必须有明确的完成标志
- 所有关键决策必须记录在文档中
- agent 接手任务前必须先阅读已有文档

### MUST NOT DO
- 不要跳过流程阶段（除非用户明确要求）
- 不要在没有需求文档的情况下直接编码
- 不要修改其他任务的文档（除非有明确关联）
- 不要删除任何历史记录，只追加不覆盖
