---
name: tiered-learning-path
description: |
  当用户询问"我应该从哪个项目开始"、"如何系统化提升编码技能"或"有没有适合初学者的项目"时调用此 skill。不适用于：纯信息查询、已有明确学习路径的用户、需要团队协作指导的场景。关键 trigger 信号：分级、难度级别、学习路径、初学者/中级/高级。
source_book: App Ideas Collection Florin Pop
source_project: florinpop17/app-ideas
source_chapter: Projects / Tier table
tags: [learning-path, tiered-structure, progressive-learning]
related_skills: ["portfolio-ready-output"]
---

# SKILL.md - Tiered Learning Path（分级学习路径）

## R (Reading) - 原文引用

> "Projects are divided into three tiers based on the knowledge and experience required to complete them."
>
> "| Tier | Developer Profile |"
> "| :--: | --- |"
> "| 1 | Developers in the early stages of their learning journey. Those who are typically focused on creating user-facing applications. |"
> "| 2 | Developers at an intermediate stage of learning and experience. They are comfortable in UI/UX, using development tools, and building apps that use API services. |"
> "| 3 | Developers who have all of the above, and are learning more advanced techniques like implementing backend applications and database services. |"

## I (Interpretation) - 方法论骨架

**核心思想**：将项目按难度分为三个层级（Beginner → Intermediate → Advanced），每个层级对应不同的开发者画像。这种分级方法帮助学习者根据自身水平选择合适的项目，避免过早接触过于复杂的内容或停留在舒适区。

**关键要素**：
1. **Tier 1 (Beginner)**: 面向学习初期的开发者，专注于创建用户界面应用
2. **Tier 2 (Intermediate)**: 面向中级学习者，熟练使用 UI/UX、开发工具和 API 服务
3. **Tier 3 (Advanced)**: 面向高级学习者，学习后端应用和数据库服务等高级技术

## A1 (Past Application) - 书中作者用过的案例

App Ideas Collection 本身就是一个实际案例，展示了如何将 89 个项目按难度分为三个层级：
- **Tier 1**: 35 个项目（Bin2Dec, Calculator, Weather App 等）
- **Tier 2**: 33 个项目（Book Finder App, To-Do App, Markdown Previewer 等）
- **Tier 3**: 21 个项目（Chat App, Instagram Clone, NASA Exoplanet Query 等）

这种分级方法在实际项目集合中已经应用并验证有效，97,038+ stars 也证明了这种方法的有效性。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户是初学者，不知道从哪里开始学习编程
- 用户完成了几个简单项目，想知道下一步该做什么
- 用户想系统化提升编码技能，而不是随机选择项目
- 用户想评估自己当前的水平处于哪个阶段

**与相邻 skill 的区分**：
- 与 `portfolio-ready-output` 的区别：tiered-learning-path 关注**学习路径的选择**，而 portfolio-ready-output 关注**项目的职业价值**。两者可以组合使用：先根据难度选择项目，再确保该项目适合放入作品集。

## E (Execution) - 可执行步骤

1. **评估用户当前水平**
   - 询问用户已有的编程经验（语言、框架、项目经历）
   - 判断用户处于 Beginner / Intermediate / Advanced 哪个阶段
   - 完成标准：基于用户回答给出唯一的层级归属（Tier 1/2/3），并列出支撑该判断的具体经历证据

2. **推荐对应层级的项目**
   - Tier 1: 推荐 35 个 Beginner 项目中的 2-3 个（如 Calculator, Weather App, Notes App）
   - Tier 2: 推荐 33 个 Intermediate 项目中的 2-3 个（如 To-Do App, Markdown Previewer, GitHub Profiles）
   - Tier 3: 推荐 21 个 Advanced 项目中的 2-3 个（如 Chat App, Instagram Clone, NASA Exoplanet Query）
   - 完成标准：推荐数量为 2-3 个且全部来自用户所属层级的项目清单，每个推荐附一句应覆盖的知识点

3. **提供渐进式建议**
   - 完成当前层级的项目后，尝试下一个层级的 1-2 个项目
   - 不要跳跃太大，确保每一步都有挑战性但可完成
   - 完成标准：给出的进阶路线满足"相邻层级递进"，不存在跳过整个层级的安排，或跳级时有明确的风险说明与补偿练习

4. **追踪进度**
   - 记录用户已完成的项目
   - 定期回顾是否真正提升了技能（能否独立完成更复杂的项目）
   - 完成标准：已有完成项目清单，且回顾时能对"能否独立完成更复杂项目"给出是/否结论及下一步动作

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 用户已经有明确的学习路径或课程大纲
- 用户需要团队协作指导（app-ideas 缺少这方面的内容）
- 用户需要测试和质量保障指导（app-ideas 完全没有提到 TDD）
- 纯信息查询（如"Calculator 项目怎么做"）

**作者的盲点**：
- app-ideas 只解决了"不知道要构建什么"的问题，但没有提供系统性的学习方法论
- 缺少测试指导、进度追踪机制和协作指导
- 假设学习者独立完成项目，没有考虑真实团队环境
