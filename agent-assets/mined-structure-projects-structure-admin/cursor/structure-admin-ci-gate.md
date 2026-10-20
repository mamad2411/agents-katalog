---
description: |
triggers:
  - 提交
  - commit
  - 推送
  - push
  - 合并
  - merge
  - 提交代码
  - 保存
  - 打个点
  - checkpoint
role: devops
priority: high
category: ci
stack: _common
alwaysApply: false
---


# CI 门禁

> 提交代码的物理门禁。本地预检 + git hooks + CI 监控。
> 即使绕过其他 skills，本层也拦得住。

## 前置条件（MUST 全部满足）

1. **编码完成**：`tasks.md` 所有任务勾选
2. **测试通过**：本地测试全部通过
3. **评审完成**：`changes/proposals/<current>/review.md` 存在，无未解决的 MUST fix

## 分级检查

### MUST 检查（任何提交都必须通过）

- commit-msg 格式（Conventional Commits）
- 分支名（`feat-*` / `fix-*` / `hotfix-*` / `release-*`）
- 编译通过（`mvn clean package -DskipTests` / `npm run build` / ...）
- 核心单测通过

### SHOULD 检查（hotfix 可降级）

- 覆盖率 ≥ 80%
- 全量测试通过
- lint 无 error
- 安全扫描通过

## 执行步骤

### 第 1 步：本地预检

```bash
# 分支检查
git branch --show-current | grep -E "^(feat|fix|hotfix|release)-"

# 编译
mvn clean package -DskipTests  # 或 npm run build / pytest

# 核心单测
mvn test  # 或 npm test / pytest
```

### 第 2 步：生成 commit message

调用 `git-commit` 子技能：
- 按 Conventional Commits 生成 `<type>(<scope>): <description>`
- 校验 commit-msg hook

### 第 3 步：提交

```bash
git commit -m "<message>"
```

### 第 4 步：推送

```bash
git push origin <branch>
# 首次推送：
git push -u origin <branch>
```

### 第 5 步：监控远程 CI

- 追踪 CI 状态（GitHub Actions / GitLab CI / Jenkins）
- 失败 MUST 修复，不允许"先合并再说"

## Hotfix 快速通道

紧急 hotfix 时可降级 SHOULD 检查：
- 跳过覆盖率检查
- 跳过全量测试（仅跑核心单测）
- 事后 24h 内补跑完整 CI

MUST 检查任何情况都不可跳过。

## 完成标准

- commit-msg hook 通过
- 编译通过
- 核心单测通过
- 远程 CI 通过
- 推送成功

## 关联

- 前置：`coding` `unit-testing` `expert-review`
- 后续：`deployment-verification`
- 子技能：`git-commit`
- Wiki：`wiki/_common/git.md` `wiki/_common/ci-cd-pipeline.md`
- 物理拦截：`_common/checks/commit-msg.sh`
