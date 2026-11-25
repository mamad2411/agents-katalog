---
name: "product-designer-skills-os"
display_name: "产品设计 Skills OS"
display_name_en: "Product Designer Skills OS"
description: "产品设计与独立产品构建：判断下一步、整理上下文、梳理假设、概念模型、原型验证、交互原型、设计评审、意图检查、定位发布及复盘。用户明确指定任务时直接执行相应能力。"
description_zh: "以最高风险未知驱动的产品设计与学习闭环。"
description_en: "An uncertainty-driven product design and learning skill network."
version: "0.1.0"
author: "jiayuewangjavy"
---

# Product Designer Skills OS · WorkBuddy

## 使用方式

默认按用户语言回复。保留原始技能中的方法、证据边界和决策责任。
此整合包已包含全部 10 个能力；它们是包内参考指令，不依赖另行安装的技能、Codex 插件、`$skill-name` 语法或特定 MCP 工具。

- 用户明确提出原型、评审、复盘等任务：只读取对应能力文件并执行，不强制经过完整流程。
- 用户不知道下一步做什么：先读取 @references/product-design-router.md，按最高风险未知选择一个主能力，必要时最多两个支持能力。
- 选中能力后读取下方对应文件；不要只报技能名称就结束。文件内的“调用 / route to”表示读取并应用本包对应指令，不是调用不存在的工具。
- 需要跨能力闭环时读取 @references/LOOP-CONTRACT.md；不要一次性加载所有资料。
- 参考指令含英文时，按其含义执行并用用户语言交付，不要求用户懂英文。

## 能力索引

- 产品设计路由（`product-design-router`）：@references/product-design-router.md
- 产品上下文（`product-context`）：@references/product-context.md
- 机会与假设地图（`opportunity-and-assumption-map`）：@references/opportunity-and-assumption-map.md
- 概念模型设计（`conceptual-model-design`）：@references/conceptual-model-design.md
- 原型验证问题（`prototype-question`）：@references/prototype-question.md
- 交互原型（`interactive-prototype`）：@references/interactive-prototype.md
- 设计判断评分（`design-judgment-scorecard`）：@references/design-judgment-scorecard.md
- 产品意图检查（`intent-preservation-check`）：@references/intent-preservation-check.md
- 定位与发布假设（`position-and-launch-hypothesis`）：@references/position-and-launch-hypothesis.md
- 学习闭环复盘（`learning-loop-readout`）：@references/learning-loop-readout.md

## WorkBuddy 执行约定

- 只使用当前会话实际可用的文件、浏览、代码执行或连接器能力。先检查已有附件和工作区；不得假装已访问 Figma、GitHub、分析后台或其他服务。
- 相对链接以所属参考文件所在目录解析；补充资料已包含在本包的 references 目录内。
- 复用已有产品上下文；无既有文件且允许写入时，使用工作区中的 `.agents/product-context.md`。无法写文件时在对话提供可复制的 Markdown，并明确尚未保存。
- 交互原型优先复用项目现有实现；无项目时可用无外部依赖的 HTML/CSS/JavaScript。无代码执行能力时提供可保存的代码、操作说明及“尚未运行验证”的限制。
- 模拟数据、假设和真实观察分开标注。生成原型不等于验证了需求；没有参与者测试时不得宣称通过可用性验证。
- 跨会话不假定自动记忆。输出已知、产出、学到什么、决策变化、下一个未知，供用户保存并在下一会话提供。
- 仍按用户已授权范围执行；不把 workshop 练习视为授权发布、发消息、付款、删除或修改线上系统。
