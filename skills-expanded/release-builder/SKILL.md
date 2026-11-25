---
name: release-builder
description: Prepare builds, packages, smoke tests and release evidence for the actual project ecosystem. External publishing requires explicit authorization; a local build is not a release.
---

# 发布技能 (release-builder)

## Purpose

把已验证代码转成可追溯、可复现、可回滚的交付物，并把本地发布准备与真实发布明确分开。

## Trigger

- 开发完成，需要构建、打包、产物冒烟或发布准备报告。
- 用户要求部署或上线前检查。
- 仓库已有可识别的构建生态、版本来源或交付目标。

## Required context

- 当前路线、交付契约、风险级别和审查结果。
- 仓库构建/打包配置、锁文件、CI 或 Wrapper 命令。
- 目标平台、产物形式、发布环境和回滚要求。
- 对真实推送、部署或上线的明确授权（如要执行）。

## Workflow

1. 从仓库文件识别生态和原生命令，不假设 npm 或固定技术栈。
2. 检查版本、依赖锁定、构建入口、部署配置和审查门禁。
3. 执行敏感信息与隐私审计，输出只包含 secret 名称和注入位置。
4. 构建/打包后对最终产物执行与生态匹配的安装、启动或接口冒烟。
5. 记录命令、结果、产物路径、失败/跳过项和回滚路径，复用仍适用的证据；真实发布后同步现状入口的版本/环境和回读依据。
6. 只有取得明确授权时才执行真实发布、推送或上线。

## Output

- 发布准备状态与证据。
- 隐私/敏感信息审计结果。
- 构建、打包、产物冒烟和部署路径。
- 发布说明、阻塞项、授权记录与回滚方案。

## Stop or escalate

- 真实秘密暴露、用户数据处理不清或构建失败：阻止发布。
- 找不到可复现构建入口：标记阻塞，不声明可发布。
- 必要门禁缺失时记录具体缺口；用户已接受的例外保留范围和证据，不伪造通过。一般例外不能覆盖未授权外部动作、真实秘密暴露或构建失败。
- 未获得明确授权：只完成本地发布准备，不执行外部状态变更。
- 未授权部署不阻塞仍在授权范围内的构建、打包、产物冒烟和发布报告；只有用户目标必须真实上线时才请求授权并等待。

## References

执行前读取 [stage-contract.md](references/stage-contract.md)。
