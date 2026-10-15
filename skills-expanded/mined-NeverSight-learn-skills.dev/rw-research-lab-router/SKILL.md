---
name: rw-research-lab-router
description: |
  根据科研任务、数据和运行环境选择可用工具；没有预设本地 research-lab 也能工作。 Use when the user asks for “科研任务用哪个工具”、“帮我选科研工具”、“这个 repo 有用吗”, or requests the rw-research-lab-router workflow. Runs without a private local workspace or preset research-lab; use user-provided material and bundled public-source methods.
---

# RW Research Lab Router

根据科研任务、数据和运行环境选择可用工具；没有预设本地 research-lab 也能工作。

## 启动

1. 读取 `references/standalone.md`、`references/method.md` 和 `references/standards.md`。
2. 读取用户本轮提供的材料；没有材料时，只完成当前证据允许的部分。
3. 需要规则判断时检索 `references/atoms.jsonl`；遇到相似任务时读取 `references/cases.md`。
4. 需要选择方法或工具时读取 `references/domain-guide.md`，并使用 `assets/worksheet.md` 组织交付。
5. 读取 `references/acceptance.md`。`references/behavior-tests.json` 只用于测试，不作为用户任务事实。
6. 当前文献、API、报告规范和期刊要求可能变化时，打开 `references/source-map.md` 中的官方链接核验并记录日期。

## 工作阶段

1. 确认任务、输入格式、数据敏感性、运行环境、交付物和可接受失败方式。
2. 把任务拆成发现、获取、去重、提取、评价、综合、统计、可视化或写作检查。
3. 盘点当前可用的本机命令、Python 包、API、网页工具和用户提供的仓库。
4. 检查许可证、认证、费用、限流、维护状态、数据外发和可复现性。
5. 选择一个首选工具和一个回退方案，并设计最小样本测试。
6. 运行或描述最小测试，记录版本、命令、结果、失败和停止条件。

## 运行规则

- 先从任务和输入选择工具，不从已有 repo 名称选择任务。
- 本地 research-lab 是可选集成，不是运行前提。
- 代码能安装或编译不等于实时 API、模型或数据源可用。
- 工具输出必须保留输入、版本、参数和来源。
- 发现工具和系统综述数据库覆盖不能混为一谈。
- API 元数据可能不完整，关键标识符要交叉核验。
- 限流、认证、费用和服务条款要在批量运行前检查。
- 敏感数据优先选择本地或批准的处理路径。
- 批量任务先用最小样本测试字段和失败处理。
- 选择工具时同时计算人工复核成本。
- 仓库知名度、星标和最近提交不能单独证明适合。
- 没有合适工具时，输出可执行的人工流程而不是硬选。

## 输出

- 首选工具、回退和选择理由。
- 环境、许可证、隐私和费用要求。
- 最小测试、结果和停止条件。

## 停止条件

- 没有运行证据时，不声称工具当前可用。
- 不在未获授权的平台上传敏感研究数据。
- 不因缺少某个本地目录而停止工具路由。
- 不自动安装、登录、付费或修改生产环境。

## 独立运行

- 默认不读取私人工作区、个人语料目录或预设 research-lab。
- 用户提供的文件、文本、链接和数据是当前任务输入，不是安装依赖。
- 网络不可用时，使用 Skill 内的稳定方法继续；需要当前事实的部分标记为待核验。
- 本包内其他科研 Skill 存在时可以接续；单独安装时直接返回下一步说明，不停止当前任务。

## 来源纪律

- 把用户材料、公开来源、当前推断和未知事项分开。
- 报告规范只检查报告透明度，不自动证明设计质量。
- 公开来源摘要保存在 Skill 内；需要版本、费用、政策、API 或期刊现状时回到官方页面。
- 不生成不存在的论文、数据、DOI、工具运行结果或期刊要求。
