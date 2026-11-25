# Jina Web Analyzer (Jina 网页分析)

## 技能描述
由周医生的科研馆 | 深度云创科技团队开发，支持输入任意网址 URL，自动分析并总结网页内容。

## 使用方式

### 命令格式
```
分析网页：[URL]
```

### 示例
```
分析网页：https://example.com/article
分析网页：https://arxiv.org/abs/2401.12345
```

## 核心功能

1. **Jina 抓取**: 通过 r.jina.ai 将网页转换为 Markdown 格式
2. **AI 总结**: 使用 AI 模型分析并总结网页内容
3. **中文输出**: 最终结果用中文呈现

## 工作流程

1. 接收用户输入的 URL
2. 调用 Jina API (`https://r.jina.ai/{URL}`) 抓取网页内容
3. AI 阅读并整理为 Markdown 格式
4. 输出中文总结

## 输出格式

- 完整 Markdown 格式网页内容
- 中文总结摘要

## 环境要求

- Jina API 访问权限（Bearer Token）
- LLM 模型访问权限（支持 gpt-oss:120b-cloud 或同类模型）

## 注意事项

- URL 必须是完整的有效链接
- 支持 HTTPS/HTTP协议
- 自动处理网页内容提取

## 来源
由周医生科研馆 | 深度云创科技团队开发
