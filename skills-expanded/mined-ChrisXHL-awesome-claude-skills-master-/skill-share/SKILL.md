---
name: skill-share
description: 一项使用 Rube 自动在 Slack 上共享新创建的 Claude 技能，以实现无缝团队协作和技能发现的技能。
license: Complete terms in LICENSE.txt
---

## 何时使用此技能

当您需要执行以下操作时使用此技能：
- **创建新的 Claude 技能** 具有适当的结构和元数据
- **生成技能包** 准备分发
- **自动共享创建的技能** 到 Slack 频道以提高团队可见性
- **验证技能结构** 在共享之前
- **打包和分发** 技能给您的团队

此外，在以下情况下也可以使用此技能：
- **用户说他想创建/分享他的技能**

此技能非常适合：
- 作为团队工作流程的一部分创建技能
- 构建需要技能创建 + 团队通知的内部工具
- 自动化技能开发流程
- 带有团队通知的协作技能创建

## 关键特性

### 1. 技能创建
- 创建具有 SKILL.md 的结构合理的技能目录
- 生成标准化 scripts/、references/ 和 assets/ 目录
- 自动生成带有必需元数据的 YAML frontmatter
- 强制命名约定 (hyphen-case)

### 2. 技能验证
- 验证 SKILL.md 格式和必需字段
- 检查命名约定
- 确保打包前元数据的完整性

### 3. 技能打包
- 创建可分发的 zip 文件
- 包含所有技能资产和文档
- 打包前自动运行验证

### 4. 通过 Rube 集成 Slack
- 自动将创建的技能信息发送到指定的 Slack 频道
- 共享技能元数据 (名称、描述、链接)
- 发布技能摘要以供团队发现
- 提供技能文件的直接链接

## 工作原理

1. **初始化**: 提供技能名称和描述
2. **创建**: 使用适当的结构创建技能目录
3. **验证**: 验证技能元数据的正确性
4. **打包**: 将技能打包成可分发的格式
5. **Slack 通知**: 技能详情发布到您团队的 Slack 频道

## 示例用法

```
当您要求 Claude 创建一个名为 "pdf-analyzer" 的技能时：
1. 创建带有 SKILL.md 模板的 /skill-pdf-analyzer/
2. 生成结构化目录 (scripts/, references/, assets/)
3. 验证技能结构
4. 将技能打包为 zip 文件
5. 发布到 Slack: "New Skill Created: pdf-analyzer - Advanced PDF analysis and extraction capabilities"
```

## 与 Rube 集成

此技能利用 Rube 进行：
- **SLACK_SEND_MESSAGE**: 将技能信息发布到团队频道
- **SLACK_POST_MESSAGE_WITH_BLOCKS**: 共享丰富的格式化技能元数据
- **SLACK_FIND_CHANNELS**: 发现用于技能公告的目标频道

## 要求

- 通过 Rube 连接 Slack 工作区
- 对技能创建目录的写入访问权限
- 用于技能创建脚本的 Python 3.7+
- 用于技能通知的目标 Slack 频道
