---
name: international-ai-deploy
description: WorkBuddy技能 - 帮助用户配置和部署国际AI模型（GPT、Claude、Gemini）。当用户需要添加国际AI模型、配置API代理、或设置自定义AI模型时使用此技能。
---

# International AI Deploy - WorkBuddy技能

## 功能简介

帮助用户一键配置国际AI模型。用户只需提供 `baseurl`（API端点）、`provider`（提供商）和 `api-key`（API密钥），即可自动生成AI模型配置文件。

## 触发关键词

当用户说以下内容时，使用此技能：
- "添加GPT模型"
- "配置Claude API"
- "部署国际AI模型"
- "添加自定义模型"
- "配置模型代理"
- "我想用GPT"
- "添加OpenAI"
- "配置Anthropic"

## 使用流程

### 步骤1：收集用户配置信息

向用户收集以下信息：

| 参数 | 说明 | 示例 |
|------|------|------|
| baseurl | API端点地址 | `https://api.openai.com/v1` |
| provider | 模型提供商 | `openai`, `anthropic`, `google`, `custom` |
| api-key | API密钥 | `sk-xxxxxx` |
| model-name | 模型名称（可选） | `gpt-4o`, `claude-3-opus` |

### 步骤2：生成配置

根据用户提供的provider类型，生成对应的配置：

**OpenAI配置：**
```json
{
  "models": [{
    "id": "openai/gpt-4o",
    "name": "GPT-4o",
    "vendor": "OpenAI",
    "apiKey": "${api-key}",
    "url": "https://api.openai.com/v1/chat/completions",
    "maxInputTokens": 128000,
    "maxOutputTokens": 4096
  }]
}
```

**Anthropic配置：**
```json
{
  "models": [{
    "id": "anthropic/claude-3-sonnet",
    "name": "Claude 3 Sonnet",
    "vendor": "Anthropic",
    "apiKey": "${api-key}",
    "url": "https://api.anthropic.com/v1/messages",
    "maxInputTokens": 200000,
    "maxOutputTokens": 4096
  }]
}
```

**Google配置：**
```json
{
  "models": [{
    "id": "google/gemini-1.5-pro",
    "name": "Gemini 1.5 Pro",
    "vendor": "Google",
    "apiKey": "${api-key}",
    "url": "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent",
    "maxInputTokens": 1000000,
    "maxOutputTokens": 8192
  }]
}
```

**自定义配置：**
```json
{
  "models": [{
    "id": "custom/${model-name}",
    "name": "${model-display-name}",
    "vendor": "${provider}",
    "apiKey": "${api-key}",
    "url": "${baseurl}/chat/completions",
    "maxInputTokens": 128000,
    "maxOutputTokens": 4096
  }]
}
```

## 支持的模型

### OpenAI (GPT系列)
- 端点: `https://api.openai.com/v1`
- 支持模型: gpt-4o, gpt-4-turbo, gpt-3.5-turbo

### Anthropic (Claude系列)
- 端点: `https://api.anthropic.com/v1/messages`
- 支持模型: claude-3-opus, claude-3-sonnet, claude-3-haiku

### Google (Gemini系列)
- 端点: `https://generativelanguage.googleapis.com/v1`
- 支持模型: gemini-1.5-pro, gemini-1.5-flash

### 自定义/代理服务
- SiliconFlow: `https://api.siliconflow.cn/v1`
- OpenRouter: `https://openrouter.ai/api/v1`
- 任意兼容OpenAI API的服务

## 配置保存位置

- 项目目录: `.codebuddy/models.json`
- 用户目录: `~/.config/codebuddy/models.json`

## 示例对话

**用户**: 我想添加GPT-4o
**技能**: 请提供您的OpenAI API密钥

**用户**: sk-xxxxxx
**技能**: ✅ 已成功配置GPT-4o！配置已保存到 `.codebuddy/models.json`

---

**版本**: 1.0.0  
**作者**: hangtiger  
**许可证**: MIT
