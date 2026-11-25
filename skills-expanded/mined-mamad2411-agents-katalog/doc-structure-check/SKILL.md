---
name: doc-structure-check
description: This skill should be used when checking, validating, or creating ZEGO documentation structure. Triggered by queries like "check document structure", "validate doc structure", "is this document complete", "document structure review", or when creating new Overview, ReleaseNote, RunDemo, QuickStart, FunctionGuide, ClientAPI, or FAQ documents.
version: 1.0.0
---

# 文档结构检查

本技能用于检查 ZEGO 文档的完整性和结构规范。支持多种文档类型的结构验证。

## 检查原则

站在完全没用过 ZEGO 产品的用户角度，审核文档结构是否清晰、完整，是否容易理解。

## 支持的文档类型

| 文档类型 | 说明 | 结构标准文件 |
|---------|------|-------------|
| **Overview** | 产品概述 | `references/overview.md` |
| **ReleaseNote** | 发布日志 | `references/release-note.md` |
| **RunDemo** | 跑通示例代码 | `references/run-demo.md` |
| **QuickStart** | 快速开始 | `references/quick-start.md` |
| **FunctionGuide** | 功能指南 | `references/function-guide.md` |
| **ClientAPI** | 客户端 API | `references/client-api.md` |
| **FAQ** | 常见问题 | `references/faq.md` |

## 检查流程

### 1. 识别文档类型

确定待检查的文档类型。根据文档标题、目录结构、内容特征判断：

- **Overview**: 以"产品介绍"、"概述"开头，包含产品架构图、核心功能列表
- **ReleaseNote**: 包含版本号、发布日期、更新内容分类
- **RunDemo**: 包含环境准备、源码获取、运行步骤
- **QuickStart**: 强调时间（如"5分钟实现"），有集成 SDK 步骤
- **FunctionGuide**: 以功能命名（如"推流"、"美颜"），有实现原理说明
- **ClientAPI**: 以函数/方法命名，有函数签名、参数说明
- **FAQ**: 问句形式标题，按问题组织内容

### 2. 按需加载结构标准

**重要：仅加载当前检查的文档类型对应的参考文件。**

根据识别出的文档类型，使用 Read 工具读取对应的参考文件：

| 文档类型 | 加载命令 |
|---------|---------|
| Overview | `Read references/overview.md` |
| ReleaseNote | `Read references/release-note.md` |
| RunDemo | `Read references/run-demo.md` |
| QuickStart | `Read references/quick-start.md` |
| FunctionGuide | `Read references/function-guide.md` |
| ClientAPI | `Read references/client-api.md` |
| FAQ | `Read references/faq.md`|

### 3. 逐项检查验证

对照结构标准，检查：

1. **必需章节是否存在** - 列出缺失的必需章节
2. **章节内容是否完整** - 检查内容是否满足要求
3. **格式是否规范** - 检查是否使用正确的组件（如 Steps、折叠面板）
4. **内容质量** - 检查是否有配图、代码示例是否完整

### 4. 输出检查结果

按照标准格式输出检查结果：

- ✅ 结构完整（当所有必需章节都存在时）
- ❌ 缺失章节（列出缺失章节及建议）
- ⚠️ 章节内容不足（列出内容不足的章节及改进建议）
- ⚠️ 其他问题（格式、链接、术语等问题）

## 特殊检查项

### 图片检查

- 简介/概述章节是否配有配图
- 架构说明是否有架构图
- 示例代码说明是否有运行效果截图

### 链接检查

- 相关文档链接是否有效
- API 链接是否正确
- 控制台链接是否准确

### 代码示例检查

- 代码示例是否完整
- 是否有关键参数说明
- 是否有预期效果描述

### 术语检查

- 是否使用统一的术语（AppID 非 App Id）
- 中英文是否混用得当
- 技术术语是否准确

## Additional Resources

### Reference Files

每种文档类型都有独立的结构标准文件，**按需加载**对应的文件：

- **`references/overview.md`** - Overview（产品概述）结构标准
- **`references/release-note.md`** - ReleaseNote（发布日志）结构标准
- **`references/run-demo.md`** - RunDemo（跑通示例代码）结构标准
- **`references/quick-start.md`** - QuickStart（快速开始）结构标准
- **`references/function-guide.md`** - FunctionGuide（功能指南）结构标准
- **`references/client-api.md`** - ClientAPI（客户端 API）结构标准
- **`references/faq.md`** - FAQ（常见问题）结构标准

## 使用示例

**用户**: 检查这个文档结构是否完整 [文档内容为 RunDemo 类型]

**Claude**:
1. 识别文档类型为 RunDemo
2. **仅加载** `references/run-demo.md`
3. 对照标准检查各章节
4. 输出 RunDemo 结构检查结果

**用户**: 这个 API 文档结构可以吗 [文档内容为 ClientAPI 类型]

**Claude**:
1. 识别文档类型为 ClientAPI
2. **仅加载** `references/client-api.md`
3. 检查函数签名、参数说明、代码示例等
4. 输出 ClientAPI 结构检查结果
