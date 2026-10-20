---
description: |
triggers:
  - 热修复
  - hotfix
  - 紧急上线
  - 线上bug
  - 紧急修复
  - emergency fix
role: devops
priority: critical
category: deployment
stack: _common
alwaysApply: false
---


# 热修复快速通道（Hotfix）

> 线上紧急 bug 快速修复上线。**跳过完整 SDLC，但 MUST 保留质量门禁**。
> 6 步流程：分支 → 修复 → 快速 CI → 灰度 → 全量 → 复盘。

## 前置条件

- 线上确认存在紧急 bug（影响用户 / 资金 / 安全）
- 用户已确认走 hotfix 通道（跳过完整 SDLC）

## 执行步骤

### 第 1 步：创建 hotfix 分支

```bash
# MUST 从 main/master 拉分支，NOT develop
git checkout main
git pull origin main
git checkout -b hotfix-{version}-{brief}

# 例：hotfix-1.2.1-login-crash
```

**约束**：
- MUST 从 `main` / `master` 拉分支（生产代码基线）
- MUST NOT 从 `develop` 拉分支（develop 可能有未发布功能）
- 分支名 MUST `hotfix-{version}-{brief}`

### 第 2 步：最小修复 + 单测

```bash
# 仅修复必要代码，MUST NOT 顺手重构
# ... 修改代码 ...

# MUST 补充 / 更新单测覆盖修复点
npm test -- --grep "{修复点}"
# 或 mvn test -Dtest={X}Test
```

**约束**：
- 最小化改动范围，仅修复 bug
- MUST 补充单测覆盖修复点
- MUST NOT 顺手重构 / 改无关代码

### 第 3 步：快速 CI（ci-gate 缩减版）

调用 `ci-gate` 走 hotfix 快速通道：

```bash
# MUST 检查（不可跳过）
git branch --show-current | grep -E "^hotfix-"
npm run build  # 或 mvn clean package -DskipTests
npm test       # 或 mvn test（核心单测）

# SHOULD 检查（hotfix 可降级）
# - 跳过覆盖率检查
# - 跳过全量测试
# - MUST 安全扫描（不可跳过）
npm audit  # 或 mvn org.owasp:dependency-check:check
```

**约束**：
- MUST 检查任何情况都不可跳过（编译 + 核心单测 + 安全扫描）
- SHOULD 检查可降级（覆盖率 / 全量测试）
- 事后 24h 内 MUST 补跑完整 CI

### 第 4 步：灰度发布（deployment-verification 灰度模式）

调用 `deployment-verification` 灰度模式：

```bash
# 灰度发布（MUST 用户确认）
# 例：先灰度 10% 流量
kubectl rollout canary --percentage=10
# 或 docker tag + 部分节点更新
```

**灰度验证**：
- 灰度流量健康检查通过
- 关键指标无异常（错误率 / 延迟 / QPS）
- 灰度观察期 ≥ 15 分钟

**MUST 用户确认全量发布后才继续。**

### 第 5 步：全量发布

```bash
# 全量发布（MUST 用户确认）
kubectl rollout deployment {x} --percentage=100
# 或 docker compose up -d
```

**全量验证**：
- 健康检查全部通过
- 日志无新 ERROR
- 监控指标正常

### 第 6 步：事后复盘（retrospective.md）

写入 `changes/proposals/<id>/retrospective.md`：

```markdown
# Hotfix 事后复盘

| 字段 | 值 |
|---|---|
| Hotfix ID | hotfix-{version}-{brief} |
| 触发时间 | YYYY-MM-DD HH:MM |
| 影响范围 | <受影响用户 / 业务> |
| 修复版本 | X.Y.Z |
| 修复人 | <user> |
| 上线时间 | YYYY-MM-DD HH:MM |

## 根因分析

<bug 根本原因，5 Why 分析>

## 修复方案

<修复内容说明>

## 预防措施

- <措施 1：如增加监控告警>
- <措施 2：如补充单测>
- <措施 3：如改进流程>

## 改进项

- [ ] 24h 内补跑完整 CI
- [ ] 补充回归测试用例
- [ ] 更新故障应急预案
- [ ] <其他改进项>
```

## 完成标准

- hotfix 分支已合并回 `main` / `master`（MUST）和 `develop`（SHOULD）
- 全量发布成功，健康检查通过
- retrospective.md 已写入
- 改进项已记录

## 下一步

- 成功 → 归档变更提案到 `changes/archive/`
- 补跑完整 CI（24h 内）
- 跟进改进项

## 关联

- 前置：`ci-gate`（快速通道）
- 相关：`deployment-verification`（灰度 / 全量）/ `rollback`（失败时回滚）
- Wiki：`wiki/_common/git.md` `wiki/_common/error-handling.md`
