---
name: tgi
description: |
  文生图工具 - 使用阿里云 DashScope API 生成图片。支持千问(Qwen-Image)和万相(Wan)系列模型。

  **务必主动触发此 Skill 的场景：**
  - 用户说"生成一张图片"、"帮我画"、"文生图"、"用AI画图"
  - 用户提到 AI 绘画、图像生成、文字转图片
  - 用户描述一个场景并想要看到对应的图片
  - 用户使用 /tgi 命令
  - 用户需要创建任何类型的图片（头像、风景、插画、写实照片等）

  **支持的模型：**
  - 千问系列：qwen-image-2.0-pro, qwen-image-2.0-max, qwen-image-2.0, qwen-image-max, qwen-image-plus
  - 万相系列：wan2.7-image-pro, wan2.7-image, wan2.6-image, wan2.6-t2i, wan2.5-t2i-preview
---

# TGI (Text Generate Image) Skill

基于阿里云 DashScope API 的统一文生图工具，支持千问和万相两大模型系列。

## 执行流程

1. **读取 usage.md**：首先读取 `references/usage.md` 了解详细用法
2. **检查工具**：确认 `tgi` 命令可用
3. **构建命令**：根据用户需求选择合适的模型和参数
4. **执行生成**：运行 tgi 命令生成图片

## 模型选择建议

| 需求场景 | 推荐模型 |
|---------|---------|
| 通用图像生成 | qwen-image-2.0-pro（默认） |
| 4K 超高清 | wan2.7-image-pro |
| 组图/连环画 | wan2.7-image-pro（支持 sequential 模式） |
| 需要反向提示词 | 千问系列（qwen-image-*) |

## 注意事项

- **API Key 配置**：需要设置 `DASHSCOPE_API_KEY` 环境变量或在 `~/.tgi.env` 配置
- **模型能力差异**：
  - 万相系列支持思考模式(thinking)和组图(sequential)
  - 千问系列支持反向提示词(negative)和 Prompt 改写(extend)
  - 仅 wan2.7-image-pro 支持 4K 分辨率
- **参数互斥**：思考模式(thinking)与组图模式(sequential)不能同时开启
- **尺寸格式**：支持 `1K`/`2K`/`4K` 缩写或 `宽*高` 格式（如 `1024*1024`）

## 错误处理

| 错误场景 | 解决方案 |
|---------|---------|
| API Key 无效/未设置 | 设置 `DASHSCOPE_API_KEY` 环境变量或创建 `~/.tgi.env` 文件 |
| 模型不支持 | 检查模型名称是否正确，参考支持的模型列表 |
| 尺寸不支持 | 检查模型支持的尺寸范围，qwen-max/plus 仅支持5种预设尺寸 |
| 4K 不支持 | 仅 wan2.7-image-pro 支持 4K，切换模型 |
| 宽高比超出范围 | 调整图片宽高比到模型支持范围内 |
| 组图与思考冲突 | 同时开启两个参数时出错，关闭其中之一 |

## 参考文档

详细命令用法、参数说明、尺寸对照表和示例请参考 `references/usage.md`。
