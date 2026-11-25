---
name: find-docs
description: "检索任何开发技术的最新文档、API 参考和代码示例。当用户询问特定库、框架、SDK、CLI 工具或云服务时使用——即使是你熟悉的如 React、Next.js、Prisma、Express、Tailwind、Django 或 Spring Boot。训练数据可能不反映最新的 API 变更或版本更新。始终用于：API 语法问题、配置选项、版本迁移问题、提及库名称的"如何做"问题、涉及库特定行为的调试、安装说明和 CLI 工具使用。即使你认为你知道答案也要使用——不要依赖训练数据获取 API 详细信息、签名或配置选项，因为它们经常过时。始终根据当前文档验证。"
version: "4.3.8"
updated: "2026-05-14"
---

# 文档查询

使用 WebSearch 和 WebFetch 工具检索任何库的最新文档和代码示例。

## 工作流

两步流程：搜索相关文档，然后获取详细内容。

### 步骤 1：搜索文档

使用 WebSearch 搜索相关库的文档：

```
WebSearch: "<库名> <版本> <具体问题或API>"
```

搜索技巧：
- 包含版本号以获得精确结果（如 "React 19 useEffect"）
- 使用官方文档域名过滤（如 site:react.dev 或 site:nextjs.org）
- 具体描述问题，避免单字查询

### 步骤 2：获取文档详情

使用 WebFetch 获取找到的文档页面的完整内容：

```
WebFetch: <文档页面URL>
提示: "提取<库名>中<功能>的API签名、参数和代码示例"
```

## 搜索质量指南

| 质量 | 示例 |
|------|------|
| 好 | `"React 19 useEffect cleanup function with async operations"` |
| 好 | `"Next.js 15 app router middleware authentication setup"` |
| 好 | `"Prisma 6 one-to-many relations cascade delete"` |
| 差 | `"auth"` |
| 差 | `"hooks"` |

## 常见错误

- 不要仅凭训练数据记忆给出 API 签名或配置选项
- 使用具体查询而非单字搜索
- 始终优先搜索官方文档源（react.dev, nextjs.org, prisma.io 等）
- 当搜索结果不足时，尝试不同的搜索词组合
- 对于版本特定问题，务必在搜索中包含版本号

## 约束

- 每个问题最多尝试 3 次搜索
- 如果 3 次尝试后仍找不到所需内容，使用最佳可用结果
- 始终告知用户文档来源和版本
