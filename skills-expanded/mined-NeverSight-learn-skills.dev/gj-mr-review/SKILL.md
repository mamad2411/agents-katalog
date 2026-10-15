---
name: gj-mr-review
description: Review GitLab merge requests for workflow compliance, code risks, test and documentation gaps, and merge readiness. Use when an MR is opened, marked ready, has review feedback, or needs a decision-ready report before a human chooses whether to merge.
---

# GJ 合并请求审阅

## 工作流程

1. 读取 MR 标题、描述、关联 Issue、diff、Pipeline 结果和评论。
2. 检查 MR 必填章节：关联 Issue、变更摘要、自测、风险、回滚、数据库/配置变化、AI 使用。
3. 根据 `.gj/workflow.yml` 匹配变更路径。
4. 从 `.gj/context.yml` 加载相关模块上下文。
5. 检查文档影响：
   - MR 描述或 Skill 结果包含文档决策表，含路径、动作、触发事实、阶段/状态和确认人/
     跟进项；
   - 动作是 `create`、`update`、`no-change` 或 `follow-up`，且每个 `follow-up` 都有
     Issue、负责人和期限；
   - 决策表与实际 diff 和行为变化一致；
   - 已考虑产品、交互、API/事件、数据库、架构/ADR、模块规则、测试基线、发布和运行
     状态影响；
   - 机器契约/migration、说明文档、实现和测试一致，并列出可执行与说明路径；
   - 新当前事实文档使用语义文件名和必填元数据，不使用模板名；
   - GitLab Solution/Task/Test Issue 没有被当成仓库长期文档的替代品。
6. 检查版本追溯：Issue、MR 和功能文档使用同一目标版本/Milestone；普通功能 MR 不在
   没有明确发布范围时创建 Tag 或提升 manifest 版本。发布准备 MR 要核验最终 SemVer、
   发布说明路径、包含工作、测试和回滚证据。
7. 审阅代码中的缺陷、回归、测试缺口和文档缺口。
8. 检查合并就绪度：MR 已打开且非草稿、head Pipeline 成功、讨论已解决、flow 证据有效、
   必要时已关联 Issue、测试证据完整、回滚已准备。
9. 先按严重级别列出发现，摘要放在后面。
10. 停在人工决策门。不得批准、合并、部署、强制操作、跳过 CI 或绕过未解决讨论。

## 输出格式

```markdown
## MR 审阅

问题：

流程策略：

风险路径：

目标版本/版本追溯：

测试缺口：

文档缺口：

文档决策核验：

需要更新的上下文：

合并就绪度：

待确认问题：

摘要：
```

## 参考资料

- 需要首次 MR 审阅示例时读取 `references/demo-run.md`。
- 需要真实 MR 和 Pipeline 证据时读取 `references/gitlab-readiness.md`。
