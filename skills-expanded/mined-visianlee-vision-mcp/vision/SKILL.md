---
name: vision
description: 多模型视觉桥接 — 让 DeepSeek 等纯文本模型获得看图能力。支持6个免费Provider自动Fallback：Gemini、硅基流动、智谱、月之暗面、魔搭、Intern-AI。7个专用工具：分析、OCR、对比、错误诊断、图表、UI评估、状态检查。
version: 1.1.0
author: 自定义Skill
triggers:
  - 当用户发送图片路径(.png/.jpg/.webp等)并要求分析时
  - 当用户说"看看这张图"、"分析这个截图"、"这张图是什么"时
  - 当用户要求对比两张截图/设计稿时
  - 当用户粘贴错误截图要求诊断时
  - 当用户发送架构图/流程图要求分析时
  - 当用户发送UI截图要求评估时
  - 当用户要求从图片提取文字(OCR)时
  - 当用户要求批量分析多张截图时
auto_trigger_patterns:
  - "\.(png|jpg|jpeg|webp|gif|bmp|svg|tiff|heic)\b"
  - "截图|图片|照片|设计稿|架构图|流程图|界面|报错截图|屏幕截图"
  - "看.*图|分析.*图|描述.*图|这张图|那个图|OCR|提取文字"
---

# Vision MCP Skill — 多模型视觉桥接

## 概述

当 Claude Code 使用 DeepSeek 等纯文本模型时，模型无法直接理解图片内容。本 Skill 通过 MCP Server 桥接到 **6 个免费视觉模型**，将图片转为详细文字描述后返回给主模型处理。

## 架构

```
用户发送图片
    ↓
Claude Code (DeepSeek 等纯文本模型)
    ↓ 检测到图片 → 调用 vision-mcp 工具
Vision MCP Server
    ↓ 按优先级自动选择Provider
Gemini → 硅基流动 → 智谱 → 月之暗面 → 魔搭 → Intern-AI
    ↓ 返回文字描述
主模型基于描述继续工作
```

## 可用工具

| 工具 | 用途 | 典型场景 |
|------|------|----------|
| `analyze_image` | 通用图片分析 | 截图、照片、设计稿 |
| `compare_images` | 两张图对比 | UI回归测试、设计稿vs实现 |
| `ocr_text` | 文字提取 | 扫描件、表格、手写笔记 |
| `diagnose_error` | 错误诊断 | 报错截图、堆栈跟踪 |
| `analyze_diagram` | 图表分析 | 架构图、流程图、UML |
| `analyze_ui` | UI评估 | 界面设计、可用性审查 |
| `check_vision` | 状态检查 | 查看Provider可用性 |

## 使用方式

### 基本用法

```
分析这张截图: /path/to/screenshot.png
用OCR提取文字: /path/to/scan.jpg
诊断这个错误截图: /path/to/error.png
分析这个架构图: /path/to/architecture.png
对比设计稿和实现: 设计稿/实现两张路径
检查视觉服务状态
```

### 批量分析

```
分析这个文件夹下的所有截图，输出功能和设计报告:
/path/to/screenshots/
```

### 指定Provider

```
用智谱分析这张图: /path/to/photo.jpg
用魔搭做OCR: /path/to/document.png
```

## 支持的Provider（全部免费）

| # | Provider | 模型 | 参数 | 国内直连 |
|---|----------|------|------|:--:|
| 1 | Google Gemini | gemini-2.5-flash | — | ❌ |
| 2 | 硅基流动 | Qwen3-VL-32B-Instruct | 32B | ✅ |
| 3 | 智谱AI | GLM-4V-Flash | — | ✅ |
| 4 | 月之暗面 | moonshot-v1-8k-vision | — | ✅ |
| 5 | 魔搭 | Qwen3-VL-235B-A22B | 235B | ✅ |
| 6 | Intern-AI | InternVL3.5-241B | 241B | ✅ |

**自动 Fallback 顺序**：Gemini → 硅基流动 → 智谱 → 月之暗面 → 魔搭 → Intern-AI

## 快速安装

### 1. 获取免费 API Key（任选一个即可，推荐多个）

| Provider | 获取地址 | 免费额度 |
|----------|----------|----------|
| Gemini | https://aistudio.google.com/apikey | 1500次/天 |
| 硅基流动 | https://siliconflow.cn | 注册送额度 |
| 智谱AI | https://open.bigmodel.cn | 永久免费 |
| 月之暗面 | https://platform.moonshot.cn | 3 RPM |
| 魔搭 | https://modelscope.cn | 2000次/天 |
| Intern-AI | https://chat.intern-ai.org.cn | 10 RPM |

### 2. 安装依赖

```bash
cd vision-mcp
npm install
```

### 3. 注册到 Claude Code

创建或编辑 `~/.mcp.json`：

```json
{
  "mcpServers": {
    "vision-mcp": {
      "command": "node",
      "args": ["/path/to/vision-mcp/index.js"],
      "env": {
        "GEMINI_API_KEY": "AIza...",
        "SILICONFLOW_API_KEY": "sk-...",
        "ZHIPU_API_KEY": "xxx...",
        "MOONSHOT_API_KEY": "sk-...",
        "MODELSCOPE_API_KEY": "ms-...",
        "INTERN_AI_API_KEY": "sk-..."
      }
    }
  }
}
```

> 💡 只配置你获取了 Key 的 Provider，未配置的会自动跳过。

### 4. 验证

```
检查视觉服务状态
```

看到可用 Provider 列表即安装成功。

## 自定义配置

编辑 `config.json` 可以：
- 启用/禁用特定 Provider
- 调整 Provider 优先级（数字越小越优先）
- 修改模型选择
- 关闭特定工具
- 调整缓存 TTL（默认7天）
- 添加自定义 OpenAI 兼容 API
