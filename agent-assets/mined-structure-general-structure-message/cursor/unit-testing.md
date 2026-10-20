---
description: |
triggers:
  - 写测试
  - 补测试
  - 跑测试
  - 单测
  - 单元测试
  - write test
  - UT
  - 测试用例
role: tester
priority: high
category: testing
stack: _common
alwaysApply: false
---


# 单元测试

> 为新代码编写单元测试并验证覆盖率。与 `coding` 技能并行执行。

## 前置条件

- 至少有一项编码任务完成（`tasks.md` 中有 `- [x]` 项）

## 分层测试策略

| 层级 | 范围 | 工具 | 覆盖要求 |
|---|---|---|---|
| **单元测试** | 函数级、类级 | Jest / JUnit / pytest | 行覆盖 ≥ 80%，分支 ≥ 70% |
| **集成测试** | 跨模块、跨服务 | Testcontainers / Supertest | 关键路径 100% |
| **E2E 测试** | 端到端用户场景 | Playwright / Cypress | 核心业务流程 100% |

## 测试替身决策树

```
被测代码依赖什么？
   ├─ 纯函数 / 纯计算 → 无替身
   ├─ 外部 HTTP 服务 → mock（如 MSW / WireMock）
   ├─ 数据库 → Testcontainers（真实 DB，不用 H2）
   ├─ 消息队列 → Testcontainers 或内存实现
   ├─ 文件系统 → 临时目录
   └─ 时间 / 随机数 → 注入 Clock / Seed
```

## 执行步骤

### 第 1 步：读被测代码

理解业务逻辑、输入输出、边界条件、异常路径。

### 第 2 步：读测试 Wiki

MUST Read：`wiki/_common/testing-strategies.md`
按需 Read：`wiki/<stack>/tester.md`

### 第 3 步：设计测试用例

每个函数 MUST 覆盖：
- **正常路径**：典型输入 → 预期输出
- **边界条件**：空值、最大值、最小值、边界字符
- **异常路径**：非法输入、外部依赖失败、并发冲突

### 第 4 步：编写测试

- 命名：`should<Expected>When<Condition>` 或 `test<What>_<Condition>`
- 结构：Arrange / Act / Assert（Given / When / Then）
- 每个测试 MUST 独立运行，无顺序依赖

### 第 5 步：跑测试 + 覆盖率

```bash
# Java
mvn clean test jacoco:report
# Node
npm test -- --coverage
# Python
pytest --cov --cov-report=html
```

### 第 6 步：分析覆盖率

行覆盖 ≥ 80%，分支覆盖 ≥ 70%，关键路径 100%。

不达标 → 回到第 3 步补充用例。**不允许降低阈值**。

## 产出物

- 单元测试代码
- 覆盖率报告（HTML 或 CLI 输出）

## 完成标准

- 所有新增代码有对应测试
- 覆盖率达标
- 测试全部通过
- 测试独立于执行环境（本地 / CI 表现一致）

## 关联

- 并行：`coding`
- 后续：`ci-gate`
- Wiki：`wiki/_common/testing-strategies.md`
