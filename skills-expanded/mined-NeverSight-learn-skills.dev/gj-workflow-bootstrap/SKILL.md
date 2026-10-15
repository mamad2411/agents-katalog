---
name: gj-workflow-bootstrap
description: Install and verify the GitLab AI workflow skeleton in a repository. Use when setting up labels, issue/MR templates, .gj workflow and context config, role ownership, docs/context, CI policy checks, CODEOWNERS, orchestrator skeletons, or preflight checks before writing workflow objects to GitLab.
---

# GJ 工作流初始化

## 工作流程

1. 任何 GitLab 写操作前先运行预检：
   - 缺少 `.gj/gitlab.local.json` 时运行
     `python scripts/gitlab_api.py configure --url <url> --project-id <id>`.
   - 运行 `python scripts/gitlab_api.py doctor`，在不输出 Token 的前提下比较
     `git remote origin` 与 GitLab API 项目路径。
   - 确认 `.gj/gitlab.local.json` 已忽略且未暂存。
   - 确认 GitLab Runner 可用；示例 Pipeline 优先使用 Docker executor。
   - 把缺失的 GitLab 权限记录为人工确认项。
2. 一次性安装所有可复用资产：
   - 在源码目录运行 `scripts/install_workflow.py --target <repo>`。
   - 只有本 Skill 已安装时，定位本 Skill 目录并运行
     `scripts/bootstrap_from_github.py --target <repo>`；它获取可信源码包并调用同一个
     非破坏式安装器。
   - 安装器返回退出码 `2` 时停止，并给出准确的手工 CI include 操作。Fast、Standard
     和 Hotfix 是运行时通道，不是安装版本。
3. 需要角色路由时，让 Maintainer 替换 `.gj/workflow.yml` 中的占位角色，并审阅
   `docs/standards/06-release-standard.md`。确认 `.gj/workflow.yml` 版本策略、Tag 格式、
   发布说明路径和 `docs/standards/13-versioning-standard.md`，不要添加通用 `VERSION`
   文件。确认 `.gj/doc-templates/` 作为工作流模板安装，项目事实目录没有通用模板文件。
4. 通过已配置 helper 或获准 GitLab connector 幂等创建标签、Milestone 和起始 Issue。
5. 按需根据 `.gj/workflow.yml` 指派由人负责的起始 Issue/MR；需要通知时添加
   `@username` 交接评论。
6. 运行本地校验。
7. 输出初始化摘要，列出已创建、已跳过、失败和需人工确认的项目。

## 输出格式

```markdown
## 初始化摘要

GitLab 项目：

已创建：

已跳过/已存在：

失败：

本地变更文件：

校验结果：

需要人工确认：

已安装到 `.gj/doc-templates/` 的文档模板：

发现的阻碍：
```

## 参考资料

需要具体首次运行示例时读取 `references/demo-run.md`。
