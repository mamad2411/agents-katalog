---
description: |
triggers:
  - 写流水线
  - 加 CI
  - 加 CD
  - GitHub Actions
  - 构建流水线
  - 发布流水线
  - ci/cd
  - workflow
  - 加 workflow
role: devops
priority: high
category: ci
stack: _common
alwaysApply: false
---


# CI/CD 流水线设计

> 按生态三件套模板生成 GitHub Actions 流水线。**MUST 手动触发，禁止自动发布**。

## 前置条件

- 项目已有 Dockerfile（`dockerfile-writing` 技能产出）
- 已确定镜像仓库 / npm scope / Maven 仓库

## 执行步骤

### 第 1 步：确定流水线需求

**MUST 询问用户**：

```
Q1: 项目类型？
    a) 后端 Java（需要 build-and-push + release-maven）
    b) 前端（需要 build-and-push）
    c) npm 组件库（需要 publish-npm）
    d) 全栈（三件套都需要）

Q2: 镜像仓库？
    默认：registry.cn-hangzhou.aliyuncs.com/structured

Q3: 是否发布到 Maven Central / npmjs？
    a) 是
    b) 否（仅构建 Docker 镜像）
```

### 第 2 步：生成对应 workflow

按用户选择生成对应的 `.github/workflows/*.yml` 文件。

**模板来源**：`wiki/_common/ci-cd-pipeline.md` 中的三件套模板。

**关键替换**：
- `structure-${{ inputs.module }}` → 实际项目路径
- `structure-${{ inputs.component }}` → 实际组件路径
- Secrets 名称 → 保持不变（约定俗成）

### 第 3 步：配置 Secrets

**MUST 告诉用户需要配置哪些 Secrets**：

```bash
# 通过 gh CLI 设置
gh secret set ALIYUN_ACR_USERNAME --body "..."
gh secret set ALIYUN_ACR_PASSWORD --body "..."
gh secret set OSSRH_USERNAME --body "..."        # Java 项目
gh secret set OSSRH_PASSWORD --body "..."        # Java 项目
gh secret set GPG_PRIVATE_KEY --body "..."       # Java 项目
gh secret set GPG_PASSPHRASE --body "..."        # Java 项目
gh secret set NPM_TOKEN --body "..."             # npm 项目
```

### 第 4 步：验证流水线

```bash
# 本地验证 yaml 语法
yamllint .github/workflows/*.yml

# 提交并推送
git add .github/workflows/
git commit -m "ci(workflows): 新增三件套流水线"
git push

# 手动触发验证
gh workflow run build-and-push.yml -f module=<module> -f version=<version>
```

### 第 5 步：监控运行

```bash
gh run list
gh run view <run-id>
gh run view <run-id> --log  # 查看日志
```

## 关键约束（MUST 遵守）

- ❌ **MUST NOT** 使用 `on: release: published` 自动触发发布
- ✅ **MUST** 所有发布用 `workflow_dispatch` 手动触发
- ✅ **MUST** 使用缓存（Maven / npm）加速构建
- ✅ **MUST** 镜像打 `version` + `latest` 双 tag
- ✅ **MUST** npm 发布校验 scope 和 private

## 产出物

- `.github/workflows/build-and-push.yml`
- `.github/workflows/release-maven.yml`（Java 项目）
- `.github/workflows/publish-npm.yml`（npm 组件）
- Secrets 配置说明

## 完成标准

- 流水线 yaml 语法正确
- 手动触发成功
- 产物（镜像 / 包）成功推送

## 关联

- 前置：`dockerfile-writing`
- 后续：`gh-pr-workflow`（通过 PR 合并流水线变更）
- Wiki：`wiki/_common/ci-cd-pipeline.md` `wiki/_common/github-workflow.md`
