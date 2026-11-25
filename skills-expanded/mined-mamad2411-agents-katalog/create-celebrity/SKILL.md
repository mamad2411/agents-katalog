---
name: create-celebrity
slug: create-celebrity
author: 你的名字
description: 根据名人的特点和行为创建自定义AI技能
version: 1.0.0
tags: [名人, 人格, 蒸馏]
icon: ⭐
color: '#ff6b6b'
commands:
  - name: create-celebrity
    description: 根据名人的特点创建自定义AI技能
    usage: /create-celebrity
  - name: list-celebrities
    description: 列出所有名人技能
    usage: /list-celebrities
  - name: delete-celebrity
    description: 删除名人技能
    usage: /delete-celebrity {slug}
  - name: celebrity-rollback
    description: 回滚到之前的版本
    usage: /celebrity-rollback {slug} {version}

files:
  - path: prompts/intake.md
    description: 名人信息收集对话
  - path: prompts/celebrity_analyzer.md
    description: 名人性格和风格提取
  - path: prompts/persona_builder.md
    description: 名人角色生成模板
  - path: prompts/merger.md
    description: 增量合并逻辑
  - path: prompts/correction_handler.md
    description: 对话纠正处理
  - path: tools/skill_writer.py
    description: 技能文件管理
  - path: tools/version_manager.py
    description: 版本存档和回滚
  - path: tools/text_parser.py
    description: 名人内容文本解析器
---

# 名人技能创建器

这个技能允许你根据名人的特点、行为和沟通风格创建自定义AI技能。它通过提取名人的本质，创建一个能够模仿他们说话和思考方式的AI技能。

## 工作原理

1. **信息收集**：收集关于名人的信息，包括他们的性格、沟通风格和任何可用的文本数据（采访、演讲、社交媒体帖子等）
2. **分析**：分析收集到的信息，提取关键性格特征和沟通模式
3. **技能生成**：创建一个体现这些特征和模式的自定义AI技能
4. **进化**：随着更多信息的获得，技能可以不断更新和完善

## 使用方法

1. 运行 `/create-celebrity` 开始技能创建过程
2. 按照提示提供关于名人的信息
3. 创建完成后，使用 `/{slug}` 与名人技能互动
4. 使用 `/list-celebrities` 查看所有创建的技能
5. 使用 `/delete-celebrity {slug}` 删除技能
6. 使用 `/celebrity-rollback {slug} {version}` 回滚到之前的版本

## 数据源

该技能可以分析各种类型的数据，以创建更准确的表现：
- 采访和演讲
- 社交媒体帖子
- 自传和传记
- 新闻文章和个人资料
- 对名人特点的直接描述

你提供的数据越多，名人技能就越准确。