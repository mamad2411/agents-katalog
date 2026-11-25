---
name: ask-user-demo
description: Use when demonstrating the AskUserQuestion tool capabilities or testing question-based user interactions
---

# AskUserQuestion 工具演示

## 概述

演示如何使用内置工具 AskUserQuestion 与用户进行结构化问答交互。这个工具非常适合收集用户偏好、澄清需求或引导决策。

## 何时使用

- 需要从用户那里收集结构化信息
- 用户请求包含多个可能的选项
- 需要引导用户做出明确选择
- 想要提供预定义选项同时保留自定义输入

## 核心模式

### 基本结构

```
AskUserQuestion({
  questions: [
    {
      question: "你的问题？",
      header: "短标签",
      options: [
        { label: "选项1", description: "选项1说明" },
        { label: "选项2", description: "选项2说明" }
      ],
      multiSelect: false  // true 表示可多选
    }
  ]
})
```

### 最佳实践

1. **问题要具体明确** - 避免模糊的问法
2. **提供 2-4 个选项** - 太多选项会增加认知负担
3. **描述要有价值** - 解释每个选项的含义和影响
4. **合理使用多选** - 当多个选项可以共存时启用

## 快速参考

| 参数 | 说明 |
|------|------|
| `question` | 完整问题文本 |
| `header` | 短标签（最多12字符） |
| `options` | 2-4个选项数组 |
| `multiSelect` | 是否允许多选 |
| `label` | 选项显示文本 |
| `description` | 选项详细说明 |

## 示例场景：选择编程学习路径

```json
{
  "questions": [
    {
      "question": "你想学习哪个编程领域？",
      "header": "学习领域",
      "options": [
        { "label": "前端开发", "description": "HTML/CSS/JavaScript，构建用户界面" },
        { "label": "后端开发", "description": "服务器、数据库、API 开发" },
        { "label": "移动开发", "description": "iOS/Android 应用开发" },
        { "label": "数据科学", "description": "数据分析、机器学习、AI" }
      ],
      "multiSelect": false
    },
    {
      "question": "你的经验水平如何？",
      "header": "经验水平",
      "options": [
        { "label": "完全新手", "description": "从未写过代码" },
        { "label": "初级 (Recommended)", "description": "了解基础概念，需要系统学习" },
        { "label": "中级", "description": "能独立完成项目，想提升技能" }
      ],
      "multiSelect": false
    },
    {
      "question": "你希望的学习方式？（可多选）",
      "header": "学习方式",
      "options": [
        { "label": "视频教程", "description": "跟随视频一步步学习" },
        { "label": "实战项目", "description": "通过做项目来学习" },
        { "label": "阅读文档", "description": "系统阅读官方文档和书籍" }
      ],
      "multiSelect": true
    }
  ]
}
```

## 用户输入处理

用户回答后会返回类似这样的结构：

```json
{
  "学习领域": "前端开发",
  "经验水平": "初级",
  "学习方式": ["视频教程", "实战项目"]
}
```

## 常见错误

| 错误 | 修复方法 |
|------|----------|
| 选项太多（5+个） | 精简到2-4个核心选项 |
| 问题太长 | 简化问题，细节放在 description |
| 没有推荐标记 | 在合适选项后加 "(Recommended)" |
| header 超过12字符 | 缩短为更简洁的标签 |
