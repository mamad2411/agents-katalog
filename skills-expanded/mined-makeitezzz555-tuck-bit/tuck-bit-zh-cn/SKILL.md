---
name: tuck-bit-zh-cn
description: "TuckBit 是面向编程智能体的可移植技能，帮助选择适当的上下文、工具和验证步骤，而不牺牲正确性。"
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: zh-CN
---

# TuckBit — 简体中文

> 核心技能文件已翻译；技术参考资料暂时保留英文，并需要社区审核。

优化单位资源对应的正确且经过验证的结果，而不是单纯减少 token 数量。

四项默认能力：注册表、上下文、验证和预算。编排与指标为可选项。

## 标准工作流程

从用户的原始请求、实际可见的指令及已获授权的工具出发。保留全部约束、批准事项和必需检查。

1. 定义目标、约束、风险和停止条件；简单任务无需冗长计划。
2. 精准查找相关代码、文档或工具，只在依赖需要时扩大范围。
3. 优先使用宿主的原生工具发现机制；元数据仅供参考，绝不代表执行权限。
4. 小任务使用单个智能体；独立任务只有在明确责任和验收条件后才并行分配。
5. 先运行针对性测试，再对最终版本执行所有必需的集成及安全检查。
6. 提供可核验的变更、测试、风险与阻碍记录。使用检查点，不要无休止地轮询。

## 只加载相关参考资料

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## 必须遵守的边界

不得跳过安全检查、降低正确性、编造数据、读取凭据、绕过批准或执行未经授权的破坏性操作。权限始终由宿主管理。

**开发者预览版。安装本身并不能证明技能已被调用，也不能保证节省 token。**
