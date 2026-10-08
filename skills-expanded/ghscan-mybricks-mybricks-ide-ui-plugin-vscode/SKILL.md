---
name: mybricks-assistant-skill
description: 开发 MyBricks 以及指导 MyBricks Mcp 使用方式 的助手，任何与 MyBricks 有关的操作建议先使用此技能
disable-model-invocation: true
---

## 重要前提
做任何事情之前，先查询 MyBricks Mcp 中有什么工具，本 Skill 需要你清楚地查询过 MyBricks Mcp 中有什么工具才可以进行。

## 背景知识
MyBricks 是一个低代码搭建系统，通过 MyBricks Mcp 我们可以使用 MyBricks 生成强大的前端UI和逻辑。

这个 Skill 教会你如何与用户协同完成 MyBricks 开发。

在 MyBricks 设计器中，一个项目包含多个页面，用户可以聚焦到任意元素（页面/组件）上进行精确的手动搭建修改。

而我们可以针对页面级别进行UI的生成。

## 工作流
我们需要对用户的核心诉求进行分类，不同的类型有不同的工作流，

但是，任何情况下，我们都应当事先了解了当前项目的情况，用户聚焦在哪里，才能进行下一步操作。

### UI生成
涵盖了一句话需求生成UI、根据附件（图片/设计稿/原型文件）生成UI等。

核心是根据「组件配置文档」+ 「UI搭建指南」来生成页面
所以需要遵循以下流程
  1. 分析需求阶段，最终目的是拿到「设计风格指南」和「结合和内容需求」
    1.1 调用 MCP 工具获取当前可用的所有组件摘要列表，了解当前可用的组件
    1.2 分析用户需求，完成页面结构和内容的需求生成，返回一个「结合和内容需求」，需求文档生成时必须参考 [references/requirement-template-creative.md](references/requirement-template-creative.md)
    1.3 分析用户的UI需求，使用工具获取「设计风格指南」，为需求提供设计风格
  2. 生成UI阶段，根据「组件配置文档」+ 「UI搭建指南」，生成UI
    2.1 据需求，调用 MCP 工具获取「组件配置文档」和「UI搭建指南」，用于指导UI生成
    2.2 根据「UI搭建指南」的格式生成 actionsString 参数（注意一行一个action json），通过 开始标记 -> 生成UI / 分批生成UI -> 结束生成，调用MCP生成UI工具进行生成
      2.2.1 开始生成
      2.2.2 根据「UI搭建指南」的格式生成 actionsString 参数（注意一行一个action json），使用这个参数调用生成UI工具
      2.2.3 结束生成

## 注意事项
生成UI / 修改UI 都必须是一个完整的事务，如果需要批量生成，注意合理的进行分批。