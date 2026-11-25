# Jina Web Crawler (Jina 网页爬虫)

## 技能描述
由周医生的科研馆 | 深度云创科技团队开发，支持输入任意网址 URL，自动整理并输出 Markdown 格式的网页内容。

## 使用方式

### 命令格式
```
爬取网页：[URL]
```

### 示例
```
爬取网页：https://example.com/article
爬取网页：https://github.com/trending
```

## 核心功能

1. **Jina 抓取**: 通过 r.jina.ai 将网页转换为 Markdown 格式
2. **内容整理**: 完整整理网页内容为结构化 Markdown
3. **原样输出**: 保持网页原始结构和内容

## 工作流程

1. 接收用户输入的 URL
2. 调用 Jina API (`https://r.jina.ai/{URL}`) 抓取网页内容
3. 输出完整 Markdown 格式内容

## 输出格式

- 完整 Markdown 格式网页内容（无总结，原样输出）

## 环境要求

- Jina API 访问权限（Bearer Token）
- LLM 模型访问权限（可选，用于内容整理）

## 注意事项

- URL 必须是完整的有效链接
- 输出为原始 Markdown 内容，不包含分析总结
- 与 Web Analyzer 的区别：本工具只提取内容，不进行分析

## 来源
由周医生科研馆 | 深度云创科技团队开发
